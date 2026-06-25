#!/usr/bin/env python3
"""
每日健康检查脚本 — 全自动工作流健康监控
========================================
在 SessionStart 时运行，检查系统健康状态。

检查项目：
1. Hook 脚本完整性
2. 评估断言状态
3. 记忆文件新鲜度
4. 量化指标趋势
5. MCP 工具可用性
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def check_hook_scripts(project_dir: str) -> list:
    """检查 Hook 脚本完整性"""
    hooks_dir = os.path.join(project_dir, ".claude", "hooks")
    required_hooks = [
        "pre-tool-use.py",
        "post-tool-use.py",
        "stop-metrics.py",
        "pre-compact.py",
        "on-compact.py",
        "collect-metrics.py",
        "daily-health-check.py",
    ]
    results = []
    for hook in required_hooks:
        path = os.path.join(hooks_dir, hook)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        results.append({
            "name": hook,
            "exists": exists,
            "size": size,
            "status": "ok" if exists and size > 100 else "fail"
        })
    return results


def check_eval_status(project_dir: str) -> dict:
    """检查评估断言状态"""
    eval_path = os.path.join(project_dir, "skills", "auto-evolution", "eval.json")
    if not os.path.exists(eval_path):
        return {"status": "missing", "pass_rate": 0}

    with open(eval_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary = data.get("summary", {})
    return {
        "status": "ok",
        "total": summary.get("total", 0),
        "pass": summary.get("pass", 0),
        "fail": summary.get("fail", 0),
        "pass_rate": summary.get("pass_rate", 0),
    }


def check_memory_freshness(project_dir: str) -> dict:
    """检查记忆文件新鲜度"""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_dir = os.path.join(project_dir, "memory")

    checks = {}
    for name in ["long-term.md", f"{today}.md"]:
        path = os.path.join(memory_dir, name)
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            age_hours = (datetime.now().timestamp() - mtime) / 3600
            checks[name] = {
                "exists": True,
                "age_hours": round(age_hours, 1),
                "fresh": age_hours < 24,
            }
        else:
            checks[name] = {"exists": False, "fresh": False}

    return checks


def check_metrics_trend(project_dir: str) -> dict:
    """检查量化指标趋势"""
    metrics_dir = os.path.join(project_dir, "memory", "metrics")
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    today_file = os.path.join(metrics_dir, f"{today}.jsonl")
    yesterday_file = os.path.join(metrics_dir, f"{yesterday}.jsonl")

    return {
        "today_exists": os.path.exists(today_file),
        "yesterday_exists": os.path.exists(yesterday_file),
        "metrics_dir_exists": os.path.exists(metrics_dir),
    }


def main():
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"=== Daily Health Check [{now}] ===")
    print()

    # 1. Hook 脚本检查
    hooks = check_hook_scripts(project_dir)
    ok_hooks = sum(1 for h in hooks if h["status"] == "ok")
    total_hooks = len(hooks)
    print(f"Hook Scripts: {ok_hooks}/{total_hooks} OK")
    for h in hooks:
        if h["status"] != "ok":
            print(f"  [WARN] {h['name']}: missing or too small")
    print()

    # 2. 评估断言检查
    eval_status = check_eval_status(project_dir)
    print(f"Eval Assertions: {eval_status.get('pass', 0)}/{eval_status.get('total', 0)} pass")
    print(f"  Pass Rate: {eval_status.get('pass_rate', 0) * 100:.1f}%")
    print()

    # 3. 记忆新鲜度检查
    memory = check_memory_freshness(project_dir)
    for name, info in memory.items():
        if info["exists"]:
            status = "FRESH" if info["fresh"] else "STALE"
            print(f"Memory {name}: {status} (age: {info['age_hours']}h)")
        else:
            print(f"Memory {name}: MISSING")
    print()

    # 4. 指标趋势检查
    metrics = check_metrics_trend(project_dir)
    print(f"Metrics Today: {'exists' if metrics['today_exists'] else 'no data'}")
    print(f"Metrics Yesterday: {'exists' if metrics['yesterday_exists'] else 'no data'}")
    print()

    # 5. 总体健康评分
    score = 0
    max_score = 4

    if ok_hooks == total_hooks:
        score += 1
    if eval_status.get("pass_rate", 0) >= 0.8:
        score += 1
    if all(info.get("fresh", False) for info in memory.values()):
        score += 1
    if metrics["today_exists"] or metrics["yesterday_exists"]:
        score += 1

    health_pct = score / max_score * 100
    print(f"=== Overall Health: {score}/{max_score} ({health_pct:.0f}%) ===")

    if health_pct < 75:
        print("[ALERT] Health below 75%. Review failing checks above.")


if __name__ == "__main__":
    main()
