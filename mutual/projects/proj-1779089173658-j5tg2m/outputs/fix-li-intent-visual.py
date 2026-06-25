import os, sys
sys.stdout.reconfigure(encoding='utf-8')

# Fix li-intent: add cases
intent_path = r'C:\Users\13975\.newmax\skills\li-intent\SKILL.md'
with open(intent_path, 'r', encoding='utf-8') as f:
    content = f.read()

case1 = "### Case 1: 公众号链接分析\n"
case1 += "**触发**: 用户发送微信公众号 URL + 帮我看看\n"
case1 += "**意图匹配**: content_extract_and_analyze\n"
case1 += "**Skill 链**: baoyu-url-to-markdown -> li-analyze (Mode A) -> li-memory\n"
case1 += "**结果**: 自动提取文章 -> 道法术器四层分析 -> 事实提取入记忆\n"
case1 += "**关键**: 用户不需要说先提取再分析再存储，SOP 自动串联\n"

case2 = "\n### Case 2: 帮我调研 FPGA 舵机控制\n"
case2 += "**触发**: 自然语言，无 URL 无文件\n"
case2 += "**意图匹配**: research_and_hardware\n"
case2 += "**Skill 链**: li-research -> li-hardware -> li-devil\n"
case2 += "**结果**: 搜外部 -> 结合用户 FPGA 经验 -> 泼冷水检查可行性\n"
case2 += "**关键**: li-research 搜到的资料自动流入 li-hardware 的上下文\n"

case3 = "\n### Case 3: 这个方案不行，换个思路\n"
case3 += "**触发**: 对话中途的方向转换\n"
case3 += "**意图匹配**: pivot_and_redesign\n"
case3 += "**Skill 链**: li-devil (预验尸) -> li-research (重新搜索) -> li-analyze (对比)\n"
case3 += "**结果**: 先泼冷水分析为什么不行 -> 搜新方向 -> 对比新旧方案\n"
case3 += "**关键**: 意图理解层识别否定+重定向模式，不需要用户重新描述需求\n"

cases_section = "\n## Case Studies\n\n" + case1 + case2 + case3

if "Case Studies" not in content and "案例" not in content:
    # Insert before last section or at end
    if "## References Index" in content:
        content = content.replace("## References Index", cases_section + "\n\n## References Index")
    elif "---" in content and content.count("---") > 1:
        # Insert before last ---
        last_sep = content.rfind("---")
        content = content[:last_sep] + cases_section + "\n\n" + content[last_sep:]
    else:
        content = content.rstrip() + cases_section

    with open(intent_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"li-intent: {len(content.splitlines())} lines, cases added")
else:
    print("li-intent: already has cases")

# Fix li-visual: add cross-links
visual_path = r'C:\Users\13975\.newmax\skills\li-visual\SKILL.md'
with open(visual_path, 'r', encoding='utf-8') as f:
    vc = f.read()

links = "\n\n## Cross-Skill Links\n\n"
links += "| Skill | Trigger | Integration |\n"
links += "|-------|---------|-------------|\n"
links += "| li-analyze | 文章需配图 | 视觉风格注入分析报告 |\n"
links += "| li-storyboard | 分镜需视觉风格 | 调色板应用到分镜 |\n"
links += "| li-prompt | 跨平台prompt需视觉指令 | 风格描述嵌入六维框架 |\n"
links += "| li-skillcreate | 新skill需封面 | 生成封面prompt |\n"
links += "| li-manage | 视觉资产归档 | prompt/参考图纳入管理 |\n"

if "Cross-Skill" not in vc and "联动" not in vc:
    vc = vc.rstrip() + links
    with open(visual_path, 'w', encoding='utf-8') as f:
        f.write(vc)
    print(f"li-visual: {len(vc.splitlines())} lines, links added")
else:
    print("li-visual: already has links")
