#!/usr/bin/env python3
"""
SessionStart Hook v2 (compact matcher) — 压缩后上下文恢复
=========================================================
在每次 compaction（手动/自动）后触发，向 Claude 注入恢复上下文。

核心功能：
- 读取 PreCompact 写入的检查点
- 读取项目文件（CLAUDE.md / memory / project.md）
- 50K token 预算重读策略
- 输出恢复指令到 stdout → Claude 自动注入上下文

来源：Anthropic 最佳实践 + Forge Code
"""

import json
import os
import sys
from datetime import datetime


def read_file_head(filepath, max_chars=4000):
    """读取文件前 N 个字符"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_chars).strip()
    except (IOError, OSError):
        return ""


def read_file_tail(filepath, max_lines=10):
    """读取文件最后 N 行"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            return "".join(lines[-max_lines:]).strip()
    except (IOError, OSError):
        return ""


def find_project_files(project_dir):
    """查找项目中的关键文件（兼容不同项目结构）"""
    candidates = {
        "CLAUDE.md": os.path.join(project_dir, "CLAUDE.md"),
        "memory/long-term.md": os.path.join(project_dir, "memory", "long-term.md"),
        "project.md": os.path.join(project_dir, "project.md"),
    }
    # 查找今日记忆
    today = datetime.now().strftime("%Y-%m-%d")
    candidates[f"memory/{today}.md"] = os.path.join(project_dir, "memory", f"{today}.md")

    found = {}
    for name, path in candidates.items():
        if os.path.exists(path):
            found[name] = path
    return found


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
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

    # 2. 查找并读取项目文件
    project_files = find_project_files(project_dir)
    if project_files:
        parts.append("## Project Files Found")
        for name, path in project_files.items():
            if "memory" in name and name != "memory/long-term.md":
                content = read_file_tail(path, max_lines=5)
            else:
                content = read_file_head(path, max_chars=2000)
            if content:
                parts.append(f"### {name}")
                parts.append(f"[{len(content)} chars loaded from {path}]")
                parts.append("")
        parts.append(f"[Total project files: {len(project_files)}]")
        parts.append("")

    # 3. 恢复指令
    parts.extend([
        "## Recovery Actions Required",
        "1. Read .claude/session-checkpoint.md for full pre-compaction state",
        "2. Read your CLAUDE.md for project instructions",
        "3. Read project memory files if they exist",
        "4. Resume the task from the checkpoint's 'Latest user request'",
        "5. Verify modified files still have correct content",
        "",
    ])

    output = "\n".join(parts)

    # 确保不超 10K 字符限制
    if len(output) > 9500:
        output = output[:9500] + "\n[Truncated: checkpoint too large]"

    print(output)


if __name__ == "__main__":
    main()
