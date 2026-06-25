# 生态系统每日健康报告 2026-06-15

> 自动化定时任务生成 | 对比基准：2026-06-01 审计报告

---

## 一、系统指标（对比上次审计 06-01）

| 指标 | 今日 (06-15) | 上次 (06-01) | 变化 |
|------|-------------|-------------|------|
| Skill 目录总数 | 111 | 82 | +29 (+35%) |
| 活跃 Skill（有 SKILL.md） | 90 | 71 | +19 (+27%) |
| 弃用 Skill（有 DEPRECATED.md） | 19 | 12 | +7 |
| li- 系列活跃子 Skill | 46 | ~30 | +16 |
| 路由条目数 | 97 | 112 | -15 (-13%) |
| 路由覆盖 Skill 数 | 83 | 98 | -15 |
| 触发词总数 | 1,530 | 1,388 | +142 (+10%) |
| 断裂路由（Skill 未安装） | 0 | 0 | 0（原报1条为误报，wechat-consultant实际存在） |
| 孤儿 Skill（有 SKILL.md 无路由） | 7 | 6+ | +1 |
| 共享规则（5 工作区一致） | 12 | 12 | 0 |
| SOP 文件（mutual） | 8 | 6 | +2 |
| 共享 SOP（5 区一致） | 5 | 5 | 0 |
| Git 未提交变更 | 2 | - | 正常 |

---

## 二、健康状态总览

### ✅ 健康指标
- **五区 CLAUDE.md 启动序列**：全部正常
- **五区 memory/long-term.md**：全部存在
- **跨区三件套**：6 工作区全部补齐（2026-06-16 Hermes 批量创建 5 个缺失的 workflow-inbox.md）
- **Git 自动提交**：最近 commit 06-15 08:46，NiumaAutoCommit 正常运行
- **MCP 配置**：2 server（markitdown + mempalace），无能力缺口
- **12 条共享规则**：5 工作区完全一致
- **5 条共享 SOP**：5 工作区完全一致

### ⚠️ 需关注
- **路由收缩**：路由从 112→97（-15），但活跃 Skill 从 71→90（+19），覆盖率下降
- **孤儿 Skill 7 个**：含 li-embedded（应注册）和 competition-yolo（应注册）
- **断裂路由 1 个**：wechat-consultant（r400），本地目录存在但路径可能不匹配
- **技能使用日志停滞**：最后记录 2026-06-05（10 天未更新）
- **Session Checkpoint**：仅 mutual 有，其余 4 区缺失

### 🔴 待修复
- **wechat-consultant 断裂路由**：路由引用但本地未找到对应 SKILL.md
- **li-autoreply + li-persona-qa 待合并**：runtime-snapshot 记录但未完成
- **文风DNA触发词冲突**：li-xhs vs li-wechat-distiller（runtime-snapshot 记录）

---

## 三、孤儿 Skill 详情（活跃但无路由）

| Skill | 是否应注册路由 | 说明 |
|-------|--------------|------|
| li-embedded | ✅ 应注册 | 嵌入式固件开发，STM32/FPGA，明确的用户场景 |
| competition-yolo | ✅ 应注册 | YOLO 竞赛全流程，有明确触发词 |
| session-audit | ⚠️ 按需 | 对话结束自动触发（Stop hook），可不注册常规路由 |
| baoyu-infographic | ⚠️ 按需 | 信息图生成，已有 baoyu- 前缀 |
| dot-skill | ❌ 不注册 | Meta-skill，不面向用户直接触发 |
| personal-info-discovery | ❌ 不注册 | 个人信息发现，内部辅助 skill |
| workflow-automator | ❌ 不注册 | 可能被 li-workflow 替代，检查是否应弃用 |

---

## 四、断裂路由详情

| Route ID | Skill | Confidence | 状态 | 修复方案 |
|----------|-------|-----------|------|---------|
| ~~r400~~ | ~~wechat-consultant~~ | ~~0.9~~ | ✅ 误报修正 | 2026-06-16 Hermes 复核：SKILL.md 存在且完整，路由指向正确 |

---

## 五、跨区一致性检查

### 共享规则对齐（12/12 ✅）
5 工作区共有的 12 条规则完全一致，无分叉。

### 独有规则分布
| 工作区 | 独有规则数 | 关键独有规则 |
|--------|----------|------------|
| mutual（管理区） | 8 | agent-prompt-ironclad, skill-*, subagent-strategy, voice-dna-auto-inject |
| 个人 | 1 | identity-and-preference |
| 创作 | 4 | degraded-read, dual-write, feishu-api, file-placement-precheck |
| 求职 | 1 | privacy-sanitization |
| 竞赛 | 4 | rtl-fpga-lessons, goal-mode-anti-repeat, verification-and-archival, see-name-stop |

