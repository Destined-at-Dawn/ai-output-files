## 用法：Vivado Tcl Console → cd D:/AMD → source create_project.tcl

## 修复中文Windows用户名污染.Xil临时路径
set ::env(USERNAME) "vivado_user"

set script_dir [file dirname [file normalize [info script]]]
set project_name "lcd_logo"
set part_name    "xc7a35tfgg484-2"

puts ""
puts "============================================"
puts "  Creating project: $project_name"
puts "  Part: $part_name"
puts "  Script dir: $script_dir"
puts "============================================"

## Step 1 — Create project
catch {close_project -quiet}
file delete -force ${script_dir}/${project_name}
create_project $project_name ${script_dir}/${project_name} -part $part_name -force

## Step 2 — Add ALL RTL sources
## logo_rom.v is a static wrapper for BMG IP
add_files -norecurse [list \
    ${script_dir}/lcd_top.v \
    ${script_dir}/lcd_ctrl.v \
    ${script_dir}/spi_master.v \
    ${script_dir}/logo_rom.v \
]
set_property top lcd_top [current_fileset]
puts "  RTL sources added: 4 files"

## Step 3 — Add constraints
add_files -fileset constrs_1 -norecurse ${script_dir}/lcd_top.xdc

## Step 4 — Add simulation
add_files -fileset sim_1 -norecurse ${script_dir}/lcd_top_tb.v
set_property top lcd_top_tb [get_filesets sim_1]
puts "  Simulation set: lcd_top_tb"

## Step 5 — Create BMG IP (Block Memory Generator)
puts "  Creating BMG IP..."
set bmg_versions {8.4 8.3}
set bmg_created 0
foreach ver $bmg_versions {
    if {![catch {create_ip -name blk_mem_gen -vendor xilinx.com -library ip \
        -version $ver -module_name blk_mem_logo} err]} {
        puts "    BMG v$ver created successfully"
        set bmg_created 1
        break
    }
}
if {!$bmg_created} {
    puts "    Falling back to default BMG version..."
    create_ip -name blk_mem_gen -vendor xilinx.com -library ip \
        -module_name blk_mem_logo
    puts "    BMG created with default version"
}

## Step 6 — Copy COE file + configure ROM
set proj_dir [get_property DIRECTORY [current_project]]
file copy -force ${script_dir}/logo_rom_data.coe ${proj_dir}/logo_rom_data.coe
puts "  COE file copied to project dir"

set_property -dict [list \
    CONFIG.Component_Name {blk_mem_logo} \
    CONFIG.Memory_Type {Single_Port_ROM} \
    CONFIG.Write_Width_A {24} \
    CONFIG.Write_Depth_A {29583} \
    CONFIG.Read_Width_A {24} \
    CONFIG.Enable_A {Use_ENA_Pin} \
    CONFIG.Register_PortA_Output_of_Memory_Primitives {true} \
    CONFIG.Load_Init_File {true} \
    CONFIG.Coe_File ${proj_dir}/logo_rom_data.coe \
] [get_ips blk_mem_logo]
puts "  ROM configured: 24-bit x 29583 depth"

## Step 7 — Generate IP output products
puts "  Generating IP output products..."
generate_target all [get_ips blk_mem_logo]

## Step 8 — Add generated IP files to project
set ip_files [get_files -of_objects [get_ips blk_mem_logo]]
add_files -norecurse $ip_files
puts "  IP files added to project: [llength $ip_files] file(s)"

## Step 9 — Disable OOC synthesis (after generate_target)
if {[llength $ip_files] > 0} {
    foreach f $ip_files {
        catch {set_property generate_synth_checkpoint false $f}
    }
    puts "  OOC synthesis: disabled"
}

## Step 10 — Finalize
update_compile_order -fileset sources_1

puts ""
puts "============================================"
puts "  Project created successfully!"
puts "  Path: ${script_dir}/${project_name}"
puts ""
puts "  NEXT STEP: In Flow Navigator, click"
puts "    Run Synthesis"
puts "============================================"
puts ""
