#!/usr/bin/env python3
"""Correct skill-bloat-analysis report with verified data."""
import os

report_path = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\skill-bloat-analysis-2026-06-22.md'

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ===== CORRECTION 1: Add verification disclaimer at top =====
# Find the first ## heading and insert before it
old_h1 = '## 一、定量全景'
new_h1 = '''## 〇、数据验真声明

> **用户要求验证数据真伪后重写。** 以下数字均为直接从文件系统/路由表读取的原始值。
> 初报中有 3 项数据经核实后修正（见下方「初报错误」）。

### 初报错误清单

| 错误项 | 初报值 | 核实后值 | 错误原因 |
|--------|--------|---------|---------|
| 活跃 skill 数 | 109 | **107** | os.listdir 含 2 个空目录被误计入 |
| 弃用 skill 有路由 | 16 | **14** | li-skills-mgmt 路由条目不重复计算 |
| li-design vs li-image 重叠 | 86% | **不重叠** | 凭关键词脚本猜重叠，未读 SKILL.md 原文 |
| li-bestskill vs li-local-search 重叠 | 边界模糊 | **不重叠** | 同上，未区分"发现"和"路由"的本质差异 |
| fpga vs systemverilog 重叠 | 有重叠 | **边界清晰** | fpga 覆盖 Vivado/时序/AXI，systemverilog 覆盖 ASIC/验证 |

### 数据验真记录

| 数据项 | 验证方法 | 结果 |
|--------|---------|------|
| 130 个目录项 | os.listdir(skills_dir) | 含 4 个非目录文件（2 txt + 1 json + 1 bak） |
| 126 个 skill 目录 | 130 - 4 非目录文件 | 其中 124 有 SKILL.md，2 为空目录 |
| 107 活跃 / 17 弃用 | 检查每个目录的 DEPRECATED.md | 精确值 |
| 105 路由 / 1651 触发词 | skill-routing-table.json 解析 | 精确值 |
| 14 弃用 skill 有路由 | 交叉比对路由表 + DEPRECATED.md | 精确值 |
| 18 幽灵 skill | 107 活跃 - 89 有路由 = 18 | 精确值 |
| 12 触发词冲突 | 路由表 triggers 字段交叉比对 | 精确值 |
| 33.3 MB | os.walk 递归求和 | 精确值 |
| SKILL.md 大小 | os.path.getsize | 精确值 |

## 一、定量全景'''

content = content.replace(old_h1, new_h1)

# ===== CORRECTION 2: Fix overlap group A =====
old_a = """#### 组 A：视觉/设计创作（5 个 skill 争抢同一场景）

| Skill | 大小 | 核心能力 | 建议 |
|-------|------|---------|------|
| li-design | 2.5 KB | 品牌视觉/UI设计/前端页面 | 与 li-image 合并 |
| li-image | 2.1 KB | 图片生成与编辑 | 与 li-design 合并 |
| li-video | 6.2 KB | 视频制作 | 独立（视频有独特流程） |
| li-web | 2.5 KB | 网页开发 | 独立（代码型，非生成型） |
| li-xhs | 9.2 KB | 小红书内容创作 | 独立（文案型，非视觉型） |

**建议**：li-design + li-image → 合并为 li-visual（已有 li-visual，直接扩展）。保留 li-video/li-web/li-xhs 独立。"""

new_a = """#### 组 A：视觉/设计创作（5 个 skill 分工清晰）

| Skill | 大小 | 核心能力 | 重叠度 | 建议 |
|-------|------|---------|--------|------|
| li-design | 2.5 KB | 品牌视觉/UI设计/前端页面/设计系统 | 低 | 独立 |
| li-image | 2.1 KB | 图片生成与编辑（DALL-E/Gemini/信息图） | 低 | 独立 |
| li-video | 6.2 KB | 视频制作 | 无 | 独立 |
| li-web | 2.5 KB | 网页开发 | 无 | 独立（代码型） |
| li-xhs | 9.2 KB | 小红书内容创作 | 无 | 独立（文案型） |

**纠正**：初报声称 li-design + li-image 有 86% 关键词重叠，实际读取 SKILL.md 原文后发现：
- li-design：品牌视觉/UI 设计/前端页面/设计系统 → **设计方向**
- li-image：图片生成与编辑（DALL-E/Gemini/信息图）→ **生成方向**

两者互补而非重叠。**不合并。**"""

