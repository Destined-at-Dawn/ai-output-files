# RTL Code Lessons

Purpose: make every RTL correction reusable before the next FPGA/Vivado edit.

## 2026-06-01 AT21CS01 Protocol Timing Lesson

- Symptom: EEPROM project in `D:/xillin` still ended with `D1=1, D0=0` after
  LED pins and address scan were fixed.
- Root cause: the RTL treated AT21CS01 like a Dallas-style 1-Wire part: it
  issued long reset pulses before each transaction and then used slow standard
  bit slots. AT21CS01 defaults to high-speed mode after reset, requires a
  discovery response flow, and only then can be switched to standard speed.
- Fix: reworked `at21cs01_master.v` to run reset/discovery, scan address 0..7
  with the high-speed Standard Speed Mode opcode, then perform normal EEPROM
  write/readback at standard speed for margin with the board 4.7 kOhm pullup.
- Check before next edit: for AT21CS01, do not insert reset between normal
  write/read commands unless the following command sequence restarts from
  high-speed discovery/mode setup.
- Verification: `D:/xillin` rebuilt through Vivado synthesis and bitstream on
  2026-06-01; synthesis had 0 errors/critical warnings/warnings, bitgen
  completed, `.bit/.ltx` exist, timing constraints are met.

## 2026-06-02 AT21CS01 Warm Reset Lesson

- Symptom: after power-cycle and download, EEPROM passed with D0/pass. Pressing
  the board reset then made the same design fail with D1/fail.
- Root cause: after a successful run the AT21CS01 can remain in standard-speed
  mode, and the board powers the part from the DQ line. The earlier 150 us bus
  reset was enough for the cold high-speed path but too short as a conservative
  warm reset after the chip had been switched to standard speed.
- Fix: increase DQ high recharge wait to 50 ms, increase bus reset low to
  600 us, increase reset-release high to 200 us, and keep last fail state/address
  visible in ILA.
- Check before next edit: for bus-powered single-wire EEPROM, test both cold
  programming and push-button warm reset; do not assume power-on pass means reset
  pass.
- Verification: rebuilt `D:/xillin` through bitstream on 2026-06-02; synthesis
  0 errors/critical warnings/warnings, bitgen completed, timing constraints met,
  `.bit/.ltx` exist, source files ASCII.

## 2026-06-02 FPGA Customer Handoff Packaging Lesson

- Symptom: RTL was accepted on hardware, but the final customer handoff still
  required separate function-named ZIP packages and matching DOCX experiment
  manuals.
- Root cause: code correctness is only one part of the deliverable. For company
  handoff, the package must include project files, bit/ltx, README, and a
  client-readable lab manual with real paths, real pins, real device addresses,
  experiment steps, expected phenomena, and troubleshooting.
- Fix: generated one DOCX per experiment, placed the DOCX inside its matching
  project folder, copied central document copies to
  `D:/AMD/project_output/实验文档`, then produced two function-named ZIP files:
  ADC1 10 Hz loopback and AT21CS01 warm-reset EEPROM.
- Check before next edit: after hardware PASS, do not stop at the bitstream.
  Build the final handoff package and inspect the ZIP contents for `.docx`,
  RTL, XDC, Tcl, `.bit`, `.ltx`, README, and notes.
- Verification: both 2026-06-02 ZIP packages were inspected for required files;
  DOCX files opened through `python-docx`, contained tables/images, and had no
  common mojibake tokens.

## 2026-05-30 ADC/DAC 0-75 kHz Stability Lesson

- Symptom: boss reported the high-speed ADC1-to-DAC1 replay version was worse
  than the fixed 10 Hz version, while the desired target was arbitrary 0-75 kHz
  waveform sampling and reconstruction.
- Root cause: Nyquist math alone is insufficient. A 75 kHz input needs at least
  150 ksps just to avoid aliasing, but stable shape reconstruction needs more
  samples per cycle and deterministic end-to-end sample timing. The current
  design uses one shared I2C bus for ADC read plus DAC write, so transaction
  overhead limits replay rate below the requested 150 ksps target.
- Fix direction: do not promise 0-75 kHz arbitrary waveform stability on the
  current shared-I2C ADC/DAC chain. Either keep the fixed 10 Hz demo as the
  stable deliverable, or change hardware/architecture: faster ADC/DAC interface,
  separate buses, FIFO buffering, deterministic sample clock, and analog
  anti-alias/reconstruction filtering.
