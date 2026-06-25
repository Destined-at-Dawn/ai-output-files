# 长期记忆 — 竞赛工作区

> 由 longmemory skill 每日归档维护。对话中只读。

## 工作区定位
- 竞赛区：集创赛(5.7已结束)、ICAN小车(9月)、皮影戏(6.15)
- 大创红色赛道：马克思学院高教授
- 赵老师推荐实验室（无人机/小车/机械臂）

## 关键约束
- F7 禁止编造（零容忍）
- F8 数据备份 3-2-1 规则
- 宁可误触发 Skill 不能漏触发（F5）

## 迭代记录
- 2026-05-25: R16 根目录优先架构落地

## 跨工作区共享铁律（2026-05-30 同步自 mutual 区）

### 🔴 内容丢失恢复协议
发现任何文件丢失/损坏时：
1. 检查 GitHub 备份（mutual 区有 3 个远程）：
   - origin: `github.com/Destined-at-Dawn/mutual`
   - niuma: `github.com/Destined-at-Dawn/niuma-ecosystem`
   - gitee: `gitee.com/li-lanyuan/mutual`
2. 查看提交历史：`cd E:\ai产出文件\牛马\mutual\mutual && git log --oneline -20`
3. 从 git 恢复：`git checkout <commit-hash> -- <文件相对路径>`
4. 恢复后立即 Read 验证文件完整性
5. 记录事故到 mutual 区 memory/long-term.md

