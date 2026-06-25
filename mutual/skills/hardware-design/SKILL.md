---
name: hardware-design
description: >
  硬件设计综合指南，覆盖 Verilog/SystemVerilog 编码规范、FPGA 开发（Vivado/Quartus）、
  ASIC 设计、时序收敛、Verilator 仿真与 lint、AXI 接口、CDC 处理、FPGABuilder 自动构建。
  触发词：verilog, systemverilog, sv, fpga, 硬件, 电路, asic, vivado, quartus, 时序, 逻辑, rtl, 仿真, 综合, fpgabuilder, 构建。
---

# Hardware Design: Verilog / SystemVerilog / FPGA / FPGABuilder

You are an expert in FPGA and ASIC development with SystemVerilog, Vivado, Quartus, hardware design optimization, and automated build toolchains.

## Documentation

All modules, wires, and registers require comments:

```systemverilog
// Module: counter
// Purpose: Simple up-counter with synchronous reset
module counter #(
    parameter WIDTH = 8  // Counter bit width
) (
    input  logic             clk,      // System clock
    input  logic             rst_n,    // Active-low reset
    output logic [WIDTH-1:0] count     // Current count value
);
```

### Fixed-Point Notation

Document all fixed-point values using TI-style Q notation:

- `Qm.n` — signed: m integer bits (including sign bit), n fractional bits, total width = m + n bits.
- `UQm.n` — unsigned: m integer bits, n fractional bits, total width = m + n bits.

### Naming Conventions

- Active-low signals: use `_n` suffix (e.g., `rst_n`, `chip_select_n`)
- Clocks: `clk` or `clk_<domain>`
- Use descriptive names over abbreviations

## Coding Style

### always_ff: Simple Assignments Only

`always_ff` blocks must contain ONLY simple non-blocking assignments. No logic, no expressions — this ensures Verilator simulation matches synthesized behavior. (Exceptions: memory inference and async reset synchronizers — see those sections.)

```systemverilog
// CORRECT - simple assignment
always_ff @(posedge clk) begin
    count <= count_next;
    state <= state_next;
end

// WRONG - logic in always_ff
always_ff @(posedge clk) begin
    count <= count + 1;                // Move to always_comb
    state <= enable ? RUNNING : IDLE;  // Move to always_comb
end
```

### always_comb: All Logic Here

All combinational logic belongs in `always_comb` blocks:

```systemverilog
always_comb begin
    count_next = count + 8'd1;
    state_next = enable ? RUNNING : IDLE;
end
```

### Formatting

- One statement per line — never chain multiple statements or assignments on a single line
- One declaration per line
- Explicit bit widths on all literals
- Start files with `` `default_nettype none ``
- Always use `begin`/`end` blocks for `if`, `else`, `case` items (prevents bugs when adding code later)
- Prefer to keep modules under ~500 lines; if a module grows significantly larger, consider refactoring into smaller sub-modules

```systemverilog
`default_nettype none

module example (
    input  logic        clk,
    input  logic        rst_n,
    input  logic [7:0]  data_in,
    output logic [7:0]  data_out
);

    logic [7:0] data_reg;    // Registered data
    logic [7:0] data_next;   // Next state value
    logic       valid;       // Data valid flag

    localparam logic [7:0] INIT_VAL = 8'd0;

endmodule

`default_nettype wire
```

### FSM Patterns

Separate state register from next-state logic. Use enums for state encoding.

```systemverilog
typedef enum logic [1:0] {
    IDLE,
    RUN,
    DONE
} state_t;

state_t state;       // Current state register
state_t state_next;  // Next state value

// Next-state logic (combinational)
always_comb begin
    state_next = state;
    case (state)
        IDLE: if (start) state_next = RUN;
        RUN:  if (finish) state_next = DONE;
        DONE: state_next = IDLE;
        default: state_next = IDLE;
    endcase
end

// State register (sequential)
always_ff @(posedge clk) begin
    state <= state_next;
end
```

### Module Instantiation

- One module per file, filename matches module name
- Always use named port connections (never positional)

```systemverilog
// CORRECT - named connections
counter #(.WIDTH(16)) u_counter (
    .clk   (clk),
    .rst_n (rst_n),
    .count (count_value)
);

// WRONG - positional connections
counter u_counter (clk, rst_n, count_value);
```

## Modular Design & Code Organization

- Structure designs into small, reusable modules to enhance readability and testability
- Start with a top-level design module and gradually break it down into sub-modules
- Use SystemVerilog `interface` blocks for clear interfaces
- Maintain consistent naming conventions across modules

## Synchronous Design Principles

- Prioritize single clock domains to simplify timing analysis
- Favor synchronous reset over asynchronous reset to ensure predictable behavior
- Avoid timing hazards during synthesis
- Use proper clock domain crossing (CDC) techniques when multiple clocks are required

## Timing Closure & Constraints

- Establish timing constraints early using XDC/SDC files
- Review Static Timing Analysis reports regularly
- Identify critical timing paths using Vivado/Quartus timing reports
- Address violations by adding pipeline stages or optimizing logic
- Use multi-cycle path constraints where appropriate

## Resource Utilization & Optimization

- Optimize LUTs, flip-flops, and block RAM through efficient SystemVerilog
- Leverage Vivado/Quartus built-in IP cores (AXI interfaces, DSP blocks, memory controllers)
- Select appropriate synthesis strategies based on design priorities
- Use `reg []` for RAM inference and minimize register usage
- Balance area vs. speed optimization based on requirements

## Power Optimization

- Implement clock gating to reduce dynamic power consumption
- Use power-aware synthesis (Vivado power optimization / Quartus PowerPlay)
- Set power constraints for low-power applications
- Minimize switching activity in non-critical paths

## Yosys Synthesis Compatibility

Synthesizable RTL should work with both **Verilator** (lint/simulation) and **Yosys** (synthesis for open-source FPGA flows).
Yosys supports a subset of SystemVerilog via `read_verilog -sv`.

**Constructs to avoid in synthesizable RTL:**

| Avoid | Use instead |
| --- | --- |
| `return <expr>;` in functions | `function_name = <expr>;` (Verilog-2005 style) |
| `interface` / `modport` | Explicit port lists |
| `unique case` / `priority case` | Plain `case` with `default` |
| Multi-dimensional packed arrays in ports | Flatten to single vectors |

```systemverilog
// CORRECT - Yosys-compatible function
function automatic logic [7:0] add_saturate(input logic [7:0] a, input logic [7:0] b);
    logic [8:0] sum;
    sum = {1'b0, a} + {1'b0, b};
    add_saturate = sum[8] ? 8'hFF : sum[7:0];