- Check before next edit: calculate required samples per cycle, bus bit slots
  per sample, actual SCL, ADC conversion timing, DAC settling time, and analog
  input/output headroom.
- Verification: current project README already documents that 150 ksps
  ADC-to-DAC replay is not reachable on one shared I2C bus.

## 2026-05-30 ADC/DAC Stable Delivery Lesson

- Symptom: boss said the high-speed ADC->DAC version did not work as well as
  the fixed 10 Hz version.
- Root cause: pushing I2C to high-speed made the board-level result less stable
  than a lower-rate deterministic demo.
- Fix: archived the rejected high-speed project, restored the pre-high-speed
  ADC1-to-DAC1 replay design, kept I2C at 400 kHz, and set the ADC request rate
  to 2 kHz. This gives about 200 samples per 10 Hz cycle while retaining bus
  margin.
- Check before next edit: for same-day boss delivery, prefer a stable scoped
  demo over a theoretical bandwidth target.
- Verification: rebuilt `D:/AMD/dac_adc1_loopback_10hz` through bitstream and
  packaged `D:/AMD/ADC1采样_DAC1稳定回放_10Hz示波器对比工程_20260530.zip`.

## Mandatory Loop

1. Before editing: read this file and `skills/rtl-fpga-lessons/references/vivado_rtl_lessons.md`.
2. During editing: classify the issue as board mapping, protocol address, bus
   throughput, analog range, reset/LED status, ILA visibility, constraints,
   encoding, or packaging.
3. Before delivery: archive old project, rebuild through bitstream, check timing,
   check source encoding, and inspect package contents.
4. After delivery: append the new symptom/root-cause/fix/check/verification.

## Current High-Value Rules

- Do not trust logical names like DAC1/DAC2 until board measurement confirms
  physical address and probe point.
- Do not choose waveform frequency or sample rate without I2C bit-budget math.
- Do not assume the FPGA model determines peripheral address; device protocol
  address bits are separate.
- Do not let README, XDC, and top-level ports drift apart after a pin correction.
- Do not judge slow waveform debug with a too-short ILA capture window.
- Do not deliver RTL/Tcl/XDC source with non-ASCII comments unless explicitly
  required and encoding is verified.
- Always expose debug state, ACK/error, counters, readback data, and selected
  peripheral address to ILA for board bring-up.

## 2026-06-02 D:/AMD Workspace Organization Lesson

- Symptom: after several ADC/DAC/EEPROM iterations, final packages, current
  projects, old ZIPs, docs, logs, scripts, and AI handoff notes were mixed in
  `D:/AMD`.
- Root cause: project delivery work had focused on bitstream/package generation,
  but the workspace itself did not have a non-destructive handoff structure.
- Fix: create a new dated folder such as `D:/AMD/_整理版_20260602_143315`,
  copy files into clear categories, generate `整理清单.csv`, and generate an
  original-file snapshot `原始D_AMD文件快照.csv`.
- Check before next edit: do not delete or move original customer files during
  cleanup. Treat organization as a versioned copy operation unless the user
  explicitly approves a destructive cleanup.
- Verification: README for the organized folder states that no original file was
  deleted or moved, and the manifest records the copied final ZIPs,工程,
  experiment docs, AI experience files, references, and scripts.

## 2026-06-02 I2C ADC Sampling Rate Lesson

- Symptom: boss asked whether an I2C ADC theoretically can only do 10 Hz, and
  noted that I2C high-speed mode can reach 3.4 MHz.
- Root cause: the stable demo used a 10 Hz analog input and 2 kHz ADC request
  rate, but that was a demonstration choice, not the ADC081C021 limit.
- Fix: distinguish three ceilings: ADC-only chip throughput, current shared
  ADC-read plus DAC-write bus budget, and stable waveform reconstruction
  bandwidth. ADC081C021 is listed at 188.9 ksps max at 3.4 MHz SCL; the current
  shared ADC-to-DAC transaction is about 77 I2C bit slots per sample pair, so
  the rough upper bound is 5.2 k sample-pairs/s at 400 kHz and 44.2 k
  sample-pairs/s at 3.4 MHz.
- Check before next edit: do not equate input waveform frequency with sample
  rate. For high-speed mode, verify HS-mode entry sequence, SCL divider
  rounding, bus capacitance, pull-up/rise time, ACK stability, and clock
  stretching assumptions.
