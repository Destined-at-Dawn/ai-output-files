import os, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

rt_path = os.path.expanduser('~/.newmax/skill-routing-table.json')
with open(rt_path, 'r', encoding='utf-8') as f:
    rt = json.load(f)

routes = rt.get('routes', [])
existing_skills = set(r.get('skill', '') for r in routes)
skills_dir = os.path.expanduser('~/.newmax/skills')

need_route = [
    'li-analyze', 'li-dbs', 'li-design', 'li-image', 'li-infra', 'li-intent',
    'li-migrate', 'li-office', 'li-pptx', 'li-prompt', 'li-redesign', 'li-scaffold',
    'li-video', 'li-web', 'li-wechat', 'li-workspace', 'li-xhs'
]

trigger_map = {
    'li-analyze': ['分析文章', '深度分析', '道法术器', '拆解内容', '内容分析', '案例拆解', '百大认知', '认知科学分析', '分析这篇文章', '帮我分析', '深度拆解', '解析文章', '内容质量评估', '知识提炼', '信息提取', '观点分析', '逻辑分析', '分析报告'],
    'li-dbs': ['dbs', 'DBS框架', 'dbs-diagnosis', 'dbs-learning', 'dbs-goal', 'dbs-hook', 'dbs-save', '诊断框架', '深度诊断', '恢复框架', '目标设定'],
    'li-design': ['设计', 'UI设计', 'UX设计', '交互设计', '界面设计', '视觉设计', '设计规范', '设计系统', '排版', '布局设计', '配色方案', '设计语言'],
    'li-image': ['图片处理', '图像生成', 'P图', '修图', '压缩图片', '图片压缩', '图片格式转换', '裁剪图片', '图片编辑', '截图', '生成图片', 'AI画图', '图片优化', 'image'],
    'li-infra': ['基础设施', 'CLAUDE.md', 'memory管理', 'SOP管理', '路由表管理', '工作区配置', '约束文件', '系统维护', '基础设施维护', '工作区管理', '配置管理', '系统管理', 'infra'],
    'li-intent': ['意图理解', '意图识别', '自动路由', 'SOP路由', '任务分流', '消息路由', '意图匹配', '自动触发', '智能路由', '任务理解', 'intent'],
    'li-migrate': ['迁移', '工作台迁移', '数据迁移', '项目迁移', '环境迁移', '备份恢复', '系统迁移', '迁移项目', '搬数据', '迁移到新环境', 'agent迁移', 'migrate'],
    'li-office': ['Office', 'Word文档', 'Excel表格', '文档处理', '表格处理', 'docx', 'xlsx', 'csv', '数据表', '电子表格', '文档转换', 'office'],
    'li-pptx': ['PPT', '演示文稿', '幻灯片', '做PPT', '制作PPT', 'PPT模板', 'slides', 'presentation', '汇报PPT', '课件', '演示', 'pptx'],
    'li-prompt': ['写提示词', 'prompt设计', '提示词优化', 'prompt工程', '跨平台提示词', 'GPT提示词', 'Claude提示词', '系统提示词', '提示词模板', 'prompt', '提示词', '系统指令', 'system prompt'],
    'li-redesign': ['重构项目', '项目重构', '优化项目', '改造项目', '重写项目', '代码重构', '架构重构', '项目升级', '项目翻新', 'refactor', 'redesign'],
    'li-scaffold': ['创建工作区', '初始化项目', '项目脚手架', '新建项目', '项目模板', '工作区模板', '搭建环境', '初始化环境', '新建工作区', 'scaffold', 'bootstrap'],
    'li-video': ['视频', '视频处理', '视频剪辑', '视频转码', '字幕', '字幕生成', '视频下载', '视频压缩', '视频格式', '视频编辑', 'ffmpeg', 'video'],
    'li-web': ['网页', '网站', '爬虫', '网页采集', '网页抓取', '网页截图', '网页转PDF', 'URL解析', '网页分析', 'WebFetch', '网页内容', 'web'],
    'li-wechat': ['微信', '公众号', '微信文章', '公众号文章', '微信采集', '公众号分析', '微信数据', '公众号运营', '微信导出', 'wechat'],
    'li-workspace': ['工作区操作', '整理工作区', '工作区迁移', '工作区重构', '工作区搭建', 'workspace', '环境搭建', '项目整理', '归档项目', '清理工作区'],
    'li-xhs': ['小红书', '小红书帖子', '小红书文案', '小红书标题', '小红书运营', '小红书内容', '小红书爆款', '小红书选题', 'xhs', 'rednote', '种草', '笔记'],
}

name_map = {
    'li-analyze': 'li-analyze 深度分析引擎',
    'li-dbs': 'li-dbs DBS框架',
    'li-design': 'li-design 设计能力',
    'li-image': 'li-image 图像处理',
    'li-infra': 'li-infra 基础设施管理',
    'li-intent': 'li-intent 意图理解',
    'li-migrate': 'li-migrate 工作台迁移',
    'li-office': 'li-office 办公文档',
    'li-pptx': 'li-pptx 演示文稿',
    'li-prompt': 'li-prompt Prompt构建',
    'li-redesign': 'li-redesign 项目重构',
    'li-scaffold': 'li-scaffold 工作区脚手架',
    'li-video': 'li-video 视频处理',
    'li-web': 'li-web 网页工具',
    'li-wechat': 'li-wechat 微信生态',
    'li-workspace': 'li-workspace 工作区操作',
    'li-xhs': 'li-xhs 小红书运营',
}

new_routes = []
max_id = max(int(r['id'][1:]) for r in routes)

for skill in need_route:
    if skill in existing_skills:
        print(f"SKIP {skill} (already has route)")
        continue
    max_id += 1
    new_routes.append({
        'id': f'r{max_id:03d}',
        'name': name_map.get(skill, skill),
        'skill': skill,
        'triggers': trigger_map.get(skill, [skill]),
        'priority': 5,
        'auto': True,
        'confidence': 0.9,
        'note': ''
    })

routes.extend(new_routes)
rt['routes'] = routes

with open(rt_path, 'w', encoding='utf-8') as f:
    json.dump(rt, f, ensure_ascii=False, indent=2)

print(f"\nAdded {len(new_routes)} routes:")
for r in new_routes:
    print(f"  {r['id']} -> {r['skill']} ({len(r['triggers'])} triggers)")

# Verify
all_li = set(r['skill'] for r in routes if r['skill'].startswith('li-'))
skills_li = set(d for d in os.listdir(skills_dir) if d.startswith('li-') and os.path.isdir(os.path.join(skills_dir, d)))
unrouted = skills_li - all_li
print(f"\nUnrouted: {unrouted if unrouted else 'NONE'}")
print(f"Total routes: {len(routes)}, li- routes: {len([r for r in routes if r['skill'].startswith('li-')])}")
