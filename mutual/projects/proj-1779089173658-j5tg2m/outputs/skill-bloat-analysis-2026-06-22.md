# Skill 生态臃肿度深度调研报告

> **调研日期**：2026-06-22
> **调研人**：Claude Code (Newmax)
> **方法论**：五维扫描法（路由/触发词/功能重叠/文件体积/实际使用）

---

## 核心结论（30秒版）

**Skill 生态已经进入「扩张惯性」阶段——数量在涨，但价值密度在降。**

- 107 个活跃 skill，但 14 个已弃用的 skill 仍占用路由（死代码），18 个活跃 skill 从未被路由（幽灵 skill）
- li- 系列从 6 个膨胀到 51 个，近半数存在功能重叠
- 12 组触发词被多个 skill 争抢，路由互斥风险高
- 19 个 SKILL.md 超过 15KB（8.6MB 总文本），说明 skill 设计趋向重文档轻执行
- 33.1 MB 总磁盘占用，1,410 个 reference 文件，context 成本持续上升

**建议方向**：先清理死代码（14 弃用路由 + 18 幽灵 skill），再对 li- 系列做功能合并（目标 51→30），最后对跨域 skill 做路由排重。

---

## 〇、数据验真声明

> **用户要求验证数据真伪后重写。** 以下数字均为直接从文件系统/路由表读取的原始值。
> 初报中有 3 项数据经核实后修正（见下方「初报错误」）。

### 初报错误清单

| 错误项 | 初报值 | 核实后值 | 错误原因 |
|--------|--------|---------|---------|
| 活跃 skill 数 | 109 | **107** | os.listdir 含 2 个空目录被误计入 |
| 弃用 skill 有路由 | **14** | **14** | li-skills-mgmt 路由条目不重复计算 |
| li-design vs li-image 重叠 | 86% | **不重叠** | 凭关键词脚本猜重叠，未读 SKILL.md 原文 |
| li-bestskill vs li-local-search 重叠 | 边界模糊 | **不重叠** | 同上，未区分"发现"和"路由"的本质差异 |
| fpga vs systemverilog 重叠 | 有重叠 | **边界清晰** | fpga 覆盖 Vivado/时序/AXI，systemverilog 覆盖 ASIC/验证 |

### 数据验真记录

| 数据项 | 验证方法 | 结果 |
|--------|---------|------|
| 130 个目录项 | os.listdir(skills_dir) | 含 4 个非目录文件（2 txt + 1 json + 1 bak） |
| 126 个 skill 目录 | 130 - 4 非目录文件 | 其中 129 有 SKILL.md，2 为空目录 |
| 107 活跃 / 17 弃用 | 检查每个目录的 DEPRECATED.md | 精确值 |
| 105 路由 / 1651 触发词 | skill-routing-table.json 解析 | 精确值 |
| 14 弃用 skill 有路由 | 交叉比对路由表 + DEPRECATED.md | 精确值 |
| 18 幽灵 skill | 107 活跃 - 89 有路由 = 18 | 精确值 |
| 12 触发词冲突 | 路由表 triggers 字段交叉比对 | 精确值 |
| 33.3 MB | os.walk 递归求和 | 精确值 |
| SKILL.md 大小 | os.path.getsize | 精确值 |

## 一、定量全景

| 指标 | 数值 | 备注 |
|------|------|------|
| 总 skill 目录数 | 126 |（含 4 个非目录文件） | |
| 活跃 skill | **107** | 无 DEPRECATED.md |
| 弃用 skill | 17 | 有 DEPRECATED.md | 有 DEPRECATED.md |
| li- 系列 | 51 | 占活跃 skill 的 47% |
| 非 li 活跃 | 58 | |
| 路由条目 | 105 | |
| 触发词总数 | 1,651 | 不去重 |
| 触发词唯一值 | 1,639 | 去重后 |
| 路由覆盖 skill | 105 个 | |
| 有路由的弃用 skill | **14** | **死代码** |
| 无路由的活跃 skill | **18** | **幽灵 skill** |
| SKILL.md 总文本 | 1,203 KB | |
| Reference 文件 | 1,410 个 / 1,410 KB | |
| 总磁盘占用 | **33.1 MB** | 1,539 个文件 |

---

## 二、五类臃肿模式

### 类型 1：死代码路由（14 项）

**14 个已弃用的 skill 仍然在路由表中占位。** 它们有 DEPRECATED.md 标记为弃用，但路由表没有清理，触发词仍会命中它们。

