import os, json, shutil, subprocess, sys, time

start = time.time()
TIMEOUT = 120  # 2 min max

def dir_size(path, max_time=10):
    total = 0
    t0 = time.time()
    try:
        for root, dirs, files in os.walk(path):
            if time.time() - t0 > max_time:
                break
            for f in files:
                try:
                    total += os.path.getsize(os.path.join(root, f))
                except:
                    pass
    except:
        pass
    return total

def fmt(b):
    if b > 1024**3: return f"{b/1024**3:.1f}GB"
    return f"{b/1024**2:.0f}MB"

# 1. Disk space
print("=== 1. DISK SPACE ===")
for drive in ['C:\\', 'D:\\', 'E:\\']:
    try:
        u = shutil.disk_usage(drive)
        print(f"  {drive} Used={fmt(u.used)} Free={fmt(u.free)} Total={fmt(u.total)}")
    except:
        print(f"  {drive}: N/A")

# 2. .newmax breakdown
print("\n=== 2. .newmax DIRECTORY SIZES ===")
newmax = os.path.expanduser("~/.newmax")
items = []
for d in os.listdir(newmax):
    dp = os.path.join(newmax, d)
    if os.path.isdir(dp):
        s = dir_size(dp, max_time=5)
        if s > 1024*1024:
            items.append((d, s))
for name, size in sorted(items, key=lambda x: -x[1]):
    print(f"  {name}: {fmt(size)}")

# 3. npm global
print("\n=== 3. NPM GLOBAL PACKAGES ===")
try:
    r = subprocess.run(["npm", "list", "-g", "--depth=0"], capture_output=True, text=True, timeout=15)
    lines = [l for l in r.stdout.strip().split('\n') if l.strip()]
    for l in lines[:30]:
        print(f"  {l}")
    print(f"  Total: {len(lines)-1} packages")
except Exception as e:
    print(f"  Error: {e}")

# 4. pip packages count
print("\n=== 4. PIP PACKAGES ===")
try:
    r = subprocess.run(["pip", "list", "--format=json"], capture_output=True, text=True, timeout=15)
    pkgs = json.loads(r.stdout)
    print(f"  Total: {len(pkgs)} packages")
    for p in pkgs[:20]:
        print(f"    {p['name']}=={p['version']}")
    if len(pkgs) > 20:
        print(f"    ... and {len(pkgs)-20} more")
except Exception as e:
    print(f"  Error: {e}")

# 5. AppData/Local large dirs
print("\n=== 5. AppData/Local LARGE DIRS (>200MB) ===")
local_app = os.path.expandvars(r"%LOCALAPPDATA")
items = []
if os.path.exists(local_app):
    for d in os.listdir(local_app):
        dp = os.path.join(local_app, d)
        if os.path.isdir(dp):
            s = dir_size(dp, max_time=3)
            if s > 200*1024*1024:
                items.append((d, s))
for name, size in sorted(items, key=lambda x: -x[1])[:15]:
    print(f"  {name}: {fmt(size)}")

# 6. AppData/Roaming large dirs
print("\n=== 6. AppData/Roaming LARGE DIRS (>100MB) ===")
roaming = os.path.expandvars(r"%APPDATA")
items = []
if os.path.exists(roaming):
    for d in os.listdir(roaming):
        dp = os.path.join(roaming, d)
        if os.path.isdir(dp):
            s = dir_size(dp, max_time=3)
            if s > 100*1024*1024:
                items.append((d, s))
for name, size in sorted(items, key=lambda x: -x[1])[:15]:
    print(f"  {name}: {fmt(size)}")

# 7. D drive top-level
print("\n=== 7. D:\\ LARGE DIRS (>500MB) ===")
if os.path.exists('D:\\'):
    items = []
    for item in os.listdir('D:\\'):
        ip = os.path.join('D:\\', item)
        if os.path.isdir(ip):
            s = dir_size(ip, max_time=5)
            if s > 500*1024*1024:
                items.append((item, s))
    for name, size in sorted(items, key=lambda x: -x[1]):
        print(f"  {name}: {fmt(size)}")

# 8. E drive - just scan ai产出文件
print("\n=== 8. E:\\ai产出文件 SIZES ===")
base = 'E:\\ai产出文件'
if os.path.exists(base):
    items = []
    for item in os.listdir(base):
        ip = os.path.join(base, item)
        if os.path.isdir(ip):
            s = dir_size(ip, max_time=5)
            items.append((item, s))
    for name, size in sorted(items, key=lambda x: -x[1]):
        print(f"  {name}: {fmt(size)}")

# 9. MCP/tool leftovers
print("\n=== 9. MCP & TOOL LEFTOVERS ===")
checks = [
    ("~/.mcp.json (OLD, should not exist)", os.path.expanduser("~/.mcp.json")),
    ("~/.newmax/.mcp.json (ACTIVE)", os.path.expanduser("~/.newmax/.mcp.json")),
    ("~/.codex", os.path.expanduser("~/.codex")),
    ("~/.claude", os.path.expanduser("~/.claude")),
    ("~/.newmax/stepfun-daemon (OLD)", os.path.expanduser("~/.newmax/stepfun-daemon")),
    ("Antigravity IDE", os.path.expanduser("~\\AppData\\Local\\Antigravity")),
    ("Marvis", "E:\\Marvis"),
    ("~/.mempalace (junction)", os.path.expanduser("~/.mempalace")),
    ("D:\\mempalace (actual)", "D:\\mempalace"),
    ("~/.gemini", os.path.expanduser("~\\.gemini")),
    ("n8n data", os.path.expanduser("~\\.n8n")),
    ("MiKTeX", os.path.expanduser("~\\AppData\\Local\\Programs\\MiKTeX")),
]
for name, p in checks:
    exists = os.path.exists(p)
    size = 0
    if exists and os.path.isdir(p):
        size = dir_size(p, max_time=3)
    elif exists:
        size = os.path.getsize(p)
    status = f"EXISTS {fmt(size)}" if exists else "NOT FOUND"
    print(f"  {name}: {status}")

# 10. Check deprecated skills still on disk
print("\n=== 10. DEPRECATED li- skills still in .newmax/skills ===")
skills_dir = os.path.expanduser("~/.newmax/skills")
deprecated = []
if os.path.exists(skills_dir):
    for d in os.listdir(skills_dir):
        dp = os.path.join(skills_dir, d)
        if os.path.isdir(dp) and d.startswith('li-'):
            dep = os.path.join(dp, 'DEPRECATED.md')
            if os.path.exists(dep):
                s = dir_size(dp, max_time=1)
                deprecated.append((d, s))
for name, size in sorted(deprecated, key=lambda x: -x[1]):
    print(f"  {name}: {fmt(size)} (DEPRECATED but still on disk)")

print(f"\n=== SCAN COMPLETE in {time.time()-start:.0f}s ===")
