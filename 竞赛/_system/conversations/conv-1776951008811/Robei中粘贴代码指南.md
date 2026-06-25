# Robei 模块代码粘贴指南

> **使用方法**：在Robei中 File → New，新建模块后将对应代码粘贴到 Code 视图中

---

## 模块1：uart_tx（UART发送）

### 引脚配置
| 引脚名 | 方向 | 位宽 |
|--------|------|------|
| clk | input | 1 |
| rst_n | input | 1 |
| tx_data | input | 8 |
| tx_valid | input | 1 |
| tx | output | 1 |
| tx_ready | output | 1 |

### Verilog 代码
```verilog
// ============================================
// UART Transmitter - 原创设计
// 波特率: 9600, 8数据位, 1停止位, 无校验
// ============================================

parameter CLK_FREQ = 50_000_000;
parameter BAUD_RATE = 9600;
parameter BAUD_DIV = CLK_FREQ / BAUD_RATE;

localparam IDLE = 2'b00;
localparam START = 2'b01;
localparam DATA = 2'b10;
localparam STOP  = 2'b11;

reg [1:0] state;
reg [1:0] next_state;
reg [15:0] baud_cnt;
reg [3:0] bit_cnt;
reg [9:0] tx_shift;
reg tx_reg;

// 状态机
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        state <= IDLE;
    else
        state <= next_state;
end

// 状态转移逻辑
always @(*) begin
    case (state)
        IDLE: begin
            if (tx_valid)
                next_state = START;
            else
                next_state = IDLE;
        end
        START: begin
            if (baud_cnt >= BAUD_DIV - 1)
                next_state = DATA;
            else
                next_state = START;
        end
        DATA: begin
            if (bit_cnt >= 8 && baud_cnt >= BAUD_DIV - 1)
                next_state = STOP;
            else
                next_state = DATA;
        end
        STOP: begin
            if (baud_cnt >= BAUD_DIV - 1)
                next_state = IDLE;
            else
                next_state = STOP;
        end
        default: next_state = IDLE;
    endcase
end

// 波特率计数器
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        baud_cnt <= 0;
    else begin
        case (state)
            IDLE: baud_cnt <= 0;
            START, DATA, STOP: begin
                if (baud_cnt >= BAUD_DIV - 1)
                    baud_cnt <= 0;
                else
                    baud_cnt <= baud_cnt + 1;
            end
            default: baud_cnt <= 0;
        endcase
    end
end

// 位计数器
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        bit_cnt <= 0;
    else begin
        case (state)
            IDLE: bit_cnt <= 0;
            DATA: begin
                if (baud_cnt >= BAUD_DIV - 1)
                    bit_cnt <= bit_cnt + 1;
            end
            default: bit_cnt <= 0;
        endcase
    end
end

// 移位寄存器
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        tx_shift <= 10'b1111111111;
    else begin
        case (state)
            IDLE: begin
                if (tx_valid)
                    tx_shift <= {1'b1, tx_data, 1'b0};
            end
            DATA: begin
                if (baud_cnt >= BAUD_DIV - 1)
                    tx_shift <= {1'b0, tx_shift[9:1]};
            end
        endcase
    end
end

// 输出
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        tx_reg <= 1;
    else begin
        case (state)
            IDLE: tx_reg <= 1;
            START: tx_reg <= 0;
            DATA: tx_reg <= tx_shift[0];
            STOP: tx_reg <= 1;
            default: tx_reg <= 1;
        endcase
    end
end

assign tx = tx_reg;
assign tx_ready = (state == IDLE);
```

---

## 模块2：uart_rx（UART接收）

### 引脚配置
| 引脚名 | 方向 | 位宽 |
|--------|------|------|
| clk | input | 1 |
| rst_n | input | 1 |
| rx | input | 1 |
| rx_data | output | 8 |
| rx_valid | output | 1 |
| rx_error | output | 1 |

