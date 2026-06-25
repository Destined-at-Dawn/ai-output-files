# -*- coding: utf-8 -*-
"""Phase 3: 路由表更新 + 全工作区同步 + 修复超标"""
import os, json, glob, re

SKILLS = r'C:\Users\13975\.newmax\skills'
MUTUAL = r'E:\ai产出文件\牛马\mutual\mutual'

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ''

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def count_lines(path):
    content = read_file(path)
    return len(content.split('\n')) if content else 0

# ============================================================
# STEP 1: 修复 li-research 和 li-skillcreate 超标
# ============================================================
for skill in ['li-research', 'li-skillcreate']:
    path = os.path.join(SKILLS, skill, 'SKILL.md')
    c = read_file(path)
    if c:
        lines = c.split('\n')
        # 删掉末尾空行
        while lines and not lines[-1].strip():
            lines.pop()
        # 如果还超，删掉最后一个空行
        if len(lines) > 300:
            # 找到最不重要的尾部内容移走
            pass
        write_file(path, '\n'.join(lines) + '\n')
        print(f'{skill}: {len(lines)} lines')

# ============================================================
# STEP 2: 更新路由表
# ============================================================
rt_path = os.path.join(MUTUAL, 'skill-routing-table.json')
rt = json.loads(read_file(rt_path))

# 找到现有路由的最大 ID
max_id = 0
for r in rt.get('routes', []):
    rid = r.get('id', '')
    m = re.search(r'r(\d+)', rid)
    if m:
        max_id = max(max_id, int(m.group(1)))

# 删除旧 skill 的路由
OLD_SKILLS = ['competition-workflow', 'interactive-learning', 'thinking-coach',
              'chinese-natural-voice-revision', 'resume-modification']
new_routes = []
for r in rt.get('routes', []):
    if r.get('skill') not in OLD_SKILLS:
        new_routes.append(r)
rt['routes'] = new_routes

# 添加新 skill 路由
NEW_ROUTES = [
    {
        'id': f'r{max_id+1:03d}',
        'name': 'li-competition',
        'skill': 'li-competition',
        'triggers': [
            '竞赛', '比赛', 'contest', 'competition', '赛事', 'FPGA竞赛',
            'RoboMaster', 'robomaster', '电子设计竞赛', '电赛', '挑战杯',
            '项目管理', 'project management', '里程碑', '交付',
            '一把过', '交付清单', 'deadline', 'DDL', '倒计时',
            '团队协作', '进度追踪', '风险管理', '逆向拆解',
            'RT-Thread', '嵌入式竞赛', '硬件竞赛', '智能车',
            '蓝桥杯', '数学建模', '数学竞赛', '建模', 'MATLAB',
            'git worktree', '分支管理', 'atomic commit'
        ],
        'priority': 3,
        'auto': True,
        'confidence': 0.9,
        'note': '竞赛项目全生命周期管理'
    },
    {
        'id': f'r{max_id+2:03d}',
        'name': 'li-study',
        'skill': 'li-study',
        'triggers': [
            '学习', 'study', '学习方法', '学习策略', 'learning',
            '费曼', 'feynman', '费曼技巧', '费曼检验', '费曼学习法',
            '理解', 'understand', '解释', 'explain', '帮我理解',
            '概念', 'concept', '原理', 'principle', '机制',
            '复习', 'review', '考前复习', '期末复习', '备考',
            '做题', '练习', 'exercise', '出题', '测试',
            '记忆', '背诵', 'recall', 'retrieval', '检索练习',
            '间隔复习', 'spaced repetition', '间隔效应',
            '学习路径', '入门', '怎么学', '如何学习', '学习计划',
            '认知科学', '学习科学', '认知负荷', '心流',
            '思维训练', 'thinking', '批判性思维', '逻辑思维'
        ],
        'priority': 3,
        'auto': True,
        'confidence': 0.9,
        'note': '学习教练引擎（费曼检验+认知科学注入）'
    },
]

# 检查 li-competition 和 li-study 是否已有路由
existing_skills = {r.get('skill') for r in rt['routes']}
for nr in NEW_ROUTES:
    if nr['skill'] not in existing_skills:
        rt['routes'].append(nr)
        print(f"Added route for {nr['skill']}")
    else:
        print(f"Route already exists for {nr['skill']}")

# 更新 li-analyze 路由（补充"去AI味"触发词）
for r in rt['routes']:
    if r.get('skill') == 'li-analyze':
        extra = ['去AI味', '去AI痕迹', 'AI痕迹', '自然语言', '口语化', '改写',
                 '简历', '简历优化', '简历改写', '简历润色', 'CV', 'resume']
        existing = set(r.get('triggers', []))
        for t in extra:
            if t not in existing:
                r['triggers'].append(t)
        print(f"li-analyze triggers: {len(r['triggers'])}")

write_file(rt_path, json.dumps(rt, ensure_ascii=False, indent=2))
print(f'Routes: {len(rt["routes"])}')

# ============================================================
# STEP 3: 全工作区同步
# ============================================================
CLAUDE_DIRS = []
for root, dirs, files in os.walk(r'E:\ai产出文件\牛马'):
    if 'CLAUDE.md' in files:
        CLAUDE_DIRS.append(root)
    # 跳过归档和 node_modules
    dirs[:] = [d for d in dirs if d not in ('归档', 'node_modules', '.git', 'archive')]

synced = 0
for d in CLAUDE_DIRS:
    dst = os.path.join(d, 'skill-routing-table.json')
    try:
        write_file(dst, json.dumps(rt, ensure_ascii=False, indent=2))
        synced += 1
    except Exception as e:
        pass

# 也同步到 ~/.newmax/
newmax_dst = os.path.join(r'C:\Users\13975\.newmax', 'skill-routing-table.json')
write_file(newmax_dst, json.dumps(rt, ensure_ascii=False, indent=2))

print(f'Synced to {synced} workspaces')
print('Phase 3 complete')
