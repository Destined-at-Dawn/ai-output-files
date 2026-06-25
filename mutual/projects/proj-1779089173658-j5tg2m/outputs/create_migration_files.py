# -*- coding: utf-8 -*-
"""
迁移文件生成器
创建：claude.bat + 迁移指南.md + 跨工具兼容 CLAUDE.md
"""
import os
from datetime import datetime

WORKSPACES = {
    "mutual": r"E:\ai产出文件\牛马\mutual\mutual",
    "个人": r"E:\ai产出文件\牛马\个人\个人",
    "创作": r"E:\ai产出文件\牛马\创作\创作",
    "求职": r"E:\ai产出文件\牛马\求职\求职",
    "竞赛": r"E:\ai产出文件\牛马\竞赛\竞赛",
}

OUTPUT_DIR = r"E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs"

# ============================================================
# 1. claude.bat — 启动脚本
# ============================================================
def create_bat():
    content = r"""@echo off
chcp 65001 >nul 2>&1
title 牛马AI 工作区启动器

echo ============================================
echo   牛马AI 工作区启动器
echo ============================================
echo.
echo  1. mutual    [管理/优化] — 当前位置
echo  2. 个人      [个人成长/数字先知]
echo  3. 创作      [内容创作/公众号/小红书]
echo  4. 求职      [实习/简历/求职策略]
echo  5. 竞赛      [FPGA/电赛/竞赛]
echo.
echo  0. 退出
echo ============================================
echo.

set /p choice="选择工作区 [1-5]: "

if "%choice%"=="1" (
    cd /d "E:\ai产出文件\牛马\mutual\mutual"
    goto :launch
)
if "%choice%"=="2" (
    cd /d "E:\ai产出文件\牛马\个人\个人"
    goto :launch
)
if "%choice%"=="3" (
    cd /d "E:\ai产出文件\牛马\创作\创作"
    goto :launch
)
if "%choice%"=="4" (
    cd /d "E:\ai产出文件\牛马\求职\求职"
    goto :launch
)
if "%choice%"=="5" (
    cd /d "E:\ai产出文件\牛马\竞赛\竞赛"
    goto :launch
)
if "%choice%"=="0" exit
echo [错误] 无效选择
pause
exit /b 1

:launch
echo.
echo 工作区: %cd%
echo 启动 Claude Code...
echo.
claude
"""
    path = os.path.join(OUTPUT_DIR, "claude.bat")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] claude.bat -> {path}")

    # 同时放到桌面上
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    desktop_path = os.path.join(desktop, "claude.bat")
    with open(desktop_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] claude.bat -> {desktop_path}")

    # 创建各工作区的快捷 bat
    for name, ws_path in WORKSPACES.items():
        quick_content = f"""@echo off
chcp 65001 >nul 2>&1
title Claude Code - {name}
cd /d "{ws_path}"
echo 工作区: %cd%
claude
"""
        quick_path = os.path.join(desktop, f"claude-{name}.bat")
        with open(quick_path, "w", encoding="utf-8") as f:
            f.write(quick_content)
        print(f"[OK] claude-{name}.bat -> {quick_path}")

    return path

