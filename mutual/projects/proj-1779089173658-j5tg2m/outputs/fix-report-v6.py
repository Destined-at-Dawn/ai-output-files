#!/usr/bin/env python3
"""Final comprehensive fix for all remaining number inconsistencies."""
import os

report_path = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\skill-bloat-analysis-2026-06-22.md'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = []

for i, line in enumerate(lines):
    # L346: "16 死路由" -> "14 死路由"
    if '16 死路由' in line:
        lines[i] = line.replace('16 死路由', '14 死路由')
        changes.append(f'L{i+1}: "16 死路由" -> "14 死路由"')

    # L325: "清除弃用的 15 个" -> "清除弃用的 14 个"
    if '清除弃用的 15 个' in line:
        lines[i] = line.replace('15 个', '14 个')
        changes.append(f'L{i+1}: "清除弃用的 15 个" -> "清除弃用的 14 个"')

    # Also check for "15 个" near "弃用" more broadly
    if '弃用' in line and '15' in line and '15.' not in line:
        if 'KB' not in line:
            # This is L325 area
            if '15 个' in line:
                lines[i] = line.replace('15 个', '14 个')
                changes.append(f'L{i+1}: "15 个" -> "14 个" (near 弃用)')

with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Made {len(changes)} corrections:')
for c in changes:
    print(f'  {c}')

# Final verification - check ALL remaining number issues
with open(report_path, 'r', encoding='utf-8') as f:
    final = f.read()

print('\n--- Checking all numbers near "弃用" ---')
for i, line in enumerate(final.split('\n'), 1):
    if '弃用' in line and any(x in line for x in ['16', '15']):
        if 'KB' not in line and '16.' not in line and '15.' not in line:
            if '初报' not in line and '修正' not in line and '数据验真' not in line:
                print(f'  L{i}: {line.strip()[:100]}')

print('\n--- Checking "死路由" ---')
for i, line in enumerate(final.split('\n'), 1):
    if '死路由' in line:
        print(f'  L{i}: {line.strip()[:100]}')

print(f'\nFinal size: {os.path.getsize(report_path)} bytes')