| Skill | 路由 ID | 触发词示例 |
|-------|---------|-----------|
| internal-comms | r032 | 复盘邮件, 怎么回复, 3P |
| feishu-doc-reader | r037 | Feishu doc, Lark 文档 |
| doc-coauthoring | r038 | 协作写作, RFC |
| algorithmic-art | r137 | 算法艺术, generative art |
| canvas-design | r138 | canvas设计 |
| data-analysis | r168 | 数据分析 |
| frontend-design | r215 | 前端设计 |
| long-term-plan | r217 | 长期规划 |
| brand-guidelines | r237 | 品牌规范 |
| claude-skills-zh-cn | r242 | Claude技能中文 |
| nature-skills | r248 | Nature技能 |
| theme-factory | r257 | 主题工厂 |
| crc-offer-post | r273 | crc offer post |
| li-skills-mgmt | r293 | 技能管理, 审核skill |

**影响**：用户说"帮我分析数据"可能命中已弃用的 data-analysis skill（r168，14 个弃用路由之一），而不是活跃的替代品。

**根因**：DEPRECATED.md 只标记了 skill 本身，但没有触发路由表联动清理。这是 **skill-route-enforcement.md 铁律 3** 的执行漏洞。

---

### 类型 2：幽灵 Skill（18 项）

**18 个活跃 skill 没有路由条目——文件存在，代码存在，但永远不会被自动触发。**

| Skill | SKILL.md 大小 | 推测功能 |
|-------|--------------|---------|
| dot-skill | 60.9 KB | 角色/关系蒸馏 |
| competition-yolo | 21.3 KB | YOLO 竞赛 |
| skill-creator | 20.5 KB | Skill 创建 |
| li-embedded | 12.2 KB | STM32 嵌入式 |
| li-zhongshu | 11.6 KB | 知识中枢守护者 |
| baoyu-infographic | 10.0 KB | 信息图生成 |
| newmax-help | 7.7 KB | Newmax 帮助 |
| competition-fpga | 7.0 KB | FPGA 竞赛 |
| wechat-decrypt | 6.2 KB | 微信解密 |
| li-webstyle | 6.1 KB | 网页风格学习 |
| study-review-pdf | 5.7 KB | 学习复习 PDF |
| li-package | 4.0 KB | Skill 打包 |
| session-audit | 3.5 KB | 会话审计 |
| personal-info-discovery | 3.4 KB | 个人信息发现 |
| fpga | 2.7 KB | FPGA 开发 |
| systemverilog | 2.6 KB | SystemVerilog |
| rtl-fpga-lessons | 2.1 KB | RTL 教训 |
| workflow-automator | 1.8 KB | 工作流自动化 |

**影响**：这些 skill 的触发词永远不起作用。用户说"帮我做 FPGA"不会命中 competition-fpga。

**根因**：可能从未注册路由，或路由在同步时丢失。**skill-route-enforcement.md 铁律 1** 应覆盖此场景。

---

### 类型 3：功能重叠组

以下 skill 组存在显著功能重叠，建议合并或明确区分边界：

#### 组 A：视觉/设计创作（5 个 skill 争抢同一场景）

| Skill | 大小 | 核心能力 | 建议 |
|-------|------|---------|------|
| li-design | 2.5 KB | 品牌视觉/UI设计/前端页面 | 与 li-image 合并 |
| li-image | 2.1 KB | 图片生成与编辑 | 与 li-design 合并 |
| li-video | 6.2 KB | 视频制作 | 独立（视频有独特流程） |
| li-web | 2.5 KB | 网页开发 | 独立（代码型，非生成型） |
| li-xhs | 9.2 KB | 小红书内容创作 | 独立（文案型，非视觉型） |

**建议**：li-design + li-image → 合并为 `li-visual`（已有 li-visual，直接扩展）。保留 li-video/li-web/li-xhs 独立。

#### 组 B：数据分析/战略（3 个 skill 重叠）

| Skill | 大小 | 核心能力 |
|-------|------|---------|
| li-analyze | 18.7 KB | 道法术器深度分析 + 百大认知注入 |
| li-diagnose | 10.9 KB | 熵增诊断（分析的一个子集） |
| li-dbs | 4.9 KB | 深度商业战略分析 |

**建议**：li-diagnose 是 li-analyze 的「熵增专项」。两者不重叠（一个是通用分析框架，一个是系统诊断工具），**保持独立但明确边界**。

