# ============================================================
# ILA debug core setup script
#
# Usage:
#   1. Open touchscreen project in Vivado
#   2. Run Synthesis
#   3. In Tcl Console: source setup_ila.tcl
#   4. Re-run Synthesis -> Implementation -> Generate Bitstream
#   5. Program FPGA, open Hardware Manager
#
# Debug signals (13 signals, 29 bits total):
#   dbg_scl       (1)  -- I2C SCL output (should see 200kHz square wave)
#   dbg_sda_in    (1)  -- I2C SDA input (slave data)
#   dbg_sda_out   (1)  -- I2C SDA output (master data)
#   dbg_sda_oe    (1)  -- SDA direction (1=master driving, 0=released)
#   dbg_cmd_valid (1)  -- Command valid pulse (rising edge = I2C op starts)
#   dbg_im_ustate (4)  -- i2c_master internal state machine
#   dbg_tc_state  (5)  -- touch_ctrl main state machine
#   dbg_touch_x   (4)  -- X coordinate (0-F)
#   dbg_touch_y   (4)  -- Y coordinate (0-F)
#   dbg_i2c_busy  (1)  -- I2C master is processing a command
#   dbg_i2c_ack   (1)  -- Last I2C transaction got ACK from slave
#   dbg_activity  (1)  -- Toggle on each successful coordinate read
#   dbg_touch_valid(1) -- Pulse when new coordinate data ready
#
# Pin verification:
#   Trigger on dbg_cmd_valid rising edge
#   -> Check dbg_scl for 200kHz square wave (yes = correct pins)
#   -> Check dbg_im_ustate transitions (should go 0->1->2->...->15->0)
#   -> If SCL/SDA always high with no activity -> wrong PMOD pins
# ============================================================

# Create ILA core (run after synthesis)
# Sample clock=sys_clk(50MHz), 13 probes, total width=29-bit, depth=4096
create_debug_core u_ila_0 ila
set_property C_DATA_DEPTH 4096 [get_debug_cores u_ila_0]
set_property C_TRIGIN_EN false [get_debug_cores u_ila_0]
set_property C_INPUT_PIPE_STAGES 2 [get_debug_cores u_ila_0]

# Connect sample clock
set_property port_width 1 [get_debug_ports u_ila_0/clk]
connect_debug_port u_ila_0/clk [get_nets sys_clk_IBUF_BUFG]

# Set probe0 (total width=29-bit)
set_property port_width 29 [get_debug_ports u_ila_0/probe0]

# Connect all MARK_DEBUG signals to probe0
# Bit allocation: [28]=scl, [27]=sda_in, [26]=sda_out, [25]=sda_oe,
#   [24]=cmd_valid, [23:20]=im_ustate, [19:15]=tc_state,
#   [14:11]=touch_x, [10:7]=touch_y, [6]=i2c_busy, [5]=i2c_ack,
#   [4]=activity, [3]=touch_valid, [2:0]=reserved
connect_debug_port u_ila_0/probe0 [list \
    [get_nets dbg_scl] \
    [get_nets dbg_sda_in] \
    [get_nets dbg_sda_out] \
    [get_nets dbg_sda_oe] \
    [get_nets dbg_cmd_valid] \
    [get_nets {dbg_im_ustate[0]}] \
    [get_nets {dbg_im_ustate[1]}] \
    [get_nets {dbg_im_ustate[2]}] \
    [get_nets {dbg_im_ustate[3]}] \
    [get_nets {dbg_tc_state[0]}] \
    [get_nets {dbg_tc_state[1]}] \
    [get_nets {dbg_tc_state[2]}] \
    [get_nets {dbg_tc_state[3]}] \
    [get_nets {dbg_tc_state[4]}] \
    [get_nets {dbg_touch_x[0]}] \
    [get_nets {dbg_touch_x[1]}] \
    [get_nets {dbg_touch_x[2]}] \
    [get_nets {dbg_touch_x[3]}] \
    [get_nets {dbg_touch_y[0]}] \
    [get_nets {dbg_touch_y[1]}] \
    [get_nets {dbg_touch_y[2]}] \
    [get_nets {dbg_touch_y[3]}] \
    [get_nets dbg_i2c_busy] \
    [get_nets dbg_i2c_ack] \
    [get_nets dbg_activity] \
    [get_nets dbg_touch_valid] \
]

puts "=========================================="
puts " ILA debug core setup complete!"
puts " Please re-run: Synthesis -> Implementation -> Generate Bitstream"
puts " Trigger: dbg_cmd_valid rising edge"
puts " Watch for:"
puts "   dbg_scl square wave = I2C pins correct"
puts "   dbg_im_ustate changes = I2C master running"
puts "   dbg_tc_state changes = touch_ctrl running"
puts "   dbg_activity toggles = coordinates being read"
puts "=========================================="
