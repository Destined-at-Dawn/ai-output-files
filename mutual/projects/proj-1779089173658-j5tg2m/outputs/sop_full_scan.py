import os, json

all_sops = []
for root, dirs, files in os.walk(r'E:\ai产出文件\牛马'):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '归档']]
    for f in files:
        if f.endswith('.md'):
            if any(k in f.lower() for k in ['sop-', 'sop_', '总索引']):
                fp = os.path.join(root, f)
                try:
                    size = os.path.getsize(fp)
                    # Extract workspace from path
                    rel = fp.replace(r'E:\ai产出文件\牛马\\', '')
                    ws = rel.split(os.sep)[0] if os.sep in rel else 'root'
                    all_sops.append({'path': fp, 'name': f, 'size': size, 'workspace': ws})
                except Exception as e:
                    all_sops.append({'path': fp, 'name': f, 'error': str(e)})

workspaces = {}
for sop in all_sops:
    ws = sop.get('workspace', 'unknown')
    if ws not in workspaces:
        workspaces[ws] = []
    workspaces[ws].append(sop)

out = {'total': len(all_sops), 'workspaces': {k: len(v) for k, v in sorted(workspaces.items())}, 'all': all_sops}
outpath = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\sop-eco-map.json'
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f'Total SOP files: {len(all_sops)}')
for ws, sops in sorted(workspaces.items()):
    total_size = sum(s['size'] for s in sops if 'size' in s)
    print(f'  {ws}: {len(sops)} SOPs, {total_size} bytes')
