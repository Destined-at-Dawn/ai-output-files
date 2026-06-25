## 7 系列四大子系列概览

| 子系列 | 代号 | 定位 | 典型应用 |
|--------|------|------|---------|
| Spartan-7 | XC7Sxx | 最低成本+最低功耗 | IoT、传感器接口、简单控制 |
| Artix-7 | XC7Axx | 最佳性价比+收发器优化 | 医疗、工业视觉、LCD驱动、ADC/DAC |
| Kintex-7 | XC7Kxx | 最佳价格性能比 | 通信基站、视频处理、雷达 |
| Virtex-7 | XC7Vxx | 最高性能+最大容量 | 航天、5G、数据中心加速 |

## XC7A35T 关键资源表（Artix-7 中端代表）

| 资源 | 数量 | 说明 | 对应手册 |
|------|------|------|---------|
| Logic Cells | 33,280 | 可配置逻辑块(CLB) | UG474 |
| Slices | 5,200 | 每Slice含4个LUT+8个FF | UG474 |
| CLB Flip-Flops | 41,600 | 寄存器资源 | UG474 |
| Block RAM (36Kb) | 50块 | 可拆为100块18Kb | UG473 |
| Block RAM 总容量 | 1,800 Kb | 含校验位，有效数据1,600Kb | UG473 |
| DSP48E1 Slices | 90 | 25x18乘法+48bit累加 | UG479 |
| CMTs (MMCM+PLL) | 5 | 时钟管理 | UG472 |
| Max Single-Ended I/O | 250 | SelectIO | UG471 |
| Max Differential I/O | 120对 | LVDS | UG471 |
| GTP Transceivers | 4 | 6.6 Gb/s | UG482 |
| XADC | 1 | 12bit 1MSPS ADC | UG480 |
| PCIe Gen2 | 1 | 硬核PCIe | DS181 |

## BRAM 架构（UG473 核心知识）

### 18Kb vs 16Kb 的真相

每块 18Kb BRAM = 16,384 bits 数据区 + 2,048 bits 校验位(Parity)。

```
RAMB18E1 (18,432 bits 总容量)
┌──────────────────────────────────┐
│  Data Array: 16,384 bits (16Kb)  │  ← 这部分存你的数据
├──────────────────────────────────┤
│  Parity Array: 2,048 bits (2Kb)  │  ← ECC校验用，不用则浪费
└──────────────────────────────────┘
```

- 非ECC应用中，每块18Kb BRAM的有效容量 = 16Kb
- 配置模式：Single Port / Simple Dual Port / True Dual Port
- 最大工作频率：Artix-7 约 388-509 MHz（视配置而定）
- **ROM推断**：`(* rom_style = "block" *)` + `initial $readmemh` 即可让综合器自动映射到BRAM

### BRAM用量计算公式

```
所需18Kb块数 = CEILING(总bits / 16,384)

示例：173x171x24bit = 709,992 bits
  709,992 / 16,384 = 43.33 → 44块18Kb BRAM
  占比：44/100 = 44%（XC7A35T有100块18Kb）
```

### BRAM ROM 推断完整代码（XC7A35T 实战示例）

```verilog
// ============================================================
// Module: logo_rom
// Purpose: RGB888 Logo ROM，综合后自动映射到BRAM
// Target:  XC7A35T (100 x 18Kb BRAM)
// Usage:   29583 x 24bit = 709,992 bits → 44块18Kb BRAM
// ============================================================
module logo_rom (
    input  wire        clk,      // 系统时钟
    input  wire [14:0] addr,     // 读地址 0~29582 (15bit足够)
    output reg  [23:0] data      // RGB888像素数据
);

    // 存储阵列声明 — 综合器自动推断为BRAM
    (* rom_style = "block" *)
    reg [23:0] mem [0:29582];

    // 从HEX文件初始化（Vivado会自动找到这个文件）
    initial $readmemh("logo_rom_data.hex", mem);

    // 同步读取（BRAM必须同步读，这是硬性要求）
    always @(posedge clk) begin
        data <= mem[addr];
    end

endmodule
```

**关键要点**：
- `(* rom_style = "block" *)` 告诉综合器**必须**用BRAM实现，不用分布式RAM
- `$readmemh` 的文件路径相对于Vivado工程的 `srcs` 目录，建议把hex文件放到工程根目录
- BRAM只支持**同步读**（必须有时钟沿），不能组合逻辑读取
- 如果不加 `rom_style` 属性，小规模ROM（<64bit）可能被综合为LUT实现

### BRAM RAM 推断完整代码（Simple Dual Port）

```verilog
// ============================================================
// Module: line_buffer
// Purpose: 行缓存，用于图像处理3x3卷积
// Target:  XC7A35T BRAM
// ============================================================
module line_buffer #(
    parameter DATA_WIDTH = 16,    // RGB565
    parameter LINE_LEN   = 480    // 一行480像素
)(
    input  wire                    clk,
    input  wire                    we,       // 写使能
    input  wire [$clog2(LINE_LEN)-1:0] waddr, // 写地址
    input  wire [$clog2(LINE_LEN)-1:0] raddr, // 读地址
    input  wire [DATA_WIDTH-1:0]   wdata,    // 写数据
    output reg  [DATA_WIDTH-1:0]   rdata     // 读数据
);

    reg [DATA_WIDTH-1:0] mem [0:LINE_LEN-1];

    always @(posedge clk) begin
        if (we) mem[waddr] <= wdata;  // 写端口
        rdata <= mem[raddr];           // 读端口（独立地址）
    end

endmodule
```

