# 失败教训：Vivado静默崩溃与大容量ROM强制BRAM约束

## 1. 错误表现
- **现象**：Vivado 在综合（Synthesis）阶段，读取完 hex 文件后，日志戛然而止（没有 error 报错，直接停止）。
- **用户反馈**：Synthesis Failed 亮红灯，但 Messages 窗口里 Error 数为 0。

## 2. 错误根因
- 在编写 `logo_rom.v` 时，虽然数组大小达到了 29583 * 24bit ≈ 700Kb，但仅仅声明了 `reg [23:0] mem [0:29582];`。
- **致命失误**：没有添加硬件约束属性。导致 Vivado 综合器默认使用分布式 RAM（LUT资源）去强行拼凑这 700Kb 空间。这引起了综合工具的内存消耗指数级爆炸，最终触发 Windows 系统级别的 Out-Of-Memory (OOM) Killer，导致 Vivado 底层进程直接被系统静默杀死。

## 3. 正确做法
对于任何大于 10KB 的 ROM/RAM 数组实例化，**必须、强制**在声明的最前面加上 BRAM 综合指令：
```verilog
(* rom_style = "block" *) reg [23:0] mem [0:29582];
```

## 4. 铁律补充（已固化至 SKILL）
**【大数组声明铁律】**：严禁在不加约束的情况下声明大型存储器数组！这是导致 EDA 工具崩溃的第一元凶！
