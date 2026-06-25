# lcd_top.xdc — XC7A35T-2FGG484I 引脚约束
# 皮赛电子 Artix-35T 开发板 + 3.5寸TFT-LCD (SPI)

# 时钟 (50MHz)
set_property PACKAGE_PIN F4      [get_ports sys_clk]
set_property IOSTANDARD LVCMOS33 [get_ports sys_clk]
create_clock -period 20.000 -name sys_clk [get_ports sys_clk]

# SPI 生成时钟 (12.5MHz)
create_generated_clock -name spi_clk \
    -source [get_pins u_spi_master/clk] \
    -divide_by 4 \
    [get_ports lcd_sclk]

# 复位按键 (低有效)
set_property PACKAGE_PIN J2      [get_ports sys_rst_n]
set_property IOSTANDARD LVCMOS33 [get_ports sys_rst_n]

# LCD SPI接口
set_property PACKAGE_PIN AB6     [get_ports lcd_sclk]
set_property IOSTANDARD LVCMOS33 [get_ports lcd_sclk]

set_property PACKAGE_PIN AB7     [get_ports lcd_mosi]
set_property IOSTANDARD LVCMOS33 [get_ports lcd_mosi]

set_property PACKAGE_PIN AA6     [get_ports lcd_cs]
set_property IOSTANDARD LVCMOS33 [get_ports lcd_cs]

# LCD 控制信号
set_property PACKAGE_PIN Y6      [get_ports lcd_rst]
set_property IOSTANDARD LVCMOS33 [get_ports lcd_rst]

set_property PACKAGE_PIN W6      [get_ports lcd_bl]
set_property IOSTANDARD LVCMOS33 [get_ports lcd_bl]

# 调试信号 (init_done → LED)
set_property PACKAGE_PIN G1      [get_ports init_done]
set_property IOSTANDARD LVCMOS33 [get_ports init_done]

# 配置选项
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]

# 位流生成设置
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]
