# -*- coding: utf-8 -*-
"""Full audit of all li- skills: real size, routing coverage, quality."""
import os, json

BASE = os.path.expanduser(r"~\.newmax\skills")
RT_PATH = os.path.expanduser(r"~\.newmax\skills\skill-routing-table.json")

# 1. List all li- dirs with SKILL.md
li_skills = {}
for d in sorted(os.listdir(BASE)):
    full = os.path.join(BASE, d)
    skill_md = os.path.join(full, "SKILL.md")
    if d.startswith("li") and os.path.isdir(full) and os.path.exists(skill_md):
        size = os.path.getsize(skill_md)
        lines = 0
        with open(skill_md, 'r', encoding='utf-8', errors='ignore') as f:
            lines = sum(1 for _ in f)
        # Check for key sections
        with open(skill_md, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        has_cases = any(x in content for x in ["案例库", "Case Stud", "案例"])
        has_anti = any(x in content for x in ["反模式", "Anti-Pattern", "反面"])
        has_golden = os.path.exists(os.path.join(full, "golden_rules.md"))
        golden_size = os.path.getsize(os.path.join(full, "golden_rules.md")) if has_golden else 0
        has_eval = os.path.exists(os.path.join(full, "eval.json"))
        has_meta = os.path.exists(os.path.join(full, "_meta.json"))
        refs = os.path.join(full, "references")
        ref_count = 0
        ref_size = 0
        if os.path.isdir(refs):
            for f2 in os.listdir(refs):
                fp = os.path.join(refs, f2)
                if os.path.isfile(fp) and f2 != ".gitkeep":
                    ref_count += 1
                    ref_size += os.path.getsize(fp)
        dep_exists = os.path.exists(os.path.join(full, "DEPRECATED.md"))

        li_skills[d] = {
            "lines": lines,
            "size": size,
            "has_cases": has_cases,
            "has_anti": has_anti,
            "golden_size": golden_size,
            "has_eval": has_eval,
            "has_meta": has_meta,
            "ref_count": ref_count,
            "ref_size": ref_size,
            "deprecated": dep_exists
        }

# 2. Check routing coverage
routes = {}
if os.path.exists(RT_PATH):
    with open(RT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for r in data.get("routes", []):
        sk = r.get("skill", "")
        if sk.startswith("li"):
            if sk not in routes:
                routes[sk] = {"count": 0, "triggers": 0}
            routes[sk]["count"] += 1
            routes[sk]["triggers"] += len(r.get("triggers", []))

# 3. Print report
print("=" * 80)
print(f"LI-SERIES AUDIT: {len(li_skills)} skills")
print("=" * 80)

no_route = []
low_quality = []

for name, info in sorted(li_skills.items()):
    if info["deprecated"]:
        status = "DEPRECATED"
    else:
        issues = []
        if not info["has_cases"]: issues.append("no-cases")
        if not info["has_anti"]: issues.append("no-anti")
        if info["golden_size"] < 500: issues.append("weak-rules")
        if not info["has_eval"]: issues.append("no-eval")
        if name not in routes: issues.append("NO-ROUTE")
        status = ", ".join(issues) if issues else "OK"

    rt = routes.get(name, {})
    rt_info = f"r:{rt.get('count',0)}/t:{rt.get('triggers',0)}" if rt else "NO-ROUTE"

    if name not in routes and not info["deprecated"]:
        no_route.append(name)
    if not info["has_cases"] and not info["deprecated"]:
        low_quality.append(name)

    print(f"  {name:25s} {info['lines']:4d}L {info['size']//1024:3d}KB "
          f"refs:{info['ref_count']:2d} {rt_info:15s} [{status}]")

print(f"\nSUMMARY:")
print(f"  Total: {len(li_skills)}")
print(f"  Active (no DEPRECATED): {sum(1 for v in li_skills.values() if not v['deprecated'])}")
print(f"  Deprecated: {sum(1 for v in li_skills.values() if v['deprecated'])}")
print(f"  Has routing: {sum(1 for n in li_skills if n in routes)}")
print(f"  NO routing: {len(no_route)} -> {no_route}")
print(f"  No case studies: {len(low_quality)} -> {low_quality}")
print(f"  Over 300 lines: {[n for n,v in li_skills.items() if v['lines'] > 300 and not v['deprecated']]}")
