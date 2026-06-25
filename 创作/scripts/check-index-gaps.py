#!/usr/bin/env python3
"""检查 INDEX.md 是否覆盖所有教训文件（零缺口验证）
用法：
  python scripts/check-index-gaps.py          # 检查并报告
  python scripts/check-index-gaps.py --quiet  # 只输出摘要

设计原则：
  - 纯 Python，避免 bash 中文路径编码问题
  - 输出 UTF-8
  - 返回非零 exit code 当有缺口时（可集成到 CI/门禁）
"""

import os, sys
from datetime import datetime

ROOT = r'E:\ai产出文件\牛马\创作\创作\自我进化'
INDEX_PATH = os.path.join(ROOT, 'INDEX.md')

def check():
    if not os.path.exists(INDEX_PATH):
        print(f'[FAIL] INDEX.md not found: {INDEX_PATH}')
        return 1

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        idx_content = f.read()

    gaps = []

    # 检查失败教训
    fail_dir = os.path.join(ROOT, '做得差的避免')
    if os.path.exists(fail_dir):
        for f in os.listdir(fail_dir):
            if f.endswith('.md'):
                if f not in idx_content:
                    gaps.append(('失败教训', f))

    # 检查成功案例
    good_dir = os.path.join(ROOT, '做得好的')
    if os.path.exists(good_dir):
        for f in os.listdir(good_dir):
            if f.endswith('.md'):
                if f not in idx_content:
                    gaps.append(('成功案例', f))

    quiet = '--quiet' in sys.argv

    total_files = 0
    for d in [fail_dir, good_dir]:
        if os.path.exists(d):
            total_files += len([f for f in os.listdir(d) if f.endswith('.md')])

    if not quiet:
        print(f'\n{"="*60}')
        print(f'INDEX 完整性检查 — {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        print(f'{"="*60}')
        print(f'INDEX.md: {os.path.getsize(INDEX_PATH)} bytes')
        print(f'总文件数: {total_files}')
        print(f'INDEX 中: {total_files - len(gaps)}')
        print(f'缺口: {len(gaps)}')

        if gaps:
            print(f'\n[GAP] Missing entries:')
            for cat, fname in gaps:
                print(f'   [{cat}] {fname}')
            print(f'\nFix: python scripts/rebuild-index.py')
            return 1
        else:
            print(f'\n[PASS] INDEX 100% coverage - 0 gaps')
            return 0
    else:
        if gaps:
            print(f'[FAIL] INDEX gaps: {len(gaps)}/{total_files}')
            return 1
        else:
            return 0

if __name__ == '__main__':
    sys.exit(check())
