# li- 系列 Skill 联动规则（强制读取）

> **铁律**：本文件在每个 li- skill 被调用时必须 Read。不读 = 跳过联动 = 产出不完整。
> **位置**：每个 li- skill 的 `references/skill-linkage.md`（同一文件，各放一份）
> **更新**：发现新联动关系时，更新本文件并同步到所有 li- skill。

---

## 一、联动链定义

### 链 1：Skill 生命周期（最高优先级）

```
触发词："拆分/融合/创建/审核/弃用/skill"

li-skillfusion（拆分/融合）
  ├─→ 拆分后：检查新 skill 是否已在路由表注册
  │     └─ 未注册 → li-skillcreate（注册路由）
  ├─→ 拆分后：li-skills-mgmt（质量审核）
  └─→ 拆分记录 → li-improve（记录教训）

li-skillcreate（创建新 skill）
  ├─→ 创建后：必须更新 skill-routing-table.json（注册触发词）
  ├─→ 创建后：li-skills-mgmt（质量审核）
  └─→ 创建记录 → li-improve（记录教训）

li-skills-mgmt（审核/弃用）
  ├─→ 审核发现：问题 → li-improve（改进）
  ├─→ 弃用后：从路由表移除
  └─→ 审核记录 → li-memory（记忆归档）
```

### 链 2：改进闭环（核心学习链）

```
触发词："教训/改进/进化/踩坑/复盘"

li-improve（教训记录）
  ├─→ 教训涉及 skill → li-skillfusion（改 skill 结构）
  ├─→ 教训涉及 SOP → 直接 Edit SOP 迭代日志
  ├─→ 教训涉及规则 → 直接 Edit .claude/rules/
  └─→ 教训涉及路由 → 更新 skill-routing-table.json

li-diagnose（诊断）
  ├─→ 发现系统性问题 → li-improve（记录教训）
  ├─→ 发现 skill 问题 → li-skills-mgmt（审核）
  └─→ 发现配置问题 → li-infra（修复配置）
```

### 链 3：知识沉淀（调研→分析→记录）

```
触发词："调研/分析/研究/学习"

li-research（深度调研）
  ├─→ 调研完成 → li-analyze（深度分析）
  ├─→ 调研发现方法 → li-memory（记录到方法论库）
  └─→ 调研结果 → li-competition/li-hardware（应用到项目）

li-analyze（分析）
  ├─→ 分析完成 → li-memory（记录分析结果）
  └─→ 分析发现改进点 → li-improve（记录教训）
```

### 链 4：内容创作（素材→创作→分发）

```
触发词："写/创作/内容/小红书/公众号"

li-research（素材调研）
  └─→ 调研完成 → li-xhs/li-wechat（内容创作）

li-xhs / li-wechat（内容创作）
  ├─→ 创作完成 → li-image（配图）
  └─→ 创作记录 → li-memory（记录爆款模式）
```

---

## 二、联动执行规则

### 强制检查（每个 li- skill 执行完后必做）

```
Step 1: 执行本 skill 核心任务
Step 2: 检查联动链（本文件）
Step 3: 有联动 → 立即调用下一个 skill
Step 4: 无联动 → 正常结束
Step 5: 记录联动执行情况到 skill audit
```

### 联动触发条件

| 条件 | 触发 | 说明 |
|------|------|------|
| 拆分/创建了新 skill | li-skillcreate + li-skills-mgmt | 新 skill 必须注册+审核 |
| 发现了系统性问题 | li-improve | 问题必须记录+回写 |
| 调研完成了 | li-analyze | 调研结果需要深度分析 |
| 用户纠正了 | li-improve | 纠正必须记录教训 |
| skill 执行失败 | li-diagnose | 失败必须诊断根因 |
| 修改了全局配置 | li-sync | 配置变更需要同步 |

### 联动中断条件

| 条件 | 动作 | 说明 |
|------|------|------|
| 下一个 skill 不存在 | 跳过，记录到 audit | 不要手动实现 skill 功能 |
| 下一个 skill 执行失败 | 记录失败原因，继续 | 不要重试（R19 协议） |
| 用户明确说"不要" | 尊重用户，跳过联动 | 用户意图优先于联动规则 |
| 上下文已接近压缩阈值 | 写 checkpoint，开新对话 | 不要在压缩边缘继续 |

---

## 三、与 CLAUDE.md 铁律的关系

| 铁律 | 在联动中的应用 |
|------|---------------|
| F1 技能审计 | 联动执行情况必须记录在审计日志 |
| F6 教训回写 | li-improve 的教训必须流向对应 skill/SOP |
| F11 Skill 链定 | 创建前 Glob 检查，已存在则 Edit |
| F14 Skill 生命周期 | 拆分/融合/创建必须通过对应 skill |

---

## 四、常见联动场景速查

| 用户说 | 主 skill | 联动 skill | 联动动作 |
|--------|---------|-----------|---------|
| "拆分这个 skill" | li-skillfusion | li-skillcreate | 注册新 skill 到路由表 |
| "创建一个新 skill" | li-skillcreate | li-skills-mgmt | 质量审核 |
| "我发现了一个教训" | li-improve | 对应 skill | 教训回写到 skill/SOP |
| "帮我调研一下" | li-research | li-analyze | 调研结果深度分析 |
| "检查一下系统" | li-diagnose | li-improve | 诊断结果记录教训 |
| "同步一下规则" | li-sync | li-infra | 配置同步+验证 |
| "这个竞赛怎么做" | li-competition | li-research | 竞赛调研+分析 |

---

> 版本：v1.0
> 创建：2026-06-13
> 维护：每次发现新联动关系时更新本文件
