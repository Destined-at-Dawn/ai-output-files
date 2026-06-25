#!/usr/bin/env python3
"""Batch register all zero-route skills + upgrade li-skill quality."""
import os, json, re, shutil

SKILLS_DIR = r"C:\Users\13975\.newmax\skills"
RT_PATH = os.path.join(SKILLS_DIR, "skill-routing-table.json")

# Load routing table
with open(RT_PATH, encoding="utf-8", errors="replace") as f:
    data = json.load(f)

# Existing IDs
existing_ids = set()
for r in data["routes"]:
    rid = r.get("id", "")
    if rid.startswith("r"):
        try:
            existing_ids.add(int(rid[1:]))
        except ValueError:
            pass

next_id = max(existing_ids) + 1 if existing_ids else 120

def gen_id():
    global next_id
    rid = f"r{next_id:03d}"
    next_id += 1
    return rid

# === Cluster definitions: skill_name -> triggers ===
clusters = {
    "li-writing": {
        "baoyu-post-to-wechat": ["发布微信", "发布公众号", "post wechat", "微信发布", "公众号发布", "推送文章"],
        "baoyu-post-to-x": ["发布推特", "post to x", "发推", "twitter发布", "x平台发布"],
        "khazix-writer": ["凯瑞克斯写作", "爆款文案", "viral writing", "裂变写作"],
        "magazine-cover": ["杂志封面", "magazine cover", "封面设计", "封面制作"],
        "koubo-script-writer": ["口播脚本", "口播文案", "直播脚本", "短视频文案"],
        "x-article-publisher": ["发布X文章", "x平台文章", "发推文"],
        "jincheng-pyq": ["朋友圈", "朋友圈文案", "朋友圈图片", "pyq"],
        "copywriting-skills": ["广告文案", "copywriting", "文案写作"],
    },
    "li-image": {
        "baoyu-image-gen": ["生成图片", "AI绘图", "AI作画", "文生图", "image generation"],
        "baoyu-compress-image": ["压缩图片", "图片压缩", "compress image"],
        "baoyu-article-illustrator": ["文章配图", "插图生成", "illustration"],
        "baoyu-cover-image": ["封面图", "cover image", "头图生成"],
        "baoyu-infographic": ["信息图", "infographic", "数据可视化"],
        "baoyu-comic": ["漫画", "漫画生成", "comic", "条漫"],
        "baoyu-xhs-images": ["小红书图片", "xhs images", "笔记配图"],
        "gemini-image": ["gemini图片", "gemini生成图片"],
        "imagemagick-conversion": ["图片格式转换", "格式转换", "webp转png"],
        "design-extract": ["设计提取", "提取配色", "提取设计元素"],
        "image-to-code-skill": ["图片转代码", "截图转代码", "image to code"],
        "imagegen-frontend-mobile": ["移动端UI生成", "手机界面设计"],
        "imagegen-frontend-web": ["网页UI生成", "网页设计图"],
        "algorithmic-art": ["算法艺术", "生成艺术", "generative art"],
        "canvas-design": ["画布设计", "canvas设计"],
        "zerox": ["OCR识别", "图片文字识别"],
        "image-editing": ["图片编辑", "修图", "P图"],
    },
    "li-slide": {
        "baoyu-slide-deck": ["生成幻灯片", "slide deck", "演示文稿"],
        "NanoBanana-PPT-Skills": ["PPT生成", "PPT制作", "幻灯片设计"],
        "ppt-generator-pro": ["PPT高级生成", "pro幻灯片", "专业PPT"],
        "pptx": ["读取PPT", "解析pptx", "PPT解析"],
        "guizang-ppt-skill": ["桂藏PPT", "PPT风格"],
        "dg-gray-slide-designer": ["灰度幻灯片", "灰色PPT设计"],
        "dg-planner": ["演示规划", "slide planner"],
        "dg-slide-dev": ["幻灯片开发", "slide开发"],
        "dg-slide-tester-animation": ["PPT动画测试", "幻灯片动画"],
        "dg-slide-tester-beauty": ["PPT美学测试", "幻灯片美观度"],
        "dg-slide-tester-layout": ["PPT布局测试", "幻灯片排版"],
        "frontend-slides": ["前端幻灯片", "网页幻灯片"],
    },
    "li-video": {
        "video-creator": ["视频创作", "视频制作", "video creation"],
        "video-optimize": ["视频优化", "video optimization"],
        "video-use": ["视频使用", "视频工具"],
        "short-video-production": ["短视频制作", "短视频", "抖音制作"],
        "remotion-video": ["remotion视频", "代码视频"],
        "ffmpeg-usage": ["ffmpeg", "视频转码", "视频剪辑"],
        "jianying-editor-skill": ["剪映", "剪映编辑", "视频剪辑"],
        "seedance-storyboard": ["分镜脚本", "storyboard", "视频分镜"],
        "slack-gif-creator": ["GIF创建", "动图制作"],
    },
    "li-translate": {
        "deepl": ["DeepL翻译", "deepl翻译", "翻译"],
        "chinese-natural-voice-revision": ["去AI味", "AI痕迹消除", "自然化改写"],
        "humanizer-zh": ["中文人味", "人类化", "去机器感"],
    },
    "research-tools": {
        "deep-research": ["深度研究", "deep research", "学术研究"],
        "deep-review": ["深度审阅", "peer review", "论文审阅"],
        "research-daily": ["每日研究", "daily research"],
        "data-analysis": ["数据分析", "data analysis", "数据处理"],
        "step-search": ["逐步搜索", "step search", "多步搜索"],
        "web-access": ["网页访问", "web access", "读取网页"],
        "lazyweb-skill": ["懒人网页", "lazyweb"],
        "baoyu-url-to-markdown": ["网页转markdown", "URL转MD", "链接转文本", "读取链接", "读取URL"],
        "baoyu-format-markdown": ["格式化markdown", "markdown格式"],
        "baoyu-markdown-to-html": ["markdown转HTML", "MD转网页"],
        "pdf": ["PDF解析", "读取PDF", "PDF转换"],
        "docx": ["读取Word", "解析docx", "Word文档"],
    },
    "wechat-ecosystem": {
        "wechat-analysis": ["微信分析", "wechat analysis"],
        "wechat-db-update": ["微信数据库", "wechat db", "聊天记录更新"],
        "wechat-distiller": ["微信提炼", "聊天提炼", "wechat distill"],
        "wechat-exporter": ["微信导出", "聊天记录导出", "wechat export"],
        "wechat-article-collector": ["微信文章采集", "公众号采集", "文章收藏"],
        "html-to-notes": ["网页转笔记", "HTML转笔记"],
    },
    "platform-publish": {
        "github-publisher": ["发布到GitHub", "github发布", "推送github"],
        "aihot": ["AI热榜", "AI热门", "aihot"],
        "opc-private-domain": ["私域运营", "OPC私域", "私域流量"],
    },
}

