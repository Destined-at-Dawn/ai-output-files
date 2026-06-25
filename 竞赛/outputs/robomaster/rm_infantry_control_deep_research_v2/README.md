# RM 简易步兵电控 deep-research v2

## 结论

这是在上一版学习包基础上，用 `deep-research` 技能工作流做过调研和迭代的新版本。上一版不覆盖，v2 独立放在本文件夹。

## 文件结构

```text
rm_infantry_control_deep_research_v2/
  README.md
  research_report.md
  _skill_snapshot/
    SKILL.md
    INTRODUCTION.md
    _meta.json
  docs_docx/
    00_v2_overview.docx
    ...
    10_full_combined_document.docx
  docs_pdf/
    00_v2_overview.pdf
    ...
    10_full_combined_document.pdf
  improved_pack/
    Core/
    docs/
    README.md
    main_integration_example.c
```

## 推荐阅读顺序

1. `research_report.md`：先看为什么要从 v1 迭代到 v2。
2. `improved_pack/README.md`：看 v2 代码包结构。
3. `improved_pack/docs/tutorial_step_by_step.md`：让提交者按步骤真正写懂。
4. `improved_pack/docs/code_walkthrough.md`：逐函数讲清楚。
5. `improved_pack/docs/test_plan.md`：按风险从低到高测试。

## v2 新增能力

- 下载/快照了你指定的 `.newmax` deep-research 技能到 `_skill_snapshot/`。
- 新增调研报告 `research_report.md`。
- 新增 `safety.c/h`，独立安全状态机。
- 新增 `c620_can.c/h`，用于 RoboMaster 常见 C620/M3508 CAN 电调协议。
- 更新技术文档和教程，加入官方资料校准后的解释。

## 边界

v2 仍然是应用层参考代码，不是某块具体 STM32 板子的完整 CubeMX 工程。真实提交前，需要在自己的板子上补 `bsp_port.c` 的 HAL 实现，并把测试记录改成真实结果。

Source: `${WORKSPACE_ROOT}/outputs/robomaster/rm_infantry_control_deep_research_v2/research_report.md:1`