## DSP48E1 架构（UG479 核心知识）

每个 DSP48E1 Slice 包含：
- **25 x 18 位乘法器**（有符号）
- **48 位累加器/加法器**
- **可选预加法器**（25bit）
- 支持流水线（最多4级寄存器）

### 使用方式

**方式1：代码自动推断**（推荐）
```verilog
(* use_dsp = "yes" *)
wire [14:0] result = operand_a * operand_b + operand_c;
```

**方式2：手动例化原语**
```verilog
DSP48E1 #(
    .A_INPUT("DIRECT"), .B_INPUT("DIRECT"),
    .USE_MULT("MULTIPLY"), .USE_SIMD("ONE48")
) u_dsp (...);
```

### 适用场景
- 坐标计算（如 ROM 地址 = y * width + x）
- 图像处理卷积（3x3滤波）
- FIR/IIR 滤波器系数乘加
- Alpha 混合（pixel_out = pixel_a * alpha + pixel_b * (1-alpha)）
- FFT 蝶形运算

### DSP48E1 完整代码示例（ROM地址计算 + Alpha混合）

**示例1：ROM地址计算（LCD Logo显示）**

```verilog
// ============================================================
// 坐标→ROM地址: addr = y * WIDTH + x
// 用DSP48E1实现乘加，不用LUT搭建乘法器
// ============================================================
module rom_addr_calc #(
    parameter LOGO_W = 173     // Logo宽度
)(
    input  wire        clk,
    input  wire [8:0]  rel_x,  // 0~172 (9bit)
    input  wire [8:0]  rel_y,  // 0~170 (9bit)
    output reg  [14:0] addr    // 0~29582 (15bit)
);

    // 综合属性：强制使用DSP48E1硬核
    (* use_dsp = "yes" *)
    wire [23:0] addr_calc = rel_y * LOGO_W + rel_x;

    always @(posedge clk) begin
        addr <= addr_calc[14:0]; // 截取低15位
    end

endmodule
```

**示例2：Alpha透明度混合（视频叠加）**

```verilog
// ============================================================
// Alpha混合: out = fg * alpha + bg * (256 - alpha)
// fg/bg: RGB888, alpha: 8bit (0=全背景, 255=全前景)
// ============================================================
module alpha_blend (
    input  wire        clk,
    input  wire [23:0] fg_pixel,   // 前景 RGB888
    input  wire [23:0] bg_pixel,   // 背景 RGB888
    input  wire [7:0]  alpha,      // 透明度 0~255
    output reg  [23:0] out_pixel   // 混合结果
);

    // 三个颜色通道分别用DSP48E1做乘加
    (* use_dsp = "yes" *)
    wire [15:0] r_blend = fg_pixel[23:16] * alpha + bg_pixel[23:16] * (8'd255 - alpha);
    (* use_dsp = "yes" *)
    wire [15:0] g_blend = fg_pixel[15:8]  * alpha + bg_pixel[15:8]  * (8'd255 - alpha);
    (* use_dsp = "yes" *)
    wire [15:0] b_blend = fg_pixel[7:0]   * alpha + bg_pixel[7:0]   * (8'd255 - alpha);

    // 除以256（右移8位）得到最终颜色
    always @(posedge clk) begin
        out_pixel <= {r_blend[15:8], g_blend[15:8], b_blend[15:8]};
    end

endmodule
```

**验证方法**：综合后打开 Utilization Report，检查 DSPs 一栏。如果显示用了N个DSP48E1，说明 `(* use_dsp = "yes" *)` 生效。如果显示0，说明综合器用LUT搭了乘法器——检查是否写了 `(* use_dsp = "yes" *)` 属性。

## MMCM/PLL 时钟管理（UG472 核心知识）

XC7A35T 有 5 个 CMT（Clock Management Tile），每个 CMT = 1 MMCM + 1 PLL。

| 特性 | MMCM | PLL |
|------|------|-----|
| 输入频率范围 | 10-800 MHz | 10-800 MHz |
| 输出频率范围 | 4.69-800 MHz | 4.69-800 MHz |
| 分频/倍频 | 整数+小数 | 仅整数 |
| 相位移动 | 精细可调 | 粗调 |
| Jitter | 更低 | 稍高 |

### 使用方式
- **Vivado IP Catalog → Clocking Wizard**：图形化配置
- **Verilog原语**：`MMCME2_ADV` / `PLLE2_ADV`

### 典型应用
- 50MHz → 100MHz 系统时钟倍频
- 生成多相位时钟（DDR接口）
- 生成多个域时钟（如 50MHz逻辑 + 148.5MHz HDMI）

### MMCM/PLL 完整代码示例（Clocking Wizard IP 核输出）

