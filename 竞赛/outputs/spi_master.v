// SPI主机模块 —— 把并行数据按SPI协议串行发出去
//
// 工作原理：
//   输入一个9bit的data_in（1bit命令/数据标志 + 8bit有效载荷），
//   模块把它拆成9个bit，通过MOSI线一位一位发给LCD，
//   同时产生SCLK时钟和CS片选信号。
//
// SPI Mode 0 说明（ST7796S用的就是这个模式）：
//   - CPOL=0：空闲时SCLK保持低电平
//   - CPHA=0：数据在SCLK上升沿被从机采样，在下降沿切换
//   - 简单说就是：先摆好数据，再给时钟沿
//
// 时钟分频：
//   系统时钟50MHz，每4个系统时钟翻转一次SCLK → SCLK频率 = 50/4 = 12.5MHz
//   这个频率在ST7796S的数据手册规定的SPI时钟范围内（最高约15MHz）

module spi_master (
    input  wire        clk,       // 系统时钟 50MHz
    input  wire        rst_n,     // 低电平有效复位
    input  wire        start,     // 启动脉冲，拉高一拍开始发送
    input  wire [8:0]  data_in,   // 9bit输入：bit[8]=1数据/0命令，bit[7:0]=实际数据
    output reg         spi_sclk,  // SPI时钟输出
    output reg         spi_mosi,  // SPI数据输出（主机→从机）
    output reg         spi_cs,    // SPI片选（低有效）
    output reg         done       // 发送完成脉冲，高一拍
);

    // 分频计数器：0→1→2→3→0 循环，每个状态一个系统时钟周期
    // 0,1: SCLK低电平阶段；2,3: SCLK高电平阶段
    reg [1:0] clk_cnt;

    // 已发送的bit计数，0~8共9位
    reg [3:0] bit_cnt;

    // 移位寄存器：把data_in锁存进来，然后逐位移出到MOSI
    reg [8:0] shift_reg;

    // busy标志：防止start信号还没结束就被重复触发
    reg       busy;

    // 三段式状态机
    localparam S_IDLE = 2'd0,  // 空闲：等待start信号
               S_SEND = 2'd1,  // 发送：逐bit移出数据
               S_DONE = 2'd2;  // 完成：拉高CS，产生done脉冲

    reg [1:0] state;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state     <= S_IDLE;
            clk_cnt   <= 2'd0;
            bit_cnt   <= 4'd0;
            shift_reg <= 9'd0;
            spi_sclk  <= 1'b0;
            spi_mosi  <= 1'b0;
            spi_cs    <= 1'b1;  // 空闲时CS拉高（不选中从机）
            busy      <= 1'b0;
            done      <= 1'b0;
        end else begin
            done <= 1'b0;  // done默认拉低，只在S_DONE时拉高一拍

            case (state)
                S_IDLE: begin
                    spi_sclk <= 1'b0;  // SPI Mode 0：空闲时SCLK保持低
                    if (start && !busy) begin
                        shift_reg <= data_in;      // 锁存要发送的数据
                        bit_cnt   <= 4'd0;
                        clk_cnt   <= 2'd0;
                        spi_cs    <= 1'b0;          // 拉低CS，开始选中从机
                        spi_mosi  <= data_in[8];    // 先发最高位（bit[8]是命令/数据标志）
                        busy      <= 1'b1;
                        state     <= S_SEND;
                    end
                end

                S_SEND: begin
                    clk_cnt <= clk_cnt + 1'b1;

                    // 4个时钟周期为一个SCLK周期：
                    // cnt=0: SCLK低电平，准备下一个bit的数据
                    // cnt=1: SCLK仍低（建立时间）
                    // cnt=2: SCLK拉高 → 从机在这个上升沿采样MOSI上的数据
                    // cnt=3: SCLK仍高，同时检查是否发完了
                    case (clk_cnt)
                        2'd0: begin
                            spi_sclk <= 1'b0;
                            if (bit_cnt > 4'd0) begin
                                // 移位：把下一位数据挪到bit[8]的位置
                                // 同时bit[7]自动到了MOSI输出位置
                                shift_reg <= {shift_reg[7:0], 1'b0};
                                spi_mosi  <= shift_reg[7];
                            end
                        end
                        2'd2: begin
                            spi_sclk <= 1'b1;  // 上升沿，从机采样
                        end
                        2'd3: begin
                            bit_cnt <= bit_cnt + 1'b1;
                            if (bit_cnt == 4'd8) begin
                                // 9位全部发完（bit_cnt从0到8，共9次）
                                state <= S_DONE;
                            end
                        end
                        default: ;
                    endcase
                end

                S_DONE: begin
                    spi_cs <= 1'b1;  // 拉高CS，结束本次传输
                    busy   <= 1'b0;
                    done   <= 1'b1;  // 通知lcd_ctrl：这一帧发完了
                    state  <= S_IDLE;
                end

                default: state <= S_IDLE;
            endcase
        end
    end

endmodule
