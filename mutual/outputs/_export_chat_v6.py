"""
v6: 精确导出聊天记录到个人区交往目录
目标：每条消息格式 "[日期 时间] 发言人：消息内容"
处理：zstd解压、群聊成员名解析、clean text提取
"""
import sqlite3
import json
import re
import os
import sys
import zstandard as zstd

DB_PATH = r'C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22\message_0.db'
CONTACT_PATH = r'C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22\contact.db'

TARGET_DIR = r'E:\ai产出文件\牛马\个人\个人\projects\20260425-成长历程\成长历程\交往'
os.makedirs(TARGET_DIR, exist_ok=True)

# ========== 配置 ==========
# 私聊 (username -> (display_name, [sender_map]))
PRIVATE_CHATS = {
    'wxid_bfgr9dxq2o6m22': {
        'display': 'Camellia',
        'senders': {
            '2': '小黎',
            '6': 'Camellia',
            '7': '[系统]',
        }
    },
    'wxid_4afm4lnos29o12': {
        'display': '米蛋糕（陈雅婷）',
        'senders': {
            '2': '小黎',
            '3026': '陈雅婷',
            '3': '[系统]',
        }
    },
}

# 群聊
GROUP_CHATS = {
    '50267796386@chatroom': '🍋青柠丨同频轻创圈',
    '56820316831@chatroom': '破界青年OPC会员',
    '45375846863@chatroom': 'OPC启动计划1.0',
    '49472124843@chatroom': '破界向上生长基地六群',
    '56989512808@chatroom': '牛马AI灰度测试群',
}

# Also add key OPC individuals as private chats
OPC_INDIVIDUALS = {
    'wxid_iaeun6rhbyb532': {
        'display': '少年Lee（OPC合伙人）',
        'senders': {'2': '小黎', None: '少年Lee'},
    },
}

# 需要合并上面
PRIVATE_CHATS.update(OPC_INDIVIDUALS)

# ========== 工具函数 ==========
dctx = zstd.ZstdDecompressor()

def decompress_zstd(blob):
    """解压zstd压缩的blob"""
    if blob is None:
        return None
    try:
        return dctx.decompress(blob).decode('utf-8', errors='replace')
    except:
        return None

def clean_xml_content(xml_str, msg_type):
    """从微信消息XML中提取纯文本"""
    if not xml_str:
        return ''

    text = xml_str

    # 图片消息: <img .*/> or <msg><img .../></msg>
    if msg_type in (3, 47):
        # 图片
        md5_match = re.search(r'md5="([^"]+)"', text)
        cdn_match = re.search(r'cdnattachurl="([^"]+)"', text)
        aes_match = re.search(r'aeskey="([^"]+)"', text)
        # Also try <img> without quotes
        if not md5_match:
            md5_match = re.search(r'md5=([a-f0-9]+)', text, re.IGNORECASE)

        parts = ['[图片]']
        if md5_match:
            parts.append(f'MD5:{md5_match.group(1)}')
        if aes_match:
            parts.append(f'AES:{aes_match.group(1)[:16]}...')
        if cdn_match:
            cdn = cdn_match.group(1)
            # Extract filename from CDN URL if possible
            fn_match = re.search(r'[?&]filename=([^&]+)', cdn)
            if fn_match:
                parts.append(f'文件:{fn_match.group(1)}')
        return ' '.join(parts)

    # 视频
    if msg_type == 43:
        md5 = re.search(r'md5="([^"]+)"', text)
        return f'[视频] MD5:{md5.group(1)}' if md5 else '[视频]'

    # 文件
    if msg_type == 49:
        title = re.search(r'<title>(.*?)</title>', text, re.DOTALL)
        # AppMsg - shared links, files, etc
        appmsg_type = re.search(r'<type>(\d+)</type>', text)
        fn_match = re.search(r'<title>(.*?)</title>', text, re.DOTALL)
        if fn_match:
            title_text = fn_match.group(1).strip()
            return f'[文件/链接] {title_text}'
        return '[文件/链接]'

    # 语音
    if msg_type == 34:
        return '[语音]'

    # 表情
    if msg_type == 47:
        emoji_md5 = re.search(r'md5="([^"]+)"', text)
        return f'[表情]' if not emoji_md5 else f'[表情 {emoji_md5.group(1)[:8]}]'

    # 系统消息
    if msg_type == 10000:
        sys_content = re.search(r'<sysmsgtemplate.*?<content_template.*?>(.*?)</content_template>', text, re.DOTALL)
        if sys_content:
            return f'[系统] {sys_content.group(1).strip()}'
        return '[系统消息]'

    # 红包
    if msg_type == 436207665:
        return '[红包]'

    # 位置
    if msg_type == 48:
        loc = re.search(r'label="([^"]+)"', text)
        return f'[位置] {loc.group(1)}' if loc else '[位置]'

    # 引用回复
    if msg_type == 57:
        return '[引用回复]'

    # 其他类型 - 尝试提取文本
    content = re.search(r'<title>(.*?)</title>', text, re.DOTALL)
    if content:
        return content.group(1).strip()

    desc = re.search(r'<des>(.*?)</des>', text, re.DOTALL)
    if desc:
        return desc.group(1).strip()

    # 纯文本XML - 去掉CDATA标签
    if text.startswith('<msg>') or text.startswith('<?xml'):
        cdata = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
        if cdata:
            return ' '.join(cdata).strip()

    return f'[{msg_type}]'

