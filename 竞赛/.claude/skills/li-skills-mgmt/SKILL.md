---
name: li-skills-mgmt
version: "1.0"
description: li系列 · Skill生命周期管理（创建/审核/融合/弃用）
---


> **必读（执行前必须 Read）**：`references/skill-linkage.md` — li- 系列联动规则。不读 = 跳过联动 = 产出不完整。500 万 token 上下文中本文件可能被压缩，但 references/ 不会被压缩。


## [LIGHTNING] 执行协议（强制 - 禁止跳过）

> **本段是执行约束，不是参考建议。违反 = 产出质量不可信。**

### [RED] 必读（执行前必须读取，不可跳过）

- 执行前**必须** `Read references/quality-checklist.md` - 不读 = 不了解核心方法论 = 产出不合格

### [STOP] 门禁

- Phase 执行前：确认已读取 references/quality-checklist.md。未读 -> **禁止继续**
- 输出结论前：确认有 evidence path (Source: path#line)。无证据 -> **禁止声称**
- 跳过本协议 = 违反工程法则 8（门禁不可跳过）


# li-skills-mgmt: Skill creation, vetting, and lifecycle management

> li-系列协调 skill。自动触发，不需要用户指定。

## 触发场景
- 创建skill
- create skill
- 新建技能
- 技能管理
- skill审核
- skill vetting
- 技能融合
- 技能拆分
- 重构skill
- 优化skill
- skill review
- skill质量

## 委托给的底层 skill（当前架构）
- li-skillcreate（从零创建/迭代）
- li-skillfusion（融合/拆分/弃用/生命周期）
- li-bestskill（外部搜索参考）


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

## Phase 0: 需求消解
- 创建新 skill？优化已有？融合多个？
- 目标场景和用户？
- 是否有类似 skill 可复用？

## Phase 1: 创建/优化
- 创建: li-skillcreate v2.0 流程（搜外部→骨架→内容→质量门禁→路由注册）
- 优化: 读当前 SKILL.md → 识别缺口 → 定向补充
- 融合: 读多个 SKILL.md → 识别重叠和互补 → 合并

## Phase 2: 质量门禁（15项强制检查）
- 主文件 ≤300 行
- 有案例库/反模式/联动技能
- golden_rules ≥500B
- 路由已注册 + 全工作区同步

## Phase 3: 生命周期
- 运行中: 收集使用反馈 → 优化
- 弃用: 创建 DEPRECATED.md → 清理路由
- 提取: 多次重复使用 → 独立 skill

## 案例库

### 案例 1: li- 系列大规模审计
- **场景**: 44 个 li- skill 需要全量质量审计
- **做法**: Phase 1 扫描所有目录（SKILL.md行数/golden_rules/eval.json/references） → Phase 2 生成审计报告 → Phase 3 分类（Tier S/A/B/C）
- **结果**: 发现 9 个空壳 skill + 40 个活跃，生成可操作修复清单
- **来源**: mutual 工作区，2026-06-11

### 案例 2: 路由表去重治理
- **场景**: 35 个跨 skill 重复触发词导致路由冲突
- **做法**: Phase 1 grep 全路由表找出重复 → Phase 2 仲裁（同skill合并/跨skill仲裁） → Phase 3 验证
- **结果**: 35→0 重复，路由从 113→109 条
- **来源**: mutual 工作区，2026-06-08

### 案例 3: 弃用 skill 残留清理
- **场景**: 6 个旧 skill 已创建 DEPRECATED.md 但路由表仍有残留
- **做法**: Phase 2 列表视图 → 标记每个 skill 的状态 → 生成清理计划
- **结果**: 清除 li-evolve/li-skillcraft 等已弃用路由
- **来源**: mutual 工作区，2026-06

## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|---------|
| A1 | 批量创建 skill 不注册路由 | skill 存在但永远不被触发 | 创建后立即更新路由表 + 全工作区同步 |
| A2 | 声称"达标"但案例是编造的 | 用户信任崩塌 | 没有真实使用的 skill 标注"待验证" |
| A3 | 用行数少当弃用理由 | 7行的zoom-out有独立价值，110行的workflow也有 | 按功能价值判断，不按行数 |
| A4 | 改第三方仓库的文件 | 数据事故 | 第三方仓库 = 只读 |
| A5 | 只扫顶层目录 | 深层嵌套的工作区被漏掉 | os.walk() 全递归扫描 |
| A6 | 删文件不先归档 | 无法恢复 | 删前 git checkpoint + 归档目录备份 |
| A7 | golden_rules 写模板占位符 | 10个skill的golden_rules是同一段废话 | 每个skill的规则必须领域特化 |

## 联动技能
- **li-skillcreate**: 核心创建流程
- **li-skillfusion**: 融合/拆分
- **li-manage**: 生命周期管理
- **li-bestskill**: 搜索外部参考
- **li-sync**: 跨工作区同步

| li- | 联动方式 | 触发时机 |
|-----|---------|---------|
| li-manage | 全生命周期编排 | skill 状态变更 |
| li-skillcreate | 创建新 skill | 发现能力缺口 |
| li-skillfusion | 融合/拆分 skill | 功能重叠或过度膨胀 |
| li-bestskill | 跨平台搜索 | 造 skill 前先搜外部 |
## 设计哲学
- **不需要用户指定用哪个底层 skill** — 本 skill 自动选择最合适的
- **协调优先** — 底层 skill 负责能力，本 skill 负责编排和上下文
- **自进化** — 每次使用后收集反馈，优化 golden_rules
- **Progressive Disclosure** — 主文件 ≤300 行，详细内容在 references/

## 禁忌

- **禁止**：清理旧版本不备份——归档目录 > 30 天后才删除
- **禁止**：不通知用户就删除 skill——DEPRECATED 标记 → 30 天 → 再删
- **禁止**：版本号跳跃——从 v1.0 直接到 v3.0，跳过了 v2.0 的验证

## 条件下一步

- 版本管理完成 → 调用 li-sync 同步 → 更新路由表
