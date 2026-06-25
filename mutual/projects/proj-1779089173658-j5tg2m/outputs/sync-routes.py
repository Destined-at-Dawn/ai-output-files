#!/usr/bin/env python3
"""Sync routing table to all workspaces with CLAUDE.md."""
import os, shutil, json

SKILLS_DIR = r"C:\Users\13975\.newmax\skills"
RT_PATH = os.path.join(SKILLS_DIR, "skill-routing-table.json")

# Load and verify routing table
with open(RT_PATH, encoding="utf-8") as f:
    data = json.load(f)

rt_size = os.path.getsize(RT_PATH)
rt_routes = len(data["routes"])

# Find all CLAUDE.md
BASE = r"E:\ai产出文件\牛马"
claude_files = []
for root, dirs, files in os.walk(BASE):
    if "CLAUDE.md" in files:
        claude_files.append(os.path.join(root, "CLAUDE.md"))

# Also check personal workspace
PERSONAL_BASE = r"E:\ai产出文件\个人"
if os.path.exists(PERSONAL_BASE):
    for root, dirs, files in os.walk(PERSONAL_BASE):
        if "CLAUDE.md" in files:
            claude_files.append(os.path.join(root, "CLAUDE.md"))

# Remove duplicates
claude_files = list(set(claude_files))

# Skip third-party repos (github downloads, .shared)
skip_patterns = [".shared", "归档", "archive", "node_modules", ".git"]
user_workspaces = []
for cf in claude_files:
    skip = False
    for pattern in skip_patterns:
        if pattern in cf.lower():
            skip = True
            break
    if skip:
        continue
    user_workspaces.append(os.path.dirname(cf))

synced = 0
already_ok = 0
failed = []

for ws_dir in user_workspaces:
    rt_dest = os.path.join(ws_dir, "skill-routing-table.json")
    try:
        shutil.copy2(RT_PATH, rt_dest)
        # Verify
        if os.path.exists(rt_dest) and os.path.getsize(rt_dest) == rt_size:
            synced += 1
        else:
            failed.append(ws_dir)
    except Exception as e:
        failed.append((ws_dir, str(e)))

print(f"=== ROUTE SYNC COMPLETE ===")
print(f"User workspaces found: {len(user_workspaces)}")
print(f"Synced: {synced}")
print(f"Failed: {len(failed)}")
if failed:
    for f in failed[:5]:
        print(f"  FAIL: {f}")
