# Phase 1 详细搜索方法论

> 本文件是 li-skillcreate SKILL.md Phase 1 的详细参考，包含联网搜索的完整方法论。

---

## 联网搜索平台矩阵（必须执行，不可跳过）

> 根因教训：不搜网上就造技能 = 闭门造车的平方。skills.sh 有 61,000+ skill，awesome-claude-skills 有 10,000+，大概率你想要的已经有人做过了。

**必须执行以下搜索（按优先级顺序，至少完成 P0）**：

| 优先级 | 平台 | 搜索方式 | 搜索词模板 |
|--------|------|---------|-----------|
| **P0** | skills.sh | `WebFetch("https://skills.sh/search?q={关键词}")` | `{功能关键词} skill` / `{功能关键词} Claude Code` |
| **P0** | GitHub awesome-claude-skills | `WebFetch("https://github.com/search?q={关键词}+claude+skill&type=repositories")` | `{功能关键词} claude code skill` |
| **P0** | MCP Registry | `WebFetch("https://modelcontextprotocol.io/registry?q={关键词}")` | `{功能关键词} MCP server` |
| **P1** | Agent Skills Hub | `WebFetch("https://agentskillshub.top/best/?q={关键词}")` | `{功能关键词} agent skill` |
| **P1** | ToolSDK | `WebFetch("https://toolsdk.ai/mcp/search?q={关键词}")` | `{功能关键词} MCP tool` |
| **P2** | mcpm.sh | `WebFetch("https://mcpm.sh/search?q={关键词}")` | `{功能关键词}` |

---

## 搜索关键词生成规则

1. 从用户需求中提取核心功能词（2-3 个）
2. 翻译成英文搜索词（中文 skill 生态太小，英文搜索命中率高 10 倍）
3. 至少搜 3 组不同关键词组合

---

## 搜索结果评估

对每个找到的 skill/MCP：
- 功能相似度 > 70%？→ **必须深入读取其 SKILL.md / README**，提取设计模式
- 功能相似度 40-70%？→ 记录为参考，提取可借鉴的机制
- 功能相似度 < 40%？→ 记录存在，不深入

---

## 搜索结果汇报格式（必须输出给用户看）

```markdown
## 联网搜索结果

### 找到 N 个相关 skill/MCP

| # | 名称 | 来源 | 相似度 | 核心功能 | 是否值得参考 |
|---|------|------|--------|---------|-------------|
| 1 | xxx | skills.sh | 85% | ... | ✅ 深入读取 |
| 2 | yyy | GitHub | 60% | ... | ⚠️ 记录参考 |
| 3 | zzz | MCP Registry | 30% | ... | ❌ 仅记录 |

### 结论
- [可以直接用/需要本地化改造/没有现成的需要从零造]
- 参考了哪些设计模式：...
```

**铁律：跳过联网搜索 = 违规。"本地没有所以要造"不是理由——网上可能有。**

---

## 本地技能扫描命令

```powershell
# 列出所有可用技能
ls ${NEWMAX_HOME}/skills/ | Select-Object Name
ls C:/Users/13975/.codex/skills/ | Select-Object Name
ls "E:\ai产出文件\牛马\mutual\mutual\skills\" | Select-Object Name
```

---

## 分类并深入读取（Step 1.2）

综合本地 + 联网搜索结果，按与新技能的关联度分类，然后**深入读取至少 5 个最相关的 SKILL.md/README**（本地 + 网上各至少 2 个）：

| 关联类型 | 读什么 | 提取什么 |
|---------|--------|---------|
| **功能相似** | 同类技能的 SKILL.md | 工作流模式、Phase 结构 |
| **理念优秀** | 高质量 skill 的设计哲学 | 触发词设计、行动锁、问题消解 |
| **生态集成好的** | 一鱼多吃做得好的 skill | 生态副作用清单、文件更新模式 |
| **迭代设计好的** | 有自我进化能力的 skill | 数据采集、自动优化规则 |
| **教训相关的** | conversation-to-knowledge | 教训固化流程、失败模式 |

---

## 设计模式提取模板（Step 1.3）

从每个参考 skill 中提取 1-3 个核心设计决策：

```markdown
## 参考技能设计模式提取

| Skill | 核心机制 | 为什么好 | 如何融入新技能 |
|-------|---------|---------|--------------|
| jc-clarifier | 行动锁 | 防止模糊需求导致垃圾产出 | Phase 0 加澄清漏斗 |
| dbs-diagnosis | 问题消解 | 90% 的需求是假需求 | 创建前先消解 |
| li-devil | 触发词从对话中长出来 | 路由越用越准 | 触发词自进化 |
| ... | ... | ... | ... |
```

**铁律：不读 5 个以上已有技能就动手 = 违规。**
