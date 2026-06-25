# Vivado RTL Lessons Database

## How To Add A Lesson

Use this compact format:

- Date:
- Symptom:
- Root cause:
- Fix:
- Check before next edit:
- Verification:
- Source:

## Lessons From D:/AMD ADC/DAC/EEPROM Work

### AT21CS01 Reset Defaults To High-Speed Mode

- Symptom: EEPROM project still failed with `D1=1, D0=0` after LED pins and
  address scan were fixed.
- Root cause: AT21CS01 is not a Dallas-style 1-Wire part. After reset it
  defaults to high-speed mode, expects the reset/discovery response sequence,
  and will not reliably accept slow standard-speed slots immediately after
  reset.
- Fix: perform reset/discovery first, send the Standard Speed Mode opcode using
  high-speed timing for each candidate address, then run EEPROM write/readback
  at standard speed.
- Check before next edit: never insert reset between normal AT21CS01
  transactions unless the following sequence restarts with discovery and speed
  mode setup.
- Verification: expose state/address/readback/LED pass-fail to ILA, rebuild
  through bitstream, and check `.bit/.ltx` plus timing.

### AT21CS01 Warm Reset Needs Standard-Speed-Safe Reset Width

- Symptom: EEPROM passed after power-cycle download, then failed after pressing
  reset.
- Root cause: after a passing run the AT21CS01 may remain in standard-speed
  mode, while the board powers it from DQ. A short high-speed reset pulse can be
  insufficient for warm reset in that state.
- Fix: add a long DQ-high recharge wait, use at least a standard-speed-safe bus
  reset low time, then restart discovery and mode setup.
- Check before next edit: validate both cold download and button reset; expose
  last_fail_state and last_fail_addr for ILA.
- Verification: bitstream must still fit after ILA changes; reduce MARK_DEBUG
  width/depth before increasing debug probes.

### Hardware PASS Is Not The End Of Delivery

- Symptom: hardware-confirmed RTL still needed customer-ready ZIP packages and
  DOCX experiment manuals before it could be sent out.
- Root cause: the company deliverable is a reproducible experiment, not only a
  working `.bit` file.
- Fix: package each experiment separately with a function-named Chinese ZIP;
  include DOCX lab manual, RTL, XDC, Tcl scripts, Vivado project, `.bit`, `.ltx`,
  README, and protocol notes when relevant.
- Check before next edit: inspect ZIP contents explicitly and verify each DOCX
  opens without mojibake before saying it is ready for the boss/customer.
- Verification: cite the final ZIP paths and central document archive paths in
  the final response.

### Board Mapping Beats Names

- Symptom: DAC1 project waveform appeared on DAC2, or DAC2 appeared on DAC1.
- Root cause: logical name and physical I2C device/address mapping were not the
  same as initial assumption.
- Fix: use board-tested address mapping, not schematic labels alone.
- Check before next edit: find `DAC_ADDR`, I2C address constants, XDC pins, and
  measured probe point before touching waveform logic.
- Verification: scope the named physical output after programming the exact
  `.bit` file.

### I2C Throughput Must Be Calculated Before Choosing Waveform Points

- Symptom: 1 kHz DAC waveform had only about 8 visible points per cycle.
- Root cause: I2C transaction time limited how many DAC codes could be written
  per second.
- Fix: reduce waveform frequency to 10 Hz and use 800 points, or calculate the
  point rate from `clk / update_div / point_count`.
- Check before next edit: compute bus bit slots per sample and compare against
  requested sample rate.
- Verification: ILA should show update counter progress and oscilloscope should
  show smooth output.

### ILA Depth Can Hide Slow Signals

- Symptom: `dbg_dac_code` looked stuck even when DAC output changed.
- Root cause: 4096 samples at 50 MHz covers only 81.92 us, shorter than the
  125 us update interval.
- Fix: increase ILA depth, or capture a faster debug event/counter.
- Check before next edit: compare ILA capture window against expected event
  period.
- Verification: ILA sees at least one complete code transition.

### ADC/DAC Shared I2C Cannot Promise 150 ksps End-To-End

- Symptom: user requested ADC1 sample and DAC1 replay at 150 ksps on one shared
  I2C bus.
- Root cause: ADC read plus DAC write consumes many I2C bit slots per sample;
  the bus, not FPGA timing, is the bottleneck.
- Fix: remove artificial 10 Hz gating and run continuous high-speed scheduling,
  but document the achievable rate and hardware limits.
- Check before next edit: separate chip conversion-rate limits from bus
  transaction-rate limits.
- Verification: timing passes, ACK/error debug stays clear, and scope shows
  stable replay without rail clipping.

### 0-75 kHz Arbitrary Waveform Requires System Throughput, Not Just RTL

- Symptom: high-speed ADC1-to-DAC1 replay was worse than the fixed 10 Hz version,
  while the desired target was arbitrary 0-75 kHz sampling and reconstruction.
- Root cause: 75 kHz needs at least 150 ksps by Nyquist, but useful waveform
  shape requires more than two samples per cycle and deterministic sample
  spacing. A shared I2C ADC-read plus DAC-write loop cannot guarantee that.
