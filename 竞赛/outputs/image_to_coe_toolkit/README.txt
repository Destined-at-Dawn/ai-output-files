===================================================================
  IMAGE TO COE TOOLKIT — FPGA ROM 初始化文件生成工具包
===================================================================

作用：把一张图片（Logo）转换成 Vivado BMG IP 核可用的 .coe 文件。

面向：AI（Claude Code / Copilot 等），不是给人看的操作手册。


一、工具包文件清单
===================

  logo_to_rom.py             主脚本：图片 → HEX + COE（支持 RGB888 和 RGB565）
  hex_to_coe.py              辅助：把 .hex 文件转成 .coe（不改位宽）
  coe_rgb888_to_rgb565.py    辅助：把 24-bit COE 批量转成 16-bit RGB565 COE

  logo_preview_173x171.png           Logo 预览图（可当作输入源图片用）
  logo_rom_data_rgb888_reference.hex 参考输出：RGB888 HEX 格式（24-bit）
  logo_rom_data_rgb565_reference.coe 参考输出：RGB565 COE 格式（16-bit，最终交付格式）


二、给 AI 的操作指令
=====================

主流程（一步到位，推荐）：

  python logo_to_rom.py logo.png --rgb565

  输入：任意 PNG/JPG/BMP 图片
  输出：
    logo_rom_data.hex           HEX 格式（$readmemh 用，备选）
    logo_rom_data.coe           COE 格式（BMG IP 用）
    logo_preview_173x171.png    缩放后的预览图

  参数说明：
    --rgb565      输出 16-bit RGB565（不加此参数默认输出 24-bit RGB888）
    --width W     目标宽度，默认 173
    --height H    目标高度，默认 171
    --output-dir  输出目录，默认脚本所在目录

分步流程（已有旧 HEX 需要转换时）：

  python hex_to_coe.py logo_rom_data.hex logo_rom_data.coe

  --rgb565 三步流程（888 HEX → 888 COE → 565 COE）：

  python hex_to_coe.py data.hex data_rgb888.coe                    # HEX→COE
  python coe_rgb888_to_rgb565.py data_rgb888.coe data_rgb565.coe   # 888→565


三、关键格式说明
=================

  BMG IP .coe 文件格式：
    memory_initialization_radix=16;
    memory_initialization_vector=
    FFFF,
    FFFF,
    ...
    FFFF;

  RGB565 (16-bit)：
    每个值 4 位 hex：RRRRRGGGGGGBBBBB
    例：0xFFFF = 全白，0x0000 = 全黑
    BMG IP 配置：Port A Width = 16, Depth = 像素总数

  RGB888 (24-bit)：
    每个值 6 位 hex：RRRRRRRRGGGGGGGGBBBBBBBB
    例：0xFFFFFF = 全白
    BMG IP 配置：Port A Width = 24, Depth = 像素总数


四、BMG IP 核配置速查
======================

  生成 COE 后，在 Vivado 里配置 BMG IP：
    Memory Type:             Single Port ROM
    Port A Width:            16 (RGB565) 或 24 (RGB888)
    Port A Depth:            像素总数（173x171 = 29583）
    Enable Port Type:        Use ENA Pin
    Primitive Output Register: true（2拍延迟，稳定时序）
    Load Init File:          true
    Coe File:                选生成的 logo_rom_data.coe


五、Verilog BRAM Wrapper 模板
===============================

  // RGB565 (16-bit):
  module logo_rom (
      input  wire        clk,
      input  wire [14:0] addr,    // ceil(log2(29583)) = 15 bit
      output wire [15:0] data     // RGB565
  );
      blk_mem_gen_0 u_bram (
          .clka  (clk),
          .ena   (1'b1),
          .addra (addr),
          .douta (data)
      );
  endmodule

  // RGB888 (24-bit):
  module logo_rom (
      input  wire        clk,
      input  wire [14:0] addr,
      output wire [23:0] data     // RGB888
  );
      blk_mem_gen_0 u_bram (
          .clka  (clk),
          .ena   (1'b1),
          .addra (addr),
          .douta (data)
      );
  endmodule


六、常见踩坑
=============

  1. PIL 没装：pip install pillow
  2. COE 数据条数不对：确认深度 = 宽×高，不是宽×高-1
  3. BMG IP 宽度不匹配：16-bit COE 必须配 16-bit IP 端口，报错 "outside range" 就是宽度不匹配
  4. IP 改了 COE 没重新 Generate：改 .coe 后必须 reset_target + generate_target
  5. BRAM 读延迟：Register_PortA_Output=true 时是 2 拍出数据，RTL 流水线要提前 1 拍给地址
  6. Vivado 锁死 IP：手动改 .xci 后要删 .xml 缓存，否则 "stale content" 锁死
  7. $readmemh 大 ROM OOM：深度 > 16K 时不要用 $readmemh 推断，用 BMG IP 核


七、依赖
========

  pip install pillow


八、首次使用的 AI 自检清单
=============================

  [ ] 输入图片存在、可读？
  [ ] 目标分辨率正确？（默认 173x171）
  [ ] 输出格式选对了？（--rgb565 还是默认 RGB888）
  [ ] COE 数据条数 = 宽 × 高？（29583 = 173×171）
  [ ] BMG IP 宽度匹配？（16-bit COE → Port A Width = 16）
  [ ] COE 文件放在了 IP 能找到的路径？（工程目录或 imports/code/）
  [ ] 生成 IP 后跑了 reset_target + generate_target？
