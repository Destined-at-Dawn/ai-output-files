# 2026-06-20 第6章 image_gen 成功经验沉淀与拔高页

## 结论

用户确认：高要求复习 PDF 的成功路径是完全使用 Codex 内置 `image_gen` 直出页面，效果优于脚本/字体层/LaTeX 修补。后续任意学科、任意章节的复习 PDF 应默认继承该路径。

## 本次新增产物

- 拔高页目录：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch06_static_review_v5_imagegen_full\advanced_pages`
- 8页增强版 PDF：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch06_static_review_v5_imagegen_full\final_pdf\第06章_静电场_imagegen直出版_含拔高.pdf`
- 8页总览图：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch06_static_review_v5_imagegen_full\preview\ch06_static_review_v5_8p_contact_sheet.png`

## 两张拔高页

1. 拔高 1：非均匀带电球体与高斯积分，重点训练 `q_in(r)` 积分、分区场强和 `E-r` 曲线。
2. 拔高 2：圆弧缺口、电势梯度与导体球壳综合，重点训练补偿法、`E=-grad U`、导体球壳分区。

## 已沉淀规则

- 更新根目录 SOP：`SOPs\高要求复习PDF制作SOP.md`
- 更新入口规则：`AGENTS.md`
- 更新大学物理 SOP：`20260603-大学物理\SOPs\06_复习PDF制作SOP.md`
- 更新 Codex 技能：`C:\Users\13975\.codex\skills\study-review-pdf\SKILL.md`
- 新增技能参考契约：`C:\Users\13975\.codex\skills\study-review-pdf\references\imagegen-direct-review.md`

## 新红线

- 高要求复习页必须由 Codex 内置 `image_gen` 直出完整成品图。
- 本地脚本、HTML、ReportLab、LaTeX、字体层只能用于源材料整理或最终图片装订，不能冒充页面生成。
- 每章必须至少包含 1-2 页拔高/综合页，避免只训练简单判断和选择。
- 若 image_gen 页面有文字/公式问题，优先重写 prompt 整页再生。