content = content.replace(old_a, new_a)

# ===== CORRECTION 3: Fix group E =====
old_e = """#### 组 E：双胞胎（完全重复）

| Pair | 大小 | 分析 |
|------|------|------|
| **newmax-help + niuma-help** | 各 7.7 KB | **完全重复**。两个帮助 skill，SKILL.md 完全相同（54.7 KB each）。合并为 1 个。 |
| **li-bestskill + li-local-search** | 13.7+11.3 KB | **边界模糊**。li-bestskill 搜外部，li-local-search 搜本地。功能互补，但两者 SKILL.md 中有大量重复（都讲"怎么找 skill"）。建议合为 li-search（外部+内部一体）。 |"""

new_e = """#### 组 E：双胞胎（1 对确认重复，1 对确认不重叠）

| Pair | 大小 | 分析 |
|------|------|------|
| **newmax-help + niuma-help** | 各 7.7 KB | **确认重复**。两个帮助 skill，SKILL.md 内容几乎逐字相同（仅产品名称不同：NewMax AI vs 牛马AI）。**合并为 1 个。** |
| **li-bestskill + li-local-search** | 13.7+11.3 KB | **不重叠**。li-bestskill 搜外部 skill 市场（找新 skill），li-local-search 搜本地已安装 skill（路由已有 skill）。一个是"发现"，一个是"调度"，功能互补而非重复。**不合并。** |"""

content = content.replace(old_e, new_e)

# ===== CORRECTION 4: Fix group C =====
old_c = """#### 组 C：硬件/FPGA（7 个 skill 竞逐）

| Skill | 大小 | 核心能力 | 建议 |
|-------|------|---------|------|
| fpga | 2.7 KB | FPGA 开发 | 与 li-hardware 合并 |
| systemverilog | 2.6 KB | SystemVerilog | 与 li-hardware 合并 |
| rtl-fpga-lessons | 2.1 KB | RTL 教训 | 作为 li-hardware 的 reference |
| li-hardware | 12.4 KB | FPGA RTL + Arduino + 伺服 | 核心 skill |
| li-embedded | 12.2 KB | STM32/ARM 嵌入式 | 核心 skill |
| competition-fpga | 7.0 KB | FPGA 竞赛 | 独立（竞赛流程特殊） |
| competition-yolo | 21.3 KB | YOLO 竞赛 | 独立 |

**建议**：fpga + systemverilog + rtl-fpga-lessons → 归入 li-hardware references/ 目录。li-hardware + li-embedded 保持独立（FPGA vs 嵌入式是不同技术栈）。"""

new_c = """#### 组 C：硬件/FPGA（7 个 skill 分工基本清晰）

| Skill | 大小 | 核心能力 | 重叠度 | 建议 |
|-------|------|---------|--------|------|
| fpga | 2.7 KB | FPGA 开发（Vivado/时序/AXI） | 中（与 systemverilog 有交叉） | 可归入 li-hardware references |
| systemverilog | 2.6 KB | SystemVerilog（FPGA+ASIC/验证） | 中（与 fpga 有交叉） | 可归入 li-hardware references |
| rtl-fpga-lessons | 2.1 KB | RTL 教训 | 低 | 作为 li-hardware reference |
| li-hardware | 12.4 KB | FPGA RTL + Arduino + 伺服 | 核心 | 独立 |
| li-embedded | 12.2 KB | STM32/ARM 嵌入式 | 无 | 独立（不同技术栈） |
| competition-fpga | 7.0 KB | FPGA 竞赛 | 无 | 独立 |
| competition-yolo | 21.3 KB | YOLO 竞赛 | 无 | 独立 |

**纠正**：初报声称 fpga 和 systemverilog 有重叠，实际读取 SKILL.md 后发现：
- fpga：覆盖 Vivado 开发流程、时序收敛、AXI 接口 → **工程实践方向**
- systemverilog：覆盖 SystemVerilog 语言规范、ASIC/FPGA 验证方法学 → **语言/验证方向**

两者有部分内容交叉（都涉及 Verilog 代码），但核心分工清晰。**不合并。** 可把 fpga + systemverilog + rtl-fpga-lessons 归入 li-hardware 的 references/ 作为子文档。"""

content = content.replace(old_c, new_c)

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Report corrected successfully')
print(f'Size: {os.path.getsize(report_path)} bytes')
