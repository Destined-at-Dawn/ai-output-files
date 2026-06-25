# 双路由文件混乱 + 技能自动激活系统性失败

## 日期
2026-06-08

## 事故概述
AI 在整轮对话中（约11个环节）**零次调用 skill**，所有工作手动完成。用户指出后复盘发现根因是多层次的系统性故障。

## 事故完整链条

### 直接原因：路由表空白区
`skill-routing-table.json` 中存在但缺少 `li-*` 系列 skill 的触发词（0条），导致 AI 扫描触发词时无法匹配。

### 深层根因 1：双路由文件混乱
两个路由文件同时存在且格式不同：
- `skill-routing-table.json`（根目录）→ 111条规则，triggers[] 格式，Step 4.5 加载
- `.claude/skill-rules.json` → 37条规则，keywords[] 格式，CLAUDE.md §Skill路由段引用

CLAUDE.md 同时引用两者，造成 AI 不知道该读哪个。且 skill-rules.json 中包含已废弃的 skill（li-skillfusion、claude-skill-verilog）。

### 深层根因 2：缺失技能自动激活协议
CLAUDE.md 引用了 `.claude/rules/skill-auto-activation.md` 但该文件**不存在**。路由表只被当作"参考"读取，没有强制匹配-调用协议。

### 深层根因 3：skill 被视为"可选参考"
即使路由表有匹配，AI 也倾向于"手动 Read SKILL.md"替代 `mcp__skill-handler__Skill` 调用。这绕过了 skill 的强制工作流和门禁。

## 为什么看起来行其实不行
- 路由表"存在"且"有内容" → 看起来 skill 激活机制正常
- CLAUDE.md "写了"自动激活规则 → 看起来协议已定义
- 但实际上：双文件打架 + 协议文件缺失 + 无强制匹配逻辑 = 纸面上完美，实战中完全失效

## 退出判据
当以下所有条件同时满足时，技能自动激活才算真正修复：
1. ✅ 双路由文件统一为单一真相源
2. ✅ 废弃文件加 _deprecated 标记
3. ✅ CLAUDE.md 清除过期引用
4. ✅ 创建 skill-auto-activation.md 硬协议
5. ✅ 新对话中 AI 实际调用了 ≥80% 应调用的 skill

## 修复清单

| # | 修复项 | 文件 | 状态 |
|---|-------|------|------|
| 1 | 废弃 .claude/skill-rules.json | `.claude/skill-rules.json` | ✅ 已加 _deprecated 标记 |
| 2 | 统一 CLAUDE.md 路由引用 | `CLAUDE.md` §Skill路由段 | ✅ 已改为单一引用 skill-routing-table.json |
| 3 | 修复 MEMORY.md 过期引用 | `MEMORY.md` | ✅ 已更新 |
| 4 | 创建技能自动激活协议 | `.claude/rules/skill-auto-activation.md` | ✅ 已创建 v1.0 |
| 5 | 交接文档 | `outputs/handoff-20260608.md` | ✅ 已创建 |
| 6 | 自我进化归档 | 本文件 | ✅ 已完成 |

## 影响范围
- 所有工作区的 skill 自动激活机制
- CLAUDE.md Step 4.5 加载路由表后的执行协议
- 新对话的启动质量（错误的 skill 调用 = 整轮对话质量崩塌）

## 关联法则
- 法则 7（负结果归档）：本事故必须归档，防止新对话重复
- 法则 8（门禁文化）：skill 调用是工作流门禁，绕过 = 跳过所有验证
- 法则 10（规则结晶）：发现→修复→写入规则→Skill，完整闭环
