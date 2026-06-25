#!/usr/bin/env python3
"""
打包微信聊天记录读取工具包 v2.0
- 精选6个核心脚本
- 去除硬编码个人信息，参数化路径
- 生成 README 和打包 zip
"""

import os, shutil, re, zipfile

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(WORK_DIR, '_toolkit_build')
OUTPUT_ZIP = os.path.join(WORK_DIR, 'wechat-reader-toolkit-v2.0.zip')

# 源文件路径映射
SOURCES = {
    'extract_full_data.py': os.path.join(WORK_DIR, 'extract_full_data.py'),
    'analyze_voice_dna.py': os.path.join(WORK_DIR, 'analyze_voice_dna.py'),
    'export_chat.py': os.path.join(WORK_DIR, '..', '..', '..', 'outputs', '_export_chat_v8.py'),
    'analyze_wechat.py': os.path.join(WORK_DIR, '..', '..', '..', 'outputs', 'wechat-reproducible-kit', 'scripts', 'analyze_wechat.py'),
    'extract_red_envelopes.py': os.path.join(WORK_DIR, 'extract_red_envelopes.py'),
    'extract_transfer_amounts.py': os.path.join(WORK_DIR, 'extract_transfer_amounts.py'),
}

README_CONTENT = """# 微信聊天记录读取工具包 v2.0

## 简介

一套完整的微信聊天记录提取与分析工具链。从已解密的微信数据库中提取聊天记录、联系人信息、转账红包记录，并进行文风分析。

## 环境要求

- **Python 3.8+**（推荐 3.10+）
- **已解密的微信数据库文件**（message_0.db, contact.db, general.db, session.db）

### 安装依赖

```bash
pip install zstandard
```

## 文件说明

| 脚本 | 功能 | 核心输出 |
|------|------|---------|
| `extract_full_data.py` | 全量数据提取（聊天+联系人+群成员） | corpus.json, all_sessions.json 等 |
| `export_chat.py` | 单个联系人/群聊记录导出为 Markdown | chat_xxx.md |
| `analyze_wechat.py` | 聊天分类汇总+统计报告 | MD + JSON 报告 |
| `analyze_voice_dna.py` | 文风DNA蒸馏（私聊vs群聊风格对比） | 文风分析报告 |
| `extract_red_envelopes.py` | 红包记录提取（含金额） | red_envelopes.json |
| `extract_transfer_amounts.py` | 转账记录提取（含金额） | transfers.json |

## 快速开始

### Step 1: 获取解密后的数据库

你需要先解密微信数据库。推荐工具：
- **PyWxDump**: `pip install pywxdump` → `pywxdump bias_addr` → `pywxdump decrypt`
- **wx_key**: `pip install wx_key`（需微信正在运行）

解密后你会得到以下文件（通常在同一个目录下）：
```
message_0.db    # 聊天记录（最大，几百MB）
contact.db      # 联系人信息
general.db      # 转账/红包/收藏等
session.db      # 会话列表
```

### Step 2: 全量提取

```bash
python extract_full_data.py --db-dir "你的数据库目录" --output "输出目录"
```

输出文件：
- `all_sessions.json` — 所有会话统计
- `top_private.json` — 私聊排行 Top 20
- `top_groups.json` — 群聊排行 Top 20
- `corpus.json` — 全量消息语料
- `transfers.json` — 转账记录
- `group_members.json` — 群成员列表
- `data_summary.md` — Markdown 报告

### Step 3: 导出特定聊天

```bash
python export_chat.py --db "消息数据库路径/message_0.db" --contact-db "联系人数据库路径/contact.db" --target "张三" --output "chat_张三.md"
```

支持导出私聊和群聊，自动解析联系人名称和群成员昵称。

### Step 4: 生成分析报告

```bash
python analyze_wechat.py --db-dir "数据库目录" --out-dir "输出目录"
```

生成分类汇总报告，自动按"学习/AI/竞赛/生活"等类别归类消息。

### Step 5: 文风分析

```bash
python analyze_voice_dna.py --corpus "输出目录/corpus.json" --output "文风报告.txt"
```

对比你的私聊和群聊用语差异：消息长度、标点使用、高频词等。

### Step 6: 提取红包和转账

```bash
python extract_red_envelopes.py --db-dir "数据库目录" --output "red_envelopes.json"
python extract_transfer_amounts.py --db-dir "数据库目录" --output "transfers.json"
```

## 数据库 Schema 说明

微信 4.0 使用 WCDB（自定义 AES-CBC 加密 SQLite），解密后的关键表：

### message_0.db
- **表名**: `Msg_00` ~ `Msg_xx`（按 hash 分表，需遍历）
- **关键列**: `local_id`, `create_time`(Unix时间戳), `real_sender_id`, `message_content`, `compress_content`(zstd压缩), `status`, `local_type`(10000=系统消息)
- **sender_id=2 永远是数据库主人**
- **群聊消息内容**: 格式为 `sender_wxid:\\n消息内容`

### contact.db
- **contact 表**: `username`, `nick_name`, `remark`, `alias`
- **chatroom_member 表**: `room_id`, `member_id`
- **chat_room 表**: `id`, `username`, `owner`

### general.db
- **transferTable**: 转账记录
- **redEnvelopeTable**: 红包记录

### session.db
- **session 表**: 会话列表（username + 最新消息时间）

## 常见问题

### Q: zstandard 安装失败？
```bash
pip install zstandard --only-binary=:all:
```

### Q: 数据库是加密的怎么办？
本工具只处理**已解密**的数据库。解密步骤请参考 PyWxDump 或 wx_key 文档。

### Q: 不知道数据库在哪里？
微信 4.0 默认路径: `D:\\data\\wechat\\xwechat_files\\wxid_xxx\\db_storage\\message\\message_0.db`
或: `%LOCALAPPDATA%\\Packages\\...\\LocalCache\\Roaming\\Tencent\\WeChat\\...`

### Q: 消息内容是乱码/bytes？
微信 4.0 的 message_content 可能是 zstd 压缩的。脚本已内置解压，确保安装了 zstandard。

### Q: 群聊消息只有 wxid 没有名字？
需要同时读取 contact.db 的 chatroom_member 表。`extract_full_data.py` 会自动处理。

## 技术细节

- **加密算法**: PBKDF2-HMAC-SHA1, 64000 迭代, 32 字节密钥, 4096 页大小
- **压缩**: zstd（magic bytes: `\\x28\\xb5\\x2f\\xfd`）
- **分表**: 消息按 `Msg_md5_hash % N` 分到多个表
- **时间戳**: Unix timestamp（秒）

## 免责声明

本工具仅供个人数据分析使用。请遵守当地法律法规，尊重他人隐私。
"""

