# 2026-06-19 Codex：study-review-kit 介绍页符合性审计

## 事实

- 审计对象：`E:\ai产出文件\牛马\日常学习\study-review-kit.zip` 与 `E:\ai产出文件\牛马\日常学习\study-review-kit-intro.html`。
- HTML 介绍页承诺：16 个 skills、认知科学驱动、LaTeX + image2、AI 运维特化、LLM / PyTorch、26 个 PyTorch 实战题。
- 原 zip 已包含 16 个顶层 skill 目录、AGENTS、SOP、迁移指南、AI 运维路径、PyTorch 样章。
- 原 zip 缺口：没有独立的 PyTorch 26 题矩阵，只有样章和“照着做其余 25 题”的说明。

## 处理

- 新增 `docs/pytorch-26-practice-map.md`：把 datawhalechina `llm-algo-leetcode` Chapter 2 的 00-25 共 26 题按 8 组映射到本包固定产出。
- 新增 `docs/intro-conformance-audit.md`：记录 HTML 介绍页符合性审计结论。
- 更新 `README.md` 与 `docs/ai-ops-llm-track.md`，把 26 题矩阵纳入入口说明。
- 用户提醒：对方机器绝对不能假设已有 `baoyu-image-gen`。已确认并强化 `study-review-kit/skills/baoyu-image-gen/` 随包交付，且在 `skills/baoyu-image-gen/SKILL.md` 第一节、`docs/codex-migration-guide.md` 写明复制整个 `skills/` 后即可获得该 skill。

## 决策

- 不把第三方官方 notebook 全文复制进资料包，只保留学习矩阵和官方题源定位。原因：官方题源会更新，固化全文容易过期；本包定位是工作流交付包，不是第三方课程镜像。

## 后续提醒

- 使用 PyTorch 26 题时，以 datawhalechina 官方仓库最新 `02_PyTorch_Algorithms` 为一手资料。
- 如果以后 HTML 继续宣传“完整题库离线包”，再考虑内置官方题面或 notebook，并同步处理许可证说明。
