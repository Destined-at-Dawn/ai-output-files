# -*- coding: utf-8 -*-
"""Delete 9 fabricated shell skills and clean routing table."""
import os, json, shutil

BASE = os.path.expanduser(r"~\.newmax\skills")
RT_PATH = os.path.expanduser(r"~\.newmax\skills\skill-routing-table.json")
BACKUP = r"E:\ai产出文件\牛马\归档\2026-06-10-9-fabricated-shells"

SHELLS = [
    "li-session", "li-voice", "li-search", "li-personal",
    "li-writing", "li-docs", "li-frontend", "li-platform", "li-intent"
]

# 1. Archive then delete
os.makedirs(BACKUP, exist_ok=True)
for name in SHELLS:
    src = os.path.join(BASE, name)
    if os.path.isdir(src):
        dst = os.path.join(BACKUP, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        shutil.rmtree(src)
        print(f"ARCHIVED+DELETED: {name}")
    else:
        print(f"SKIP: {name} not found")

# 2. Clean routing table
if os.path.exists(RT_PATH):
    with open(RT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original = len(data.get("routes", []))
    data["routes"] = [r for r in data.get("routes", [])
                      if r.get("skill") not in SHELLS]
    new_count = len(data["routes"])

    with open(RT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"RT: {original} -> {new_count} (-{original - new_count})")
else:
    print("RT: not found")

# 3. List remaining
remaining = sorted([d for d in os.listdir(BASE)
                    if os.path.isdir(os.path.join(BASE, d))
                    and not d.startswith('.')
                    and os.path.exists(os.path.join(BASE, d, "SKILL.md"))])
print(f"\nREMAINING ({len(remaining)}):")
for r in remaining:
    print(f"  {r}")
