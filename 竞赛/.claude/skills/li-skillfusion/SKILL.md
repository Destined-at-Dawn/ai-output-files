---
name: li-skillfusion
description: >
  技能融合器——技能的融合、拆分、微技能创建、生命周期管理。
  不同工作区需要不同粒度的技能：有些需要 1/3 个技能，有些需要两个技能合并。
  本 Skill 提供统一的规范，让所有技能操作（创建/融合/拆分/软删除）都在标准框架下进行。
  每次操作必须有记录，即使要删除也是加 DEPRECATED 文件而非删除 SKILL.md。
  触发词：融合技能/合并skill/拆分技能/技能拆分/微技能/小技能/skillfusion/技能融合/
  弃用技能/废弃skill/软删除/技能生命周期/技能管理/技能整理。
---

## [LIGHTNING] 执行协议（强制 - 禁止跳过）

> **执行约束（非建议）。** **必读（必须 Read）**: `references/skill-linkage.md`（li- 联动规则，500万token上下文不压缩） | `references/fusion-templates.md` | `references/split-templates.md` | `references/deprecation-templates.md` | `references/dependency-analysis.md` | `references/micro-skill-spec.md` | `references/lifecycle-log-format.md`。无 Source = 禁止声称。跳过 = 违反法则8。Phase 执行前确认已 Read 所有 references/ 必读文件，未读 = 禁止继续。
> **按需**: `references/split-templates.md` | `references/deprecation-templates.md` | `references/dependency-analysis.md` | `references/micro-skill-spec.md` | `references/lifecycle-log-format.md`


# li-skillfusion：技能融合器

> 「如无必要，勿增实体。」——奥卡姆剃刀
> 但当实体确实必要时，它应该被精确地切割、融合、归档，而不是粗暴地删除。

---

## 设计哲学

1. **真源+分发**：任何技能只维护一份真源，多工作区通过引用/链接分发，不复制。
2. **软删除 > 硬删除**：弃用 = 添加 `DEPRECATED.md`，SKILL.md 永不删除。
3. **每次操作必须有记录**：融合/拆分/创建/弃用都写入 `lifecycle-log.md`。
4. **工作区隔离**：微技能通过 `.workspace-only` 标记，不污染全局路由。
5. **统一规范**：命名、目录结构、版本号、记录格式遵循同一套标准。

---

## 理论锚点

| # | 理论 | 应用 | 来源 |
|---|------|------|------|
| T1 | 双系统理论 | 快速路由 vs 深度分析 | 《思考，快与慢》 |
| T2 | 认知负荷理论 | 主文件<=300行 | 《认知负荷理论》 |
| T3 | WYSIATI | AI只看到用户说的 | 《思考，快与慢》 |
| T4 | 锚定效应 | 首次结果影响后续判断 | 《思考，快与慢》 |
| T5 | 奥卡姆剃刀 | 最简方案优先 | 《精要主义》 |
| T6 | 刻意练习 | 迭代必须有实质差异 | 《刻意练习》 |
| T7 | 反脆弱 | 负结果归档 | 《反脆弱》 |
| T8 | 间隔效应 | 定期复习有效 | 《认知天性》 |
| T9 | 损失厌恶 | 先备份再操作 | 《思考，快与慢》 |
| T10 | 第一性原理 | 先问为什么 | 《第一性原理》 |
| T11 | 费曼检验 | 简单话解释 | 《费曼学习法》 |
| T12 | 预验尸 | 假设已失败倒推 | 《超越智商》 |

## Phase 0：需求判断 + 依赖分析

| 类型 | 触发场景 | 走哪个 Phase |
|------|---------|-------------|
| 融合 | "A 技能和 B 技能功能重叠，合并" | Phase 1 |
| 拆分 | "这个技能太大了，只要其中 1/3" | Phase 2 |
| 微技能 | "这个工作区需要一个专用的小技能" | Phase 3 |
| 软删除 | "这个技能不用了" / "弃用" | Phase 4 |
| 生命周期查询 | "这个技能的历史" / "谁创建的" | Phase 5 |
| 定制 | "这个功能在xx区用不到" | Phase 6 |

### 依赖分析（每次操作前必做）

读取目标 SKILL.md → 扫描路由表 → 扫描其他 skill 引用 → 检查使用频率 → 输出依赖图 + 风险评估。

> 详细流程、风险判定标准、扫描命令：见 `references/dependency-analysis.md`

---

## Phase 1：技能融合

