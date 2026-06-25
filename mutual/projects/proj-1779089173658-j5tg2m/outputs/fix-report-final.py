#!/usr/bin/env python3
"""Comprehensive final fix for skill-bloat-analysis report.

Uses ONLY verified numbers from direct filesystem/routing-table reads.
"""
import os

report_path = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\skill-bloat-analysis-2026-06-22.md'

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ===== VERIFIED NUMBERS (from direct verification) =====
# Route entries: 105
# Unique skills in routes: 105
# Total skill dirs: 126 (os.listdir)
# SKILL.md files: 124 (126 - 2 empty dirs)
# Active skills (no DEPRECATED.md): 107
# Deprecated skills (has DEPRECATED.md): 17
# Deprecated with routes: 14
# Deprecated without routes: 3
# Active with routes: 89
# Active without routes (ghost): 20 (NOT 18!)
# Total triggers raw: 1651
# Unique triggers: 1639
# Trigger conflicts: 12

# CRITICAL CORRECTIONS NEEDED:
# 1. Ghost skills: 18 -> 20
# 2. Some other numbers derived from 18 need updating

changes = []

# Fix ghost skills count: 18 -> 20
old = '18 个活跃 skill 没有路由条目'
new = '20 个活跃 skill 没有路由条目'
if old in content:
    content = content.replace(old, new)
    changes.append(f'Ghost skills: 18 -> 20')

# Fix all occurrences of "18 幽灵" -> "20 幽灵"
content = content.replace('18 个幽灵', '20 个幽灵')
content = content.replace('18 幽灵', '20 幽灵')

# Fix "107 活跃 - 89 有路由 = 18" -> "107 活跃 - 87 有路由 = 20"
# Wait: 107 active - 20 ghost = 87 with routes. Let me verify:
# Active with routes: 89 (from verification). But 107 - 20 = 87.
# Hmm, 89 != 87. Let me re-check.
#
# From verification: active_with_routes = 89, active_without_routes = 20
# 89 + 20 = 109. But we said 107 active.
#
# The bash script counted 109 active (including 2 empty dirs).
# The Python script counted 107 active (excluding 2 empty dirs).
#
# The bash script's 109 = 107 real active + 2 empty dirs (no DEPRECATED.md, no SKILL.md)
# The Python script's 107 = only dirs with SKILL.md and no DEPRECATED.md
#
# Which is correct? The bash script is more accurate - it counts all dirs without DEPRECATED.md.
# So the REAL active count is 109, not 107.
#
# Wait, but the 2 empty dirs have no SKILL.md - they're not functional skills.
# The report should use 107 (functional skills with SKILL.md) or 109 (all dirs without DEPRECATED.md)?
#
# The report's definition of "active skill" = no DEPRECATED.md. By that definition, 109.
# But the report also says "124 有 SKILL.md" - so only 124 are functional.
#
# I think the report should use 107 (skills with both SKILL.md and no DEPRECATED.md)
# because empty dirs aren't real skills.
#
# BUT: the routing table references 105 unique skills. If only 107 have SKILL.md,
# and 14 deprecated have routes, then 107 - 14 = 93 active with SKILL.md.
# But we counted 89 active with routes. 93 != 89.
#
# Something is off. Let me re-examine.
#
# The bash script counted:
# - 126 total dirs
# - 109 without DEPRECATED.md (active)
# - 17 with DEPRECATED.md (deprecated)
# - Of 109 active: 89 with routes, 20 without
# - Of 17 deprecated: 14 with routes, 3 without
# - Total: 109 + 17 = 126 ✓
# - Total routed: 89 + 14 = 103
# - Route entries: 105 (2 skills have multiple route entries)
#
# The Python script counted:
# - 124 dirs with SKILL.md
# - 2 empty dirs
# - 124 = 107 active + 17 deprecated
#
# So: 107 active (with SKILL.md) + 17 deprecated (with SKILL.md) = 124
# Plus 2 empty dirs = 126 total
#
# But bash says 109 active without DEPRECATED.md.
# 109 - 107 = 2. Those are the 2 empty dirs (no SKILL.md, no DEPRECATED.md).
#
# So the REAL count depends on definition:
# - By "has SKILL.md": 107 active, 17 deprecated
# - By "no DEPRECATED.md": 109 active, 17 deprecated
#
# The report should use "has SKILL.md" as the definition of a real skill.
# So 107 active is correct. But then the routing table references 105 unique skills.
# 107 active + 17 deprecated = 124 with SKILL.md.
# 105 unique skills in routes.
# 105 - 14 deprecated = 91 active skills with routes.
# 107 active - 91 = 16 ghost skills (not 18 or 20!).
#
# Wait, this doesn't match the bash output either (89 active with routes).
#
# I think the issue is that the bash script's routing table check includes
# skills that don't have SKILL.md (the 2 empty dirs).
# If 2 empty dirs happen to be in the routing table, they'd be counted as
# "active with routes" even though they have no SKILL.md.
#
# Let me check which skills are in the routes but have no SKILL.md.

# For now, let me use the most rigorous definition:
# REAL skills = directories with SKILL.md
# Active = has SKILL.md + no DEPRECATED.md = 107
# Deprecated = has SKILLATED.md + has DEPRECATED.md = 17
# Ghost = active (107) - active_with_routes_among_real_skills

# I need to re-run the verification with this stricter filter
print("Need to re-verify with stricter filter (only dirs with SKILL.md)")
print("Current report uses 107 active / 17 deprecated")
print("Ghost count needs recalculation")
