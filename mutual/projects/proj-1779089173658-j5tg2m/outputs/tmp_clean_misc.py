import os, shutil

# 1. newmax.db 旧备份
db_bak = os.path.expanduser("~/.newmax/newmax.db.bak-20260611-120631")
if os.path.exists(db_bak):
    size = os.path.getsize(db_bak)
    os.remove(db_bak)
    print(f"删除 newmax.db 旧备份: {size/1024/1024:.1f}MB")

# 2. skills.zip（skills目录已有完整内容）
skills_zip = os.path.expanduser("~/.newmax/skills.zip")
skills_dir = os.path.expanduser("~/.newmax/skills")
if os.path.exists(skills_zip) and os.path.exists(skills_dir):
    size = os.path.getsize(skills_zip)
    # 先归档再删
    archive_dir = r"E:\ai产出文件\牛马\归档\2026-06-12-workflow-audit"
    os.makedirs(archive_dir, exist_ok=True)
    shutil.copy2(skills_zip, os.path.join(archive_dir, "skills.zip.bak"))
    os.remove(skills_zip)
    print(f"删除 skills.zip: {size/1024/1024:.1f}MB（已备份到归档目录）")

# 3. D:\Qoder（用户上次没删成因为打错命令）
qoder = r"D:\Qoder"
if os.path.exists(qoder):
    try:
        size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(qoder) for f in fn)
        shutil.rmtree(qoder)
        print(f"删除 D:\\Qoder: {size/1024/1024:.1f}MB")
    except PermissionError:
        print(f"D:\\Qoder: 被占用（可能正在运行），需手动关闭后删除")
    except Exception as e:
        print(f"D:\\Qoder: 删除失败 - {e}")

# 4. Temp中>7天的临时文件
import time
temp_dir = os.environ.get('TEMP', '')
if temp_dir and os.path.exists(temp_dir):
    cutoff = time.time() - 7*86400
    freed = 0
    count = 0
    errors = 0
    for dp, dn, fn in os.walk(temp_dir):
        for f in fn:
            fp = os.path.join(dp, f)
            try:
                if os.path.getmtime(fp) < cutoff:
                    size = os.path.getsize(fp)
                    os.remove(fp)
                    freed += size
                    count += 1
            except:
                errors += 1
    print(f"Temp清理: 删除{count}个文件, {freed/1024/1024:.1f}MB, {errors}个跳过")

# 5. .newmax/.git 大小报告
git_dir = os.path.expanduser("~/.newmax/.git")
if os.path.exists(git_dir):
    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(git_dir) for f in fn)
    print(f"\n.newmax/.git: {size/1024/1024:.1f}MB（不删除，但可考虑 gc）")

print("\n完成")
