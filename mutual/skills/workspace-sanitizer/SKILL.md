---
name: workspace-sanitizer
description: |
  工作区深度结构清理器——存量工作区的根目录卫生、结构重组、归档统一、死链接修复。
  不是文档同步（那是 li-manage），不是新建脚手架（那是 scaffold-workspace），
  是"已有工作区越用越乱"这个问题的解药。
  触发词：工作区清理、根目录太乱、文件整理、结构重组、死链接修复、清理工作区、
  workspace cleanup、workspace sanitize、整理目录、目录结构优化、文件乱了
---

# Workspace Sanitizer — 工作区深度结构清理器

> 从 2026-06-22 mutual 工作区清理实战中提炼：45 项根目录 -> 21 项，
> 38 个垃圾文件清除 + 10 个错位目录归位 + 13 处死链接修复。
> 每次清理都是结构手术，不是文件搬家。

---

## 核心原则

**"乱"不是垃圾多，是职责不清。** 第一轮清垃圾（表面），第二轮清结构（根因）。

清理必须分两层：
1. **卫生层**：timestamp 碎片、0 字节文件、空目录——这些是垃圾，直接删
2. **结构层**：目录放在根目录但不属于根目录——这些是错位，需要归位

只做第一层 = 隔靴搔痒，用户下次还会说"还是很乱"。

---

## 与其他 Skill 的关系

| Skill | 管什么 | 本 Skill 补什么 |
|-------|--------|----------------|
| li-manage (neat-freak) | 会话结束后文档同步、知识库一致性 | 不管文件系统结构 |
| scaffold-workspace | 新建工作区时生成标准结构 | 不管存量工作区的清理 |
| storage-analyzer | 磁盘空间分析（哪些文件占空间） | 不管结构合理性 |
| **workspace-sanitizer** | **存量工作区的结构清理 + 死链接修复** | **补上"越用越乱"的能力缺口** |

典型调用链：
```
workspace-sanitizer（清理结构）
  -> li-manage（同步文档一致性）
  -> scaffold-workspace template（防止新建时复发）
```

---

## Phase 0：诊断（必做，不可跳过）

**目标**：量化"乱"的程度，决定是否需要清理。

### Step 0.1 根目录项数检查

```python
import os
ws = r"{工作区根路径}"
items = os.listdir(ws)
print(f"根目录项数: {len(items)}")
```

**门禁**：
- <= 15 项：健康，跳过清理
- 16-25 项：轻度，只做 Phase 1（卫生）
- > 25 项：重度，执行全流程

### Step 0.2 垃圾文件统计

扫描三类垃圾：
1. **timestamp 粘贴文件**：文件名以数字开头 + 含 "Pasted"（如 `1781088737437-Pasted-1.txt`）
2. **0 字节空文件**：排除 `.gitkeep`、`.gitignore`、`__init__.py`
3. **空目录**：无文件无子目录的目录

### Step 0.3 结构审计

检查根目录每个目录/文件的**职责归属**：

```
根目录该有什么？
  - 入口文件（CLAUDE.md, AGENT.md, runtime-snapshot.md 等）
  - 核心目录（memory/, outputs/, projects/, skills/, scripts/, SOPs/）
  - 隐藏目录（.claude/, .github/）

不该在根目录的？
  - 归档目录（应移到全局归档 E:\ai产出文件\牛马\归档\）
  - 临时目录（.tmp/、conversations/、drafts/）
  - 系统目录（unified-index/ -> _system/）
  - 旧版残留（自我进化/ -> self-evolution/）
  - 项目内部文件（在 projects/ 下不该溢出到根目录）
```

输出诊断报告：
```
=== {工作区名} 结构诊断 ===
根目录项数: {N}
垃圾文件: {timestamp} 个 timestamp + {empty} 个空文件 + {empty_dirs} 个空目录
结构问题: {misplaced} 个目录/文件错位
建议: {健康/轻度清理/重度清理}
```

---

## Phase 1：卫生清理（低风险，自主执行）

**目标**：清除垃圾文件，不改变结构。

### Step 1.1 归档垃圾

所有垃圾文件**先移到归档目录再删除**，不直接 rm：

```python
ARCHIVE = r"E:\ai产出文件\牛马\归档\{日期}-{工作区名}-sanitizer\"
# 移动 timestamp 文件、0 字节文件、空目录内容到归档
```

### Step 1.2 验证

- 归档目录文件数 = 预期垃圾数
- 工作区根目录无 timestamp/0字节文件残留

---

## Phase 2：结构重组（中风险，dry-run + 确认）

**目标**：把错位的目录移到正确位置。

### 铁律：必须先 dry-run 再执行

每个移动操作先打印：
```
WOULD MOVE: {源路径} -> {目标路径} (原因: {SRP/归档/命名统一})
```

用户确认后才执行。

### 标准移动模式

