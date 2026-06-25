# AMD FPGA Delivery SOP

## Always Read First

For `D:/AMD` tasks, read these files before editing or packaging:

- `D:/AMD/快速查找索引.md`
- `D:/AMD/交付物对应关系.csv`
- `${WORKSPACE_ROOT}/SOPs/13_AMD_FPGA跨对话交付SOP.md`
- `${WORKSPACE_ROOT}/memory/rtl_code_lessons.md`
- `C:/Users/13975/.agents/skills/rtl-fpga-lessons/references/vivado_rtl_lessons.md`

## Current Final Functions

- `ADC1采样_DAC1可调采样率回放_默认4kSPS`
- `ADC1采样_DAC1固定10Hz回放`
- `AT21CS01单总线EEPROM暖复位读写`

Use `D:/AMD/最终交付包/<功能名>/` to find the final ZIP, DOCX, RTL, XDC, Tcl,
and README together. Use `D:/AMD/老板可直接发送的最终压缩包/` when the user only
wants files to send to the boss.

## User/Boss Preferences

- Use concise Chinese function names. Avoid numbered prefixes in final folders
  and package names.
- Archive before modifying. Never delete original customer files unless
  explicitly requested.
- Boss hardware feedback overrides old README assumptions.
- RTL/Tcl/XDC comments should be ASCII unless encoding has been verified.
- If Vivado was not run, say so explicitly.
- Final answer should mention verification status and remaining risk.

## Board Facts

- FPGA: `XC7A35T-2FGG484I`
- Clock: `clk` W19, 50 MHz
- Reset: `reset` Y19, active low
- I2C: `i2c_scl` W21, `i2c_sda` AA18
- EEPROM DQ: Y6
- EEPROM LEDs: `D0` AB22 success, `D1` AB21 failure
- ADC1: ADC081C021, `7'h55`
- ADC2: ADC081C021, `7'h56`
- DAC1: DAC081C085, board-tested `7'h0a`
- DAC2: DAC081C085, reference `7'h09`

## RTL Pitfalls To Check

- Do not confuse waveform input frequency with sample request rate.
- ADC/DAC variable-rate version defaults to `ADC_SAMPLE_HZ=4000`.
- 40 Hz input looks very good; 100 Hz works but visible steps are expected.
- Use `2.0Vpp` to `2.4Vpp` with `1.65V` offset to avoid rail clipping.
- Shared I2C ADC-read plus DAC-write cannot guarantee arbitrary 0-75 kHz replay.
- I2C HS-mode is not a one-line `I2C_HZ=3400000` change.
- EEPROM AT21CS01 warm reset needs special handling; do not treat it as Dallas
  1-Wire.
- EEPROM success/fail LEDs must be done-gated: reset leaves D0/D1 off.
- If peripheral ACK fails, check protocol address bits before blaming FPGA.

## Document SOP

For experiment guides, create `.docx` with:

- title page;
- experiment overview;
- real schematic images;
- pin table matching XDC;
- requirements;
- Vivado and board steps;
- program explanation;
- observed phenomena using real boss feedback;
- FAQ/troubleshooting;
- file structure.

Validate DOCX with `python-docx`: tables, images, key text, and mojibake tokens
(`锟`, `�`, `Â`, `Ã`). If no renderer is available, say page rendering was not
checked.

## Package SOP

- ZIP name must describe the function in Chinese.
- Include DOCX, README/老板先看, RTL, XDC, Tcl, and references.
- Do not include stale `.bit`, `.ltx`, or `vivado_project` when the RTL changed
  and Vivado was not rebuilt.
- Inspect ZIP contents before saying it is ready.

## Closeout SOP

Append the new lesson to:

- `${WORKSPACE_ROOT}/memory/rtl_code_lessons.md`
- `C:/Users/13975/.agents/skills/rtl-fpga-lessons/references/vivado_rtl_lessons.md`

Use the format: symptom, root cause, fix, next check, verification.
