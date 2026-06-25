`timescale 1ns / 1ps

// 测试平台 —— 用软件模拟LCD的行为，验证设计是否正确
//
// TB的思路：
//   1. 例化被测模块（DUT），用参数覆盖把延时缩到200ns
//   2. 监听SPI总线，把LCD收到的每一个9bit帧记录下来
//   3. 统计命令帧数、数据帧数、像素个数
//   4. 检查非Logo区域是否全部白色
//   5. 最后打印PASS/FAIL报告
//
// 为什么要自检验？光看波形太累了，153600个像素肉眼看不过来。
// 自动检查能立刻告诉你哪里出问题。

module tb_lcd_top;

    // 时钟和复位
    reg        sys_clk;
    reg        sys_rst_n;

    // LCD SPI接口（TB会监听这些信号）
    wire       lcd_sclk;
    wire       lcd_mosi;
    wire       lcd_cs;
    wire       lcd_rst;
    wire       lcd_bl;
    wire       init_done;

    // 产生50MHz时钟（周期20ns）
    initial sys_clk = 1'b0;
    always #10 sys_clk = ~sys_clk;

    // 仿真加速：把延时参数覆盖成10个时钟周期（200ns）
    // 这样不用真的等120ms，仿真跑得飞快
    lcd_top #(
        .T_10MS  (10),   // 实际10ms → 仿真200ns
        .T_20MS  (10),   // 实际20ms → 仿真200ns
        .T_120MS (10)    // 实际120ms → 仿真200ns
    ) u_dut (
        .sys_clk    (sys_clk),
        .sys_rst_n  (sys_rst_n),
        .lcd_sclk   (lcd_sclk),
        .lcd_mosi   (lcd_mosi),
        .lcd_cs     (lcd_cs),
        .lcd_rst    (lcd_rst),
        .lcd_bl     (lcd_bl),
        .init_done  (init_done)
    );

    // ━━━ SPI总线监控器 ━━━
    // 模拟LCD接收端：在SCLK上升沿采样MOSI数据，组装成9bit帧
    reg [8:0]  spi_rx_frame;     // 正在接收的帧
    reg [3:0]  spi_bit_cnt;      // 已接收的bit数
    reg        spi_active;       // CS低电平期间=1
    reg        spi_frame_valid;  // 收满9bit时拉高一拍
    reg [8:0]  spi_last_frame;   // 最近一帧完整数据

    // CS下降沿 → 开始接收
    always @(negedge lcd_cs) begin
        spi_active      <= 1'b1;
        spi_bit_cnt     <= 4'd0;
        spi_rx_frame    <= 9'd0;
        spi_frame_valid <= 1'b0;
    end

    // CS上升沿 → 停止接收
    always @(posedge lcd_cs) begin
        spi_active      <= 1'b0;
        spi_frame_valid <= 1'b0;
    end

    // SCLK上升沿 → 采样MOSI（SPI Mode 0，上升沿采样）
    always @(posedge lcd_sclk) begin
        if (spi_active) begin
            spi_rx_frame <= {spi_rx_frame[7:0], lcd_mosi};  // MSB first移入
            spi_bit_cnt  <= spi_bit_cnt + 1'b1;
            if (spi_bit_cnt == 4'd8) begin
                spi_frame_valid <= 1'b1;
                spi_last_frame  <= {spi_rx_frame[7:0], lcd_mosi};
            end else begin
                spi_frame_valid <= 1'b0;
            end
        end
    end

    // ━━━ 统计计数器 ━━━
    integer cmd_count;       // 命令帧总数
    integer data_count;      // 数据帧总数
    integer pixel_hi_count;  // 像素高字节计数
    integer pixel_lo_count;  // 像素低字节计数
    integer total_pixels;    // 完整像素计数
    integer err_count;       // 验证错误计数
    reg     all_pixels_done;

    // 像素坐标跟踪（用于检查非Logo区域是否白色）
    integer pixel_x;
    integer pixel_y;
    reg     expect_hi;       // 下一个应该是高字节

    reg [15:0] captured_color;  // 拼好的RGB565颜色
    reg [7:0]  captured_hi;     // 暂存高字节

    integer cap_x, cap_y;       // 捕获时的坐标

    // 每收到一个9bit帧，做分类统计
    always @(posedge spi_frame_valid) begin
        if (spi_last_frame[8] == 1'b0) begin
            // bit[8]=0 → 命令帧
            cmd_count = cmd_count + 1;
            if (spi_last_frame[7:0] == 8'h2C) begin
                // 收到0x2C（Memory Write）→ 接下来全是像素数据
                pixel_x    <= 0;
                pixel_y    <= 0;
                expect_hi  <= 1'b1;
            end
        end else begin
            // bit[8]=1 → 数据帧
            data_count = data_count + 1;

            if (total_pixels < 153600) begin
                if (expect_hi) begin
                    // 高字节：暂存，等低字节来拼成完整颜色
                    captured_hi    <= spi_last_frame[7:0];
                    expect_hi      <= 1'b0;
                    pixel_hi_count <= pixel_hi_count + 1;
                end else begin
                    // 低字节：和之前存的高字节拼成RGB565
                    captured_color  <= {captured_hi, spi_last_frame[7:0]};
                    pixel_lo_count  <= pixel_lo_count + 1;
                    total_pixels    <= total_pixels + 1;
                    expect_hi       <= 1'b1;

                    // 记录这个像素的坐标（用于后续验证）
                    cap_x <= pixel_x;
                    cap_y <= pixel_y;
                    if (pixel_x == 479) begin
                        pixel_x <= 0;
                        if (pixel_y < 319)
                            pixel_y <= pixel_y + 1;
                    end else begin
                        pixel_x <= pixel_x + 1;
                    end
                end
            end
        end
    end

    // ━━━ 验证逻辑 ━━━
    // 检查：不在Logo区域的像素必须是白色
    // Logo区域：x∈[153,325], y∈[74,244]
    wire cap_in_logo  = (cap_x >= 153) && (cap_x <= 325) &&
                        (cap_y >= 74)  && (cap_y <= 244);
    wire cap_is_white = (captured_color == 16'hFFFF);

    always @(total_pixels) begin
        if (total_pixels > 0 && total_pixels <= 153600) begin
            if (!cap_in_logo && !cap_is_white) begin
                $display("[%0t] ERROR: Non-logo pixel (%0d,%0d) = 0x%04H, expected WHITE",
                         $time, cap_x, cap_y, captured_color);
                err_count = err_count + 1;
            end
        end
    end

    // ━━━ 主测试流程 ━━━
    initial begin
        // 初始化
        cmd_count      = 0;
        data_count     = 0;
        pixel_hi_count = 0;
        pixel_lo_count = 0;
        total_pixels   = 0;
        err_count      = 0;
        pixel_x        = 0;
        pixel_y        = 0;
        expect_hi      = 1'b1;
        captured_color = 16'h0000;
        captured_hi    = 8'h00;
        cap_x          = 0;
        cap_y          = 0;

        // 复位序列
        sys_rst_n = 1'b0;
        #100;
        sys_rst_n = 1'b1;

        // 等初始化完成
        $display("[%0t] Waiting for init_done...", $time);
        wait (init_done == 1'b1);
        $display("[%0t] init_done asserted", $time);

        // 等所有像素传完，或者超时
        // 用fork-join实现两个并行等待，哪个先到算哪个
        all_pixels_done = 1'b0;
        fork : pixel_wait
            begin
                wait (total_pixels >= 153600);
                all_pixels_done = 1'b1;
                $display("[%0t] All %0d pixels transmitted", $time, total_pixels);
                disable pixel_wait;
            end
            begin
                #300_000_000;  // 300ms超时
                if (!all_pixels_done)
                    $display("[%0t] TIMEOUT: Only %0d/153600 pixels in 300ms", $time, total_pixels);
                disable pixel_wait;
            end
        join

        #10000;

        // ━━━ 测试结果汇总 ━━━
        $display("");
        $display("============================================================");
        $display("  LCD Display Driver Testbench - Results");
        $display("============================================================");
        $display("  Command frames:      %0d", cmd_count);
        $display("  Data frames:         %0d", data_count);
        $display("  Pixel high bytes:    %0d", pixel_hi_count);
        $display("  Pixel low bytes:     %0d", pixel_lo_count);
        $display("  Complete pixels:     %0d / 153600", total_pixels);
        $display("  Verification errors: %0d", err_count);
        $display("");

        if (total_pixels >= 153600) begin
            $display("  [PASS] All 153600 pixels transmitted");
        end else begin
            $display("  [FAIL] Only %0d/153600 pixels transmitted", total_pixels);
        end

        if (err_count == 0) begin
            $display("  [PASS] No verification errors");
        end else begin
            $display("  [FAIL] %0d verification errors detected", err_count);
        end

        if (cmd_count > 0) begin
            $display("  [PASS] Commands detected: %0d", cmd_count);
        end else begin
            $display("  [FAIL] No commands detected");
        end

        $display("============================================================");

        if (total_pixels >= 153600 && err_count == 0) begin
            $display("  *** ALL TESTS PASSED ***");
        end else begin
            $display("  *** TEST FAILED ***");
        end
        $display("============================================================");
        $display("");

        #1000;
        $finish;
    end

    // ━━━ 关键事件日志 ━━━
    always @(posedge init_done) begin
        $display("[%0t] >> init_done asserted", $time);
    end

    always @(posedge lcd_bl) begin
        $display("[%0t] >> backlight ON", $time);
    end

    always @(negedge lcd_rst) begin
        $display("[%0t] >> LCD reset ACTIVE (low)", $time);
    end

    always @(posedge lcd_rst) begin
        $display("[%0t] >> LCD reset RELEASED (high)", $time);
    end

    // 每10000个像素打印一次进度
    always @(total_pixels) begin
        if (total_pixels > 0 && total_pixels % 10000 == 0) begin
            $display("[%0t] Progress: %0d/153600 pixels (%0d%%)",
                     $time, total_pixels, total_pixels * 100 / 153600);
        end
    end

endmodule
