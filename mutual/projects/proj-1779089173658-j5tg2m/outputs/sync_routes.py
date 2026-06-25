#!/usr/bin/env python3
"""
跨工作区路由表同步脚本
把 mutual 工作区的 skill-routing-table.json 同步到其他工作区
"""

import shutil
import sys
from pathlib import Path

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    # 源路由表
    source = Path(r'E:\ai产出文件\牛马\mutual\mutual\skill-routing-table.json')

    if not source.exists():
        print(f"❌ 源路由表不存在: {source}")
        return 1

    # 目标工作区（主要工作区）
    workspaces = [
        r'E:\ai产出文件\牛马\个人\个人',
        r'E:\ai产出文件\牛马\创作\创作',
        r'E:\ai产出文件\牛马\学习\学习',
        r'E:\ai产出文件\牛马\求职\求职',
        r'E:\ai产出文件\牛马\竞赛\竞赛',
        r'E:\ai产出文件\牛马\日常学习',
    ]

    print(f"📊 源路由表: {source}")
    print(f"   文件大小: {source.stat().st_size} 字节")
    print()

    synced = []
    failed = []

    for ws_path in workspaces:
        ws = Path(ws_path)
        if not ws.exists():
            print(f"⚠️ {ws.name}: 目录不存在，跳过")
            continue

        target = ws / 'skill-routing-table.json'

        try:
            shutil.copy2(source, target)
            print(f"✅ {ws.name}: 同步成功")
            synced.append(ws.name)
        except Exception as e:
            print(f"❌ {ws.name}: 同步失败 - {e}")
            failed.append(ws.name)

    print()
    print("=" * 60)
    print("📋 同步总结")
    print("=" * 60)
    print(f"✅ 成功: {len(synced)} 个工作区")
    if failed:
        print(f"❌ 失败: {len(failed)} 个工作区")
    print()

    return 0 if not failed else 1

if __name__ == '__main__':
    sys.exit(main())
