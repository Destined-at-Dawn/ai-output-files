import os, json, re

skills_dir = os.path.expanduser('~/.newmax/skills')
route_path = os.path.expanduser('~/.newmax/skills/skill-routing-table.json')

# Fix 1: Read routing table
rt = None
for p in [route_path,
          os.path.expanduser('~/.newmax/skill-routing-table.json')]:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            rt = json.load(f)
        route_path = p
        break

if not rt:
    # Search everywhere
    for root, dirs, files in os.walk(os.path.expanduser('~/.newmax')):
        if 'skill-routing-table.json' in files:
            route_path = os.path.join(root, 'skill-routing-table.json')
            with open(route_path, 'r', encoding='utf-8') as f:
                rt = json.load(f)
            break

if not rt:
    print("ERROR: Route table not found")
    exit(1)

routes = rt.get('routes', [])

# Fix 2: Remove duplicate route IDs
seen_ids = {}
dup_ids = []
for i, r in enumerate(routes):
    rid = r.get('id', '')
    if rid in seen_ids:
        dup_ids.append(i)
    else:
        seen_ids[rid] = i

# Remove duplicates (keep first occurrence)
if dup_ids:
    for i in sorted(dup_ids, reverse=True):
        del routes[i]
    print(f"Removed {len(dup_ids)} duplicate route IDs")

# Fix 3: Remove routes pointing to deleted skills
li_skills = set()
for d in os.listdir(skills_dir):
    if os.path.isdir(os.path.join(skills_dir, d)):
        if not os.path.exists(os.path.join(skills_dir, d, 'DEPRECATED.md')):
            li_skills.add(d)

# Filter out routes to non-existent skills
valid_routes = []
removed = 0
for r in routes:
    skill = r.get('skill', '')
    if skill and skill in li_skills:
        valid_routes.append(r)
    elif skill:
        # Check if it exists as non-li skill
        if os.path.exists(os.path.join(skills_dir, skill)):
            valid_routes.append(r)
        else:
            removed += 1

if removed:
    print(f"Removed {removed} phantom routes (skill directory doesn't exist)")
    routes = valid_routes

# Fix 4: Find li-* skills without routes
li_with_routes = set()
for r in routes:
    li_with_routes.add(r.get('skill', ''))

li_no_route = [d for d in li_skills if d.startswith('li-') and d not in li_with_routes]
if li_no_route:
    print(f"Skills missing routes: {li_no_route}")

# Fix 5: Deduplicate triggers across skills
trigger_map = {}  # trigger -> first skill that owns it
dup_triggers = []
for r in routes:
    skill = r.get('skill', '')
    new_triggers = []
    for t in r.get('triggers', []):
        if t in trigger_map:
            if trigger_map[t] == skill:
                # Same skill duplicate - remove
                dup_triggers.append(f"{skill}: {t}")
                continue
            else:
                # Cross-skill duplicate - keep first, remove this one
                dup_triggers.append(f"{t}: {trigger_map[t]} vs {skill}")
                continue
        trigger_map[t] = skill
        new_triggers.append(t)
    r['triggers'] = new_triggers

if dup_triggers:
    print(f"Cleaned {len(dup_triggers)} duplicate triggers")

# Save cleaned table
rt['routes'] = routes
with open(route_path, 'w', encoding='utf-8') as f:
    json.dump(rt, f, ensure_ascii=False, indent=2)

# Count stats
li_count = len([r for r in routes if r.get('skill', '').startswith('li-')])
total_triggers = sum(len(r.get('triggers', [])) for r in routes)
li_triggers = sum(len(r.get('triggers', [])) for r in routes if r.get('skill', '').startswith('li-'))

print(f"\n=== FINAL STATS ===")
print(f"Total routes: {len(routes)}")
print(f"Li- routes: {li_count}")
print(f"Total triggers: {total_triggers}")
print(f"Li- triggers: {li_triggers}")
print(f"Duplicate IDs: 0")
print(f"Phantom routes: 0")

# Quality audit all li-* skills
print(f"\n=== QUALITY AUDIT ===")
issues = []
for d in sorted(li_skills):
    if not d.startswith('li-'):
        continue
    skill_path = os.path.join(skills_dir, d, 'SKILL.md')
    if not os.path.exists(skill_path):
        continue

    with open(skill_path, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = len(text.split('\n'))

    checks = {
        'cases': bool(re.search(r'## (案例|Case Stud)', text)),
        'anti': bool(re.search(r'## (反模式|Anti)', text)),
        'linked': bool(re.search(r'## (联动|Linked)', text)),
        'theory': bool(re.search(r'(T1|T2|理论锚点|Theoretical)', text)),
        'conditions': bool(re.search(r'## (条件|Conditions)', text)),
    }

    meta_ok = os.path.exists(os.path.join(skills_dir, d, '_meta.json'))
    eval_ok = os.path.exists(os.path.join(skills_dir, d, 'eval.json'))
    gr_ok = os.path.exists(os.path.join(skills_dir, d, 'golden_rules.md'))

    status = 'OK'
    missing = []

    if lines > 300:
        status = 'FAIL'
        missing.append(f'OVERSIZE:{lines}')
    if not meta_ok:
        missing.append('meta')
        status = 'WARN'
    if not eval_ok:
        missing.append('eval')
        status = 'WARN'
    if not gr_ok:
        missing.append('golden_rules')
        status = 'WARN'
    if not checks['cases']:
        missing.append('cases')
        status = 'WARN'
    if not checks['anti']:
        missing.append('anti')
        status = 'WARN'
    if not checks['linked']:
        missing.append('linked')
        status = 'WARN'

    if missing:
        issues.append(f"{status} {d}: {lines}L | missing: {', '.join(missing)}")
    else:
        issues.append(f"OK {d}: {lines}L")

for i in issues:
    print(i)

ok_count = len([i for i in issues if i.startswith('OK')])
warn_count = len([i for i in issues if i.startswith('WARN')])
fail_count = len([i for i in issues if i.startswith('FAIL')])
print(f"\nPASS: {ok_count} | WARN: {warn_count} | FAIL: {fail_count}")
