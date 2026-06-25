# -*- coding: utf-8 -*-
"""Update niuma-engine README, CHANGELOG, and docs for v4.0 release."""
import os
from datetime import datetime

REPO = r"C:\Users\13975\AppData\Local\Temp\niuma-engine"

def get_rules_list():
    """Get sorted list of rule files from repo."""
    rules_dir = os.path.join(REPO, ".claude", "rules")
    rules = sorted([f for f in os.listdir(rules_dir) if f.endswith('.md')])
    return rules

def get_rule_size(name):
    return os.path.getsize(os.path.join(REPO, ".claude", "rules", name))

def get_rule_desc(name):
    """Get a one-line description for each rule."""
    descs = {
        "10-engineering-laws.md": "十条贯穿性工程法则 (证据分层/防假象审计/实测优先/隔离契约/负结果归档/规则结晶等)",
        "_MIGRATED-TO-RULES.md": "规则迁移说明与反向防御",
        "agent-concurrency-fallback.md": "Agent 并发降级协议 -- 429限流时立即切换顺序模式，禁止等待重试",
        "agent-prompt-ironclad.md": "Agent Prompt 铁律 -- 三要素强制(具体目标/输出格式/停止条件)",
        "anti-illusion-audit.md": "防假象审计 -- 五连问检测异常好/坏数字是否为假象",
        "anti-info-overload.md": "防信息过载 -- 金字塔结构/信息分层/数据筛选",
        "boundary-declaration.md": "边界声明 -- 三栏清单(可写入/不可写入/尚不能声称)",
        "chinese-path-safety.md": "中文路径安全 -- Windows下中文路径必须用Python,禁Bash heredoc",
        "competition-workspace-architecture.md": "竞赛项目工作区架构 -- 主文件夹唯一真相源+两级Memory",
        "dual-write-protocol.md": "双写协议 -- 经验教训必须同时写入根级和模块级",
        "git-recovery.md": "Git检查点与恢复 -- 删前commit快照+30秒恢复",
        "lesson-auto-update.md": "教训闭环自动更新 -- 用户纠正→工作流更新→不再重犯",
        "lifecycle-sop.md": "六阶段项目生命周期SOP -- 立项/探索/并行/签核/复盘/交付",
        "mcp-config-protocol.md": "MCP配置协议 -- 路径/命令格式/wrapper启动/验证四铁律",
        "memory-candidate-protocol.md": "记忆沉淀候选机制 -- 写入前用户确认+四种Nudge自动推动",
        "memory-confidence.md": "记忆置信度与失效条件 -- 高/中/待确认三级+过期自动标注",
        "negative-results.md": "负结果归档 -- 死路必须入档,防止下个对话重新踩坑",
        "no-blind-overwrite.md": "禁止盲目覆写 -- 写已有文件前必须先Read",
        "no-root-rules-dir.md": "禁止根目录rules/ -- 规则唯一存放位置:.claude/rules/",
        "powershell-safety.md": "PowerShell安全 -- 禁止inline $_ / 中文路径用Python",
        "pre-action-check.md": "动手前检查 -- 写脚本/生成图/填模板前必须先检索已有资源",
        "script-safety-check.md": "脚本安全检查 -- 删除精确到文件/dry-run/路径白名单",
        "search-decision-tree.md": "搜索决策树 -- 何时搜索/搜索深度/工具选择的精确决策流程",
        "skill-auto-activation.md": "技能自动激活 (v2.0) -- 三层路由+联动链+自我学习闭环",
        "skill-execution-discipline.md": "Skill执行纪律 -- 调用skill必须先读执行协议,不可跳过",
        "skill-logging-enforcement.md": "Skill调用日志 -- 每次调用后记录/漏调回检/沉睡技能审查",
        "skill-route-enforcement.md": "Skill路由注册 -- 创建/修改/弃用skill必须注册路由",
        "subagent-strategy.md": "Sub-Agent策略 -- 何时用/不用/模型选择/故障恢复",
        "think-before-act.md": "Think Before Act -- 新问题必须研究先行,不可凭感觉动手",
    }
    return descs.get(name, "")