def extract_text_content(msg_type, content, compressed_content, is_compressed):
    """提取消息文本内容"""
    if is_compressed and compressed_content:
        decompressed = decompress_zstd(compressed_content)
        if decompressed:
            return clean_xml_content(decompressed, msg_type)

    if content:
        return clean_xml_content(content, msg_type)

    return ''

def get_sender_name(talker, status, msg_content):
    """获取群聊中的发送者名称"""
    # 从XML中提取发言者微信ID
    if not msg_content:
        return f'wxid_unknown'

    # 从sender XML中提取
    sender_match = re.search(r'<atuserlist>.*?<username><!\[CDATA\[(.*?)\]\]>', msg_content)
    if not sender_match:
        sender_match = re.search(r'<username><!\[CDATA\[(.*?)\]\]>', msg_content)

    if sender_match:
        return sender_match.group(1)

    # 从msg XML里也可能有
    if isinstance(msg_content, bytes):
        try:
            msg_content = msg_content.decode('utf-8', errors='replace')
        except:
            pass

    if isinstance(msg_content, str) and '<?xml' in msg_content:
        sender_match = re.search(r'<username><!\[CDATA\[(.*?)\]\]>', msg_content)
        if sender_match:
            return sender_match.group(1)

    # fallback: use talker with status
    return f'{talker.replace("@chatroom", "")}'

# ========== 主导出逻辑 ==========

