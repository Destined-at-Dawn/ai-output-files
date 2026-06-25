# Auto-Evolution Skill v2

> 被 CLAUDE.md "自动进化检查"段落引用。每次对话启动时检查 `self-evolution/evolution-calendar.md`。
> v2: 增加评估闭环 + 量化评分 + 反馈循环（基于 MindStudio li-improve + EvoAgentX）

## Phase 1：小改（校准/补漏）

**触发**：日历中标注"小改"的任务。
**动作**：
1. 读 `self-evolution/evolution-calendar.md` → 确认今天待执行任务
2. 执行具体改进操作（更新规则、修正路径、补充缺失文件）
3. 操作完成后 Read 验证
4. 运行 `eval.json` 中的相关断言验证
5. 更新日历状态为 ✅已执行

## Phase 2：大改（重构/升级）

**触发**：日历中标注"大改"的任务。
**动作**：
1. 读 `self-evolution/evolution-calendar.md` → 确认全量任务范围
2. 执行结构化重构（如 28 轮迭代、跨工作区同步）
3. 每个阶段完成后 Read 验证 + 写今日记忆
4. 运行全量 `eval.json` 断言验证
5. 更新日历状态为 ✅已执行

## Phase 3：评估闭环（v2 新增）

**触发**：每次进化完成后自动执行。
**动作**：
1. 读 `skills/auto-evolution/eval.json`
2. 对每个 evaluation 运行 test_method
3. 更新 last_result / last_tested / pass_count / fail_count
4. 计算 pass_rate，写入今日记忆
5. 如果 pass_rate < 0.8 → 标记为"需要人工审查"
6. 如果 fail_count > 3 → 自动创建修复任务

## 进化任务优先级

高于所有其他 auto task（Daily Git Health Report、Daily Ecosystem Audit 等）。

## 量化指标（v2 新增）

每次进化记录以下指标到 `memory/metrics/{date}-evolution.json`：
```json
{
  "date": "2026-05-28",
  "phase": "Phase 1",
  "eval_pass_rate": 0.75,
  "rules_changed": 2,
  "lessons_added": 1,
  "skills_improved": 0,
  "duration_minutes": 15,
  "token_cost": 5000
}
```

## 反馈循环（v2 新增）

基于 MindStudio 的三文件架构：
- **skill.md**（本文件）= 流程定义
- **eval.json** = 二元断言（Pass/Fail，可跨轮比较）
- **long-term.md** = 持久记忆（= MindStudio 的 learnings.md）

循环：`执行 → 评估 → 记录 → 改进 → 再评估`

## 维护规则

- 新增进化任务 → Edit 追加到 `evolution-calendar.md`
- 完成任务 → 将 ⏳ 改为 ✅已执行
- 跨工作区任务 → 同步更新所有受影响工作区的日历
- 新增评估断言 → Edit 追加到 `eval.json`
