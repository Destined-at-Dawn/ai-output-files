# Auto-Evolution Skill

> 被 CLAUDE.md "自动进化检查"段落引用。每次对话启动时检查 `self-evolution/evolution-calendar.md`。

## Phase 1：小改（校准/补漏）

**触发**：日历中标注"小改"的任务。
**动作**：
1. 读 `self-evolution/evolution-calendar.md` → 确认今天待执行任务
2. 执行具体改进操作（更新规则、修正路径、补充缺失文件）
3. 操作完成后 Read 验证
4. 更新日历状态为 ✅已执行

## Phase 2：大改（重构/升级）

**触发**：日历中标注"大改"的任务。
**动作**：
1. 读 `self-evolution/evolution-calendar.md` → 确认全量任务范围
2. 执行结构化重构（如 28 轮迭代、跨工作区同步）
3. 每个阶段完成后 Read 验证 + 写今日记忆
4. 更新日历状态为 ✅已执行

## 进化任务优先级

高于所有其他 auto task（Daily Git Health Report、Daily Ecosystem Audit 等）。

## 维护规则

- 新增进化任务 → Edit 追加到 `evolution-calendar.md`
- 完成任务 → 将 ⏳ 改为 ✅已执行
- 跨工作区任务 → 同步更新所有受影响工作区的日历
