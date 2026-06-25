# Codex study-review-kit image_gen 口径更新

## 结论

`study-review-kit` 的目标运行环境是 Codex 时，不应把“缺少外部 image2 脚本”判为核心缺陷。正确验收口径是：Codex 能自动读取项目 `AGENTS.md` 与 `study-review-pdf` skill，并在高要求复习 PDF 流程中调用内置 `image_gen` 生成逐页图片预览。

## 已更新

- `study-review-kit/AGENTS.md`：默认出图链路改为 Codex 内置 `image_gen`，image2 / `baoyu-image-gen` 仅作为非 Codex fallback。
- `study-review-kit/SOPs/study-pdf-sop.md`：高密度材料 pipeline 改为 `image_gen` 优先。
- `study-review-kit/docs/codex-migration-guide.md`：迁移自检改为验证 Codex 是否能自动识别并调用内置 `image_gen`。
- `study-review-kit/README.md`：主链路、核心规矩、快速开始同步改为 Codex 自动识别 + 内置 `image_gen`。

## 经验

后续评估该 kit 时，重点看三件事：

1. `skills/` 是否已放入 Codex 可自动加载的技能目录。
2. 学习项目根目录是否放置 `AGENTS.md`。
3. Codex 是否能在复习 PDF / A4 / 原题截图融入任务中自动触发 `study-review-pdf` 并调用内置 `image_gen`。

不要再用“没有 image2 独立脚本”作为 Codex 环境下的扣分项。
