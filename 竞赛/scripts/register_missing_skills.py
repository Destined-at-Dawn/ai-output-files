"""注册 21 个缺失的 li- skill 到路由表"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

ROUTING_FILE = "${WORKSPACE_ROOT}/skill-routing-table.json"

with open(ROUTING_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

routes = data.get("routes", data) if isinstance(data, dict) else data
registered = {r.get("name", r.get("skill", "")) for r in routes}

MISSING_ROUTES = [
    {"name": "li-research", "auto": True, "enabled": True, "priority": 3,
     "triggers": ["调研", "研究报告", "深度调研", "技术调研", "市场调研", "调研报告", "帮我查一下", "帮我搜一下", "调研一下", "调查一下", "研究一下", "了解一下", "背景信息", "有没有相关的", "最新进展", "最新资讯"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-research"},
     "description": "深度调研"},
    {"name": "li-devil", "auto": True, "enabled": True, "priority": 3,
     "triggers": ["质疑", "决策质疑", "反面意见", "魔鬼代言人", "有什么风险", "有什么问题", "帮我质疑", "反面分析", "风险分析", "利弊分析", "优缺点"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-devil"},
     "description": "决策质疑器"},
    {"name": "li-hardware", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["FPGA", "硬件设计", "PCB设计", "原理图", "电路设计", "硬件知识库", "RTL", "verilog", "Vivado", "STM32", "Arduino", "嵌入式硬件", "芯片设计", "硬件调试"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-hardware"},
     "description": "硬件设计知识库"},
    {"name": "li-skillcreate", "auto": True, "enabled": True, "priority": 3,
     "triggers": ["创建skill", "新建skill", "创建技能", "新建技能", "做个skill", "建个skill", "做一个新的skill", "skill模板"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-skillcreate"},
     "description": "新skill创建"},
    {"name": "li-memory", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["管理记忆", "记忆管理", "记忆清理", "记忆整理", "清理记忆", "过期记忆", "记忆审计"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-memory"},
     "description": "记忆系统管理"},
    {"name": "li-sync", "auto": True, "enabled": True, "priority": 3,
     "triggers": ["同步规则", "跨工作区同步", "知识中枢同步", "同步配置", "同步到", "全局同步", "同步一下"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-sync"},
     "description": "跨工作区知识同步"},
    {"name": "li-design", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["设计", "设计模式", "设计方案", "架构设计", "系统设计", "UI设计", "交互设计"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-design"},
     "description": "设计技能"},
    {"name": "li-image", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["生成图片", "画图", "配图", "图片生成", "技术图", "架构图", "流程图", "示意图", "图片质量"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-image"},
     "description": "图片生成"},
    {"name": "li-xhs", "auto": True, "enabled": True, "priority": 1,
     "triggers": ["小红书", "xhs", "小红书笔记", "小红书内容", "小红书标题", "小红书封面", "涨粉", "爆款", "爆款笔记"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-xhs"},
     "description": "小红书内容创作"},
    {"name": "li-data", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["数据处理", "数据分析", "数据清洗", "数据转换", "数据集处理", "数据格式"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-data"},
     "description": "数据处理技能"},
    {"name": "li-embedded", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["嵌入式", "单片机", "MCU", "固件", "驱动开发", "底层开发"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-embedded"},
     "description": "嵌入式开发技能"},
    {"name": "li-local-search", "auto": True, "enabled": True, "priority": 3,
     "triggers": ["本地搜索", "搜索本地", "搜文件", "找文件", "本地查找"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-local-search"},
     "description": "本地文件搜索"},
    {"name": "li-manage", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["项目管理", "任务管理", "进度管理", "里程碑", "项目规划"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-manage"},
     "description": "项目管理技能"},
    {"name": "li-office", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["office", "Word文档", "Excel表格", "PPT演示", "办公文档", "文档排版"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-office"},
     "description": "Office文档处理"},
    {"name": "li-persona-qa", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["人格问答", "角色问答", "模拟面试", "模拟对话", "问答训练"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-persona-qa"},
     "description": "人格化问答模拟"},
    {"name": "li-personal", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["个人信息", "个人资料", "个人设置", "个人偏好", "个人配置"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-personal"},
     "description": "个人信息管理"},
    {"name": "li-web", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["网页内容", "抓取网页", "爬取网页", "网页分析", "网页提取", "网页搜索"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-web"},
     "description": "网页内容处理"},
    {"name": "li-video", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["视频脚本", "视频制作", "视频内容", "视频策划", "视频编辑"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-video"},
     "description": "视频内容创作"},
    {"name": "li-transcript", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["字幕", "转录", "语音转文字", "转文字", "听写"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-transcript"},
     "description": "语音转录处理"},
    {"name": "li-bestskill", "auto": True, "enabled": True, "priority": 3,
     "triggers": ["最佳技能", "最佳实践", "技能推荐", "推荐skill", "用什么skill", "哪个skill好"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-bestskill"},
     "description": "技能推荐引擎"},
    {"name": "li-autoreply", "auto": True, "enabled": True, "priority": 2,
     "triggers": ["自动回复", "自动应答", "自动响应", "自动消息", "消息模板"],
     "action": "mcp__skill-handler__Skill", "args": {"skill": "li-autoreply"},
     "description": "自动回复技能"},
]

added = 0
for route in MISSING_ROUTES:
    name = route["name"]
    if name not in registered:
        routes.append(route)
        added += 1
        print(f"+ {name}: {len(route['triggers'])} triggers")

if isinstance(data, dict) and "metadata" in data:
    data["metadata"]["total_routes"] = len(routes)
    data["metadata"]["last_updated"] = "2026-06-13"

with open(ROUTING_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n新增 {added} 个路由，总路由数: {len(routes)}")