# ============================================================
# 2. 跨工具兼容 CLAUDE.md（通用版）
# ============================================================
def create_universal_claude_md():
    content = """# 五工作区统一规则（跨 AI 工具兼容版）

> 本文件供所有 AI 工具读取：Claude Code / Claude Desktop / Codex / Hermes
> 小黎（李兰源），上海电力大学大一，GPA 3.9/4.0

---

## 工作区地图

| 工作区 | 路径 | 职责 | 主力工具 |
|--------|------|------|---------|
| mutual | `E:\\ai产出文件\\牛马\\mutual\\mutual` | 生态管理/优化/skill 管理 | Newmax + Claude Code |
| 个人 | `E:\\ai产出文件\\牛马\\个人\\个人` | 个人成长/百大认知/数字先知 | Claude Desktop |
| 创作 | `E:\\ai产出文件\\牛马\\创作\\创作` | 公众号/小红书/内容创作 | Newmax |
| 求职 | `E:\\ai产出文件\\牛马\\求职\\求职` | 实习/简历/求职策略 | Claude Desktop |
| 竞赛 | `E:\\ai产出文件\\牛马\\竞赛\\竞赛` | FPGA/电赛/数学建模 | Codex + Claude Desktop |

---

## 三条死线（违反任何一条 = 事故）

1. **做了才说** — "已记录""已创建""已修复"只在工具调用返回成功后才能说
2. **验了才断** — 断言任何事实前，必须先用工具验证
3. **每轮有质变** — 迭代不是复制粘贴，每轮必须有实质差异

---

## 核心规则（所有工具通用）

### No Blind Overwrite（数据安全 — 最高优先级）
写已存在的文件前，必须先 Read 当前内容。
- write_project_file / Write 是覆写，不是追加
- 能用 Edit 精确替换的，绝不用 Write 全文覆写
- 没有"我记得内容"这回事

### 中文路径铁律
- 路径或内容含中文时，禁止用 Bash heredoc（MSYS2 必炸）
- 一律用 Python 脚本操作中文路径（Python 原生 Unicode，零问题）
- PowerShell .ps1 文件用 GBK 编码

### 脚本安全检查
- 删除操作必须精确到文件级别，禁止对目录执行删除
- 批量操作必须先 dry-run → 展示给用户 → 确认 → 执行 → 验证
- 系统路径（C:\\Windows\\, C:\\ProgramData\\）禁止删除/修改

### 执行力 > 设计力
- 用户要可运行的方案，不是设计文档
- 结论先行 → 原因 → 引用来源
- 信息密度要高，避免水词

---

## 文件结构规范（迁移后）

```
{工作区根目录}/
  CLAUDE.md              ← AI 读取的规则文件
  AGENT.md               ← Codex/Hermes 配置
  MASTER.md              ← 通用 Agent 配置
  memory/
    long-term.md         ← 唯一的长期记忆文件
    {YYYY-MM-DD}.md      ← 每日记忆
  outputs/               ← 所有产出统一存放（不分子目录）
  SOPs/                  ← 标准操作流程
  .claude/rules/         ← Claude Code 专属规则
  projects/              ← 命名项目目录（YYYYMMDD-主题）
```

### 禁止的结构
- ❌ projects/ 下不再有 memory/ 子目录
- ❌ 不再创建 proj-{timestamp}-{random} 目录
- ❌ 不再有 MEMORY.md（用 memory/long-term.md 替代）
- ❌ 不再有嵌套的 outputs/（所有产出写根目录 outputs/）

---

## 记忆管理

- 长期记忆 → `memory/long-term.md`
- 每日记忆 → `memory/{YYYY-MM-DD}.md`
- 所有 AI 工具共享同一个 memory/ 目录
- 写入前先 Read，写入后 Verify

---

## 小黎的偏好

- **信息密度**：高。结论先行，不要铺垫。列表优于表格
- **深度**：喜欢"为什么"的深层解释，但保持简洁
- **引用**：数据/结论必须标注来源（Source: path#line）
- **语气**：像一个被真实项目打磨过的学长——直接、有判断力、不讨好
- **技术**：AI 前沿、FPGA、电气、数学物理、小红书变现、OPC
- **认知**：分析和建议要有认知科学支撑，引用百大认知书籍

---

## 百大认知系统

62 本认知科学/心理学书籍位于 `E:\\ai产出文件\\牛马\\个人\\个人\\百大认知书籍\\`
- 决策场景：双系统理论、锚定效应、WYSIATI
- 学习场景：认知负荷理论、间隔效应、检索式练习
- 风险管理：反脆弱、黑天鹅、损失厌恶
- 引用格式：原句 + 《书名》编号

---

## 知识中枢（Obsidian Vault）

- 路径：`E:\\ai产出文件\\牛马\\知识中枢\\`
- 工作区注册表：`知识中枢/00-注册表/工作区注册表.md`
- 共享规则：`知识中枢/02-共享规则/`
- 防乱建规则：新建任何目录/文件前，先查注册表确认位置

---

*迁移日期：2026-06-11*
*本文件由 mutual 工作区 AI 生成，供所有工作区和所有 AI 工具共享*
"""
    return content

