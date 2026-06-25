# Sender 映射实操指南

> 从 DB 字段到聊天记录中的"发言人姓名"

## 私聊映射（最简单）

**规则**：Status 字段直接区分。

```python
def get_private_sender(status, contact_name):
    if status == 2:
        return "我"
    elif status == 3:
        return contact_name
    else:
        return f"系统({status})"
```

**已验证数据**：
- Camellia 私聊：Status=2 → 我，Status=3 → Camellia
- 米蛋糕私聊：Status=2 → 我，Status=3 → 米蛋糕

## 群聊映射（需要额外信息）

### 方法 1：BytesExtra 提取 wxid

```python
import re

def extract_wxid_from_bytes_extra(bytes_extra):
    if not bytes_extra:
        return None
    try:
        text = bytes_extra.decode('latin-1')
        match = re.search(r'(wxid_[a-z0-9]+)', text)
        if match:
            return match.group(1)
    except:
        pass
    return None
```

### 方法 2：contact.db 查昵称

```python
def wxid_to_nickname(contact_db_path, wxid):
    conn = sqlite3.connect(contact_db_path)
    row = conn.execute(
        "SELECT NickName, Remark FROM contact WHERE UserName=?", (wxid,)
    ).fetchone()
    if row:
        return row[1] or row[0]  # 优先用备注
    return wxid
```

### 方法 3：Name2Id 表（如果存在）

```python
def resolve_from_name2id(contact_db_path, chatroom_id, sender_id):
    conn = sqlite3.connect(contact_db_path)
    # Name2Id 表结构因版本而异，先查表是否存在
    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()]
    if 'Name2Id' in tables:
        row = conn.execute(
            "SELECT * FROM Name2Id WHERE Name=?", (chatroom_id,)
        ).fetchone()
        # 解析 protobuf 获取 sender_id → wxid 映射
    return None
```

## 完整映射流程

```python
def resolve_sender(row, contact_db_path, chat_type, contact_name=None):
    """
    row: (StrContent, CompressContent, CreateTime, Type, Status, BytesExtra)
    chat_type: 'private' | 'group'
    """
    str_content, compress_content, create_time, msg_type, status, bytes_extra = row

    # 系统消息
    if msg_type == 10000:
        return "系统消息"

    # 私聊
    if chat_type == 'private':
        return "我" if status == 2 else (contact_name or "对方")

    # 群聊
    wxid = extract_wxid_from_bytes_extra(bytes_extra)
    if wxid:
        return wxid_to_nickname(contact_db_path, wxid)

    # 回退：用 Des 字段
    return "我" if status == 0 else "群成员"
```

## 常见问题

**Q: 为什么导出的聊天记录中全是"未知"？**
A: BytesExtra 为空或解析失败。检查是否用了正确的解密后的 DB。

**Q: 群聊中"我"的消息怎么识别？**
A: 优先用 BytesExtra 提取 wxid 后与自己的 wxid 比对。回退方案：Des=0 或 Status=0。

**Q: 不同群的 sender_id 会重复吗？**
A: 会。sender_id 只在单个聊天内唯一，跨聊天无意义。
