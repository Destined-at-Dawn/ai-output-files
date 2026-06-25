# 生态系统每日健康报告 2026-06-21

> 自动化定时任务 · 数据采集时间 08:00 CST
> 对比基线：2026-06-17 审计报告

---

## 系统指标（对比上次审计 06-17）

| 指标 | 今日 (06-21) | 上次 (06-17) | 变化 | 状态 |
|------|-------------|-------------|------|------|
| total_routes | 104 | 105 | -1 | ✅ |
| routed_skills | 104 | 105 | -1 | ✅ |
| total_triggers | 1632 | 1633 | -1 | ✅ |
| duplicate_triggers | 15 | N/A | - | ⚠️ |
| trigger_conflicts | 14 | 14 | 0 | ⚠️ 持平 |
| unrouted_skills (active) | 47 | 8 | +39 | ❌ 恶化 |
| unrouted_skills (deprecated) | 5 | N/A | - | ✅ |
| shared_rules (mutual) | 31 | 30 | +1 | ✅ |
| 知识中枢教训 (6月) | 7 | N/A | - | ✅ |
| git_status | ✅ | ✅ | - | ✅ |

---

## 关键变化分析

### 1. unrouted_skills 从 8 暴涨到 47（+39）

**根因**：上次审计只统计了"有SKILL.md但无路由"的skill，本次扫描范围扩大到本地+全局两个目录（共155个skill），发现了大量历史遗留skill未注册路由。

**高价值unrouted skill**（建议优先补注册）：

| Skill | 场景 | 优先级 |
|-------|------|--------|
| li-embedded | 嵌入式/STM32/ARM | 🔴 高 |
| competition-yolo | YOLO竞赛训练 | 🔴 高 |
| li-zhongshu | 知识中枢守护 | 🟡 中 |
| baoyu-infographic | 信息图生成 | 🟡 中 |
| deep-research | 深度研究 | 🟡 中 |
| study-review-pdf | 复习PDF生成 | 🟡 中 |
| fpga | FPGA开发指南 | 🟡 中 |
| session-audit | 会话审计 | 🟢 低（hook自动触发） |

**已弃用但仍无路由**（5个，无需处理）：
- jc-plan, li-persona-qa, three-tier-memory, web-artifacts-builder, 行业研究

### 2. trigger_conflicts 14 个持平

冲突触发词分布：

| 冲突触发词 | 涉及skill | 建议 |
|-----------|-----------|------|
| "文风DNA" | li-wechat-distiller, niuma-voice-dna, wechat-consultant | 🔴 优先级裁决：niuma-voice-dna 保留，其余移除 |
| "小红书文案"/"写作风格" | li-xhs, niuma-voice-dna | niuma-voice-dna 优先级更高 |
| "公众号文章" | li-wechat, niuma-voice-dna | niuma-voice-dna 优先级更高 |
| "论文"/"paper" | blog-post-writer, li-research | 区分场景：学术用li-research，通用用blog-post-writer |
| "有没有现成的" | li-bestskill, li-script | li-bestskill 保留（搜索已有方案） |
| "批处理"/"批量处理" | li-script, li-workflow | 区分：脚本用li-script，流程用li-workflow |
| "道法术器"/"读书笔记" | html-to-notes, li-analyze/li-study | 按内容类型区分 |
| "脚本"/"写脚本" | li-code, li-script | li-script 保留（脚本库管家） |
| "嘉宾分享" | html-to-notes, wechat-consultant | 按来源区分 |

### 3. shared_rules 差异稳定

| 工作区 | 规则数 | 与mutual差异 | 状态 |
|--------|--------|-------------|------|
| mutual | 31 | 基准 | ✅ |
| competition | 26 | -5 | ⚠️ |
| creation | 24 | -7 | ⚠️ |
| personal | 21 | -10 | ⚠️ |
| job | 21 | -10 | ⚠️ |

**说明**：差异部分包含工作区特有规则，不一定需要同步。核心共享规则（no-blind-overwrite, script-safety-check, chinese-path-safety等）应确保全覆盖。

---

## 4 个工作区同步状态