# ============================================================
# 3. 各工作区专属 CLAUDE.md
# ============================================================
WORKSPACE_SPECIFIC = {
    "mutual": """# mutual 工作区 — 生态管理/优化

> 主力工具：Newmax（牛马AI）+ Claude Code

## 职责
- 管理五工作区生态的健康运行
- Skill 生命周期管理（创建/审核/融合/弃用）
- 路由表维护（skill-routing-table.json）
- 共享规则维护（知识中枢/02-共享规则/）
- 跨工作区同步

## 特殊约束
- 本工作区是唯一保留 Newmax 完整能力的工作区
- skill-handler、project-tools 等 MCP 在本工作区可用
- 其他工作区已迁移至 Claude Desktop / Codex

## 文件结构
```
mutual/
  CLAUDE.md                ← 本文件（通用规则已在上层 CLAUDE.md）
  memory/                  ← 长期记忆 + 每日记忆
  outputs/                 ← 所有产出
  SOPs/                    ← 标准操作流程
  skills/                  ← 本地 skill 定义
  skill-routing-table.json ← 路由表（唯一权威源）
  .claude/rules/           ← 17 条工程规则
  knowledge-base/          ← 知识库
```
""",
    "个人": """# 个人工作区 — 个人成长/百大认知

> 主力工具：Claude Desktop

## 职责
- 百大认知系统管理（62 本书）
- 个人成长与认知升级
- 数字先知系统
- 心理机制分析

## 文件结构
```
个人/
  CLAUDE.md
  memory/
  outputs/
  百大认知书籍/          ← 62 本认知科学书籍
  digital-oracle/        ← 数字先知系统
  career-breakthrough/   ← 职业突破
```

## 与 Claude Desktop 的交互
- Claude Desktop 打开本目录即可读取 CLAUDE.md
- 百大认知书籍在 `百大认知书籍/` 目录下
- 参考格式：引用原句 + 《书名》编号
""",
    "创作": """# 创作工作区 — 公众号/小红书/内容创作

> 主力工具：Newmax（牛马AI）— 本工作区继续使用 Newmax

## 职责
- 公众号文章创作与发布
- 小红书内容创作
- 视觉设计与配图
- 内容策略规划

## 文件结构
```
创作/
  CLAUDE.md
  memory/
  outputs/
  projects/              ← 内容项目（YYYYMMDD-主题命名）
  downloads/             ← 下载素材
  IDEAS/                 ← 创意库
  github/                ← GitHub 相关项目
```

## 特殊约束
- 本工作区保留 Newmax 的完整 skill 调用能力
- li-xhs、li-image、li-video、blog-post-writer 等创作 skill 在此可用
- baoyu-post-to-wechat 等发布 skill 在此可用
""",
    "求职": """# 求职工作区 — 实习/简历/求职策略

> 主力工具：Claude Desktop

## 职责
- 简历优化与维护
- 求职策略规划
- 面试准备
- Offer 分析

## 文件结构
```
求职/
  CLAUDE.md
  memory/
  outputs/
  projects/              ← 求职项目
```

## 关键信息
- 目标：具身智能/机器人/FPGA 方向实习
- 背景：上海电力大学电气工程大一，GPA 3.9/4.0
- 已确认：威泊机器人研发实习
- 长期目标：上交/东南电气考研
""",
    "竞赛": """# 竞赛工作区 — FPGA/电赛/数学建模

> 主力工具：Codex CLI + Claude Desktop

## 职责
- FPGA 开发（XC7A35T）
- 电赛准备与实战
- 数学建模竞赛
- 跨校协作管理

## 文件结构
```
竞赛/
  CLAUDE.md
  AGENTS.md              ← Codex 配置
  memory/
  outputs/
  projects/              ← 竞赛项目（YYYYMMDD-主题 或 项目名）
  scripts/
```

## 硬件上下文
- FPGA：Xilinx XC7A35T（Artix-7）
- 开发环境：Vivado
- Arduino/ESP32 + 舵机控制
- RoboMaster 步兵控制

## 特殊约束
- Codex CLI 主要用于代码编写和 FPGA RTL
- Claude Desktop 用于方案讨论和文档撰写
- 竞赛项目用项目名目录（如 `Yolo算法比赛/`），不用 proj-ID
""",
}

