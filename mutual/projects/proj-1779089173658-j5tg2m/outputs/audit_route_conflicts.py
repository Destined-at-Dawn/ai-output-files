#!/usr/bin/env python3
"""
路由冲突审计脚本 - Pre-flight Check
修改 skill-routing-table.json 前必须运行此脚本

检查项:
1. frontmatter name 是否已被其他目录名注册？
2. 新触发词是否与已有路由重复？
3. route id 是否唯一？
4. 所有活跃 skill 是否都有路由？

用法: python audit_route_conflicts.py [--fix]
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

def load_routing_table(table_path):
    """加载路由表"""
    with open(table_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_skill_frontmatter_name(skill_dir):
    """从 SKILL.md 读取 frontmatter name"""
    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        return None

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析 frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            frontmatter = content[3:end]
            for line in frontmatter.split('\n'):
                if line.startswith('name:'):
                    return line.split(':', 1)[1].strip()
    return None

def check_duplicate_route_ids(routes):
    """检查重复的 route id"""
    id_count = defaultdict(list)
    for r in routes:
        id_count[r['id']].append(r.get('skill', r.get('name', 'unknown')))

    duplicates = {k: v for k, v in id_count.items() if len(v) > 1}
    return duplicates

def check_duplicate_triggers(routes):
    """检查跨 skill 重复触发词"""
    trigger_map = defaultdict(list)
    for r in routes:
        skill = r.get('skill', r.get('name', 'unknown'))
        for trigger in r.get('triggers', []):
            trigger_map[trigger].append(skill)

    duplicates = {k: v for k, v in trigger_map.items() if len(v) > 1}
    return duplicates

def check_frontmatter_conflicts(routes, skills_dir):
    """检查 frontmatter name 冲突"""
    # 建立 skill -> frontmatter name 映射
    skill_to_name = {}
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
            name = get_skill_frontmatter_name(skill_dir)
            if name:
                skill_to_name[skill_dir.name] = name

    # 检查是否有多个目录指向同一个 frontmatter name
    name_to_dirs = defaultdict(list)
    for skill, name in skill_to_name.items():
        name_to_dirs[name].append(skill)

    conflicts = {k: v for k, v in name_to_dirs.items() if len(v) > 1}
    return conflicts

def check_unregistered_skills(routes, skills_dir):
    """检查未注册路由的技能"""
    registered_skills = {r.get('skill') for r in routes}
    unregistered = []

    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
            # 跳过已弃用的
            if (skill_dir / 'DEPRECATED.md').exists():
                continue
            if skill_dir.name not in registered_skills:
                unregistered.append(skill_dir.name)

    return unregistered

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    # 路径配置
    mutual_dir = Path(r'E:\ai产出文件\牛马\mutual\mutual')
    table_path = mutual_dir / 'skill-routing-table.json'
    skills_dir = mutual_dir / 'skills'

    if not table_path.exists():
        print(f"❌ 路由表不存在: {table_path}")
        return 1

    # 加载路由表
    data = load_routing_table(table_path)
    routes = data.get('routes', [])

    print(f"📊 路由表统计")
    print(f"   版本: {data.get('version', 'unknown')}")
    print(f"   总路由数: {len(routes)}")
    print()

    # 检查 1: 重复 route id
    print("🔍 检查 1: 重复 route id")
    dup_ids = check_duplicate_route_ids(routes)
    if dup_ids:
        print(f"   ❌ 发现 {len(dup_ids)} 个重复 id:")
        for id, skills in dup_ids.items():
            print(f"      {id}: {', '.join(skills)}")
    else:
        print("   ✅ 无重复 id")
    print()

    # 检查 2: 跨 skill 重复触发词
    print("🔍 检查 2: 跨 skill 重复触发词")
    dup_triggers = check_duplicate_triggers(routes)
    if dup_triggers:
        print(f"   ❌ 发现 {len(dup_triggers)} 个重复触发词:")
        for trigger, skills in list(dup_triggers.items())[:10]:
            print(f"      '{trigger}': {', '.join(skills)}")
        if len(dup_triggers) > 10:
            print(f"      ... 还有 {len(dup_triggers) - 10} 个")
    else:
        print("   ✅ 无重复触发词")
    print()

    # 检查 3: frontmatter name 冲突
    print("🔍 检查 3: frontmatter name 冲突")
    name_conflicts = check_frontmatter_conflicts(routes, skills_dir)
    if name_conflicts:
        print(f"   ❌ 发现 {len(name_conflicts)} 个 name 冲突:")
        for name, dirs in name_conflicts.items():
            print(f"      '{name}': {', '.join(dirs)}")
    else:
        print("   ✅ 无 name 冲突")
    print()

    # 检查 4: 未注册路由的技能
    print("🔍 检查 4: 未注册路由的技能")
    unregistered = check_unregistered_skills(routes, skills_dir)
    if unregistered:
        print(f"   ⚠️ 发现 {len(unregistered)} 个未注册技能:")
        for skill in unregistered:
            print(f"      - {skill}")
    else:
        print("   ✅ 所有活跃技能都已注册")
    print()

    # 检查 5: 触发词数量不足
    print("🔍 检查 5: 触发词数量不足 (<15)")
    low_triggers = []
    for r in routes:
        skill = r.get('skill', r.get('name', 'unknown'))
        count = len(r.get('triggers', []))
        if count < 15:
            low_triggers.append((skill, count))

    if low_triggers:
        print(f"   ⚠️ 发现 {len(low_triggers)} 个技能触发词不足:")
        for skill, count in sorted(low_triggers, key=lambda x: x[1]):
            print(f"      - {skill}: {count} 个")
    else:
        print("   ✅ 所有技能触发词数量充足")
    print()

    # 总结
    print("=" * 60)
    print("📋 审计总结")
    print("=" * 60)

    issues = []
    if dup_ids:
        issues.append(f"重复 route id: {len(dup_ids)} 个")
    if dup_triggers:
        issues.append(f"重复触发词: {len(dup_triggers)} 个")
    if name_conflicts:
        issues.append(f"name 冲突: {len(name_conflicts)} 个")
    if unregistered:
        issues.append(f"未注册技能: {len(unregistered)} 个")
    if low_triggers:
        issues.append(f"触发词不足: {len(low_triggers)} 个")

    if issues:
        print("❌ 发现以下问题:")
        for issue in issues:
            print(f"   - {issue}")
        print()
        print("🚫 禁止写入路由表！请先修复以上问题。")
        return 1
    else:
        print("✅ 所有检查通过，可以安全写入路由表。")
        return 0

if __name__ == '__main__':
    sys.exit(main())
