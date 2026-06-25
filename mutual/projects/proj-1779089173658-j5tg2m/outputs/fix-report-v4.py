#!/usr/bin/env python3
"""Fix remaining issues in skill-bloat-analysis report."""
import os

report_path = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\skill-bloat-analysis-2026-06-22.md'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = []

for i, line in enumerate(lines):
    # L96: "16 个已弃用的" (without "skill" after it)
    if '16 个已弃用的' in line:
        lines[i] = line.replace('16 个已弃用的', '14 个已弃用的')
        changes.append(f'L{i+1}: "16 个已弃用的" -> "14 个已弃用的"')

with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Made {len(changes)} corrections:')
for c in changes:
    print(f'  {c}')

# Final verification
with open(report_path, 'r', encoding='utf-8') as f:
    final = f.read()

# Check all remaining "16" near "弃用" (excluding file sizes like 16.6 KB)
for i, line in enumerate(final.split('\n'), 1):
    if '弃用' in line and '16' in line:
        if 'KB' not in line and '16.' not in line:
            print(f'STILL WRONG L{i}: {line.strip()[:100]}')

# Note: L32 "| 活跃 skill 数 | 109 | **107**" is correct - it's a comparison table showing old vs new

print(f'\nFinal size: {os.path.getsize(report_path)} bytes')
