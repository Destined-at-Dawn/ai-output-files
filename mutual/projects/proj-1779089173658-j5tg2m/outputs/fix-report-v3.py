#!/usr/bin/env python3
"""Final correction pass for skill-bloat-analysis report."""
import os

report_path = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\skill-bloat-analysis-2026-06-22.md'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = []

for i, line in enumerate(lines):
    original = line

    # L19: "16 弃用路由" -> "14 弃用路由"
    if '16 弃用路由' in line:
        lines[i] = line.replace('16 弃用路由', '14 弃用路由')
        changes.append(f'L{i+1}: "16 弃用路由" -> "14 弃用路由"')

    # L33: table with "| 弃用 skill 有路由 | 16 | **14" -> fix the left column
    if '| 弃用 skill 有路由' in line and '| 16 |' in line:
        lines[i] = line.replace('| 16 |', '| **14** |')
        changes.append(f'L{i+1}: table old-value "16" -> "14"')

    # L75: "16 项" -> "14 项"
    if '死代码路由（16 项）' in line:
        lines[i] = line.replace('16 项', '14 项')
        changes.append(f'L{i+1}: "16 项" -> "14 项"')

    # L96: "16 个已弃用的 skill" -> "14"
    if '16 个已弃用的 skill' in line:
        lines[i] = line.replace('16 个已弃用的', '14 个已弃用的')
        changes.append(f'L{i+1}: "16 个已弃用的" -> "14 个已弃用的"')

    # L316: "109→102" -> "107→100"
    if '109→102' in line:
        lines[i] = line.replace('109→102', '107→100')
        changes.append(f'L{i+1}: "109→102" -> "107→100"')

    # Also fix "109 个活跃" -> "107 个活跃" anywhere
    if '109 个活跃' in line:
        lines[i] = line.replace('109 个活跃', '107 个活跃')
        changes.append(f'L{i+1}: "109 个活跃" -> "107 个活跃"')

with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f'Made {len(changes)} corrections:')
for c in changes:
    print(f'  {c}')

# Final verification
with open(report_path, 'r', encoding='utf-8') as f:
    final = f.read()

# Check for remaining problems
issues = []
for i, line in enumerate(final.split('\n'), 1):
    # 16 near 弃用 (but not file sizes like 16.6 KB or 16.3 KB)
    if '弃用' in line and '16' in line:
        # Skip if it's clearly a file size
        if 'KB' not in line and '16.' not in line:
            issues.append(f'L{i}: {line.strip()[:80]}')

if issues:
    print(f'\nREMAINING ISSUES ({len(issues)}):')
    for iss in issues:
        print(f'  {iss}')
else:
    print('\nAll "16 near 弃用" issues resolved!')

# Check for remaining 109
for i, line in enumerate(final.split('\n'), 1):
    if '109' in line and 'skill' in line.lower():
        if '初报' not in line and '修正' not in line:
            print(f'Remaining 109 at L{i}: {line.strip()[:80]}')

print(f'\nFinal size: {os.path.getsize(report_path)} bytes')