# === DBS series (grouped triggers) ===
dbs_skills = {
    "dbs-action": ["DBS行动", "行动框架", "action框架"],
    "dbs-ai-check": ["AI检测", "AI审查", "内容检测"],
    "dbs-benchmark": ["DBS基准", "benchmark评估"],
    "dbs-chatroom": ["DBS聊天室", "协作讨论"],
    "dbs-content": ["DBS内容", "内容创作框架"],
    "dbs-content-system": ["DBS内容系统", "内容体系"],
    "dbs-deconstruct": ["DBS解构", "解构分析"],
    "dbs-diagnosis": ["DBS诊断", "系统诊断"],
    "dbs-goal": ["DBS目标", "目标管理"],
    "dbs-hook": ["DBS钩子", "hook机制"],
    "dbs-report": ["DBS报告", "进度报告"],
    "dbs-restore": ["DBS恢复", "系统恢复"],
    "dbs-save": ["DBS保存", "知识保存"],
    "dbs-slowisfast": ["慢即是快", "slow is fast"],
    "dbs-xhs-title": ["DBS小红书标题", "xhs标题"],
    "dbs-agent-migration": ["Agent迁移", "工作台迁移"],
}

# === Vercel series ===
vercel_skills = {
    "vercel-composition-patterns": ["vercel组合模式", "composition patterns"],
    "vercel-deploy-to-vercel": ["vercel部署", "deploy vercel"],
    "vercel-react-best-practices": ["vercel React最佳实践"],
    "vercel-react-native-skills": ["vercel React Native"],
    "vercel-react-view-transitions": ["vercel视图过渡", "view transitions"],
    "vercel-vercel-cli-with-tokens": ["vercel CLI", "vercel命令行"],
    "vercel-web-design-guidelines": ["vercel网页设计规范"],
}

