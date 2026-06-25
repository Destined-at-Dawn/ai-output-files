// touchscreen_top.v
// Top module: reset synchronizer + touch_ctrl + i2c_master + seg7_drv
//
// External ports (4 signals, same style as lcd_top):
//   sys_clk, sys_rst_n, i2c_scl, i2c_sda, seg[6:0], dp, an[3:0]
//
// Hardware-default signals (NOT connected, same lesson as lcd_rst/lcd_bl):
//   FT6336U RST, INT, VCC, GND -> module handles by itself
//
// System architecture:
//
//   sys_clk ---> [reset sync] ---> rst_n_sync
//                                     |
//   rst_n_sync ---> [touch_ctrl] ---> I2C cmd/if ---> [i2c_master] ---> FT6336U
//                      |                                   |             (I2C bus)
//                   touch_x/y ---> [seg7_drv] ---> 7-segment display
//
// Signal flow:
//   touch_ctrl issues I2C commands (START/WRITE/READ/STOP)
//   -> i2c_master drives SCL/SDA at bit level
//   -> FT6336U responds with touch data
//   -> touch_ctrl parses coordinates -> seg7_drv displays

module touchscreen_top #(
    parameter T_300MS_OVERRIDE = 0,  // 0=use default, >0=override
    parameter T_POLL_OVERRIDE  = 0,
    parameter T_WD_OVERRIDE    = 0
) (
    input  wire        sys_clk,     // 50MHz system clock (W19)
    input  wire        sys_rst_n,   // Active-low reset (Y19=PB0)

    // I2C interface to FT6336U (only 2 signals needed)
    output wire        i2c_scl,     // I2C clock
    inout  wire        i2c_sda,     // I2C data (bidirectional, tri-state)

    // 7-segment display
    output wire [6:0]  seg,         // Segment select (a-g)
    output wire        dp,          // Decimal point
    output wire [3:0]  an           // Digit select (active low)
);

    // ============================================
    // ILA debug signals (MARK_DEBUG for Vivado auto-detect)
    // Trigger on dbg_cmd_valid rising edge to catch I2C activity
    // If SCL/SDA always high with no activity -> check dbg_rst_n, dbg_state
    // ============================================
    (* MARK_DEBUG = "TRUE" *) wire       dbg_scl;
    (* MARK_DEBUG = "TRUE" *) wire       dbg_sda_in;
    (* MARK_DEBUG = "TRUE" *) wire       dbg_sda_out;
    (* MARK_DEBUG = "TRUE" *) wire       dbg_sda_oe;
    (* MARK_DEBUG = "TRUE" *) wire       dbg_cmd_valid;
    (* MARK_DEBUG = "TRUE" *) wire [3:0] dbg_im_ustate;  // I2C master internal state
    (* MARK_DEBUG = "TRUE" *) wire [4:0] dbg_tc_state;   // touch_ctrl state
    (* MARK_DEBUG = "TRUE" *) wire       dbg_touch_valid;
    (* MARK_DEBUG = "TRUE" *) wire [3:0] dbg_touch_x;
    (* MARK_DEBUG = "TRUE" *) wire [3:0] dbg_touch_y;
    (* MARK_DEBUG = "TRUE" *) wire       dbg_i2c_busy;   // I2C master busy
    (* MARK_DEBUG = "TRUE" *) wire       dbg_i2c_ack;    // last I2C got ACK
    (* MARK_DEBUG = "TRUE" *) wire       dbg_activity;   // toggle on each read
    (* MARK_DEBUG = "TRUE" *) wire       dbg_rst_n;      // reset sync output
    (* MARK_DEBUG = "TRUE" *) wire [3:0] dbg_i2c_raw;    // {scl_out, sda_out, sda_oe, sda_in}

    // ============================================
    // Reset Synchronizer
    // ============================================
    reg [1:0] rst_sync;
    wire      rst_n_sync;

    always @(posedge sys_clk or negedge sys_rst_n) begin
        if (!sys_rst_n)
            rst_sync <= 2'b00;
        else
            rst_sync <= {rst_sync[0], 1'b1};
    end

    assign rst_n_sync = rst_sync[1];

    // ============================================
    // I2C internal interface wires
    // ============================================
    wire       i2c_cmd_valid;
    wire [2:0] i2c_cmd;
    wire [7:0] i2c_wr_data;
    wire [7:0] i2c_rd_data;
    wire       i2c_done;
    wire       i2c_ack_err;   // 1=NAK (error), 0=ACK (success)
    wire       i2c_ack;       // 1=ACK (success), inverted from ack_err

    // I2C physical signals
    wire       scl_out;
    wire       sda_out;
    wire       sda_oe;
    wire       sda_in;

    // I2C master internal state for ILA
    wire [3:0] i2c_ustate;

    // Coordinate signals
    wire [3:0] touch_x;
    wire [3:0] touch_y;
    wire       touch_valid;

    // ACK inversion: touch_ctrl uses i2c_ack (1=success), i2c_master uses ack_err (1=fail)
    assign i2c_ack = ~i2c_ack_err;

    // I2C busy: any state except IDLE(0) and DONE(15)
    wire i2c_busy = (i2c_ustate != 4'd0) && (i2c_ustate != 4'd15);

    // ============================================
    // ILA signal assignments
    // ============================================
    assign dbg_scl       = scl_out;
    assign dbg_sda_in    = sda_in;
    assign dbg_sda_out   = sda_out;
    assign dbg_sda_oe    = sda_oe;
    assign dbg_cmd_valid = i2c_cmd_valid;
    assign dbg_im_ustate = i2c_ustate;
    assign dbg_tc_state  = tc_state;
    assign dbg_touch_x   = touch_x;
    assign dbg_touch_y   = touch_y;
    assign dbg_i2c_busy  = i2c_busy;
    assign dbg_i2c_ack   = i2c_ack;
    assign dbg_activity  = tc_activity;
    assign dbg_touch_valid = touch_valid;
    assign dbg_rst_n     = rst_n_sync;
    assign dbg_i2c_raw   = {scl_out, sda_out, sda_oe, sda_in};

    // ============================================
    // SDA tri-state buffer
    // sda_oe=1: FPGA drives SDA (sda_out)
    // sda_oe=0: release SDA (external pull-up)
    // ============================================
    assign i2c_sda = sda_oe ? sda_out : 1'bz;
    assign sda_in  = i2c_sda;      // Always read SDA state
    assign i2c_scl = scl_out;      // SCL direct drive

    // ============================================
    // Touch controller internal signals for debug
    // ============================================
    wire [4:0] tc_state;
    wire [15:0] tc_raw_x, tc_raw_y;
    wire       tc_activity;

    // ============================================
    // I2C Master Instance
    // ============================================
    i2c_master u_i2c_master (
        .clk        (sys_clk),
        .rst_n      (rst_n_sync),
        .cmd_valid  (i2c_cmd_valid),
        .cmd        (i2c_cmd),
        .wr_data    (i2c_wr_data),
        .rd_data    (i2c_rd_data),
        .done       (i2c_done),
        .ack_err    (i2c_ack_err),
        .scl_out    (scl_out),
        .sda_out    (sda_out),
        .sda_oe     (sda_oe),
        .sda_in     (sda_in),
        .dbg_ustate (i2c_ustate)
    );

    // ============================================
    // Touch Controller Instance
    // RST/INT: hardware default, not connected
    // ============================================
    touch_ctrl #(
        .T_300MS_VAL (T_300MS_OVERRIDE),
        .T_POLL_VAL  (T_POLL_OVERRIDE)
    ) u_touch_ctrl (
        .clk           (sys_clk),
        .rst_n         (rst_n_sync),
        .i2c_cmd_valid (i2c_cmd_valid),
        .i2c_cmd       (i2c_cmd),
        .i2c_wr_data   (i2c_wr_data),
        .i2c_rd_data   (i2c_rd_data),
        .i2c_done      (i2c_done),
        .i2c_ack       (i2c_ack),
        .i2c_busy      (i2c_busy),
        .touch_x       (touch_x),
        .touch_y       (touch_y),
        .touch_valid   (touch_valid),
        .dbg_state     (tc_state),
        .dbg_raw_x     (tc_raw_x),
        .dbg_raw_y     (tc_raw_y),
        .dbg_activity  (tc_activity),
        .dbg_i2c_busy  (/* unused: top derives i2c_busy from i2c_ustate */),
        .dbg_i2c_ack   (/* unused: top derives i2c_ack from ~i2c_ack_err */)
    );

    // ============================================
    // 7-Segment Display Instance
    // Display format: [ 0 ][ X ][ 0 ][ Y ]
    //   digit3(left)  digit2     digit1    digit0(right)
    //   X high nibble always 0 -> shows "0"
    //   X low  nibble = touch_x (0~F)
    //   Y high nibble always 0 -> shows "0"
    //   Y low  nibble = touch_y (0~F)
    //
    // Example: finger at center -> X=8, Y=B -> shows "080B"
    seg7_drv u_seg7_drv (
        .clk     (sys_clk),
        .rst_n   (rst_n_sync),
        .data0   (touch_y[3:0]),   // Y coordinate (low nibble)
        .data1   (4'd0),           // Y high nibble (always 0)
        .data2   (touch_x[3:0]),   // X coordinate
        .data3   (4'd0),           // X high nibble (always 0)
        .dp      (4'b0000),        // Decimal points off
        .seg     (seg),
        .dp_out  (dp),
        .an      (an)
    );

endmodule
