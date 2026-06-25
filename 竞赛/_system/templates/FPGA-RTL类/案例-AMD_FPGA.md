# 案例：AMD FPGA 跨对话交付

> **类型**：FPGA-RTL 类 | **客户**：老板（D:/AMD 工程）
> **来源**：从 SOP-13 提取，保留项目特定信息
> **用途**：接 D:/AMD 相关任务时直接参考，不从零摸索

---

## 板级固定信息

- FPGA：XC7A35T-2FGG484I
- 时钟：clk = W19，50 MHz
- 低有效复位：reset = Y19
- I2C：i2c_scl = W21，i2c_sda = AA18
- 1-Wire EEPROM：DQ = Y6
- LED：D0 = AB22（成功），D1 = AB21（失败）
- ADC1：ADC081C021，地址 7'h55
- ADC2：ADC081C021，地址 7'h56
- DAC1：DAC081C085，实测地址 7'h0a
- DAC2：DAC081C085，参考地址 7'h09

---

## 用户和老板偏好

- 命名用简洁中文功能名，不要编号前缀（`01_`、`02_`）
- 最终 ZIP 放 `D:/AMD/老板可直接发送的最终压缩包`
- 每个功能的 ZIP/DOCX/RTL/XDC/Tcl 聚合到 `D:/AMD/最终交付包/<功能名>/`
- 文档要公司风格，不能乱码，必须 .docx
- RTL/Tcl/XDC 注释默认 ASCII
- 整理动作默认不删除原文件，先归档

---

## 当前最终交付功能

- `ADC1采样_DAC1可调采样率回放_默认4kSPS`
- `ADC1采样_DAC1固定10Hz回放`
- `AT21CS01单总线EEPROM暖复位读写`

入口：`D:/AMD/快速查找索引.md`（记录每个功能对应的 ZIP/DOCX/top/模块/XDC）

---

## 已踩坑（血泪教训）

| 坑 | 详细 |
|----|------|
| AT21CS01 ≠ Dallas 1-Wire | reset 后默认高速，需要 discovery + Standard Speed Mode 流程 |
| AT21CS01 暖复位 | 可能不同于冷下载；芯片靠 DQ 供电时 reset low 需要覆盖标准速要求 |
| 共享 I2C 吞吐 | ADC读 + DAC写共享总线，不能承诺 0-75 kHz 任意波形稳定回放 |
| 10 Hz 是演示频率 | 不是 ADC/DAC 链路上限，早期稳定不代表上限 |
| 可调采样率默认值 | `ADC_SAMPLE_HZ=4000`；40 Hz 漂亮，100 Hz 可用但台阶明显 |
| 输入波形范围 | 2.0~2.4Vpp、offset 1.65V，3.3Vpp 满幅会削峰 |
| EEPROM 复位后 LED | D0/D1 应先灭；完成成功 D0 亮、失败 D1 亮 |
| EEPROM 地址 | 不能硬编码，失败优先考虑地址/协议/速度状态 |
| ILA 深度 | 慢波形不能用过短采样窗口判断「没动」 |

---

## 文件夹结构

`D:/AMD` 按功能查找，不按编号：
- `老板可直接发送的最终压缩包`
- `最终交付包`
- `公共资料`
- `AI协作记录`
- `历史参考包`
- `工具脚本`
- `历史归档`

维护：`D:/AMD/快速查找索引.md` + `D:/AMD/交付物对应关系.csv`

---

## 收尾记录要求

每次修复完成后，写入：
- `memory/rtl_code_lessons.md`（工作区）
- `skills/rtl-fpga-lessons/references/vivado_rtl_lessons.md`（skill）

格式：现象 → 根因 → 修复 → 下次检查 → 验证结果
