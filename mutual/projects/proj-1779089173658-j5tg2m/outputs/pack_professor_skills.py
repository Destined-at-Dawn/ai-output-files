import zipfile
import os
import shutil

skills_root = r"C:\Users\13975\.newmax\skills"
output_zip = r"E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\professor_skills.zip"

# 图片中展示的全部技能（按分类）
skills_to_pack = [
    # 2 项目管理与竞赛
    "li-competition", "li-plan", "li-triage", "li-workflow",
    # 3 AI编程与调试
    "li-code", "li-debug", "li-script", "li-web", "li-webtest", "li-hardware", "li-embedded",
    # 4 学习与研究
    "li-research", "li-study", "li-mindcoach", "li-industry",
    # 5 决策与分析
    "li-analyze", "li-devil", "li-diagnose", "li-intent",
    # 7 工作区运维
    "li-improve", "li-memory", "li-manage", "li-sync", "li-infra", "li-workspace", "li-zhongshu",
    # 8 技能生态
    "li-skillcreate", "li-skillfusion", "li-skills-mgmt", "li-bestskill",
    # 10 办公与通用
    "li-office", "li-prompt", "li-package",
    # 11 本地搜索与迁移
    "li-local-search", "li-dbs",
]

missing = []
packed = []

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for skill in skills_to_pack:
        skill_path = os.path.join(skills_root, skill)
        if not os.path.exists(skill_path):
            missing.append(skill)
            continue
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join("professor_skills", skill, os.path.relpath(file_path, skill_path))
                zf.write(file_path, arcname)
        packed.append(skill)

print(f"[OK] 打包完成: {output_zip}")
print(f"[OK] 成功打包 {len(packed)} 个技能:")
for s in packed:
    print(f"  - {s}")
if missing:
    print(f"[WARN] 以下技能目录不存在，已跳过:")
    for s in missing:
        print(f"  - {s}")

zip_size = os.path.getsize(output_zip)
print(f"[OK] ZIP文件大小: {zip_size / 1024 / 1024:.2f} MB")