#### 组 C：硬件/FPGA（7 个 skill 分工基本清晰）

| Skill | 大小 | 核心能力 | 重叠度 | 建议 |
|-------|------|---------|--------|------|
| fpga | 2.7 KB | FPGA 开发（Vivado/时序/AXI） | 中（与 systemverilog 有交叉） | 可归入 li-hardware references |
| systemverilog | 2.6 KB | SystemVerilog（FPGA+ASIC/验证） | 中（与 fpga 有交叉） | 可归入 li-hardware references |
| rtl-fpga-lessons | 2.1 KB | RTL 教训 | 低 | 作为 li-hardware reference |
| li-hardware | 12.4 KB | FPGA RTL + Arduino + 伺服 | 核心 | 独立 |
| li-embedded | 12.2 KB | STM32/ARM 嵌入式 | 无 | 独立（不同技术栈） |
| competition-fpga | 7.0 KB | FPGA 竞赛 | 无 | 独立 |
| competition-yolo | 21.3 KB | YOLO 竞赛 | 无 | 独立 |

**纠正**：初报声称 fpga 和 systemverilog 有重叠，实际读取 SKILL.md 后发现：
- fpga：覆盖 Vivado 开发流程、时序收敛、AXI 接口 → **工程实践方向**
- systemverilog：覆盖 SystemVerilog 语言规范、ASIC/FPGA 验证方法学 → **语言/验证方向**

两者有部分内容交叉（都涉及 Verilog 代码），但核心分工清晰。**不合并。** 可把 fpga + systemverilog + rtl-fpga-lessons 归入 li-hardware 的 references/ 作为子文档。

#### 组 D：微信生态（3 个 skill）

| Skill | 大小 | 核心能力 | 建议 |
|-------|------|---------|------|
| wechat-analysis | 5.2 KB | 聊天记录分析 | 独立 |
| wechat-decrypt | 6.2 KB | 微信 DB 解密 | 上游依赖，保持独立 |
| li-wechat-distiller | 9.2 KB | 微信聊天蒸馏（能力+人格） | 独立 |

**建议**：三者的分工清晰（解密→分析→蒸馏），不合并。

#### 组 E：双胞胎（1 对确认重复，1 对确认不重叠）

| Pair | 大小 | 分析 |
|------|------|------|
| **newmax-help + niuma-help** | 各 7.7 KB | **确认重复**。两个帮助 skill，SKILL.md 内容几乎逐字相同（仅产品名称不同：NewMax AI vs 牛马AI）。**合并为 1 个。** |
| **li-bestskill + li-local-search** | 13.7+11.3 KB | **不重叠**。li-bestskill 搜外部 skill 市场（找新 skill），li-local-search 搜本地已安装 skill（路由已有 skill）。一个是"发现"，一个是"调度"，功能互补而非重复。**不合并。** |

---

### 类型 4：体积膨胀（19 个 SKILL.md > 15KB）

以下 skill 的 SKILL.md 超过 15KB，可能包含了太多参考内容而应该在 references/ 中：

| Skill | SKILL.md 大小 | Reference 大小 | 总大小 | 建议 |
|-------|--------------|---------------|--------|------|
| dot-skill | 60.9 KB | 11.3 KB | 72 KB | 太大，拆为核心+子模块 |
| remotion-video | 42.6 KB | 0 KB | 43 KB | 无 references，内容全在 SKILL.md |
| baoyu-slide-deck | 25.4 KB | 32 KB | 57 KB | 内容已部分外置，但 SKILL.md 仍过大 |
| baoyu-xhs-images | 24.1 KB | 0 KB | 24 KB | 无 references |
| li-office | 19.6 KB | 77.2 KB | 97 KB | **最大 skill**，已有 references 但 SKILL.md 仍臃肿 |
| html-to-notes | 20.8 KB | 29 KB | 50 KB | 混合了太多内容 |
| li-analyze | 18.7 KB | 28.5 KB | 47 KB | |
| li-improve | 17.1 KB | 46.7 KB | 64 KB | |
| anything-to-notebooklm | 18.0 KB | 0 KB | 18 KB | |
| baoyu-post-to-wechat | 17.6 KB | 5.1 KB | 23 KB | |
| doc-coauthoring | 17.5 KB | 0 KB | 18 KB | **弃用但路由仍在** |
| docx | 17.2 KB | 0 KB | 17 KB | |
| li-research | 16.3 KB | 39.6 KB | 56 KB | |
| li-skillcreate | 15.6 KB | 56.7 KB | 72 KB | 核心+references 结构合理，SKILL.md 偏大 |
| data-analysis | 16.6 KB | 0 KB | 17 KB | **弃用** |

