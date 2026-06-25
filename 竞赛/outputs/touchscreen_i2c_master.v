// ============================================================
// I2C主机模块 —— 字节级软件I2C
//
// 设计依据：
//   1. FT6336U数据手册 Table 2-2 I2C时序特性
//   2. FT6X36寄存器地址手册 §1.2 I2C读写接口描述
//   3. 实验15 ctiic.c 的软件I2C位操作实现
//
// 接口设计思路：
//   提供字节级操作命令，由上层模块(touch_ctrl)组合成完整的I2C事务。
//   这样做的好处：I2C模块只管"发一个字节/收一个字节"，
//   上层模块负责"先发地址再发数据"的协议逻辑，职责分离清晰。
//
// 命令列表：
//   CMD_IDLE    = 000: 产生START条件
//   CMD_START   = 001: 发送一个字节（wr_data），自动等ACK
//   CMD_WRITE   = 010: 读一个字节，发ACK（还有后续字节要读）
//   CMD_READ_ACK= 011: 读一个字节，发NACK（最后一个字节）
//   CMD_READ_NAK= 100: 产生STOP条件
//
// FT6336U读寄存器完整时序示例：
//   [CMD_START] → [CMD_WRITE 0x70] → [CMD_WRITE REG] → [CMD_START]
//   → [CMD_WRITE 0x71] → [CMD_READ_ACK] × (N-1) → [CMD_READ_NAK] → [CMD_STOP]
// ============================================================

