---
name: wechat-analysis
description: |
  微信聊天记录分析主入口 v3.0。四模式：分类汇总/精细查询/联系人统计/会话导出。
  自动探测解密DB路径，不硬编码。支持zstd解压、sender映射、群聊成员名解析。
  触发词：微信/聊天记录/聊天统计/私聊排行/群聊排行/微信数据库/wechat
version: "3.0"
---

# 微信聊天记录分析 v3.0

## 引用文档

| 文档 | 路径 | 用途 |
|------|------|------|
| DB 结构速查 | `references/db-structure.md` | 表名/字段/消息类型码/zstd 解压 |
| Sender 映射 | `references/sender-resolution.md` | 私聊/群聊发送者 ID → 姓名 |
| 踩坑铁律 | `references/pitfalls.md` | 22 条编码/解密/导出避坑规则 |

---

## Phase 0: 环境探测

**目标**：定位已解密的 SQLite 数据库，不硬编码路径。

**搜索顺序**：
1. **用户指定路径**（优先级最高）
2. **创作区原始解密**：`E:\ai产出文件\牛马\创作\创作\output\wechat_decrypted\`
3. **Temp 备份**：`C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22\`
4. **其他常见位置**：扫描 `%TEMP%` 下 `wechat-decrypted*` 目录

**验证步骤**：
- 检查 `message_0.db` 是否存在且可读
- `python -c "import sqlite3; conn=sqlite3.connect(path); print(len(conn.execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall()))"` 验证表数量
- 预期：16 个 DB 文件，~500 张表

**输出**：DB 根路径 + 文件清单

---

## Phase 1: 分类汇总报告

**目标**：一次扫描生成全局概览。

**执行步骤**：
1. 遍历 `message_0.db` ~ `message_9.db`（及 `message.db`）
2. 按 `StrTalker` 分组统计消息数
3. 区分私聊（`@chatroom` 不出现）和群聊（`@chatroom` 出现）
4. 按消息数降序排列
5. 输出 Top 20 联系人 + Top 20 群聊

**输出格式**：
```
## 分类汇总报告
- 总消息数：XXX
- 私聊会话数：XXX | 群聊会话数：XXX
- 时间跨度：YYYY-MM-DD ~ YYYY-MM-DD

### 私聊 Top 10
| 排名 | 联系人 | 消息数 | 最近消息时间 |
|------|--------|--------|-------------|

### 群聊 Top 10
| 排名 | 群名 | 消息数 | 最近消息时间 |
|------|------|--------|-------------|
```

---

## Phase 2: 精细查询

**目标**：按需查询特定联系人/群聊的详细数据。

**支持的查询类型**：
- **联系人查找**：模糊匹配 `StrTalker` 字段（wxid / 昵称 / 备注）
- **消息内容查询**：按时间范围、关键词、消息类型过滤
- **统计分析**：日均消息数、活跃时段分布、消息类型分布
- **聊天导出**：委派给 `wechat-exporter` skill

**查询模板**：
```python
# 查找联系人
SELECT DISTINCT StrTalker FROM MSG WHERE StrTalker LIKE '%关键词%'

# 按时间范围查询
SELECT * FROM MSG WHERE StrTalker='目标' AND CreateTime BETWEEN start AND end

# 消息类型分布
SELECT Type, COUNT(*) FROM MSG WHERE StrTalker='目标' GROUP BY Type
```

---

## Phase 3: 会话导出

**委派**：当用户要求导出聊天记录为文件时，路由到 `wechat-exporter` skill。

**触发信号**：导出/转成MD/保存聊天/聊天记录文件

---

## Phase 4: 心理蒸馏

**委派**：当用户要求分析人格/性格/心理画像时，路由到 `wechat-distiller` skill。

**触发信号**：蒸馏/心理画像/人格分析/性格分析/XX是什么样的人

---

## 反模式

1. **硬编码路径**：不要假设 DB 在某个固定位置，每次都要 Phase 0 探测
2. **忽略 zstd 压缩**：新版微信消息内容用 zstd 压缩，不解压会得到乱码
3. **sender_id 硬编码**：不同聊天的 sender_id 含义不同，必须查映射表
4. **一次性加载全部消息**：大群可能有 10 万+消息，必须分页或限制范围
5. **不验证 DB 完整性**：解密可能中途失败，必须先验证表数量
6. **拍一拍不过滤**：系统消息（Type=10000）中拍一拍占比 40%+，必须先过滤

---

## 条件下一步

| 用户意图 | 下一步 | 路由目标 |
|---------|--------|---------|
| "看看有哪些聊天" | Phase 1 分类汇总 | 本 skill |
| "查一下 XXX 的消息" | Phase 2 精细查询 | 本 skill |
| "导出 XXX 的聊天记录" | Phase 3 导出 | wechat-exporter |
| "分析 XXX 是什么样的人" | Phase 4 蒸馏 | wechat-distiller |
| "群聊里有什么资源" | 资源过滤 | community-filter |
