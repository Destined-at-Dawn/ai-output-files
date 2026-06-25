# RTL One-Pass SOP

Goal: make each FPGA RTL fix increase the probability of first-pass success next time.

## Before RTL Changes

- Read project README, top module, XDC, Tcl build scripts, and previous memory.
- Search for stale constants: addresses, pins, clock rates, dividers, ILA depth,
  reset polarity, active-high/active-low LED behavior.
- Identify whether the observed failure is hardware mapping, protocol, analog
  setup, ILA visibility, bandwidth, or RTL state sequencing.
- Archive the current project before changing deliverable files.

## While Changing RTL

- Keep edits narrow and explainable.
- Prefer parameters for board-dependent values only when the board value is
  known; otherwise add auto-detection or ILA-visible debug state.
- Add enough debug signals for board bring-up: FSM state, ACK/error, selected
  address, readback data, valid/done/pass/fail, counters.
- Keep `.v/.tcl/.xdc` comments ASCII to avoid customer-facing mojibake.

## Before Delivery

- Recreate or update Vivado project.
- Run synthesis, implementation, and bitstream.
- Confirm timing constraints are met.
- Confirm `.bit` and `.ltx` exist.
- Confirm XDC pins match latest boss/hardware feedback.
- Inspect ZIP contents after packaging.
- Append lessons to `memory/rtl_code_lessons.md` and the RTL skill reference.

## AT21CS01 Special Case

- Treat AT21CS01 as single-wire I2C, not Dallas 1-Wire.
- After reset, assume high-speed mode until the device explicitly accepts the
  Standard Speed Mode opcode.
- Run discovery before commands; do not use reset as a generic transaction
  separator.
- With 4.7 kOhm board pullup, prefer standard-speed EEPROM data transfer after
  the high-speed mode switch command succeeds.
- If the part is bus-powered from DQ, validate both cold programming and
  push-button warm reset. Use a standard-speed-safe reset-low width and a long
  DQ-high recharge wait.
- Keep ILA debug small enough for XC7A35T; last_fail_state style summary probes
  are better than wide counters at deep capture depth.

## Customer Handoff Closure

- Hardware PASS is not closure until the matching customer package exists.
- For each experiment, create a separate function-named Chinese ZIP instead of
  one mixed archive.
- Put the DOCX lab manual inside the project folder before zipping, and also
  copy it to `D:/AMD/project_output/实验文档`.
- Inspect the ZIP after compression. Required items: DOCX, README, RTL, XDC,
  Tcl scripts, Vivado project, `.bit`, `.ltx`, and protocol/debug notes when
  relevant.
- Validate DOCX files structurally with `python-docx`; if LibreOffice is not
  available, report that PDF render verification was not possible.

## Skill Invocation Order

1. `rtl-fpga-lessons`: read memory, classify failure, preserve board-confirmed
   pins, archive, edit RTL, rebuild, verify bit/ltx/timing/source encoding.
2. `doc`: create or update the experiment manual after the hardware behavior
   and final project paths are known.
3. `session-summary`: after delivery, record used skills, missed opportunities,
   final artifacts, and next-pass rules.
