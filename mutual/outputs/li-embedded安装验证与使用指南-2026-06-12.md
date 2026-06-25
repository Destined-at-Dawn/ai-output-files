# li-embedded 安装完成与使用指南

> 日期：2026-06-12 ｜ 状态：✅ 已安装到三套工具
> 资料来源：cpq bare-metal guide (4.7k★) + Miro Samek 现代嵌入式课程 (1.3k★) + Awesome-Embedded (8.7k★)
> 融合：li-debug + li-hardware + li-code + li-improve + li-analyze

---

## 安装状态检查表

### ✅ 文件已复制到三套工具

| 工具 | 路径 | 状态 |
|------|------|------|
| **Codex** | `C:/Users/13975/.codex/skills/li-embedded/SKILL.md` | ✅ 存在 |
| **Claude Code** | `C:/Users/13975/.claude/skills/li-embedded/SKILL.md` | ✅ 存在 |
| **Newmax** | `${NEWMAX_HOME}/skills/li-embedded/SKILL.md` | ✅ 存在 |

### ✅ 路由表已更新

| 系统 | 条目 ID | 条目名 | 优先级 | 自动触发 | 状态 |
|------|--------|--------|--------|---------|------|
| **Newmax** | r242 | li-embedded — STM32/ARM实时固件开发 | 2 | Yes | ✅ |

**总路由数**：46（新增 1 条）

### ✅ 触发词已配置

你现在可以用以下任何关键词触发 li-embedded：
```
STM32 / ARM Cortex-M / 嵌入式固件 / 嵌入式开发 / 裸机编程
寄存器编程 / 中断处理 / SWD调试 / RTT实时传输
状态机控制 / RTOS / 硬件调试 / GPIO配置 / I2C驱动
电机控制 / 具身智能硬件 / 硬件工程师 / 代码调试
（及其他 40+ 个触发词）
```

---

## 立即可用的四大工作流

### 工作流 1：初始化一个 GPIO 输出（3 分钟）

**触发 li-embedded**：说「我要配置一个 GPIO 输出，PA5」

AI 会自动：
1. 用 pin abstraction macro 而不是裸写寄存器
2. 提醒你 RCC 时钟配置（常见 AI 错误）
3. 给出 Ozone 断点设置示例

```c
// AI 会这样写（自动范式）
#define PIN(bank,num) ((((bank)-'A')<<8)|(num))
gpio_output(PIN('A', 5));
// 而不是这样（容易出错）
GPIOA->MODER |= 0x0C00;
```

---

### 工作流 2：调试一个卡住的设备（5 分钟）

**触发 li-embedded**：说「变量 motor_speed 为什么总是 0？」或「代码卡在中断里了」

AI 会自动：
1. 建议用 RTT（不用 printf）快速观测
2. 用 Ozone 断点定位代码位置
3. 询问是否有 volatile 关键字（常见 bug）
4. 给出插桩代码示例

```c
#include "SEGGER_RTT.h"
SEGGER_RTT_printf(0, "Motor speed: %d\n", motor_speed);  // 实时看值
```

---

### 工作流 3：把 superloop 改成状态机（10 分钟）

**触发 li-embedded**：说「这个控制逻辑太混乱了」或「中断和主循环冲突」

AI 会自动：
1. 识别当前的 superloop 反模式
2. 设计状态机框架
3. 改写代码（event-driven 风格）

```c
// AI 会改成这样
enum { STATE_IDLE, STATE_ACTIVE };
void ISR_handler(void) { postEvent(EVENT_TRIGGER); }
void handle_events(void) {
  switch(current_state) {
    case STATE_IDLE:
      if (event == EVENT_TRIGGER) current_state = STATE_ACTIVE;
      break;
    // ...
  }
}
```

---

### 工作流 4：建硬件 CI/CD（第一次 20 分钟，之后自动）

**触发 li-embedded**：说「我要自动测试固件」或「每次 push 都验证」

AI 会自动：
1. 写 GitHub Actions 编译脚本
2. 配 vcon.io 远程烧录
3. 加硬件输出验证

```makefile
test: build
  curl -su :$(KEY) https://dash.vcon.io/api/v3/devices/ID/ota --data-binary @fw.bin
  curl -su :$(KEY) https://dash.vcon.io/api/v3/devices/ID/tx?t=5 | grep "OK"
```

---

## 日常工作场景速查

### 场景：「我的 I2C ADC 读不出来」

1. 说「用 li-embedded 帮我排查 I2C」
2. AI 会问：
   - 是硬件（缺 RCC？引脚反了？）还是协议（寄存器配错了？）
   - 要不要用 RTT 看实时数据
3. AI 给出检查清单：
   - ✓ RCC→APBx→I2C 时钟链路
   - ✓ GPIO alternate function 配置
   - ✓ I2C 寄存器初始化顺序
   - ✓ 用 Ozone 看寄存器值

---

### 场景：「代码开始卡，怎么调？」

1. 说「li-embedded 调试死循环」
2. AI 会建议：
   - **第 1 步**：Ozone 断点，看卡在哪
   - **第 2 步**：RTT 打 log，看有没有执行到某处
   - **第 3 步**：看寄存器，判断中断/外设状态
   - **第 4 步**：改代码→vcon.io 自动测试

---

### 场景：「电机启动不了，领导在等」

1. 说「li-embedded 电机控制紧急排查」
2. AI 会：
   - **15 秒**：问"现象是什么"（完全不动 vs 抖一下 vs 反向）
   - **1 分钟**：建议最可能的原因（PWM/方向/反馈）
   - **5 分钟**：给排查清单 + 修复代码
   - **2 分钟**：vcon.io 远程验证

---