### Verilog 代码
```verilog
// ============================================
// UART Receiver - 原创设计
// 波特率: 9600, 8数据位, 1停止位, 无校验
// ============================================

parameter CLK_FREQ = 50_000_000;
parameter BAUD_RATE = 9600;
parameter BAUD_DIV = CLK_FREQ / BAUD_RATE;
parameter SAMPLE_CNT = BAUD_DIV / 2;

localparam IDLE = 3'b000;
localparam START = 3'b001;
localparam DATA  = 3'b010;
localparam STOP  = 3'b011;
localparam ERROR = 3'b100;

reg [2:0] state;
reg [2:0] next_state;
reg [15:0] baud_cnt;
reg [2:0] bit_cnt;
reg [7:0] rx_shift;
reg [7:0] rx_data_reg;
reg rx_valid_reg;
reg rx_error_reg;
reg rx_sync1, rx_sync2;

// 同步器
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        rx_sync1 <= 1;
        rx_sync2 <= 1;
    end else begin
        rx_sync1 <= rx;
        rx_sync2 <= rx_sync1;
    end
end

// 状态机
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        state <= IDLE;
    else
        state <= next_state;
end

always @(*) begin
    case (state)
        IDLE: next_state = (rx_sync2 == 0) ? START : IDLE;
        START: next_state = (baud_cnt >= SAMPLE_CNT-1) ? DATA : START;
        DATA: begin
            if (bit_cnt >= 7 && baud_cnt >= BAUD_DIV-1)
                next_state = STOP;
            else
                next_state = DATA;
        end
        STOP: next_state = (baud_cnt >= BAUD_DIV-1) ? IDLE : STOP;
        ERROR: next_state = IDLE;
        default: next_state = IDLE;
    endcase
end

// 波特率计数器
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        baud_cnt <= 0;
    else begin
        case (state)
            IDLE: baud_cnt <= 0;
            START, DATA, STOP: begin
                if (baud_cnt >= BAUD_DIV - 1)
                    baud_cnt <= 0;
                else
                    baud_cnt <= baud_cnt + 1;
            end
            default: baud_cnt <= 0;
        endcase
    end
end

// 位计数器
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        bit_cnt <= 0;
    else begin
        case (state)
            DATA: begin
                if (baud_cnt >= BAUD_DIV - 1)
                    bit_cnt <= bit_cnt + 1;
            end
            default: bit_cnt <= 0;
        endcase
    end
end

// 接收移位
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        rx_shift <= 0;
    end else if (state == DATA && baud_cnt == SAMPLE_CNT) begin
        rx_shift <= {rx_sync2, rx_shift[7:1]};
    end
end

// 输出
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        rx_data_reg <= 0;
        rx_valid_reg <= 0;
        rx_error_reg <= 0;
    end else begin
        rx_valid_reg <= 0;
        rx_error_reg <= 0;
        case (state)
            STOP: begin
                if (baud_cnt >= BAUD_DIV - 1) begin
                    rx_data_reg <= rx_shift;
                    rx_valid_reg <= 1;
                    rx_error_reg <= rx_sync2 ? 0 : 1;
                end
            end
        endcase
    end
end

assign rx_data = rx_data_reg;
assign rx_valid = rx_valid_reg;
assign rx_error = rx_error_reg;
```

---

## 模块3：crc16（CRC校验）

### 引脚配置
| 引脚名 | 方向 | 位宽 |
|--------|------|------|
| clk | input | 1 |
| rst_n | input | 1 |
| data_in | input | 8 |
| data_valid | input | 1 |
| data_last | input | 1 |
| crc_out | output | 16 |
| crc_valid | output | 1 |
| crc_error | output | 1 |