# ============================================================
# Phase 3: Update README.md
# ============================================================
print("=== Updating README.md ===")

with open(os.path.join(REPO, "README.md"), "r", encoding="utf-8") as f:
    readme = f.read()

# Find and replace the rules catalog section
# Old: listing of ~10 rules
# New: full 29-rule catalog with descriptions

old_catalog = """## 仓库结构

```
niuma-engine/
├── README.md                     ← 你在这
├── .claude/rules/                ← 核心规则（Claude Code 自动加载）
│   ├── 10-engineering-laws.md        十条贯穿性工程法则
│   ├── lifecycle-sop.md              六阶段项目生命周期
│   ├── anti-illusion-audit.md        防假象审计（五连问）
│   ├── negative-results.md           负结果归档
│   ├── think-before-act.md           动手前必先思考
│   ├── script-safety-check.md        脚本安全检查
│   ├── no-blind-overwrite.md         禁止盲目覆写
│   ├── memory-candidate-protocol.md  记忆写入确认
│   ├── memory-confidence.md          记忆置信度与失效
│   └── ...（更多规则）
├── templates/                    ← 记忆模板
├── adapters/                     ← 各 Agent 适配器
└── docs/                         ← 设计哲学 + 安装指南
```"""

rules = get_rules_list()
rule_lines = []
for r in rules:
    desc = get_rule_desc(r)
    rule_lines.append(f"│   ├── {r:<40s} {desc}")

new_catalog = f"""## 仓库结构

```
niuma-engine/
├── README.md                     ← 你在这
├── CHANGELOG.md                  ← 版本历史
├── .claude/rules/                ← 核心规则（Claude Code 自动加载，共 {len(rules)} 条）
{chr(10).join(rule_lines)}
├── templates/                    ← 记忆模板（中/英）
├── adapters/                     ← 各 Agent 适配器
└── docs/                         ← 设计哲学 + 安装指南
```"""

readme = readme.replace(old_catalog, new_catalog)

# Update "进化日志" to add v4.0 entries
old_evo_end = """| 2026-05-28 | 10 条法则 + 6 阶段融为一个框架 | 进化日历 + 启动序列 |

**这个框架现在还活着。** 每次我在 5 个工作区里继续协作，新的模式被识别，规则就更新。你看到的不是"最终版"，是这个时间点的快照。"""

new_evo_end = """| 2026-05-28 | 10 条法则 + 6 阶段融为一个框架 | 进化日历 + 启动序列 |
| 2026-06-07 | Windows 中文路径反复炸 heredoc | chinese-path-safety (禁Bash heredoc + 中文用Python) |
| 2026-06-09 | Agent子会话无上下文跑偏(5次故障复盘) | agent-prompt-ironclad (三要素铁律) |
| 2026-06-10 | 并发Agent全部429浪费2整轮对话 | agent-concurrency-fallback (并发降级协议) |
| 2026-06-11 | 教训只记不改=白记 | lesson-auto-update (用户纠正→自动更新工作流) |
| 2026-06-11 | SKILL.md执行协议被跳过 | skill-execution-discipline + skill-logging-enforcement |
| 2026-06-13 | 6次创建skill后忘记注册路由 | skill-route-enforcement (创建必注册) |
| 2026-06-14 | "必要时搜索"太模糊,需要精确决策树 | search-decision-tree (搜索决策树+深度分级) |
| 2026-06-14 | 竞赛项目文件管理混乱 | competition-workspace-architecture (主文件夹唯一真相源) |
| 2026-06-15 | AI写作风格与用户不一致 | 文风DNA自动注入 (写作默认用用户风格) |
| 2026-06-20 | Git .gitignore误排除可恢复临时文件 | git-recovery (删前commit+30秒恢复) |
| 2026-06-21 | 单技能不够,需要联动协作链 | skill-auto-activation v2.0 (三层路由+联动+自学习) |
| 2026-06-22 | 仓库从1.0升级到v4.0: 10条规则 → 29条 | **v4.0 发布** (规则全集+结构性修复) |

**这个框架现在还活着。** 每次我在 5 个工作区里继续协作，新的模式被识别，规则就更新。v4.0 包含了从 2026年5月底到6月22日的所有事故教训和规则结晶。你看到的不是"最终版"，是这个时间点的快照。"""