- Verification: wrote `D:/AMD/I2C_ADC采样率理论分析_20260602.md` with the bus
  budget and TI datasheet references.

## 2026-06-02 ADC-DAC Variable-Rate RTL Lesson

- Symptom: the stable ADC-to-DAC project name, README, and top-level parameters
  made the design look locked to a 10 Hz waveform.
- Root cause: the old version mixed up input waveform frequency with ADC request
  rate. RTL used `.ADC_SAMPLE_DIV(25000)` directly, and comments/docs described
  the experiment as a fixed 10 Hz demo.
- Fix: created `D:/AMD/dac_adc1_loopback_variable_rate_20260602` from a
  non-destructive copy. The top now exposes `ADC_SAMPLE_HZ` and `I2C_HZ`,
  derives `ADC_SAMPLE_DIV` internally, defaults to 4 kSPS, and adds
  `dbg_replay_backlog_count` for ILA overload diagnosis. I2C phase ticks now
  round upward so actual SCL is not faster than the requested target.
- Check before next edit: never hard-code a demo waveform frequency as the
  architecture limit. Put sample rate in a named parameter, document expected
  points per waveform cycle, and use backlog/ACK probes to decide whether a
  higher rate is stable on hardware.
- Verification: static checks passed: default actual SCL is 390.625 kHz,
  default actual ADC request rate is 4 kSPS, source RTL/Tcl/XDC ASCII count is
  zero, and old `ADC_SAMPLE_DIV(25000)` / `dac_adc1_loopback_10hz` code
  references are gone from the new version. Vivado CLI and local iverilog could
  not be used in this environment, so synthesis still needs to be run in Vivado.

## 2026-06-02 Variable-Rate Package Handoff Lesson

- Symptom: the variable-rate project was created from the working 10 Hz project,
  so the copied `vivado_project` directory still contained the old project name
  and old bitstream artifacts.
- Root cause: copying a known-good Vivado folder is useful for recovery, but
  generated project/run directories can become stale after RTL changes.
- Fix: package the variable-rate handoff as a clean source/project-generation
  ZIP: top-level README, RTL, XDC, Tcl scripts, rate config, theory notes, and
  schematic images; exclude stale `vivado_project`, `.bit`, and `.ltx`.
- Check before next edit: if Vivado cannot be rebuilt in the current
  environment, say the ZIP is a source engineering package, not a verified
  bitstream package.
- Verification: ZIP inspection for
  `D:/AMD/ADC1采样_DAC1可调采样率回放_默认4kSPS_源码工程包_20260602.zip`
  showed no `vivado_project`, `.bit`, `.ltx`, or old `dac_adc1_loopback_10hz`
  entries.

## 2026-06-03 ADC-DAC Variable-Rate Documentation Lesson

- Symptom: after board feedback confirmed the variable-rate version worked
  well, the handoff ZIP still lacked the company-style DOCX experiment guide.
- Root cause: source engineering packages and customer teaching packages have
  different completion criteria. A source ZIP is not enough when the boss asks
  for a customer-facing experiment document.
- Fix: generated
  `实验指导书_ADC1采样DAC1可调采样率回放_默认4kSPS.docx`, copied it into the
  package root and `D:/AMD/project_output/实验文档`, updated package README and
  file manifest, then created
  `D:/AMD/ADC1采样_DAC1可调采样率回放_默认4kSPS_含实验文档_20260603.zip`.
- Check before next edit: include real hardware feedback in the document.
  Here, record that 40 Hz looks very good and 100 Hz works but has visible
  steps, and pair that with amplitude/offset guidance to avoid clipping.
- Verification: DOCX opened with `python-docx`, contained 6 tables and 2
  schematic images, included 40 Hz/100 Hz feedback, and had no common mojibake
  tokens. ZIP inspection showed the DOCX was included and no stale
  `vivado_project`, `.bit`, or `.ltx` files were present.

## 2026-06-03 Functional Workspace Organization Lesson

- Symptom: the first `D:/AMD` cleanup used numbered category folders such as
  `00_...` and `01_...`, which made handoff browsing feel artificial and made it
  harder to jump from a final ZIP to its document or RTL file.
- Root cause: categories were organized by archive mechanics instead of the
  user's actual lookup workflow: "which function is this, where is its final
  ZIP, where is its DOCX, and where is the exact code file?"
