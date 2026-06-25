# RTL FPGA Lessons Rule

Purpose: every RTL/Vivado correction must become reusable engineering memory.

## Trigger

Use this rule before writing, modifying, reviewing, packaging, or debugging FPGA
RTL/Vivado projects, especially under `D:/AMD`.

## Required Reads Before RTL Edits

1. `${WORKSPACE_ROOT}/memory/rtl_code_lessons.md`
2. `${WORKSPACE_ROOT}/skills/rtl-fpga-lessons/SKILL.md`
3. `${WORKSPACE_ROOT}/skills/rtl-fpga-lessons/references/vivado_rtl_lessons.md`

## Required Workflow

1. Inspect current RTL, top module, XDC, Tcl build scripts, README, and prior
   working versions before editing.
2. Archive the working folder before non-trivial changes.
3. Classify the failure before changing code:
   - board mapping
   - peripheral protocol/address
   - bus throughput
   - analog range/headroom
   - reset/result indication
   - ILA visibility
   - timing/constraints
   - source encoding
   - packaging/handoff drift
4. Keep `.v`, `.tcl`, and `.xdc` comments ASCII unless the file already has a
   clean verified non-ASCII encoding.
5. Preserve latest board-confirmed pins, addresses, and scope results over older
   README or AI assumptions.
6. Add ILA-visible debug for FSM state, ACK/error, counters, data, selected
   address, done/pass/fail when relevant.
7. Rebuild through Vivado synthesis, implementation, and bitstream.
8. Verify `.bit`, `.ltx`, timing report, DRC status, source encoding, and ZIP
   contents before delivery.
9. After delivery, append the new lesson to:
   - `memory/rtl_code_lessons.md`
   - `skills/rtl-fpga-lessons/references/vivado_rtl_lessons.md`
   - relevant daily/project memory file

## Current High-Value Lessons

- DAC1/DAC2 names are not proof; board-tested I2C address/probe mapping wins.
- I2C waveform point rate must be budgeted before choosing frequency.
- ILA capture depth must cover the event period being observed.
- Shared ADC-read plus DAC-write I2C cannot be assumed to reach chip headline
  sample rate.
- 0-75 kHz arbitrary waveform replay requires end-to-end throughput and analog
  filtering; Nyquist alone is not a stability guarantee.
- Full-rail analog waveforms can clip; document amplitude and offset.
- LED result outputs should be gated by final `done`.
- EEPROM/1-Wire device address bits must not be hard-coded when hardware address
  is unknown; scan or expose the address.
- AT21CS01 reset leaves the device in high-speed mode. Run discovery and the
  speed-mode command before normal EEPROM access; do not use reset as a normal
  transaction separator.
- AT21CS01 warm reset can differ from cold download when the part remains in
  standard-speed mode or is bus-powered from DQ; use long reset/recharge timing
  and test the board reset button.
- XDC, top-level ports, README, and package contents must be updated together.
- Source encoding is a delivery requirement, not a cosmetic detail.
