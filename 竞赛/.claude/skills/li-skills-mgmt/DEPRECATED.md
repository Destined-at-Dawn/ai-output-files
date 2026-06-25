# DEPRECATED — li-skills-mgmt

**弃用日期**：2026-06-17
**弃用原因**：中间路由层冗余——它的唯一职责"决定调哪个底层 skill"已由 `skill-routing-table.json` 承担；其 Phase 0 需求消解、15 项质量门禁等内容在 li-skillcreate 中均有覆盖。

**替代方案**：
- 创建新 skill → **li-skillcreate**
- 融合/拆分/弃用/审核 → **li-skillfusion**
- 外部搜索参考 → **li-bestskill**

**迁移说明**：无需迁移，三个触发词已在路由表中重新指向 li-skillfusion。

> SKILL.md 永不删除，保留历史参考。
