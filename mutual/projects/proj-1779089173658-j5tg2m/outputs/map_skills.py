import os
import json

skills_root = r'E:\ai产出文件\牛马\mutual\mutual\skills'
routing_table_path = r'E:\ai产出文件\牛马\mutual\mutual\skill-routing-table.json'

# 1. 获取目录名
dir_skills = [d for d in os.listdir(skills_root) if os.path.isdir(os.path.join(skills_root, d))]

# 2. 获取路由表中的技能
with open(routing_table_path, 'r', encoding='utf-8') as f:
    routing_data = json.load(f)

routing_skills = set()
for route in routing_data.get('routes', []):
    if 'skill' in route and route['skill']:
        routing_skills.add(route['skill'])

# 3. 交叉验证
results = {
    "only_in_dirs": sorted(list(set(dir_skills) - routing_skills)),
    "only_in_routing": sorted(list(routing_skills - set(dir_skills))),
    "both": sorted(list(set(dir_skills) & routing_skills))
}

print(json.dumps(results, ensure_ascii=False, indent=2))