## 五大 li-skills 融合点

| li-skill | 何时自动触发 | 用途 |
|---------|-------------|------|
| **li-debug** | 「代码卡住了」「变量为什么是这个值」 | 调试循环：反馈→复现→假设→插桩→修复→回归 |
| **li-hardware** | 「寄存器怎么配」「硬件不响应」 | 理解硬件→寄存器映射→内存模型→时钟树 |
| **li-code** | 「代码太乱」「性能慢」 | 编码规范：volatile、pin abstraction、MISRA-C |
| **li-improve** | 「AI 又算错了」「这个坑之前踩过」 | AI 错误反思：RTT printf 太慢、RCC 漏配、中断竞态 |
| **li-analyze** | 「为什么 AI 容易在 STM32 出错」「这个架构好在哪」 | 道法术器穿透：Why→How→What→With What |

---

## 快速测试（验证安装）

### 立即试试

在 Codex / Claude Code 里，说以下任何一句：

```
「用 li-embedded 帮我初始化一个 SPI」
「li-embedded 调试一下这个中断没触发的问题」
「li-embedded 改一下这个 superloop 成状态机」
「li-embedded 搭建硬件 CI/CD」
```

**预期**：AI 会自动进入"STM32 专业固件工程师"模式，带着你一步步做。

### 验证成功的信号

你会看到 AI：
- ✅ 问"是硬件还是软件"的诊断问题
- ✅ 用 pin abstraction / volatile / RTT 等术语
- ✅ 建议用状态机而不是 superloop
- ✅ 提到 Segger Ozone / SWD / MISRA-C
- ✅ 指出"忘了 RCC"之类的常见错误
- ✅ 建议硬件 CI/CD（vcon.io）

---

## 边界清楚（what's in / out）

### ✅ li-embedded 覆盖

- STM32/ARM Cortex-M 裸机编程
- 寄存器级初始化
- 状态机与事件驱动架构
- SWD/RTT/ITM 调试工具链
- MISRA-C 嵌入式编码规范
- 硬件 CI/CD（vcon.io/GitHub Actions）
- RTOS 基础（FreeRTOS 架构）
- 电机控制、I2C/SPI 驱动等外设

### ❌ li-embedded 不覆盖

- FPGA/Verilog（用 li-hardware）
- Python/高级应用代码（用 li-code）
- 学术固件理论（太深，用 li-research）
- 某个企业的专有协议
- 无线通信协议深度（超出范围）

---

## 后续优化（给你的建议）

### 第 1 周：实际用 2-3 次

用「li-embedded 帮我排查 I2C」和「li-embedded 初始化 GPIO」之类的真实场景。

→ AI 会记录"你问过什么"，下次会更精准。

### 第 2 周：反馈改进

如果 AI 某次建议不对，告诉它「这个不对，应该…」

→ li-improve 会记录教训，AI 下次避免。

### 第 3 周+：扩展场景

用「li-embedded + li-debug」组合调试设备；用「li-embedded + li-improve」反思 AI 错误模式。

→ 五大 li-skills 的联动会越来越顺。

---

## 技术细节（如果你想深入）

### 能读的核心文献
- cpq/bare-metal-programming-guide：从零开始写 STM32（寄存器级）+ Ozone 调试
- Miro Samek 现代嵌入式课程：状态机 + Active Object（用在控制层很爽）
- Awesome-Embedded：知识导航（FreeRTOS、调试工具、编码标准）

### 内嵌知识库
Skill 里已经有：
- Pin abstraction 宏模板
- 状态机架构示例
- RTT 日志模板
- MISRA-C 合规清单
- 硬件 CI/CD 脚本骨架
- 常见 AI 错误 + 修正

### 联动工具
- **与 li-debug**：调试循环（反馈→复现→假设→插桩→修复→回归）
- **与 li-improve**：AI 踩过的 5 大坑自动记录
- **与 li-research**：需要深研 STM32 datasheet 时
- **与 li-analyze**：用道法术器拆解某个硬件设计决策

---

## 三套工具的协作模式

### Codex 日常用（快速）

```
Codex 里说「li-embedded 初始化 GPIO」
→ 2 分钟搞定，直接写进代码
```

### Claude Code 深度用（讲究）

```
Claude Code 里说「li-embedded + li-debug 帮我排查中断问题」
→ 5 分钟诊断，给出完整思路
```

### Newmax 记录用（审计）

```
在 Newmax 的 skill-usage-log 里会自动记录
「2026-06-12 14:23 / li-embedded / 调试电机 / success」
```

---

## 常见问题（FAQ）

**Q：为什么 AI 以前总在 STM32 上出错？**
A：AI 默认堆 HAL 调用，没看过"专业固件长什么样"。li-embedded 给了它范式，现在就对。

**Q：li-embedded 和 li-hardware 的区别？**
A：li-hardware 是通用硬件（FPGA/Arduino/舵机）；li-embedded 专攻 STM32 实时固件（裸机+状态机+调试）。

**Q：我已经装了 li-hardware，还要装 li-embedded 吗？**
A：要。li-hardware 是 10 万英尺的视图；li-embedded 是"具体怎么写"的 1 千英尺细节。两个互补。

**Q：触发词太多了，怎么记？**
A：不用全记。只要说「STM32」、「硬件调试」、「写固件」之类的常见词，AI 会自动进入 li-embedded 模式。

**Q：我的代码在 Codex/Claude Code 里效果不一样？**
A：正常。三套工具的上下文和对话历史不同。建议一个工具里工作完成再切。

---

> **工程法则**：专业固件不是"会编程"，是"知道为什么要这样编"。如果 AI 写出的代码你能看懂并且不踩坑，说明 skill 工作了。