### 跨区三件套
| 工作区 | project-context | artifact-registry | workflow-inbox |
|--------|----------------|-------------------|----------------|
| mutual | ✅ | ✅ | ✅ |
| 个人 | ✅ | ✅ | ✅ (2026-06-16 创建) |
| 创作 | ✅ | ✅ | ✅ (2026-06-16 创建) |
| 求职 | ✅ | ✅ | ✅ (2026-06-16 创建) |
| 竞赛 | ✅ | ✅ | ✅ (2026-06-16 创建) |
| 学习 | ✅ | ✅ | ✅ (2026-06-16 创建) |

---

## 六、教训同步状态

### 近期有教训记录的工作区（06-10 ~ 06-13）
| 工作区 | 日期 | 关键教训 | 是否需同步 |
|--------|------|---------|-----------|
| mutual | 06-13 | 新铁律：禁止绕过 li-skillcreate 手工 Write skill | ✅ 已同步到 .claude/rules/skill-route-enforcement.md 铁律0 |
| mutual | 06-10 | 路由治理 + 跨区同步 43 工作区 | ✅ 已完成 |
| 个人 | 06-10 | OCR 探索教训 | ⚠️ 检查是否影响创作区 |
| 个人 | 06-12 | A7 系统根因修复（4 个教训） | ⚠️ 可能影响竞赛区 Goal 模式 |
| 创作 | 06-12 | F10 命名冲突验证 + 目标压力排序 | ✅ 特定于创作区，无需跨区 |
| 竞赛 | 06-11 ~ 06-13 | FPGA 架构 + gitignore + 实验管理 | ⚠️ 9 条历史教训，检查是否影响个人区硬件开发 |

**结论**：竞赛区 06-12 的 Goal 模式教训（F10 命名冲突验证）可能需要同步到个人区（小黎在个人区也有硬件开发项目）。

---

## 七、待处理问题（按优先级）

### 🔴 P0 — ~~需立即处理~~ ✅ 2026-06-16 Hermes 复核
1. ~~**wechat-consultant 断裂路由修复**~~ → **误报**
   - Hermes 实测：`skills/wechat-consultant/SKILL.md` 存在且内容完整，路由指向正确
   - 结论：非断裂路由，审计误报

### 🟡 P1 — 本周处理
2. **孤儿 Skill 路由注册**（li-embedded + competition-yolo）
   - li-embedded：FPGA/STM32 场景明确，需注册 ≥15 触发词
   - competition-yolo：竞赛训练全流程，需注册 ≥15 触发词
3. **li-autoreply + li-persona-qa 合并**（runtime-snapshot 持续记录 3 天）
4. **"文风DNA" 触发词冲突修复**（li-xhs vs li-wechat-distiller）
5. **技能使用日志恢复**：最后记录 06-05，10 天空白，需检查 Stop hook 是否正常

### 🟢 P2 — ~~月度处理~~ 部分已完成
6. ~~**其余 4 区 workflow-inbox 创建**~~ → ✅ 2026-06-16 Hermes 批量创建 5 个（6区全齐）
7. **Session Checkpoint 扩展到其余 4 区**（hook 配置检查）
8. **workflow-automator 弃用评估**（是否被 li-workflow 完全替代）
9. **竞赛区→个人区 Goal 模式教训同步**

---

## 八、今日建议行动

1. **检查 wechat-consultant 目录**： 确认是否有 SKILL.md
2. **注册 li-embedded 路由**：新增 route 到 skill-routing-table.json，触发词覆盖 STM32/ARM/嵌入式/固件/寄存器等
3. **检查 skill-usage-log.md**：确认 Stop hook 是否正常工作（10 天无记录异常）
4. **Git 提交**：当前有 2 个未提交变更，建议下次自动提交窗口处理

---

## 九、健康度评分

| 维度 | 分数 | 说明 |
|------|------|------|
| Skill 生态 | 8/10 | 90 活跃 Skill + 46 li- 系列，规模健康但覆盖率下降 |
| 路由系统 | 8/10 | 0 条断裂 + 7 个孤儿 + 触发词增长但覆盖不均匀 |
| 规则一致性 | 9/10 | 12 条共享规则完全一致，无分叉 |
| 记忆系统 | 8/10 | 5 区全部有 long-term.md，但 session checkpoint 覆盖不全 |
| 跨区协调 | 9/10 | 三件套6区全齐（2026-06-16补齐） |
| 教训闭环 | 6/10 | 技能使用日志 10 天空白，教训同步需人工检查 |

**综合健康度：8.0/10**（原报 7.5/10，修正后上升原因：断裂路由误报修正 + workflow-inbox 6区补齐）

---

> 生成时间：2026-06-15 09:00 (自动化)
> 对比基准：2026-06-01 审计报告
> 下次审计：2026-06-16