def patch_extract_full_data(content):
    """参数化 extract_full_data.py"""
    # 替换硬编码配置块
    old_config = '''# ====== 配置 ======
DB_DIR = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\databases\\wxid_3nvidmluot0a22'
OUTPUT_DIR = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\wechat_analysis'
YOUR_WXID = 'wxid_3nvidmluot0a22\''''

    new_config = '''# ====== 配置（通过命令行参数传入） ======
import argparse
_parser = argparse.ArgumentParser(description='全量微信数据提取 v2.0')
_parser.add_argument('--db-dir', required=True, help='解密后的数据库目录（含 message_0.db, contact.db 等）')
_parser.add_argument('--output', required=True, help='输出目录')
_parser.add_argument('--wxid', default=None, help='你的微信 wxid（可选，用于识别自己发的消息）')
_args = _parser.parse_args()
DB_DIR = _args.db_dir
OUTPUT_DIR = _args.output
YOUR_WXID = _args.wxid or 'unknown\''''

    content = content.replace(old_config, new_config)
    return content


def patch_analyze_voice_dna(content):
    """参数化 analyze_voice_dna.py"""
    old_config = '''CORPUS_PATH = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\wechat_analysis\\corpus.json'
SESSIONS_PATH = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\wechat_analysis\\top_private.json\''''

    new_config = '''import argparse
_parser = argparse.ArgumentParser(description='文风DNA蒸馏分析')
_parser.add_argument('--corpus', required=True, help='corpus.json 文件路径')
_parser.add_argument('--sessions', default=None, help='top_private.json 文件路径（可选）')
_parser.add_argument('--output', default=None, help='输出文件路径（可选，默认打印到终端）')
_args = _parser.parse_args()
CORPUS_PATH = _args.corpus
SESSIONS_PATH = _args.sessions or CORPUS_PATH.replace('corpus.json', 'top_private.json')'''

    content = content.replace(old_config, new_config)
    return content