- Fix: reorganized `D:/AMD` by functional names. Top-level folders now include
  `老板可直接发送的最终压缩包`, `最终交付包`, `公共资料`, `AI协作记录`,
  `历史参考包`, `工具脚本`, and `历史归档`. Each final function folder contains
  its final ZIP, DOCX, RTL, XDC, Tcl, and README together.
- Check before next edit: avoid numbered prefixes in final handoff folders and
  filenames unless they are inside a historical archive. Provide both
  `快速查找索引.md` and `交付物对应关系.csv`.
- Verification: `D:/AMD` top level no longer contains numbered category
  folders; old numbered cleanup folders were moved into
  `D:/AMD/历史归档/旧版编号整理目录_20260602`; final function folders have no
  files starting with numeric prefixes; index rows show final ZIP, DOCX, RTL,
  and XDC paths for the three final deliverables.

## 2026-06-03 Cross-Conversation Continuity Lesson

- Symptom: user wanted future conversations to behave like this long AMD FPGA
  thread when asked to write experiment docs, modify RTL, package final ZIPs, or
  react to boss feedback.
- Root cause: chat context is not a reliable long-term storage layer. New
  conversations need durable files and skill triggers, not implicit memory.
- Fix: created `D:/AMD/新对话启动提示词.md`,
  `D:/AMD/AMD_FPGA交付技能介绍.md`, and
  `SOPs/13_AMD_FPGA跨对话交付SOP.md`; updated the global
  `rtl-fpga-lessons` skill and added
  `references/amd_fpga_delivery_sop.md`; synchronized the skill to workspace
  skills and `C:/Users/13975/.claude/skills/rtl-fpga-lessons`.
- Check before next edit: when starting a fresh thread, tell the agent to use
  `rtl-fpga-lessons` and read `D:/AMD/快速查找索引.md`,
  `D:/AMD/交付物对应关系.csv`, the SOP, and `memory/rtl_code_lessons.md`.
- Verification: files exist in `D:/AMD`, workspace SOPs, global skills, and
  Claude skills. Basic SKILL.md frontmatter check passed; official
  `quick_validate.py` could not run because PyYAML is not installed in the
  bundled Python environment.

## 2026-06-22 CTP/TFT Work Document Continuation Lesson

- Symptom: user needed to continue writing work documents from old
  `D:/AMD_before/zip/ctp.zip` and `D:/AMD_before/zip/tft_logo.zip` according to
  the existing AMD SOP and skills.
- Root cause: these were older Vivado project ZIPs outside the organized
  `D:/AMD/final` handoff tree, so the safe path was to inspect and document
  them without modifying the original ZIPs or updating final-deliverable
  indexes prematurely.
- Fix: extracted the ZIPs into a temporary workspace, analyzed top RTL, control
  RTL, XDC, existing build logs, timing reports, BMG ROM summary, and source
  assets. Generated working DOCX guides under `D:/AMD/工作文档_20260622` for
  FT6336U touch-coordinate display and TFT-LCD centered Logo display.
- Check before next edit: when documenting historical FPGA ZIPs, distinguish
  "working documentation draft" from "final handoff package"; only update
  `快速查找索引.md` and `交付物对应关系.csv` after the user confirms the docs should
  become final deliverables.
- Verification: DOCX structure check passed with `python-docx`; the CTP guide
  has 43 paragraphs, 2 tables, and 1 image; the TFT guide has 49 paragraphs, 2
  tables, and 2 images. Common mojibake tokens were not found. Page-render
  verification was not performed because LibreOffice/soffice was not available
  in PATH.

## 2026-05-30 EEPROM Address Lesson

- Symptom: boss tested EEPROM project and saw `D1=1, D0=0`.
- Root cause: code fixed `.DEVICE_ADDR(3'b000)`, but AT21CS01 command bytes
  include device-address bits and board part may answer elsewhere.
- Fix: scan addresses 0..7; retry full write/read/compare after NACK/mismatch;
  fail only after all addresses fail.
- Check before next edit: when a peripheral fails ACK, inspect address bits,
  not only FPGA part number or top-level pins.
- Verification: rebuilt `D:/AMD/eeprom_rw` through bitstream; package generated
  as `D:/AMD/EEPROM单总线读写_自动扫描地址_D0成功D1失败_20260530.zip`.
