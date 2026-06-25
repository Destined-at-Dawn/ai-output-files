#!/usr/bin/env python3
"""Audit all li-* skills for quality metrics."""
import os, json

SKILLS_DIR = r"C:\Users\13975\.newmax\skills"

results = []
for d in sorted(os.listdir(SKILLS_DIR)):
    if not d.startswith("li"):
        continue
    skill_dir = os.path.join(SKILLS_DIR, d)
    if not os.path.isdir(skill_dir):
        continue
    # Skip non-skill dirs
    if d in ["li-series-skills-20260607", "li-series-skills-v2-20260607"]:
        continue

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        continue

    size = os.path.getsize(skill_md)
    with open(skill_md, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    line_count = len(lines)

    # Check quality markers
    content = "".join(lines)
    has_theory = any(k in content for k in ["理论锚点", "认知科学", "Theory", "T1", "T2"])
    has_cases = any(k in content for k in ["案例", "Case", "真实场景", "实战"])
    has_antipatterns = any(k in content for k in ["反模式", "Anti-pattern", "Anti-illusion", "禁止模式"])
    has_golden = os.path.exists(os.path.join(skill_dir, "golden_rules.md"))
    has_eval = os.path.exists(os.path.join(skill_dir, "eval.json"))
    has_meta = os.path.exists(os.path.join(skill_dir, "_meta.json"))
    has_refs = os.path.isdir(os.path.join(skill_dir, "references"))

    # Count reference files
    ref_dir = os.path.join(skill_dir, "references")
    ref_count = 0
    ref_size = 0
    if os.path.isdir(ref_dir):
        for f in os.listdir(ref_dir):
            fp = os.path.join(ref_dir, f)
            if os.path.isfile(fp) and not f.startswith("."):
                ref_count += 1
                ref_size += os.path.getsize(fp)

    # Check golden_rules size
    gr_path = os.path.join(skill_dir, "golden_rules.md")
    gr_size = os.path.getsize(gr_path) if os.path.exists(gr_path) else 0

    # Count DEPRECATED
    is_deprecated = os.path.exists(os.path.join(skill_dir, "DEPRECATED.md"))

    results.append({
        "name": d,
        "lines": line_count,
        "size_kb": round(size/1024, 1),
        "theory": has_theory,
        "cases": has_cases,
        "antipatterns": has_antipatterns,
        "golden_rules": gr_size,
        "eval": has_eval,
        "meta": has_meta,
        "ref_count": ref_count,
        "ref_kb": round(ref_size/1024, 1),
        "deprecated": is_deprecated
    })

# Print summary
print(f"=== LI-SERIES QUALITY AUDIT ===")
print(f"Total: {len(results)} skills")
print()

# Sort by quality score
for r in sorted(results, key=lambda x: x["lines"]):
    quality = sum([
        r["theory"], r["cases"], r["antipatterns"],
        r["golden_rules"] > 500, r["eval"], r["meta"],
        r["ref_count"] > 0, r["lines"] <= 300
    ])
    status = "PASS" if quality >= 6 else "WARN" if quality >= 4 else "FAIL"
    dep = " [DEPRECATED]" if r["deprecated"] else ""
    print(f"{r['name']:25s} {r['lines']:4d}L {r['size_kb']:6.1f}KB refs={r['ref_count']:2d}({r['ref_kb']:5.1f}KB) "
          f"T={'Y' if r['theory'] else 'N'} C={'Y' if r['cases'] else 'N'} A={'Y' if r['antipatterns'] else 'N'} "
          f"GR={r['golden_rules']:>5d}B eval={'Y' if r['eval'] else 'N'} "
          f"→ {quality}/8 {status}{dep}")

# Count pass/warn/fail
pass_count = sum(1 for r in results if sum([r["theory"], r["cases"], r["antipatterns"], r["golden_rules"]>500, r["eval"], r["meta"], r["ref_count"]>0, r["lines"]<=300]) >= 6)
warn_count = sum(1 for r in results if 4 <= sum([r["theory"], r["cases"], r["antipatterns"], r["golden_rules"]>500, r["eval"], r["meta"], r["ref_count"]>0, r["lines"]<=300]) < 6)
fail_count = sum(1 for r in results if sum([r["theory"], r["cases"], r["antipatterns"], r["golden_rules"]>500, r["eval"], r["meta"], r["ref_count"]>0, r["lines"]<=300]) < 4 and not r["deprecated"])

print(f"\nPASS: {pass_count} | WARN: {warn_count} | FAIL: {fail_count}")
