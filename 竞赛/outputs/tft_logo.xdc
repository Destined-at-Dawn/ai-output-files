create_clock -period 20.000 [get_ports sys_clk]
set_property -dict {PACKAGE_PIN W19 IOSTANDARD LVCMOS33} [get_ports sys_clk]
set_property -dict {PACKAGE_PIN Y19 IOSTANDARD LVCMOS33} [get_ports sys_rst_n]

set_property -dict {PACKAGE_PIN AA20 IOSTANDARD LVCMOS33} [get_ports lcd_sclk]
set_property -dict {PACKAGE_PIN AB18 IOSTANDARD LVCMOS33} [get_ports lcd_mosi]
set_property -dict {PACKAGE_PIN AA19 IOSTANDARD LVCMOS33} [get_ports lcd_cs]

