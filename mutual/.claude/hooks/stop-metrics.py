#!/usr/bin/env python3
"""
Stop Hook — 自主循环控制 + 量化指标追踪
========================================
在 Claude Code 完成一轮对话后触发。功能：
1. 记录本轮会话的量化指标（工具调用次数、文件修改数、耗时）
2. 检查是否需要继续自主循环（Ralph Loop 模式）
3. 写指标到 memory/metrics/ 目录供长期分析

来源：
- Ralph Loop（pig4cloud）：自主迭代循环技术
- Anthropic Context Compaction Cookbook：量化基准数据
- JetBrains AI Arena：Agent 性能评估框架
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


def read_stdin_json():
    try:
        raw = sys.stdin.read()
        if raw.strip():
            return json.loads(raw)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def extract_metrics(meta: dict) -> dict:
    """从 Stop hook 元数据提取量化指标"""
    return {
        "timestamp": datetime.now().isoformat(),
        "session_id": meta.get("session_id", "unknown"),
        "stop_reason": meta.get("stop_reason", "unknown"),
        "turn_count": meta.get("turn_count", 0),
        "tool_calls": meta.get("tool_calls", []),
        "total_input_tokens": meta.get("total_input_tokens", 0),
        "total_output_tokens": meta.get("total_output_tokens", 0),
        "duration_ms": meta.get("duration_ms", 0),
    }


def write_metrics(metrics: dict, project_dir: str):
    """写指标到 metrics 目录"""
    metrics_dir = os.path.join(project_dir, "memory", "metrics")
    os.makedirs(metrics_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    metrics_file = os.path.join(metrics_dir, f"{today}.jsonl")

    with open(metrics_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(metrics, ensure_ascii=False) + "\n")


def update_daily_summary(project_dir: str):
    """更新今日指标汇总"""
    today = datetime.now().strftime("%Y-%m-%d")
    metrics_file = os.path.join(project_dir, "memory", "metrics", f"{today}.jsonl")
    summary_file = os.path.join(project_dir, "memory", "metrics", f"{today}-summary.md")

    if not os.path.exists(metrics_file):
        return

    # 读取今日所有指标
    entries = []
    with open(metrics_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if not entries:
        return

    # 计算汇总
    total_input = sum(e.get("total_input_tokens", 0) for e in entries)
    total_output = sum(e.get("total_output_tokens", 0) for e in entries)
    total_turns = sum(e.get("turn_count", 0) for e in entries)
    session_count = len(entries)

    tool_usage = {}
    for e in entries:
        for tool in e.get("tool_calls", []):
            if isinstance(tool, str):
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
            elif isinstance(tool, dict):
                name = tool.get("name", "unknown")
                tool_usage[name] = tool_usage.get(name, 0) + 1

    # 写汇总
    lines = [
        f"# {today} 指标汇总",
        "",
        f"- 会话数: {session_count}",
        f"- 总轮次: {total_turns}",
        f"- Input tokens: {total_input:,}",
        f"- Output tokens: {total_output:,}",
        f"- 总 tokens: {total_input + total_output:,}",
        "",
        "## 工具使用频率",
    ]

    for tool, count in sorted(tool_usage.items(), key=lambda x: -x[1])[:15]:
        lines.append(f"- {tool}: {count}")

    lines.append("")
    lines.append(f"> 最后更新: {datetime.now().strftime('%H:%M:%S')}")

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    meta = read_stdin_json()
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

    # 1. 提取并记录指标
    metrics = extract_metrics(meta)
    write_metrics(metrics, project_dir)

    # 2. 更新今日汇总
    update_daily_summary(project_dir)

    # 3. 检查自主循环条件（Ralph Loop 模式）
    # 如果 stop_reason 是 "end_turn" 且有未完成的循环任务，可注入继续指令
    stop_reason = meta.get("stop_reason", "")

    # 4. 输出简洁状态到 stdout（不影响主对话）
    output_parts = [
        f"[Metrics] Session logged at {datetime.now().strftime('%H:%M:%S')}",
        f"[Metrics] Tokens: {metrics['total_input_tokens']:,} in / {metrics['total_output_tokens']:,} out",
    ]

    # 如果 token 使用量高，提醒可能需要压缩
    total_tokens = metrics['total_input_tokens'] + metrics['total_output_tokens']
    if total_tokens > 100000:
        output_parts.append("[Metrics] ⚠️ Token usage >100K, consider /compact")

    print("\n".join(output_parts))


if __name__ == "__main__":
    main()
