# -*- coding: utf-8 -*-
"""Clean visual emoji from niuma-engine rule files.
Rules: 📋🔴🟡🟢❓ → text markers. Keep: ❌✅✗✓⚠⛔⚡"""
import os

REPO = r"C:\Users\13975\AppData\Local\Temp\niuma-engine"
RULES = os.path.join(REPO, ".claude", "rules")

# Map: filename → list of (old_string, new_string)
FIXES = {
    "memory-candidate-protocol.md": [
        ("📋 记忆候选", "记忆候选"),
    ],
    "anti-info-overload.md": [
        ("🔴 关键/必须", "`[CRITICAL]` 关键/必须"),
        ("🟡 重要/建议", "`[WARN]` 重要/建议"),
        ("🟢 可选/参考", "`[OK]` 可选/参考"),
    ],
    "lifecycle-sop.md": [
        ("🔴 致命", "`[FATAL]` 致命"),
    ],
    "boundary-declaration.md": [
        ("❓ 尚不能声称", "`[UNKNOWN]` 尚不能声称"),
    ],
}

for fname, replacements in FIXES.items():
    path = os.path.join(RULES, fname)
    if not os.path.exists(path):
        print(f"  [MISSING] {fname}")
        continue
    with open(path, encoding="utf-8") as f:
        content = f.read()
    changed = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  [FIX] {fname}: '{old}' -> '{new}'")
            changed = True
        else:
            print(f"  [NOT FOUND] {fname}: '{old}'")
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

# Remove stray variation selectors (U+FE0F) from all rule files
for fname in os.listdir(RULES):
    if not fname.endswith(".md"):
        continue
    path = os.path.join(RULES, fname)
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if '️' in content:
        content = content.replace('️', '')
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [VS16] {fname}: removed variation selectors")

print("\nAll emoji cleaned.")
