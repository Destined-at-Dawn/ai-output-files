# -*- coding: utf-8 -*-
"""li- 系列端到端路由触发审计"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load routing table
with open(r'E:\ai产出文件\牛马\mutual\mutual\skill-routing-table.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)['routes']

# List installed li-* skills
skills_dir = os.path.expanduser(r'~\.newmax\skills')
installed = set()
for d in os.listdir(skills_dir):
    full = os.path.join(skills_dir, d)
    if os.path.isdir(full) and d.startswith('li-') and not d.endswith('.zip'):
        installed.add(d)

# Routes that reference li-* skills
li_routes = [r for r in routes if r.get('skill','').startswith('li-')]
routed_skills = set(r['skill'] for r in li_routes)

# ============ 1. GAP: Installed but NOT routed ============
missing_routes = installed - routed_skills
print('=' * 60)
print('1. 已安装但无路由 (GAP - 永远不会被触发)')
print('=' * 60)
for s in sorted(missing_routes):
    print(f'   ❌ {s}')
print(f'   共 {len(missing_routes)} 个')

# ============ 2. GHOST: Routed but NOT installed ============
missing_install = routed_skills - installed
print(f'\n{"=" * 60}')
print('2. 有路由但未安装 (GHOST ROUTE - 路由指向不存在)')
print('=' * 60)
for s in sorted(missing_install):
    print(f'   👻 {s}')
print(f'   共 {len(missing_install)} 个')

# ============ 3. Trigger count audit ============
print(f'\n{"=" * 60}')
print('3. 触发词数量审计 (目标: >=15)')
print('=' * 60)
low_trigger = []
for r in sorted(li_routes, key=lambda x: len(x.get('triggers',[])), reverse=True):
    cnt = len(r.get('triggers',[]))
    flag = ' ⚠️ <15' if cnt < 15 else ''
    if cnt < 15:
        low_trigger.append((r['skill'], cnt))
    print(f'   {r["skill"]:25s} {cnt:4d} triggers{flag}')

if low_trigger:
    print(f'\n   ⚠️ 触发词不足15个: {len(low_trigger)} 个技能')

# ============ 4. Duplicate triggers across different skills ============
print(f'\n{"=" * 60}')
print('4. 跨技能重复触发词检测')
print('=' * 60)

trigger_map = {}  # trigger -> list of (skill, route_id)
for r in li_routes:
    for t in r.get('triggers', []):
        t_lower = t.lower().strip()
        if t_lower not in trigger_map:
            trigger_map[t_lower] = []
        trigger_map[t_lower].append((r['skill'], r.get('id','?')))

duplicates = {k: v for k, v in trigger_map.items() if len(v) > 1}
if duplicates:
    print(f'   发现 {len(duplicates)} 个跨技能重复触发词:')
    for trigger, skills in sorted(duplicates.items()):
        skill_list = ', '.join([f'{s[0]}({s[1]})' for s in skills])
        print(f'   ⚡ "{trigger}" -> {skill_list}')
else:
    print('   ✅ 无跨技能重复触发词')

# ============ 5. Summary stats ============
print(f'\n{"=" * 60}')
print('5. 总览')
print('=' * 60)
print(f'   已安装 li-* 技能:      {len(installed)}')
print(f'   有路由的 li-* 技能:    {len(routed_skills)}')
print(f'   缺失路由 (GAP):        {len(missing_routes)}')
print(f'   幽灵路由 (GHOST):      {len(missing_install)}')
print(f'   触发词不足15个:        {len(low_trigger)}')
print(f'   跨技能重复触发词:      {len(duplicates)}')
print(f'   总 li-* 路由条目:      {len(li_routes)}')
print(f'   总路由条目:            {len(routes)}')

total_triggers = sum(len(r.get('triggers',[])) for r in li_routes)
print(f'   总 li-* 触发词:        {total_triggers}')

# ============ 6. Sample E2E test cases ============
print(f'\n{"=" * 60}')
print('6. 端到端抽样测试 (10条真实用户消息)')
print('=' * 60)

test_cases = [
    ("帮我写一篇小红书帖子，主题是FPGA学习", ["li-xhs"]),
    ("这个FPGA代码的时序收敛不了，帮我看看", ["li-hardware"]),
    ("我想做一个深度调研，对比一下市场上的AI编程工具", ["li-research"]),
    ("帮我分析一下这篇文章的认知科学支撑", ["li-analyze"]),
    ("我觉得自己学不进去了，总是拖延", ["li-mindcoach"]),
    ("把这几个skill合并一下", ["li-skillfusion"]),
    ("昨天的工作做一个复盘", ["li-improve"]),
    ("帮我设计一个品牌视觉规范", ["li-design"]),
    ("把这段会议录音转成文字", ["li-transcript"]),
    ("帮我做一个PPT，答辩用", ["li-office"]),
]

def match_skills(message):
    """Simple trigger matching"""
    msg_lower = message.lower()
    matched = []
    for r in li_routes:
        for t in r.get('triggers', []):
            if t.lower() in msg_lower:
                matched.append(r['skill'])
                break
    return matched

for msg, expected in test_cases:
    matched = match_skills(msg)
    # Check if any expected skill is in matched
    hits = [e for e in expected if e in matched]
    status = '✅' if hits else '❌'
    print(f'   {status} "{msg}"')
    print(f'      期望: {expected}')
    print(f'      匹配: {matched}')
    if not hits:
        print(f'      ⚠️ 未命中期望技能!')
