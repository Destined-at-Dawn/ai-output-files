#!/usr/bin/env python3
"""Fix L96 - add specific count to data-analysis reference."""
import os

report_path = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\skill-bloat-analysis-2026-06-22.md'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'data-analysis skill（r168）' in line and '已弃用' in line:
        old = '已弃用的 data-analysis skill（r168）'
        new = '已弃用的 data-analysis skill（r168，14 个弃用路由之一）'
        lines[i] = line.replace(old, new)
        print(f'L{i+1}: Added count to data-analysis reference')
        break

with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Final verification
with open(report_path, 'r', encoding='utf-8') as f:
    final = f.read()

# Check for any remaining issues
print('\n--- Final check ---')
for i, line in enumerate(final.split('\n'), 1):
    if '弃用' in line and '16' in line:
        if 'KB' not in line and '16.' not in line:
            print(f'L{i}: {line.strip()[:100]}')

print('Done!')
print(f'Size: {os.path.getsize(report_path)} bytes')