Vivado中通过 IP Catalog → Clocking Wizard 图形化配置后，会生成一个封装模块。以下是直接例化Clocking Wizard的标准写法：

```verilog
// ============================================================
// Module: clk_gen
// Purpose: 50MHz输入 → 100MHz系统时钟 + 25MHz SPI时钟
// 方法：  在Vivado IP Catalog中配置Clocking Wizard后
//         例化其生成的模块（模块名由IP配置决定）
// ============================================================
module clk_gen (
    input  wire  clk_50m_in,    // 板上50MHz晶振
    input  wire  rst_in,        // 外部复位
    output wire  clk_100m,      // 100MHz系统时钟
    output wire  clk_25m,       // 25MHz SPI/外设时钟
    output wire  locked          // PLL锁定标志（高=时钟稳定）
);

    // Clocking Wizard IP核实例化
    // 模块名和端口名取决于IP配置时的命名
    clk_wiz_0 u_clk_wiz (
        .clk_in1  (clk_50m_in),  // 50MHz输入
        .reset    (rst_in),      // 复位
        .clk_out1 (clk_100m),    // 100MHz输出
        .clk_out2 (clk_25m),     // 25MHz输出
        .locked   (locked)       // PLL锁定
    );

endmodule
```

**如果不使用Clocking Wizard IP，直接例化MMCME2_ADV原语**（高级用法）：

```verilog
// ============================================================
// MMCME2_ADV 原语直接例化（50MHz → 100MHz）
// 参考: UG472 Table 2-1 (MMCME2_ADV Port Summary)
// ============================================================
module mmcm_clk_gen (
    input  wire  clk_50m,
    input  wire  rst,
    output wire  clk_100m,
    output wire  locked
);

    wire clk_fb;  // MMCM反馈时钟（必须连）

    MMCME2_ADV #(
        .BANDWIDTH          ("OPTIMIZED"),
        .CLKFBOUT_MULT_F   (20.0),      // VCO = 50MHz × 20 = 1000MHz
        .CLKIN1_PERIOD      (20.0),      // 输入时钟周期20ns = 50MHz
        .CLKOUT0_DIVIDE_F  (10.0),      // 1000MHz / 10 = 100MHz
        .DIVCLK_DIVIDE     (1)          // 输入分频系数
    ) u_mmcm (
        .CLKIN1     (clk_50m),
        .CLKIN2     (1'b0),           // 不用第二输入
        .CLKINSEL   (1'b1),           // 选CLKIN1
        .CLKFBIN    (clk_fb),         // 反馈输入
        .CLKFBOUT   (clk_fb),         // 反馈输出（回环）
        .CLKFBOUTB  (),               // 不用互补反馈
        .CLKOUT0    (clk_100m),       // 100MHz输出
        .CLKOUT0B   (),
        .CLKOUT1    (),               // 未用
        .CLKOUT2    (),
        .CLKOUT3    (),
        .CLKOUT4    (),
        .CLKOUT5    (),
        .CLKOUT6    (),
        .LOCKED     (locked),         // 锁定标志
        .PWRDWN     (1'b0),           // 不关电源
        .RST        (rst),            // 复位
        .DADDR      (7'd0),           // DRP地址（不用动态重配）
        .DCLK       (1'b0),
        .DEN        (1'b0),
        .DI         (16'd0),
        .DO         (),
        .DRDY       (),
        .DWE        (1'b0),
        .PSCLK      (1'b0),           // 动态相移（不用）
        .PSEN       (1'b0),
        .PSINCDEC   (1'b0),
        .PSDONE     ()
    );

endmodule
```

**关键参数公式**：
- VCO频率 = 输入频率 × CLKFBOUT_MULT_F / DIVCLK_DIVIDE
- 输出频率 = VCO频率 / CLKOUTn_DIVIDE
- VCO范围：Artix-7 必须在 600MHz ~ 1200MHz（不在范围内MMCM不会锁定）
- 示例：50MHz × 20 / 1 = 1000MHz VCO → 1000 / 10 = 100MHz 输出

## GTP 高速收发器（UG482）

XC7A35T 有 4 个 GTP Transceiver，单通道最高 6.6 Gb/s。

适用接口协议：PCIe Gen1/Gen2、SATA、SGMII（千兆以太网）、JESD204B

## 硬核资源选择决策表

| 你的需求 | 用什么硬核 | 为什么 |
|---------|-----------|--------|
| 存数据（ROM/RAM/FIFO） | Block RAM | 比分布式RAM大得多，同步读写 |
| 小型查找表/分布式FIFO | 分布式RAM(LUT实现) | 低于64bit时比BRAM高效 |
| 乘法/乘加/MAC | DSP48E1 | 比LUT搭乘法器快3-5倍 |
| 时钟倍频/分频/移相 | MMCM/PLL | 比手动计数器分频抖动小 |
| 高速串行通信 | GTP | PCIe/SATA/千兆以太网必备 |
| 模拟采集（温度/电压） | XADC | 12bit 1MSPS，不用外挂ADC |
| LVDS高速IO | SelectIO | 显示接口、ADC/DAC接口 |

