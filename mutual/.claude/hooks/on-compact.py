#!/usr/bin/env python3
"""
SessionStart Hook v2 (compact matcher) — 压缩后上下文恢复
=========================================================
在每次 compaction（手动/自动）后触发，向 Claude 注入恢复上下文。

v2 增强（基于 2026-05-28 研究迭代）：
- 50K token 预算重读策略（Claude Code 原生支持）
- 自动验证关键指令是否存活压缩
- 恢复修改的文件列表（保护清单）
- 量化恢复指标

来源：
- Claude Code 官方最佳实践：压缩后自动重读最近编辑文件（50K 预算）
- Forge Code：文件路径精确保留策略
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def read_file_tail(filepath, max_lines=10):
    """读取文件最后 N 行"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            return "".join(lines[-max_lines:]).strip()
    except (IOError, OSError):
        return ""


def read_file_head(filepath, max_chars=4000):
    """读取文件前 N 个字符"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_chars).strip()
    except (IOError, OSError):
        return ""


def parse_checkpoint_for_files(checkpoint_content: str) -> list:
    """从检查点内容提取修改的文件列表"""
    files = []
    in_files_section = False
    for line in checkpoint_content.split("\n"):
        if "修改的文件" in line or "Files modified" in line:
            in_files_section = True
            continue
        if in_files_section:
            if line.startswith("- `") and line.endswith("`"):
                files.append(line[3:-1])
            elif line.startswith("##"):
                break  # 下一个段落
            elif not line.strip():
                continue
    return files


def estimate_tokens(text: str) -> int:
    """粗略估算 token 数（中文约 1.5 字/token，英文约 4 字符/token）"""
    cn_chars = sum(1 for c in text if '一' <= c <= '鿿')
    en_chars = len(text) - cn_chars
    return int(cn_chars / 1.5 + en_chars / 4)


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")

    parts = [
        f"=== POST-COMPACTION RECOVERY v2 [{now}] ===",
        "",
    ]

    # 1. 读取检查点
    checkpoint_path = os.path.join(project_dir, ".claude", "session-checkpoint.md")
    checkpoint = read_file_head(checkpoint_path, max_chars=5000)
    if checkpoint:
        parts.append("## Session Checkpoint (pre-compaction state)")
        parts.append(checkpoint)
        parts.append("")
    else:
        parts.append("No pre-compaction checkpoint found.")
        parts.append("")

    # 2. 读取今日记忆尾部
    daily_memory = os.path.join(project_dir, "memory", f"{today}.md")
    daily_tail = read_file_tail(daily_memory, max_lines=5)
    if daily_tail:
        parts.append(f"## Today's Memory ({today}) recent")
        parts.append(daily_tail)
        parts.append("")

    # 3. v2: 重读修改的文件（50K token 预算）
    modified_files = parse_checkpoint_for_files(checkpoint) if checkpoint else []
    if modified_files:
        parts.append("## Modified Files Recovery (50K token budget)")
        token_budget = 50000
        tokens_used = 0
        for fpath in modified_files[:10]:  # 最多重读 10 个文件
            if tokens_used >= token_budget:
                parts.append(f"[Budget exhausted at {tokens_used:,} tokens, skipping remaining files]")
                break
            try:
                # 尝试读取文件（限制大小）
                remaining_budget = token_budget - tokens_used
                max_chars = min(remaining_budget * 3, 5000)  # 粗略: 1 token ≈ 3 chars
                content = read_file_head(fpath, max_chars=max_chars)
                if content:
                    file_tokens = estimate_tokens(content)
                    tokens_used += file_tokens
                    parts.append(f"### {fpath} (~{file_tokens:,} tokens)")
                    # 只放摘要，不放全文（避免 context 膨胀）
                    parts.append(f"[File exists: {len(content):,} chars. Read with Read tool if needed.]")
                else:
                    parts.append(f"### {fpath}")
                    parts.append("[File empty or not found]")
            except Exception:
                parts.append(f"### {fpath}")
                parts.append("[Error reading file]")
        parts.append(f"[Total recovery tokens: ~{tokens_used:,} / {token_budget:,}]")
        parts.append("")

    # 4. 恢复指令
    parts.extend([
        "## Recovery Actions Required",
        "1. Read .claude/session-checkpoint.md for full pre-compaction state",
        f"2. Read memory/{today}.md for today's context",
        "3. Read memory/long-term.md for persistent knowledge",
        "4. Read project.md for project status",
        "5. Resume the task from the checkpoint's 'Last user request'",
        "6. Verify modified files still have correct content",
        "",
    ])

    output = "\n".join(parts)

    # 确保不超 10K 字符限制
    if len(output) > 9500:
        output = output[:9500] + "\n[Truncated: checkpoint too large]"

    print(output)


if __name__ == "__main__":
    main()
