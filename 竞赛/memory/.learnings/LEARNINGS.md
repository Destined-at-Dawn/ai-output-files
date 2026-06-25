# Learnings Log

## [LRN-20260427-001] knowledge_gap

**Logged**: 2026-04-27T20:00:00+08:00
**Priority**: critical
**Status**: resolved
**Area**: infra

### Summary
MediaPipe 没有 Linux ARM64 (aarch64) 预编译包，不能在 RDK X5 等 ARM 开发板上直接 pip install

### Details
PyPI 上 mediapipe 只提供 x86_64 Linux、x86_64 Windows、ARM64 macOS 的 wheel。GitHub issue #5965 未关闭。从源码编译需要 Bazel，在 4-8GB RAM 的 ARM 板上极难成功。

### Suggested Action
ARM64 Linux 姿态检测替代方案：MoveNet (TFLite)、YOLOv8-Pose (ONNX Runtime)、NCNN

### Resolution
- **Resolved**: 2026-04-27
- **Notes**: 在采购验证报告中已修正为 MoveNet TFLite 方案

### Metadata
- Source: investigation
- Tags: mediapipe, arm64, rdk-x5, pose-estimation
- Pattern-Key: arm64.mediapipe_unavailable

---

## [LRN-20260427-002] knowledge_gap

**Logged**: 2026-04-27T20:00:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
RDK X5 供电是 5V/5A USB-C，不是 12V/3A

### Details
地平线官方文档明确标注 5V/5A USB Type-C 供电。之前采购清单错误写成 12V/3A。I2C/UART 配置用 srpi-config 工具，不是手动改 config.txt。

### Resolution
- **Resolved**: 2026-04-27
- **Notes**: 采购清单已修正

### Metadata
- Source: investigation
- Tags: rdk-x5, power-supply, hardware
- Pattern-Key: hardware.verify_power_spec

---

## [LRN-20260427-003] best_practice

**Logged**: 2026-04-27T20:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
皮影/轻量级 puppet 项目应选 MG90S 而非 MG996R 舵机

### Details
MG996R (55g, 11kg·cm, 1.4A堵转) 对于驱动几十克的亚克力皮影严重过剩。MG90S (14g, 2.2kg·cm, 0.4A堵转) 完全够用，且省钱、省电、省重量。12个 MG90S 总堵转电流 4.8A，5V/5A 电源即可；12个 MG996R 需要 16.8A+。

### Metadata
- Source: investigation
- Tags: servo, mg90s, mg996r, puppet, budget
- Pattern-Key: servo.match_load_to_torque

---

## [LRN-20260427-004] best_practice

**Logged**: 2026-04-27T22:00:00+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
竞赛工作区需要独立 CLAUDE.md，将15种竞赛任务映射到14个专用 Skill（不同于创作工作区的映射）

### Details
用户要求为竞赛工作区创建类似创作工作区 CLAUDE.md 的全局约束文件。核心差异：竞赛文档强制去AI味（khazix-writer）、需要PDF读取、技术调研、设备验证等场景。关键创新是"任务→Skill映射表"——每个任务对应必须调用的Skill并标注顺序（如"五步写作法 → khazix-writer"）。

### Suggested Action
新竞赛项目启动时第一时间创建专用 CLAUDE.md 映射表

### Metadata
- Source: user_feedback
- Related Files: 2026跨校协作新场景赛项/CLAUDE.md
- Tags: claude.md, skill-mapping, competition, workflow
- Pattern-Key: claude.init_workspace_skill_map

---


---

## 认知科学支撑：竞赛学习记录的认知原理（百大认知书籍）

