// touch_ctrl.v - FT6336U touch controller
//
// FT6336U registers:
//   0x02 = TD_STATUS (touch count, 0/1/2)
//   0x03 = P1_XH    [event_flag(7:6)][touch_id(5:4)][X_h(3:0)]
//   0x04 = P1_XL    X_l(7:0)
//   0x05 = P1_YH    [7:4 reserved][Y_h(3:0)]
//   0x06 = P1_YL    Y_l(7:0)
//
// I2C read protocol (matches ctp.c FT6336_RD_Worker):
//   START + WR(0x70) + reg + RepeatedSTART + RD(0x71) + ACK/NAK + STOP
//
// Coordinate mapping (DSP48E1 multiply + shift, rounding):
//   X: raw_x in [0,479], Kx=65536 (15*2^21/480)
//      touch_x = (raw_x * 65536 + 2^20) >> 21  -> 0~15
//   Y: raw_y in [0,319], Ky=98304 (15*2^21/320)
//      touch_y = (raw_y * 98304 + 2^20) >> 21  -> 0~15
//
// Physical: long edge=X(0~479, left-right), short edge=Y(0~319, top-bottom)
//   bottom-left=(0,0)  top-right=(F,F)
//
// COORD_SWAP=0: default (reg0x03->X, reg0x05->Y)
// COORD_SWAP=1: vendor landscape (reg0x03->Y, reg0x05->X)

