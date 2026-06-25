#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiumaAutoCommit - Auto commit and push script.
Called every 2 hours by Windows Task Scheduler.
"""
import subprocess, os, sys, datetime

GIT_ROOT = r"E:\ai产出文件\牛马"
LOG_DIR = os.path.join(GIT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "auto-commit.log")

os.makedirs(LOG_DIR, exist_ok=True)

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} | {msg}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)

def run(cmd, **kw):
    return subprocess.run(cmd, cwd=GIT_ROOT, capture_output=True, text=True, encoding="utf-8", **kw)

try:
    os.chdir(GIT_ROOT)
except Exception as e:
    log(f"ERROR: Cannot cd to {GIT_ROOT}: {e}")
    sys.exit(1)

# Verify git repo
r = run(["git", "rev-parse", "--git-dir"])
if r.returncode != 0:
    log(f"ERROR: Not a git repo at {GIT_ROOT}")
    sys.exit(1)

# Check for changes
r = run(["git", "status", "--porcelain"])
if not r.stdout.strip():
    log("INFO: No changes to commit")
    sys.exit(0)

lines = [l for l in r.stdout.strip().split("\n") if l.strip()]
modified = sum(1 for l in lines if l.startswith(" M") or l.startswith("M "))
untracked = sum(1 for l in lines if l.startswith("??"))
deleted = sum(1 for l in lines if l.startswith(" D") or l.startswith("D "))
total = len(lines)

log(f"INFO: Found {total} changes (M:{modified} U:{untracked} D:{deleted})")

# Stage all
run(["git", "add", "-A"])

# Auto-detect type/scope
commit_type = "chore"
scope = "auto"
if modified > 0 and untracked == 0 and deleted == 0:
    commit_type = "fix"
    scope = "sync"
elif untracked > modified:
    commit_type = "feat"

status_text = r.stdout
if "memory/" in status_text:
    scope = "memory"
elif "sop" in status_text.lower():
    scope = "sop"
elif any(x in status_text for x in [".json", ".yaml", ".yml", "CLAUDE.md"]):
    scope = "config"

date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
commit_msg = (
    f"{commit_type}({scope}): auto batch commit {date}\n\n"
    f"Changes: {total} files ({modified} modified, {untracked} new, {deleted} deleted)\n"
    f"Auto-committed by NiumaAutoCommit scheduled task\n\n"
    f"Agent-Task: auto-scheduled\n"
    f"Agent-Model: auto-commit.py\n"
    f"Agent-Decision: batch commit {total} changes\n"
    f"Agent-Limitation: no semantic review, auto-detected type={commit_type} scope={scope}"
)

r = run(["git", "commit", "-m", commit_msg])
if r.returncode == 0:
    log(f"OK: Committed {commit_type}({scope}): {total} files")

    # Get current branch
    br = run(["git", "branch", "--show-current"])
    branch = br.stdout.strip() or "main"

    # Push to GitHub
    r_push = run(["git", "push", "origin", branch])
    if r_push.returncode == 0:
        log(f"OK: Pushed to GitHub (origin/{branch})")
    else:
        log(f"WARN: GitHub push failed: {r_push.stderr.strip()}")

    # Push to Gitee
    r_push = run(["git", "push", "gitee", branch])
    if r_push.returncode == 0:
        log(f"OK: Pushed to Gitee (gitee/{branch})")
    else:
        log(f"WARN: Gitee push failed: {r_push.stderr.strip()}")
else:
    log(f"WARN: Commit failed: {r.stderr.strip()}")
    run(["git", "reset", "HEAD"])

log("INFO: Script finished")
