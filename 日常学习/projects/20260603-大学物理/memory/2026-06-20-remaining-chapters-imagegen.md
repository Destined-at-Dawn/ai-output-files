# 2026-06-20 大学物理剩余章节 image_gen 直出版

## 结论

已仿照第06章 `ch06_static_review_v5_imagegen_full` 路径，为第01、02、03、07、08章生成 image_gen 直出版复习 PDF。每章 8 页：6 页核心复习 + 2 页拔高页。PDF 只做图片装订，不添加文字层。

## 产物

- 第01章：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch01_kinematics_review_v1_imagegen_full\final_pdf\第01章_质点运动学_imagegen直出版_含拔高.pdf`
- 第02章：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch02_dynamics_review_v1_imagegen_full\final_pdf\第02章_质点动力学_imagegen直出版_含拔高.pdf`
- 第03章：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch03_rigidbody_review_v1_imagegen_full\final_pdf\第03章_刚体力学基础_imagegen直出版_含拔高.pdf`
- 第07章：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch07_magnetism_review_v1_imagegen_full\final_pdf\第07章_电流与磁场_imagegen直出版_含拔高.pdf`
- 第08章：`E:\ai产出文件\牛马\日常学习\projects\20260603-大学物理\outputs\ch08_emfield_review_v1_imagegen_full\final_pdf\第08章_电磁场_imagegen直出版_含拔高.pdf`

## 验证

- 每章页图：8 张。
- 每章 PDF 页数：8 页。
- 每章已生成 contact sheet。
- 抽查第08章总览图，页序完整：P01 到 P08，含两页拔高。

## 经验

- 内置 Python 通过 PowerShell 管道接收脚本文本时，中文字面量会乱码；中文路径应通过环境变量传入，中文 PDF 文件名可用 Unicode 转义生成。
- 默认系统 Python 缺少 Pillow；图片装订应使用 Codex workspace dependency Python。