| 认知机制 | 来源 | 在竞赛LEARNINGS.md中的应用 |
|---------|------|--------------------------------|
| **错误驱动学习** | 009-认知天性 §概念2 | 竞赛中的错误(时序违例/资源溢出/引脚冲突)=最强学习信号——错误比成功更能推动知识重构。LEARNINGS.md强制记录错误→每次失败都转化为认知升级 |
| **心理模型校准** | 023-认知觉醒 §概念3 | FPGA开发需要精确的心理模型("信号在第几个时钟周期到达")——LEARNINGS.md的时序教训=心理模型校准器→模型偏差逐步收窄→调试时间↓ |
| **工具认知内化** | 016-习惯的力量 §概念1 | Quartus/iverilog操作记录=工具使用的程序性记忆——"上次怎么解决综合错误的"→不靠记忆靠记录→操作从"每次查手册"升级为"查LEARNINGS.md"→效率×3 |
| **迁移学习** | 028-我们如何学习 §概念1 | 竞赛学到的调试方法→其他硬件项目=迁移学习——LEARNINGS.md中的教训不只适用于当前竞赛→未来遇到类似FPGA问题→直接调用→学习收益最大化 |
| **即时反馈** | 016-习惯的力量 §概念1 | 编译→发现错误→记录到LEARNINGS→修复→再编译=即时反馈回路——反馈延迟<5分钟→行为修正最有效→比"事后总结"有效10倍 |

---

## [LRN-20260610-001] routing_failure

**Logged**: 2026-06-10T22:00:00+08:00
**Priority**: critical
**Status**: resolved
**Area**: skill-routing

### Summary
li-sync 路由失败：用户消息"全常用工作区同步"精确匹配触发词"同步"+"全工作区"，但 AI 手动执行了 6 个工作区的 CLAUDE.md 编辑，完全绕过了 li-sync skill。

### Details
**发生了什么**：
1. 用户要求"全常用工作区同步"——修改 F1 技能审计格式
2. AI 正确识别了需要改哪些工作区、哪些行
3. 但 AI 选择手动 Edit 每个文件，没有调用 `mcp__skill-handler__Skill(skill="li-sync")`
4. 结果：跳过了 li-sync 的 Phase 4 一致性检查、同步报告、同步前检查清单

**根因分析**（道法术器）：
- **道**：「你并没有上升到你的目标水平，你下降到了你的系统水平。」——《原子习惯》001。AI 绕过 skill 系统手动执行，就是"下降到系统水平"的典型案例。系统（li-sync）设计了质量门禁，但 AI 选择"更快的手动路径"，结果是跳过了所有门禁。skill-auto-activation.md 明确禁止的"手动替代综合征"
- **法**：路由表匹配逻辑在长文本中被忽略——用户消息只有 7 个字，但前一轮对话很长，AI 在"执行模式"中没有回头检查路由
- **术**：li-sync 的 Phase 3（传播工作区改动）本应驱动同步流程，包含：读取源文件 → 判断分类 → 逐个 Edit → Read 验证 → 输出同步报告
- **器**：li-sync 的同步前检查清单（6 项）被完全跳过

**为什么看起来合理实际不行**：
手动 Edit 看起来"效率更高"——直接改不就完了？但绕过 skill 意味着：
1. 没有一致性检查（Phase 4）——不知道改完后各工作区是否真的一致
2. 没有同步报告——无法确认所有文件都改了
3. 没有旧版备份——高风险修改前没有归档
4. 教训没有进入 skill 的经验积累——下次还会犯

### Suggested Action
1. **强制**：用户消息含"同步/工作区/跨区/一改全改"等关键词时，必须先调 li-sync，由 skill 驱动流程
2. **检查**：每次"批量编辑多个工作区"操作前，自问"这是不是应该由 li-sync 驱动的？"
3. **路由增强**：考虑在 li-sync 中增加"工作区文件修改"触发——当 AI 检测到自己正在编辑 ≥3 个工作区的文件时，自动中断并调用 li-sync

### Resolution
- **Resolved**: 2026-06-10
- **Notes**: 用户指出问题后补调 li-sync + li-improve，按五步闭环记录教训

### Metadata
- Source: user_feedback
- Tags: li-sync, routing-failure, skill-auto-activation, manual-bypass
- Pattern-Key: routing.manual_bypass_li_sync
- Recurrence-Count: 1（首次）
- Related Rule: `.claude/rules/skill-auto-activation.md` "手动替代综合征"