endfunction
```

## Testing with Verilator

Every module requires a testbench. Build and run with Verilator:

```sh
# Build testbench
verilator --binary -Wall module_tb.sv module.sv

# Run simulation
./obj_dir/Vmodule_tb
```

### Verilator Linting

```sh
verilator --lint-only -Wall module.sv
```

- Fix all warnings — do not suppress with pragmas
- Key warnings: WIDTH (bit-width mismatch), UNUSED, UNDRIVEN

### Verilator Simulation Flags

```sh
verilator --binary \
    -Wall \
    -Wno-fatal \
    -j 0 \
    --assert \
    --timing \
    --trace-fst \
    --trace-structs \
    --main-top-name "-" \
    --x-assign unique \
    --x-initial unique \
    module_tb.sv module.sv
```

### Testbench Structure

```systemverilog
module counter_tb;
    logic       clk = 1'b0;
    logic       rst_n;
    logic [7:0] count;

    counter dut (.*);

    always begin
        #5 clk = ~clk;
    end

    initial begin
        rst_n = 1'b0;
        #20 rst_n = 1'b1;
        #100;
        $display("Test complete, count=%d", count);
        $finish;
    end
endmodule
```

### Testbenches & Debugging

- Write detailed, self-checking testbenches covering typical use cases and edge cases
- Use SystemVerilog assertions for verification
- Run behavioral and post-synthesis simulations
- Use Integrated Logic Analyzer (ILA) for real-time signal debugging
- Implement assertion-based verification to catch protocol violations

## Avoiding Latches

Latches are inferred when signals are not assigned in all paths. Prevent with:
- Default assignments at start of `always_comb`
- Cover all cases including `default`

```systemverilog
always_comb begin
    data_next = data_reg;
    valid_next = 1'b0;
    case (state)
        IDLE:   data_next = 8'd0;
        LOAD:   data_next = data_in;
        default: data_next = data_reg;
    endcase
