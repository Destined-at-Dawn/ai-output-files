# 外部研究库（技能创建/管理领域）

> 来源：GitHub 全局搜索（按 Stars 降序）+ skills.sh + Agent Skills Hub
> 搜索策略：宽泛关键词 → 四阶段全平台覆盖（详见 SKILL.md Phase 1 Step 1.1b）

---

## S 级（必读，直接可用的高质量实现）

### 1. mattpocock/skills（GitHub, 19 个 skill）
**搜索词**：`claude code skills`
**核心价值**：极简 skill 设计典范——diagnose(117行)/triage(103行)/caveman(49行)
**学到的机制**：
- **反馈循环优先**：先建反馈循环（能跑测试），再修 bug——不建反馈循环就修 = 盲修
- **5 状态机分流**：triage 的 investigating/fixing/done/wontfix/blocked 状态追踪
- **75% token 压缩**：caveman 模式——技术精度不丢，但输出极简
**对 li-skillcreate 的启示**：好 skill 不需要 500 行——49 行的 caveman 比 500 行的臃肿 skill 更实用

### 2. facebookresearch/HyperAgents（GitHub, 2.6K★）
**搜索词**：`self-improving agent`
**核心价值**：双层架构（task agent + meta agent）——元认知自修改
**学到的机制**：
- **改进流程本身也应该被优化**——meta agent 审查 task agent 的改进效果
- **跨域迁移**——一个领域的改进模式可迁移到另一个领域
**对 li-skillcreate 的启示**：Phase 7 的自动进化不只是"教训固化"，还应该审查"进化流程本身是否有效"

### 3. letta-ai/letta（GitHub, 23.2K★）
**搜索词**：`stateful agent memory`
**核心价值**：有状态 agent + 分层记忆架构
**学到的机制**：
- **分层记忆**：短期（对话）/ 中期（任务）/ 长期（跨对话）——和我们的三层记忆对应
- **记忆一致性**：多 agent 共享记忆时的一致性保证
**对 li-skillcreate 的启示**：技能创建过程中产生的知识（设计决策/教训/模式）应该分层存储

### 4. ASI-Arch/Hue（GitHub, 3.7K★）
**搜索词**：`meta skill prompt engineering`
**核心价值**：跨 AI 平台 prompt 构建框架（六维：目标/平台/约束/例证/格式/审计）
**学到的机制**：
- **平台适配**：同一个 prompt 在不同平台（Claude/GPT/Gemini）需要不同写法
- **审计维度**：prompt 完成后必须过 6 维审计
**对 li-skillcreate 的启示**：SKILL.md 的 description 应该考虑不同 AI 工具的路由匹配差异

---

## A 级（值得参考，提取部分机制）

### 5. peterskoett/self-improving-agent（GitHub, 641★）
**搜索词**：`self-improving`
**核心价值**：Hook 驱动 + 结构化日志 + 自动 skill 提取
**学到的机制**：
- `.learnings/` 三文件日志（LRN/ERR/FEAT 编号系统）
- `Recurrence-Count ≥ 3 + 跨 ≥ 2 任务 + 30 天内` 自动晋升规则
- `extract-skill.sh` 自动提取独立 skill
**对 li-skillcreate 的启示**：教训固化不能靠 AI 记得——需要结构化日志 + 自动计数

### 6. Jeffallan/claude-skills embedded-systems（GitHub, 459★）
**搜索词**：`embedded systems claude`
**核心价值**：嵌入式 skill 的结构化模板（6 步工作流 + ISR/FreeRTOS/GPIO 模板）
**对 li-skillcreate 的启示**：领域专用 skill 的 references/ 应该包含代码模板

### 7. AGENTS.md 标准（Linux Foundation, 60K+ 项目采用）
**搜索词**：`AGENTS.md standard`
**核心价值**：给 AI Agent 的标准化指令文件格式
**学到的机制**：
- 指令预算 150-200 条（Augment Code 研究）——和我们的 300 行限制一致
- 可检测性——Agent 应该能自动发现和加载 AGENTS.md
**对 li-skillcreate 的启示**：SKILL.md 应该有机器可读的 frontmatter 让路由系统自动发现

### 8. agent-starter-pack（Google, 3K★）
**搜索词**：`agent workspace scaffold`
**核心价值**：Agent 项目脚手架标准化
**对 li-skillcreate 的启示**：新建 skill 后的标准检查清单可以自动化

---

## B 级（了解即可，间接参考）

### 9. skillsmith/forge-me
**核心价值**：技能质量评估框架
**参考点**：评分维度（功能完整性/代码质量/文档质量/测试覆盖）

### 10. awesome-claude-skills（社区维护）
**核心价值**：61,000+ skill 的索引
**参考点**：分类体系（工具/创作/开发/研究/生活）

### 11. jennyzzt/dgm（GitHub, 2.1K★）
**搜索词**：`open-ended evolution`
**核心价值**：开放式进化算法
**参考点**：进化不只是"教训固化"——还包括探索新能力

### 12. metauto-ai/GPTSwarm（GitHub, 1.0K★）
**搜索词**：`self-optimizing agent`
**核心价值**：RL/Prompting 自优化
**参考点**：优化目标应该是"用户满意度"不是"技能数量"

---

## 搜索历史

| 日期 | 搜索词 | 平台 | 找到数量 | 关键发现 |
|------|--------|------|---------|---------|
| 2026-06-09 | `self-improving agent` | GitHub | 10+ | HyperAgents(2.6K★)/Letta(23.2K★)/peterskoett(641★) |
| 2026-06-09 | `claude code skills` | GitHub | 10+ | mattpocock(19个skill)/AGENTS.md(60K+项目) |
| 2026-06-09 | `skill creation agent` | skills.sh | 5+ | skill-creator/skill-vetter/output-skill |
| 2026-06-09 | `meta skill prompt` | GitHub | 5+ | Hue(3.7K★) |
| 2026-06-09 | `embedded systems claude` | GitHub | 5+ | Jeffallan(459★)/ezrover |
