---
name: wechat-exporter
description: |
  从已解密的微信数据库导出聊天记录为Markdown。
  支持私聊和群聊，格式：[日期 时间] 发言人：内容。
  自动处理zstd压缩、sender→姓名映射。
  触发词：导出聊天/转成MD/保存聊天/导出微信/聊天记录文件
version: "1.0"
---

# 微信聊天记录导出 v1.0

## 引用文档

| 文档 | 路径 | 用途 |
|------|------|------|
| Sender 映射 | `references/sender-mapping.md` | 私聊/群聊发送者 ID → 姓名实操指南 |
| DB 结构 | `../wechat-analysis/references/db-structure.md` | 表名/字段/zstd 解压 |
| 踩坑铁律 | `../wechat-analysis/references/pitfalls.md` | 22 条避坑规则 |

---

## Phase 0: 数据源确认

**目标**：确认有可用的已解密 DB。

**优先级**：
1. 用户指定路径
2. 已知解密路径（按 wechat-analysis Phase 0 探测）
3. 提示用户需要先解密

**验证**：
- `message_0.db` 存在且可读
- `contact.db` 存在且可读
- 表数量 >= 100

---

## Phase 1: 联系人/群聊查找

**目标**：根据用户指定的名称，找到对应的 StrTalker 标识。

**私聊查找**：
```python
# 在 contact.db 中查找
SELECT UserName, NickName, Remark FROM contact
WHERE NickName LIKE '%关键词%' OR Remark LIKE '%关键词%'
```

**群聊查找**：
```python
# 群聊的 StrTalker 格式为 wxid@chatroom
SELECT DISTINCT StrTalker FROM MSG
WHERE StrTalker LIKE '%@chatroom%'
```

**输出**：StrTalker 标识 + 会话类型（私聊/群聊）+ 预估消息数

---

## Phase 2: 消息导出

**目标**：将消息导出为 Markdown 文件。

### 私聊导出

```python
def export_private_chat(db_path, str_talker, contact_name):
    """私聊导出：Status=2 是我，Status=3 是对方"""
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT StrContent, CompressContent, CreateTime, Type, Status "
        "FROM MSG WHERE StrTalker=? ORDER BY CreateTime", (str_talker,)
    ).fetchall()

    lines = []
    for row in rows:
        content = decompress_message(row[1], row[0])
        ts = datetime.fromtimestamp(row[2], tz=timezone(timedelta(hours=8)))
        sender = "我" if row[4] == 2 else contact_name
        time_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"[{time_str}] {sender}：{content}")

    return "\n".join(lines)
```

### 群聊导出

```python
def export_group_chat(db_path, str_talker, name2id_map):
    """群聊导出：需要 Name2Id 映射 sender_id → 昵称"""
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT StrContent, CompressContent, CreateTime, Type, BytesExtra "
        "FROM MSG WHERE StrTalker=? ORDER BY CreateTime", (str_talker,)
    ).fetchall()

    lines = []
    for row in rows:
        if row[3] == 10000:  # 系统消息，跳过
            continue
        content = decompress_message(row[1], row[0])
        ts = datetime.fromtimestamp(row[2], tz=timezone(timedelta(hours=8)))
        sender = resolve_sender(row[4], name2id_map)  # 查映射表
        time_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"[{time_str}] {sender}：{content}")

    return "\n".join(lines)
```

### 输出格式

```markdown
# 聊天记录：{联系人/群名}

- 导出时间：YYYY-MM-DD HH:MM
- 消息总数：XXX 条
- 时间跨度：YYYY-MM-DD ~ YYYY-MM-DD

---

[2025-01-01 10:00:00] 我：你好
[2025-01-01 10:00:30] 对方：你好呀
[2025-01-01 10:01:00] 我：最近怎么样
```

---

## Phase 3: 质量验证

**导出后必须验证**：

1. **消息数量**：导出行数 vs DB 中查询行数，差异 < 1%
2. **发送者分布**：检查是否有异常的发送者（全部是"未知"说明映射失败）
3. **无二进制垃圾**：检查是否有不可打印字符（图片/视频的 XML 内容需过滤）
4. **UTF-8 编码**：用 `python -c "open(path, encoding='utf-8').read()"` 验证

**输出位置**：
- 私聊：`{out_dir}/{联系人备注或昵称}_chat.md`
- 群聊：`{out_dir}/{群名}_chat.md`

---

## 反模式

1. **不过滤系统消息**：Type=10000 的系统消息（拍一拍/撤回/入群）混在正常消息中
2. **不解压 zstd**：直接用 StrContent，部分消息为空（实际在 CompressContent 中）
3. **sender 映射硬编码**：不要假设 sender_id=2 一定是"我"，不同聊天可能不同
4. **不分页导出**：大群 10 万+消息，一次性加载会 OOM
5. **不验证导出结果**：导出后不检查文件完整性和编码
6. **保留 XML 标签**：图片/视频消息的 XML 标签不应出现在纯文本导出中
