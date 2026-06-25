#!/usr/bin/env python3
"""
PreToolUse Hook — 安全守卫 + 操作审计
=====================================
在每次工具调用前触发。功能：
1. 拦截危险操作（删除系统文件、覆写关键配置）→ exit 2 阻止
2. 记录操作到审计日志 → exit 0 允许
3. 注入安全提醒到上下文 → exit 0 + JSON 输出

来源：
- Claude Code 官方 hooks 文档
- DataCamp Claude Code Hooks 教程
- claude-world.com hooks-development-guide

安全规则参考：
- .claude/rules/script-safety-check.md
- .claude/rules/no-blind-overwrite.md
- .claude/rules/git-recovery.md
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


# === 危险路径黑名单 ===
DANGEROUS_PATHS = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\ProgramData\\Microsoft\\Windows\\Start Menu",
    "/System",
    "/usr/bin",
    "/usr/sbin",
    "/etc",
]

# === 关键配置文件（覆写前必须确认）===
CRITICAL_FILES = [
    "CLAUDE.md",
    ".claude/settings.json",
    ".claude/rules/",
    "memory/long-term.md",
    "skill-routing-table.json",
]

# === 审计日志路径 ===
AUDIT_LOG_DIR = os.path.join(
    os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()),
    ".claude", "audit-logs"
)


def read_stdin_json():
    """从 stdin 读取 Claude Code 传入的 JSON 元数据"""
    try:
        raw = sys.stdin.read()
        if raw.strip():
            return json.loads(raw)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def is_dangerous_path(path: str) -> bool:
    """检查路径是否在危险黑名单中"""
    if not path:
        return False
    normalized = os.path.normpath(path).replace("/", "\\").lower()
    for dp in DANGEROUS_PATHS:
        if normalized.startswith(dp.lower()):
            return True
    return False


def is_critical_file(path: str) -> bool:
    """检查是否为关键配置文件"""
    if not path:
        return False
    for cf in CRITICAL_FILES:
        if cf in path:
            return True
    return False


def check_delete_safety(tool_input: dict) -> tuple:
    """
    检查删除操作的安全性。
    返回 (is_safe: bool, reason: str)
    """
    path = tool_input.get("file_path", "") or tool_input.get("path", "") or tool_input.get("directory", "")
    if not path:
        return True, ""

    # 检查危险路径
    if is_dangerous_path(path):
        return False, f"BLOCKED: 尝试操作危险路径 {path}"

    # 检查是否对目录执行删除（应该精确到文件）
    if path.endswith("\\") or path.endswith("/"):
        return False, f"BLOCKED: 路径以目录分隔符结尾，可能删除整个目录: {path}"

    return True, ""


def log_audit(tool_name: str, tool_input: dict, decision: str, reason: str = ""):
    """记录操作审计日志"""
    try:
        os.makedirs(AUDIT_LOG_DIR, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        log_path = os.path.join(AUDIT_LOG_DIR, f"{today}.jsonl")

        entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "decision": decision,
            "reason": reason,
            "input_summary": {
                k: str(v)[:200] for k, v in list(tool_input.items())[:5]
            }
        }

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # 审计日志失败不应阻断正常操作


def main():
    meta = read_stdin_json()
    tool_name = meta.get("tool_name", "")
    tool_input = meta.get("tool_input", {})
    tool_id = meta.get("tool_use_id", "")

    # === 规则 1: 删除操作安全检查 ===
    if tool_name in ("bash", "Bash"):
        command = tool_input.get("command", "")
        # 检查 rm / Remove-Item / del 命令
        dangerous_commands = ["rm -rf", "rm -r", "Remove-Item", "del /", "rmdir"]
        for dc in dangerous_commands:
            if dc in command:
                # 检查是否涉及系统路径
                for dp in DANGEROUS_PATHS:
                    if dp.lower() in command.lower():
                        reason = f"BLOCKED: 危险命令 '{dc}' 涉及系统路径 '{dp}'"
                        log_audit(tool_name, tool_input, "blocked", reason)
                        # 输出阻止信息到 stderr
                        print(reason, file=sys.stderr)
                        sys.exit(2)  # exit 2 = 阻止操作

        # 检查 rm 对目录的操作
        if "rm " in command and "-r" in command:
            reason = "WARNING: 递归删除命令，请确认目标路径安全"
            log_audit(tool_name, tool_input, "warning", reason)

    # === 规则 2: 文件覆写安全检查 ===
    if tool_name in ("write_project_file", "Write"):
        file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
        if is_dangerous_path(file_path):
            reason = f"BLOCKED: 尝试覆写危险路径 {file_path}"
            log_audit(tool_name, tool_input, "blocked", reason)
            print(reason, file=sys.stderr)
            sys.exit(2)

    # === 规则 3: 记录所有操作到审计日志 ===
    log_audit(tool_name, tool_input, "allowed")

    # === 规则 4: 对关键文件操作注入提醒 ===
    additional_context = ""
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if file_path and is_critical_file(file_path):
        additional_context = (
            f"[Safety Guard] 操作关键文件: {file_path}. "
            "请确保已 Read 当前内容后再 Write（No Blind Overwrite 规则）。"
        )

    # 输出结果
    if additional_context:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": additional_context,
            }
        }
        print(json.dumps(output))

    sys.exit(0)  # 允许操作


if __name__ == "__main__":
    main()
