#!/usr/bin/env python3
"""Trim 5 skills that went over 300 lines"""
import os

base = os.path.expanduser(os.path.join('~', '.newmax', 'skills'))
over = ['li-hardware', 'li-industry', 'li-skillcreate', 'li-sync', 'li-webtest']

for name in over:
    path = os.path.join(base, name, 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    excess = len(lines) - 300
    if excess <= 0:
        print(f'{name}: {len(lines)}L OK')
        continue

    # Strategy: remove last "禁忌" section's last N lines (they're the least important)
    # Find the 禁忌 section and trim its tail
    forbidden_start = -1
    for i, line in enumerate(lines):
        if '## 禁忌' in line or '## Forbidden' in line:
            forbidden_start = i
            break

    if forbidden_start > 0:
        # Remove the last N lines from forbidden section
        end = len(lines)
        # Find the end of forbidden section (next ## or EOF)
        for i in range(forbidden_start + 1, len(lines)):
            if lines[i].startswith('## ') and i > forbidden_start + 1:
                end = i
                break

        # Trim from the end of forbidden section
        trim_start = max(forbidden_start + 1, end - excess)
        lines = lines[:trim_start] + lines[end:]
    else:
        # Fallback: trim from end
        lines = lines[:300]

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'{name}: {len(lines)}L (trimmed {excess} lines)')
