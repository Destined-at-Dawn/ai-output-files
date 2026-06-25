# 微信数据库结构速查

## 数据库文件清单

| 文件 | 用途 | 关键表 |
|------|------|--------|
| message_0.db ~ message_9.db | 聊天消息（按 wxid hash 分片） | Msg_{md5(wxid)} |
| message.db | 补充消息 | 同上 |
| contact.db | 联系人信息 | contact（UserName/NickName/Remark） |
| bizchat.db | 企业微信消息 | biz_msg / biz_chat |
| emoticon.db | 表情包 | emoticon |
| hardlink.db | 媒体文件映射（hash→路径） | hardlink |
| media_0.db | 媒体元数据 | media |
| message_resource.db | 消息资源（图片/文件） | resource |
| Name2Id.db | 发送者 ID 映射 | Name2Id |
| session.db | 会话列表 | session |

## 消息类型码

| Type | 含义 |
|------|------|
| 1 | 文本消息 |
| 3 | 图片消息 |
| 34 | 语音消息 |
| 42 | 名片消息 |
| 43 | 视频消息 |
| 47 | 表情消息 |
| 48 | 位置消息 |
| 49 | 链接/文件/公众号文章 |
| 10000 | 系统消息（拍一拍/撤回/入群） |
| 10002 | 系统消息（红包/转账） |

## zstd 压缩检测

```python
def is_zstd_compressed(data: bytes) -> bool:
    """检查是否为 zstd 压缩数据"""
    return len(data) >= 4 and data[:4] == b'\x28\xb5\x2f\xfd'

def decompress_zstd(data: bytes) -> bytes:
    """解压 zstd 数据"""
    import zstandard
    ctx = zstandard.ZstdDecompressor()
    return ctx.decompress(data, max_output_size=10 * 1024 * 1024)
```

## Sender 映射策略

### 私聊
- `Status=2` → 小黎发送
- `Status=3` → 对方发送

### 群聊
- 从消息内容前缀 `{wxid}:{content}` 提取发送者 wxid
- 或从 `BytesExtra` protobuf 字段解析 `real_sender_id`
- 用 `contact.db` 的 `NickName` 映射 wxid → 真名

## 表名计算

```python
import hashlib
def get_msg_table_name(wxid: str) -> str:
    return 'Msg_' + hashlib.md5(wxid.encode()).hexdigest()
```
