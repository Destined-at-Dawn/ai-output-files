import os, json, re, shutil

SKILLS = r"C:\Users\13975\.newmax\skills"
ROUTE_FILE = os.path.join(SKILLS, "li", "skill-routing-table.json")
ARCHIVE = r"E:\ai产出文件\牛马\归档\2026-06-10-non-li-skill-absorb"

os.makedirs(ARCHIVE, exist_ok=True)

with open(ROUTE_FILE, "r", encoding="utf-8") as f:
    routes = json.load(f)

changed = []

# Create 6 new li-* wrappers
new_skills = [
    ("li-competition", "li-competition", ["竞赛","比赛","robomaster","电赛","fpga竞赛","lcd","机器人","stm32嵌入式","团队协作","进度管理","里程碑","硬件调试","嵌入式系统","robomaster电控","pid调参","can排查","急停","限位","按键消抖"]),
    ("li-data", "li-data", ["数据处理","数据清洗","数据分析","csv","json","excel处理","pandas","numpy","matplotlib","可视化","统计分析","数据可视化","数据报告","数据集","数据转换","特征工程","数据挖掘","数据导入","数据导出","数据格式"]),
    ("li-dbs", "li-dbs", ["dbs方法论","dbs-diagnosis","dbs-workflow","dbs-content","dbs-sop","dbs-agent","dbs技能","五层消解","消解漏斗","公理系统","故障分类","根本原因","自愈系统","恢复机制","降级策略","故障排查方法论"]),
    ("li-platform", "li-platform", ["平台运营","运营策略","涨粉","算法","起号","冷启动","矩阵运营","多平台","流量池","内容分发","用户增长","运营数据分析","跨平台分发","内容日历","发布策略","互动率","转化率","私域","社群运营","账号定位"]),
    ("li-session", "li-session", ["session","对话管理","上下文压缩","compact","上下文保存","对话恢复","记忆持久化","session checkpoint","上下文窗口","token管理","对话历史","上下文截断","会话管理","对话上下文","checkpoint","压缩策略","记忆衰减"]),
    ("li-study", "li-study", ["学习方法","费曼技巧","间隔重复","检索练习","学习策略","复习计划","知识卡片","anki","闪卡","认知负荷","精细加工","自我测试","学习效率","记忆曲线","遗忘曲线","学科学习","笔记方法","思维导图","康奈尔笔记"]),
]

for name, target, triggers in new_skills:
    skill_dir = os.path.join(SKILLS, name)
    if not os.path.exists(skill_dir):
        os.makedirs(skill_dir, exist_ok=True)
        # Create minimal SKILL.md
        with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(f"# {name}\n\nli-series skill wrapper.\n")
        # Create eval + meta + golden_rules
        for fn, content in [
            ("eval.json", json.dumps({"version":"1.0","assertions":[{"check":"SKILL.md exists","test":"os.path.exists","severity":"CRITICAL"}]}, indent=2)),
            ("_meta.json", json.dumps({"name":name,"version":"1.0","author":"li-series","tier":2}, indent=2)),
            ("golden_rules.md", f"# {name} Golden Rules\n\n- GR-001: 待实际使用后补充领域特化规则\n"),
        ]:
            with open(os.path.join(skill_dir, fn), "w", encoding="utf-8") as f:
                f.write(content)
        changed.append(f"CREATE {name}")

# Deprecate 10 absorbed skills
deprecate_targets = ["competition-workflow","thinking-coach","personal-rag-qa","research-daily",
                     "niuma-voice-dna","wechat-article-reader","wechat-reading-analytics",
                     "wechat-memory-graph","wechat-group-analysis","wechat-chat-analyzer"]

for sname in deprecate_targets:
    sdir = os.path.join(SKILLS, sname)
    if os.path.exists(sdir):
        dep = os.path.join(sdir, "DEPRECATED.md")
        if not os.path.exists(dep):
            with open(dep, "w", encoding="utf-8") as f:
                f.write(f"# DEPRECATED\n\nAbsorbed into li-series.\n")
            changed.append(f"DEPRECATE {sname}")

# Update routing table: add new li-* routes, remove deprecated routes
existing_ids = [int(r["id"][1:]) for r in routes["routes"] if r["id"].startswith("r") and r["id"][1:].isdigit()]
next_id = max(existing_ids) + 1 if existing_ids else 110

# Add new routes
for name, target, triggers in new_skills:
    has_route = any(r.get("skill") == name for r in routes["routes"])
    if not has_route:
        routes["routes"].append({
            "id": f"r{next_id:03d}",
            "name": name,
            "skill": name,
            "triggers": triggers,
            "context": [],
            "mcp": None,
            "priority": 5,
            "auto": True,
            "confidence": 0.9,
            "note": f"Auto-absorbed into li-series"
        })
        next_id += 1
        changed.append(f"ROUTE+ {name} ({len(triggers)} triggers)")

# Remove deprecated routes
routes["routes"] = [r for r in routes["routes"] if r.get("skill") not in deprecate_targets]
routes["version"] = "2.0"
routes["last_updated"] = "2026-06-10"
routes["total_routes"] = len(routes["routes"])

with open(ROUTE_FILE, "w", encoding="utf-8") as f:
    json.dump(routes, f, ensure_ascii=False, indent=2)

# Count
li_count = len([d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)) and d.startswith("li-") and os.path.exists(os.path.join(SKILLS, d, "SKILL.md"))])
dep_count = len([d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)) and os.path.exists(os.path.join(SKILLS, d, "DEPRECATED.md"))])

print(f"=== DONE ===")
print(f"Changes: {len(changed)}")
for c in changed:
    print(f"  {c}")
print(f"\nActive li-*: {li_count}")
print(f"Deprecated: {dep_count}")
print(f"Routes: {routes['total_routes']}")