| 工作区 | 最新memory | 日期 | 教训内容 | 待同步 |
|--------|-----------|------|---------|--------|
| 个人 | 2026-06-19.md | 06-19 | ❌ 无 | ⚠️ 2天无记录 |
| 创作 | 2026-06-09-小黎个人网站设计决策.md | 06-09 | ❌ 无 | ⚠️ 12天无记录 |
| 竞赛 | 2026-06-15.md | 06-15 | ❌ 无 | ⚠️ 6天无记录 |
| 求职 | 2026-06-21.md | 06-21 | ✅ 有 | ✅ 最新 |

### 知识中枢教训（6月新增）

| 日期 | 教训主题 | 同步状态 |
|------|---------|---------|
| 06-17 | Windows UTF-8 模式 | ⚠️ 待同步到mutual |
| 06-16 | Junction跨盘迁移+4技术坑 | ⚠️ 待同步到mutual/competition |
| 06-15 | HTML个人站经验孤岛化治理 | ⚠️ 待同步到creation |
| 06-14 | 动手前检查门禁缺失 | ✅ 已全局部署 |
| 06-01 | 文件存在不等于能被找到 | ✅ 已记录 |

---

## Git 健康

- **最近提交**：2026-06-21 02:00（auto batch commit）
- **NiumaAutoCommit**：正常运行 ✅
- **最近5次提交间隔**：~2小时，节奏正常
- **分支**：master

---

## 待处理问题（按优先级）

### 🔴 高优先

1. **trigger_conflicts 14个冲突未解决** — "文风DNA"相关冲突已扩散到3个skill，必须做优先级裁决
2. **高价值unrouted skill** — li-embedded（嵌入式）和competition-yolo（竞赛）对用户日常价值高，建议补注册

### 🟡 中优先

3. **创作区记忆断档12天** — 06-09后无记录，说明该区近2周无活跃对话或记忆未落盘
4. **知识中枢教训待同步** — 3条教训（06-15/16/17）已记录但未同步到对应工作区memory
5. **共享规则差异** — personal/job各21条 vs mutual 31条，需确认核心共享规则是否全覆盖

### 🟢 低优先

6. **duplicate_triggers 15个** — 同一触发词在不同skill中重复出现，影响路由精度
7. **ChatGPT Plus续费提醒** — 2026-06-27到期，还剩6天
8. **runtime-snapshot.md数字过时** — 仍写着92 routes/140 skills，需更新

---

## 今日建议行动

1. **触发词去重** — 对14个冲突触发词做优先级裁决，更新路由表（预计30分钟）
2. **补注册2个高价值skill** — li-embedded + competition-yolo（预计15分钟）
3. **同步知识中枢教训** — 将06-15/16/17的教训写入对应工作区memory（预计20分钟）
4. **更新runtime-snapshot.md** — 同步最新数字（5分钟）
5. **ChatGPT Plus续费** — 2026-06-27前完成续费

---

## 教训同步状态

| 来源 | 教训 | 同步目标 | 状态 |
|------|------|---------|------|
| 知识中枢 06-17 | Windows UTF-8 模式 | mutual | ⚠️ 待同步 |
| 知识中枢 06-16 | Junction迁移+4坑 | mutual + competition | ⚠️ 待同步 |
| 知识中枢 06-15 | HTML孤岛化治理 | creation | ⚠️ 待同步 |
| 知识中枢 06-14 | 动手前检查门禁 | 全局 | ✅ 已同步 |

---

## 生态健康评分

**综合评分：72/100**（较06-17下降5分）

| 维度 | 得分 | 说明 |
|------|------|------|
| 路由覆盖 | 68 | 104/155 skill有路由（67%），unrouted过多 |
| 触发词质量 | 65 | 14个冲突+15个重复，路由精度受影响 |
| 记忆连续性 | 70 | 创作区断档12天，其他区基本正常 |
| 规则一致性 | 75 | 核心规则覆盖，但差异较大 |
| 教训同步 | 78 | 知识中枢有记录，但本地同步滞后 |
| Git健康 | 95 | 自动提交正常，节奏稳定 |

---

*报告生成：自动定时任务 · 下次审计：2026-06-22*
