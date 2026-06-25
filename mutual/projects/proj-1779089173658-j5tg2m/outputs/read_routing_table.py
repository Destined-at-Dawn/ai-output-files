# -*- coding: utf-8 -*-
"""
路由表读取工具 - 稳定版
用法：
  python read_routing_table.py              # 显示所有路由摘要
  python read_routing_table.py karpathy     # 搜索包含关键词的路由
  python read_routing_table.py --detail r023 # 显示指定ID的详细信息
"""

import json
import sys
import os

# Windows 终端编码修复
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 路由表路径
ROUTING_TABLE = r"E:\ai产出文件\牛马\mutual\mutual\skill-routing-table.json"


def load_routing_table():
    """加载路由表"""
    if not os.path.exists(ROUTING_TABLE):
        print(f"错误: 路由表文件不存在: {ROUTING_TABLE}")
        sys.exit(1)

    with open(ROUTING_TABLE, "r", encoding="utf-8") as f:
        return json.load(f)


def show_summary(data):
    """显示路由表摘要"""
    routes = data.get("routes", [])
    print("=" * 60)
    print(f"路由表版本: {data.get('version', '未知')}")
    print(f"总路由数: {len(routes)}")
    print("=" * 60)
    print()

    # 统计
    auto_count = sum(1 for r in routes if r.get("auto", False))
    print(f"自动激活路由: {auto_count}/{len(routes)}")
    print()

    # 列出所有路由
    print("路由列表:")
    print("-" * 60)
    for r in routes:
        rid = r.get("id", "?")
        name = r.get("name", "未命名")
        skill = r.get("skill", "?")
        triggers_count = len(r.get("triggers", []))
        auto = "[Y]" if r.get("auto", False) else "[N]"
        print(f"  [{rid}] {name}")
        print(f"       技能: {skill} | 触发词: {triggers_count}个 | 自动: {auto}")


def search_routes(data, keyword):
    """搜索包含关键词的路由"""
    routes = data.get("routes", [])
    keyword_lower = keyword.lower()
    results = []

    for r in routes:
        # 搜索名称
        if keyword_lower in r.get("name", "").lower():
            results.append(r)
            continue

        # 搜索技能名
        if keyword_lower in r.get("skill", "").lower():
            results.append(r)
            continue

        # 搜索触发词
        for trigger in r.get("triggers", []):
            if keyword_lower in trigger.lower():
                results.append(r)
                break

    print(f"搜索 \"{keyword}\" 找到 {len(results)} 条路由:")
    print("=" * 60)

    for r in results:
        rid = r.get("id", "?")
        name = r.get("name", "未命名")
        skill = r.get("skill", "?")
        triggers = r.get("triggers", [])
        auto = "[Y]" if r.get("auto", False) else "[N]"

        print(f"\n[{rid}] {name}")
        print(f"  技能: {skill}")
        print(f"  自动激活: {auto} | 置信度: {r.get('confidence', '?')}")
        print(f"  触发词 ({len(triggers)}个):")
        for t in triggers:
            print(f"    - {t}")


def show_detail(data, route_id):
    """显示指定路由的详细信息"""
    routes = data.get("routes", [])

    for r in routes:
        if r.get("id") == route_id:
            print(f"路由详情: {route_id}")
            print("=" * 60)
            print(json.dumps(r, indent=2, ensure_ascii=False))
            return

    print(f"未找到路由 ID: {route_id}")
    print("可用的路由 ID:")
    for r in routes[:10]:
        print(f"  {r.get('id')}: {r.get('name')}")
    print("  ...")


def main():
    data = load_routing_table()

    if len(sys.argv) == 1:
        # 无参数，显示摘要
        show_summary(data)
    elif sys.argv[1] == "--detail" and len(sys.argv) > 2:
        # 显示详情
        show_detail(data, sys.argv[2])
    else:
        # 搜索关键词
        keyword = sys.argv[1]
        search_routes(data, keyword)


if __name__ == "__main__":
    main()
