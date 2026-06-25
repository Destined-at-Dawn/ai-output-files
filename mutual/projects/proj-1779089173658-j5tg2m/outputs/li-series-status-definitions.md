# li-series 状态定义（单一真相源）

> 创建：2026-06-11 | 维护：Hermes 记忆中枢
> 目的：统一所有 li- 系列文档的数量统计口径，消除 before-after / final-status / logbook / memory 之间的矛盾

---

## 状态枚举

| 状态 | 定义 | 判断标准 |
|------|------|---------|
| **active** | 活跃 skill | 有 SKILL.md + 没有 DEPRECATED.md |
| **deprecated** | 已弃用，30 天缓冲期 | 有 DEPRECATED.md，目录还在 |
| **deleted** | 物理删除 | 目录不存在（归档目录有备份） |

## 统计口径（强制）

| 指标 | 计算方式 |
|------|---------|
| "活跃 skill 数" | 只统计 active |
| "总目录数" | active + deprecated |
| "质量通过率" | 只统计 active 中通过质量门禁的 |
| "弃用数" | 只统计 deprecated |
| "删除数" | 只统计 deleted（目录物理移除） |

## 禁止的表述

- ❌ "48 个活跃 skill"（实际 40 活跃 + 8 弃用）
- ❌ "48/48 (100%) 通过质量检查"（应为 40/40）
- ❌ "删除了 9 个 skill"（实际 0 物理删除，8 标记弃用）

## 验证命令

```bash
# 活跃 li- skill 数（无 DEPRECATED.md）
ls -d ~/.newmax/skills/li-*/SKILL.md 2>/dev/null | while read f; do
  dir=$(dirname "$f")
  [ ! -f "$dir/DEPRECATED.md" ] && basename "$dir"
done | wc -l

# 弃用 li- skill 数（有 DEPRECATED.md）
find ~/.newmax/skills/li-* -name "DEPRECATED.md" -type f | wc -l

# 总目录数（排除 .zip）
ls -d ~/.newmax/skills/li-*/ 2>/dev/null | grep -v '.zip' | wc -l
```

## 当前状态（2026-06-11 验证）

- 总目录：48（排除 .zip）
- 活跃：40
- 弃用：8（li-writing/li-session/li-voice/li-search/li-personal/li-docs/li-frontend/li-platform）
- 物理删除：0

---

> 本文件是 li- 系列文档的统计口径唯一权威源。所有文档（before-after / final-status / logbook / memory）的数量声明必须与本文件一致。
