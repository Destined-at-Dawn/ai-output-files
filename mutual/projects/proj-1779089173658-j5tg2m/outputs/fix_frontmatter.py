"""Add frontmatter to skills missing it"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

SKILLS = r"C:\Users\13975\.newmax\skills"

# Map: skill_name -> (description, version)
FIXES = {
    "li-bestskill": ("li系列 · 技能雷达，搜索外部最佳skill方案并评估", "1.0"),
    "li-competition": ("li系列 · 竞赛项目管理引擎，FPGA/电赛/数学建模全流程", "1.0"),
    "li-design": ("li系列 · 品牌视觉/UI设计/前端页面/设计系统", "1.0"),
    "li-image": ("li系列 · 图片生成与编辑（DALL-E/Gemini/信息图）", "1.0"),
    "li-manage": ("li系列 · 全局记忆与工作流管家，跨工作区协调", "1.0"),
    "li-office": ("li系列 · Office全栈处理（Word/Excel/PDF/PPT），已吸收li-pptx", "2.0"),
    "li-study": ("li系列 · 学习教练引擎（费曼+间隔重复+认知负荷）", "1.0"),
    "li-video": ("li系列 · 视频制作（AI故事/短视频/ffmpeg/TTS）", "1.0"),
    "li-web": ("li系列 · 网页开发（React/HTML/Vercel/仪表盘）", "1.0"),
    "li-wechat": ("li系列 · 公众号文章提取+分析+内容改写", "1.0"),
    "li-xhs": ("li系列 · 小红书内容创作（素人文/投流帖/文风DNA）", "1.0"),
    "karpathy-guidelines": ("Karpathy编程规范（100K+ stars），简洁性+外科手术式修改", "1.0"),
    "nature-skills": ("Nature期刊标准学术内容产出技能集", "1.0"),
}

for name, (desc, ver) in FIXES.items():
    path = os.path.join(SKILLS, name, "SKILL.md")
    if not os.path.exists(path):
        print(f"  SKIP {name}: SKILL.md not found")
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has frontmatter
    if content.startswith('---\n'):
        print(f"  SKIP {name}: already has frontmatter")
        continue

    # Build frontmatter
    frontmatter = f"---\nname: {name}\nversion: \"{ver}\"\ndescription: {desc}\n---\n\n"

    # Prepend to content
    new_content = frontmatter + content

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  FIXED: {name}")

print("\nDone.")