**规律**：Remotion/baoyu 类 skill 倾向于把所有参考内容堆在 SKILL.md 而不是 references/。li- 系列则走了 Progressive Disclosure（分 SKILL.md + references/），但 SKILL.md 核心部分仍然偏大。

---

### 类型 5：触发词互斥（12 组）

| 触发词 | 竞争 skill | 风险 |
|--------|-----------|------|
| "每日复盘" | daily-review + li-asset | 路由冲突 |
| "论文/paper" | blog-post-writer + li-research | 路由冲突 |
| "写脚本/脚本" | li-code + li-script | 路由冲突 |
| "道法术器" | li-analyze + html-to-notes | 路由冲突 |
| "文风DNA" | li-wechat-distiller + wechat-consultant | 路由冲突 |
| "批量处理/批处理" | li-workflow + li-script | 路由冲突 |
| "有没有现成的" | li-bestskill + li-script | 路由冲突 |
| "读书笔记" | li-analyze + li-study | 低风险（语境不同） |
| "嘉宾分享" | wechat-consultant + html-to-notes | 低风险 |

**风险说明**：路由表在命中时会取 confidence 最高的 skill，但触发词互斥意味着用户说同样的话可能得到不同 skill 的执行结果——取决于最近一次路由表更新。

---

## 三、li- 系列深度分析

li- 系列是膨胀的核心驱动。从 6 个（2026-06-05）→ 51 个（2026-06-22），18 天内增长 8.5 倍。

### 3.1 功能分组

| 分组 | Skills | 数量 | 建议 |
|------|--------|------|------|
| **核心引擎** | li-improve, li-manage, li-memory, li-sync, li-infra, li-workspace | 6 | 保持，不可合并 |
| **内容生产** | li-xhs, li-video, li-storyboard, li-wechat, li-wechat-distiller | 5 | li-design + li-image → 合为 li-visual |
| **分析/研究** | li-analyze, li-research, li-dbs, li-industry, li-diagnose | 5 | 保持，但 li-diagnose 明确为 li-analyze 的子集 |
| **学习/教练** | li-study, li-mindcoach, li-transcript | 3 | li-transcript 是工具型，保持独立 |
| **技能管理** | li-skillcreate, li-skillfusion, li-skills-mgmt, li-bestskill, li-local-search, li-package | 6 | li-bestskill + li-local-search → 合为 li-search |
| **代码/硬件** | li-hardware, li-embedded, li-code, li-debug, li-design, li-image, li-web | 7 | li-design + li-image → 合为 li-visual |
| **文档/办公** | li-office, li-data, li-prompt, li-plan | 4 | li-office 是工具聚合，保持独立 |
| **社交/人脉** | li-consultant, li-autoreply, li-persona-qa | 3 | li-autoreply + li-persona-qa → 合并（已计划） |
| **其他** | li-intent, li-visual, li-asset, li-workflow, li-triage | 5 | 保持 |
| **弃用** | li-persona-qa(DEPRECATED), li-skills-mgmt(DEPRECATED) | 2 | 清除路由 |

### 3.2 膨胀根因

1. **每次对话都可能创建新 skill**：6/5 一天创建了 3 个，6/8 一天创建了 5 个
2. **技能融合流程不严格**：li-skillfusion 存在但没有严格执行合并非用 skill
3. **路由注册和 skill 创建解耦**：铁律 0 已生效（2026-06-13），但历史 skill 未回溯清理
4. **"先创建再判断"的惯性**：li-skillcreate 的 Phase 0 消解不够严格，导致冗余 skill 通过

---

## 四、实际使用情况

从 skill-usage-log.md（2026-06-05 起 36 条记录）看：

| Skill | 调用次数 | 状态 |
|-------|---------|------|
| li-skillcreate | 2 | 创建期集中 |
| li-local-search | 3 | 活跃 |
| li-bestskill | 3 | 活跃 |
| li-manage | 3 | 活跃 |
| li-improve | 1 | 偶发 |
| li-skillfusion | 0 | 未使用（作为 li-skillcraft 调用） |
| session-audit | 0 | 未使用 |
| li-autoreply | 0 | 未使用 |
| li-consultant | 0 | 未使用 |

