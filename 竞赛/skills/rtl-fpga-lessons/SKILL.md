---
name: rtl-fpga-lessons
description: Use when writing, modifying, reviewing, documenting, packaging, organizing, or debugging FPGA RTL/Vivado projects for the AMD board workspaces, especially when the user mentions D:/AMD, ADC/DAC, I2C, AT21CS01 EEPROM, 1-Wire, ILA, Vivado 2020.1, boss feedback, experiment documents, final ZIPs, or customer handoff.
---

# RTL FPGA Lessons

Before changing RTL, writing docs, packaging, or organizing `D:/AMD` FPGA
projects, read:

1. `references/amd_fpga_delivery_sop.md`
2. `references/vivado_rtl_lessons.md`
3. `D:/AMD/快速查找索引.md` when the task references a final function.

## Required Workflow

1. Inspect the current project and prior working versions before editing.
2. Archive the working folder before non-trivial changes.
3. Identify whether the failure is RTL logic, board mapping, protocol address,
   analog range, ILA visibility, timing, or packaging.
4. Keep source comments ASCII unless the existing file already uses another
   clean encoding.
5. Preserve board-confirmed constraints over earlier assumptions.
6. Rebuild with Vivado through synthesis, implementation, and bitstream.
7. Verify `.bit`, `.ltx`, timing, DRC, source encoding, and package contents.
8. Add the new lesson to memory/self-evolution/this skill reference after the
   task closes.

## AMD Handoff Defaults

- Use function-name folders under `D:/AMD/最终交付包`.
- Use `D:/AMD/老板可直接发送的最终压缩包` for final ZIPs.
- Experiment docs must be `.docx` and follow the company guide structure.
- Boss hardware feedback overrides stale README assumptions.
- Do not include stale `.bit/.ltx/vivado_project` in a new source package.

## Minimum Final Checks

- `synth_1/runme.log`: synthesis has 0 errors and no critical warnings.
- `impl_1/runme.log`: bitgen completed successfully.
- routed timing summary: all user timing constraints are met.
- XDC pins match the latest board-confirmed pins.
- ILA probes exist for internal state, ACK/error flags, counters, and data.
- Package includes RTL, XDC, Tcl scripts, `.bit`, `.ltx`, and README/handoff notes.
