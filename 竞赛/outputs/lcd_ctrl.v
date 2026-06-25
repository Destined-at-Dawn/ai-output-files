// LCD控制器 —— 整个显示驱动的大脑
//
// 这个模块干的事情按时间顺序分三大阶段：
//   1. 复位LCD屏幕（拉低RST引脚，等它稳定）
//   2. 发初始化命令（通过SPI告诉LCD芯片怎么工作）
//   3. 逐像素写显示数据（153600个像素，一个一个发）
//
// 用到的LCD芯片是ST7796S，3.5寸TFT屏，分辨率480×320。
// 初始化命令存在一个20条的ROM里，按顺序发出去就行。
// 像素格式用RGB565（16bit），分高8位和低8位两次SPI传输。

module lcd_ctrl (
    input  wire        clk,         // 系统时钟 50MHz
    input  wire        rst_n,       // 低电平有效复位（已经过顶层两级同步）
    output reg         spi_start,   // 给spi_master的启动脉冲
    output reg  [8:0]  spi_data,    // 给spi_master的数据（bit8=命令/数据标志）
    input  wire        spi_done,    // spi_master发完一帧的应答
    output reg         lcd_rst,     // LCD硬件复位引脚
    output reg         lcd_bl,      // LCD背光控制（最后才开，避免初始化时看到杂画面）
    output reg  [14:0] logo_addr,   // 去logo_rom读数据的地址
    input  wire [15:0] logo_data,   // 从logo_rom读回来的RGB565像素数据
    output wire        init_done    // 初始化完成标志，给外部用
);

    // ━━━ 主状态机 ━━━
    // 共11个状态，走完一轮就显示完一帧图像
    localparam [3:0]
        S_RST_HIGH    = 4'd0,   // 复位预充电：先拉高10ms
        S_RST_LOW     = 4'd1,   // 复位脉冲：拉低20ms
        S_RESET_WAIT  = 4'd2,   // 复位释放后等120ms（芯片内部初始化）
        S_INIT_CMD    = 4'd3,   // 从ROM取命令
        S_INIT_SEND   = 4'd4,   // 等SPI把命令发出去
        S_INIT_WAIT   = 4'd5,   // （保留）
        S_INIT_DELAY  = 4'd6,   // 命令之间的120ms等待
        S_SET_WINDOW  = 4'd7,   // 设置显示窗口（全屏480×320）
        S_WRITE_CMD   = 4'd8,   // 发Memory Write命令（0x2C）
        S_PIXEL_DATA  = 4'd9,   // 逐像素发送显示数据
        S_DONE        = 4'd10;  // 全部完成，开背光

    reg [3:0] state;
    reg       init_done_r;

    // ━━━ 时钟常数 ━━━
    // 系统时钟50MHz，1个时钟周期=20ns
    // 10ms = 500000个周期，20ms = 1000000，120ms = 6000000
    // 仿真时这些值会被tb覆盖成很小的数，加速仿真
    parameter T_10MS  = 500_000;
    parameter T_20MS  = 1_000_000;
    parameter T_120MS = 6_000_000;

    // 延时计数器，最大要数到6000000，需要23bit
    reg [22:0] delay_cnt;

    // ━━━ ST7796S初始化命令ROM ━━━
    // 共20条命令/数据，存在reg数组里
    // 每条10bit，格式：{delay_flag, data_flag, value[7:0]}
    //   delay_flag=1: 发完这条后要等120ms
    //   data_flag =1: 这8bit是数据（不是命令）
    //   data_flag =0: 这8bit是命令
    //
    // 这些命令从ST7796S数据手册里抄的，顺序和参数都不能乱改
    localparam ROM_SIZE = 20;
    reg [9:0] rom [0:ROM_SIZE-1];
    reg [4:0] rom_addr;

    initial begin
        rom[0]  = {1'b1, 1'b0, 8'h00}; // 复位后已经在S_RESET_WAIT等过了，这里是占位
        rom[1]  = {1'b0, 1'b0, 8'h11}; // Sleep Out（0x11）：唤醒LCD，退出睡眠模式
        rom[2]  = {1'b1, 1'b0, 8'h00}; // 等120ms：Sleep Out后LCD需要时间稳定
        rom[3]  = {1'b0, 1'b0, 8'hF0}; // CSCR命令集控制（0xF0）：解锁厂商扩展命令
        rom[4]  = {1'b0, 1'b1, 8'hC3}; // 参数0xC3：解锁第一步
        rom[5]  = {1'b0, 1'b0, 8'hF0}; // 再次发0xF0
        rom[6]  = {1'b0, 1'b1, 8'h96}; // 参数0x96：解锁第二步（必须C3+96配对）
        rom[7]  = {1'b0, 1'b0, 8'h36}; // MADCTL（0x36）：设置显示方向和颜色顺序
        rom[8]  = {1'b0, 1'b1, 8'h48}; // 参数0x48：竖屏，RGB顺序，行列不交换
        rom[9]  = {1'b0, 1'b0, 8'h3A}; // COLMOD（0x3A）：设置像素格式
        rom[10] = {1'b0, 1'b1, 8'h55}; // 参数0x55：16bit/pixel（RGB565格式）
        rom[11] = {1'b0, 1'b0, 8'hB4}; // 显示反转控制（0xB4）
        rom[12] = {1'b0, 1'b1, 8'h01}; // 参数：列反转
        rom[13] = {1'b0, 1'b0, 8'h29}; // Display ON（0x29）：打开显示
        rom[14] = {1'b1, 1'b0, 8'h00}; // 等120ms：让显示稳定
        rom[15] = {1'b0, 1'b0, 8'hF0}; // 再次进入CSCR命令集
        rom[16] = {1'b0, 1'b1, 8'h3C}; // 参数
        rom[17] = {1'b0, 1'b0, 8'hF0}; // 再次CSCR
        rom[18] = {1'b0, 1'b1, 8'h69}; // 参数（这组是ST7796S特定的优化参数）
        rom[19] = {1'b0, 1'b0, 8'h29}; // Display ON（最终确认）
    end

    // 从ROM读出来的字段拆开用
    wire        rom_delay   = rom[rom_addr][9];   // 要不要延时
    wire        rom_is_data = rom[rom_addr][8];   // 是数据还是命令
    wire [7:0]  rom_value   = rom[rom_addr][7:0]; // 实际的命令字节或数据字节

    // ━━━ 窗口设置子状态机 ━━━
    // 设置显示窗口要发两组命令：
    //   列地址（0x2A）+ 起始列高字节 + 起始列低字节 + 结束列高字节 + 结束列低字节
    //   行地址（0x2B）+ 起始行高字节 + 起始行低字节 + 结束行高字节 + 结束行低字节
    // 一共9个SPI帧，用一个子状态机控制
    localparam [2:0]
        W_COL_CMD  = 3'd0,  // 发列地址命令0x2A
        W_COL_SXH  = 3'd1,  // 起始列高字节（0x00）
        W_COL_SXL  = 3'd2,  // 起始列低字节（0x00）
        W_COL_EXH  = 3'd3,  // 结束列高字节（0x01）
        W_COL_EXL  = 3'd4,  // 结束列低字节（0xDF=239→总共0x01DF=479）
        W_ROW_CMD  = 3'd5,  // 发行地址命令0x2B
        W_ROW_DATA = 3'd6;  // 4字节行地址数据

    reg [2:0] win_state;
    reg [2:0] win_cnt;

    // ━━━ 像素坐标 ━━━
    reg [8:0]  pixel_x;    // 当前列 0~479
    reg [8:0]  pixel_y;    // 当前行 0~319
    reg [15:0] pixel_color; // 当前像素的RGB565颜色

    // ━━━ Logo显示参数 ━━━
    // 怎么算的：屏幕480×320，Logo图片173×171
    // 水平居中：(480-173)/2 = 153.5 → 取153
    // 垂直居中：(320-171)/2 = 74.5 → 取74
    localparam LOGO_W       = 9'd173;  // Logo宽度
    localparam LOGO_H       = 9'd171;  // Logo高度
    localparam LOGO_X_START = 9'd153;  // Logo左上角列坐标
    localparam LOGO_X_END   = 9'd325;  // Logo右下角列坐标（153+173-1=325）
    localparam LOGO_Y_START = 9'd74;   // Logo左上角行坐标
    localparam LOGO_Y_END   = 9'd244;  // Logo右下角行坐标（74+171-1=244）
    localparam WHITE_COLOR  = 16'hFFFF; // 白色（RGB565全1）

    // 判断当前像素是否在Logo区域内
    wire in_logo_x = (pixel_x >= LOGO_X_START) && (pixel_x <= LOGO_X_END);
    wire in_logo_y = (pixel_y >= LOGO_Y_START) && (pixel_y <= LOGO_Y_END);
    wire in_logo   = in_logo_x && in_logo_y;

    // ━━━ Logo ROM地址计算 ━━━
    // 把屏幕坐标转换成ROM中的线性地址
    // logo_rel_x/y是相对于Logo左上角的偏移
    // 地址 = 行偏移 × Logo宽度 + 列偏移（一维数组模拟二维）
    //
    // 为什么用乘法？因为Logo宽度173不是2的幂次，不能用移位代替。
    // 综合工具会自动推断成DSP48E1硬核乘法器（(* use_dsp = "yes" *)提示）
    // 7系列FPGA有DSP48E1，做15bit×9bit的乘法只要1个时钟周期
    wire [8:0]  logo_rel_x = pixel_x - LOGO_X_START;
    wire [8:0]  logo_rel_y = pixel_y - LOGO_Y_START;
    (* use_dsp = "yes" *) wire [14:0] logo_addr_next = {6'd0, logo_rel_y} * LOGO_W + {6'd0, logo_rel_x};

    wire       is_high_byte;
    reg        byte_sel;  // 0=发高字节，1=发低字节

    // ━━━ SPI数据组装 ━━━
    // 9bit帧格式：bit[8]是D/C标志（0=命令，1=数据），bit[7:0]是实际数据
    wire [8:0] cmd_frame  = {1'b0, rom_value};       // 命令帧
    wire [8:0] data_frame = {1'b1, rom_value};        // 数据帧
    wire [8:0] pixel_hi   = {1'b1, pixel_color[15:8]}; // 像素高字节
    wire [8:0] pixel_lo   = {1'b1, pixel_color[7:0]};  // 像素低字节

    assign init_done = init_done_r;
    assign is_high_byte = (byte_sel == 1'b0);

    // ━━━ 主状态机 ━━━
    // 整个流程：复位→初始化→设窗口→写像素→完成
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state       <= S_RST_HIGH;
            lcd_rst     <= 1'b1;
            lcd_bl      <= 1'b0;
            spi_start   <= 1'b0;
            spi_data    <= 9'd0;
            delay_cnt   <= 23'd0;
            rom_addr    <= 5'd0;
            win_state   <= 3'd0;
            win_cnt     <= 3'd0;
            pixel_x     <= 9'd0;
            pixel_y     <= 9'd0;
            pixel_color <= 16'd0;
            byte_sel    <= 1'b0;
            logo_addr   <= 15'd0;
            init_done_r <= 1'b0;
        end else begin
            // spi_start默认拉低（脉冲信号，只在需要时拉高一拍）
            spi_start <= 1'b0;

            case (state)
                // ── 阶段一：复位 ──

                // 先拉高10ms：预充电，确保RST引脚处于已知状态
                S_RST_HIGH: begin
                    lcd_rst <= 1'b1;
                    if (delay_cnt == T_10MS - 1) begin
                        delay_cnt <= 23'd0;
                        state     <= S_RST_LOW;
                    end else begin
                        delay_cnt <= delay_cnt + 1'b1;
                    end
                end

                // 拉低20ms：产生复位脉冲，ST7796S要求至少10ms
                S_RST_LOW: begin
                    lcd_rst <= 1'b0;
                    if (delay_cnt == T_20MS - 1) begin
                        delay_cnt <= 23'd0;
                        lcd_rst   <= 1'b1;  // 释放复位
                        state     <= S_RESET_WAIT;
                    end else begin
                        delay_cnt <= delay_cnt + 1'b1;
                    end
                end

                // 复位释放后等120ms：ST7796S内部初始化需要时间
                // 数据手册写了"Wait 120ms after Sleep Out"
                S_RESET_WAIT: begin
                    if (delay_cnt == T_120MS - 1) begin
                        delay_cnt <= 23'd0;
                        rom_addr  <= 5'd0;
                        state     <= S_INIT_CMD;
                    end else begin
                        delay_cnt <= delay_cnt + 1'b1;
                    end
                end

                // ── 阶段二：发送初始化命令 ──

                // 从ROM取命令：如果rom_addr已经到头了，说明初始化完成
                S_INIT_CMD: begin
                    if (rom_addr >= ROM_SIZE) begin
                        init_done_r <= 1'b1;   // 初始化完成
                        win_state   <= 3'd0;   // 准备进入窗口设置
                        win_cnt     <= 3'd0;
                        state       <= S_SET_WINDOW;
                    end else begin
                        // 根据rom_is_data决定发命令帧还是数据帧
                        spi_data  <= rom_is_data ? data_frame : cmd_frame;
                        spi_start <= 1'b1;       // 启动SPI发送
                        state     <= S_INIT_SEND;
                    end
                end

                // 等SPI发完：收到spi_done后，看这条命令要不要延时
                S_INIT_SEND: begin
                    if (spi_done) begin
                        rom_addr <= rom_addr + 1'b1; // 指向下一条
                        if (rom_delay) begin
                            delay_cnt <= 23'd0;
                            state     <= S_INIT_DELAY;  // 需要延时
                        end else begin
                            state <= S_INIT_CMD;        // 直接发下一条
                        end
                    end
                end

                // 命令间120ms延时
                S_INIT_DELAY: begin
                    if (delay_cnt == T_120MS - 1) begin
                        delay_cnt <= 23'd0;
                        state     <= S_INIT_CMD;
                    end else begin
                        delay_cnt <= delay_cnt + 1'b1;
                    end
                end

                // ── 阶段三：设置显示窗口 ──
                // 告诉LCD："我要从第0列第0行开始，到第479列第319行，逐个写像素"
                // 列地址命令0x2A + 4字节参数，行地址命令0x2B + 4字节参数
                S_SET_WINDOW: begin
                    case (win_state)
                        W_COL_CMD: begin
                            spi_data  <= {1'b0, 8'h2A};  // 列地址设置命令
                            spi_start <= 1'b1;
                            win_state <= W_COL_SXH;
                        end
                        W_COL_SXH: if (spi_done) begin
                            spi_data  <= {1'b1, 8'h00};  // 起始列高字节 = 0x00
                            spi_start <= 1'b1;
                            win_state <= W_COL_SXL;
                        end
                        W_COL_SXL: if (spi_done) begin
                            spi_data  <= {1'b1, 8'h00};  // 起始列低字节 = 0x00
                            spi_start <= 1'b1;
                            win_state <= W_COL_EXH;
                        end
                        W_COL_EXH: if (spi_done) begin
                            spi_data  <= {1'b1, 8'h01};  // 结束列高字节 = 0x01
                            spi_start <= 1'b1;
                            win_state <= W_COL_EXL;
                        end
                        W_COL_EXL: if (spi_done) begin
                            spi_data  <= {1'b1, 8'hDF};  // 结束列低字节 = 0xDF（0x01DF=479）
                            spi_start <= 1'b1;
                            win_state <= W_ROW_CMD;
                        end
                        W_ROW_CMD: if (spi_done) begin
                            spi_data  <= {1'b0, 8'h2B};  // 行地址设置命令
                            spi_start <= 1'b1;
                            win_cnt   <= 3'd0;
                            win_state <= W_ROW_DATA;
                        end
                        W_ROW_DATA: if (spi_done) begin
                            case (win_cnt)
                                3'd0: spi_data <= {1'b1, 8'h00};  // 起始行高字节 = 0x00
                                3'd1: spi_data <= {1'b1, 8'h00};  // 起始行低字节 = 0x00
                                3'd2: spi_data <= {1'b1, 8'h01};  // 结束行高字节 = 0x01
                                3'd3: spi_data <= {1'b1, 8'h3F};  // 结束行低字节 = 0x3F（0x013F=319）
                                default: ;
                            endcase
                            spi_start <= 1'b1;
                            if (win_cnt == 3'd3) begin
                                state <= S_WRITE_CMD;  // 窗口设置完成
                            end
                            win_cnt <= win_cnt + 1'b1;
                        end
                        default: win_state <= W_COL_CMD;
                    endcase
                end

                // 发Memory Write命令（0x2C）：告诉LCD"接下来都是像素数据"
                S_WRITE_CMD: begin
                    if (!spi_start) begin
                        spi_data  <= {1'b0, 8'h2C};  // 0x2C = Memory Write
                        spi_start <= 1'b1;
                        pixel_x   <= 9'd0;  // 从(0,0)开始
                        pixel_y   <= 9'd0;
                        byte_sel  <= 1'b0;
                        logo_addr <= 15'd0;
                    end
                    if (spi_done) begin
                        pixel_color <= WHITE_COLOR;  // 默认白色背景
                        state       <= S_PIXEL_DATA;
                    end
                end

                // ── 阶段四：逐像素发送 ──
                // 每个像素分两次SPI传输（高8位+低8位）
                // 总共 480×320 = 153600 个像素，每个2字节 = 307200字节
                //
                // RGB565格式说明：
                //   bit[15:11] = R（5位，0~31）
                //   bit[10:5]  = G（6位，0~63）
                //   bit[4:0]   = B（5位，0~31）
                //   白色 = 0xFFFF = R31 G63 B31
                //
                // byte_sel控制发哪个字节：
                //   byte_sel=0 → 发高字节，然后切到1
                //   byte_sel=1 → 发低字节，然后切到0，同时推进像素坐标
                S_PIXEL_DATA: begin
                    if (spi_done) begin
                        if (byte_sel == 1'b0) begin
                            // 刚发完高字节，接下来发低字节
                            byte_sel <= 1'b1;

                            // 像素坐标推进（在发高字节时就推进，给ROM读取留出时间）
                            if (pixel_x == 9'd479) begin
                                pixel_x <= 9'd0;
                                if (pixel_y == 9'd319) begin
                                    state <= S_DONE;  // 最后一个像素，结束了
                                end else begin
                                    pixel_y <= pixel_y + 1'b1;
                                end
                            end else begin
                                pixel_x <= pixel_x + 1'b1;
                            end

                            // 预取下一个像素的ROM地址
                            // 在同一行内：地址连续递增
                            // 换行时：重新计算新行起始地址 = 行偏移 × 宽度
                            if (pixel_x < 9'd479)
                                logo_addr <= logo_addr_next + 1'b1;
                            else if (pixel_y < 9'd319)
                                logo_addr <= {6'd0, pixel_y + 1'b1 - LOGO_Y_START} * LOGO_W;
                        end else begin
                            // 刚发完低字节，准备下一个像素的颜色
                            byte_sel <= 1'b0;

                            // 根据是否在Logo区域选择颜色
                            if (in_logo)
                                pixel_color <= logo_data;   // 用ROM里的Logo像素
                            else
                                pixel_color <= WHITE_COLOR;  // 不在Logo区域就是白色

                            // 继续预取ROM地址
                            if (pixel_x < 9'd479)
                                logo_addr <= logo_addr_next;
                            else if (pixel_y < 9'd319)
                                logo_addr <= {6'd0, pixel_y + 1'b1 - LOGO_Y_START} * LOGO_W;
                        end
                    end

                    // SPI空闲时就发数据（流水线：这边准备数据，那边发上一个）
                    if (!spi_start && !spi_done) begin
                        if (byte_sel == 1'b0) begin
                            spi_data  <= {1'b1, pixel_color[15:8]}; // 发高字节
                        end else begin
                            spi_data  <= {1'b1, pixel_color[7:0]};  // 发低字节
                        end
                        spi_start <= 1'b1;
                    end
                end

                // 全部完成，开背光
                // 为什么不一开始就开？因为初始化时LCD可能显示随机数据，
                // 先不开背光，等画面准备好了再亮，用户体验好
                S_DONE: begin
                    lcd_bl <= 1'b1;
                end

                default: state <= S_RST_HIGH;
            endcase
        end
    end

endmodule
