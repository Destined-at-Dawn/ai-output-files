"""
li-script Phase 0: 清扫过期归档脚本
今天 = 2026-06-22，所有待删脚本已过期
"""
import os
import shutil
from datetime import datetime

ARCHIVE_DIR = r"E:\ai产出文件\牛马\script-library\_archive"
ARCHIVE_LOG = os.path.join(ARCHIVE_DIR, "ARCHIVE_LOG.md")
TODAY = "2026-06-22"

# 过期脚本清单（全部到期日 < 2026-06-22）
EXPIRED = [
    ("gen_book63_v2.py", "2026-06-20"),
    ("gen_book63_v3.py", "2026-06-20"),
    ("gen_book63_v4.py", "2026-06-20"),
    ("gen_book63_v5.py", "2026-06-20"),
    ("build_v4_simple.py", "2026-06-21"),
    ("build_v4_v2.py", "2026-06-21"),
    ("iterate_model.py", "2026-06-21"),
    ("fix_insert_sections.py", "2026-06-21"),
]

def main():
    print("=== li-script Phase 0: 清扫过期归档 ===\n")

    deleted = []
    not_found = []

    for fname, expiry in EXPIRED:
        fpath = os.path.join(ARCHIVE_DIR, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            print(f"  DELETED: {fname} (expired {expiry})")
            deleted.append((fname, expiry))
        else:
            print(f"  NOT FOUND (already gone): {fname}")
            not_found.append((fname, expiry))

    # 更新 ARCHIVE_LOG.md
    if deleted:
        with open(ARCHIVE_LOG, "r", encoding="utf-8") as f:
            content = f.read()

        # 清空待删清单（所有项都已过期）
        old_table = """| 脚本文件 | 一句话用途 | 入档日期 | 到期删除日期 | 为什么是一一次性 |
|----------|-----------|----------|--------------|----------------|
| gen_book63_v2.py | v2: 模板扩充尝试(.format冲突) | 2026-06-13 | 2026-06-20 | 试错迭代版本，v6已入库替代 |
| gen_book63_v3.py | v3: 超量扩充尝试(循环不足) | 2026-06-13 | 2026-06-20 | 试错迭代版本，v6已入库替代 |
| gen_book63_v4.py | v4: 6x模板尝试(格式冲突遍历修复) | 2026-06-13 | 2026-06-20 | 试错迭代版本，v6已入库替代 |
| gen_book63_v5.py | v5: f-string替换尝试(变量未定义) | 2026-06-13 | 2026-06-20 | 试错迭代版本，v6已入库替代 |
| build_v4_simple.py | CadQuery v4简化中间版 | 2026-06-14 | 2026-06-21 | 被 build_v4.py 替代，已入库为 cadquery-parametric-base.py |
| build_v4_v2.py | CadQuery v4 v2中间版 | 2026-06-14 | 2026-06-21 | 被 build_v4.py 替代，已入库为 cadquery-parametric-base.py |
| iterate_model.py | v1工程迭代脚本 | 2026-06-14 | 2026-06-21 | 被 iterate_v3.py 替代，已入库为 engineering-review-100rounds.py |
| fix_insert_sections.py | 文档插入章节修复 | 2026-06-14 | 2026-06-21 | 一次性文档修复，无迁移价值 |"""

        new_table = """| 脚本文件 | 一句话用途 | 入档日期 | 到期删除日期 | 为什么是一次性 |
|----------|-----------|----------|--------------|----------------|
| _(无待删项)_ | | | | |"""

        content = content.replace(old_table, new_table)

        # 追加已删除记录
        old_deleted = """| 脚本文件 | 用途 | 入档日期 | 实际删除日期 |
|----------|------|----------|--------------|
| _（空）_ | | | |"""

        new_deleted_rows = "| 脚本文件 | 用途 | 入档日期 | 实际删除日期 |\n|----------|------|----------|--------------|\n"
        for fname, expiry in deleted:
            # 从原始待删清单推断用途
            usage_map = {
                "gen_book63_v2.py": "v2: 模板扩充尝试",
                "gen_book63_v3.py": "v3: 超量扩充尝试",
                "gen_book63_v4.py": "v4: 6x模板尝试",
                "gen_book63_v5.py": "v5: f-string替换尝试",
                "build_v4_simple.py": "CadQuery v4简化中间版",
                "build_v4_v2.py": "CadQuery v4 v2中间版",
                "iterate_model.py": "v1工程迭代脚本",
                "fix_insert_sections.py": "文档插入章节修复",
            }
            entry_date = "2026-06-13" if "gen_book" in fname else "2026-06-14"
            usage = usage_map.get(fname, "unknown")
            new_deleted_rows += f"| {fname} | {usage} | {entry_date} | {TODAY} |\n"

        content = content.replace(old_deleted, new_deleted_rows.rstrip())

        with open(ARCHIVE_LOG, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"\n  Summary: {len(deleted)} deleted, {len(not_found)} not found")
    print("=== Phase 0 DONE ===\n")

if __name__ == "__main__":
    main()