| 问题 | 源 | 目标 | 原因 |
|------|-----|------|------|
| 归档目录在根目录 | `{ws}/归档/` | `E:\ai产出文件\牛马\归档\` | 全局归档统一 |
| 临时文件过期 | `{ws}/.tmp/` | `归档/.tmp/` | .tmp 超 14 天 = 垃圾 |
| 对话记录在根目录 | `{ws}/conversations/` | `memory/conversations/` | SRP: 对话属于记忆 |
| 草稿在根目录 | `{ws}/drafts/` | `outputs/drafts/` | SRP: 草稿属于产出 |
| 旧版目录 | `{ws}/自我进化/` | 合并到 `self-evolution/` | 命名统一 |
| 系统目录在根目录 | `{ws}/unified-index/` | `_system/unified-index/` | SRP: 系统归系统 |
| 空交接目录 | `{ws}/handoffs/` | 删除（空目录） | 空目录 = 无用目录 |
| 项目壳子 | `{ws}/projects/proj-xxx/`（只有1-2个文件） | 归档 | 空项目 = 历史残留 |

### 每次移动后验证

```python
# 确认源目录已空/已移走
# 确认目标目录文件完整
# 用 os.path.getsize 对比总大小
```

---

## Phase 3：死链接扫描与修复（高风险，逐个确认）

**目标**：配置文件引用了已移走的路径 -> 修复为新路径。

### Step 3.1 扫描

在以下文件中搜索已移走的旧路径名：

**必须扫描的文件**：
1. `CLAUDE.md`、`AGENT.md`、`runtime-snapshot.md`
2. `.claude/rules/` 下所有 `.md`
3. `memory/` 下所有 `.md`（排除历史日期文件）
4. `SOPs/` 下所有文件
5. `skills/*/SKILL.md`（特别是 scaffold-workspace 的模板）
6. `skill-routing-table.json`
7. `workflow-inbox.md`、`artifact-registry.md`
8. `project-context/` 下所有文件
9. `cross-workspace-sync/shared-rules/` 下所有文件
10. `_system/` 下所有文件

**搜索关键词**（根据实际移走的目录调整）：
```
自我进化/  .tmp/  handoffs/  conversations/  归档/
unified-index/  文书文档/  skill-calls/  drafts/
```

### Step 3.2 分类

每个匹配分为三类：

| 类别 | 处理方式 | 示例 |
|------|---------|------|
| **配置引用**（指导行为的） | 必须修复 | scaffold 模板里建 `自我进化/` |
| **历史记录**（描述已发生的事） | 不动 | memory/2026-06-22.md 记录了清理过程 |
| **描述其他工作区** | 不动 | file-registry 描述创作区还有 `归档/` |

### Step 3.3 修复

对配置引用，用 Edit 精确替换：
- `自我进化/` -> `self-evolution/`
- `归档/`（工作区级）-> `E:\ai产出文件\牛马\归档\{日期}-{主题}\`（全局）
- `unified-index/` -> `_system/unified-index/`
- `handoffs/` -> 移除引用（已废弃）
- `conversations/` -> `memory/conversations/`

### Step 3.4 模板同步（防根因复发）

**关键**：如果 scaffold-workspace 的模板还教新工作区建旧结构，清理完还会复发。

检查并修复：
- `skills/scaffold-workspace/SKILL.md` 中的旧路径描述
- `skills/scaffold-workspace/templates/` 中的旧路径模板
- `cross-workspace-sync/shared-rules/` 中的旧路径规范

---

## Phase 4：验证与报告

### 验证清单

- [ ] 根目录项数 <= 25
- [ ] 零 timestamp 碎片
- [ ] 零 0 字节空文件（排除 .gitkeep 等）
- [ ] 归档目录不在工作区根目录
- [ ] `自我进化/` 已合并到 `self-evolution/`
- [ ] 配置文件中零旧路径引用（排除历史记录）
- [ ] scaffold 模板已同步更新

### 报告格式

```
=== {工作区名} 清理报告 ===

[卫生层]
  清除 timestamp 碎片: {N} 个
  清除 0 字节文件: {N} 个
  清除空目录: {N} 个

[结构层]
  归档旧版项目: {N} 个 -> E:\归档\{日期}\
  移动错位目录: {N} 个（列出每个）
  合并重复结构: {N} 个（如 自我进化/ -> self-evolution/）

[死链接层]
  扫描文件: {N} 个
  发现旧路径引用: {N} 处
  修复配置引用: {N} 处
  保留历史记录: {N} 处（不动）

[防复发]
  scaffold 模板已更新: {是/否}
  共享规则已更新: {是/否}

归档位置: E:\ai产出文件\牛马\归档\{日期}-{工作区名}-sanitizer\
```

---

## 铁律

1. **归档优先**：所有被移走/删除的文件先进归档，不直接 rm
2. **dry-run 必须**：Phase 2 和 Phase 3 必须先展示变更清单，用户确认后才执行
3. **历史不动**：memory/ 和 outputs/ 中的历史记录是事实，即使引用旧路径也不改
4. **模板同步**：修完工作区后必须检查 scaffold 模板，防止下一个工作区复发
5. **根因优先**：如果"乱"的根因是模板/规则/共享规范，必须修根因，不能只清表面

---

## 认知科学支撑

| 认知机制 | 来源 | 在本 Skill 中的应用 |
|---------|------|---------------------|
| **破窗效应** | 010-思考快与慢 | 一个 timestamp 碎片不清理 -> 更多碎片堆积 -> "反正已经乱了" -> 彻底放弃维护 |
| **SRP（单一职责）** | 005-系统之美 | 目录放错位置 = 职责混乱 -> 每次找文件都要多想一步 -> 认知负荷累积 |
| **外部化认知** | 022-认知神经科学 | 清晰的目录结构 = AI 的"空间记忆外部化" -> 减少"文件去哪了"的搜索成本 |
| **预防优于治疗** | 004-穷查理宝典 | 修 scaffold 模板 = 从源头预防 -> 比每次清理更高效 |
| **习惯回路** | 009-习惯的力量 | 定期清理触发器（根目录 > 25 项）-> 自动进入清理流程 -> 形成维护习惯 |
