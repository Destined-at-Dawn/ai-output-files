#!/usr/bin/env python3
"""
PostToolUse Hook — 操作后自动验证 + 后处理
==========================================
在每次工具调用完成后触发。功能：
1. Write/Edit 后自动验证文件存在且内容非空
2. 记录工具调用结果到审计日志
3. 对关键操作注入验证提醒

来源：
- DataCamp Claude Code Hooks 教程：PostToolUse 可自动触发验证
- Forge Code：模式匹配压缩中的文件路径精确保留
"""

import json
import sys
import os
from datetime import datetime


def read_stdin_json():
    try:
        raw = sys.stdin.read()
        if raw.strip():
            return json.loads(raw)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def verify_file_operation(tool_name: str, tool_input: dict, tool_response: dict) -> str:
    """
    验证文件操作是否成功。
    返回验证结果消息，或空字符串表示无需验证。
    """
    if tool_name not in ("write_project_file", "Write", "Edit"):
        return ""

    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if not file_path:
        return ""

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return f"[VERIFY FAIL] 文件操作后文件不存在: {file_path}"

    # 检查文件是否为空
    try:
        size = os.path.getsize(file_path)
        if size == 0:
            return f"[VERIFY FAIL] 文件操作后文件为空: {file_path}"
        return f"[VERIFY OK] {file_path} ({size:,} bytes)"
    except OSError:
        return "[VERIFY WARN] 无法检查文件大小"


def main():
    meta = read_stdin_json()
    tool_name = meta.get("tool_name", "")
    tool_input = meta.get("tool_input", {})
    tool_response = meta.get("tool_response", {})

    # 对文件操作做自动验证
    verify_msg = verify_file_operation(tool_name, tool_input, tool_response)

    if verify_msg:
        print(verify_msg)


if __name__ == "__main__":
    main()
