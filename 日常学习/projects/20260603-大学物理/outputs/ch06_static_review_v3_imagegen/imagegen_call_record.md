# 第06章静电场 v3 image_gen 调用记录

## 结论

本目录从 v3 开始重新按用户要求使用 Codex 内置 `image_gen`（即 image2）生成视觉页。此前 v1/v2 中由 PIL 脚本生成的图片不再视为合格 image2 成品，只保留为结构草稿。

## 本次 image_gen 产物

- 默认生成路径：`C:\Users\13975\.codex\generated_images\019ed384-ecd6-7cb3-ae4f-3fbe3fcfb8d3\ig_0eceed16019013eb016a354171f3d8819a8fb7b8c2e1709f4d.png`
- 项目保存路径：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch06_static_review_v3_imagegen\imagegen_base_template_01.png`
- 当前状态：视觉底图，不是最终复习页。

## Prompt 摘要

生成一张大学物理静电场期末复习 A4 视觉底图，要求无文字、无数字、无公式、无 logo；保留标题区、思维导图区、题图证据区、紧凑卡片区，用静电场线和电荷分布作为视觉元素。

## 后续正确流程

1. 使用 image_gen 生成/重绘正式复习页，而不是用 PIL 脚本冒充。
2. 公式用人工整理后的标准表达写入 prompt，降低单页公式密度。
3. 若 image_gen 的公式或上下标出错，再用 LaTeX/RaTex 局部修补。
4. 原资料截图必须与 image_gen 页面视觉融合。
5. 用户确认图片后再合成 PDF。
