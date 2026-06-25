# -*- coding: utf-8 -*-
"""Lightweight cleanup of chrome-profiles cache - keep login data intact"""
import os, shutil

base = os.path.expanduser(r'~\.newmax\chrome-profiles\bp-default')

# Target dirs to delete (cache only, NOT login data)
targets = [
    os.path.join(base, 'OptGuideOnDeviceModel'),
    os.path.join(base, 'Default', 'Service Worker'),
    os.path.join(base, 'Default', 'Cache'),
    os.path.join(base, 'Default', 'Code Cache'),
]

# ======== Step 1: Check C: free space ========
before = shutil.disk_usage('C:\\')
print(f'C drive free before cleanup: {before.free / 1e9:.1f} GB')

# ======== Step 2: Dry-run - check sizes ========
print('\n=== DRY RUN ===')
total_size = 0
for t in targets:
    if os.path.exists(t):
        size = 0
        for root, dirs, files in os.walk(t):
            for f in files:
                try:
                    size += os.path.getsize(os.path.join(root, f))
                except:
                    pass
        print(f'  [WOULD DELETE] {t} ({size / 1e9:.2f} GB)')
        total_size += size
    else:
        print(f'  [MISSING] {t}')

print(f'\n  Total would free: {total_size / 1e9:.2f} GB')
print(f'  C drive after: {(before.free + total_size) / 1e9:.1f} GB')

# ======== Step 3: Ask and execute ========
print('\n=== EXECUTING ===')
deleted = 0
errors = []

for t in targets:
    if os.path.exists(t):
        try:
            shutil.rmtree(t)
            print(f'  [DELETED] {os.path.basename(t)}')
            deleted += 1
        except Exception as e:
            errors.append((t, str(e)))
            print(f'  [FAILED] {os.path.basename(t)}: {e}')

# ======== Step 4: Verify ========
print(f'\n=== RESULT ===')
print(f'  Deleted: {deleted}/{len(targets)} dirs')
if errors:
    for path, err in errors:
        print(f'  FAILED: {path} - {err}')

after = shutil.disk_usage('C:\\')
freed = after.free - before.free
print(f'  C drive free: {before.free/1e9:.1f} GB -> {after.free/1e9:.1f} GB')
print(f'  Freed: {freed/1e9:.2f} GB')

# ======== Step 5: Confirm login data intact ========
print('\n=== LOGIN DATA INTEGRITY ===')
sensitive = ['Login Data', 'Web Data', 'Preferences', 'Cookies']
for s in sensitive:
    path = os.path.join(base, 'Default', s)
    if os.path.exists(path):
        print(f'  [OK] {s}: {os.path.getsize(path)/1e3:.1f} KB')
    else:
        print(f'  [MISSING!] {s}')