def patch_export_chat(content):
    """参数化 export_chat.py (v8)"""
    # 替换硬编码路径和联系人
    old_db = '''DB_PATH = r'C:\\Users\\13975\\AppData\\Local\\Temp\\wechat-decrypted-wxid_3nvidmluot0a22\\message_0.db'
TARGET_DIR = r'E:\\ai产出文件\\牛马\\个人\\个人\\projects\\20260425-成长历程\\成长历程\\交往'
os.makedirs(TARGET_DIR, exist_ok=True)'''

    new_db = '''import argparse
_parser = argparse.ArgumentParser(description='微信聊天记录导出工具 v8')
_parser.add_argument('--db', required=True, help='解密后的 message_0.db 路径')
_parser.add_argument('--contact-db', default=None, help='contact.db 路径（用于解析联系人名称）')
_parser.add_argument('--target', required=True, help='导出目标：联系人 wxid 或群聊 ID（xxx@chatroom）')
_parser.add_argument('--target-name', default=None, help='目标显示名（可选，默认从 contact.db 查询）')
_parser.add_argument('--output', required=True, help='输出 Markdown 文件路径')
_parser.add_argument('--sender-map', default=None, help='发送者映射 JSON（可选，格式: {"2":"我","对方wxid":"名字"}）')
_args = _parser.parse_args()
DB_PATH = _args.db
TARGET_DIR = os.path.dirname(_args.output) or '.'
os.makedirs(TARGET_DIR, exist_ok=True)'''

    content = content.replace(old_db, new_db)

    # 替换硬编码的 PRIVATE_CHATS 和 GROUP_CHATS
    old_chats = '''PRIVATE_CHATS = {
    'wxid_bfgr9dxq2o6m22': {'display': 'Camellia', 'senders': {'2': '小黎', '6': 'Camellia', '7': '[系统]'}},
    'wxid_4afm4lnos29o12': {'display': '米蛋糕（陈雅婷）', 'senders': {'2': '小黎', '3026': '陈雅婷', '3': '[系统]'}},
    'wxid_iaeun6rhbyb532': {'display': '少年Lee（OPC合伙人）', 'senders': {'2': '小黎', None: '少年Lee'}},
}

GROUP_CHATS = {
    '50267796386@chatroom': '青柠同频轻创圈',
    '56820316831@chatroom': '破界青年OPC会员',
    '45375846863@chatroom': 'OPC启动计划1.0',
    '49472124843@chatroom': '破界向上生长基地六群',
    '56989512808@chatroom': '牛马AI灰度测试群',
}'''

    new_chats = '''# 从命令行参数构建目标列表
PRIVATE_CHATS = {}
GROUP_CHATS = {}

def _load_sender_map():
    if _args.sender_map:
        import json as _json
        return _json.loads(_args.sender_map)
    return {'2': '我'}

_target_id = _args.target
_target_name = _args.target_name or _target_id

if '@chatroom' in _target_id:
    GROUP_CHATS[_target_id] = _target_name
else:
    PRIVATE_CHATS[_target_id] = {
        'display': _target_name,
        'senders': _load_sender_map()
    }'''

    content = content.replace(old_chats, new_chats)
    return content