readme = readme.replace(old_evo_end, new_evo_end)

# Update the "快速开始" section to mention 29 rules
old_quick = """| 想从零搭建完整纪律体系 | 全装 `.claude/rules/` |"""
new_quick = """| 想从零搭建完整纪律体系 | 全装 `.claude/rules/`（共29条） |"""
readme = readme.replace(old_quick, new_quick)

# Update version reference in readme (if any)
if "v1.0.0" in readme:
    # Find the badge or version reference
    pass  # No explicit version badge, handled by story

with open(os.path.join(REPO, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)
print(f"[OK] README.md updated ({len(readme)} chars)")

# ============================================================
# Phase 4: Update CHANGELOG.md
# ============================================================
print("\n=== Updating CHANGELOG.md ===")

changelog = f"""# Changelog

## v4.0.0 (2026-06-22) — 从单体纪律到多Agent协作生态

### 结构性修复
- **修复 .gitignore 阻止规则分发**：`.claude/` 整目录排除 → `.claude/*` + `!.claude/rules/`
- **全量规则入库**：从实际工作区同步全部 29 条规则（v1.0 仅含 10 条）

### 新增规则（19条，自v1.0以来）
#### Agent管理与故障恢复
- `agent-concurrency-fallback.md` — Agent 并发降级协议（429限流零等待切换）
- `agent-prompt-ironclad.md` — Agent Prompt 三要素铁律（目标/格式/停止条件）
- `subagent-strategy.md` — Sub-Agent 策略（何时用/不用/模型选择/故障恢复）

#### 信息搜索与纪律
- `search-decision-tree.md` — 搜索决策树（何时搜/搜多深/用什么工具）
- `lesson-auto-update.md` — 教训闭环自动更新（用户纠正→工作流自动修改）

#### Skill管理与路由
- `skill-auto-activation.md` v2.0 — 技能自动激活（三层路由+联动链+自我学习闭环）
- `skill-execution-discipline.md` — Skill 执行纪律（必读执行协议，不可跳过）
- `skill-logging-enforcement.md` — Skill 调用日志强制记录
- `skill-route-enforcement.md` — Skill 路由注册强制规则

#### 安全与运维深化
- `chinese-path-safety.md` — Windows 中文路径安全（禁Bash heredoc）
- `powershell-safety.md` — PowerShell 安全规则
- `pre-action-check.md` — 动手前检查门禁
- `git-recovery.md` — Git 检查点与恢复（删前commit+30秒恢复）
- `mcp-config-protocol.md` — MCP 配置协议四铁律

#### 架构与治理
- `competition-workspace-architecture.md` — 竞赛项目工作区架构
- `dual-write-protocol.md` — 双写协议（经验教训根级+模块级同步）
- `no-root-rules-dir.md` — 禁止根目录 rules/（防回退）
- `_MIGRATED-TO-RULES.md` — 规则迁移说明

### 优化
- `anti-info-overload.md` — 补充数据筛选和折叠技巧
- `no-blind-overwrite.md` — 补充 .gitignore 安全策略
- `script-safety-check.md` — 细化路径白名单

### 移除（太个人化/信息密度低）
- `identity-consistency.md` — 太泛泛，具体规则已覆盖
- `preference-memory.md` — 信息密度不足
- `voice-dna-auto-inject.md` — 个人文风，不适合通用框架

---

## v1.0.0 (2026-05-26)

### Added
- 10 cross-cutting engineering laws
- 6-stage project lifecycle SOP
- 3-layer memory architecture (with confidence labels)
- Anti-illusion audit (five-question check)
- Negative result archiving mechanism
- Memory candidate confirmation protocol
- Script safety check protocol
- Anti-information overload rules
- Boundary declaration rules
- Claude Code / Codex / Cursor / Aider / Gemini CLI adapters
- Chinese and English memory templates
"""

with open(os.path.join(REPO, "CHANGELOG.md"), "w", encoding="utf-8") as f:
    f.write(changelog)
print(f"[OK] CHANGELOG.md updated ({len(changelog)} chars)")

# ============================================================
# Phase 5: Update docs/philosophy.md
# ============================================================
print("\n=== Updating docs/philosophy.md ===")

philosophy = """# 设计哲学

## niuma-engine 不是什么

❌ 不是"又一个提示词模板"
❌ 不是"让 AI 变聪明"的魔法
❌ 不是闭着眼装上就能用的插件

**这是一个纪律框架。** 它不会让 AI 变聪明，但它会让 AI：
1. **少犯错** — 每个规则堵住一个已证实的事故模式
2. **犯了错能被抓住** — 防假象审计、证据分层、门禁文化
3. **同样的错不犯第二次** — 负结果归档、教训闭环、规则结晶

## 核心设计原则

### 1. 从事故中生长，不从设计中诞生
niuma-engine 的每一条规则，都对应至少一次真实事故。没有"我觉得应该有这条规则"——只有"这次事故后，必须加上这条规则"。

### 2. 按痛点安装，不按功能安装
用户不需要理解所有规则。只需要知道：我踩过什么坑 → 装对应的规则。

### 3. 纪律 > 技巧
提示词技巧在一周内过时。工程纪律在十年内有效。niuma-engine 追求的是后者。

### 4. 信息密度 > 信息量
每条规则文件都追求高信息密度：具体场景 + 具体禁止行为 + 具体触发条件。拒绝泛泛的"最佳实践"。

### 5. 负结果是一等公民
一条没被记录的死路，会被每个后续 Agent 重新踩一遍。负结果日志和正结果同等重要。

## v4.0 的核心洞察

v1.0 解决的是"单个 AI 如何像工程师一样工作"。
v4.0 解决的是"多个 AI Agent 如何像工程团队一样协作"。

规则从 10 条增长到 29 条，不是膨胀，是覆盖面的质变：
- **Agent 管理三件套**：prompt铁律 + 子agent策略 + 并发降级
- **Skill 生态治理**：创建必注册 + 调用必记录 + 执行协议不可跳过
- **搜索与信息纪律**：搜索决策树 + 教训闭环自动更新
- **安全纵深**：中文路径 + PowerShell + 脚本安全 + Git恢复

## 与 comemo 的关系

niuma-engine 不替代 comemo。comemo 管记忆存储，niuma-engine 管工程纪律。两者互补：
- 用 comemo 做记忆分层存储
- 用 niuma-engine 的记忆置信度标签 + 失效条件做可信度管理
- 用 niuma-engine 的负结果归档防止重复踩坑
"""

with open(os.path.join(REPO, "docs", "philosophy.md"), "w", encoding="utf-8") as f:
    f.write(philosophy)
print(f"[OK] docs/philosophy.md updated")

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*60}")
print(f"v4.0 upgrade complete!")
print(f"{'='*60}")
print(f"Rules: {len(rules)} files in .claude/rules/")
total_size = sum(get_rule_size(r) for r in rules)
print(f"Total rules size: {total_size:,} bytes")
print(f"README: updated")
print(f"CHANGELOG: updated (v4.0.0)")
print(f"docs/philosophy.md: updated")
print(f"\nReady for git commit and tag.")