# === All remaining zero-route skills ===
remaining_skills = {
    "cold-water": ["泼冷水", "预验尸", "pre-mortem"],
    "devils-advocate": ["魔鬼代言人", "质疑决策"],
    "cross-workspace-sync": ["跨工作区同步", "cross-workspace"],
    "neat-freak": ["整洁检查", "文档洁癖"],
    "find-skills": ["搜索技能", "find skills", "找技能"],
    "follow-builders": ["关注建造者", "follow builders"],
    "frontend-design": ["前端设计", "frontend design"],
    "executing-plans": ["执行计划", "执行方案"],
    "long-term-plan": ["长期计划", "长期规划"],
    "longmemory": ["长期记忆", "long memory"],
    "three-tier-memory": ["三层记忆", "tiered memory"],
    "self-improving": ["自我改进", "self improving"],
    "skill-activator": ["技能激活", "skill activation"],
    "skill-creator": ["技能创建", "skill creation"],
    "skill-vetter": ["技能审查", "skill vetting"],
    "mcp-builder": ["MCP构建", "MCP开发"],
    "project-init": ["项目初始化", "project init"],
    "webapp-testing": ["Web应用测试", "webapp test"],
    "workflow-automator": ["工作流自动化", "workflow automation"],
    "soft-skill": ["软技能", "soft skill"],
    "taste-skill": ["品味技能", "审美"],
    "personal-rag-qa": ["个人RAG问答", "知识库问答"],
    "personal-info-discovery": ["个人信息发现", "个人档案"],
    "post-task-audit": ["任务后审计", "post audit"],
    "input-content-guard": ["输入内容守卫", "内容检查"],
    "niuma-help": ["牛马帮助", "niuma help", "系统帮助"],
    "niuma-voice-dna": ["牛马语音DNA", "语音风格"],
    "office-hours": ["办公时间", "office hours"],
    "brand-guidelines": ["品牌指南", "品牌规范"],
    "brandkit": ["品牌工具包", "brand kit"],
    "anything-to-notebooklm": ["转NotebookLM", "notebooklm"],
    "audit-optimizer": ["审计优化", "audit优化"],
    "cursor-acp-adapter": ["Cursor适配", "cursor adapter"],
    "claude-skills-zh-cn": ["Claude技能中文", "技能中文版"],
    "dbs-danger-gemini-web": ["DBS危险Gemini", "gemini检测"],
    "hv-analysis": ["HV分析", "高价值分析"],
    "jc-plan": ["教程计划", "jc plan"],
    "kami": ["Kami工具"],
    "minimalist-skill": ["极简技能", "minimalist"],
    "nature-skills": ["Nature技能", "自然技能"],
    "nuwa-skill": ["女娲技能", "nuwa"],
    "openclawmp": ["OpenClaw", "openclaw"],
    "output-skill": ["输出技能", "output格式"],
    "ppocrv5": ["PaddleOCR", "文字识别"],
    "qiaomu-mondo-poster-design": ["海报设计", "poster design"],
    "redesign-skill": ["重设计", "重构项目"],
    "scaffold-workspace": ["工作区脚手架", "scaffold"],
    "stitch-skill": ["Stitch技能", "缝合技能"],
    "theme-factory": ["主题工厂", "theme factory"],
    "transcript-cleaner": ["逐字稿清理", "transcript clean"],
    "web-artifacts-builder": ["Web组件构建", "artifacts builder"],
    "web-design-engineer": ["网页设计工程", "web design"],
    "xiaojiang": ["小将工具"],
    "channel-config": ["频道配置", "channel config"],
    "writing-plans": ["写作计划", "writing plan"],
}

