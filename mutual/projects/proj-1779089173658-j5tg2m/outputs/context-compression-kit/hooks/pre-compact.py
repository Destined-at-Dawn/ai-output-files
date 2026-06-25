#!/usr/bin/env python3
"""
PreCompact Hook v2 — 压缩前紧急检查点 + 保护清单
=================================================
Claude Code 在 context compaction 前自动触发本脚本。

核心功能：
- 解析 JSONL 对话记录，提取关键会话状态
- 生成九段式结构化检查点（写入磁盘）
- 返回 additionalContext（存活压缩，注入上下文）
- 保护清单：文件路径、行号、错误消息、关键决策永不丢失

来源：Anthropic Context Compaction Cookbook + Forge Code
"""

import json
import sys
import os
import re
from datetime import datetime


def read_stdin_json():
    try:
        raw = sys.stdin.read()
        if raw.strip():
            return json.loads(raw)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def parse_transcript(transcript_path, max_lines=300):
    """解析 JSONL 对话记录，提取最近的对话轮次"""
    if not transcript_path or not os.path.exists(transcript_path):
        return []
    messages = []
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            lines = []
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
                if len(lines) > max_lines * 2:
                    lines = lines[-max_lines:]
            for line in lines[-max_lines:]:
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except (IOError, OSError):
        pass
    return messages


def extract_session_state(messages):
    """从消息列表提取关键会话状态"""
    state = {
        "user_messages": [],
        "tool_calls": [],
        "files_modified": set(),
        "files_read": set(),
        "errors": [],
        "key_decisions": [],
        "recent_assistant": [],
        "file_line_refs": set(),
    }
    for msg in messages:
        msg_type = msg.get("type", "")
        role = msg.get("role", "")

        # 用户消息
        if role == "user" or msg_type == "human":
            content = msg.get("content", "")
            if isinstance(content, str) and content.strip():
                state["user_messages"].append(content[:500])
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        state["user_messages"].append(block.get("text", "")[:500])

        # 助手消息
        if role == "assistant" or msg_type == "assistant":
            content = msg.get("content", "")
            if isinstance(content, str) and content.strip():
                text = content[:300]
                state["recent_assistant"].append(text)
                if any(kw in text for kw in ["决策", "决定", "选择", "方案", "结论", "判断"]):
                    state["key_decisions"].append(text[:200])
                refs = re.findall(r'[\w/\\.-]+:\d+', text)
                state["file_line_refs"].update(refs[:10])
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        if block.get("type") == "text":
                            text = block.get("text", "")[:300]
                            state["recent_assistant"].append(text)
                            if any(kw in text for kw in ["决策", "决定", "选择", "方案", "结论"]):
                                state["key_decisions"].append(text[:200])
                            refs = re.findall(r'[\w/\\.-]+:\d+', text)
                            state["file_line_refs"].update(refs[:10])
                        elif block.get("type") == "tool_use":
                            tool_name = block.get("name", "")
                            tool_input = block.get("input", {})
                            state["tool_calls"].append(tool_name)
                            file_path = tool_input.get("file_path", "")
                            if file_path:
                                state["files_modified"].add(file_path)
                            if tool_name in ("Read", "read_project_file"):
                                read_path = tool_input.get("file_path", "")
                                if read_path:
                                    state["files_read"].add(read_path)

        # 工具结果中的错误
        if msg_type == "tool_result" or (role == "tool" and msg.get("is_error")):
            content = msg.get("content", "")
            if isinstance(content, str) and ("error" in content.lower() or "fail" in content.lower()):
                state["errors"].append(content[:300])

    return state


