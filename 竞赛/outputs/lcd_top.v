// 顶层模块 —— 把三个子模块连起来
//
// 整体架构：
//
//   sys_clk ──┬──→ [复位同步器] ──→ lcd_ctrl ──→ spi_master ──→ LCD屏幕
//   sys_rst_n─┘                    ?                            (SCLK/MOSI/CS)
//                                  logo_rom
//                                  (BRAM)
//
// 信号流：
//   lcd_ctrl 发起"我要发一帧数据" → spi_master 把9bit并行转成串行发出 → LCD收到
//   lcd_ctrl 说"给我第N个像素的颜色" → logo_rom 从BRAM读出 → lcd_ctrl 拿到颜色继续发
//
// 为什么要这个顶层？
//   实际工程不会把所有逻辑塞一个文件。分模块的好处：
//   1. 各模块可以独立仿真验证
//   2. SPI协议换一个LCD芯片只改lcd_ctrl，spi_master不用动
//   3. Logo换一张图只改ROM的COE文件，其他代码不动

module lcd_top #(
    // 延时参数做成parameter，方便仿真时覆盖成小值加速
    parameter T_10MS  = 500_000,   // 10ms = 500K个时钟周期
    parameter T_20MS  = 1_000_000, // 20ms
    parameter T_120MS = 6_000_000  // 120ms
)(
    input  wire       sys_clk,   // 系统时钟 50MHz
    input  wire       sys_rst_n, // 按键复位（低有效，直接来自引脚）
    output wire       lcd_sclk,  // → LCD SPI时钟
    output wire       lcd_mosi,  // → LCD SPI数据
    output wire       lcd_cs     // → LCD SPI片选
    // 以下三个信号如果需要观察，取消注释即可
    // output wire       lcd_rst,
    // output wire       lcd_bl,
    // output wire       init_done
);

    // ━━━ 复位同步器 ━━━
    // sys_rst_n来自外部按键，是异步信号（跟sys_clk没有时序关系）
    // 直接用异步信号可能在时钟边沿附近产生亚稳态（metastability）
    // 解决办法：过两级D触发器，把亚稳态概率降到极低
    //
    // 为什么两级够了？假设单级MTBF=1ms，两级同步后MTBF≈几年
    // （MTBF = Mean Time Between Failures，平均故障间隔）
    reg [1:0] rst_sync;
    wire      rst_n_sync;

    always @(posedge sys_clk or negedge sys_rst_n) begin
        if (!sys_rst_n)
            rst_sync <= 2'b00;   // 复位时两级都清零
        else
            rst_sync <= {rst_sync[0], 1'b1};  // 1逐级移入
    end

    assign rst_n_sync = rst_sync[1];  // 用第二级输出作为同步后的复位

    // ━━━ 内部连线 ━━━
    wire       spi_start;
    wire [8:0] spi_data;
    wire       spi_done;
    wire [14:0] logo_addr;
    wire [15:0] logo_data;

    // ━━━ LCD控制器 ━━━
    // 负责整个流程：复位→初始化→设窗口→写像素
    lcd_ctrl #(
        .T_10MS  (T_10MS),
        .T_20MS  (T_20MS),
        .T_120MS (T_120MS)
    ) u_lcd_ctrl (
        .clk        (sys_clk),
        .rst_n      (rst_n_sync),    // 用同步后的复位
        .spi_start  (spi_start),
        .spi_data   (spi_data),
        .spi_done   (spi_done),
        .lcd_rst    (lcd_rst),
        .lcd_bl     (lcd_bl),
        .logo_addr  (logo_addr),
        .logo_data  (logo_data),
        .init_done  (init_done)
    );

    // ━━━ SPI主机 ━━━
    // 负责把9bit并行数据转成SPI串行信号
    spi_master u_spi_master (
        .clk        (sys_clk),
        .rst_n      (rst_n_sync),
        .start      (spi_start),
        .data_in    (spi_data),
        .done       (spi_done),
        .spi_sclk   (lcd_sclk),
        .spi_mosi   (lcd_mosi),
        .spi_cs     (lcd_cs)
    );

    // ━━━ Logo ROM ━━━
    // 173×171像素的RGB565图片，存在BRAM里
    // 深度29583，宽度16bit，大约占7个BRAM块
    logo_rom u_logo_rom (
        .clk   (sys_clk),
        .addr  (logo_addr),
        .data  (logo_data)
    );

endmodule
