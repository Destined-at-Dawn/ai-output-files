import os, shutil, time
from datetime import datetime, timedelta

conv_dir = os.path.expanduser("~/.newmax/conversations")
archive_dir = os.path.expanduser("~/.newmax/conversations-archive")

if not os.path.exists(conv_dir):
    print("conversations目录不存在")
    exit()

# 30天前的时间戳
cutoff = time.time() - 30*86400

# 扫描旧文件
old_files = []
new_files = []
total_old_size = 0

for f in os.listdir(conv_dir):
    fp = os.path.join(conv_dir, f)
    if not os.path.isfile(fp):
        continue
    mtime = os.path.getmtime(fp)
    size = os.path.getsize(fp)
    if mtime < cutoff:
        old_files.append((f, fp, size, datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')))
        total_old_size += size
    else:
        new_files.append((f, size))

print(f"总文件: {len(old_files)+len(new_files)}")
print(f">30天: {len(old_files)}个, {total_old_size/1024/1024:.1f}MB")
print(f"最近30天: {len(new_files)}个")

if not old_files:
    print("没有>30天的旧文件")
    exit()

# 创建归档目录
os.makedirs(archive_dir, exist_ok=True)

# 移动旧文件
moved = 0
moved_size = 0
errors = 0
for f, fp, size, date in old_files:
    dst = os.path.join(archive_dir, f)
    try:
        shutil.move(fp, dst)
        moved += 1
        moved_size += size
    except Exception as e:
        errors += 1
        if errors <= 3:
            print(f"  移动失败: {f} - {e}")

print(f"\n归档完成:")
print(f"  移动: {moved}个文件, {moved_size/1024/1024:.1f}MB")
print(f"  失败: {errors}个")
print(f"  归档目录: {archive_dir}")