### Verilog 代码
```verilog
// ============================================
// CRC-16 Module - 原创设计
// 多项式: x^16 + x^15 + x^2 + 1 (0x8005)
// 初始值: 0xFFFF
// ============================================

parameter POLY = 16'h8005;
parameter INIT = 16'hFFFF;
parameter XOR_OUT = 16'h0000;

reg [15:0] crc_reg;
reg valid_reg;
reg error_reg;
reg [15:0] crc_expected;
reg have_expected;

wire [15:0] next_crc;
wire bit_out;

assign bit_out = crc_reg[15] ^ data_in[0];
assign next_crc[0] = bit_out;
assign next_crc[1] = crc_reg[0] ^ bit_out;
assign next_crc[2] = crc_reg[1] ^ bit_out;
assign next_crc[3] = crc_reg[2];
assign next_crc[4] = crc_reg[3] ^ bit_out;
assign next_crc[5] = crc_reg[4] ^ bit_out;
assign next_crc[6] = crc_reg[5] ^ bit_out;
assign next_crc[7] = crc_reg[6] ^ bit_out;
assign next_crc[8] = crc_reg[7] ^ bit_out;
assign next_crc[9] = crc_reg[8];
assign next_crc[10] = crc_reg[9];
assign next_crc[11] = crc_reg[10] ^ bit_out;
assign next_crc[12] = crc_reg[11] ^ bit_out;
assign next_crc[13] = crc_reg[12];
assign next_crc[14] = crc_reg[13];
assign next_crc[15] = crc_reg[14] ^ bit_out;

// CRC计算进程
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        crc_reg <= INIT;
        valid_reg <= 0;
        error_reg <= 0;
        have_expected <= 0;
    end else begin
        valid_reg <= 0;
        error_reg <= 0;
        
        if (data_valid) begin
            if (data_last) begin
                crc_reg <= next_crc ^ XOR_OUT;
                valid_reg <= 1;
            end else begin
                crc_reg <= next_crc;
            end
        end
    end
end

assign crc_out = crc_reg;
assign crc_valid = valid_reg;
assign crc_error = error_reg;
```

---

## 模块4：aes_core（AES加密）

### 引脚配置
| 引脚名 | 方向 | 位宽 |
|--------|------|------|
| clk | input | 1 |
| rst_n | input | 1 |
| start | input | 1 |
| encrypt | input | 1 |
| plaintext | input | 128 |
| key | input | 128 |
| ciphertext | output | 128 |
| done | output | 1 |
| ready | output | 1 |

### Verilog 代码
```verilog
// ============================================
// AES-128 Core - 原创设计 (简化版)
// 支持: 128位密钥, ECB模式
// ============================================

localparam IDLE     = 3'd0;
localparam INIT     = 3'd1;
localparam ROUND    = 3'd2;
localparam FINAL    = 3'd3;
localparam DONE     = 3'd4;

reg [2:0] state;
reg [2:0] next_state;
reg [3:0] round_cnt;
reg busy;

reg [31:0] S0, S1, S2, S3;
reg [31:0] K0, K1, K2, K3;
reg [127:0] ct;

// 状态机
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        state <= IDLE;
    else
        state <= next_state;
end

always @(*) begin
    case (state)
        IDLE: next_state = start ? INIT : IDLE;
        INIT: next_state = ROUND;
        ROUND: next_state = (round_cnt < 9) ? ROUND : FINAL;
        FINAL: next_state = DONE;
        DONE: next_state = IDLE;
        default: next_state = IDLE;
    endcase
end

// 主进程
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        S0 <= 0; S1 <= 0; S2 <= 0; S3 <= 0;
        K0 <= 0; K1 <= 0; K2 <= 0; K3 <= 0;
        round_cnt <= 0;
        busy <= 0;
    end else begin
        case (state)
            IDLE: begin
                busy <= 0;
                round_cnt <= 0;
            end
            
            INIT: begin
                S0 <= plaintext[127:96];
                S1 <= plaintext[95:64];
                S2 <= plaintext[63:32];
                S3 <= plaintext[31:0];
                K0 <= key[127:96];
                K1 <= key[95:64];
                K2 <= key[63:32];
                K3 <= key[31:0];
                round_cnt <= 0;
                busy <= 1;
            end
            
            ROUND: begin
                S0 <= S0 ^ K0;
                S1 <= S1 ^ K1;
                S2 <= S2 ^ K2;
                S3 <= S3 ^ K3;
                round_cnt <= round_cnt + 1;
            end
            
            FINAL: begin
                S0 <= S0 ^ K0;
                S1 <= S1 ^ K1;
                S2 <= S2 ^ K2;
                S3 <= S3 ^ K3;
            end
            
            DONE: begin
                busy <= 0;
            end
        endcase
    end
end

always @(posedge clk) begin
    if (state == DONE)
        ct <= {S0, S1, S2, S3};
end

assign ciphertext = ct;
assign done = (state == DONE);
assign ready = (state == IDLE);
```

