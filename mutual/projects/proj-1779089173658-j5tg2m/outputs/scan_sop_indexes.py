import os, json

# 1. Scan all SOP总索引 files
sop_indexes = []
for root, dirs, files in os.walk(r'E:\ai产出文件\牛马'):
    for f in files:
        if 'SOP总索引' in f and f.endswith('.md'):
            path = os.path.join(root, f)
            sop_indexes.append(path)

results = []
for path in sop_indexes:
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        # Extract routing sections
        routing_data = {
            'path': path,
            'size': len(content),
            'has_routing': False,
            'has_chain': False,
            'has_self_learning': False,
        }
        for keyword in ['消息路由', '输入分发', 'IF/ELSE', 'intent', '路由规则']:
            if keyword in content:
                routing_data['has_routing'] = True
                break
        for keyword in ['链式调用', 'skill chain', 'Skill Chain', '调用链']:
            if keyword in content:
                routing_data['has_chain'] = True
                break
        for keyword in ['自学习', 'self-learn', '反馈闭环', 'Feedback']:
            if keyword in content:
                routing_data['has_self_learning'] = True
                break
        results.append(routing_data)
    except Exception as e:
        results.append({'path': path, 'error': str(e)})

# 2. Scan all SOP files for skill chains
all_sops = []
for root, dirs, files in os.walk(r'E:\ai产出文件\牛马'):
    # Skip node_modules and .git
    dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '归档']]
    for f in files:
        if f.startswith('sop-') and f.endswith('.md') and f != 'sop-indexes.txt':
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                # Extract skill chain
                has_li = 'li-' in content
                has_chain = any(k in content for k in ['Skill Chain', 'skill chain', '调用链', 'Chain'])
                all_sops.append({
                    'path': path,
                    'name': f,
                    'size': len(content),
                    'has_li': has_li,
                    'has_chain': has_chain,
                })
            except:
                pass

# 3. Scan all SOPs that reference li- skills
li_skill_usage = {}
for sop in all_sops:
    if sop.get('has_li'):
        try:
            with open(sop['path'], 'r', encoding='utf-8') as fh:
                content = fh.read()
            import re
            li_skills = re.findall(r'li-\w+', content)
            for skill in set(li_skills):
                if skill not in li_skill_usage:
                    li_skill_usage[skill] = []
                li_skill_usage[skill].append(sop['name'])
        except:
            pass

# Output results
output = {
    'sop_indexes': results,
    'total_sops': len(all_sops),
    'sops_with_li': len([s for s in all_sops if s.get('has_li')]),
    'sops_with_chain': len([s for s in all_sops if s.get('has_chain')]),
    'li_skill_usage': {k: len(v) for k, v in sorted(li_skill_usage.items(), key=lambda x: -len(x[1]))},
    'all_sop_names': [s['name'] for s in all_sops],
}

out_path = os.path.join(r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs', 'sop-scan.json')
with open(out_path, 'w', encoding='utf-8') as fh:
    json.dump(output, fh, ensure_ascii=False, indent=2)

print(f'Wrote {out_path}')
print(f'SOP indexes: {len(results)}')
print(f'Total SOPs: {len(all_sops)}')
print(f'SOPs with li- skills: {len([s for s in all_sops if s.get("has_li")])}')
print(f'SOPs with skill chains: {len([s for s in all_sops if s.get("has_chain")])}')
print(f'li- skill usage (top 10):')
for k, v in list(li_skill_usage.items())[:10]:
    print(f'  {k}: referenced by {len(v)} SOPs')
