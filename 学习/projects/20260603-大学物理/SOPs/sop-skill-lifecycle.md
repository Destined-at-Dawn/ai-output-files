# SOP: Skill Lifecycle Pipeline

## Trigger Intent
用户说"创建/融合/优化/弃用/搜索" + skill/技能

## Skill Chain
```
Step 1: li-bestskill — 搜索外部（四阶段: GitHub wide → skills.sh → Chinese platforms → forums）
Step 2: li-skillcreate Phase 0 — 问题消解（WHY/WHAT/HOW 三层追问）
Step 3: li-skillcreate Phase 1 — 调研（本地5+技能 + 外部Top 3）
Step 4: li-skillcreate Phase 2 — 生成（li-系列标准骨架）
Step 5: li-skillcreate Phase 3.5 — 质量门禁（15项强制检查, 不过不提交）
Step 6: li-skillfusion — 如果是融合, 走融合流程
Step 7: li-manage — 更新技能清单 + 路由表 + 全工作区同步
Step 8: li-improve — 记录 skill 创建/融合模式
```

## Mandatory Post-Creation
1. 路由表新增（≥15触发词）
2. li/SKILL.md 入口更新
3. li-local-search 品牌路由更新
4. 全工作区路由表同步（os.walk递归）
5. eval.json 通过（12项质量断言）

## Feedback Loop
- skill 被实际触发使用 → 记录"活跃skill"
- skill 30天未触发 → 标记"沉睡"，下次 li-manage Flow E 审查
