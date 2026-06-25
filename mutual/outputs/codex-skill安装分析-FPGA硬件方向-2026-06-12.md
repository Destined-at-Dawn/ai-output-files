# Codex Skill 安装分析 · FPGA/硬件方向

> 日期：2026-06-12 ｜ 方法：解析 5 个 Codex 线程实际任务 + 三库 skill 比对 + 自介佐证
> 结论一句话：你未来一个月最重要的三件事高度收敛在 FPGA/Verilog/硬件，应把 Codex 武装成专业 FPGA 协同工程师。

---

## 一、你在 Codex 上实际跑的任务（线程解码）

| 线程 | 工作区 | 真实任务 | 领域 |
|------|--------|---------|------|
| `019eba97` ★国奖 | 竞赛/FPGA安全通信优化 | 续国赛任务、Robei EDA实例调研、教学PPT生成、处理PNG/XLSX/PDF/DOCX输入材料转MD、按手册严格实现每个模块 | **FPGA** |
| `019e6e25` 巨生实习 | 竞赛 | 分析历史RTL经验+AI犯过的错；领导真实任务：Verilog驱动 I2C ADC/DAC + 1-Wire EEPROM，DAC出三角波、ADC采样用ILA看；Vivado 2020.1；引脚约束 | **FPGA** |
| `019e82fb` | 创作 | HTML传Vercel + **改RTL代码重新生成ILA**、看波形1→0跳变、给老板交可验证压缩包 | **FPGA**+部署 |
| `019e78c4` | 竞赛 | STAR法则简历+跨平台(X/YT/B站/知乎)调研写简历方法 | 求职/调研 |
| `019eb688` | 创作 | docx英文标点转中文(形势与政策心得) | 文档清洗 |

**自介佐证**：暑期线上帮 FPGA 硬件企业做 AI 化流程改造 / 具身智能企业董事长面试(巨生) / A类赛入围华东总决赛冲国赛、独立完成核心代码+技术文档+PPT。

→ **三大主线（国奖 / 巨生线下实习 / FPGA企业线上实习）全是 FPGA/Verilog。** 你的诉求"提高AI写代码+调试设备能力"= 把 Codex 打造成 FPGA 协同工程师。

---

## 二、Codex 现状（已装 30 个）

相关已有：`hardware-design`（Verilog/SV/Vivado/Quartus/时序/AXI/CDC/Verilator/lint 全覆盖）、`code`、`deep-research`、`pdf`、`doc`、`competition-workflow`、`prompt-optimizer`、`daily-review`、`devils-advocate`。

---

## 三、安装清单（去重后，按优先级）

### 🔴 P0 — 装了立刻命中当前任务

| Skill | 来源库 | 为什么是刚需 | 证据 |
|-------|--------|------------|------|
| **rtl-fpga-lessons** | `.claude` | **描述逐字命中巨生实习线程**：D:/AMD、I2C ADC/DAC、AT21CS01 1-Wire EEPROM、ILA、Vivado 2020.1、boss feedback、final ZIP。这skill就是从你这工作提炼的，Codex却没装 | 线程019e6e25 + skill description 完全吻合 |
| **ppocrv5** (OCR) | `.claude/.newmax` | 国奖任务要提取一堆PNG要求截图（分赛区/总决赛要求.png），Codex**无任何OCR能力** | 线程019eba97消息2 |
| **xlsx** | `.claude/.newmax` | A7-50T引脚约束表.xlsx、资源约束表.xlsx 要解析，Codex**无xlsx能力** | 线程019eba97消息2 |
| **PPT技能**(pptx 或 baoyu-slide-deck) | `.claude/.newmax` | 国奖明确要"生成教学PPT(16:9/特定样式)"，Codex**无PPT能力** | 线程019eba97消息1 |

### 🟡 P1 — 调试能力增强

| Skill | 来源库 | 为什么 |
|-------|--------|--------|
| **li-debug** | `.claude/.newmax` | 你诉求明说"调试设备"。Codex有`code`但无纪律化调试循环（复现→假设→插桩→修复→回归）。`devils-advocate`是泼冷水≠调试 |

### ⚪ 不推荐（Codex已覆盖，装了是重复）

- `fpga` / `systemverilog` → `hardware-design` 已全覆盖
- `li-hardware` → `hardware-design` 是其等价/超集
- `li-research` → 已有 `deep-research`
- `li-competition` → 已有 `competition-workflow`
- `li-code` → 已有 `code`

---

## 四、可行性说明

- Codex skill 格式 = `---name/description---` frontmatter + SKILL.md，与 `.claude` 完全一致 → **可直接复制目录到 `~/.codex/skills/`**。
- `rtl-fpga-lessons`/`fpga`/`systemverilog` 仅 `.claude` 有；`ppocrv5`/`xlsx`/`pptx`/`li-debug` 两库都有。
- 建议 Codex 内重命名遵循其风格（如 li-debug → debug-loop），保持命名一致性。

---

## 五、工作流优化建议（回答"怎么优化"）

1. **单点最高杠杆**：装 `rtl-fpga-lessons` → Codex 立刻继承你过去的踩坑教训，少犯重复错（这正是线程019e6e25开头你要求的"分析之前AI犯的错"）。
2. **材料入口标准化**：ppocrv5+xlsx+pdf 三件套让 Codex 能吃下竞赛/实习的任何输入材料（截图/表格/手册）→ 转MD → 喂进工作流，不再靠你手动转述。
3. **交付闭环**：PPT技能补上"技术文档→教学PPT"最后一公里（国奖要、企业AI化培训也要）。

> 口径：本分析基于 5 个线程的真实用户消息 + skill description 比对，`@中级口径`。是否每个 skill 装入后真能在 Codex 触发，需装后各跑一次验证（同遥测系统的 debug-first 原则）。