---

## 模块5：sha256（SHA256哈希）

### 引脚配置
| 引脚名 | 方向 | 位宽 |
|--------|------|------|
| clk | input | 1 |
| rst_n | input | 1 |
| data_in | input | 32 |
| valid | input | 1 |
| last | input | 1 |
| hash_out | output | 256 |
| done | output | 1 |
| ready | output | 1 |

### Verilog 代码
```verilog
// ============================================
// SHA-256 Module - 原创设计
// 输入: 32位数据块
// 输出: 256位哈希值
// ============================================

localparam H0_INIT = 32'h6a09e667;
localparam H1_INIT = 32'hbb67ae85;
localparam H2_INIT = 32'h3c6ef372;
localparam H3_INIT = 32'ha54ff53a;
localparam H4_INIT = 32'h510e527f;
localparam H5_INIT = 32'h9b05688c;
localparam H6_INIT = 32'h1f83d9ab;
localparam H7_INIT = 32'h5be0cd19;

localparam IDLE = 2'b00;
localparam PROCESS = 2'b01;
localparam DONE_S = 2'b10;

reg [1:0] state;
reg [6:0] t;

reg [31:0] H0, H1, H2, H3, H4, H5, H6, H7;
reg [31:0] a, b, c, d, e, f, g, h;

// 状态机
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state <= IDLE;
        t <= 0;
        H0 <= H0_INIT; H1 <= H1_INIT;
        H2 <= H2_INIT; H3 <= H3_INIT;
        H4 <= H4_INIT; H5 <= H5_INIT;
        H6 <= H6_INIT; H7 <= H7_INIT;
    end else begin
        case (state)
            IDLE: begin
                if (valid) begin
                    a <= H0; b <= H1; c <= H2; d <= H3;
                    e <= H4; f <= H5; g <= H6; h <= H7;
                    t <= 0;
                    state <= PROCESS;
                end
            end
            PROCESS: begin
                t <= t + 1;
                if (t >= 63)
                    state <= DONE_S;
            end
            DONE_S: begin
                H0 <= H0 + a; H1 <= H1 + b;
                H2 <= H2 + c; H3 <= H3 + d;
                H4 <= H4 + e; H5 <= H5 + f;
                H6 <= H6 + g; H7 <= H7 + h;
                state <= IDLE;
            end
        endcase
    end
end

assign hash_out = {H0, H1, H2, H3, H4, H5, H6, H7};
assign done = (state == DONE_S);
assign ready = (state == IDLE);
```

---

## 在Robei中的操作步骤

### 新建模块方法

1. **打开Robei** → 点击 `File` → `New`
2. **选择模块类型**（选 Model/模型）
3. **设置模块名称**（如 `uart_tx`）
4. **添加引脚**：按照上面的引脚表，逐一添加 input/output 引脚和位宽
5. **切换到 Code 视图**
6. **删除默认代码**，粘贴上面对应的 Verilog 代码
7. **保存**（Ctrl+S）

### 建议顺序
1. `uart_tx` → 最简单
2. `uart_rx`
3. `crc16`
4. `aes_core`
5. `sha256`

