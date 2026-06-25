#!/usr/bin/env python3
"""
路由修复脚本
1. 给 li-research 补口语触发词
2. 弃用 6 个冗余 GAP 技能
3. 注册 li-personal 路由
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def backup_routing_table(table_path):
    """备份路由表"""
    backup_path = table_path.parent / f"skill-routing-table.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    shutil.copy2(table_path, backup_path)
    print(f"✅ 已备份路由表到: {backup_path}")
    return backup_path

def add_research_triggers(data):
    """给 li-research 补口语触发词"""
    new_triggers = [
        "搜一下", "帮我搜", "找一下", "查一下", "搜搜", "帮我找",
        "查查", "搜索一下", "帮我查", "找找看", "搜一搜", "帮我找找",
        "查一下资料", "帮我搜一下", "找一下资料"
    ]

    for route in data['routes']:
        if route.get('skill') == 'li-research':
            existing = set(route['triggers'])
            added = [t for t in new_triggers if t not in existing]
            route['triggers'].extend(added)
            print(f"✅ li-research: 新增 {len(added)} 个口语触发词")
            print(f"   触发词总数: {len(route['triggers'])}")
            return True

    print("❌ 未找到 li-research 路由")
    return False

def deprecate_redundant_skills(skills_dir):
    """弃用 6 个冗余 GAP 技能"""
    skills_to_deprecate = [
        "li-frontend",    # 被 li-web 覆盖
        "li-platform",    # 被 li-wechat 覆盖
        "li-search",      # 被 li-research + li-bestskill + li-local-search 三重覆盖
        "li-session",     # 被 li-sync + li-manage + li-improve 三重覆盖
        "li-voice",       # 零案例，可并入 li-writing
        "li-docs"         # = doc-coauthoring，已路由
    ]

    deprecated = []
    for skill_name in skills_to_deprecate:
        skill_dir = skills_dir / skill_name
        if not skill_dir.exists():
            print(f"⚠️ {skill_name}: 目录不存在，跳过")
            continue

        # 检查是否已有 DEPRECATED.md
        deprecated_md = skill_dir / 'DEPRECATED.md'
        if deprecated_md.exists():
            print(f"⚠️ {skill_name}: 已弃用，跳过")
            continue

        # 创建 DEPRECATED.md
        content = f"""# {skill_name} - 已弃用

## 弃用日期
{datetime.now().strftime('%Y-%m-%d')}

## 弃用原因
功能被以下已有路由技能完全覆盖：
"""
        if skill_name == "li-frontend":
            content += "- li-web (r112, 19触发词，Web全能入口)\n"
        elif skill_name == "li-platform":
            content += "- li-wechat (r296, 22触发词，微信全能入口)\n"
        elif skill_name == "li-search":
            content += "- li-research (r083, 57触发词)\n"
            content += "- li-bestskill (外部搜索)\n"
            content += "- li-local-search (本地搜索)\n"
        elif skill_name == "li-session":
            content += "- li-sync (同步)\n"
            content += "- li-manage (管理)\n"
            content += "- li-improve (改进)\n"
        elif skill_name == "li-voice":
            content += "- 零真实案例\n"
            content += "- 可并入 li-writing\n"
        elif skill_name == "li-docs":
            content += "- = doc-coauthoring (r038, 15触发词)\n"
            content += "- 同一个 skill，只是目录名不同\n"

        content += """
## 处置
- 不再注册路由
- SKILL.md 保留作为历史参考
- 触发词由覆盖技能处理
"""

        with open(deprecated_md, 'w', encoding='utf-8') as f:
            f.write(content)

        deprecated.append(skill_name)
        print(f"✅ {skill_name}: 已标记弃用")

    return deprecated

def register_personal_route(data):
    """注册 li-personal 路由"""
    # 检查是否已存在
    for route in data['routes']:
        if route.get('skill') == 'li-personal':
            print(f"⚠️ li-personal 路由已存在: {route['id']}")
            return False

    # 生成新的 route id
    existing_ids = {r['id'] for r in data['routes']}
    new_id = 'r300'
    while new_id in existing_ids:
        new_id = f"r{int(new_id[1:]) + 1}"

    # 创建新路由
    new_route = {
        "id": new_id,
        "name": "个人发展协调器",
        "triggers": [
            "简历", "写简历", "简历优化", "简历修改", "简历润色",
            "面试", "面试准备", "面试问题", "模拟面试", "面试技巧",
            "职业规划", "职业发展", "职业选择", "职业咨询",
            "求职", "找工作", "求职技巧", "求职准备",
            "自我介绍", "个人介绍", "自我描述",
            "实习", "实习准备", "实习申请",
            "职业转型", "转行", "跳槽",
            "工作", "工作机会", "工作申请"
        ],
        "context": ["求职/面试/职业规划场景"],
        "skill": "li-personal",
        "mcp": None,
        "priority": 2,
        "auto": True,
        "confidence": 0.9,
        "note": "个人发展协调器：简历/面试/职业规划/求职全流程"
    }

    data['routes'].append(new_route)
    print(f"✅ li-personal: 已注册路由 {new_id}，{len(new_route['triggers'])} 个触发词")
    return True

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    mutual_dir = Path(r'E:\ai产出文件\牛马\mutual\mutual')
    table_path = mutual_dir / 'skill-routing-table.json'
    skills_dir = mutual_dir / 'skills'

    if not table_path.exists():
        print(f"❌ 路由表不存在: {table_path}")
        return 1

    # 备份
    backup_routing_table(table_path)

    # 加载路由表
    with open(table_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\n📊 当前路由表: {len(data['routes'])} 条路由")
    print()

    # 修复 1: 给 li-research 补口语触发词
    print("=" * 60)
    print("修复 1: 给 li-research 补口语触发词")
    print("=" * 60)
    add_research_triggers(data)
    print()

    # 修复 2: 弃用 6 个冗余 GAP 技能
    print("=" * 60)
    print("修复 2: 弃用 6 个冗余 GAP 技能")
    print("=" * 60)
    deprecated = deprecate_redundant_skills(skills_dir)
    print()

    # 修复 3: 注册 li-personal 路由
    print("=" * 60)
    print("修复 3: 注册 li-personal 路由")
    print("=" * 60)
    register_personal_route(data)
    print()

    # 保存路由表
    with open(table_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("📋 修复总结")
    print("=" * 60)
    print(f"✅ li-research: 已补口语触发词")
    print(f"✅ 弃用技能: {len(deprecated)} 个")
    print(f"✅ li-personal: 已注册路由")
    print(f"\n📊 修复后路由表: {len(data['routes'])} 条路由")
    print()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