- Fix: do not overpromise this target on the current shared-I2C hardware. Use a
  fixed low-frequency demo for stable delivery, or change the architecture to
  faster/separate ADC and DAC interfaces with FIFO buffering and real sample
  clocks.
- Check before next edit: compute bus bit slots per sample, actual SCL, samples
  per input cycle, DAC settling, ADC conversion time, and analog filters.
- Verification: compare the calculated end-to-end sample rate against the
  requested signal bandwidth before writing RTL.

### Stable Same-Day Delivery Beats Risky High-Speed Claims

- Symptom: boss reported the high-speed ADC-to-DAC replay looked worse than the
  fixed 10 Hz version.
- Root cause: the board result was limited by I2C/device stability and analog
  behavior, not FPGA timing closure.
- Fix: restore the last stable fixed-frequency ADC-to-DAC design, keep I2C at a
  conservative 400 kHz, and choose a sample request rate that gives enough
  points per 10 Hz cycle with bus margin.
- Check before next edit: if hardware feedback says a lower-speed version looks
  better, do not keep chasing headline sample rate in the same deliverable.
- Verification: build through bitstream, then scope original ADC input and DAC
  replay output on two channels.

### ADC/DAC Analog Range Can Clip At Rails

- Symptom: replay waveform top and bottom were clipped.
- Root cause: full-rail analog input/output headroom is unsafe around ADC/DAC
  limits.
- Fix: use a safer signal such as 3.0 Vpp with 1.65 V offset instead of full
  3.3 Vpp.
- Check before next edit: document input amplitude, offset, ADC reference, and
  DAC output range.
- Verification: compare original and replay on a two-channel oscilloscope.

### EEPROM LED Result Must Be Done-Gated

- Symptom: reset behavior could confuse pass/fail LEDs.
- Root cause: LEDs directly tied to pass/fail can show intermediate state.
- Fix: drive `D0 = done & pass` and `D1 = done & fail`.
- Check before next edit: reset must leave both LEDs off.
- Verification: after reset D0/D1 are off; after final compare only one LED is
  on.

### EEPROM Address Must Not Be Hard-Coded When Board Address Is Unknown

- Symptom: boss saw `D1=1, D0=0` after LED pin fix; fixed
  `.DEVICE_ADDR(3'b000)` was suspected.
- Root cause: AT21CS01 command byte includes device-address bits; the board
  part may not answer at address 0.
- Fix: scan device addresses 0..7 and retry write/read/compare until one passes;
  fail only after all addresses fail.
- Check before next edit: distinguish FPGA part number from peripheral device
  address/protocol configuration.
- Verification: expose `current_addr` and `found_addr` to ILA, rebuild through
  bitstream, and package `.bit/.ltx`.

### XDC Pin Feedback From Hardware Overrides Old README

- Symptom: EEPROM LED pins in README did not match boss-provided pins.
- Root cause: stale documentation from previous assumption.
- Fix: update XDC and README together; verify package contains the corrected
  files.
- Check before next edit: search README, XDC, top ports, and package manifest for
  stale pin names.
- Verification: source refs should show the final pins, not old pins.

### Source Encoding Is A Delivery Requirement

- Symptom: Chinese comments can become mojibake in Verilog/Tcl/XDC handoff.
- Root cause: mixed editor encodings.
- Fix: keep RTL/Tcl/XDC comments ASCII unless there is a strong reason not to.
- Check before next edit: run an ASCII scan on source files excluding generated
  Vivado output.
- Verification: no byte above 127 in `.v`, `.tcl`, `.xdc` source files.

### Workspace Cleanup Must Be Versioned And Non-Destructive

- Symptom: final ZIPs, current Vivado projects, old builds, docs, screenshots,
  scripts, and AI handoff notes can become mixed after many board iterations.
- Root cause: successful RTL delivery does not automatically produce a clean
  workspace structure for future handoff.
- Fix: create a dated organized copy folder under the workspace, classify files
  into final deliverables, active projects, docs, AI collaboration records,
  intermediate/history, references, and tools.
- Check before next edit: never delete, move, or overwrite original customer
  files during cleanup unless the user explicitly approves it.
- Verification: generate a manifest and an original-file snapshot, and make the
  README state that the organized folder was created by copying/indexing only.

### Demo Waveform Frequency Must Not Become An RTL Limit

- Symptom: a stable ADC-to-DAC demo can look locked to 10 Hz when the project
  name, README, comments, and top parameters all describe the same demo value.
- Root cause: input waveform frequency and ADC sample request rate were mixed.
- Fix: expose `ADC_SAMPLE_HZ` as a top-level parameter, derive the divider from
  clock frequency, document points per waveform cycle, and keep ACK/backlog ILA
  probes.
- Check before next edit: sample rate is an RTL parameter; input waveform
  frequency is a signal-generator setting.
- Verification: calculate actual sample rate and actual SCL after integer
  divider rounding before promising hardware bandwidth.