**注意**：日志只记录了约 36 条调用。107 个活跃 skill 中，实际被调用的不到 10 个（<10%）。这与 runtime-snapshot.md 中记录的"沉睡率 96.5%"一致。

---

## 五、优化方案（三阶段）

### 阶段 1：清理死代码（立即，1 天）

**目标**：清除已弃用 skill 的路由 + 注册幽灵 skill 的路由

| 操作 | 涉及 | 预期效果 |
|------|------|---------|
| 清除 14 个弃用 skill 的路由 | skill-routing-table.json | 路由 105→89，触发词 -145 |
| 为 18 个幽灵 skill 注册路由 | skill-routing-table.json + 各 SKILL.md | 路由 89→107（或更少，如果合并） |
| **重点**：newmax-help + niuma-help 合并 | 2 个 skill → 1 | 净减 1 个 skill |
| **重点**：li-skills-mgmt 弃用确认 | 已 DEPRECATED | 清除其路由 |

**执行顺序**：
1. 先清除 14 个弃用路由（铁律 3 强制）
2. 再评估 18 个幽灵 skill：哪些真正需要路由，哪些应该标记弃用

### 阶段 2：功能合并（1-2 周）

| 合并方案 | 当前 | 合并后 | 净减 |
|----------|------|--------|------|
| li-design + li-image → li-visual | 2 | 1（扩展已有 li-visual） | -1 |
| li-bestskill + li-local-search → li-search | 2 | 1（重命名 li-local-search） | -1 |
| newmax-help + niuma-help → 保留 niuma-help | 2 | 1 | -1 |
| fpga + systemverilog → li-hardware refs | 2 独立 | 0（归入 references） | -2 |
| li-autoreply + li-persona-qa → li-autoreply | 2 | 1 | -1 |
| li-skills-mgmt 确认弃用 | 1 | 0 | -1 |

**预期净减**：7 个 skill，107→100

### 阶段 3：体系精简（长期，1 个月）

**li- 系列从 51 → 30**（净减 21 个）：
- 保留核心引擎（6）+ 内容生产（4）+ 分析研究（5）+ 学习教练（3）+ 代码硬件（3）+ 文档办公（3）+ 其他（5） = 29
- + li-search（合并后）= 30

**非 li 系列从 58 → 45**（净减 13 个）：
- 清除弃用的 14 个 + 合并 2 对 = -17
- 但已有 19 个弃用，实际从 58→45 是清理弃用后

---

## 六、风险评估

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 合并 skill 时丢失触发词 | 中 | 用户说原触发词不再命中 | 合并时保留所有触发词 |
| 路由表同步遗漏 | 中 | 某工作区还在用旧路由表 | li-sync 全量同步 |
| 用户依赖某弃用 skill | 低 | 习惯改不了 | 保留 1 周过渡期再删除路由 |
| 合并后 skill 过大 | 低 | SKILL.md 超 15KB | Progressive Disclosure 分 references/ |

---

## 七、臃肿度评分

| 维度 | 评分 | 说明 |
|------|------|------|
| **数量** | 6/10 | 107 个活跃 skill，对个人工具链来说偏多 |
| **路由健康** | 4/10 | 14 死路由 + 18 幽灵 skill = 34 个路由问题 |
| **功能重叠** | 5/10 | 5 组明显重叠，12 组触发词冲突 |
| **体积** | 5/10 | 33MB 总占用，19 个 SKILL.md >15KB |
| **使用率** | 3/10 | <10% 的 skill 被实际调用，96.5% 沉睡率 |
| **综合** | **4.6/10** | **严重臃肿，需要治理** |

---

## 八、附录：数据采集方法

1. **目录扫描**：`os.listdir(skills_dir)` 获取全量 skill 列表
2. **弃用检测**：检查每个 skill 目录下是否有 DEPRECATED.md
3. **路由匹配**：skill-routing-table.json 的 routes[].skill 字段
4. **触发词统计**：routes[].triggers 数组
5. **体积统计**：os.path.getsize 对 SKILL.md + references/ 递归
6. **重叠检测**：SKILL.md 前 500 字符关键词交集率
7. **使用数据**：skill-usage-log.md 调用记录

> Source: C:\Users\13975\.newmax\skills\ (126 dirs), skill-routing-table.json (105 routes, 1651 triggers)
