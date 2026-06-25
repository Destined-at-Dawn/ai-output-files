import os, json, shutil, time
from datetime import datetime

# === 1. 磁盘空间 ===
print("=== 磁盘空间 ===")
for letter in ['C', 'D', 'E']:
    path = letter + ':\\'
    if os.path.exists(path):
        total, used, free = shutil.disk_usage(path)
        print(f"  {letter}: 总计{total/1024**3:.1f}GB  已用{used/1024**3:.1f}GB  剩余{free/1024**3:.1f}GB ({free/total*100:.1f}%)")

# === 2. .newmax 目录分析 ===
print("\n=== .newmax 目录分析 ===")
nm_dir = os.path.expanduser("~/.newmax")
if os.path.exists(nm_dir):
    for item in sorted(os.listdir(nm_dir)):
        fp = os.path.join(nm_dir, item)
        try:
            if os.path.isdir(fp):
                size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(fp) for f in fn)
            else:
                size = os.path.getsize(fp)
            if size > 1024*100:  # >100KB
                print(f"  .newmax/{item}: {size/1024/1024:.2f}MB")
        except Exception as e:
            print(f"  .newmax/{item}: err - {e}")

# === 3. MCP 配置 ===
print("\n=== MCP配置 ===")
mcp_path = os.path.expanduser("~/.newmax/.mcp.json")
if os.path.exists(mcp_path):
    with open(mcp_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    servers = data.get('mcpServers', {})
    print(f"  当前MCP servers: {len(servers)}个")
    for name, conf in servers.items():
        cmd = conf.get('command', '')
        args = conf.get('args', [])
        args_str = ' '.join(str(a)[:60] for a in args[:4])
        print(f"    {name}: {cmd} {args_str}")
else:
    print("  文件不存在")

# === 4. Qoder ===
print("\n=== D:\\Qoder ===")
qoder = r"D:\Qoder"
if os.path.exists(qoder):
    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(qoder) for f in fn)
    print(f"  存在: {size/1024/1024:.1f}MB")
else:
    print("  不存在")

# === 5. edge_install ===
print("\n=== D:\\edge_install ===")
edge = r"D:\edge_install"
if os.path.exists(edge):
    files = [(f, os.path.getsize(os.path.join(edge, f))) for f in os.listdir(edge) if os.path.isfile(os.path.join(edge, f))]
    total = sum(s for _, s in files)
    print(f"  文件数: {len(files)}, 总大小: {total/1024/1024:.1f}MB")
    for f, s in sorted(files, key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {f}: {s/1024/1024:.1f}MB")
else:
    print("  不存在")

# === 6. conversations ===
print("\n=== conversations ===")
conv = os.path.expanduser("~/.newmax/conversations")
if os.path.exists(conv):
    items = os.listdir(conv)
    total_size = 0
    for f in items:
        fp = os.path.join(conv, f)
        if os.path.isfile(fp):
            total_size += os.path.getsize(fp)
    print(f"  文件数: {len(items)}, 总大小: {total_size/1024/1024:.1f}MB")
else:
    print("  不存在")

# === 7. npm全局包 ===
print("\n=== npm全局包 ===")
npm_global = os.path.expanduser("~\\AppData\\Roaming\\npm\\node_modules")
if os.path.exists(npm_global):
    packages = []
    for item in os.listdir(npm_global):
        fp = os.path.join(npm_global, item)
        if os.path.isdir(fp):
            try:
                size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(fp) for f in fn)
                packages.append((item, size))
            except:
                pass
    packages.sort(key=lambda x: x[1], reverse=True)
    total = sum(s for _, s in packages)
    print(f"  包数: {len(packages)}, 总大小: {total/1024/1024:.1f}MB")
    for name, size in packages[:15]:
        print(f"    {name}: {size/1024/1024:.1f}MB")

# === 8. pip/npm 缓存 ===
print("\n=== 缓存 ===")
for label, p in [("pip", os.path.expanduser("~\\AppData\\Local\\pip\\cache")),
                  ("npm", os.path.expanduser("~\\AppData\\Local\\npm-cache")),
                  ("yarn", os.path.expanduser("~\\AppData\\Local\\Yarn\\Cache"))]:
    if os.path.exists(p):
        size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(p) for f in fn)
        print(f"  {label}: {size/1024/1024:.1f}MB")

# === 9. Temp ===
print("\n=== Temp ===")
td = os.environ.get('TEMP', '')
if td and os.path.exists(td):
    size = 0
    count = 0
    try:
        for dp, dn, fn in os.walk(td):
            for f in fn:
                try:
                    size += os.path.getsize(os.path.join(dp, f))
                    count += 1
                except:
                    pass
        print(f"  {td}: {count}个文件, {size/1024/1024:.1f}MB")
    except:
        print(f"  无权限")

# === 10. MarvisData ===
print("\n=== Marvis ===")
for label, p in [("E:\\MarvisData", r"E:\MarvisData"),
                  ("AppData Marvis", os.path.expanduser(r"~\AppData\Roaming\Tencent\Marvis"))]:
    if os.path.exists(p):
        try:
            size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(p) for f in fn)
            print(f"  {label}: {size/1024/1024/1024:.2f}GB")
        except:
            print(f"  {label}: 无权限")

# === 11. D盘大目录TOP15 ===
print("\n=== D盘大目录TOP15 ===")
d_dirs = []
d_root = "D:\\"
try:
    for item in os.listdir(d_root):
        fp = os.path.join(d_root, item)
        if os.path.isdir(fp):
            try:
                size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(fp) for f in fn)
                d_dirs.append((item, size))
            except:
                d_dirs.append((item, -1))
    d_dirs.sort(key=lambda x: x[1] if x[1] > 0 else 0, reverse=True)
    for name, size in d_dirs[:15]:
        if size > 0:
            print(f"  D:\\{name}: {size/1024/1024/1024:.2f}GB")
        else:
            print(f"  D:\\{name}: 无权限")
except Exception as e:
    print(f"  扫描失败: {e}")