end
```

## Reset Handling

Use synchronous resets when possible. For external async resets, synchronize first.

```systemverilog
// Synchronous reset (preferred)
always_comb begin
    count_next = rst_n ? (count + 8'd1) : 8'd0;
end
always_ff @(posedge clk) begin
    count <= count_next;
end

// Reset synchronizer for external async reset
logic [1:0] rst_sync;
always_comb begin
    rst_sync_next = {rst_sync[0], 1'b1};
end
always_ff @(posedge clk or negedge rst_async_n) begin
    if (!rst_async_n) rst_sync <= 2'b00;
    else rst_sync <= rst_sync_next;
end
assign rst_n = rst_sync[1];
```

## Clock Domain Crossing (CDC)

Single-bit signals: use 2-FF synchronizer. Multi-bit: use gray coding or handshake.

```systemverilog
// 2-FF synchronizer for single-bit CDC
logic [1:0] sync_reg;
always_comb begin
    sync_reg_next = {sync_reg[0], signal_src};
end
always_ff @(posedge clk_dst) begin
    sync_reg <= sync_reg_next;
end
assign signal_sync = sync_reg[1];

// Gray code for multi-bit
function automatic logic [WIDTH-1:0] bin2gray(input logic [WIDTH-1:0] bin);
    bin2gray = bin ^ (bin >> 1);
endfunction
```

### CDC Techniques

- Use synchronizers or FIFOs to handle CDC safely
- Implement proper handshaking protocols
- Verify CDC paths thoroughly

## Memory Inference

Use standard patterns for RAM/ROM inference by synthesis tools. (Exception to the "simple assignments only" rule.)

```systemverilog
// Single-port RAM
logic [DATA_WIDTH-1:0] mem [0:DEPTH-1];
always_ff @(posedge clk) begin
    if (we) mem[addr] <= wdata;
    rdata <= mem[addr];
end

// ROM (initialized memory)
logic [7:0] rom [0:255];
initial $readmemh("rom_data.hex", rom);
always_ff @(posedge clk) begin
    rdata <= rom[addr];
end
```

### ⚠️ Vivado 大容量 ROM 综合生存指南（2026-05-13 铁律）

> **来源**：2026-05-12/13 连续7次综合失败的血泪教训。ROM深度>16384时，`$readmemh`代码推断方案会导致Vivado综合器OOM崩溃。

#### 决策树

```
ROM深度 > 16384 ?
├── 否 → 标准代码推断方案
│         (* rom_style = "block" *) + initial $readmemh
│         综合器自动映射到BRAM，无风险
│
└── 是 → 禁止用 $readmemh！必须用 Block Memory Generator IP核
          原因：Vivado 2025.2 综合器对大$readmemh数组的优化算法会OOM
```

#### BMG IP核 TCL 建工程完整模板（含全部5个防崩溃铁律）

```tcl
# 铁律1: create_ip前必须mkdir（否则报错"IP directory does not exist"）
file mkdir $proj_dir/ip

# 铁律2: 不写IP版本号（让Vivado自动选，否则"version X.Y not found"）
create_ip -name blk_mem_gen -vendor xilinx.com -library ip \
    -module_name blk_mem_logo -dir $proj_dir/ip

# 铁律3: 配置IP参数
set_property -dict [list \
    CONFIG.Memory_Type        {Single_Port_ROM} \
    CONFIG.Write_Width_A      {24} \
    CONFIG.Write_Depth_A      {32768} \
    CONFIG.Read_Width_A       {24} \
    CONFIG.Load_Init_File     {true} \
    CONFIG.Coe_File           {logo_rom_data.coe} \
    CONFIG.Use_Byte_Write_Enable {false} \
] [get_ips blk_mem_logo]

# 铁律4: generate_target后必须add_files wrapper
generate_target all [get_ips blk_mem_logo]
add_files -norecurse [get_files $proj_dir/ip/blk_mem_logo/blk_mem_logo_stub.v]

# 铁律5: .coe文件必须加入工程（否则IP找不到初始化数据）
add_files -norecurse $proj_dir/logo_rom_data.coe
```

#### Verilog 例化模板

```verilog
// 例化BMG IP核生成的ROM模块
blk_mem_logo u_logo_rom (
    .clka  (clk),                    // 时钟
    .addra (addr[14:0]),             // 15bit地址 (0~32767)
    .douta (data)                    // 24bit RGB888输出
);
```

#### COE文件格式（BMG IP核专用）

```
memory_initialization_radix=16;
memory_initialization_vector=
FF8800,
FFFFFF,
...,
FFFFFF;   // 最后一行必须有分号
```

#### 5条防崩溃铁律（违反任何一条=综合失败）

| # | 铁律 | 违反后果 | 来源 |
|---|------|---------|------|
| 1 | ROM深度>16384时**禁止**用`$readmemh` | OOM崩溃（日志无Error，进程静默被杀） | 失败#1~#4 |
| 2 | `create_ip -dir`前**必须**`file mkdir` | `IP directory does not exist` | 失败#5 |
| 3 | `generate_target`后**必须**`add_files` wrapper | `module 'xxx' not found` | 失败#6 |
| 4 | **禁止**写死IP版本号 | `version X.Y not found` | 失败#5 |
| 5 | 添加综合约束前**检查是否与已有约束矛盾** | 如`max_bram_cascade_height 1`+深度>16384=物理不可能 | 失败#2 |

#### Vivado综合崩溃的诊断特征

| 现象 | 含义 | 排查方向 |
|------|------|---------|
| 右上角红灯`Synthesis Failed`，但Messages 0 Errors | 综合器进程被OS杀掉（OOM） | 检查Log最后几行是否有`abnormal program termination` |
| 日志在`done synthesizing module`后戛然而止 | Elaboration成功但Optimization阶段OOM | ROM太大，改用BMG IP核 |
| `[Common 17-69] IP directory does not exist` | TCL脚本漏了`file mkdir` | 加`file mkdir $dir` |
| `[Synth 8-439] module 'xxx' not found` | IP wrapper没加入工程 | 加`add_files ..._stub.v` |

## Assertions (SVA)

```systemverilog
// Immediate assertion
always_comb begin
    assert (count < MAX_COUNT) else $error("Count overflow");
end

// Concurrent assertions
property p_valid_handshake;
    @(posedge clk) disable iff (!rst_n)
    valid |-> ##[1:3] ready;
endproperty
assert property (p_valid_handshake) else $error("Handshake timeout");
```

## AXI Protocol & DMA

- Ensure proper read/write channel management and handshakes
- Optimize for high-throughput with proper burst sizing
- Configure burst transfers for maximum throughput
- Handle buffer management efficiently

## Pipelining & Latency

- Implement fine-tuned pipeline stages for performance-critical modules
- Balance pipeline depth with latency requirements
- Use retiming for optimization
- Balance latency vs. throughput requirements

---

# 实战调试经验库（从 17 个真实 Bug 提炼）

> **来源**：ECDH P-192 + AES-128 + SHA-256 + CRC-16 + UART 安全通信系统（DE2-115 Cyclone IV E）的完整调试记录。
> 累计调试约 12 小时，17 个 Bug，其中 CRC 相关 Bug 耗时最长（~6 小时）。
> **铁律：这些规则不是建议，是必须遵守的编码约束。违反即踩坑。**

## Verilog 编码七条铁律（从 17 个 Bug 中提炼）

### 铁律 1：位宽必须精确匹配

`localparam`、`reg`、`wire` 的位宽在比较、赋值、传参时必须完全一致。即使值在范围内，位宽不匹配也会导致综合工具进行隐式截断或零扩展。

**反面案例**：UART RX 过采样计数器用 `reg [2:0]` 存储 16 倍过采样的计数值（需要 0~15），高位被截断导致计数器永远到不了目标值。
**正确做法**：用 `reg [3:0]` 精确匹配 0~15 的范围。写完后用 `verilator --lint-only -Wall` 检查 WIDTH 警告。

### 铁律 2：for 循环变量内外层必须不同名

Verilog 中 `integer i` 的作用域是**整个模块**，不是 begin/end 块。嵌套循环使用同一个变量名会导致内层循环破坏外层循环的迭代变量。

**反面案例**：testbench 的 `send_byte` 任务中，外层循环和内层循环都用 `i`，导致只发送第一个字节就退出。
**正确做法**：外层用 `i`，内层用 `j`，绝不复用。

### 铁律 3：删除 $display 时必须检查 if 独占性

批量移除调试打印语句时，如果 `$display` 是某个 `if` 分支的唯一语句，删除后会留下空 `if` 体，导致下一个 `else` 或语句被意外嵌套到这个 `if` 中。

**反面案例**：删除 `if (debug) $display(...)` 后，下面的 `else` 分支逻辑被吞掉，AUTH_RSP 帧永远发不出。
**正确做法**：每次批量删除 `$display` 后，做一次完整的 diff 审查，检查所有 `if/else` 结构完整性。

### 铁律 4：disable 命名块必须正确包裹目标代码

`disable <label>` 只能退出以 `<label>` 命名的 `begin...end` 块。如果 `for` 循环不在命名块内部，`disable` 不会终止循环。

**反面案例**：testbench 中写 `disable send_byte` 但 `for` 循环在命名块外面，disable 无效导致死循环。
**正确做法**：
```verilog
begin : send_byte_block
    for (i = 0; i < len; i = i + 1) begin
        // ...
    end
end
// 需要提前退出时：
disable send_byte_block;
```

### 铁律 5：异步信号必须至少两级同步

任何来自外部或不同时钟域的信号，使用前必须经过至少两级触发器同步。之后检测边沿必须用 `sig_d1 && !sig_d2`（两级延迟后的边沿检测），不可直接使用原始信号。

**正确做法**：
```verilog
reg sig_d1, sig_d2;
always @(posedge clk) begin
    sig_d1 <= async_sig;
    sig_d2 <= sig_d1;
end
wire sig_rising = sig_d1 & ~sig_d2;  // 安全的边沿检测
```

### 铁律 6：持续高电平信号必须做边沿检测

`done`、`valid`、`ready` 等信号可能持续多个时钟周期为高。直接用 `if (done)` 作为触发条件会导致重复触发。

**反面案例**：`crypto_done` 持续高电平，FSM 在一个周期内连续执行了"等待完成"和"发送下一帧"两个状态的逻辑。
**正确做法**：用 `posedge_crypto_done = crypto_done & ~crypto_done_dly` 做单脉冲触发。

### 铁律 7：测试辅助函数必须与硬件实现完全一致

testbench 中的参考模型（如 CRC 计算函数）必须与硬件实现**在每一个维度上完全一致**，包括：
- **多项式**（如 CRC-16 CCITT-FALSE 用 0x1021，不是 0x8005）
- **位序方向**（MSB-first vs LSB-first）
- **字节输出顺序**（是否做字节交换）

**反面案例（最惨痛的 Bug）**：testbench 的 CRC 参考函数用的是 CRC-16/MODBUS（0x8005, LSB-first, 字节交换），但硬件实现的是 CRC-16/CCITT-FALSE（0x1021, MSB-first, 无字节交换）。两个"正确"的实现在三个维度上全部错配，导致 AUTH_RSP 帧校验永远失败。**累计调试 6 小时。**
**正确做法**：用独立的 Python 脚本计算参考值，三个维度逐一验证，不信任任何"看起来对"的实现。

## CRC 三维校验法（最高优先级）

当涉及 CRC/校验和等协议字段时，必须同时验证以下三个维度，缺一不可：

| 维度 | 说明 | 示例 |
|------|------|------|
| **多项式** | 使用哪个生成多项式 | CRC-16/CCITT-FALSE = 0x1021 vs CRC-16/MODBUS = 0x8005 |
| **位序方向** | MSB-first 还是 LSB-first | 处理每个字节时从高位还是低位开始 |
| **字节输出** | 输出时是否做字节交换 | 低字节在前 vs 高字节在前 |

**验证流程**：
1. 用 Python `crcmod` 或手写函数计算已知输入的 CRC 值
2. 用 testbench 打印硬件计算的 CRC 值
3. 逐维度对比：先对齐多项式，再对齐位序，最后对齐字节交换
4. **禁止**在 testbench 中复用硬件的 CRC 函数作为参考——两个"独立"实现可能共享同一个 Bug

## 五大调试方法论

### 方法论 1：建立独立参考标准

**铁律：不要在错误代码上调试另一个错误代码。**

当硬件行为不对时，用完全独立的语言/工具计算正确值。例如用 Python 计算 CRC、用在线工具验证 AES、用 Wireshark 解析帧格式。只有独立参考才能告诉你谁对谁错。

### 方法论 2：遇到时序问题先画图再看代码

当仿真显示信号时序异常（如握手信号错位、数据延迟不对），**禁止直接读代码试图"看出来"**。先在纸上画出期望的时序图（标注每个时钟沿的信号值），再与实际波形对比，找到第一个分歧点，然后定位到对应代码。

### 方法论 3：追踪根因链，不停在中间原因

Bug 往往是链式传播的。例如：
- AUTH_RSP 校验失败 → CRC 值不对 → testbench 的 CRC 函数字节序反了 → 原因是多项式和位序也对不上 → 根因是参考函数用的是 MODBUS 标准而非 CCITT-FALSE。
- 只修中间原因（比如只修字节交换），过两天又会因为另一个维度不匹配再次失败。

### 方法论 4：多维度问题用参数化交叉验证

当 Bug 涉及多个独立参数（如 CRC 的三个维度），不要一次只改一个参数然后测。用 Python 写参数化脚本，穷举所有组合（2×2×2 = 8 种），找到使硬件和软件输出一致的唯一组合。

### 方法论 5：批量修改后必须做 Diff 审查

批量操作（如删除所有 `$display`、重命名信号、修改参数）后，必须做一次完整的 diff 审查。重点关注：
- 空 `if` 体
- 悬空的 `else` 分支
- 参数传递是否全部更新
- 信号名引用是否全部替换

## 仿真调试优先级（按效率排序）

**铁律：遇到仿真失败，禁止上来就直接看波形。** 波形是最底层的信息来源，效率最低。应按以下顺序排查：

| 优先级 | 排查手段 | 适用场景 |
|--------|---------|---------|
| **P0** | `$display` 输出 | 快速定位超时、CRC 错误值、状态卡住位置 |
| **P1** | 状态机 `state` 值 | 明确 FSM 卡在哪个状态 |
| **P2** | 顶层标志信号 | `frame_valid`、`error_code`、`busy` 等 |
| **P3** | 模块握手信号对齐 | `tx_en` ↔ `tx_done`、`rx_valid` ↔ `frame_ready` |
| **P4** | 底层逐字节波形 | 帧内容 trace、过采样时序检查 |

## 常见陷阱速查表

| 症状 | 最可能原因 | 检查点 |
|------|-----------|--------|
| CRC 校验永远失败 | testbench 和硬件的 CRC 标准不一致 | 对比多项式/位序/字节交换三个维度 |
| UART RX 只收到第一个字节 | for 循环变量冲突（内外层同名 `i`） | 检查 testbench 中所有嵌套循环 |
| 仿真超时但功能似乎正确 | 超时阈值太短或 `done` 信号边沿未检测 | 增大 TIMEOUT；检查是否用了 `posedge` 检测 |
| 状态机跳过某个状态 | 持续高电平信号直接当触发条件 | 用 `sig & ~sig_dly` 做单脉冲 |
| 编译通过但功能错误 | `disable` 命名块未正确包裹循环 | 检查 `begin : label` 是否包裹了 `for` |
| 批量删除 debug 打印后功能异常 | 空 `if` 体导致逻辑错位 | diff 审查所有 if/else 结构 |
| 仿真结果随机不稳定 | 跨时钟域信号未同步 | 检查所有外部输入是否有两级同步器 |

## Testbench 编写陷阱

| 陷阱 | 反面案例 | 正确做法 |
|------|---------|---------|
| 任务中多条语句缺 begin/end | `send_byte` 任务只执行了第一条语句 | 任何包含多条语句的 task/function 必须用 begin/end 包裹 |
| 参数名不一致 | 硬件用 `CLK_FREQ`，testbench 用 `CLK_PERIOD` | 用 `.PARAM_NAME()` 命名端口连接，编译器会报错提醒 |
| 超时太短 | ECDH P-192 标量乘需 34ms，超时设了 30ms | 超时 = 预期最大时间 × 3，留足余量 |
| 缺少边沿捕获 | `rx_done` 是单周期脉冲，用 `@(posedge rx_done)` 永远等不到 | 新增 `rx_captured` 异步捕获寄存器 |

## 关键时序指标（安全通信系统参考）

| 指标 | 数值 | 说明 |
|------|------|------|
| UART 1 字节 @ 115200bps | 86.8 µs | 10 bits / 115200 |
| HELLO 握手帧 | ~4.8 ms | ~55 字节 |
| ECDH P-192 标量乘 | ~34 ms | 最耗时的密码学操作 |
| 完整握手流程 | ~80 ms | 包含 ECDH + AES 密钥派生 |

## Bug 关联关系图（四大家族）

```
家族 1: CRC 失配链（累计 ~6 小时）
  #1 CRC-16 标准错误 → #10 系统 TB CRC 多维不匹配 → #16 TB CRC 字节交换错
  根因：硬件和 testbench 使用了不同的 CRC 标准

家族 2: UART RX 架构崩塌链（累计 ~2 小时）
  #2 过采样计数器位宽不足 → #3 过采样架构 16 倍慢 → #4 停止位提前跳转 → #5 rx_done 脉冲丢失
  根因：过采样时钟架构设计错误，从寄存器位宽开始的连锁反应

家族 3: Testbench 参数不一致链（编译阶段）
  #6 UART RX TB 端口名不匹配
  #7 send_byte 循环变量冲突
  #8 UART TX TB 任务语法错误
  #9 UART TX TB 参数不匹配
  根因：testbench 编写时没有与硬件同步更新

家族 4: 独立 Bug
  #11 仿真超时太短、#12 QSF 路径错误、#13 非阻塞赋值延迟
  #14 ECDH inv_error 处理、#15 disable 命名块错误、#17 空 if 残留
```

---

# Xilinx 7 系列 FPGA 硬核资源知识库（必读）

> **铁律**：所有涉及 FPGA 内部资源举例、架构说明、器件选型的内容，必须以 Xilinx 7 系列为基准。
> Source: 7 Series Product Selection Guide (XMP101 v1.8), UG473, UG479, UG472


## 参考资料（按需读取）

> 以下内容已提取到 `references/` 目录，需要时用 Read 工具读取：

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/xilinx-7series-architecture.md` | 7系列子系列概览、BRAM/DSP48E1/MMCM/GTP架构详解、完整代码示例 | 写Verilog用到硬核资源时 |
| `references/device-selection-guide.md` | Artix-7/Kintex-7/Zynq选型对比、器件手册参考文献 | 项目选型阶段 |
| `references/fpgabuilder-guide.md` | FPGABuilder CLI工具、YAML配置、构建流程、多厂商支持、迁移指南 | 使用FPGABuilder构建项目时 |

---

# 触摸屏 I2C 驱动项目经验库（从 12 个真实 Bug 提炼）

> **来源**：FT6336U 电容触摸屏 I2C 驱动（Xilinx XC7A35T Artix-7，50MHz）的完整调试记录。
> 累计调试约 8 小时，12 个 Bug，覆盖 I2C 协议、多模块接口、三态门、坐标映射等。
> **铁律：这些规则与前面 17 个 Bug 的铁律同等优先级。**

## Verilog 编码补充铁律（从 12 个 Bug 提炼）

### 铁律 8：多模块间共享常量/命令编码必须逐一比对

**来源**：touch_ctrl 发 CMD_START(=1)，i2c_master 收到 CMD_WRITE(=1)。两个模块的命令编码差了 1，整个 I2C 通信全是乱的——FT6336U 从未收到过一个正确的 START 条件。SCL/SDA 一直高电平。

**根因**：两个模块独立编写，各自定义了 CMD 常量，但编码值不一致。没有在集成前做逐一比对。

**铁律**：新建多模块工程时，第一步检查所有共享常量/参数/命令编码的一致性。用文本搜索所有 `localparam CMD_` 或 `parameter CMD_`，列出每个模块的编码表，逐一比对。**不等到综合上板才暴露。**

```verilog
// 正确做法：所有模块引用顶层定义的统一常量
// touchscreen_top.v:
localparam CMD_IDLE     = 3'd0;
localparam CMD_START    = 3'd1;
localparam CMD_WRITE    = 3'd2;
localparam CMD_READ_ACK = 3'd3;
localparam CMD_READ_NAK = 3'd4;
localparam CMD_STOP     = 3'd5;
// i2c_master 和 touch_ctrl 都用这些值，不各自定义
```

### 铁律 9：I2C SDA 三态门必须用 open-drain 写法

**来源**：SDA 三态门用 behavioral 描述 `assign i2c_sda = sda_oe ? sda_out : 1'bz`，Vivado 综合时可能推断为 push-pull 输出。后果：ACK 阶段 FPGA 仍然驱动 SDA=高电平，与 slave 的 ACK（拉低）总线冲突，导致通信失败。偶尔看到 SCL/SDA 有短暂波形然后瞬间变全高。

**铁律**：I2C SDA 必须用 open-drain 写法。FPGA 只驱动低电平，高电平靠外部上拉电阻。

```verilog
// ❌ 错误：push-pull，FPGA 主动驱动 HIGH
assign i2c_sda = sda_oe ? sda_out : 1'bz;

// ✅ 正确：open-drain，FPGA 只驱动 LOW
assign i2c_sda = (sda_oe & ~sda_out) ? 1'b0 : 1'bz;
```

**真值表**：

| sda_oe | sda_out | 行为 | I2C 语义 |
|--------|---------|------|---------|
| 0 | x | 高阻（释放） | ACK 阶段：slave 可以拉低 |
| 1 | 0 | 驱动低 | 发送 0 bit |
| 1 | 1 | 高阻（释放） | 发送 1 bit：pull-up 拉高 |

**XDC 配置**：SDA 引脚必须配置为 open-drain + 上拉：
```tcl
set_property IOSTANDARD LVCMOS33 [get_ports i2c_sda]
set_property PULLTYPE PULLUP [get_ports i2c_sda]
```

### 铁律 10：全局错误检测必须精确匹配当前命令，禁止"每次都检查"

**来源**：touch_ctrl 在 `case` 语句之后放了一段全局 ACK 错误检测：

```verilog
// ❌ 致命：每个时钟周期都执行！
if (i2c_done && !i2c_ack && state != S_CHECK && state != S_PROCESS ...)
    state <= S_ERROR;
```

CMD_START 完成时 `done` 脉冲到达，但 `ack_err` 是上一条命令的残留值（CMD_START 不产生 ACK，ack_err 不会被清除）→ 假阳性 → 状态机被推到 S_ERROR → 短暂 I2C 波形后回到全高。现象就是"偶尔有波形瞬间变全高"。

**铁律**：
1. **禁止**在 `case` 语句之后放全局错误检测
2. 错误检测必须在**当前命令完成的同一个 `case` 分支**内执行
3. 只在 WRITE 设备地址后检查 ACK（CMD_START/CMD_STOP 不产生 ACK，不应检查）

```verilog
// ✅ 正确：在每个关键 I2C 步骤就地检查
S_RD_STA_1: begin  // WRITE device address
    if (i2c_done) begin
        if (!i2c_ack) begin
            state <= S_ERROR;    // Slave 没响应
        end else begin
            state <= S_RD_STA_2; // 正常继续
        end
    end
end
```

### 铁律 11：硬件默认信号不需要 FPGA 引出

**来源**：LCD 驱动工程中 `lcd_rst`、`lcd_bl`、`init_done` 曾错误引出到 FPGA 端口。触摸屏工程中 `touch_rst_n`、`touch_int_n` 又犯了完全一样的错误。

**铁律**：新建模块端口时，强制对照以下"内部信号清单"逐条排除：
- **复位信号**（RST）：上电自动复位，不需要 FPGA 控制
- **背光信号**（BL）：硬件默认打开
- **中断信号**（INT）：用轮询模式时不需要
- **电源/地**（VCC/GND）：硬件连接

只引出**通信线**（I2C 的 SCL/SDA、SPI 的 MOSI/MISO/SCK/CS）和**显示线**（数码管段选/位选）。

### 铁律 12：含中文注释的 .v 文件必须 GBK 编码

**来源**：Vivado 中文 Windows 环境下，UTF-8 编码的 .v 文件打开中文注释全是乱码。Write 工具默认写 UTF-8。

**铁律**：写完含中文注释的 .v 文件后，**必须立即**用 Python 转 GBK：
```python
python3 -c "
with open('file.v', 'r', encoding='utf-8') as f:
    content = f.read()
with open('file.v', 'wb') as f:
    f.write(content.encode('gbk'))
"
```

**注意**：GBK 文件不能用 Edit 工具修改（会清空文件）。修改 GBK 文件必须用 Python 读→改→写。

### 铁律 13：坐标映射常量必须手算边界值验证

**来源**：坐标映射常量 `21845` 实际最大输出是 5 不是 15；`986861` 应该是 98304。三轮修正浪费了大量时间。

**铁律**：任何映射/缩放常量，写完后必须手算 3 个边界值：
- 最小值（0）→ 应该映射到？
- 中间值（max/2）→ 应该映射到？
- 最大值（max）→ 应该映射到？

```verilog
// 验证表（必须写在注释里）：
// (0,0)→(0,0)  (240,160)→(8,8)  (479,319)→(15,15) ✓
// 常量: K_x = 65536 (15×2^21/480), K_y = 98304 (15×2^21/320)
// 公式: touch = (raw × K + 2^20) >> 21  (四舍五入)
```

## I2C 驱动设计陷阱速查表

| 症状 | 最可能原因 | 检查点 |
|------|-----------|--------|
| SCL/SDA 一直高电平 | CMD 编码不匹配，或状态机卡在初始化等待 | 对比两个模块的 CMD 常量；检查初始化延迟 |
| 偶尔有波形然后变全高 | 全局 ACK 错误检测假阳性 | 检查 `case` 后是否有全局 `if (done && !ack)` |
| SCL 有波形但 slave 不 ACK | SDA push-pull（FPGA 不释放总线） | 检查 SDA 三态门是否用 open-drain |
| slave ACK 但数据全是 0xFF | `rd_data` 锁存时序错位 | 追踪 done 脉冲和 rd_data 的更新时序 |
| 坐标只有 0 和 1 | 映射常量错误或位移取位不对 | 手算边界值验证映射公式 |
| cnt 多驱动综合报错 | 两个 always 块同时给 cnt 赋值 | 用 cnt_clr 信号桥接，计数器只在一个块驱动 |
| 状态机卡死不重试 | 无看门狗，I2C 不通时永远等 done | 加 100ms 看门狗超时 |
| touch_ctrl.v 被清空 | GBK 编码操作异常 | 修改 GBK 文件前先 Git 提交备份 |

## I2C 驱动设计检查清单（新建工程必查）

- [ ] CMD 编码：两个模块的命令常量**逐一比对**一致？
- [ ] SDA 三态门：用 open-drain 写法（`sda_oe & ~sda_out`），不是 push-pull？
- [ ] 错误检测：在当前命令的 `case` 分支内就地检查，不是全局检测？
- [ ] 看门狗：I2C 不通时状态机能自动恢复重试？
- [ ] done 脉冲：每个 done 只被消费一次，不会被多个状态误触发？
- [ ] rd_data 锁存：只在 READ 命令的 done 脉冲时 latch，不是每个 done 都 latch？
- [ ] 坐标映射：手算 0、中间值、最大值三个边界点？
- [ ] 硬件默认信号：RST/INT/BL 不引出到 FPGA 端口？
- [ ] GBK 编码：含中文注释的 .v 文件转 GBK 后再给 Vivado？
- [ ] Git 备份：工程目录第一天就 `git init`？

## 触摸屏项目 Bug 关联关系图

```
家族 1: 多模块接口不一致（累计 ~4 小时）
  #9 CMD编码不匹配（START当WRITE执行）
  #5 TD_STATUS未捕获（READ数据被覆盖）
  #6 i2c_ack/i2c_busy端口悬空
  根因：两个模块独立编写，集成前未做接口一致性检查

家族 2: I2C 物理层问题（累计 ~2 小时）
  #10 SDA push-pull（ACK阶段不释放总线）
  #11 全局ACK错误检测假阳性
  根因：I2C open-drain 特性和ACK时序理解不足

家族 3: 坐标映射错误（累计 ~1 小时）
  #2 映射常量21845算错（最大输出5不是15）
  #3 常量986861算错（应该是98304）
  #7 截断丢最大值（需要四舍五入）
  根因：映射常量未手算边界值验证

家族 4: 独立 Bug
  #1 cnt多驱动（两个always块赋值同一reg）
  #4 无看门狗（I2C不通时状态机永久卡死）
  #8 硬件默认信号引出（RST/INT不该引到FPGA）
  #12 GBK编码（Vivado中文环境的编码问题）
```

---

## 20. FPGA 构建自动化模式库（来源：FPGABuilder 开源项目逆向学习）

> 来源：https://github.com/YiHok/FPGABuilder（65星，CC BY-NC-SA 4.0）
> 学习日期：2026-05-25
> 核心价值：把"手写 TCL"升级为"配置驱动 + 模板化 + 自动化"

### 20.1 配置驱动构建（最核心模式）

**问题**：每次 FPGA 项目都从零手写 TCL 脚本，零复用、易出错、不可版本控制。

**解决方案**：YAML 配置文件定义整个项目，工具链自动生成 TCL。

**FPGABuilder 的 fpga_project.yaml 结构**：
```yaml
project:
  name: my_project
  version: "1.0"

fpga:
  vendor: xilinx
  family: artix-7
  part: xc7a35tftg256-1
  top_module: top

source:
  hdl:
    - src/hdl/*.v
    - src/hdl/*.sv
  constraints:
    - src/constraints/*.xdc
  ip_repo_paths:
    - ip_repo

build:
  synthesis:
    strategy: "Vivado Synthesis Defaults"
  implementation:
    options: {}
  hooks:
    pre_synth: "scripts/pre_synth.tcl"
    post_synth: "scripts/post_synth.tcl"
    pre_impl: "scripts/pre_impl.tcl"
    post_impl: "scripts/post_impl.tcl"

programming:
  cable: xilinx_tcf
  target: localhost:3121
```

**铁律**：配置与实现分离——YAML 描述"做什么"，插件实现"怎么做"。

### 20.2 TCL 模板系统

**问题**：TCL 脚本是一大块文本，修改一个参数就要改很多地方。

**解决方案**：把 TCL 脚本拆成独立的模板类，每个模板负责一个构建阶段。

**FPGABuilder 的 6 个模板**：

| 模板 | 职责 | 关键参数 |
|------|------|---------|
| `BasicProjectTemplate` | 创建工程、设器件、IP库路径 | project_name, fpga_part, ip_repo_paths |
| `BDRecoveryTemplate` | Block Design 恢复 + wrapper 生成 | bd_file/tcl_script, is_top, wrapper_language |
| `BuildFlowTemplate` | 综合→实现→比特流完整流程 | synthesis_strategy, impl_options, bitstream_options |
| `CleanTemplate` | 三级清理（soft/hard/all） | clean_level |
| `GUITemplate` | 打开 Vivado GUI | project_dir |
| `ProgramDeviceTemplate` | JTAG/Flash 编程 | cable, target, bitfile |

**组合方式**：
```python
class TCLScriptGenerator:
    def generate_full_build_script(self, files):
        parts = []
        parts.append(BasicProjectTemplate(config).render())   # 1. 创建工程
        parts.append(self._file_add_commands(files))           # 2. 添加文件
        parts.append(BDRecoveryTemplate(config).render())      # 3. BD恢复
        parts.append(self._top_module_setup())                 # 4. 设顶层
        parts.append(BuildFlowTemplate(config).render())       # 5. 构建流程
        return '\n'.join(parts)
```

**铁律**：TCL 脚本应该是"模板组合"的结果，不是"从零手写"的产物。

### 20.3 Hook 系统（构建阶段钩子）

**问题**：在综合前/后、实现前/后需要执行自定义操作，但没有标准化的插入点。

**解决方案**：在构建流程的 6 个关键节点设置钩子。

**6 个钩子点**：
```
pre_build → pre_synth → [综合] → post_synth → pre_impl → [实现+比特流] → post_impl → post_bitstream
```

**智能 TCL/非TCL 分离**（FPGABuilder 的关键设计）：
```python
def _is_tcl_command(self, command):
    tcl_keywords = {'source', 'puts', 'set', 'create_project', 'launch_runs', ...}
    first_word = command.split()[0]
    path = Path(first_word)

    if path.exists() and path.suffix in ['.tcl']:
        return True, f'source {{{command}}}'  # TCL 脚本文件
    elif path.exists() and path.suffix in ['.py', '.bat', '.sh']:
        return False, command  # 非 TCL 脚本
    elif first_word in tcl_keywords:
        return True, command  # TCL 命令
    else:
        return False, command  # 默认非 TCL
```

**铁律**：Hook 系统必须能自动判断命令类型——TCL 命令嵌入脚本，外部脚本用 subprocess 执行。

### 20.4 工具版本适配器

**问题**：不同 Vivado 版本的推荐策略、命令参数、输出格式不同。

**解决方案**：注册表模式，按版本正则匹配自动选择适配器。

```python
# 注册适配器
VersionAdapterRegistry.register("vivado", r"2019\..*", Vivado2019Adapter)
VersionAdapterRegistry.register("vivado", r"2023\..*", Vivado2023Adapter)
VersionAdapterRegistry.register("vivado", r"2024\..*", Vivado2024Adapter)

# 使用
adapter = VersionAdapterRegistry.get_adapter(tool_info)
adapted_config = adapter.adapt_config(config)  # 自动调整策略
```

**每个适配器处理 3 件事**：
1. `adapt_command()` — 适配命令行参数
2. `adapt_config()` — 适配配置（如综合策略名称）
3. `adapt_output()` — 适配输出解析

### 20.5 设备编程封装

**问题**：每次烧录都要手动写一长串 `open_hw_manager` → `connect_hw_server` → ... 的 TCL。

**解决方案**：封装为模板，支持 JTAG 和 Flash 两种模式。

**JTAG 编程流程**（模板化）：
```tcl
open_hw_manager
connect_hw_server -host localhost -port 3121
open_hw_target
set hw_device [lindex [get_hw_devices] 0]
current_hw_device $hw_device
set_property PROGRAM.FILE $bitfile [current_hw_device]
program_hw_devices [current_hw_device]
refresh_hw_device [current_hw_device]
close_hw_target
disconnect_hw_server
close_hw_manager
```

**自动查找 bitstream**：如果用户没指定 `--bitfile`，模板会自动从 `build/bitstreams/` 目录查找 `.bit` 文件。

### 20.6 路径处理铁律（与 CLAUDE.md §4.3 一致）

FPGABuilder 特别注意 Windows 路径问题：
```python
# 构建路径后统一用正斜杠
project_path = f'{project_dir}/{project_name}.xpr'.replace('\\', '/')
```

**铁律**：TCL 脚本中的路径一律用正斜杠 `/`，避免反斜杠在 TCL 中的转义问题。

### 20.7 三级清理模式

| 级别 | 操作 | 适用场景 |
|------|------|---------|
| `soft` | reset_runs + 删 .log/.jou/.str | 日常开发 |
| `hard` | 删整个工程目录 | 重新创建工程 |
| `all` | 删工程 + 所有生成文件 (.bit/.bin/.mcs) | 完全重置 |

**铁律**：清理必须分级，`soft` 是日常默认，`all` 需要确认。

### 20.8 适用场景速查

| 场景 | 应用的模式 |
|------|-----------|
| 新建 FPGA 工程 | 配置驱动 (20.1) + 模板系统 (20.2) |
| 综合前执行自定义脚本 | Hook 系统 (20.3) |
| 切换 Vivado 版本 | 版本适配器 (20.4) |
| 烧录到开发板 | 编程封装 (20.5) |
| 清理构建产物 | 三级清理 (20.7) |
| 跨平台路径问题 | 路径处理 (20.6) |


---

## 21. I2C协议移植铁律（2026-05-25 FT6336U实战）

### 铁律 13：C→Verilog I2C移植必须逐字节对齐
- i2c_master 是**纯字节引擎**，不理解设备地址/寄存器地址的语义区别
- C代码每个  调用 = Verilog 一个独立的 CMD_WRITE 状态
- **禁止合并**：设备地址和寄存器地址必须是两个独立的 CMD_WRITE
- 正确序列：START → WRITE(device_addr) → WRITE(reg_addr) → ReSTART → WRITE(device_addr|1) → READ → STOP

### 铁律 14：禁止在 case 外放全局错误检测
- Verilog 同一 always 块中，最后的赋值覆盖前面的
- case 外的  会覆盖 case 内的正常转移
- ACK 检查必须在每个具体 WRITE 完成的 case 分支内就地检查
- CMD_READ_NAK 的协议性 NAK 不是错误，全局检测会误判

### 铁律 15：I2C SDA 必须是 open-drain
- 错误：（push-pull）
- 正确：（只驱动低）
- idle 时 sda_oe=0（释放总线），不是 sda_oe=1 + sda_out=1

### 调试优先级（信号一直为1）
1. bitstream 是否下载成功（DONE LED）
2. 状态机是否启动（dbg_state != IDLE）
3. I2C 设备地址是否正确（第一个字节）
4. 物理层是否正常（上拉电阻、焊接、走线）
