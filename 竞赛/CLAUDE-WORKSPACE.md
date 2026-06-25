# 竞赛工作区 — FPGA/电赛/数学建模

> 主力工具：Codex CLI + Claude Desktop

## 职责
- FPGA 开发（XC7A35T）
- 电赛准备与实战
- 数学建模竞赛
- 跨校协作管理

## 文件结构
```
竞赛/
  CLAUDE.md
  AGENTS.md              ← Codex 配置
  memory/
  outputs/
  projects/              ← 竞赛项目（YYYYMMDD-主题 或 项目名）
  scripts/
```

## 硬件上下文
- FPGA：Xilinx XC7A35T（Artix-7）
- 开发环境：Vivado
- Arduino/ESP32 + 舵机控制
- RoboMaster 步兵控制

## 特殊约束
- Codex CLI 主要用于代码编写和 FPGA RTL
- Claude Desktop 用于方案讨论和文档撰写
- 竞赛项目用项目名目录（如 `Yolo算法比赛/`），不用 proj-ID