# === Build new routes ===
new_routes = []

# Cluster groups
for cluster, skills in clusters.items():
    for skill_name, triggers in skills.items():
        if not triggers:
            continue
        new_routes.append({
            "id": gen_id(),
            "name": skill_name,
            "skill": skill_name,
            "triggers": triggers,
            "priority": 5,
            "auto": True,
            "confidence": 0.9,
            "note": f"Auto-registered: {cluster} cluster"
        })

# DBS series
for skill_name, triggers in dbs_skills.items():
    new_routes.append({
        "id": gen_id(),
        "name": skill_name,
        "skill": skill_name,
        "triggers": triggers,
        "priority": 5,
        "auto": True,
        "confidence": 0.85,
        "note": "Auto-registered: dbs cluster"
    })

# Vercel series
for skill_name, triggers in vercel_skills.items():
    new_routes.append({
        "id": gen_id(),
        "name": skill_name,
        "skill": skill_name,
        "triggers": triggers,
        "priority": 6,
        "auto": True,
        "confidence": 0.8,
        "note": "Auto-registered: vercel cluster"
    })

# Remaining skills
for skill_name, triggers in remaining_skills.items():
    if not triggers:
        continue
    new_routes.append({
        "id": gen_id(),
        "name": skill_name,
        "skill": skill_name,
        "triggers": triggers,
        "priority": 5,
        "auto": True,
        "confidence": 0.85,
        "note": "Auto-registered: individual skill"
    })

# Register any STILL unregistered skills with basic triggers
registered_skills = set(r.get("skill", "") for r in data["routes"])
registered_skills.update(r.get("skill", "") for r in new_routes)

all_dirs = [d for d in os.listdir(SKILLS_DIR)
            if os.path.isdir(os.path.join(SKILLS_DIR, d))
            and not d.startswith(".")]

for skill_name in all_dirs:
    if skill_name in registered_skills:
        continue
    name = skill_name.replace(".bak", "").replace(".zip", "")
    triggers = [name]
    if "-" in name:
        triggers.append(name.replace("-", " "))
    if "_" in name:
        triggers.append(name.replace("_", " "))
    new_routes.append({
        "id": gen_id(),
        "name": name,
        "skill": skill_name,
        "triggers": list(set(triggers)),
        "priority": 7,
        "auto": True,
        "confidence": 0.7,
        "note": "Auto-registered: basic trigger from directory name"
    })

# Merge and save
data["routes"].extend(new_routes)

# De-duplicate by skill name (keep the one with more triggers)
seen = {}
deduped = []
for r in data["routes"]:
    sk = r.get("skill", "")
    if sk in seen:
        existing = seen[sk]
        if len(r.get("triggers", [])) > len(existing.get("triggers", [])):
            # Replace
            deduped.remove(existing)
            deduped.append(r)
            seen[sk] = r
        else:
            # Merge triggers
            existing_triggers = set(existing.get("triggers", []))
            existing_triggers.update(r.get("triggers", []))
            existing["triggers"] = list(existing_triggers)
    else:
        deduped.append(r)
        seen[sk] = r

data["routes"] = deduped

with open(RT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

li_count = sum(1 for r in data["routes"] if r.get("skill", "").startswith("li-"))
total = len(data["routes"])
print(f"=== ROUTE REGISTRATION COMPLETE ===")
print(f"New routes added: {len(new_routes)}")
print(f"After dedup: {total} total routes")
print(f"li- routes: {li_count}")
print(f"Non-li routes: {total - li_count}")

# Count triggers
all_triggers = set()
for r in data["routes"]:
    all_triggers.update(r.get("triggers", []))
print(f"Unique triggers: {len(all_triggers)}")