## 2026-06-03 Workspace Constraint Bootstrap Lesson

- Symptom: the user wanted future conversations to automatically behave like
  this long AMD FPGA thread, including document style, boss preferences,
  packaging rules, archive discipline, and RTL debugging lessons.
- Root cause: implicit chat context is not portable. A new conversation can
  only recover reliably from workspace instructions, SOP files, memory files,
  and skill references that are actually read at startup.
- Fix: created `${WORKSPACE_ROOT}/AGENTS.md` as the workspace
  bootstrap contract. It forces AMD/RTL/DOCX/ZIP tasks to read
  `D:/AMD/快速查找索引.md`, `D:/AMD/交付物对应关系.csv`, the AMD cross-dialog SOP,
  `memory/rtl_code_lessons.md`, and the `rtl-fpga-lessons` references before
  editing or packaging.
- Check before next edit: do not claim that old context has been inherited
  unless the bootstrap files were actually consulted. If a file is missing,
  report the missing file and proceed from local evidence.
- Verification: `AGENTS.md` exists in the workspace root and includes board
  facts, AMD final package locations, archive rules, experiment document rules,
  RTL verification rules, and final response source-citation rules.
## 2026-06-18 Enterprise Driver Task Bootstrap Lesson

- Symptom: the user provided `驱动设计任务书20260615.doc` and wanted a new AI
  to immediately know the fastest path from the task document to enterprise
  delivery, instead of rediscovering this conversation's hidden context.
- Root cause: enterprise driver work is broader than the previous AMD
  ADC/DAC/EEPROM lab. It needs a requirement matrix, PS/PL architecture split,
  interface-rate/latency analysis, SDK/Linux driver mapping, verification
  evidence, and customer handoff documents.
- Fix: created
  `${WORKSPACE_ROOT}/企业级驱动任务_新AI最快路径索引_20260618.md`.
  Updated `AGENTS.md` so enterprise triggers such as `驱动设计任务书`, ZYNQ,
  XC7Z020, PS/PL, SDK/Vitis, FSBL, Flash, UART/SPI/IIC/CAN/Ethernet, XADC,
  Intel FPGA, ANLOGIC FPGA, TI DSP, Quartus, TD, and CCS point to this index
  and to SOP-14/SOP-06/SOP-09/SOP-11.
- Check before next edit: do not reuse AMD board pins or I2C addresses for a
  ZYNQ customer task. Reuse only the delivery method: archive, inspect, build
  a requirement matrix, implement with evidence, document, package, and record
  lessons.
- Verification: the task document text was partially extracted from the old
  `.doc` file into `D:/tmp_driver_task_20260615/extracted_strings.txt`; the
  extracted content confirms BY1/ZYNQ7020, Vivado 2022.2, 20 UART, 3 IIC,
  2 SPI, 1 CAN, Ethernet, DI/DO, XADC, Flash boot, API, and handoff document
  requirements. Full layout/table extraction still needs Word/LibreOffice
  conversion because the file is an old OLE `.doc`.

## 2026-06-18 - BY1 enterprise driver offline handoff before board arrival

- Symptom: the user wanted the three BY1 task-document deliverables completed
  before the enterprise board was available.
- Root cause: enterprise delivery has useful no-board work, but it is easy to
  overclaim if Vivado, SDK/Vitis, Linux, and board-level tests have not run.
- Fix: in `${WORK_ROOT}/BY1 控制器配套设计说明文档`, created a D:/AMD-style structure
  with `最终交付包`, `老板可直接发送的最终压缩包`, `快速查找索引.md`, and
  `交付物对应关系.csv`; completed no-board deliverables for Vivado project
  skeleton, SDK driver skeleton, FPGA RTL skeleton, requirement matrix,
  engineering index, design document, validation record, split ZIPs, and total
  ZIP.
- Check before next edit: keep BY1 real board constraints separate from AMD
  examples. Do not fill XDC, bitstream, 20-UART throughput, 10us latency, Flash
  boot, or Linux-driver claims until board/Vivado/SDK evidence exists.
- Verification: SDK C sources compiled with host GCC and printed
  `BY1 CRC/frame offline test passed`; ASCII scan passed for `.v/.tcl/.xdc/.c/.h`;
  DOCX/PDF were generated; ZIP scan found no process files or AI collaboration
  records. PL simulation did not run because visible `iverilog.exe` binaries
  were not valid for this OS platform.
