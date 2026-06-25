# Sender ID 映射规则

> 来源：实测 Camellia 和米蛋糕聊天记录（2026-06-07）

## 私聊 Sender 映射

**规则**：私聊中 `Status` 字段区分发送方。

| Status | 含义 | 映射 |
|--------|------|------|
| 2 | 我发出的消息 | → "我" |
| 3 | 对方发出的消息 | → 对方昵称/备注 |

**注意**：这是最可靠的私聊发送者判断方式，不需要查额外表。

## 群聊 Sender 映射

**规则**：群聊中 sender 信息存储在 `BytesExtra` 字段或 `Name2Id` 表中。

### 方法 1：BytesExtra 解析

```python
import struct

def extract_sender_id(bytes_extra):
    """从 BytesExtra 提取 sender_id"""
    if not bytes_extra:
        return None
    # BytesExtra 是 protobuf 格式，sender_id 在 field 2
    # 简化解析：查找 wxid 模式
    text = bytes_extra.decode('latin-1')
    import re
    match = re.search(r'(wxid_[a-z0-9]+)', text)
    return match.group(1) if match else None
```

### 方法 2：Name2Id 表

如果 `contact.db` 中有 `Name2Id` 表：
```sql
SELECT * FROM Name2Id WHERE Name='群聊wxid@chatroom'
```

## 已验证的 Sender 映射

### Camellia 私聊

| sender_id | 身份 | 验证方式 |
|-----------|------|---------|
| 2 | 我（小黎） | Status=2 |
| 6 | Camellia | Status=3，与 StrTalker 对应 |
| 7 | 系统消息 | Type=10000 |

### 米蛋糕私聊

| sender_id | 身份 | 验证方式 |
|-----------|------|---------|
| 2 | 我（小黎） | Status=2 |
| 3026 | 米蛋糕 | Status=3，与 StrTalker 对应 |

### 群聊通用

| sender_id | 身份 | 验证方式 |
|-----------|------|---------|
| 0 | 系统消息 | Type=10000 |
| wxid_xxx | 群成员 | 需查 contact.db 或 Name2Id |

## 踩坑警告

1. **sender_id 不是全局唯一的**：不同聊天中 sender_id=2 可能代表不同的人
2. **不要假设 sender_id 的数值规律**：Camellia 是 6，米蛋糕是 3026，没有规律
3. **群聊 sender_id 可能是 wxid 字符串**：不是数字，需要查 contact.db 获取昵称
4. **系统消息的 sender_id 可能是 0、7 或其他值**：以 Type=10000 为准
5. **BytesExtra 可能为空**：老版本微信或部分消息没有 sender 信息

## 映射流程

```
收到消息
  ├── 私聊（无 @chatroom）→ Status=2 是我，Status=3 是对方
  ├── 群聊（有 @chatroom）
  │   ├── Type=10000 → 系统消息，跳过
  │   ├── BytesExtra 有内容 → 提取 sender_id → 查 contact.db
  │   └── BytesExtra 为空 → 用 Des 字段（0=我，1=他人）
  └── 无法确定 → 标记为 "未知"
```
