import json
import os

routing_table_path = r'E:\ai产出文件\牛马\mutual\mutual\skill-routing-table.json'
skills_root = r'E:\ai产出文件\牛马\mutual\mutual\skills'

with open(routing_table_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

unique_skills = set()
for route in data.get('routes', []):
    if 'skill' in route and route['skill']:
        unique_skills.add(route['skill'])

skills_info = []
for skill_name in sorted(list(unique_skills)):
    skill_dir = os.path.join(skills_root, skill_name)
    if os.path.isdir(skill_dir):
        skills_info.append({"name": skill_name, "path": skill_dir, "exists": True})
    else:
        skills_info.append({"name": skill_name, "path": skill_dir, "exists": False})

print(json.dumps(skills_info, ensure_ascii=False, indent=2))