def patch_extract_red_envelopes(content):
    """参数化 extract_red_envelopes.py"""
    # 替换头部配置
    old_head = '''MY_WXID = 'wxid_3nvidmluot0a22'
OUTPUT_DIR = r'E:\\ai产出文件\\牛马\\mutual\\mutual\\projects\\proj-1779089173658-j5tg2m\\outputs'

# 1. Contact name map
contact_db = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\databases\\wxid_3nvidmluot0a22\\contact.db\''''

    new_head = '''import argparse
_parser = argparse.ArgumentParser(description='微信红包金额提取')
_parser.add_argument('--db-dir', required=True, help='解密后的数据库目录')
_parser.add_argument('--output', default='red_envelopes.json', help='输出 JSON 文件路径')
_args = _parser.parse_args()

MY_WXID = 'unknown'
OUTPUT_DIR = os.path.dirname(_args.output) or '.'

# 1. Contact name map
contact_db = os.path.join(_args.db_dir, 'contact.db')'''

    content = content.replace(old_head, new_head)

    # 替换 general.db 和 message_0.db 路径
    content = content.replace(
        "gen_db = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\databases\\wxid_3nvidmluot0a22\\general.db'",
        "gen_db = os.path.join(_args.db_dir, 'general.db')"
    )
    content = content.replace(
        "msg_db = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\databases\\wxid_3nvidmluot0a22\\message_0.db'",
        "msg_db = os.path.join(_args.db_dir, 'message_0.db')"
    )
    return content


def patch_extract_transfer_amounts(content):
    """参数化 extract_transfer_amounts.py"""
    old_head = '''MY_WXID = 'wxid_3nvidmluot0a22'
OUTPUT_DIR = r'E:\\ai产出文件\\牛马\\mutual\\mutual\\projects\\proj-1779089173658-j5tg2m\\outputs'

# 1. Get contact name map
contact_db = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\databases\\wxid_3nvidmluot0a22\\contact.db\''''

    new_head = '''import argparse
_parser = argparse.ArgumentParser(description='微信转账金额提取')
_parser.add_argument('--db-dir', required=True, help='解密后的数据库目录')
_parser.add_argument('--output', default='transfers.json', help='输出 JSON 文件路径')
_args = _parser.parse_args()

MY_WXID = 'unknown'
OUTPUT_DIR = os.path.dirname(_args.output) or '.'

# 1. Get contact name map
contact_db = os.path.join(_args.db_dir, 'contact.db')'''

    content = content.replace(old_head, new_head)

    content = content.replace(
        "gen_db = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\databases\\wxid_3nvidmluot0a22\\general.db'",
        "gen_db = os.path.join(_args.db_dir, 'general.db')"
    )
    content = content.replace(
        "msg_db = r'E:\\ai产出文件\\牛马\\创作\\创作\\output\\databases\\wxid_3nvidmluot0a22\\message_0.db'",
        "msg_db = os.path.join(_args.db_dir, 'message_0.db')"
    )
    return content


def build():
    # 清理并创建临时目录
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    patches = {
        'extract_full_data.py': patch_extract_full_data,
        'analyze_voice_dna.py': patch_analyze_voice_dna,
        'export_chat.py': patch_export_chat,
        'extract_red_envelopes.py': patch_extract_red_envelopes,
        'extract_transfer_amounts.py': patch_extract_transfer_amounts,
    }

    for name, src_path in SOURCES.items():
        if not os.path.exists(src_path):
            print(f'[WARN] 源文件不存在: {src_path}')
            continue

        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 应用补丁
        if name in patches:
            content = patches[name](content)
            print(f'[PATCHED] {name}')

        # 写入临时目录
        dst_path = os.path.join(TEMP_DIR, name)
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'[COPY] {name} -> {dst_path}')

    # 写 README
    readme_path = os.path.join(TEMP_DIR, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(README_CONTENT)
    print(f'[WRITE] README.md')

    # 打 zip
    if os.path.exists(OUTPUT_ZIP):
        os.remove(OUTPUT_ZIP)

    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.join('wechat-reader-toolkit', file)
                zf.write(file_path, arc_name)
                print(f'[ZIP] {arc_name}')

    fcount = len([f for f in os.listdir(TEMP_DIR)])
    fsize = os.path.getsize(OUTPUT_ZIP) / 1024
    print(f'\n[OK] Done: {OUTPUT_ZIP}')
    print(f'   Files: {fcount}')
    print(f'   Size: {fsize:.1f} KB')

    # 清理临时目录
    shutil.rmtree(TEMP_DIR)
    print('[OK] Temp dir cleaned')


if __name__ == '__main__':
    build()
