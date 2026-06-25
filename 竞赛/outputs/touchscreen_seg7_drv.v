// 7段数码管驱动模块
//
// 功能：
//   1. 4位7段数码管动态扫描
//   2. 扫描频率：1kHz（每位250μs）
//   3. 支持小数点显示
//   4. 共阳极数码管（低电平点亮）
//
// 显示格式：
//   位3  位2  位1  位0
//   X高  X低  Y高  Y低
//
// 段码定义（共阳极，低电平点亮）：
//   a
//   ─
//   f│g│b
//   ─
//   e│ │c
//   ─
//   d
//
//   seg[6]=a, seg[5]=b, seg[4]=c, seg[3]=d
//   seg[2]=e, seg[1]=f, seg[0]=g

module seg7_drv (
    input  wire        clk,        // 50MHz系统时钟
    input  wire        rst_n,      // 低电平有效复位
    input  wire [3:0]  data0,      // 位0显示数据（0-F）
    input  wire [3:0]  data1,      // 位1显示数据（0-F）
    input  wire [3:0]  data2,      // 位2显示数据（0-F）
    input  wire [3:0]  data3,      // 位3显示数据（0-F）
    input  wire [3:0]  dp,         // 小数点控制（1=亮）
    output reg  [6:0]  seg,        // 段选（a-g）
    output reg         dp_out,     // 小数点输出
    output reg  [3:0]  an          // 位选（低有效）
);

    // ━━━ 扫描参数 ━━━
    // 50MHz时钟，1kHz扫描频率
    // 每位显示时间 = 1ms / 4 = 250μs
    // 计数器值 = 50MHz * 250μs = 12,500
    localparam SCAN_CNT = 12_500;
    localparam SCAN_CNT_WIDTH = $clog2(SCAN_CNT);

    // ━━━ 扫描计数器 ━━━
    reg [SCAN_CNT_WIDTH-1:0] scan_cnt;
    reg [1:0] digit_sel;  // 当前显示的位（0-3）

    // 扫描计数器
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            scan_cnt <= 0;
            digit_sel <= 2'd0;
        end else begin
            if (scan_cnt == SCAN_CNT - 1) begin
                scan_cnt <= 0;
                digit_sel <= digit_sel + 1;
            end else begin
                scan_cnt <= scan_cnt + 1;
            end
        end
    end

    // ━━━ 当前显示数据选择 ━━━
    reg [3:0] current_data;

    always @(*) begin
        case (digit_sel)
            2'd0: current_data = data0;
            2'd1: current_data = data1;
            2'd2: current_data = data2;
            2'd3: current_data = data3;
            default: current_data = 4'd0;
        endcase
    end

    // ━━━ 位选信号生成 ━━━
    // 共阳极数码管，低电平选中
    always @(*) begin
        case (digit_sel)
            2'd0: an = 4'b1110;  // 选中位0
            2'd1: an = 4'b1101;  // 选中位1
            2'd2: an = 4'b1011;  // 选中位2
            2'd3: an = 4'b0111;  // 选中位3
            default: an = 4'b1111;
        endcase
    end

    // ━━━ 小数点输出 ━━━
    always @(*) begin
        dp_out = ~dp[digit_sel];  // 共阳极，低电平点亮
    end

    // ━━━ 段码解码 ━━━
    // 共阳极数码管，低电平点亮
    // 段码表：{a, b, c, d, e, f, g}
    always @(*) begin
        case (current_data)
            4'h0: seg = 7'b0000001;  // 0
            4'h1: seg = 7'b1001111;  // 1
            4'h2: seg = 7'b0010010;  // 2
            4'h3: seg = 7'b0000110;  // 3
            4'h4: seg = 7'b1001100;  // 4
            4'h5: seg = 7'b0100100;  // 5
            4'h6: seg = 7'b0100000;  // 6
            4'h7: seg = 7'b0001111;  // 7
            4'h8: seg = 7'b0000000;  // 8
            4'h9: seg = 7'b0000100;  // 9
            4'hA: seg = 7'b0001000;  // A
            4'hB: seg = 7'b1100000;  // b
            4'hC: seg = 7'b0110001;  // C
            4'hD: seg = 7'b1000010;  // d
            4'hE: seg = 7'b0110000;  // E
            4'hF: seg = 7'b0111000;  // F
            default: seg = 7'b1111111;  // 全灭
        endcase
    end

endmodule
