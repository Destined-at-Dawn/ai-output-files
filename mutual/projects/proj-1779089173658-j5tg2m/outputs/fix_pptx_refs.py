"""Fix li-pptx references → li-office in other skills"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

SKILLS_DIR = r"C:\Users\13975\.newmax\skills"

REPLACEMENTS = {
    "li-design/SKILL.md": [
        ("- li-pptx: 演示文稿设计", "- li-office: 演示文稿/PPT设计（已吸收 li-pptx）"),
    ],
    "li-image/SKILL.md": [
        ("- li-pptx: PPT配图需求", "- li-office: PPT配图需求（已吸收 li-pptx）"),
    ],
    "li-video/SKILL.md": [
        ('触发: "把答辩PPT做成视频" → li-video + li-pptx → 路径D 剪映编辑',
         '触发: "把答辩PPT做成视频" → li-video + li-office → 路径D 剪映编辑'),
        ("- li-pptx: PPT转视频", "- li-office: PPT转视频（已吸收 li-pptx）"),
    ],
}

for rel_path, replacements in REPLACEMENTS.items():
    full_path = os.path.join(SKILLS_DIR, rel_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  {rel_path}: replaced '{old[:40]}...'")
        else:
            print(f"  {rel_path}: NOT FOUND '{old[:40]}...'")

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("\nDone.")
