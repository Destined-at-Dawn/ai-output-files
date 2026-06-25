#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_archive.py — 双归档强制脚本
=================================
用途：修改文件前调用此脚本，自动完成双归档（全局+工作区），带时间戳。
违反此流程 = F4铁律违规。

用法：
  python auto_archive.py <文件路径>           # 归档单个文件
  python auto_archive.py <目录路径> --dir     # 归档整个目录
  python auto_archive.py <文件路径> --dry-run # 预览归档操作，不实际执行
  python auto_archive.py --verify <归档路径>  # 验证归档文件完整性

退出码：
  0 = 归档成功（两份均已验证）
  1 = 归档失败（中断，不许继续修改）
  2 = 参数错误

示例：
  python auto_archive.py "${WORKSPACE_ROOT}/projects/跨校协作/outputs/蔡俊-CAD参数表/蔡俊-零件01-头颈件.md"
  python auto_archive.py "${WORKSPACE_ROOT}/projects/跨校协作/outputs/蔡俊-CAD参数表/" --dir
"""

import os
import sys
import shutil
import hashlib
import datetime
import argparse

# Windows GBK编码兼容：强制stdout使用utf-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ═══════════════════════════════════════════════════════════
# 配置区 — 归档目录（铁律：全局+工作区，两份）
# ═══════════════════════════════════════════════════════════
GLOBAL_ARCHIVE = r"${LEGACY_ROOT}/归档"
WORKSPACE_ARCHIVE = r"${WORKSPACE_ROOT}/归档"

# 项目根目录（用于计算相对路径）
PROJECT_ROOTS = [
    r"${WORKSPACE_ROOT}/projects",
    r"${WORKSPACE_ROOT}",
]


def get_file_hash(filepath):
    """计算文件MD5哈希值"""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_timestamp():
    """生成时间戳字符串"""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def derive_archive_name(filepath, timestamp):
    """
    从文件路径生成归档文件名。
    格式: {原文件名}_{时间戳}.bak
    """
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return f"{name}_{timestamp}{ext}"


def derive_archive_dir_name(dirpath, timestamp):
    """
    从目录路径生成归档目录名。
    格式: {原目录名}_{时间戳}
    """
    dirname = os.path.basename(dirpath.rstrip("/\\"))
    return f"{dirname}_{timestamp}"


def archive_single_file(filepath, dry_run=False):
    """
    双归档单个文件。

    Returns:
        (success: bool, global_path: str, ws_path: str, error: str)
    """
    filepath = os.path.abspath(filepath)

    # 1. 检查文件是否存在
    if not os.path.exists(filepath):
        return False, "", "", f"文件不存在: {filepath}"

    if not os.path.isfile(filepath):
        return False, "", "", f"不是文件（是目录）: {filepath}"

    timestamp = get_timestamp()
    archive_name = derive_archive_name(filepath, timestamp)

    # 2. 确定归档子目录（基于文件所在目录名）
    parent_dir_name = os.path.basename(os.path.dirname(filepath))
    archive_subdir = f"{parent_dir_name}_归档"

    global_dest_dir = os.path.join(GLOBAL_ARCHIVE, archive_subdir)
    ws_dest_dir = os.path.join(WORKSPACE_ARCHIVE, archive_subdir)

    global_dest = os.path.join(global_dest_dir, archive_name)
    ws_dest = os.path.join(ws_dest_dir, archive_name)

    if dry_run:
        print(f"[DRY RUN] 将归档: {filepath}")
        print(f"  → 全局: {global_dest}")
        print(f"  → 工作区: {ws_dest}")
        return True, global_dest, ws_dest, ""

    # 3. 创建归档目录
    os.makedirs(global_dest_dir, exist_ok=True)
    os.makedirs(ws_dest_dir, exist_ok=True)

    # 4. 复制到全局归档
    try:
        shutil.copy2(filepath, global_dest)
    except Exception as e:
        return False, "", "", f"全局归档失败: {e}"

    # 5. 复制到工作区归档
    try:
        shutil.copy2(filepath, ws_dest)
    except Exception as e:
        return False, global_dest, "", f"工作区归档失败: {e}"

    # 6. 验证两份归档与原文件一致
    src_hash = get_file_hash(filepath)
    global_hash = get_file_hash(global_dest)
    ws_hash = get_file_hash(ws_dest)

    if src_hash != global_hash:
        return False, global_dest, ws_dest, f"全局归档MD5不匹配! 原:{src_hash} 归档:{global_hash}"

    if src_hash != ws_hash:
        return False, global_dest, ws_dest, f"工作区归档MD5不匹配! 原:{src_hash} 归档:{ws_hash}"

    return True, global_dest, ws_dest, ""


def archive_directory(dirpath, dry_run=False):
    """
    双归档整个目录。

    Returns:
        (success: bool, errors: list)
    """
    dirpath = os.path.abspath(dirpath)

    if not os.path.exists(dirpath):
        return False, [f"目录不存在: {dirpath}"]

    if not os.path.isdir(dirpath):
        return False, [f"不是目录: {dirpath}"]

    timestamp = get_timestamp()
    archive_name = derive_archive_dir_name(dirpath, timestamp)

    global_dest = os.path.join(GLOBAL_ARCHIVE, archive_name)
    ws_dest = os.path.join(WORKSPACE_ARCHIVE, archive_name)

    if dry_run:
        file_count = sum(len(files) for _, _, files in os.walk(dirpath))
        print(f"[DRY RUN] 将归档目录: {dirpath}")
        print(f"  文件数: {file_count}")
        print(f"  → 全局: {global_dest}")
        print(f"  → 工作区: {ws_dest}")
        return True, []

    # 复制到全局归档
    try:
        shutil.copytree(dirpath, global_dest, dirs_exist_ok=True)
    except Exception as e:
        return False, [f"全局归档失败: {e}"]

    # 复制到工作区归档
    try:
        shutil.copytree(dirpath, ws_dest, dirs_exist_ok=True)
    except Exception as e:
        return False, [f"工作区归档失败: {e}"]

    # 验证文件数和哈希
    errors = []
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            src_file = os.path.join(root, f)
            rel_path = os.path.relpath(src_file, dirpath)

            global_file = os.path.join(global_dest, rel_path)
            ws_file = os.path.join(ws_dest, rel_path)

            src_hash = get_file_hash(src_file)

            if not os.path.exists(global_file):
                errors.append(f"全局归档缺失: {rel_path}")
                continue

            if not os.path.exists(ws_file):
                errors.append(f"工作区归档缺失: {rel_path}")
                continue

            if src_hash != get_file_hash(global_file):
                errors.append(f"全局归档MD5不匹配: {rel_path}")

            if src_hash != get_file_hash(ws_file):
                errors.append(f"工作区归档MD5不匹配: {rel_path}")

    return len(errors) == 0, errors


def verify_archive(archive_path):
    """验证归档文件完整性"""
    if not os.path.exists(archive_path):
        print(f"❌ 归档文件不存在: {archive_path}")
        return False

    size = os.path.getsize(archive_path)
    hash_val = get_file_hash(archive_path)
    print(f"✅ 归档文件存在: {archive_path}")
    print(f"   大小: {size} bytes")
    print(f"   MD5: {hash_val}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="双归档强制脚本 — 修改文件前必须先调用此脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("path", help="要归档的文件或目录路径")
    parser.add_argument("--dir", action="store_true", help="归档整个目录")
    parser.add_argument("--dry-run", action="store_true", help="预览归档操作，不实际执行")
    parser.add_argument("--verify", action="store_true", help="验证归档文件完整性")

    args = parser.parse_args()

    # 验证模式
    if args.verify:
        success = verify_archive(args.path)
        sys.exit(0 if success else 1)

    print("=" * 60)
    print("🔒 双归档执行中 — F4铁律")
    print("=" * 60)

    if args.dir:
        success, errors = archive_directory(args.path, dry_run=args.dry_run)
        if success:
            print(f"\n✅ 目录归档成功: {args.path}")
            if not args.dry_run:
                print(f"   全局: {GLOBAL_ARCHIVE}")
                print(f"   工作区: {WORKSPACE_ARCHIVE}")
        else:
            print(f"\n❌ 目录归档失败:")
            for err in errors:
                print(f"   - {err}")
    else:
        success, global_path, ws_path, error = archive_single_file(args.path, dry_run=args.dry_run)
        if success:
            print(f"\n✅ 文件归档成功: {args.path}")
            if not args.dry_run:
                print(f"   全局: {global_path}")
                print(f"   工作区: {ws_path}")
                print(f"   MD5验证: 三份一致 ✓")
        else:
            print(f"\n❌ 文件归档失败: {error}")
            if global_path:
                print(f"   全局归档（部分）: {global_path}")

    print("=" * 60)

    if not args.dry_run:
        if success:
            print("🟢 归档完成，可以安全修改原文件。")
        else:
            print("🔴 归档失败，禁止修改原文件！")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