def export_private_chat(db, username, config):
    """导出私聊"""
    display_name = config['display']
    sender_map = config['senders']
    output_file = os.path.join(TARGET_DIR, f'chat_{display_name}.md')

    print(f'导出私聊: {display_name} ({username})')

    cur = db.execute('''
        SELECT
            CreateTime,
            Type,
            SubType,
            IsSender,
            StrContent,
            CompressContent,
            StrTalker
        FROM Msg_b35297daf9c0eccd6a495ff3cb4f63ec
        WHERE StrTalker = ?
        ORDER BY CreateTime ASC
    ''', (username,))

    rows = cur.fetchall()
    print(f'  共 {len(rows)} 条消息')

    lines = []
    lines.append(f'# {display_name} 聊天记录\n')
    lines.append(f'**对象**: {display_name}（{username}）')
    lines.append(f'**消息总数**: {len(rows)}')
    lines.append(f'**导出时间**: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
    lines.append('---\n')

    last_date = ''
    msg_count = 0

    for row in rows:
        create_time, msg_type, sub_type, is_sender, content, compressed, talker = row
        is_compressed = (sub_type == 5) or (msg_type == 1 and compressed and len(compressed) > 10)

        # 时间
        dt = __import__('datetime').datetime.fromtimestamp(create_time)
        date_str = dt.strftime('%Y-%m-%d')
        time_str = dt.strftime('%H:%M:%S')

        # 发送者
        sender = str(is_sender) if str(is_sender) in sender_map else None
        if sender is None:
            # Try to infer from content
            sender = sender_map.get(str(is_sender), f'[user_{is_sender}]')
        else:
            sender = sender_map.get(str(is_sender), f'[user_{is_sender}]')

        # 提取文本
        text = extract_text_content(msg_type, content, compressed, is_compressed)

        # 跳过空消息和系统消息（除了明确有用的）
        if not text or text.strip() == '':
            continue

        # 恢复消息
        if 'revokemsg' in str(content).lower():
            text = '[消息已撤回]'

        # 格式化输出
        if date_str != last_date:
            if last_date != '':
                lines.append('')  # 空行分隔日期
            lines.append(f'## {date_str}\n')
            last_date = date_str

        lines.append(f'**[{time_str}] {sender}**：{text}')
        msg_count += 1

    lines.append(f'\n---\n*共 {msg_count} 条有效消息*')

    content_str = '\n'.join(lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content_str)

    file_size = os.path.getsize(output_file)
    print(f'  -> {output_file} ({file_size/1024:.1f} KB, {msg_count} 条)')
    return output_file, msg_count

def export_group_chat(db, username, display_name):
    """导出群聊"""
    output_file = os.path.join(TARGET_DIR, f'group_{display_name}.md')

    print(f'导出群聊: {display_name} ({username})')

    cur = db.execute('''
        SELECT
            CreateTime,
            Type,
            SubType,
            IsSender,
            StrContent,
            CompressContent,
            StrTalker
        FROM Msg_b35297daf9c0eccd6a495ff3cb4f63ec
        WHERE StrTalker = ?
        ORDER BY CreateTime ASC
    ''', (username,))

    rows = cur.fetchall()
    print(f'  共 {len(rows)} 条消息')

    # 先建立群成员名映射
    member_map = {}
    for row in rows:
        _, msg_type, _, is_sender, content, compressed, _ = row
        raw = decompress_zstd(compressed) if compressed else content
        if raw:
            sender_from_msg = get_sender_name(None, None, raw)
            if sender_from_msg and not sender_from_msg.endswith('@chatroom'):
                member_map[str(is_sender)] = sender_from_msg

    lines = []
    lines.append(f'# {display_name} 群聊记录\n')
    lines.append(f'**群聊**: {display_name}（{username}）')
    lines.append(f'**消息总数**: {len(rows)}')
    lines.append(f'**导出时间**: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")}')
    lines.append(f'**群成员**: {len(member_map)} 人识别\n')

    if member_map:
        lines.append('## 群成员名单\n')
        for sid, sname in sorted(member_map.items()):
            lines.append(f'- {sname} (ID:{sid})')
        lines.append('')

    lines.append('---\n')

    last_date = ''
    msg_count = 0

    for row in rows:
        create_time, msg_type, sub_type, is_sender, content, compressed, talker = row
        is_compressed = (sub_type == 5) or (msg_type == 1 and compressed and len(compressed) > 10)

        dt = __import__('datetime').datetime.fromtimestamp(create_time)
        date_str = dt.strftime('%Y-%m-%d')
        time_str = dt.strftime('%H:%M:%S')

        # 发送者：从群成员映射查找
        sender_name = member_map.get(str(is_sender), str(is_sender))

        text = extract_text_content(msg_type, content, compressed, is_compressed)
        if not text or text.strip() == '':
            continue

        if date_str != last_date:
            if last_date != '':
                lines.append('')
            lines.append(f'## {date_str}\n')
            last_date = date_str

        lines.append(f'**[{time_str}] {sender_name}**：{text}')
        msg_count += 1

    lines.append(f'\n---\n*共 {msg_count} 条有效消息*')

    content_str = '\n'.join(lines)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content_str)

    file_size = os.path.getsize(output_file)
    print(f'  -> {output_file} ({file_size/1024:.1f} KB, {msg_count} 条)')
    return output_file, msg_count

# ========== 执行 ==========
print('=' * 60)
print('v6 聊天记录精确导出')
print('=' * 60)

db = sqlite3.connect(DB_PATH)

results = {}

# 私聊
for username, config in PRIVATE_CHATS.items():
    try:
        path, count = export_private_chat(db, username, config)
        results[config['display']] = (path, count)
    except Exception as e:
        print(f'  ❌ {config["display"]} 导出失败: {e}')

# 群聊
for username, display_name in GROUP_CHATS.items():
    try:
        path, count = export_group_chat(db, username, display_name)
        results[display_name] = (path, count)
    except Exception as e:
        print(f'  ❌ {display_name} 导出失败: {e}')

db.close()

# 汇总
print('\n' + '=' * 60)
print('导出汇总')
print('=' * 60)
total_msgs = 0
for name, (path, count) in results.items():
    size = os.path.getsize(path)
    print(f'  {name}: {count} 条, {size/1024:.0f} KB')
    total_msgs += count

print(f'\n总计: {total_msgs} 条消息, {len(results)} 个文件')
print(f'目标目录: {TARGET_DIR}')

# 写入索引文件
index_path = os.path.join(TARGET_DIR, '_INDEX.md')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write('# 交往聊天记录索引\n\n')
    f.write(f'**导出时间**: {__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")}\n\n')
    f.write('| 文件 | 类型 | 消息数 |\n')
    f.write('|------|------|--------|\n')
    for name, (path, count) in results.items():
        fname = os.path.basename(path)
        f.write(f'| [{fname}]({fname}) | {"私聊" if "chat_" in fname else "群聊"} | {count} |\n')
    f.write(f'\n**总计**: {total_msgs} 条\n')

print(f'索引文件: {index_path}')