**触发**：功能重叠 ≥ 50% / 用户说"合并""融合" / li-manage 标记"重复组"

**流程**：
```
1. 读取两个 SKILL.md 完整内容
2. 功能矩阵对比（保留/删除/合并）
3. 确定融合后结构：保留核心 + 去重 + 合并触发词 + 统一哲学
4. 写入新 SKILL.md
5. 为两个原技能添加 DEPRECATED.md（弃用原因 + 指向新技能）
6. 更新 lifecycle-log.md
7. 更新路由表（合并触发词）
8. Write 后 Read 验证
```

**命名**：有主次 → 保留主技能名；平等 → 新名称。版本 = `max(A, B) + 0.1`

> 记录格式、功能矩阵模板、检查清单：见 `references/fusion-templates.md`

---

## Phase 2：技能拆分

**触发**：SKILL.md > 500 行且用户只需部分 / 用户说"只要 XX 功能" / li-manage 标记"建议拆分"

**流程**：
```
1. 读取原 SKILL.md 完整内容
2. 识别可拆分模块边界（通常以 Phase/Flow 为单位）
3. 确定保留部分和提取部分
4. 写入新微技能 SKILL.md（工作区专用 → 添加 .workspace-only）
5. 更新原 SKILL.md：移除已拆分内容 + 添加"引用"段
6. 更新 lifecycle-log.md
7. Write 后 Read 验证
```

**命名**：`{原技能名}-{模块名}`，新技能从 v1.0 开始。

> 模块边界识别、引用段模板、检查清单：见 `references/split-templates.md`

---

## Phase 3：微技能创建

**触发**：某工作区需要专用小功能 / 不需要全局技能完整功能

**规范**：
- 目录：`~/.newmax/skills/{workspace}-{功能名}/`
- 必须包含：`SKILL.md`（< 150 行）+ `.workspace-only` 空文件
- SKILL.md 头部标注 `workspace_only: true` 和 `parent_skill`

> 完整目录结构、SKILL.md 模板、路由隔离机制、命名规范：见 `references/micro-skill-spec.md`

---

## Phase 4：软删除（弃用）

**铁律**：永远不删除 SKILL.md 文件。弃用 = 添加 DEPRECATED.md + 更新路由。

**流程**：
```
1. 确认弃用原因（被替代 / 已合并 / 不再需要）
2. 创建 DEPRECATED.md（弃用日期 + 原因 + 替代方案 + 迁移指南）
3. 路由表中触发词标注 deprecated（不物理删除）
4. 更新 lifecycle-log.md
5. 如有替代技能 → 更新其 _meta.json 继承关系
```

**恢复**：删除 DEPRECATED.md → 恢复路由 → 记录到 lifecycle-log.md。

> DEPRECATED.md 模板、恢复流程、检查清单：见 `references/deprecation-templates.md`

---

## Phase 5：生命周期查询

| 查询意图 | 操作 |
|---------|------|
| "这个技能的历史" | 读取 lifecycle-log.md，搜索该技能名 |
| "最近的技能操作" | 读取 lifecycle-log.md 最后 10 条 |
| "哪些技能被弃用了" | 搜索所有 DEPRECATED.md |
| "哪些技能是从其他技能拆分的" | 搜索 _meta.json 的 parent_skill 字段 |
| "微技能列表" | 搜索所有 .workspace-only 文件 |

> lifecycle-log.md 完整格式：见 `references/lifecycle-log-format.md`

---

## Phase 6：工作区定制

**触发**：用户说"这个功能在xx区用不到" / 某工作区只需部分能力

**流程**：
```
1. 读取目标 skill 的 SKILL.md
2. 读取目标工作区的 CLAUDE.md（了解约束）
3. 识别可裁剪功能（不影响核心流程的部分）
4. 创建工作区特化版（头部标注源 skill + 裁剪原因）
5. 更新 lifecycle-log.md
```

**铁律**：不能移除安全检查模块；不能移除边界声明；头部必须标注源 skill。

---

## 统一规范

### 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 全局技能 | `kebab-case` | `li-bestskill` |
| 微技能 | `{workspace}-{功能}` | `创作-文风检查` |
| 融合技能 | `li-{功能}` | `li-skillfusion` |
| 弃用标记 | `DEPRECATED.md` | 在技能目录根 |

### 版本号规则

