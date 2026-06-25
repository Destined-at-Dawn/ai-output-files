# 生命周期日志格式

> 用途：lifecycle-log.md 的标准格式和查询命令

---

## lifecycle-log.md 格式

每个技能目录可维护一个操作日志：

```markdown
# 技能生命周期日志

| 日期 | 操作 | 详情 | 操作者 |
|------|------|------|--------|
| 2026-06-07 | 创建 | 初版 v1.0 | li-skillcreate |
| 2026-06-07 | 融合 | 与 xxx 合并 | li-skillfusion |
| 2026-06-07 | 拆分 | 提取 xxx 模块 | li-skillfusion |
| 2026-06-07 | 弃用 | 被 yyy 替代 | li-manage 诊断 |
| 2026-06-07 | 恢复 | 重新启用 | 用户要求 |
```

---

## 查询命令

| 查询意图 | 操作 |
|---------|------|
| "这个技能的历史" | 读取 lifecycle-log.md，搜索该技能名 |
| "最近的技能操作" | 读取 lifecycle-log.md 最后 10 条 |
| "哪些技能被弃用了" | 搜索所有 DEPRECATED.md |
| "哪些技能是从其他技能拆分的" | 搜索 _meta.json 的 parent_skill 字段 |
| "微技能列表" | 搜索所有 .workspace-only 文件 |

---

## 操作类型

| 操作 | 说明 | 典型操作者 |
|------|------|-----------|
| 创建 | 新技能初版 | li-skillcreate |
| 融合 | 两个技能合并 | li-skillfusion |
| 拆分 | 从大技能提取模块 | li-skillfusion |
| 弃用 | 添加 DEPRECATED.md | li-manage 诊断 / 用户 |
| 恢复 | 重新启用已弃用技能 | 用户要求 |
| 定制 | 工作区特化版 | li-skillfusion |
