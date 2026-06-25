"""扫描备份文件命名模式 - 排除 node_modules"""
import os
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

root = r"E:\ai产出文件"

# 备份文件命名模式（更精确）
backup_patterns = [
    r'.*备份.*',
    r'.*backup.*\.db$',
    r'.*\.bak$',
    r'.*副本.*\.pptx$',
    r'.*副本.*\.docx$',
    r'.*副本.*\.xlsx$',
    r'.*副本.*\.pdf$',
    r'.*Copy\.pptx$',
    r'.*Copy\.docx$',
    r'.*\.old$',
    r'.*\.orig$',
    r'.*\.backup$',
    r'.*\s\(2\)\.\w+$',
    r'.*\s\(3\)\.\w+$',
    r'.*-copy\.\w+$',
    r'.*_backup\.\w+$',
    r'.*_bak\.\w+$',
    r'.*_old\.\w+$',
]

compiled_patterns = [re.compile(p, re.IGNORECASE) for p in backup_patterns]

# 排除目录
exclude_dirs = {'node_modules', '.git', '__pycache__', '.next', 'dist', 'build'}

def is_backup_name(name):
    """检查文件名是否匹配备份模式"""
    for pattern in compiled_patterns:
        if pattern.match(name):
            return True
    return False

def should_skip_dir(dirpath):
    """检查是否应该跳过该目录"""
    parts = dirpath.replace(root, '').split(os.sep)
    return any(p in exclude_dirs for p in parts)

def get_file_info(path):
    """获取文件信息"""
    try:
        stat = os.stat(path)
        return {
            "path": path,
            "name": os.path.basename(path),
            "size_mb": round(stat.st_size / 1024 / 1024, 2),
            "mtime": stat.st_mtime
        }
    except:
        return None

# 扫描所有文件
backup_files = []
total_scanned = 0

for dirpath, dirnames, filenames in os.walk(root):
    # 跳过排除目录
    if should_skip_dir(dirpath):
        dirnames.clear()
        continue

    for filename in filenames:
        total_scanned += 1
        if is_backup_name(filename):
            full_path = os.path.join(dirpath, filename)
            info = get_file_info(full_path)
            if info and info["size_mb"] > 0.01:  # 忽略极小文件
                backup_files.append(info)

# 按大小倒序
backup_files.sort(key=lambda x: x["size_mb"], reverse=True)

print(f"=== 备份文件扫描结果（排除 node_modules）===")
print(f"扫描文件总数: {total_scanned}")
print(f"匹配备份模式: {len(backup_files)} 个\n")

# 按目录分组统计
dir_stats = {}
for f in backup_files:
    dir_name = os.path.dirname(f["path"]).replace(root + "\\", "")
    if dir_name not in dir_stats:
        dir_stats[dir_name] = {"count": 0, "size_mb": 0, "files": []}
    dir_stats[dir_name]["count"] += 1
    dir_stats[dir_name]["size_mb"] += f["size_mb"]
    dir_stats[dir_name]["files"].append(f)

# 打印按目录分组的结果
print("=== 按目录分组（按大小排序）===")
sorted_dirs = sorted(dir_stats.items(), key=lambda x: x[1]["size_mb"], reverse=True)

for dir_name, stats in sorted_dirs:
    print(f"\n📁 {dir_name}")
    print(f"   文件数: {stats['count']}, 总大小: {stats['size_mb']:.2f} MB")
    for f in stats["files"][:5]:  # 只显示前5个
        print(f"   📄 {f['name']} ({f['size_mb']:.2f} MB)")
    if len(stats["files"]) > 5:
        print(f"   ... 还有 {len(stats['files'])-5} 个文件")

total_size = sum(f["size_mb"] for f in backup_files)
print(f"\n备份文件总大小: {total_size:.2f} MB ({total_size/1024:.2f} GB)")