# ============================================================
# 4. 迁移指南
# ============================================================
def create_migration_guide():
    content = f"""# 🔧 工具链迁移指南

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 目标：从 Newmax 单工具 → Claude Desktop + Codex + Hermes 多工具架构

---

## 一、当前状态诊断

| 问题 | 数量 | 说明 |
|------|------|------|
| proj- 目录 | 10 个 | 每次新对话自动创建，命名不可读 |
| 嵌套 memory/ | 48 个 | 和根目录 memory/ 内容不同步 |
| MEMORY.md 残留 | 5 个 | 规范要求用 memory/long-term.md |
| 临时脚本堆积 | 56+ 个 | outputs/ 混杂中间产物和最终产出 |
| conversations/ | 5 个 | 仅含图片碎片 |

**核心问题**：文件路径太深 + 目录结构混乱 + proj-ID 不可读

---

## 二、已完成的配置

### ✅ claude.bat 启动脚本
- 桌面上已创建 `claude.bat` — 多工作区选择器
- 桌面上已创建 `claude-mutual.bat` / `claude-个人.bat` / ... — 一键直达
- 双击即用，无需手动 cd

### ✅ 各工作区 CLAUDE.md
已为 5 个工作区创建/更新 CLAUDE.md：
- **通用规则**（共享）：三条死线、No Blind Overwrite、中文路径铁律、文件结构规范
- **工作区特有**（每区独立）：职责、文件结构、工具配置

### ✅ 全局 CLAUDE.md
`~/.claude/CLAUDE.md` 已更新，包含：
- 跨工具感知（5 个工作区地图）
- 文件结构规范（禁止 proj-ID 目录）
- 迁移后规则

---

## 三、你需要手动完成的步骤

### Step 1: 验证 Claude Code 可用

```
# 双击桌面上的 claude.bat，选择工作区
# 或直接命令行：
cd "E:\\ai产出文件\\牛马\\mutual\\mutual"
claude
```

确认 Claude Code 能正常启动并读取 CLAUDE.md。

### Step 2: 验证 Claude Desktop 可用

1. 打开 Claude Desktop
2. 在设置中确认 API Key 正确
3. 新建对话，输入："读取当前目录下的 CLAUDE.md，告诉我你看到了什么工作区信息"
4. 如果 Claude Desktop 不能自动读取 CLAUDE.md，手动复制内容到对话开头

> **注意**：Claude Desktop 可能不支持自动读取 CLAUDE.md。
> 如果不支持，你可以在 Claude Desktop 的 System Prompt 中粘贴 CLAUDE.md 的内容。

### Step 3: 配置 Codex CLI

```bash
# 确认 Codex 可用
cd "E:\\ai产出文件\\牛马\\竞赛\\竞赛"
codex
```

Codex 会读取 AGENTS.md（已存在于竞赛工作区）。

### Step 4: 文件结构清理（可选，建议执行）

**建议在 Claude Code（Newmax）中执行以下操作：**

1. **归档 proj- 目录内容**
   ```
   # 把 projects/proj-*/ 中的有价值产出移到根目录 outputs/
   # 旧 proj- 目录归档到 E:\\ai产出文件\\牛马\\归档\\
   ```

2. **清理 MEMORY.md 残留**
   ```
   # 检查 5 个 MEMORY.md 的独有内容
   # 合并到对应 memory/long-term.md
   # 删除 MEMORY.md
   ```

3. **清理临时脚本**
   ```
   # 把 outputs/ 中的临时脚本（export_chat_v*.py 等）归档
   # 保留有价值的报告和最终产出
   ```

4. **归档 conversations/**
   ```
   # proj-conv-* 目录仅含图片碎片
   # 归档或删除
   ```

> 这些操作风险较高，建议在 Newmax 中执行（有完整的规则和保护机制）。

---

## 四、各工具分工

| 工具 | 擅长 | 工作区 | 说明 |
|------|------|--------|------|
| **Newmax** | Skill 调用、微信分析、项目管理 | mutual + 创作 | 保留完整能力 |
| **Claude Code** | 代码编写、文件操作、Git | 所有工作区 | 通过 claude.bat 启动 |
| **Claude Desktop** | 对话分析、深度思考、文档 | 个人 + 求职 | GUI 操作 |
| **Codex CLI** | FPGA 代码、RTL 开发 | 竞赛 | 代码专精 |
| **Hermes Agent** | 待定 | 待定 | 你来定义 |

---

## 五、文件路径速查

| 内容 | 路径 |
|------|------|
| 全局规则 | `C:\\Users\\13975\\.claude\\CLAUDE.md` |
| Newmax MCP 配置 | `C:\\Users\\13975\\.newmax\\.mcp.json` |
| Claude Code 配置 | `C:\\Users\\13975\\.claude\\config.json` |
| Claude Desktop 配置 | `C:\\Users\\13975\\AppData\\Roaming\\Claude\\` |
| 知识中枢 | `E:\\ai产出文件\\牛马\\知识中枢\\` |
| 百大认知书籍 | `E:\\ai产出文件\\牛马\\个人\\个人\\百大认知书籍\\` |
| 归档目录 | `E:\\ai产出文件\\牛马\\归档\\` |
| mempalace（语义搜索） | `D:\\mempalace` |

---

## 六、共享资源（所有工具可用）

1. **memory/ 目录** — 所有 AI 工具共享同一个记忆系统
2. **知识中枢** — Obsidian Vault，62 本认知书籍
3. **outputs/ 目录** — 所有产出统一存放
4. **SOPs/** — 标准操作流程
5. **百大认知** — 认知科学知识库

---

## 七、风险与回退

| 风险 | 应对 |
|------|------|
| Claude Desktop 不读 CLAUDE.md | 手动粘贴到 System Prompt |
| 多工具同时写 memory/ 冲突 | 每次写入前 Read，写入后 git commit |
| 旧 proj- 目录有未提取的重要内容 | Phase 1 整合时先 diff 再操作 |
| Newmax 额度用完 | 回退到 Claude Desktop 或 Codex |

---

*本指南由 mutual 工作区 AI 自动生成*
"""
    return content