### 🟡 牛马AI 升级后 Temp 残留检查
每次牛马AI 版本升级后：
- 检查 `C:\Users\13975\AppData\Local\Temp\newmax_app*`
- 若有残留 → 提醒用户迁移至 `E:\ai产出文件\牛马\备份\newmax-config-安全迁移-{日期}\`
- 配置文件备份入口：`E:\ai产出文件\牛马\备份\`

### 🟡 关键教训索引
- **PK-VERIFY-005**：Read 工具中文路径假阴性 → 多重验证，不单一采信
- 验证优先级：PowerShell Test-Path > MCP read_project_file > python -c > grep > Read
- 死线铁律：做了才说 / 验了才断 / 每轮有质变（适用于所有工作区）

### 🟡 批量下载日志检查点铁律（2026-06-01 同步自 mutual 区）
- 任何批量下载/文件处理任务，**每完成 1/3 必须写检查点日志**到本地磁盘
- 检查点日志格式：`{任务名}_checkpoint_{序号}.json`，含已完成/失败清单+统计
- 用途：进程中断后精确恢复，不用重新爬取对比
- **最终确认完成后**：删除中间检查点日志，汇总为最终日志 `{任务名}_final_report.json`
- 来源：用户指令「所有常用工作区要同步」

### 2026-05-28 — RTL工程反复出现的AI失败模式（高价值迁移教训）
- **AI失败模式清单**（从diff臆造bug、未看Vivado日志就猜测、处理大型ROM/IP流出错、非UTF8/GBK文件编码破坏、跨模块CMD常量不匹配、非开漏I2C SDA、case外全局ACK检测错误、读memory不执行）
- **真相源规则**：D:\AMD根目录下的outputs和很多文件是旧/中间/备份版本——任何RTL任务前必须确认真实源目录、版本、编码、工具链、XDC和验证目标
- **I2C检查清单**：CMD_*编码必须在i2c_master.v和touch_ctrl.v间一致；SDA必须开漏（只拉低不主动推高）；ACK检查应按写地址/寄存器/读地址状态逐个检查

### 2026-05-29 — FPGA ADC/DAC/EEPROM教学实验工程拆分经验
- **拆分策略**：按"3类实验、5个独立工程"执行（队友实际要求DAC1/DAC2/ADC1/ADC2/EEPROM都要独立写文档）
- **DAC频率计算**：UPDATE_DIV=50000、50MHz→1ms更新、8位三角波约510步→约1.96Hz
- **ILA深度教训**：原ILA depth 4096@50MHz仅覆盖81.92us，但DAC更新周期125us→需要至少16384深度
- **DAC1 10Hz重做教训**：DSP multiply/divide产生pipeline DRC警告→改用accumulator/Bresenham三角波生成器

### 2026-05-29 — FPGA客户交付质量标准
- **老板反馈**：第一版文档被夸，但以后要按"公司客户交付质量"而非"学校报告质量"
- **客户交付文档策略**：研究ETL4-7A35T PDF手册→复制A4单栏布局、公司居中页眉、页码页脚、章节编号、实操截图、图注、红色警告、文件超链接、简洁工程说明
- **示波器/探头匹配教训**：如果旧统一工程bitstream有波形但拆分工程没有，先检查project-to-probe对齐

### 2026-05-30 — 简历STAR压缩写作规则
- **STAR压缩写法**：简历bullet主要写Action+Result，Situation和Task放在项目名与第一句里
- **学生项目简历优先写**：工具、对象、动作、交付物、验证方式
- **不确定数据一律留占位符，不替用户虚构**
- **AI改写可以提高表达，但必须压回到可验证的工程事实**

### 2026-05-30 — AT21CS01 EEPROM地址扫描教训
- **老板测试结果**：D1=1, D0=0（EEPROM读写失败）
- **根因**：代码固定DEVICE_ADDR(3'b000)，但AT21CS01命令字节包含器件地址位，板上器件可能在其他地址应答
- **修复**：扫描地址0..7，每个地址重试完整写读比较序列，NACK/不匹配后继续，全部8地址失败才算失败
- **教训**：外设ACK失败时，先查地址位，不只是FPGA型号或顶层引脚

### 2026-06-02 — FPGA硬件PASS后的Next-Pass规则
- **硬件PASS = 工程确认，不等于最终交付**
- **总线供电单线器件**：必须同时测试冷下载和按钮热复位
- **ILA偏好摘要探针**（如last_fail_state）优于深度宽计数器
- **公司交接**：每个实验一个ZIP+内含DOCX，压缩后检查ZIP内容

### 2026-06-02 — I2C ADC采样率理论分析教训
- **三个天花板要区分**：①ADC芯片吞吐量 ②当前共享ADC读+DAC写总线预算 ③稳定波形重建带宽
- **ADC081C021最大188.9ksps@3.4MHz SCL**；当前共享ADC-to-DAC每样本对约77个I2C bit slot → 400kHz下约5.2k样本对/s，3.4MHz下约44.2k样本对/s
- **教训**：不要把输入波形频率等同于采样率；不要承诺超出I2C位预算的性能

### 2026-06-03 — FPGA工作区组织教训
- **按功能命名组织而非数字前缀**：顶层文件夹包括"老板可直接发送的最终压缩包""最终交付包""公共资料""AI协作记录""历史参考包""工具脚本""历史归档"
- **每个最终功能文件夹**：ZIP+DOCX+RTL+XDC+Tcl+README放在一起
- **提供快速查找索引.md和交付物对应关系.csv**

### 2026-06-03 — 跨对话连续性教训
- **聊天上下文不是可靠的长期存储层**——新对话需要持久文件和skill触发器，不靠隐式记忆
- **解决方案**：创建新对话启动提示词+技能介绍+SOP+AGENTS.md引导文件
- **新线程启动时**：告诉agent使用rtl-fpga-lessons skill，读取快速查找索引、交付物对应关系、SOP和memory/rtl_code_lessons.md

### 2026-06-06 — RM电控考核交付模式与文档工具链
- **RoboMaster电控考核核心策略**：题目是STM32 HAL简易步兵电控系统，重点不是一次性做满全部功能，而是展示模块化、控制闭环、状态机、安全保护和自学能力。"不要求全部做完"→ 策略为"最小可交付工程 + Git/README/测试记录加可信度"
- **高优先级架构**：main.c不堆逻辑、chassis/gimbal/remote/pid/app分层、底盘运动学、云台目标角、Pitch限位、输出限幅、急停、STOP/NORMAL模式
- **文档工具链确立**：Pandoc（Markdown→DOCX）+ LibreOffice（DOCX→PDF）+ Poppler（PDF→PNG渲染抽检）—— 三件套路径已固定，后续所有文档生成复用
- **客户最终交付包标准**：核心代码/ + 实验文档/ + 自我学习/ + 答辩简历材料/ 四大目录，每份Markdown同时生成DOCX+PDF
- **代码验证标准**：`gcc -std=c99 -Wall -Wextra -I Core/Inc -c` 语法检查通过即为基线合格

### 2026-06-08 — 技能自动激活系统性失败与路由基础设施修复

- **事故规模**：上一轮对话中AI在11/11个环节零次调用skill，全部手动完成。
- **四重根因**：①双路由文件混乱（skill-routing-table.json vs skill-rules.json格式不同、内容冲突）②路由表缺少li-*系列skill触发词（0条→已注册）③ skill-auto-activation.md文件不存在（CLAUDE.md引用了空路径）④AI把skill当"可选参考"而非"必须执行的工作流引擎"。
- **修复清单**：skill-rules.json加_deprecated标记→CLAUDE.md统一引用→MEMORY.md更新→skill-auto-activation.md创建v1.0硬协议。
- **路由表v2.1深度审计**：从111条→72条（去幽灵skill+去重复），P1优先级从31条→11条，补录systemverilog/longmemory/投流帖改写等关键skill。
- **FPGABuilder学习成果**：10个可复用设计模式（配置驱动/插件架构/Hook系统/TCL模板化等），已注入hardware-design SKILL.md v5.0。

### 2026-06-09 — SOP通用化重构+模板库建立+YOLO竞赛项目化+技能审计格式重构

- **SOP-14通用化重构**：从RoboMaster电控考核SOP重构为通用的"客户需求文档到最终交付SOP"(356行)。覆盖：Phase 0需求分析→交付物矩阵→代码/文档/答辩/自我学习要求→打包门禁→交付报告→边界声明。
- **模板库建立**：创建templates/目录结构（_INDEX.md + FPGA-RTL类/），从SOP提取通用模板+项目案例分离，SOP-12/13归档后从SOPs/删除。
- **阶段性落盘验证铁律**：多阶段架构重构对话截断导致2个缺口→每阶段完成后立即Glob+Read验证，不等最后一起验。已写入CLAUDE.md/AGENT.md/li-hardware/SOP-14共4处。
- **YOLO竞赛转长期项目**：M1~M5完成（YOLO12n 100ep mAP50=96.6%），M6~M10待执行（树莓派部署），项目文件：projects/20260609-YOLO绝缘子检测竞赛/。
- **技能审计格式重构**：从"Read x6, Bash x3"流水账→"已激活skill/漏激活skill/下次改进"三栏格式。新增禁令：审计不是工具调用日志。

### 2026-06-10 — 竞赛官方通知读入+路由失败复盘

- **竞赛通知**：中电教协〔2026〕16号PDF，OCR提取8页全文。承办单位上海电力大学（小黎主场）+物新智能。11月7-9日，报到11月6日。
- **两赛道对比**：常规赛道(2人/队，理论4模块+实操6单元) vs 创新赛道(≤8人/队，路演+实操展示)。小黎倾向常规赛道（YOLO训练流程覆盖实操6单元中4个）。
- **OCR踩坑**：扫描版PDF→fitz.get_text()返回0字符→EasyOCR+中文路径=必炸→必须先复制到ASCII路径再OCR。
- **路由失败复盘**：li-sync被"手动替代综合征"绕过——AI手动Edit 6个工作区完全绕过skill，跳过一致性检查+同步报告+旧版备份。补调li-sync+li-improve按五步闭环记录。

### 2026-06-11 — 指导老师进度汇报+docx中文公文规范建立

- **产出**：MD版+docx版进度汇报。docx中文公文规范：标题黑体22pt居中、一级黑体16pt、正文仿宋12pt首行缩进2字符、28pt固定行距、A4标准页边距。
- **中文写作规范**：新建.claude/rules/chinese-writing-convention.md——禁止英文引号"'，禁止日文引号「」，必须用中文双引号""。

### 2026-06-12 — 论文深度调研+Goal模式9轮系统性复盘与v4.0重写

- **10篇论文方法深度调研**：TRS-YOLO(97.0% mAP, 1.74M参数)、IDD-DETR(Patch Diffusion去雾)、Drone-DETR(ESDNet+P2)、YOLOv11n-SSA(Star Operation+NWD Loss)、RSP-YOLOv11n(参数-30%)等。
- **最高优先级改进**：27倍几何增强(defect类248框→6000+框)+类别权重平衡+NWD损失函数(小目标)。li-competition SKILL v1.0.0→v1.1.0（新增论文方法速查表+快速可集成改进排序）。
- **Goal模式9轮灾难根因**：4个A级系统性问题——①上下文压缩→失忆→重复劳动 ②没有磁盘验证就开始干活 ③中文路径+幽灵文件（"转换完成"实际0文件落盘） ④Skill反复创建没有锚定。
- **新增F10磁盘验证铁律+F11 Skill锚定铁律**（CLAUDE.md）。教训放在outputs/=死知识，嵌入Skill=实时路况——"教训长在工作流上才起效"。
- **Goal模式v4.0全流程重写**：5状态状态机 INIT→PRE_CHECK→RUNNING→RECONCILE→CP_WRITE。PRE_CHECK必须先做：磁盘验证(Glob)+资产盘点(Read CP)+路由扫描(skill)+去重检查(对比历史CP)。新增CP产出标准格式+中断续跑协议。新增F12铁律(8条Goal模式铁律)。
- **competition-yolo SKILL.md避坑指南**：从6条扩展到12条(致命4/重要5/改进3)，嵌入根因分析。新增数据存储双目录地图+文件管理指引+教训回写机制。

### 2026-06-13 — Skill分离重构+自进化机制审计修复+路由表li-全覆盖+联动规则落地

- **Skill分离架构原则**：C盘全局skill（通用方法论，任何YOLO竞赛可复用）+ 项目级skill（具体数据，本竞赛独有）。competition-yolo→v2.0(去具体数据)、li-competition→v2.0(去竞赛信息)、新建competition-local.md(项目级数据)。
- **教训：每个竞赛项目有且仅有一个主文件夹**，管理文件必须在主文件夹内（不在proj-xxx目录）。已建全局规则competition-workspace-architecture.md+F13铁律。
- **自进化机制审计**：47+条教训，回写率<10%——有规则无执行。li-improve Phase 1 Step 4重写（新增教训→目标文件映射表10种类型+6步强制检查清单+回写质量门禁）。lesson-auto-update v2.0新增铁律0（教训→目标文件映射表）。lessons.md从6条扩充到17条。
- **Memory Watcher经验沉淀Agent**：后台Python脚本(30秒轮询+关键词提取+MD5哈希去重)，自动从memory文件提取教训写入lessons-learned.md。启动序列新增Step 3.5。
- **路由表li-全覆盖**：li-skillfusion从不存在→36个触发词。21个缺失li-skill全部注册(118个触发词)。总路由76→118，触发词~1200→1816，li-skill注册率26/47→47/47(100%)。
- **skill-linkage.md联动规则**：4条联动链+强制度检查+中断条件。复制到11个关键skill的references/目录。设计原理：references/在skill调用时被强制Read（对抗500万token上下文压缩）。

### 2026-06-15 — 皮影戏决赛战略+单人物音效光效硬件方案

- **战略决策**：决赛只做一个角色的自动化（蔡俊—机长），用音效和光效弥补角色数量简化。"一人、一灯、一影、一腔"的纯粹→数字化应强化而非稀释。
- **硬件方案**：Arduino Uno+PCA9685+4路SG90金属齿舵机(动作) + DFPlayer Mini+microSD+PAM8403功放(音效) + WS2812B灯带60灯珠+FastLED库(光效)。预算约100元，重量<300g。
- **代码架构**：五层分离 config.h→motion→audio→light→choreography。事件驱动编排，时间轴触发。
- **音效设计**：5个MP3音频文件（开场BGM/引擎启动/起飞爬升/提示音/谢幕BGM），DFPlayer Mini通过SoftwareSerial通信+BUSY引脚硬件握手同步。
- **光效设计**：5种模式（暖光常亮3000K/冷光常亮6000K/呼吸闪烁/熄灭/冷暖渐变），30fps刷新率。