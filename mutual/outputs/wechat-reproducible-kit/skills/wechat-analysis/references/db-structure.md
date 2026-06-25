# 微信数据库结构速查

> 来源：实测 16 个解密后的 DB 文件（2026-06-07）

## DB 文件清单

| 文件 | 大小 | 内容 |
|------|------|------|
| `message_0.db` ~ `message_9.db` | 各 ~50MB | 聊天消息（按会话哈希分片） |
| `message.db` | ~10MB | 部分聊天消息（补充分片） |
| `contact.db` | ~5MB | 联系人信息（wxid → 昵称/备注/头像） |
| `message_resource.db` | ~20MB | 消息资源索引（图片/视频/文件 hash → 路径） |
| `hardlink.db` | ~1.3MB | 文件 hash → 物理路径映射 |
| `group_member.db` | ~2MB | 群成员关系 |
| `session.db` | ~1MB | 会话列表（最近聊天排序） |
| `fts_message*.db` | 各 ~5MB | 全文搜索索引 |
| `revoke.db` | <1MB | 已撤回消息记录 |
| `emotion.db` | <1MB | 表情包索引 |
| `favorites.db` | <1MB | 收藏内容 |
| `media.db` | <1MB | 媒体文件索引 |
| `sns.db` | <1MB | 朋友圈数据 |
| `profile.db` | <1MB | 用户资料 |
| `function.db` | <1MB | 功能配置 |

## MSG 表核心字段

```sql
CREATE TABLE MSG (
    localId INTEGER PRIMARY KEY,    -- 本地自增 ID
    MsgSvrID INTEGER,               -- 服务器消息 ID（全局唯一）
    StrTalker TEXT,                  -- 会话标识（wxid 或 wxid@chatroom）
    StrContent TEXT,                 -- 消息内容（可能 zstd 压缩）
    CreateTime INTEGER,             -- Unix 时间戳（秒）
    Type INTEGER,                   -- 消息类型码
    Status INTEGER,                 -- 状态码（私聊中区分发送方）
    Des INTEGER,                    -- 方向（0=发出, 1=收到）
    ImgStatus INTEGER,              -- 图片状态
    Sequence INTEGER,               -- 消息序号
    BytesExtra BLOB,                -- 扩展数据（含 sender_id 等）
    CompressContent BLOB,           -- zstd 压缩内容
    StrTrans TEXT                   -- 翻译文本
);
```

## 消息类型码

| Type | 含义 | StrContent 格式 |
|------|------|----------------|
| 1 | 文本消息 | 纯文本 |
| 3 | 图片消息 | XML（含图片路径/尺寸） |
| 34 | 语音消息 | XML（含语音时长） |
| 42 | 名片消息 | XML（含昵称/头像） |
| 43 | 视频消息 | XML（含视频路径/封面） |
| 47 | 表情消息 | XML（含表情 MD5） |
| 48 | 位置消息 | XML（含经纬度/地址） |
| 49 | 链接/文件/小程序 | XML（含标题/描述/URL） |
| 50 | 语音/视频通话 | XML |
| 10000 | 系统消息 | 纯文本（撤回/拍一拍/入群等） |
| 10002 | 系统消息（富文本） | XML |

## zstd 压缩

**触发条件**：新版微信（8.0+）对长文本和部分消息启用 zstd 压缩。

**识别方法**：
```python
# 检查 CompressContent 字段的 magic bytes
data = row['CompressContent']
if data and data[:4] == b'\x28\xb5\x2f\xfd':
    import zstandard as zstd
    decompressor = zstd.ZstdDecompressor()
    content = decompressor.decompress(data).decode('utf-8')
```

**解压代码**：
```python
import zstandard as zstd

def decompress_message(compress_content, str_content):
    """优先用 CompressContent，回退到 StrContent"""
    if compress_content:
        try:
            if compress_content[:4] == b'\x28\xb5\x2f\xfd':
                dctx = zstd.ZstdDecompressor()
                return dctx.decompress(compress_content).decode('utf-8')
        except Exception:
            pass
    return str_content or ''
```

## 注意事项

- `StrTalker` 格式：私聊为 `wxid_xxxxx`，群聊为 `wxid_xxxxx@chatroom`
- `CreateTime` 是 Unix 时间戳（秒），转北京时间需 +8 小时
- 部分消息的 `StrContent` 为空，内容在 `CompressContent` 中
- `message_0.db` ~ `message_9.db` 的分片规则基于会话 hash，不是时间顺序
