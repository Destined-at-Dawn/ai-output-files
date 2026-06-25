import json, os

patterns = {
    "version": "1.0",
    "description": "意图模式库：用户意图 -> SOP -> Skill 调用链。替代纯关键词路由。",
    "updated": "2026-06-10",
    "intent_patterns": [
        {
            "id": "INT-001",
            "pattern": ["帮我读", "帮我看看", "分析这篇文章", "这个链接", "公众号", "URL", "网页"],
            "intent": "content_extract_and_analyze",
            "sop": "sop-content-analysis.md",
            "skill_chain": ["baoyu-url-to-markdown", "li-analyze", "li-memory", "li-improve"],
            "cognitive_books": ["009-学习之道 §概念5", "003-如何阅读一本书 §概念3"],
            "auto": True
        },
        {
            "id": "INT-002",
            "pattern": ["帮我写", "写一篇", "写公众号", "写小红书", "创作", "写文章"],
            "intent": "content_creation",
            "sop": "sop-content-creation.md",
            "skill_chain": ["li-analyze", "li-transcript", "li-mindcoach", "li-improve"],
            "cognitive_books": ["019-影响力 §概念4", "022-自控力 §概念3"],
            "auto": True
        },
        {
            "id": "INT-003",
            "pattern": ["创建skill", "做新技能", "融合技能", "改进技能", "优化skill"],
            "intent": "skill_lifecycle",
            "sop": "sop-skill-lifecycle.md",
            "skill_chain": ["li-bestskill", "li-skillcreate", "li-skillfusion", "li-manage"],
            "cognitive_books": ["005-系统之美 §概念1", "016-刻意练习 §概念4"],
            "auto": True
        },
        {
            "id": "INT-004",
            "pattern": ["FPGA", "Verilog", "Vivado", "硬件", "Arduino", "舵机", "STM32", "嵌入式"],
            "intent": "hardware_development",
            "sop": "sop-hardware-delivery.md",
            "skill_chain": ["li-hardware", "li-debug", "li-sync"],
            "cognitive_books": ["007-反脆弱 §概念2", "004-黑天鹅 §概念3"],
            "auto": True
        },
        {
            "id": "INT-005",
            "pattern": ["调研", "研究", "搜索", "找资料", "有没有", "搜一下"],
            "intent": "deep_research",
            "sop": "sop-research.md",
            "skill_chain": ["li-research", "li-devil", "li-bestskill"],
            "cognitive_books": ["003-如何阅读一本书 §概念3", "024-学会提问 §概念1"],
            "auto": True
        },
        {
            "id": "INT-006",
            "pattern": ["分析PPT", "做幻灯片", "演示文稿", "ppt", "PPT"],
            "intent": "presentation_creation",
            "sop": "sop-content-creation.md",
            "skill_chain": ["li-pptx", "li-analyze", "li-visual"],
            "cognitive_books": ["019-影响力 §概念4"],
            "auto": True
        },
        {
            "id": "INT-007",
            "pattern": ["小红书", "红书帖子", "投流", "涨粉", "爆款"],
            "intent": "xhs_content",
            "sop": "sop-content-creation.md",
            "skill_chain": ["li-xhs", "li-analyze", "li-mindcoach"],
            "cognitive_books": ["019-影响力 §概念4", "022-自控力 §概念3"],
            "auto": True
        },
        {
            "id": "INT-008",
            "pattern": ["图片", "画", "生成图片", "视觉", "设计", "海报"],
            "intent": "image_generation",
            "sop": "sop-content-creation.md",
            "skill_chain": ["li-image", "li-visual", "li-design"],
            "cognitive_books": ["019-影响力 §概念4"],
            "auto": True
        },
        {
            "id": "INT-009",
            "pattern": ["考研", "学习", "复习", "做题", "考试", "费曼"],
            "intent": "study_and_exam",
            "sop": "sop-study.md",
            "skill_chain": ["li-study", "li-analyze", "li-memory"],
            "cognitive_books": ["009-学习之道 §概念5", "016-刻意练习 §概念4", "001-认知天性 §概念1"],
            "auto": True
        },
        {
            "id": "INT-010",
            "pattern": ["简历", "求职", "面试", "实习", "找工作"],
            "intent": "job_search",
            "sop": "sop-content-creation.md",
            "skill_chain": ["li-analyze", "li-memory", "li-improve"],
            "cognitive_books": ["019-影响力 §概念4", "022-自控力 §概念3"],
            "auto": True
        },
        {
            "id": "INT-011",
            "pattern": ["同步", "跨工作区", "更新路由", "同步规则"],
            "intent": "cross_workspace_sync",
            "sop": "sop-skill-lifecycle.md",
            "skill_chain": ["li-sync", "li-infra", "li-manage"],
            "cognitive_books": ["005-系统之美 §概念1"],
            "auto": True
        },
        {
            "id": "INT-012",
            "pattern": ["这个方案好不好", "泼冷水", "质疑", "风险", "预验尸", "值不值得"],
            "intent": "decision_challenge",
            "sop": "sop-research.md",
            "skill_chain": ["li-devil", "li-research", "li-analyze"],
            "cognitive_books": ["010-思考快与慢 §概念4", "004-黑天鹅 §概念3", "007-反脆弱 §概念2"],
            "auto": True
        },
        {
            "id": "INT-013",
            "pattern": ["项目乱了", "整理项目", "重构", "清理", "迁移项目"],
            "intent": "workspace_management",
            "sop": "sop-skill-lifecycle.md",
            "skill_chain": ["li-workspace", "li-infra", "li-manage"],
            "cognitive_books": ["005-系统之美 §概念1", "028-精要主义 §概念3"],
            "auto": True
        },
        {
            "id": "INT-014",
            "pattern": ["bug", "报错", "不工作", "调试", "fix", "修复"],
            "intent": "debugging",
            "sop": "sop-hardware-delivery.md",
            "skill_chain": ["li-debug", "li-hardware", "li-diagnose"],
            "cognitive_books": ["007-反脆弱 §概念2", "005-系统之美 §概念1"],
            "auto": True
        },
        {
            "id": "INT-015",
            "pattern": ["视频", "视频号", "抖音", "剪辑", "分镜"],
            "intent": "video_content",
            "sop": "sop-content-creation.md",
            "skill_chain": ["li-video", "li-analyze", "li-visual"],
            "cognitive_books": ["019-影响力 §概念4"],
            "auto": True
        },
        {
            "id": "INT-016",
            "pattern": ["翻译", "中译英", "英译中", "translate"],
            "intent": "translation",
            "sop": "sop-content-analysis.md",
            "skill_chain": ["li-analyze", "li-memory"],
            "cognitive_books": ["003-如何阅读一本书 §概念3"],
            "auto": True
        },
        {
            "id": "INT-017",
            "pattern": ["帮我做PPT", "做个演示", "slides", "汇报PPT"],
            "intent": "pptx_creation",
            "sop": "sop-content-creation.md",
            "skill_chain": ["li-pptx", "li-analyze", "li-visual"],
            "cognitive_books": ["019-影响力 §概念4"],
            "auto": True
        },
        {
            "id": "INT-018",
            "pattern": ["情绪", "焦虑", "压力", "想放弃", "卡住了", "没动力", "迷茫"],
            "intent": "mindset_coaching",
            "sop": "sop-research.md",
            "skill_chain": ["li-mindcoach", "li-analyze", "li-memory"],
            "cognitive_books": ["022-自控力 §概念3", "007-反脆弱 §概念2", "023-认知觉醒 §概念2"],
            "auto": True
        }
    ],
    "meta": {
        "total_patterns": 18,
        "auto_patterns": 18,
        "skill_chains": 12,
        "cognitive_coverage": "62 books, 45 references",
        "sop_sources": "创作区(23) + 求职区(7) + 个人区(4) + 学习区(3) + 竞赛区(4) + mutual(15)",
        "design_principle": "用户说什么不重要，重要的是他想做什么。意图理解 > 关键词匹配。"
    }
}

# Write to mutual root
path1 = r"E:\ai产出文件\牛马\mutual\mutual\intent-patterns.json"
with open(path1, "w", encoding="utf-8") as f:
    json.dump(patterns, f, ensure_ascii=False, indent=2)

# Write to ~/.newmax/
path2 = r"C:\Users\13975\.newmax\intent-patterns.json"
os.makedirs(os.path.dirname(path2), exist_ok=True)
with open(path2, "w", encoding="utf-8") as f:
    json.dump(patterns, f, ensure_ascii=False, indent=2)

print(f"Created: {path1}")
print(f"Created: {path2}")
print(f"Patterns: {len(patterns['intent_patterns'])}")
print(f"All auto: {all(p['auto'] for p in patterns['intent_patterns'])}")
