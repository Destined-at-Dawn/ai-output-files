"""
li-workspace: projects/ 深度清理
原则：
1. 归档旧版项目
2. 清除 timestamp/空文件碎片
3. 保留 memory/ 和 outputs/（这是项目的核心产出）
"""
import os
import shutil
from datetime import datetime

PROJECTS = r"E:\ai产出文件\牛马\mutual\mutual\projects"
ARCHIVE = r"E:\ai产出文件\牛马\归档\2026-06-22-projects-cleanup"
TODAY = "2026-06-22"


def main():
    print("=== projects/ 清理 ===\n")
    os.makedirs(ARCHIVE, exist_ok=True)

    stats = {"archived": 0, "deleted_garbage": 0, "deleted_empty": 0}

    # ========== 1. 归档旧版项目 ==========
    print("[1/3] 归档旧版项目")

    # 20260518-生态优化/ — 152个文件，全是旧版 workspace 副本
    old_project = os.path.join(PROJECTS, "20260518-生态优化")
    if os.path.exists(old_project):
        dst = os.path.join(ARCHIVE, "20260518-生态优化")
        shutil.move(old_project, dst)
        print(f"  ARCHIVED: 20260518-生态优化/ (152 files)")
        stats["archived"] += 1

    # proj-1781073838312-332mv5/ — 只有1个文件的壳子
    empty_proj = os.path.join(PROJECTS, "proj-1781073838312-332mv5")
    if os.path.exists(empty_proj):
        files = []
        for root, dirs, fs in os.walk(empty_proj):
            files.extend(fs)
        if len(files) <= 2:  # 只有 project.md 或少量文件
            dst = os.path.join(ARCHIVE, "proj-1781073838312-332mv5")
            shutil.move(empty_proj, dst)
            print(f"  ARCHIVED: proj-1781073838312-332mv5/ ({len(files)} files, nearly empty)")
            stats["archived"] += 1

    # ========== 2. 清除当前项目的垃圾文件 ==========
    print("\n[2/3] 清除 timestamp 碎片和空文件")

    current_proj = os.path.join(PROJECTS, "proj-1779089173658-j5tg2m")
    garbage_archive = os.path.join(ARCHIVE, "proj-1779089173658-j5tg2m-garbage")
    os.makedirs(garbage_archive, exist_ok=True)

    for root, dirs, files in os.walk(current_proj):
        for f in files:
            fp = os.path.join(root, f)
            size = os.path.getsize(fp)

            # timestamp 粘贴文件
            if f[0:4].isdigit() and "Pasted" in f:
                rel = os.path.relpath(fp, current_proj)
                dst = os.path.join(garbage_archive, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(fp, dst)
                stats["deleted_garbage"] += 1

            # 0 字节空文件（排除 .gitkeep 等有意的空文件）
            elif size == 0 and f not in [".gitkeep", ".gitignore", "__init__.py"]:
                rel = os.path.relpath(fp, current_proj)
                dst = os.path.join(garbage_archive, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(fp, dst)
                stats["deleted_empty"] += 1

    # 清理 share/ 中的 0 字节碎片
    share_dir = os.path.join(current_proj, "share")
    if os.path.exists(share_dir):
        for f in os.listdir(share_dir):
            fp = os.path.join(share_dir, f)
            if os.path.isfile(fp) and os.path.getsize(fp) == 0:
                dst = os.path.join(garbage_archive, "share", f)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(fp, dst)
                stats["deleted_empty"] += 1

    print(f"  清除 timestamp 碎片: {stats['deleted_garbage']} 个")
    print(f"  清除 0 字节文件: {stats['deleted_empty']} 个")

    # ========== 3. 验证 ==========
    print("\n[3/3] 验证最终状态")

    for item in sorted(os.listdir(PROJECTS)):
        path = os.path.join(PROJECTS, item)
        if os.path.isdir(path):
            total = sum(1 for _, _, fs in os.walk(path) for _ in fs)
            print(f"  {item}/ ({total} files)")

    # 归档统计
    archive_total = sum(1 for _, _, fs in os.walk(ARCHIVE) for _ in fs)
    print(f"\n  归档: {archive_total} files -> {ARCHIVE}")

    print(f"\n  归档项目: {stats['archived']}")
    print(f"  清除垃圾: {stats['deleted_garbage'] + stats['deleted_empty']} files")
    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
