# -*- coding: utf-8 -*-
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\ai产出文件\牛马\mutual\mutual\skill-routing-table.json', 'r', encoding='utf-8') as f:
    routes = json.load(f)['routes']

# ============================================================
# CRITICAL FINDING: li-docs IS doc-coauthoring
# ============================================================
print('=' * 60)
print('FATAL FINDING: li-docs = doc-coauthoring')
print('=' * 60)
print('li-docs SKILL.md frontmatter says: name: doc-coauthoring')
print('doc-coauthoring SKILL.md frontmatter says: name: doc-coauthoring')
print('They are the SAME SKILL with different directory names.')
print()

# ============================================================
# doc-coauthoring route analysis
# ============================================================
for r in routes:
    if r.get('skill') == 'doc-coauthoring':
        print('doc-coauthoring (r038):')
        print(f'  Priority: {r["priority"]}, Auto: {r["auto"]}, Confidence: {r["confidence"]}')
        print(f'  Triggers ({len(r["triggers"])}):')
        for t in r['triggers']:
            print(f'    "{t}"')

# ============================================================
# Full ecosystem analysis
# ============================================================
li_routed = []
for r in routes:
    s = r.get('skill','')
    if s.startswith('li-'):
        li_routed.append(s)

li_routed = list(set(li_routed))

# What user tasks does each handle?
task_map = {
    '深度调研': 'li-research',
    '翻译': 'li-research',
    '竞品分析': 'li-research',
    'FPGA/硬件': 'li-hardware',
    '内容分析': 'li-analyze',
    '道法术器': 'li-analyze',
    '自我改进': 'li-improve',
    '教训记录': 'li-improve',
    '记忆管理': 'li-memory + li-manage',
    '系统诊断': 'li-diagnose',
    'Bug调试': 'li-debug',
    '任务分流': 'li-triage',
    'Skill创建': 'li-skillcreate',
    'Skill搜索': 'li-bestskill',
    '本地工具': 'li-local-search',
    'Skill融合': 'li-skillfusion',
    'Skill管理': 'li-skills-mgmt',
    '跨区同步': 'li-sync',
    '工作流': 'li-workflow',
    '会议转录': 'li-transcript',
    '心理教练': 'li-mindcoach',
    '决策质疑': 'li-devil',
    '行业研究': 'li-industry',
    '任务规划': 'li-plan',
    'Web测试': 'li-webtest',
    '视频脚本': 'li-storyboard',
    '视觉风格': 'li-visual',
    '基础设施': 'li-infra',
    'Prompt设计': 'li-prompt',
    '竞赛管理': 'li-competition',
    '学习教练': 'li-study',
    '决策框架': 'li-dbs',
    '数据分析': 'li-data',
    '小红书': 'li-xhs',
    '公众号/微信': 'li-wechat',
    '办公文档': 'li-office',
    'Web开发': 'li-web',
    '设计': 'li-design',
    '图片': 'li-image',
    '视频': 'li-video',
    '代码': 'li-code',
    '意图路由': 'li-intent',
    '工作区': 'li-workspace',
    '文档共创': 'doc-coauthoring (NON-li-)',
    '飞书文档': 'feishu-doc-reader (NON-li-)',
    '内部沟通': 'internal-comms (NON-li-)',
    '每日复盘': 'daily-review (NON-li-)',
    '学术写作': 'blog-post-writer (NON-li-)',
    'Karpathy编码': 'karpathy-guidelines (NON-li-)',
}

print(f'\n{"=" * 60}')
print(f'FULL ECOSYSTEM COVERAGE')
print(f'{"=" * 60}')
print(f'Total routed skills: {len(set(r.get("skill") for r in routes))}')
print(f'Total li-* skills with routes: {len(li_routed)}')
print(f'Total non-li-* skills with routes: {len(set(r.get("skill") for r in routes if not r["skill"].startswith("li-")))}')
print(f'Total triggers (all): {sum(len(r.get("triggers",[])) for r in routes)}')
print(f'Total li-* triggers: {sum(len(r.get("triggers",[])) for r in routes if r["skill"].startswith("li-"))}')

