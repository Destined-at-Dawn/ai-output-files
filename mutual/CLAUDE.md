# ⛔ 启动序列（每次对话强制，不可跳过）

**根目录**：`${WORKSPACE_ROOT}`

| Step | 操作 | 触发条件 |
|------|------|----------|
| 0 | Read `runtime-snapshot.md` | 每次必读 |
| 1 | Read `memory/long-term.md` | 首次 / 纠正≥2次 / 新项目 |
| 2 | Read `memory/{今日}.md` | 每日首次 |
| 3 | Read `self-evolution/evolution-calendar.md` | 每次必读；匹配⏳→先执行进化任务 |
| 4.5 | 加载 `skill-routing-table.json` | 每次必读 |
| 6 | 检查 `.claude/session-checkpoint.md` | 有未完成任务则恢复 |

> **⚡ 快模式**：消息精确含 `快！`（快+全角感叹号）→ 跳过所有Step直接处理。高风险操作例外（仍需读 long-term.md）。

---

# Project Rules

## Think Before Act
新问题必须先研究再动手。禁止"我觉得"代替最佳实践。
→ 详见 `.claude/rules/think-before-act.md`

## 自动进化检查（每次任务前）
读 evolution-calendar.md → 匹配⏳ → 告知用户 → 执行 Phase 1/2 → 更新✅ → 继续用户任务。
→ 详见 `skills/auto-evolution/SKILL.md`

## 🌬️ 技能自动激活
用户说的是需求，不是技能名。收到消息→扫描路由表→匹配→直接调用（不问）→未匹配→原生处理。路由失败=我的问题。
→ 详见 `.claude/rules/skill-auto-activation.md`

## No Blind Overwrite（CRITICAL）
写已存在文件前必须先 Read。能用 Edit 就不用 Write。
→ 详见 `.claude/rules/no-blind-overwrite.md`

## Script Safety Check（CRITICAL）
流程：写脚本→安全检查→dry-run→展示→确认→执行→验证。删除精确到文件，禁止目录级删除。
→ 详见 `.claude/rules/script-safety-check.md`

## PowerShell（CRITICAL）
- 禁止在 inline `powershell -Command` 中使用 `$_`
- **中文路径铁律**：含中文路径一律用 Python 脚本，禁止 Bash heredoc
→ 详见 `.claude/rules/powershell-safety.md` `.claude/rules/chinese-path-safety.md`

## Git Workflow（Agent Coding）
- Atomic Commit + Conventional Commits + Agent Trailer（Task/Decision/Model/Limitation）
- 分支命名：`agent/<task-id>-<description>`；禁止直推 main/master
- 长任务（>15min）打 checkpoint commit；PR 等待人工审查
→ 详见 `AGENT.md` `outputs/sop-git-workflow.md`

## 上下文压缩（Hook驱动）
PreCompact→`pre-compact.py`写检查点；SessionStart(compact)→`on-compact.py`恢复上下文。
长任务每30min主动写磁盘。
→ 详见 `skills/context-compression/SKILL.md`

## 🌐 跨工作区感知（mutual = 管理/优化区）
- 全局地图：`${AI_ROOT}\知识中枢\00-注册表\工作区注册表.md`
- 共享规则：`${AI_ROOT}\知识中枢\02-共享规则\`
- 新建目录/文件前先查注册表

## 🔍 地图优先（R13）
查找顺序：MCP工具 → 注册表/SOP索引 → memory → 精确Read → grep/Agent（最后手段）。连续grep≥3次未找到→停下查地图。

## 🔧 MCP 配置（硬约束）
- 配置路径：`~/.newmax/.mcp.json`（不是 `~/.mcp.json`）
- 命令格式：直接调用 npx/python，不用 `cmd /c`
- markitdown：用 `runpy.run_module`
- 写后必须 JSON验证+文件确认+告知重启
→ 详见 `.claude/rules/mcp-config-protocol.md`

## 📁 R16 根目录优先
写入规则：记忆→`memory/`；产出→`outputs/`；约束→只写差异项；写前检查根目录是否已有同类。
项目文件夹禁止放：全局约束/SOP/记忆/技能规则/统一索引。
→ 详见 `知识中枢/02-共享规则/16-root-authority-architecture.md`

## ⛔ 防回退铁律
- ❌ 禁止在任何位置创建 `rules/` 目录（无 `.claude/` 前缀）
- 唯一规则存放位置：`.claude/rules/`

## 📦 跨区工作流三件套

| 文件 | 路径 | 功能 |
|------|------|------|
| 项目上下文卡 | `project-context/PROJECT-xxx.md` | 跨区项目导航（8字段） |
| 产出注册表 | `artifact-registry.md` | 跨区可复用产出登记 |
| 改进收件箱 | `workflow-inbox.md` | 优化想法暂存（每周清理） |

三条铁律：跨区项目先建项目卡；重要产出必须登记；长期记忆走候选确认流程。

---

# Compact Instructions

## li-intent 意图路由
URL/文件/链接 → 自动激活 li-intent → Phase 0提取 → Phase 1意图判断（7种）→ Phase 2 SOP匹配 → Phase 3执行 → Phase 4自学习。
→ 详见 `~/.newmax/skills/li-intent/SKILL.md`

## 保护清单（压缩时永不丢失）
1. 用户最新需求（原文）
2. 所有修改的文件绝对路径
3. Source: path#line 引用
4. 关键决策及理由
5. 错误根因和修复方案
6. 任务进度和下一步
7. 用户纠正原文

## 可丢弃
完整工具输出 / 中间推理链 / 逐字文件内容 / 重复错误消息 / Agent子对话

## 压缩后恢复
1. 重读 CLAUDE.md + .claude/rules/（自动）
2. 主动重读 `memory/long-term.md` + `memory/{today}.md`
3. 检查 session-checkpoint.md 未完成任务

---

## 🔴 Hermes 记忆中枢协作

创建/优化 Skill 或 SOP 前先读：
- `知识中枢/01-工作区记忆/hermes-memory/facts/atomic-facts.md`
- `知识中枢/01-工作区记忆/hermes-memory/state-tracking/cross-tool-state.md`

写入规则：❌ 禁止写 `hermes-memory/`；交接内容写 `知识中枢/05-每日记忆/YYYY-MM-DD-{工具}-{主题}.md`

## 🔴 动手前检查门禁

| 任务类型 | 先做什么 |
|----------|---------|
| 写脚本/代码 | 查 `script-library/INDEX.md` + li-script |
| 生成图片 | 确认工具（脚本 vs 生成器） |
| 多图任务 | 锁定一致性参数 |
| 模板填充 | 确认只填内容不改结构 |

收尾验证：已检索skill/SOP ✓ 工具正确 ✓ 边界确认 ✓ 交付自检 ✓
→ 详见 `.claude/rules/pre-action-check.md`
