# 模板库索引

> **用途**：接单时 10 秒匹配模板，不从零开始
> **配合**：SOP-14 §二 模板匹配
> **进化规则**：每完成一个项目，反哺模板（SOP-14 §八）

---

## 匹配表

| 客户需求关键词 | 模板路径 | 补充 SOP |
|-------------|---------|---------|
| FPGA / Verilog / RTL / Vivado / 开发板 | `FPGA-RTL类/_template.md` | SOP-06 |
| D:/AMD / ADC / DAC / EEPROM / I2C | `FPGA-RTL类/案例-AMD_FPGA.md` | SOP-06 |
| 嵌入式 / 电控 / STM32 / Arduino / 考核 | 待建 | SOP-06 |
| 算法 / 仿真 / MATLAB / Python 竞赛 | 待建 | — |
| 课程设计 / 实验报告 | 无模板，直接用 SOP-11 | SOP-11 |
| 答辩 / PPT / 演示 | 无模板，直接用 SOP-05 | SOP-05 |

---

## 模板分类规则

按 **学科领域 × 交付物类型** 分类：
- `FPGA-RTL类/` — FPGA 开发板相关（Verilog/VHDL + Vivado + 实验文档）
- `嵌入式-电控类/` — 嵌入式系统（C/MCU + Keil/IAR + 考核文档）
- `算法-仿真类/` — 算法竞赛（Python/MATLAB + 仿真报告）

新类型出现时 → 新建目录 + `_template.md` + 案例文件。

---

## 进化记录

| 日期 | 变更 |
|------|------|
| 2026-06-09 | 初始化：从 SOP-12/13 提取 FPGA-RTL 类模板和 AMD 案例 |