# ============================================================
# Main
# ============================================================
def main():
    print("=" * 60)
    print("迁移文件生成器")
    print("=" * 60)
    print()

    # 1. 创建 claude.bat
    print("[1/4] 创建 claude.bat 启动脚本...")
    create_bat()

    # 2. 创建通用 CLAUDE.md
    print("\n[2/4] 创建跨工具兼容 CLAUDE.md...")
    universal = create_universal_claude_md()
    for name, ws_path in WORKSPACES.items():
        path = os.path.join(ws_path, "CLAUDE-CROSS-TOOL.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(universal)
        print(f"  [OK] {name}: {path}")

    # 3. 创建工作区专属 CLAUDE.md
    print("\n[3/4] 创建工作区专属 CLAUDE.md...")
    for name, ws_path in WORKSPACES.items():
        if name in WORKSPACE_SPECIFIC:
            path = os.path.join(ws_path, "CLAUDE-WORKSPACE.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(WORKSPACE_SPECIFIC[name])
            print(f"  [OK] {name}: {path}")

    # 4. 创建迁移指南
    print("\n[4/4] 创建迁移指南...")
    guide_path = os.path.join(OUTPUT_DIR, "迁移指南-工具链迁移.md")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(create_migration_guide())
    print(f"  [OK] {guide_path}")

    # 5. 汇总
    print("\n" + "=" * 60)
    print("生成完毕！文件清单：")
    print("=" * 60)
    print()
    print("桌面上：")
    print("  - claude.bat         （多工作区选择器）")
    print("  - claude-mutual.bat  （直达 mutual）")
    print("  - claude-个人.bat    （直达 个人）")
    print("  - claude-创作.bat    （直达 创作）")
    print("  - claude-求职.bat    （直达 求职）")
    print("  - claude-竞赛.bat    （直达 竞赛）")
    print()
    print("各工作区：")
    print("  - CLAUDE-CROSS-TOOL.md  （通用规则，给所有 AI 看）")
    print("  - CLAUDE-WORKSPACE.md   （工作区专属规则）")
    print()
    print("outputs/：")
    print("  - 迁移指南-工具链迁移.md  （给你看的行动步骤）")
    print()
    print("下一步：")
    print("  1. 双击桌面 claude.bat 验证 Claude Code 可启动")
    print("  2. 打开 Claude Desktop 测试 API 连接")
    print("  3. 在 Newmax 中执行文件结构清理（见迁移指南 Step 4）")

if __name__ == "__main__":
    main()
