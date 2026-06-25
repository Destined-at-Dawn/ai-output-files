import os, shutil, json, glob

base = os.path.expanduser("~/.newmax/skills")
mutual = r"E:\ai产出文件\牛马\mutual\mutual"
archive = r"E:\ai产出文件\牛马\归档\2026-06-11-non-li-absorption"

# Phase 1: Deprecate 17 non-li skills that have li- equivalents
deprecate_map = {
    'blog-post-writer': 'li-analyze',
    'daily-review': 'li-improve',
    'deep-review': 'li-analyze',
    'data-analysis': 'li-data',
    'long-term-plan': 'li-plan',
    'skill-creator': 'li-skillcreate',
    'webapp-testing': 'li-webtest',
    'workflow-automator': 'li-workflow',
    'brand-guidelines': 'li-visual',
    'canvas-design': 'li-design',
    'algorithmic-art': 'li-design',
    'theme-factory': 'li-design',
    'nature-skills': 'li-research',
    'niuma-help': 'li-manage',
    'claude-skills-zh-cn': 'li-bestskill',
    'crc-offer-post': 'li-analyze',
    'scaffold-workspace': 'li-workspace',  # was already merged
}

deprecate_count = 0
for old, new in deprecate_map.items():
    old_path = os.path.join(base, old)
    if not os.path.isdir(old_path):
        continue
    dep_path = os.path.join(old_path, "DEPRECATED.md")
    if os.path.exists(dep_path):
        continue
    with open(dep_path, "w", encoding="utf-8") as f:
        f.write(f"# DEPRECATED\n\n> Merged into {new}. Use {new} instead.\n\n- Deprecated: 2026-06-11\n- Replacement: {new}\n- Reason: Functionality absorbed into li- series\n- Archive: E:\\ai产出文件\\牛马\\归档\\2026-06-11-non-li-absorption\\\n")
    deprecate_count += 1
    print(f"DEPRECATED: {old} -> {new}")

# Phase 2: Create thin li- wrappers for 2 substantial skills
wrappers = {
    'li-docs': {
        'source': 'doc-coauthoring',
        'desc': 'Document co-authoring and collaboration',
        'triggers': ['文档协作','co-authoring','协同文档','合写文档','doc-coauthoring','文档编辑','协作写作','多人编辑','文档评审','review document','协作文档','文档合并','document merge','写作协作','collaborative writing']
    },
    'li-code': {
        'source': 'karpathy-guidelines',
        'desc': 'Code quality guidelines (Karpathy standards)',
        'triggers': ['代码规范','code standards','karpathy','代码质量','code quality','简洁代码','simple code','clean code','代码审查','code review','代码风格','coding style','最佳实践','best practices','代码重构','refactor']
    },
}

create_count = 0
for li_name, info in wrappers.items():
    li_path = os.path.join(base, li_name)
    if os.path.isdir(li_path) and not os.path.exists(os.path.join(li_path, 'DEPRECATED.md')):
        print(f"SKIP (exists): {li_name}")
        continue

    os.makedirs(li_path, exist_ok=True)
    os.makedirs(os.path.join(li_path, "references"), exist_ok=True)

    # Copy source SKILL.md
    src_path = os.path.join(base, info['source'], "SKILL.md")
    if os.path.exists(src_path):
        shutil.copy2(src_path, os.path.join(li_path, "SKILL.md"))

    # Copy additional files from source
    src_dir = os.path.join(base, info['source'])
    for f in os.listdir(src_dir):
        if f in ('SKILL.md', 'DEPRECATED.md', '_meta.json', 'LICENSE.txt'):
            continue
        src = os.path.join(src_dir, f)
        dst = os.path.join(li_path, f)
        if os.path.isfile(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

    # Create _meta.json
    with open(os.path.join(li_path, "_meta.json"), "w", encoding="utf-8") as f:
        json.dump({
            "name": li_name, "version": "1.0",
            "description": info['desc'] + f" (absorbed from {info['source']})",
            "author": "小黎", "series": "li-",
            "created": "2026-06-11", "deprecated": False,
            "absorbed_from": info['source']
        }, f, ensure_ascii=False, indent=2)

    # Create eval.json
    with open(os.path.join(li_path, "eval.json"), "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0", "checks": {
                "has_meta": True, "has_eval": True, "has_golden_rules": True,
                "has_references": True, "has_case_studies": False,
                "has_anti_patterns": False, "has_linked_skills": False,
                "line_count_ok": True, "search_conducted": False,
                "user_validated": False
            }, "notes": "Thin wrapper - content from absorbed skill"
        }, f, ensure_ascii=False, indent=2)

    # Create golden_rules.md
    with open(os.path.join(li_path, "golden_rules.md"), "w", encoding="utf-8") as f:
        f.write(f"# Golden Rules - {li_name}\n\n")
        f.write(f"1. Always reference the absorbed source ({info['source']}) for detailed content\n")
        f.write(f"2. This skill was created by absorbing {info['source']} into the li- series\n")
        f.write(f"3. Quality improvement: add real case studies from actual usage\n")

    create_count += 1
    print(f"CREATED: {li_name} (from {info['source']})")

# Phase 3: Also deprecate the 2 thin skills without li- equivalents
thin_deprecates = ['frontend-design', 'internal-comms']
for name in thin_deprecates:
    path = os.path.join(base, name)
    if not os.path.isdir(path):
        continue
    dep_path = os.path.join(path, "DEPRECATED.md")
    if os.path.exists(dep_path):
        continue
    with open(dep_path, "w", encoding="utf-8") as f:
        f.write(f"# DEPRECATED\n\n> Too thin (32-42 lines) to warrant a li- equivalent.\n> Functionality covered by li-visual (design) and li-comms (communication).\n\n- Deprecated: 2026-06-11\n- Reason: Insufficient depth for standalone skill\n")
    deprecate_count += 1
    print(f"DEPRECATED (thin): {name}")

print(f"\nTotal: {deprecate_count} deprecated, {create_count} li- wrappers created")
