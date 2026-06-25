"""
C盘清理脚本 - 三阶段清理
Phase 1: Downloads安装包 (4个)
Phase 2: Ollama全删
Phase 3: 绿灯缓存/临时文件
所有删除进回收站（send2trash），误删可恢复
"""
import os, shutil, time, fnmatch
import send2trash

freed_total = 0
results = []

def long_path(p):
    """Add \\\\?\\ prefix for paths > 260 chars on Windows"""
    if os.name == 'nt' and not p.startswith('\\\\?\\'):
        return '\\\\?\\' + p
    return p

def safe_delete(path, desc):
    global freed_total
    lp = long_path(path)
    if not os.path.exists(lp):
        results.append(('SKIP', desc, 0, 'not found'))
        return 0
    if os.path.isfile(lp):
        size = os.path.getsize(lp)
    else:
        size = dir_size(path)
    try:
        send2trash.send2trash(path)
        freed_total += size
        results.append(('OK', desc, size, path))
        return size
    except Exception as e:
        # fallback: try with long_path prefix
        try:
            send2trash.send2trash(lp)
            freed_total += size
            results.append(('OK', desc, size, path))
            return size
        except Exception as e2:
            results.append(('FAIL', desc, 0, f'{path}: {e2}'))
            return 0

def dir_size(path):
    lp = long_path(path)
    if not os.path.exists(lp):
        return 0
    total = 0
    for dp, dn, fn in os.walk(lp):
        for f in fn:
            try:
                total += os.path.getsize(os.path.join(dp, f))
            except:
                pass
    return total

USER = os.path.expanduser('~')
APPDATA = os.environ.get('APPDATA', os.path.join(USER, 'AppData', 'Roaming'))
LOCAL = os.environ.get('LOCALAPPDATA', os.path.join(USER, 'AppData', 'Local'))
TEMP = os.environ.get('TEMP', os.path.join(LOCAL, 'Temp'))
DOWNLOADS = os.path.join(USER, 'Downloads')

print('=' * 60)
print('C disk cleanup - all files go to Recycle Bin (recoverable)')
print('=' * 60)

# PHASE 1
print('\n--- Phase 1: Downloads installers ---')
dl_targets = [
    'BaiduNetdisk_bingsearch_8.1.5.103_semclickid=msclkid_0fe30b25770e1fbeac5a61206fdcf298_utm_account_SS-bingtg102.exe',
    'pcsuite_setup_v6.2.6.0-cn_1774579329229.exe',
    'QoderSetup-x64.exe',
    'QQ_9.9.30-260511_x64_01.exe',
]
for name in dl_targets:
    safe_delete(os.path.join(DOWNLOADS, name), f'Downloads/{name[:50]}')

# PHASE 2
print('\n--- Phase 2: Ollama full delete ---')
safe_delete(os.path.join(USER, '.ollama'), '.ollama (model data)')
safe_delete(os.path.join(LOCAL, 'Ollama'), 'AppData/Local/Ollama')

# PHASE 3
print('\n--- Phase 3: Green-light caches/temp ---')

# 3.1 Temp
print('  Cleaning Temp...')
temp_freed = 0
temp_failed = 0
for f in os.listdir(long_path(TEMP)):
    fp = os.path.join(TEMP, f)
    try:
        if os.path.isfile(long_path(fp)):
            sz = os.path.getsize(long_path(fp))
            send2trash.send2trash(fp)
            temp_freed += sz
        elif os.path.isdir(long_path(fp)):
            sz = dir_size(fp)
            send2trash.send2trash(fp)
            temp_freed += sz
    except:
        temp_failed += 1
freed_total += temp_freed
results.append(('OK', f'Temp (skipped {temp_failed} locked)', temp_freed, TEMP))

# 3.2 Redundant backup
safe_delete(os.path.join(USER, '.newmax.zip'), '.newmax.zip (redundant backup)')

# 3.3 Dev caches
safe_delete(os.path.join(LOCAL, 'npm-cache'), 'npm-cache')
safe_delete(os.path.join(LOCAL, 'pnpm'), 'pnpm store')
safe_delete(os.path.join(LOCAL, 'pnpm-cache'), 'pnpm-cache')
safe_delete(os.path.join(USER, '.cache'), '.cache')

# pip cache
for p in [os.path.join(LOCAL, 'pip', 'Cache'), os.path.join(LOCAL, 'pip', 'cache')]:
    if os.path.exists(p):
        safe_delete(p, 'pip cache')
        break

# uv
safe_delete(os.path.join(LOCAL, 'uv'), 'uv cache')

# Playwright
safe_delete(os.path.join(LOCAL, 'ms-playwright'), 'ms-playwright browsers')

# Chromium
safe_delete(os.path.join(USER, '.chromium-browser-snapshots'), 'Chromium snapshots')

# 3.4 Updater caches
for name in ['bohrium-updater','termius-updater','geniezone-updater',
             'obsidian-updater','mubu-updater','bilibili-updater',
             'recordly-updater','xmind-updater','quark-updater',
             'stepfun-updater','dingtalk-updater','feishu-updater']:
    safe_delete(os.path.join(LOCAL, name), f'updater/{name}')

# 3.5 CrashDumps
safe_delete(os.path.join(LOCAL, 'CrashDumps'), 'CrashDumps')

# 3.6 wx_key
safe_delete(os.path.join(LOCAL, 'wx_key_v218'), 'wx_key temp')

# 3.7 VSCode installer cache
for f in os.listdir(long_path(TEMP)):
    if f.startswith('vscode-') and f.endswith('.exe'):
        safe_delete(os.path.join(TEMP, f), f'VSCode installer/{f}')

# SUMMARY
print('\n' + '=' * 60)
print('CLEANUP RESULTS')
print('=' * 60)
for status, desc, size, path in results:
    if status == 'OK' and size > 0:
        print(f'  [OK]   {desc}: {size/1024/1024:.0f} MB')
    elif status == 'FAIL':
        print(f'  [FAIL] {desc}: {path}')
    elif status == 'SKIP':
        print(f'  [SKIP] {desc}')

print(f'\nTotal freed: {freed_total/1024/1024/1024:.1f} GB')
print('All files moved to Recycle Bin - recoverable if needed')
