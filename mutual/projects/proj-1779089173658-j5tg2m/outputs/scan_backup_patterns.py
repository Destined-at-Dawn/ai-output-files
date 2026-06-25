"""扫描备份文件命名模式"""
import os
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

root = r"E:\ai产出文件"

# 备份文件命名模式
backup_patterns = [
    r'.*备份.*',
    r'.*backup.*',
    r'.*bak$',
    r'.*副本.*',
    r'.*copy.*',
    r'.*Copy.*',
    r'.*\.bak$',
    r'.*\.old$',
    r'.*\.orig$',
    r'.*\.backup$',
    r'.*\s\(2\).*',
    r'.*\s\(3\).*',
    r'.*-copy.*',
    r'.*_backup.*',
    r'.*_bak$',
    r'.*_old$',
]

compiled_patterns = [re.compile(p, re.IGNORECASE) for p in backup_patterns]

def is_backup_name(name):
    """检查文件名是否匹配备份模式"""
    for pattern in compiled_patterns:
        if pattern.match(name):
            return True
    return False

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
    for filename in filenames:
        total_scanned += 1
        if is_backup_name(filename):
            full_path = os.path.join(dirpath, filename)
            info = get_file_info(full_path)
            if info:
                backup_files.append(info)

# 按大小倒序
backup_files.sort(key=lambda x: x["size_mb"], reverse=True)

print(f"=== 备份文件扫描结果 ===")
print(f"扫描文件总数: {total_scanned}")
print(f"匹配备份模式: {len(backup_files)} 个\n")

total_size = 0
for f in backup_files:
    total_size += f["size_mb"]
    # 显示相对路径
    rel_path = f["path"].replace(root + "\\", "")
    print(f"📄 {rel_path}")
    print(f"   大小: {f['size_mb']:.2f} MB")

print(f"\n备份文件总大小: {total_size:.2f} MB ({total_size/1024:.2f} GB)")
