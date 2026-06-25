# Workspace Agent Constraints

## Core Contract

- Safety first: ask for confirmation before high-risk or destructive actions; handle low-risk inspection and editing autonomously.
- Record as memory: write important decisions, fixes, boss feedback, and reusable lessons into the relevant `memory/`, `SOPs/`, or skill reference files.
- Default answer shape: conclusion first, then reason analysis, then `Source: path#line`.
- Keep answers dense and mobile-friendly. Prefer short lists over wide tables.
- Explain the "why" behind decisions, but avoid unnecessary frameworks.
- Use the Dao/Fa/Shu/Qi framework only for unfamiliar concept analysis, business/monetization analysis, or personal growth/decision analysis.

## Cross-Conversation Bootstrap

This workspace must preserve project context across new conversations through files, not hidden chat memory.

When the user mentions any of these: `D:/AMD`, `D:\AMD`, FPGA, RTL, Verilog, Vivado, XDC, ADC, DAC, I2C, AT21CS01, EEPROM, 1-Wire, ILA, experiment document, DOCX, package, final ZIP, boss feedback, or customer handoff, do this before editing or packaging:

1. Use the `rtl-fpga-lessons` skill if available.
2. Read `D:/AMD/快速查找索引.md`.
3. Read `D:/AMD/交付物对应关系.csv`.
4. Read `${WORKSPACE_ROOT}/templates/FPGA-RTL类/案例-AMD_FPGA.md`（原 SOP-13，已迁移为模板案例）.
5. Read `${WORKSPACE_ROOT}/memory/rtl_code_lessons.md`.
6. Read `C:/Users/13975/.agents/skills/rtl-fpga-lessons/references/amd_fpga_delivery_sop.md`.
7. Read `C:/Users/13975/.agents/skills/rtl-fpga-lessons/references/vivado_rtl_lessons.md` when changing RTL or debugging hardware.

Do not claim that the old conversation context has been inherited unless these files have actually been consulted. If a file is missing, say which file is missing and continue with the best available local evidence.

When the user mentions enterprise driver delivery, `驱动设计任务书`, ZYNQ, XC7Z020, PS/PL, ARM Cortex-A9, Linux driver, SDK/Vitis, FSBL, Flash boot, UART/SPI/IIC/CAN/Ethernet, XADC, DMA, Intel FPGA, Quartus, ANLOGIC FPGA, TD, TI DSP, CCS, PWM, or customer acceptance, also read:

1. `${WORKSPACE_ROOT}/企业级驱动任务_新AI最快路径索引_20260618.md` when it exists.
2. `${WORKSPACE_ROOT}/SOPs/14_客户需求文档到最终交付SOP.md`.
3. `${WORKSPACE_ROOT}/SOPs/06_硬件设计与验证SOP.md`.
4. `${WORKSPACE_ROOT}/SOPs/09_技术沟通与交付准备SOP.md`.
5. `${WORKSPACE_ROOT}/SOPs/11_实验教学文档编写SOP.md` when the deliverable includes customer/user documents.

For enterprise driver tasks, first build a requirement matrix from the task document, then map every requirement to source code, constraints, tests, documentation, and package contents. Do not start coding until the interface count, rate, latency, boot, API, and acceptance criteria are explicit.

## AMD FPGA Project Rules

- Never delete AMD project files. Before non-trivial changes, create a dated archive or new version folder.
- Boss hardware feedback overrides stale README text, earlier assumptions, and theoretical guesses.
- Keep final handoff names as concise Chinese function names. Avoid `01_`, `02_`, or other numbered prefixes in final handoff names.
- Use `D:/AMD/老板可直接发送的最终压缩包` for ZIPs intended to send directly to the boss.
- Use `D:/AMD/最终交付包/<功能名>/` to keep final ZIP, DOCX, RTL, XDC, Tcl, README, and handoff notes together.
- If Vivado synthesis/implementation/bitstream was not actually run, state that clearly. Do not imply a bitstream was verified.
- Do not include stale `.bit`, `.ltx`, or `vivado_project` folders in a new source package unless they were generated for that exact version.

## Board Facts To Preserve

- FPGA: `XC7A35T-2FGG484I`.
- Clock: `clk`, pin `W19`, 50 MHz.
- Active-low reset: `reset`, pin `Y19`.
- I2C: `i2c_scl` pin `W21`, `i2c_sda` pin `AA18`.
- EEPROM DQ: pin `Y6`.
- EEPROM LEDs: `D0` success on `AB22`, `D1` failure on `AB21`.
- ADC1: `ADC081C021`, 7-bit I2C address `7'h55`.
- ADC2: `ADC081C021`, 7-bit I2C address `7'h56`.
- DAC1: `DAC081C085`, board-tested 7-bit I2C address `7'h0a`.
- DAC2 reference address: `7'h09`.
- ADC-DAC best practical demo result so far: 40 Hz sine is very clean; 100 Hz works but stair steps are visible.
- For clean oscilloscope display, prefer moderate input amplitude around 2.0 Vpp to 2.4 Vpp with 1.65 V offset; avoid full-scale clipping.

## RTL And Verification Rules

- Inspect the current source, XDC, README, package manifest, and prior working version before editing.
- Check for the real failure class: RTL state machine, protocol address, board pin mapping, analog range, timing, ILA visibility, or package mismatch.
- Keep RTL/Tcl/XDC comments ASCII unless the file is already cleanly encoded otherwise.
- For I2C shared ADC-read plus DAC-write designs, do not overpromise arbitrary 0-75 kHz analog replay. Explain the bus transaction limit and provide practical demo frequency guidance.
- For EEPROM warm-reset issues, remember that parasitic power behavior can require DQ high-charge/wait time before a new transaction.
- Final check should include source encoding, XDC pins, package contents, and whether `.bit/.ltx` are current or intentionally absent.

## Experiment Document Rules

- Use the `doc` skill for `.docx` experiment guides when available.
- Follow the company-style teaching document structure: experiment purpose, hardware resources, schematic/interface analysis, pin table, Vivado operation steps, program explanation, test phenomenon, FAQ, and source/project references.
- Include real schematic images or project screenshots when available.
- No mojibake in document text. Verify with `python-docx` or another available document parser.
- If page-render verification or LibreOffice conversion was not performed, state that limitation.

## File Organization Rules

- Keep lookup fast: every final function should have a direct path from ZIP to DOCX to RTL to XDC.
- Maintain `D:/AMD/快速查找索引.md` and `D:/AMD/交付物对应关系.csv` after reorganizing or adding final deliverables.
- Historical and intermediate artifacts belong in archive/reference folders, not mixed with boss-ready packages.

## Final Response Rules

- Answer in Chinese unless the user asks otherwise.
- Start with the result or conclusion.
- Include concise reasons.
- Include source references using `Source: path#line`.
- If a command failed or verification could not be completed, say so plainly.
