# FPGA RTL Delivery Skill Chain

## Default Chain

1. `rtl-fpga-lessons`
   - Trigger: any FPGA RTL, Vivado, bitstream, ILA, XDC, board-debug, or package
     request under `D:/AMD` or `D:/xillin`.
   - Output: verified RTL/Vivado project and updated RTL lessons.

2. `doc`
   - Trigger: experiment manual, DOCX, customer handoff document, tutorial, lab
     guide, or company-format document.
   - Output: DOCX inside the project folder and central document archive.

3. `session-summary`
   - Trigger: user asks for summary or the delivery is complete.
   - Output: skill audit, missed-skill audit, memory/SOP/skill-reference updates.

## Optional Supporting Skills

- `pdf`: use when the source material is a PDF manual or when PDF rendering
  verification is required.
- `li-hardware`: use when the task needs datasheet-level protocol or timing
  reasoning beyond existing board lessons.
- `code`: use when broad software-style refactor/testing is needed around
  scripts or document generators.

## Rule

Do not mark an FPGA customer handoff complete until both chains are done:

- Engineering chain: archive, edit, synth, impl, bitstream, timing, bit/ltx,
  source encoding, ZIP inspection.
- Customer chain: DOCX manual, correct paths, real pins, real images, expected
  phenomena, troubleshooting, function-named ZIP.
