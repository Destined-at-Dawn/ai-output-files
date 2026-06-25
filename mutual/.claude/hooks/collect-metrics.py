#!/usr/bin/env python3
"""
指标采集脚本 — 量化工作流效率
==============================
从 memory/metrics/ 目录收集每日指标，生成趋势分析。

运行方式：python collect-metrics.py [--days 7] [--output summary.md]
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def collect_daily_metrics(metrics_dir: str, date_str: str) -> dict:
    """收集指定日期的指标"""
    jsonl_path = os.path.join(metrics_dir, f"{date_str}.jsonl")
    if not os.path.exists(jsonl_path):
        return None

    entries = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if not entries:
        return None

    total_input = sum(e.get("total_input_tokens", 0) for e in entries)
    total_output = sum(e.get("total_output_tokens", 0) for e in entries)
    total_turns = sum(e.get("turn_count", 0) for e in entries)

    return {
        "date": date_str,
        "sessions": len(entries),
        "total_turns": total_turns,
        "input_tokens": total_input,
        "output_tokens": total_output,
        "total_tokens": total_input + total_output,
    }


def collect_eval_metrics(eval_path: str) -> dict:
    """收集评估断言指标"""
    if not os.path.exists(eval_path):
        return None

    with open(eval_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("summary", {})


def generate_trend_report(metrics_dir: str, eval_path: str, days: int = 7) -> str:
    """生成趋势分析报告"""
    today = datetime.now()
    daily_data = []

    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        data = collect_daily_metrics(metrics_dir, date_str)
        if data:
            daily_data.append(data)

    eval_data = collect_eval_metrics(eval_path)

    lines = [
        "# 工作流效率趋势报告",
        "",
        f"> 生成时间: {today.strftime('%Y-%m-%d %H:%M:%S')}",
        f"> 分析周期: {days} 天",
        "",
    ]

    # 每日指标
    if daily_data:
        lines.append("## 每日指标")
        lines.append("")
        lines.append("| 日期 | 会话数 | 轮次 | Input Tokens | Output Tokens | 总 Tokens |")
        lines.append("|------|--------|------|-------------|---------------|-----------|")

        for d in reversed(daily_data):
            lines.append(
                f"| {d['date']} | {d['sessions']} | {d['total_turns']} | "
                f"{d['input_tokens']:,} | {d['output_tokens']:,} | {d['total_tokens']:,} |"
            )
        lines.append("")

        # 趋势分析
        if len(daily_data) >= 2:
            recent = daily_data[0]["total_tokens"]
            older = daily_data[-1]["total_tokens"]
            if older > 0:
                change = (recent - older) / older * 100
                trend = "上升" if change > 0 else "下降"
                lines.append(f"**趋势**: Token 使用量 {trend} {abs(change):.1f}%")
                lines.append("")
    else:
        lines.append("## 每日指标")
        lines.append("暂无数据。指标将在下次会话结束后自动采集。")
        lines.append("")

    # 评估断言
    if eval_data:
        lines.append("## 评估断言状态")
        lines.append("")
        lines.append(f"- 总断言数: {eval_data.get('total', 0)}")
        lines.append(f"- 通过: {eval_data.get('pass', 0)}")
        lines.append(f"- 失败: {eval_data.get('fail', 0)}")
        lines.append(f"- 未知: {eval_data.get('unknown', 0)}")
        lines.append(f"- 待测: {eval_data.get('pending', 0)}")
        lines.append(f"- 通过率: {eval_data.get('pass_rate', 0) * 100:.1f}%")
        lines.append("")
    else:
        lines.append("## 评估断言状态")
        lines.append("暂无数据。")
        lines.append("")

    return "\n".join(lines)


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    metrics_dir = os.path.join(project_dir, "memory", "metrics")
    eval_path = os.path.join(project_dir, "skills", "auto-evolution", "eval.json")

    days = 7
    output_file = None

    # 解析命令行参数
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        else:
            i += 1

    report = generate_trend_report(metrics_dir, eval_path, days)

    if output_file:
        output_path = os.path.join(project_dir, output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
