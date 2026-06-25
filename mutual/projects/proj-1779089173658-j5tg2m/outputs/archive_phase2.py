"""
Phase 2 归档脚本：将已被 li- 吸收的非 li- skill 移到归档目录
"""
import shutil
import os
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SKILLS_DIR = Path(r"C:\Users\13975\.newmax\skills")
ARCHIVE_DIR = Path(r"E:\ai产出文件\归档\deprecated-skills-phase2-" + datetime.now().strftime("%Y%m%d"))
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# 分三批归档

# Batch 1: dbs-* 全系列（已被 li-dbs 完全取代）
DBS_SKILLS = [
    "dbs", "dbs-action", "dbs-ai-check", "dbs-benchmark", "dbs-chatroom",
    "dbs-chatroom-austrian", "dbs-content-system", "dbs-decision",
    "dbs-deconstruct", "dbs-diagnosis", "dbs-goal", "dbs-good-question",
    "dbs-hook", "dbs-learning", "dbs-report", "dbs-restore", "dbs-save",
    "dbs-slowisfast", "dbs-xhs-title"
]

# Batch 2: 空壳 + 极小模板（<20KB，无可迁移价值）
TINY_SKILLS = [
    "copywriting-skills", "humanizer-zh", "image-editing", "jiaying-tool",
    "qiaomu-mondo-poster-design", "short-video-production",
    "project-init", "personal-info-finder", "ppt-generator-pro",
    "AI贴片文案生成器", "BROK提示词优化器", "X搜索语法生成器",
    "chatroom-austrian", "claude-skills-zh-cn",
    "dg-slide-tester-animation", "dg-slide-tester-beauty", "dg-slide-tester-layout",
    "magazine-cover", "output-skill", "ppocrv5", "私戳作业批改",
    "虚构角色智能体生成器", "executing-plans", "五步写作法",
    "cold-water", "crc-offer-cover", "dg-planner", "dg-slide-dev",
    "gpt-tasteskill", "imagemagick-conversion", "minimalist-skill",
    "prompt-optimizer", "咨询逐字稿分析器", "feishu-doc-reader",
    "longmemory", "smart-task-planner-skill"
]

# Batch 3: 已被 li- 系列吸收的功能性 skill（有内容但功能已被覆盖）
ABSORBED_SKILLS = [
    # → li-manage/li-sync
    "AI分身迁移包", "AI方法论学习器", "channel-config", "ex-skill",
    "internal-comms", "office-hours", "nuwa-skill", "niuma-help",
    "output-skill",
    # → li-research
    "X搜索语法生成器", "follow-builders", "personal-info-finder",
    "全能网页采集器",
    # → li-prompt
    "BROK提示词优化器", "prompt-optimizer",
    # → li-xhs / li-wechat
    "AI贴片文案生成器", "copywriting-skills", "写作智能体",
    "案例拆解生成器", "五步写作法", "jincheng-pyq",
    # → li-pptx
    "dg-gray-slide-designer", "guizang-ppt-skill", "NanoBanana-PPT-Skills",
    "ppt-generator-pro",
    # → li-transcript
    "transcript-cleaner",
    # → li-study / li-mindcoach
    "shizhanying-coach", "yanjiang", "私戳作业批改",
    # → li-bestskill
    "taste-skill", "gpt-tasteskill",
    # → li-image
    "baoyu-compress-image", "imagemagick-conversion", "magazine-cover",
    # → li-video
    "short-video-production",
    # → li-skills-mgmt
    "minimalist-skill", "claude-skills-zh-cn",
    # → li-memory
    "longmemory",
    # → li-debug / li-diagnose
    "cold-water", "audit-optimizer",
    # → li-infra
    "code", "cursor-acp-adapter", "openclawmp", "mcp-builder",
    # → li-plan
    "executing-plans", "smart-task-planner-skill",
    # → li-design
    "theme-factory",
    # → li-storyboard
    "虚构角色智能体生成器",
    # → li-web
    "feishu-doc-reader", "全能网页采集器",
    # → li-hardware
    "hv-analysis",
    # → li-dbs (remaining)
    "community-filter", "kami",
    # → li-data
    "storage-analyzer",
    # → li-workflow
    "jc-clarifier", "jc-jiaocheng", "jc-zhuagongzhonghao",
    # → li-industry
    "ai-yuyi",
    # → li-visual
    "dg-slide-tester-animation", "dg-slide-tester-beauty", "dg-slide-tester-layout",
]

# 合并去重
all_to_archive = set(DBS_SKILLS + TINY_SKILLS + ABSORBED_SKILLS)

# 需要保留的（不归档）
KEEP = {
    # baoyu 工具链（独立第三方，有独特价值）
    "baoyu-danger-gemini-web", "baoyu-danger-x-to-markdown",
    "baoyu-format-markdown", "baoyu-markdown-to-html",
    "baoyu-post-to-wechat", "baoyu-post-to-x",
    "baoyu-slide-deck", "baoyu-url-to-markdown", "baoyu-xhs-images",
    # 大型第三方仓库
    "nature-skills", "web-artifacts-builder",
    # 独立工具
    "deepl", "github-publisher", "slack-gif-creator",
    "anything-to-notebooklm", "ppocrv5",
    # li 路由器本身
    "li",
    # 工作区适配的第三方
    "karpathy-guidelines",
    # 新增量工具
    "crc-offer-post",  # CRC offer 海报（独立工具）
    "doc-coauthoring",  # 文档协作
    # 已经是 li- 的
}

# 排除 li- 系列和配置文件
li_skills = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and d.name.startswith("li-")}
KEEP.update(li_skills)

# 排除配置文件
config_files = {"skill-routing-table.json"}

moved = []
skipped = []
errors = []

for skill_name in sorted(all_to_archive):
    if skill_name in KEEP:
        skipped.append(f"  SKIP (keep): {skill_name}")
        continue

    src = SKILLS_DIR / skill_name
    if not src.exists():
        skipped.append(f"  SKIP (not found): {skill_name}")
        continue

    if not src.is_dir():
        skipped.append(f"  SKIP (not dir): {skill_name}")
        continue

    dst = ARCHIVE_DIR / skill_name
    try:
        shutil.move(str(src), str(dst))
        moved.append(skill_name)
        print(f"  ✅ {skill_name}")
    except Exception as e:
        errors.append(f"  ❌ {skill_name}: {e}")
        print(f"  ❌ {skill_name}: {e}")

print(f"\n=== 归档完成 ===")
print(f"已归档: {len(moved)}")
print(f"跳过: {len(skipped)}")
print(f"错误: {len(errors)}")
print(f"归档目录: {ARCHIVE_DIR}")

# 检查剩余 skill 数量
remaining = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
print(f"\n剩余 skill 总数: {len(remaining)}")
print(f"其中 li- 系列: {len([s for s in remaining if s.startswith('li-')])}")
print(f"非 li- 系列: {len([s for s in remaining if not s.startswith('li-')])}")
print(f"\n非 li- 列表:")
for s in sorted([s for s in remaining if not s.startswith('li-')]):
    print(f"  {s}")
