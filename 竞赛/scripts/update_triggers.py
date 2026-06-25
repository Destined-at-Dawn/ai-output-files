"""
update_triggers.py — 批量更新 li- 系列 skill 的触发词
根因：触发词是"技术术语"，用户说的是"人话"，中间有语义鸿沟

原则：
1. 加自然语言同义词（"分开" = "拆分"）
2. 加用户真实表达（"有没有自进化" = "自进化功能"）
3. 不删除已有触发词（向后兼容）
4. 不创建冲突（检查是否有重复）
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROUTING_FILE = Path("${WORKSPACE_ROOT}/skill-routing-table.json")

# 每个 skill 要新增的自然语言触发词
# 只列新增的，不列已有的
NEW_TRIGGERS = {
    "li-skillfusion": [
        # 核心动作词（用户说人话版本）
        "分开", "分离", "拆开来", "拆出去", "拆成",
        "合并到一起", "融到一起", "合到一块",
        "帮我拆", "帮我分", "帮我合", "帮我融",
        "拆分skill", "融合skill", "分开skill", "合并skill",
        "skill拆分", "skill融合", "skill分开", "skill合并",
        "skill太长", "skill太大", "skill太杂",
        "拆成两个", "合到一个", "分成两个",
    ],
    "li-improve": [
        # 自进化功能的自然表达
        "自进化功能", "自进化机制", "有没有自进化",
        "为什么没有自进化", "自进化在哪",
        "进化功能", "进化机制",
        "学习功能", "学习机制",
        "教训只记不改", "教训不回写", "教训回写",
        "有壳没有引擎", "有壳无引擎",
        "形同虚设", "没有用", "没生效",
        "改进一下", "改进功能", "改进机制",
        "怎么改进", "如何改进", "改进方案",
        "经验沉淀", "教训沉淀", "沉淀机制",
        "怎么学习", "怎么进化", "怎么改进",
    ],
    "li-skills-mgmt": [
        "管理skill", "管理技能",
        "有哪些skill", "有什么skill", "skill列表", "技能列表",
        "哪个skill", "什么skill", "用哪个skill",
        "skill多了", "skill乱了", "skill管理",
        "删skill", "删除skill", "废弃skill",
        "清理skill", "整理skill", "清理技能",
        "审核一下", "审查skill", "检查skill",
    ],
    "li-diagnose": [
        # "检查"是用户最高频的诊断表达
        "帮我检查", "帮我诊断", "帮我看看",
        "查一下", "看一下", "看看哪里有问题",
        "哪里有问题", "有什么问题", "出了什么问题",
        "排查一下", "排查问题", "排查错误",
        "不正常", "不太对", "感觉有问题",
        "异常检测", "问题诊断",
    ],
    "li-competition": [
        "竞赛的skill", "竞赛skill",
        "竞赛分开", "竞赛拆分",
        "竞赛工作区", "竞赛项目",
        "竞赛流程", "竞赛管理",
        "比赛skill", "比赛管理",
    ],
    "li-infra": [
        # 用户说"写入规则"时指的是修改 CLAUDE.md/rules
        "写入规则", "写到规则", "写规则",
        "写入CLAUDE", "写到CLAUDE", "改CLAUDE",
        "写到rule", "写入rule", "改rule",
        "修改配置", "更新配置", "改配置",
        "全局配置", "系统配置",
        "基础设施", "底座",
    ],
    "li-analyze": [
        "帮我分析", "帮我看看这个",
        "分析一下", "分析问题", "分析原因",
        "深度分析", "详细分析",
        "查原因", "找原因", "为什么",
        "对比一下", "比较一下",
        "评估一下", "评价一下",
    ],
    "li-research": [
        "帮我查一下", "帮我搜一下", "帮我找一下",
        "调研一下", "调查一下",
        "了解一下", "研究一下",
        "是什么", "什么是", "怎么回事",
        "背景信息", "背景知识",
        "最新进展", "最新消息", "最新资讯",
        "有没有相关的", "有没有现成的",
    ],
    "li-soul": [
        "人格设定", "人设",
        "你是谁", "你的身份", "你的角色",
        "身份设定", "角色设定",
        "调整语气", "调整风格", "换个风格",
        "说话方式", "沟通风格",
    ],
    "li-longmemory": [
        "写入long-term", "写入长期记忆",
        "记录一下", "记住这个",
        "归档记忆", "整理记忆",
        "记忆归档", "长期记忆",
    ],
    "li-sync": [
        "同步一下", "同步规则", "同步配置",
        "同步到其他", "同步过去",
        "统一一下", "统一规则",
        "复制到其他", "搬到其他工作区",
    ],
    "li-assess": [
        "评估一下", "考核一下",
        "打分", "评分", "评分一下",
        "怎么样", "好不好", "行不行",
        "达标了吗", "合格吗", "及格吗",
        "决策打分", "评估方案",
    ],
    "li-study": [
        "教我", "给我讲讲", "帮我理解",
        "这个怎么理解", "这是什么意思",
        "怎么用", "怎么操作", "怎么弄",
        "学习一下", "学一下",
        "一步步来", "手把手", "教程",
    ],
    "li-proto": [
        "需求分析", "分析需求",
        "原型设计", "设计方案",
        "怎么做这个", "怎么实现",
        "方案设计", "方案对比",
        "帮我设计", "帮我规划",
    ],
    "li-inspect": [
        "审查代码", "检查代码", "看代码",
        "帮我review", "代码审查",
        "代码检查", "代码质量",
        "找bug", "找问题",
    ],
    "li-merge": [
        "合并文件", "合并文档", "合并报告",
        "汇总一下", "整合一下",
        "合成一个", "并到一起",
        "整理到一个文件",
    ],
    "li-search": [
        "搜索优化", "搜索改进",
        "搜索配置", "搜索设置",
        "搜索质量", "搜索效果",
    ],
    "li-max": [
        "升级系统", "更新系统",
        "升级牛马", "更新牛马",
        "版本升级", "系统升级",
    ],
    "li-epub": [
        "写书", "出书", "写电子书",
        "写一本", "写个电子书",
        "生成epub", "生成电子书",
    ],
}

# li-skillfusion 的完整路由条目（因为它是新增的）
SKILLFUSION_ROUTE = {
    "name": "li-skillfusion",
    "version": "2.0",
    "auto": True,
    "enabled": True,
    "priority": 3,
    "triggers": [
        "拆分", "融合", "合并", "微技能",
        "技能拆分", "技能融合", "技能合并",
        "skill拆分", "skill融合", "skill合并",
        "SKILL拆分", "SKILL融合", "拆分SKILL",
        "拆分到references", "融合skill", "合并skill",
        "拆成", "融到", "合到",
        # 自然语言（NEW）
        "分开", "分离", "拆开来", "拆出去",
        "合并到一起", "融到一起", "合到一块",
        "帮我拆", "帮我分", "帮我合", "帮我融",
        "skill太长", "skill太大", "skill太杂",
        "拆成两个", "合到一个", "分成两个",
    ],
    "action": "mcp__skill-handler__Skill",
    "args": {"skill": "li-skillfusion"},
    "description": "技能拆分、融合、微技能创建，统一管理 skill 结构变更",
}


def main():
    with open(ROUTING_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    routes = data.get("routes", data) if isinstance(data, dict) else data

    # Build name->index map
    name_map = {}
    for i, r in enumerate(routes):
        name = r.get("name", r.get("skill", ""))
        name_map[name] = i

    changes = []

    # 1. Add li-skillfusion if missing
    if "li-skillfusion" not in name_map:
        routes.append(SKILLFUSION_ROUTE)
        changes.append(f"+ li-skillfusion: 新增路由条目 ({len(SKILLFUSION_ROUTE['triggers'])} triggers)")
    else:
        # Update existing triggers
        idx = name_map["li-skillfusion"]
        existing = set(routes[idx].get("triggers", []))
        new_triggers = NEW_TRIGGERS.get("li-skillfusion", [])
        added = [t for t in new_triggers if t not in existing]
        if added:
            routes[idx].setdefault("triggers", []).extend(added)
            changes.append(f"+ li-skillfusion: 追加 {len(added)} 个自然语言触发词")

    # 2. Update other li- skills
    for skill_name, new_triggers in NEW_TRIGGERS.items():
        if skill_name == "li-skillfusion":
            continue  # Already handled above

        if skill_name not in name_map:
            changes.append(f"? {skill_name}: 不在路由表中，跳过")
            continue

        idx = name_map[skill_name]
        existing = set(routes[idx].get("triggers", []))
        added = [t for t in new_triggers if t not in existing]

        if added:
            routes[idx].setdefault("triggers", []).extend(added)
            changes.append(f"+ {skill_name}: 追加 {len(added)} 个触发词")
        else:
            changes.append(f"= {skill_name}: 无新增（所有触发词已存在）")

    # 3. Update metadata
    if isinstance(data, dict) and "metadata" in data:
        data["metadata"]["total_routes"] = len(routes)
        data["metadata"]["last_updated"] = "2026-06-13"

    # Write back
    with open(ROUTING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Print report
    print("=" * 60)
    print("触发词更新报告")
    print("=" * 60)
    for c in changes:
        print(f"  {c}")
    print(f"\n总路由数: {len(routes)}")
    print("Done.")


if __name__ == "__main__":
    main()