# Coverage check
print(f'\n{"=" * 60}')
print(f'COVERAGE GAPS AUDIT')
print(f'{"=" * 60}')
coverage = set()
for r in routes:
    if r.get('skill','').startswith('li-'):
        coverage.add(r['skill'])
for r in routes:
    if not r.get('skill','').startswith('li-'):
        coverage.add(r['skill'])

# What tasks do real users actually say?
real_tasks = [
    '帮我写文档',      # → doc-coauthoring (r038)
    '帮我做PPT',        # → li-office (r115)
    '帮我分析这篇文章', # → li-analyze (r108)
    '帮我搜一下',       # → li-research (r083)
    '小红书怎么写标题', # → li-xhs (r110)
    '这个FPGA代码有问题',# → li-hardware (r100)
    '我有点焦虑',       # → li-mindcoach (r091)
    '帮我创建一个skill',# → li-skillcreate (r086)
    '帮我整理会议记录', # → li-transcript (r085)
    '做个深度调研',     # → li-research (r083)
    '帮我同步一下工作区',# → li-sync (r087)
    '帮我做数据可视化', # → li-data (r200) or li-office (r115)
    '帮我做网页',       # → li-web (r112)
    '帮我设计logo',     # → li-design (r111)
    '帮我做视频',       # → li-video (r114)
    '帮我修bug',        # → li-debug (r102)
    '帮我做行业分析',   # → li-industry (r093)
    '帮我做视频分镜',   # → li-storyboard (r098)
    '帮我生成图片',     # → li-image (r113)
    '帮我写代码',       # → li-code (r210)
    '帮我分配任务优先级',# → li-triage (r103)
    '帮我做学习计划',   # → li-study (r294)
    '帮我优化prompt',   # → li-prompt (r105)
    '帮我分析竞品',     # → li-research (r083)
    '帮我做风险评估',   # → li-devil (r084)
    '帮我做职业规划',   # → internal-comms (r032) — wait no
    '帮我写简历',       # → NO ROUTE!
    '帮我写求职邮件',   # → internal-comms (r032) has '求职邮件'
    '帮我润色文章',     # → NO ROUTE! (li-writing is GAP)
    '帮我生成漫画',     # → baoyu-comic (r129)
    '帮我做算法艺术',   # → algorithmic-art (r137)
]

print('\nReal user tasks vs coverage:')
for task in real_tasks:
    matched = []
    for r in routes:
        for t in r.get('triggers',[]):
            if t in task:
                matched.append(r['skill'])
                break
    if matched:
        print(f'  OK   "{task}" -> {", ".join(matched[:2])}')
    else:
        print(f'  GAP  "{task}" -> NO ROUTE MATCH')

print(f'\n{"=" * 60}')
print(f'CONCLUSION')
print(f'{"=" * 60}')
print()
print('li-docs 不需要路由。理由：')
print('  1. li-docs SKILL.md frontmatter says: name: doc-coauthoring')
print('  2. doc-coauthoring (r038) already has 15 triggers, priority 1')
print('  3. They are the SAME skill — li-docs is just a li- wrapper')
print('  4. Registering li-docs would create duplicate triggers with doc-coauthoring')
print()
print('10个GAP技能的最终裁决：')
print('  li-docs       → SKIP (= doc-coauthoring)')
print('  li-autoreply  → SKIP (81% overlap with li-persona-qa, merge first)')
print('  li-persona-qa → SKIP (same)')
print('  li-personal   → DECIDE (独立价值: 简历/面试/考研)')
print('  li-writing    → DECIDE (独立价值: 跨平台写作协调器, 3真实案例)')
print('  li-frontend   → SKIP (= li-web)')
print('  li-platform   → SKIP (= li-wechat)')
print('  li-search     → SKIP (triple covered)')
print('  li-session    → SKIP (triple covered)')
print('  li-voice      → SKIP (zero cases, = li-writing)')
print()
print('真正需要决策的只有2个：li-personal 和 li-writing')