module i2c_master (
    input  wire        clk,        // 50MHz系统时钟
    input  wire        rst_n,      // 低电平有效复位

    // 命令接口
    input  wire        cmd_valid,  // 命令有效（高脉冲触发执行）
    input  wire [2:0]  cmd,        // 命令类型
    input  wire [7:0]  wr_data,    // 写数据（CMD_WRITE时使用）
    output reg  [7:0]  rd_data,    // 读数据输出
    output reg         done,       // 命令执行完成脉冲
    output reg         ack_err,    // ACK错误（写入时从机无应答）

    // I2C物理接口
    output reg         scl_out,    // SCL输出
    output reg         sda_out,    // SDA输出
    output reg         sda_oe,     // SDA输出使能（1=驱动，0=高阻/读）
    input  wire        sda_in,     // SDA input (directly read pin)
    output wire [3:0]  dbg_ustate  // I2C state machine state for ILA
);

    // ━━━ 命令编码 ━━━
    localparam CMD_IDLE     = 3'b000;  // No command (must match touch_ctrl)
    localparam CMD_START    = 3'b001;  // Generate START condition
    localparam CMD_WRITE    = 3'b010;  // Write one byte (MSB first)
    localparam CMD_READ_ACK = 3'b011;  // Read one byte, send ACK
    localparam CMD_READ_NAK = 3'b100;  // Read one byte, send NAK
    localparam CMD_STOP     = 3'b101;  // Generate STOP condition

    // ━━━ 时序参数 ━━━
    // FT6336U: SCL频率10~400kHz
    // 50MHz / 200kHz = 250个周期
    localparam DIV = 250;
    localparam HALF = 125;
    localparam CNT_W = $clog2(DIV);

    // ━━━ 微状态 ━━━
    // 每个字节级操作拆成若干个微状态，在每个SCL半周期执行一步
    localparam [3:0]
        U_IDLE      = 4'd0,
        U_START1    = 4'd1,   // SCL高，SDA高
        U_START2    = 4'd2,   // SCL高，SDA拉低
        U_START3    = 4'd3,   // SCL拉低
        U_BIT0      = 4'd4,   // SCL低，放SDA数据
        U_BIT1      = 4'd5,   // SCL拉高
        U_BIT2      = 4'd6,   // SCL拉低，移位
        U_ACK_RD0   = 4'd7,   // 释放SDA
        U_ACK_RD1   = 4'd8,   // SCL拉高，读SDA
        U_ACK_RD2   = 4'd9,   // SCL拉低
        U_ACK_WR0   = 4'd10,  // 发ACK（读模式）或NACK
        U_ACK_WR1   = 4'd11,  // SCL拉高
        U_STOP1     = 4'd12,  // SDA拉低
        U_STOP2     = 4'd13,  // SCL拉高
        U_STOP3     = 4'd14,  // SDA拉高
        U_DONE      = 4'd15;

    reg [3:0]       ustate;
    reg [CNT_W-1:0] cnt;
    reg [2:0]       bit_idx;    // 位计数（7→0，MSB先发）
    reg [7:0]       shift;      // 移位寄存器
    reg             send_ack;   // 读完后发ACK(1)还是NACK(0)
    reg             cnt_clr;    // 清零cnt的请求信号

    assign dbg_ustate = ustate;

    wire tick = (cnt == DIV - 1);
    wire half_tick = (cnt == HALF - 1);

    // ━━━ 分频计数器（cnt只在这一个always块里赋值，杜绝多驱动） ━━━
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            cnt <= 0;
        else if (cnt_clr)
            cnt <= 0;           // 新命令到来时同步清零
        else if (ustate != U_IDLE)
            cnt <= (cnt == DIV - 1) ? 0 : cnt + 1;
        else
            cnt <= 0;
    end

    // ━━━ 主状态机 ━━━
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ustate   <= U_IDLE;
            scl_out  <= 1'b1;
            sda_out  <= 1'b1;
            sda_oe   <= 1'b1;
            done     <= 1'b0;
            ack_err  <= 1'b0;
            rd_data  <= 8'd0;
            shift    <= 8'd0;
            bit_idx  <= 3'd0;
            send_ack <= 1'b0;
            cnt_clr  <= 1'b0;
        end else begin
            done    <= 1'b0;
            cnt_clr <= 1'b0;

            case (ustate)
                // ━━━ 空闲：等待命令 ━━━
                U_IDLE: begin
                    scl_out <= 1'b1;
                    sda_out <= 1'b1;
                    sda_oe  <= 1'b1;
                    ack_err <= 1'b0;

                    if (cmd_valid) begin
                        case (cmd)
                            CMD_START: begin
                                // START条件：SCL高时SDA从高→低
                                sda_out <= 1'b1;
                                scl_out <= 1'b1;
                                sda_oe  <= 1'b1;
                                cnt_clr <= 1'b1;
                                ustate  <= U_START1;
                            end

                            CMD_WRITE: begin
                                // 写一个字节
                                shift   <= wr_data;
                                bit_idx <= 3'd7;
                                sda_out <= wr_data[7];  // 先放MSB到SDA
                                sda_oe  <= 1'b1;
                                scl_out <= 1'b0;        // SCL已经低
                                cnt_clr <= 1'b1;
                                ustate  <= U_BIT0;      // 先到BIT0拉高SCL
                            end

                            CMD_READ_ACK: begin
                                // 读一个字节，最后发ACK
                                send_ack <= 1'b1;
                                bit_idx  <= 3'd7;
                                sda_oe   <= 1'b0;       // 释放SDA，准备读
                                scl_out  <= 1'b0;
                                cnt_clr  <= 1'b1;
                                ustate   <= U_BIT0;     // 先到BIT0拉高SCL
                            end

                            CMD_READ_NAK: begin
                                // 读一个字节，最后发NACK
                                send_ack <= 1'b0;
                                bit_idx  <= 3'd7;
                                sda_oe   <= 1'b0;
                                scl_out  <= 1'b0;
                                cnt_clr  <= 1'b1;
                                ustate   <= U_BIT0;     // 先到BIT0拉高SCL
                            end

                            CMD_STOP: begin
                                // STOP条件：SCL高时SDA从低→高
                                sda_out <= 1'b0;
                                sda_oe  <= 1'b1;
                                scl_out <= 1'b0;
                                cnt_clr <= 1'b1;
                                ustate  <= U_STOP1;
                            end

                            default: begin
                                done   <= 1'b1;
                                ustate <= U_IDLE;
                            end
                        endcase
                    end
                end

                // ━━━ START条件序列 ━━━
                // SCL=1,SDA=1 → SCL=1,SDA=0 → SCL=0
                U_START1: begin  // 保持 SCL=1,SDA=1
                    if (half_tick) begin
                        sda_out <= 1'b0;  // SDA↓ (START)
                        ustate  <= U_START2;
                    end
                end

                U_START2: begin  // 保持 SCL=1,SDA=0
                    if (half_tick) begin
                        scl_out <= 1'b0;  // SCL↓
                        ustate  <= U_START3;
                    end
                end

                U_START3: begin  // SCL=0，START完成
                    if (half_tick) begin
                        done   <= 1'b1;
                        ustate <= U_IDLE;
                    end
                end

                // ━━━ 位传输序列 ━━━
                // 写：SCL低放数据 → SCL高（从机采样） → SCL低移位
                // 读：SCL高（主机采样SDA） → SCL低

                U_BIT0: begin  // SCL低，放数据（写模式）
                    if (tick) begin
                        scl_out <= 1'b1;  // SCL↑
                        ustate  <= U_BIT1;
                    end
                end

                U_BIT1: begin  // SCL高
                    if (half_tick) begin
                        // 读模式：在SCL高电平中间采样SDA
                        if (!sda_oe) begin
                            shift <= {shift[6:0], sda_in};
                        end
                    end
                    if (tick) begin
                        scl_out <= 1'b0;  // SCL↓
                        ustate  <= U_BIT2;
                    end
                end

                U_BIT2: begin  // SCL低，移位
                    if (tick) begin
                        bit_idx <= bit_idx - 1;

                        if (bit_idx == 0) begin
                            // 8位传输完成
                            if (sda_oe) begin
                                // 写模式：需要读ACK
                                sda_oe <= 1'b0;  // 释放SDA
                                ustate <= U_ACK_RD0;
                            end else begin
                                // 读模式：锁存数据，发ACK/NACK
                                // shift在U_BIT1中已移入8位数据，直接用
                                // 不能用{shift[6:0], sda_in}，因为sda_in
                                // 在U_BIT2阶段可能已经变化
                                rd_data <= shift;
                                sda_oe  <= 1'b1;
                                sda_out <= ~send_ack;  // ACK=0, NACK=1
                                ustate  <= U_ACK_WR0;
                            end
                        end else begin
                            // 继续下一位
                            if (sda_oe) begin
                                // 写模式：放下一个bit
                                sda_out <= shift[6];  // 左移后的MSB
                                shift   <= {shift[6:0], 1'b0};
                            end
                            // 读模式：SDA保持释放
                            ustate <= U_BIT0;
                        end
                    end
                end

                // ━━━ 读ACK（写入后检查从机应答） ━━━
                U_ACK_RD0: begin  // 释放SDA，等待从机
                    if (tick) begin
                        scl_out <= 1'b1;  // SCL↑
                        ustate  <= U_ACK_RD1;
                    end
                end

                U_ACK_RD1: begin  // SCL高，读SDA
                    if (half_tick) begin
                        ack_err <= sda_in;  // SDA高=NACK=错误
                    end
                    if (tick) begin
                        scl_out <= 1'b0;  // SCL↓
                        ustate  <= U_ACK_RD2;
                    end
                end

                U_ACK_RD2: begin
                    if (half_tick) begin
                        done   <= 1'b1;
                        ustate <= U_IDLE;
                    end
                end

                // ━━━ 写ACK/NACK（读完一个字节后） ━━━
                U_ACK_WR0: begin  // SCL低，SDA已放好ACK/NACK
                    if (tick) begin
                        scl_out <= 1'b1;  // SCL↑
                        ustate  <= U_ACK_WR1;
                    end
                end

                U_ACK_WR1: begin
                    if (tick) begin
                        scl_out <= 1'b0;  // SCL↓
                        sda_oe  <= 1'b0;  // 释放SDA
                        ustate  <= U_ACK_RD2;  // 复用完成状态
                    end
                end

                // ━━━ STOP条件序列 ━━━
                // SCL低,SDA低 → SCL高 → SDA高
                U_STOP1: begin  // SCL低,SDA低
                    if (half_tick) begin
                        scl_out <= 1'b1;  // SCL↑
                        ustate  <= U_STOP2;
                    end
                end

                U_STOP2: begin  // SCL高,SDA低
                    if (half_tick) begin
                        sda_out <= 1'b1;  // SDA↑ (STOP)
                        ustate  <= U_STOP3;
                    end
                end

                U_STOP3: begin
                    if (half_tick) begin
                        done   <= 1'b1;
                        ustate <= U_IDLE;
                    end
                end

                default: ustate <= U_IDLE;
            endcase
        end
    end

endmodule
