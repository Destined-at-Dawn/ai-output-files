# -*- coding: utf-8 -*-
"""Sanitize and copy rules from mutual workspace to niuma-engine repo."""
import os
import re
import shutil

REPO = r"C:\Users\13975\AppData\Local\Temp\niuma-engine"
RULES_SRC = r"E:\ai产出文件\牛马\mutual\mutual\.claude\rules"
RULES_DST = os.path.join(REPO, ".claude", "rules")
ARCHIVE = r"E:\ai产出文件\牛马\归档\2026-06-22-niuma-engine-backup"

# Rules to skip (too personal / low info density)
SKIP = {
    "voice-dna-auto-inject.md",
    "preference-memory.md",
    "identity-consistency.md",
}

# ============================================================
# Phase 1: Backup and fix .gitignore
# ============================================================
os.makedirs(ARCHIVE, exist_ok=True)

gitignore_path = os.path.join(REPO, ".gitignore")
shutil.copy2(gitignore_path, os.path.join(ARCHIVE, ".gitignore"))

with open(gitignore_path, "r", encoding="utf-8") as f:
    gi = f.read()

# Change .claude/ to allow .claude/rules/ through
gi_new = gi.replace(".claude/", ".claude/*\n!.claude/rules/")
with open(gitignore_path, "w", encoding="utf-8") as f:
    f.write(gi_new)
print("[OK] .gitignore fixed")

# ============================================================
# Phase 2: Copy and sanitize all rules
# ============================================================
os.makedirs(RULES_DST, exist_ok=True)

# Sanitization patterns (find → replace, applied in order)
SANITIZE = [
    # Workspace paths (most specific first)
    (r"E:\\ai产出文件\\牛马\\mutual\\mutual\\", "{workspace}/"),
    (r"${WORKSPACE_ROOT}/", "{workspace}/"),
    # Knowledge hub
    (r"E:\\ai产出文件\\牛马\\知识中枢\\", "{knowledge-hub}/"),
    (r"${KNOWLEDGE_HUB}/", "{knowledge-hub}/"),
    # Other workspace dirs
    (r"E:\\ai产出文件\\牛马\\([^\\]+)\\([^\\]+)\\", r"{workspace}/\1/\2/"),
    (r"${LEGACY_ROOT}/([^/]+)/([^/]+)/", r"{workspace}/\1/\2/"),
    # User paths
    (r"C:\\Users\\13975\\.newmax\\", "{newmax-home}/"),
    (r"${NEWMAX_HOME}/", "{newmax-home}/"),
    (r"C:\\Users\\13975\\AppData\\Local\\hermes\\", "{hermes-home}/"),
    (r"C:\\Users\\13975\\", "{user-home}/"),
    (r"C:/Users/13975/", "{user-home}/"),
    # Archive path pattern
    (r"E:\\ai产出文件\\牛马\\归档\\", "{archive}/"),
    (r"${LEGACY_ROOT}/归档/", "{archive}/"),
]

def sanitize(content):
    for pattern, replacement in SANITIZE:
        content = re.sub(pattern, replacement, content)
    return content

# Backup existing repo rules first
existing_rules = os.path.join(RULES_DST)
if os.path.exists(existing_rules):
    for f in os.listdir(existing_rules):
        if f.endswith(".md"):
            src = os.path.join(existing_rules, f)
            dst = os.path.join(ARCHIVE, f"old_{f}")
            shutil.copy2(src, dst)

# Copy all rules
all_rules = sorted([f for f in os.listdir(RULES_SRC) if f.endswith(".md")])
print(f"\nFound {len(all_rules)} rule files in mutual workspace")

copied = 0
skipped_list = []
for rule_file in all_rules:
    if rule_file in SKIP:
        skipped_list.append(rule_file)
        print(f"  SKIP: {rule_file}")
        continue

    src_path = os.path.join(RULES_SRC, rule_file)
    dst_path = os.path.join(RULES_DST, rule_file)

    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = sanitize(content)

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(content)

    copied += 1
    orig_size = os.path.getsize(src_path)
    new_size = os.path.getsize(dst_path)
    print(f"  COPY: {rule_file} ({orig_size} -> {new_size} bytes)")

print(f"\n=== SUMMARY ===")
print(f"Copied: {copied}")
print(f"Skipped: {len(skipped_list)}")
if skipped_list:
    print(f"  {', '.join(skipped_list)}")

# Verify - list final state
print(f"\nRepo .claude/rules/ contains {len(os.listdir(RULES_DST))} files:")
for f in sorted(os.listdir(RULES_DST)):
    size = os.path.getsize(os.path.join(RULES_DST, f))
    print(f"  {f} ({size} bytes)")
