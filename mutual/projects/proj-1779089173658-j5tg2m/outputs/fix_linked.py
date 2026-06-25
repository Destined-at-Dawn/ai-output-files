# -*- coding: utf-8 -*-
"""Inject linked skills tables for 5 WARN skills"""

import re

INJECTIONS = {
    'li-industry': {
        # 299L, only 1L budget → need to compress first
        # Strategy: Find the longest paragraph and compress it, then inject
        'linked': """
| li- | 联动方式 | 触发时机 |
|-----|---------|---------|
| li-research | 深度调研补充行业数据 | 行业趋势需定量数据 |
| li-analyze | 道法术器穿透分析 | 行业报告需深度解读 |
| li-diagnose | 诊断行业竞争格局 | 市场进入决策 |
| li-memory | 沉淀行业知识图谱 | 持续追踪行业变化 |
""",
    },
    'li-transcript': {
        'linked': """
| li- | 联动方式 | 触发时机 |
|-----|---------|---------|
| li-analyze | 道法术器四层拆解 | 清洗后需深度分析 |
| li-memory | 沉淀关键事实和术语 | 对话中有新知识 |
| li-improve | 自进化引擎 | 用户对输出评价 |
| li-content | 内容质量评估 | 需评估清洗质量 |
""",
    },
    'li-workflow': {
        'linked': """
| li- | 联动方式 | 触发时机 |
|-----|---------|---------|
| li-infra | 基础设施管理 | 需更新 CLAUDE.md 或 SOP |
| li-manage | 生命周期管理 | 工作流变更需同步 skill |
| li-sync | 跨区同步 | 工作流涉及多工作区 |
| li-debug | 调试工作流脚本 | 自动化脚本出错 |
""",
    },
    'li-voice': {
        'linked': """
| li- | 联动方式 | 触发时机 |
|-----|---------|---------|
| li-transcript | 逐字稿清洗 | 语音转文本后需清洗 |
| li-analyze | 道法术器分析 | 语音内容需深度解读 |
| li-writing | 文风适配 | 语音转文字需风格调整 |
| li-memory | 事实提取沉淀 | 对话中有决策或偏好 |
""",
    },
    'li-skills-mgmt': {
        'linked': """
| li- | 联动方式 | 触发时机 |
|-----|---------|---------|
| li-manage | 全生命周期编排 | skill 状态变更 |
| li-skillcreate | 创建新 skill | 发现能力缺口 |
| li-skillfusion | 融合/拆分 skill | 功能重叠或过度膨胀 |
| li-bestskill | 跨平台搜索 | 造 skill 前先搜外部 |
""",
    },
}

def inject_linked_table(skill_name, table_content):
    path = f'${NEWMAX_HOME}/skills/{skill_name}/SKILL.md'
    with open(path, encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # Strategy 1: Find existing "联动技能" or "Linked Skills" section and add table after header
    link_section_idx = None
    for i, line in enumerate(lines):
        if ('联动技能' in line or 'Linked Skills' in line) and line.strip().startswith('#'):
            link_section_idx = i
            break

    if link_section_idx is not None:
        # Find the end of this section (next ## heading or end of file)
        insert_idx = link_section_idx + 1
        for i in range(link_section_idx + 1, len(lines)):
            if lines[i].strip().startswith('## ') and i > link_section_idx:
                insert_idx = i
                break
        else:
            insert_idx = len(lines)

        # Insert table content before the section end
        table_lines = table_content.strip().split('\n')
        for j, tl in enumerate(table_lines):
            lines.insert(insert_idx + j, tl)

        new_content = '\n'.join(lines)
        new_lines = new_content.count('\n')

        if new_lines <= 300:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f'{skill_name}: injected at line {insert_idx}, {new_lines} lines OK'
        else:
            # Over 300 → need to compress something first
            # For li-industry (299L + ~6 table lines = ~305), remove a verbose paragraph
            return f'{skill_name}: {new_lines} lines OVER LIMIT, needs compression first'

    return f'{skill_name}: no linked skills section found'

results = []
for skill_name, data in INJECTIONS.items():
    r = inject_linked_table(skill_name, data['linked'])
    results.append(r)
    print(r)
