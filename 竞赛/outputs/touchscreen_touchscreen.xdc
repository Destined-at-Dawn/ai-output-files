# ============================================================
# 触摸屏坐标显示工程引脚约束文件
#
# 目标芯片：Xilinx XC7A35T-2FGG484I
# 开发板：ETL4-7A35T（上海皮赛电子）
# 依据：ETL4-7A35T实验指导手册 + lab1_led_seq已验证引脚
#
# 引脚分配来源：
#   时钟/复位/数码管/LED → lab1_led_seq已验证（手册确认）
#   PMODA引脚 → 需要对照开发板原理图确认
# ============================================================

# ━━━ 时钟约束 ━━━
# 50MHz贴片有源晶振（手册 §2.1.4）
create_clock -period 20.000 -name sys_clk [get_ports sys_clk]

# ━━━ 系统时钟 ━━━
set_property -dict {PACKAGE_PIN W19 IOSTANDARD LVCMOS33} [get_ports sys_clk]

# ━━━ 复位按键 ━━━
# PB0轻触开关，低电平有效（手册 §2.1.3 / lab1已验证）
set_property -dict {PACKAGE_PIN Y19 IOSTANDARD LVCMOS33} [get_ports sys_rst_n]

# ━━━ I2C接口（PMODA连接FT6336U触摸屏） ━━━
# 只需 SCL 和 SDA 两根线！
# RST/INT/VCC/GND 由触摸屏硬件模块默认处理，不占用FPGA引脚
# 参考：lcd_rst/lcd_bl/init_done 内部信号教训（memory/long-term.md）
#
# ⚠️ 引脚号来自已有工程，需要对照开发板原理图确认！
#   B21 = PMODA Pin1 = SCL（I2C时钟）
#   B20 = PMODA Pin2 = SDA（I2C数据，双向）
set_property -dict {PACKAGE_PIN B21 IOSTANDARD LVCMOS33} [get_ports i2c_scl]
set_property -dict {PACKAGE_PIN B20 IOSTANDARD LVCMOS33} [get_ports i2c_sda]

# ━━━ 7段数码管（共阳极，4位） ━━━
# 段选信号（低电平点亮）—— lab1手册 §2.2.5 确认
# seg[0]=a, seg[1]=b, seg[2]=c, seg[3]=d, seg[4]=e, seg[5]=f, seg[6]=g
set_property -dict {PACKAGE_PIN K21 IOSTANDARD LVCMOS33} [get_ports {seg[0]}]
set_property -dict {PACKAGE_PIN H20 IOSTANDARD LVCMOS33} [get_ports {seg[1]}]
set_property -dict {PACKAGE_PIN J22 IOSTANDARD LVCMOS33} [get_ports {seg[2]}]
set_property -dict {PACKAGE_PIN K22 IOSTANDARD LVCMOS33} [get_ports {seg[3]}]
set_property -dict {PACKAGE_PIN K19 IOSTANDARD LVCMOS33} [get_ports {seg[4]}]
set_property -dict {PACKAGE_PIN J20 IOSTANDARD LVCMOS33} [get_ports {seg[5]}]
set_property -dict {PACKAGE_PIN H19 IOSTANDARD LVCMOS33} [get_ports {seg[6]}]

# 小数点
set_property -dict {PACKAGE_PIN J21 IOSTANDARD LVCMOS33} [get_ports dp]

# 位选信号（低电平选中）
set_property -dict {PACKAGE_PIN T1  IOSTANDARD LVCMOS33} [get_ports {an[0]}]
set_property -dict {PACKAGE_PIN U1  IOSTANDARD LVCMOS33} [get_ports {an[1]}]
set_property -dict {PACKAGE_PIN G20 IOSTANDARD LVCMOS33} [get_ports {an[2]}]
set_property -dict {PACKAGE_PIN H22 IOSTANDARD LVCMOS33} [get_ports {an[3]}]

# ━━━ I2C上拉电阻 ━━━
# FT6336U数据手册要求SCL/SDA有上拉电阻
# FPGA内部上拉提供弱上拉（~50kΩ），外部模块通常有4.7kΩ上拉
set_property PULLUP TRUE [get_ports i2c_scl]
set_property PULLUP TRUE [get_ports i2c_sda]

# ━━━ 配置选项 ━━━
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]

# ━━━ ILA调试核设置 ━━━
# 综合后在Vivado Tcl Console执行：source setup_ila.tcl
# 或手动：Flow Navigator → Set Up Debug → 选择MARK_DEBUG信号
# 触发条件：dbg_cmd_valid 上升沿
# 如果SCL/SDA无波形 → 换PMOD引脚（B21/B20 → 其他pin）重新综合