def build_checkpoint(state, cwd):
    """构建九段式结构化检查点"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.now().strftime("%Y-%m-%d")

    recent_user = state["user_messages"][-3:] if state["user_messages"] else []
    task_hint = recent_user[-1][:200] if recent_user else "（无法从对话中提取）"
    recent_asst = state["recent_assistant"][-5:] if state["recent_assistant"] else []

    tool_counts = {}
    for t in state["tool_calls"]:
        tool_counts[t] = tool_counts.get(t, 0) + 1
    tool_summary = ", ".join(f"{k}x{v}" for k, v in sorted(tool_counts.items(), key=lambda x: -x[1])[:10])

    files_modified = sorted(state["files_modified"])[:20]
    files_read = sorted(state["files_read"])[:10]
    key_decisions = state["key_decisions"][-5:] if state["key_decisions"] else []
    errors = state["errors"][-3:] if state["errors"] else []
    file_line_refs = sorted(state["file_line_refs"])[:15]

    lines = [
        "# Session Checkpoint",
        "",
        f"> Auto-generated by PreCompact hook v2 | {now}",
        f"> Working directory: {cwd}",
        "",
        "## 1/9 Current Task",
        f"Latest user request: {task_hint}",
        "",
    ]

    if recent_user:
        lines.append("## 2/9 Recent User Messages")
        for i, msg in enumerate(recent_user, 1):
            lines.append(f"{i}. {msg[:300]}")
        lines.append("")

    if recent_asst:
        lines.append("## 3/9 Recent Assistant Replies")
        for i, msg in enumerate(recent_asst, 1):
            lines.append(f"{i}. {msg[:300]}")
        lines.append("")

    if files_modified:
        lines.append("## 4/9 Modified Files (MUST re-read after compaction)")
        for f in files_modified:
            lines.append(f"- `{f}`")
        lines.append("")

    if files_read:
        lines.append("## 5/9 Read Files")
        for f in files_read[:10]:
            lines.append(f"- `{f}`")
        lines.append("")

    if key_decisions:
        lines.append("## 6/9 Key Decisions")
        for i, d in enumerate(key_decisions, 1):
            lines.append(f"{i}. {d}")
        lines.append("")

    if errors:
        lines.append("## 7/9 Error State")
        for e in errors:
            lines.append(f"- {e}")
        lines.append("")

    if file_line_refs:
        lines.append("## 8/9 File:Line References")
        for ref in file_line_refs:
            lines.append(f"- `{ref}`")
        lines.append("")

    if tool_summary:
        lines.append("## 9/9 Tool Usage Stats")
        lines.append(tool_summary)
        lines.append("")

    lines.extend([
        "## Recovery Instructions",
        "After compaction, read:",
        f"1. `.claude/session-checkpoint.md` (this file)",
        "2. Your CLAUDE.md / project instructions",
        "3. Resume from 'Latest user request' above",
        "4. Re-read 'Modified Files' to verify content",
        "",
    ])

    return "\n".join(lines)


def main():
    meta = read_stdin_json()
    transcript_path = meta.get("transcript_path", "")
    cwd = meta.get("cwd", os.getcwd())

    messages = parse_transcript(transcript_path, max_lines=300)
    state = extract_session_state(messages)

    # 写检查点到磁盘
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", cwd)
    checkpoint_path = os.path.join(project_dir, ".claude", "session-checkpoint.md")

    try:
        checkpoint_content = build_checkpoint(state, cwd)
        os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            f.write(checkpoint_content)
    except (IOError, OSError) as e:
        print(f"Warning: Failed to write checkpoint: {e}", file=sys.stderr)

    # 构建 additionalContext（存活压缩，< 10K chars）
    recent_user = state["user_messages"][-2:] if state["user_messages"] else []
    files_modified = sorted(state["files_modified"])[:10]
    key_decisions = state["key_decisions"][-3:] if state["key_decisions"] else []
    errors = state["errors"][-2:] if state["errors"] else []

    context_parts = [
        f"[PreCompact Checkpoint v2 saved at {datetime.now().strftime('%H:%M:%S')}]",
        f"Checkpoint: .claude/session-checkpoint.md",
    ]

    if recent_user:
        context_parts.append(f"Last user request: {recent_user[-1][:200]}")
    if files_modified:
        context_parts.append(f"Files modified (MUST re-read after compaction): {', '.join(files_modified[:5])}")
    if key_decisions:
        context_parts.append(f"Key decisions (preserve): {'; '.join(d[:100] for d in key_decisions[:3])}")
    if errors:
        context_parts.append(f"Errors (preserve): {'; '.join(e[:100] for e in errors[:2])}")

    context_parts.append("After compaction: read .claude/session-checkpoint.md to resume.")

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreCompact",
            "additionalContext": "\n".join(context_parts),
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
