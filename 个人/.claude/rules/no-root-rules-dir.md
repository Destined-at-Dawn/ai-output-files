# ⛔ 禁止创建根目录 rules/（防御性规则 — 最高优先级）

> Claude Code 自动加载本文件。每次对话启动时生效。不可跳过。

## 铁律

**根目录 `rules/` 是已废弃的目录，已全量删除。严禁在任何情况下重新创建。**

- ✅ 规则唯一存放位置：`.claude/rules/`（本文件所在目录）
- ❌ 禁止在根目录创建 `rules/` 目录
- ❌ 禁止在 proj-ID 目录创建 `rules/` 目录
- ❌ 禁止在任何文件中写入不含 `.claude/` 前缀的 `rules/` 路径

## 为什么 `.claude/rules/` 而非 `rules/`

1. **Claude Code 只自动加载 `.claude/rules/`** — 根目录 `rules/` 不会被加载
2. **避免重复** — 两份相同规则 = 维护成本翻倍 + 同步风险
3. **明确归属** — `.claude/` 前缀表明这是 Claude Code 专属的配置目录

## 如果你看到路径 `rules/`（不含 `.claude/` 前缀）

这是过时引用，必须修正。执行：
1. 将 `rules/xxx.md` 改为 `.claude/rules/xxx.md`
2. 如果是目录创建指令，改为操作 `.claude/rules/`
3. 如果是读取指令，改为读取 `.claude/rules/`

## 相关文件

- `.claude/rules/_MIGRATED-TO-RULES.md` — 迁移说明 + 反向防御
- `CLAUDE.md` § R16 根目录优先约束架构
- `CLAUDE.md` § ⛔ 防回退铁律

---

> 创建日期：2026-05-25
> 来源：R16 根目录优先约束架构治理
> 本规则属于"防御性规则"——预防 AI 在未来对话中重新创建已删除的 rules/ 目录。
