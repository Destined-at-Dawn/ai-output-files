"""扫描内容重复文件（按大小分组 + MD5 哈希）"""
import os
import sys
import hashlib
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

root = r"E:\ai产出文件"

# 排除目录
exclude_dirs = {'node_modules', '.git', '__pycache__', '.next', 'dist', 'build', '.newmax'}

def should_skip_dir(dirpath):
    """检查是否应该跳过该目录"""
    parts = dirpath.replace(root, '').split(os.sep)
    return any(p in exclude_dirs for p in parts)

def get_file_hash(path, block_size=65536):
    """计算文件 MD5 哈希"""
    try:
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            buf = f.read(block_size)
            while buf:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except:
        return None

# Step 1: 按文件大小分组
print("Step 1: 扫描文件并按大小分组...")
size_groups = defaultdict(list)
total_files = 0
skipped_dirs = 0

for dirpath, dirnames, filenames in os.walk(root):
    if should_skip_dir(dirpath):
        dirnames.clear()
        skipped_dirs += 1
        continue

    for filename in filenames:
        total_files += 1
        full_path = os.path.join(dirpath, filename)
        try:
            size = os.path.getsize(full_path)
            if size > 0:  # 忽略空文件
                size_groups[size].append(full_path)
        except:
            pass

print(f"扫描完成: {total_files} 个文件, 跳过 {skipped_dirs} 个排除目录")
print(f"不同文件大小数: {len(size_groups)}")

# Step 2: 找出大小相同的文件组（可能重复）
potential_duplicates = {size: files for size, files in size_groups.items() if len(files) > 1}
print(f"大小相同的文件组数: {len(potential_duplicates)}")
print(f"可能重复的文件数: {sum(len(files) for files in potential_duplicates.values())}")

# Step 3: 对大小相同的文件计算哈希
print("\nStep 2: 计算哈希查找内容重复...")
hash_groups = defaultdict(list)
processed = 0

for size, files in potential_duplicates.items():
    for filepath in files:
        processed += 1
        if processed % 1000 == 0:
            print(f"  已处理: {processed}/{sum(len(files) for files in potential_duplicates.values())}")

        file_hash = get_file_hash(filepath)
        if file_hash:
            hash_groups[file_hash].append({
                "path": filepath,
                "size_mb": round(size / 1024 / 1024, 2)
            })

# Step 4: 找出内容完全相同的文件组
duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
print(f"\n内容完全相同的文件组数: {len(duplicates)}")

# Step 5: 按总大小排序并输出结果
print("\n=== 内容重复文件报告 ===\n")

# 计算每组的浪费空间
duplicate_groups = []
for file_hash, files in duplicates.items():
    total_size = sum(f["size_mb"] for f in files)
    wasted_size = total_size - files[0]["size_mb"]  # 保留1个，其余浪费
    duplicate_groups.append({
        "hash": file_hash,
        "files": files,
        "count": len(files),
        "single_size_mb": files[0]["size_mb"],
        "total_size_mb": total_size,
        "wasted_size_mb": wasted_size
    })

# 按浪费空间排序
duplicate_groups.sort(key=lambda x: x["wasted_size_mb"], reverse=True)

total_wasted = 0
for i, group in enumerate(duplicate_groups[:50], 1):  # 只显示前50组
    total_wasted += group["wasted_size_mb"]
    print(f"重复组 {i}: {group['count']} 个文件, 单个 {group['single_size_mb']:.2f} MB, 浪费 {group['wasted_size_mb']:.2f} MB")
    for f in group["files"]:
        rel_path = f["path"].replace(root + "\\", "")
        print(f"  📄 {rel_path}")
    print()

print(f"\n=== 统计 ===")
print(f"总重复组数: {len(duplicate_groups)}")
print(f"前50组浪费空间: {total_wasted:.2f} MB ({total_wasted/1024:.2f} GB)")
print(f"全部重复浪费空间: {sum(g['wasted_size_mb'] for g in duplicate_groups):.2f} MB ({sum(g['wasted_size_mb'] for g in duplicate_groups)/1024:.2f} GB)")