module touch_ctrl (
    input  wire        clk,
    input  wire        rst_n,

    // I2C master interface
    output reg  [7:0]  i2c_addr_rw,
    output reg  [7:0]  i2c_wr_data,
    output reg         i2c_cmd_valid,
    output reg  [2:0]  i2c_cmd,
    input  wire        i2c_done,
    input  wire        i2c_ack,
    input  wire [7:0]  i2c_rd_data,
    input  wire        i2c_busy,

    // Touch output
    output reg  [3:0]  touch_x,
    output reg  [3:0]  touch_y,
    output reg         touch_valid,

    // Debug (directly observable by ILA)
    output reg  [4:0]  dbg_state,
    output reg  [15:0] dbg_raw_x,
    output reg  [15:0] dbg_raw_y,
    output wire        dbg_activity,
    output wire        dbg_i2c_busy,
    output wire        dbg_i2c_ack
);

    // ---- I2C Command Constants (must match i2c_master.v) ----
    localparam [2:0] CMD_IDLE       = 3'd0,
                     CMD_START      = 3'd1,
                     CMD_WRITE      = 3'd2,
                     CMD_READ_ACK   = 3'd3,
                     CMD_READ_NAK   = 3'd4,
                     CMD_STOP       = 3'd5;

    // ---- FT6336U I2C Address ----
    localparam [7:0] FT_ADDR_W = 8'h70;  // 0x38 << 1
    localparam [7:0] FT_ADDR_R = 8'h71;  // (0x38 << 1) | 1

    // ---- Coordinate Swap ----
    parameter COORD_SWAP = 0;  // 0=normal, 1=swap X and Y

    // ---- Timing ----
    // T_300MS: production=15_000_000 (300ms), debug=10_000 (200us)
    // T_POLL:  production=2_500_000 (50ms),  debug=500_000 (10ms)
    parameter T_300MS_VAL = 0;  // 0=use default, >0=override (for sim)
    parameter T_POLL_VAL  = 0;

    localparam T_300MS = (T_300MS_VAL > 0) ? T_300MS_VAL : 10_000;      // 200us @50MHz
    localparam T_POLL  = (T_POLL_VAL  > 0) ? T_POLL_VAL  : 500_000;     // 10ms @50MHz
    localparam T_WD    = 5_000_000;                                       // 100ms watchdog

    // ---- State Machine ----
    localparam [4:0]
        S_INIT_WAIT  = 5'd0,
        S_IDLE       = 5'd1,
        S_RD_STA_0   = 5'd2,   // read TD_STATUS sequence
        S_RD_STA_1   = 5'd3,
        S_RD_STA_2   = 5'd4,
        S_RD_STA_3   = 5'd5,
        S_RD_STA_4   = 5'd6,
        S_RD_STA_5   = 5'd7,
        S_RD_STA_6   = 5'd8,
        S_CHECK      = 5'd9,
        S_RD_XY_0    = 5'd10,  // read coordinates sequence
        S_RD_XY_1    = 5'd11,
        S_RD_XY_2    = 5'd12,
        S_RD_XY_3    = 5'd13,
        S_RD_XY_4    = 5'd14,
        S_RD_XY_5    = 5'd15,
        S_RD_XY_6    = 5'd16,
        S_RD_XY_7    = 5'd17,
        S_RD_XY_8    = 5'd18,
        S_RD_XY_9    = 5'd19,
        S_PROCESS    = 5'd20,
        S_ERROR      = 5'd21;

    // ---- Registers ----
    reg [4:0]  state;
    reg [31:0] delay_cnt;
    reg [31:0] poll_cnt;
    reg [3:0]  buf_td;       // latched TD_STATUS low nibble
    reg [3:0]  buf_xh;       // byte0 high nibble (X[11:8])
    reg [7:0]  buf_xl;       // byte1 (X[7:0])
    reg [3:0]  buf_yh;       // byte2 high nibble (Y[11:8])
    reg [7:0]  buf_yl;       // byte3 (Y[7:0])
    reg [15:0] raw_x, raw_y;
    reg [36:0] mul_x, mul_y; // 16-bit * 21-bit constant = 37-bit
    reg [3:0]  touch_x_div, touch_y_div;
    reg activity;             // toggle on each successful coordinate read
    reg [31:0] wd_cnt;        // watchdog counter

    // ---- Debug assignments ----
    assign dbg_activity = activity;
    assign dbg_i2c_busy = i2c_busy;
    assign dbg_i2c_ack  = i2c_ack;

    // ---- Watchdog logic ----
    // Active during any state that waits for i2c_done
    wire wd_active = (state == S_RD_STA_1 || state == S_RD_STA_2 ||
                      state == S_RD_STA_3 || state == S_RD_STA_4 ||
                      state == S_RD_STA_5 || state == S_RD_STA_6 ||
                      state == S_CHECK    ||
                      state == S_RD_XY_1  || state == S_RD_XY_2  ||
                      state == S_RD_XY_3  || state == S_RD_XY_4  ||
                      state == S_RD_XY_5  || state == S_RD_XY_6  ||
                      state == S_RD_XY_7  || state == S_RD_XY_8  ||
                      state == S_RD_XY_9);
    wire wd_rst = (wd_cnt >= T_WD);

    // ---- Coordinate Mapping (registered 2-cycle pipeline) ----
    // Cycle 1: multiply + add rounding bias
    // Cycle 2: shift right 21 bits
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mul_x       <= 37'd0;
            mul_y       <= 37'd0;
            touch_x_div <= 4'd0;
            touch_y_div <= 4'd0;
        end else begin
            if (state == S_PROCESS) begin
                mul_x <= raw_x * 65536 + 1048576;  // raw_x * Kx + 2^20
                mul_y <= raw_y * 98304 + 1048576;  // raw_y * Ky + 2^20
            end
            touch_x_div <= mul_x[36:21];  // >> 21
            touch_y_div <= mul_y[36:21];  // >> 21
        end
    end

    // ---- Main State Machine ----
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state        <= S_INIT_WAIT;
            delay_cnt    <= 32'd0;
            poll_cnt     <= 32'd0;
            i2c_cmd_valid <= 1'b0;
            i2c_cmd      <= CMD_IDLE;
            i2c_addr_rw  <= 8'd0;
            i2c_wr_data  <= 8'd0;
            buf_td       <= 4'd0;
            buf_xh       <= 4'd0;
            buf_xl       <= 8'd0;
            buf_yh       <= 4'd0;
            buf_yl       <= 8'd0;
            raw_x        <= 16'd0;
            raw_y        <= 16'd0;
            touch_x      <= 4'd0;
            touch_y      <= 4'd0;
            touch_valid   <= 1'b0;
            dbg_state    <= S_INIT_WAIT;
            dbg_raw_x    <= 16'd0;
            dbg_raw_y    <= 16'd0;
            activity     <= 1'b0;
            wd_cnt       <= 32'd0;
        end else begin
            // Default: deassert cmd_valid and touch_valid every cycle
            i2c_cmd_valid <= 1'b0;
            touch_valid   <= 1'b0;
            dbg_state     <= state;

            // Watchdog counter
            if (wd_active) begin
                if (wd_cnt < T_WD)
                    wd_cnt <= wd_cnt + 1;
            end else begin
                wd_cnt <= 32'd0;
            end

            // Watchdog: force back to S_IDLE if stuck waiting for i2c_done
            if (wd_rst && wd_active) begin
                state  <= S_IDLE;
                wd_cnt <= 32'd0;
            end else begin

            case (state)
                // ===== INIT WAIT (300ms power-on, reduced to 200us for debug) =====
                S_INIT_WAIT: begin
                    if (delay_cnt < T_300MS)
                        delay_cnt <= delay_cnt + 1;
                    else begin
                        delay_cnt <= 32'd0;
                        state     <= S_IDLE;
                    end
                end

                // ===== IDLE (poll interval between reads) =====
                S_IDLE: begin
                    if (poll_cnt < T_POLL)
                        poll_cnt <= poll_cnt + 1;
                    else begin
                        poll_cnt <= 32'd0;
                        state    <= S_RD_STA_0;
                    end
                end

                // ===== READ TD_STATUS (reg 0x02, 1 byte) =====
                S_RD_STA_0: begin  // START
                    i2c_cmd_valid <= 1'b1;
                    i2c_cmd       <= CMD_START;
                    i2c_addr_rw   <= FT_ADDR_W;
                    i2c_wr_data   <= 8'h02;
                    state <= S_RD_STA_1;
                end
                S_RD_STA_1: begin  // WRITE device address
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_WRITE;
                        i2c_addr_rw   <= FT_ADDR_W;
                        i2c_wr_data   <= 8'h02;
                        state <= S_RD_STA_2;
                    end
                end
                S_RD_STA_2: begin  // WRITE register address 0x02
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_START;  // Repeated START
                        i2c_addr_rw   <= FT_ADDR_R;
                        i2c_wr_data   <= 8'h00;
                        state <= S_RD_STA_3;
                    end
                end
                S_RD_STA_3: begin  // Repeated START
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_WRITE;  // Write read-address
                        i2c_addr_rw   <= FT_ADDR_R;
                        i2c_wr_data   <= 8'h00;
                        state <= S_RD_STA_4;
                    end
                end
                S_RD_STA_4: begin  // WRITE read-address byte
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_READ_NAK;  // Read 1 byte, NAK (last byte)
                        state <= S_RD_STA_5;
                    end
                end
                S_RD_STA_5: begin  // READ TD_STATUS byte
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_STOP;
                        state <= S_RD_STA_6;
                    end
                end
                S_RD_STA_6: begin  // STOP completed
                    if (i2c_done) begin
                        buf_td <= i2c_rd_data[3:0];  // LATCH: TD_STATUS low nibble
                        state <= S_CHECK;
                    end
                end

                // ===== CHECK touch count =====
                S_CHECK: begin
                    if (buf_td > 0)
                        state <= S_RD_XY_0;   // Touch detected, read coordinates
                    else
                        state <= S_IDLE;      // No touch, back to poll
                end

                // ===== READ COORDINATES (reg 0x03, 4 bytes with ACK) =====
                S_RD_XY_0: begin  // START
                    i2c_cmd_valid <= 1'b1;
                    i2c_cmd       <= CMD_START;
                    i2c_addr_rw   <= FT_ADDR_W;
                    i2c_wr_data   <= 8'h03;
                    state <= S_RD_XY_1;
                end
                S_RD_XY_1: begin  // WRITE device address
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_WRITE;
                        i2c_addr_rw   <= FT_ADDR_W;
                        i2c_wr_data   <= 8'h03;
                        state <= S_RD_XY_2;
                    end
                end
                S_RD_XY_2: begin  // WRITE register address 0x03
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_START;  // Repeated START
                        i2c_addr_rw   <= FT_ADDR_R;
                        i2c_wr_data   <= 8'h00;
                        state <= S_RD_XY_3;
                    end
                end
                S_RD_XY_3: begin  // Repeated START
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_WRITE;  // Write read-address
                        i2c_addr_rw   <= FT_ADDR_R;
                        i2c_wr_data   <= 8'h00;
                        state <= S_RD_XY_4;
                    end
                end
                S_RD_XY_4: begin  // WRITE read-address byte
                    if (i2c_done) begin
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_READ_ACK;  // Read byte0, ACK (more bytes follow)
                        state <= S_RD_XY_5;
                    end
                end
                S_RD_XY_5: begin  // READ byte0 (P1_XH): X[11:8] in [3:0]
                    if (i2c_done) begin
                        buf_xh <= i2c_rd_data[3:0];  // LATCH: X high nibble
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_READ_ACK;
                        state <= S_RD_XY_6;
                    end
                end
                S_RD_XY_6: begin  // READ byte1 (P1_XL): X[7:0]
                    if (i2c_done) begin
                        buf_xl <= i2c_rd_data;  // LATCH: X low byte
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_READ_ACK;
                        state <= S_RD_XY_7;
                    end
                end
                S_RD_XY_7: begin  // READ byte2 (P1_YH): Y[11:8] in [3:0]
                    if (i2c_done) begin
                        buf_yh <= i2c_rd_data[3:0];  // LATCH: Y high nibble
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_READ_NAK;  // Last byte, send NAK
                        state <= S_RD_XY_8;
                    end
                end
                S_RD_XY_8: begin  // READ byte3 (P1_YL): Y[7:0]
                    if (i2c_done) begin
                        buf_yl <= i2c_rd_data;  // LATCH: Y low byte
                        i2c_cmd_valid <= 1'b1;
                        i2c_cmd       <= CMD_STOP;
                        state <= S_RD_XY_9;
                    end
                end
                S_RD_XY_9: begin  // STOP completed
                    if (i2c_done) begin
                        // Assemble 12-bit coordinates
                        if (COORD_SWAP == 0) begin
                            // Normal: reg0x03->X(long edge), reg0x05->Y(short edge)
                            raw_x <= {buf_xh, buf_xl};  // 12-bit X
                            raw_y <= {buf_yh, buf_yl};  // 12-bit Y
                        end else begin
                            // Landscape swap: reg0x03->Y, reg0x05->X
                            raw_y <= {buf_xh, buf_xl};
                            raw_x <= {buf_yh, buf_yl};
                        end
                        state <= S_PROCESS;
                    end
                end

                // ===== PROCESS: coordinate mapping =====
                S_PROCESS: begin
                    touch_x     <= touch_x_div;  // Mapped 0~15
                    touch_y     <= touch_y_div;
                    touch_valid  <= 1'b1;         // Pulse: new data ready
                    activity    <= ~activity;     // Toggle for ILA observation
                    dbg_raw_x   <= raw_x;
                    dbg_raw_y   <= raw_y;
                    state       <= S_IDLE;
                end

                // ===== ERROR: I2C NACK or timeout, retry after delay =====
                S_ERROR: begin
                    if (delay_cnt < T_300MS)
                        delay_cnt <= delay_cnt + 1;
                    else begin
                        delay_cnt <= 32'd0;
                        state     <= S_IDLE;
                    end
                end

                default: state <= S_IDLE;
            endcase

            // ACK error detection: if I2C gets NAK unexpectedly, go to ERROR
            if (i2c_done && !i2c_ack && state != S_CHECK && state != S_PROCESS
                         && state != S_RD_STA_6 && state != S_RD_XY_9)
                state <= S_ERROR;

            end // else !wd_rst
        end
    end

endmodule