| 操作 | 版本变化 | 示例 |
|------|---------|------|
| 小改（修 bug/加触发词） | +0.1 | v1.0 → v1.1 |
| 中改（加新 Phase/重构） | +1.0 | v1.1 → v2.0 |
| 融合 | max(两版本) + 0.1 | v1.0 + v2.0 → v2.1 |
| 拆分 | 新技能从 v1.0 开始 | — |

### 目录结构标准

```
{skill-name}/
├── SKILL.md          ← 必须，< 500 行
├── _meta.json        ← 推荐，元数据
├── DEPRECATED.md     ← 弃用时添加
├── .workspace-only   ← 微技能标记
├── lifecycle-log.md  ← 推荐，操作记录
├── references/       ← 按需，详细参考
└── templates/        ← 按需，模板文件
```

---

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| **li-skillcreate** | 上游——创建新技能用 li-skillcreate，本 Skill 管后续生命周期 |
| **li-bestskill** | 上游——发现的外部技能可能需要融合/拆分后才能用 |
| **li-manage** | 数据源——技能健康度诊断（Flow E）提供融合/拆分/弃用的决策依据 |
| **li-skillfusion** | 本 Skill（技能融合/拆分/弃用/生命周期管理） |
| **li-improve** v3.0 | 记录——技能操作过程中的教训由 li-improve 记录 |

---

## 禁止行为

- 硬删除 SKILL.md（必须软删除）
- 不写 lifecycle-log.md 就做操作
- 融合后不更新路由表
- 微技能没有 .workspace-only 标记
- 不做 Write 后 Read 验证就声称完成

---

## 变更记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-06-07 | v1.0 | 初版。5 个 Phase：融合/拆分/微技能/软删除/生命周期查询。统一规范。 |
| 2026-06-07 | v1.1 | 整合 li-skillfusion：Phase 0 新增依赖分析，新增 Phase 6 工作区定制。 |
| 2026-06-08 | v1.2 | Progressive Disclosure 重构：详细模板/规范移至 references/，主文件精简至 ≤300 行。 |

## 反模式

| 反模式 | 后果 | 正确做法 |
|--------|------|---------|
| 跳过Phase 0直接执行 | 输出不符合用户意图 | Phase 0消解不可跳过 |
| 不读references/直接写 | 输出质量低、缺少理论支撑 | Progressive Disclosure——按需加载reference |
| 输出后不记录反馈 | 同样的错误重复犯 | 任何用户纠正写入golden_rules.md |
| 和其他li-skill功能重叠 | 用户困惑该触发哪个 | 检查联动技能章节确认职责边界 |
| 不更新skill-routing-table.json | skill文件存在但不被触发 | 创建/修改后立即更新路由+同步工作区 |

## 联动技能

- **li-skillcreate, li-manage, li-bestskill, li-research**
- 联动方式：上游skill决定何时调用本skill，本skill专注核心能力
- 联动触发条件：上游skill的Phase中明确写了调用本skill的步骤
- 联动验证：联动成功后由li-memory记录事实，li-improve记录教训

## 注意事项

1. Progressive Disclosure——主文件≤300行，详细内容在references/
2. 每次修改后必须更新skill-routing-table.json并同步所有工作区
3. 用户反馈（"好"或"不好"）必须写入golden_rules.md
4. 本skill的触发词必须和其他li-skill正交——不抢别人的触发词
5. 引用百大认知书籍时标注书名+编号，不空谈

## 案例库

### 案例 1：Self-Improving → li-improve 融合
**场景**：self-improving v3.5（286行）和 li-evolve v1.1（668行）并存，功能重叠
**方法**：保留 self-improving 的 Progressive Disclosure 架构 + 吸收 li-evolve 的 hook/递归度/提取 → li-improve v4.0（251行）
**结果**：2 个 skill → 1 个，主文件更精简（251 < 286），功能更强
**教训**：融合不是堆叠，是架构升级

### 案例 2：li-content + li-analyze 合并
**场景**：两个 skill 都做内容分析，触发词冲突
**方法**：li-content 的内容诊断能力融入 li-analyze 的 Mode B
**结果**：触发词冲突消除，li-analyze 成为内容分析统一入口
**教训**：功能重叠 > 50% 就该合并

### 案例 3：li-migrate + li-redesign + li-scaffold 三合一
**场景**：三个工作区操作 skill，骨架几乎一样
**方法**：提取公共 Phase 骨架 + 三种模式（迁移/重构/搭建）
**结果**：3 个 skill → li-workspace（三模式引擎）
**教训**：骨架一样的 skill 不需要各自独立