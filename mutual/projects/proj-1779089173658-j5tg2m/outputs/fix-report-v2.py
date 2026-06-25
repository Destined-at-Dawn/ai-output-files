#!/usr/bin/env python3
"""Comprehensive number correction for skill-bloat-analysis report."""
import os

report_path = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\skill-bloat-analysis-2026-06-22.md'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track changes
changes = []

for i, line in enumerate(lines):
    original = line

    # Fix "16 弃用路由" -> "14 弃用路由" (but NOT in the 数据验真声明 table where it's already correct)
    # Only fix in narrative sections, not in the 初报错误 table
    if '16 个已弃用' in line and '初报' not in line:
        lines[i] = line.replace('16 个已弃用', '14 个已弃用')
        changes.append(f'L{i+1}: "16 个已弃用" -> "14 个已弃用"')

    if '16 弃用路由' in line and '清除' in line:
        lines[i] = line.replace('16 弃用路由', '14 弃用路由')
        changes.append(f'L{i+1}: "16 弃用路由" -> "14 弃用路由"')

    if '| 清除 16 个弃用' in line:
        lines[i] = line.replace('16', '14')
        changes.append(f'L{i+1}: table "16" -> "14"')

    if '1. 先清除 16 个弃用' in line:
        lines[i] = line.replace('16', '14')
        changes.append(f'L{i+1}: "先清除 16" -> "先清除 14"')

    # Fix "109" -> "107" in contexts where it refers to active skills
    # But NOT in the 数据验真声明 table (already correct)
    if '| 预期净减' in line and '109' in line:
        lines[i] = line.replace('109', '107')
        changes.append(f'L{i+1}: "109" -> "107" in 预期净减')

    # Fix table row where old value still shows 16
    if '| 有路由的弃用 skill' in line and '| **16** |' in line:
        lines[i] = line.replace('| **16** |', '| **14** |')
        changes.append(f'L{i+1}: table "16" -> "14" for 有路由的弃用 skill')

with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Made {len(changes)} corrections:')
for c in changes:
    print(f'  {c}')

# Verify
with open(report_path, 'r', encoding='utf-8') as f:
    final = f.read()

# Check for remaining "16" near "弃用"
remaining_16 = []
for i, line in enumerate(final.split('\n'), 1):
    if '16' in line and ('弃用' in line or '死代码' in line or '弃用路由' in line):
        if '初报' not in line and '修正' not in line and '数据验真' not in line:
            remaining_16.append(f'L{i}: {line.strip()}')

if remaining_16:
    print(f'\nWARNING: {len(remaining_16)} remaining "16" near 弃用:')
    for r in remaining_16:
        print(f'  {r}')
else:
    print('\nNo remaining "16" near 弃用 found - clean!')

# Check for remaining "109" near active skills
remaining_109 = []
for i, line in enumerate(final.split('\n'), 1):
    if '109' in line and ('活跃' in line or 'skill' in line.lower()):
        if '初报' not in line and '修正' not in line:
            remaining_109.append(f'L{i}: {line.strip()}')

if remaining_109:
    print(f'\nWARNING: {len(remaining_109)} remaining "109":')
    for r in remaining_109:
        print(f'  {r}')
else:
    print('No remaining "109" found - clean!')

print(f'\nFinal size: {os.path.getsize(report_path)} bytes')
