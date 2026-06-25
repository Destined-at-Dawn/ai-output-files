
"""
v7: 精确导出聊天记录到个人区交往目录
每个联系人/群聊使用对应的 Msg_<md5> 表
"""
import sqlite3, json, re, os, sys, hashlib, zstandard as zstd

DB_PATH = r'C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22\message_0.db'
TARGET_DIR = r'E:\ai产出文件\牛马\个人\个人\projects\20260425-成长历程\成长历程\交往'
os.makedirs(TARGET_DIR, exist_ok=True)

dctx = zstd.ZstdDecompressor()

# ===== 配置 =====
PRIVATE_CHATS = {
    'wxid_bfgr9dxq2o6m22': {
        'display': 'Camellia',
        'senders': {'2': '小黎', '6': 'Camellia', '7': '[系统]'},
    },
    'wxid_4afm4lnos29o12': {
        'display': '米蛋糕（陈雅婷）',
        'senders': {'2': '小黎', '3026': '陈雅婷', '3': '[系统]'},
    },
    'wxid_iaeun6rhbyb532': {
        'display': '少年Lee（OPC合伙人）',
        'senders': {'2': '小黎', None: '少年Lee'},
    },
}

GROUP_CHATS = {
    '50267796386@chatroom': '青柠同频轻创圈',
    '56820316831@chatroom': '破界青年OPC会员',
    '45375846863@chatroom': 'OPC启动计划1.0',
    '49472124843@chatroom': '破界向上生长基地六群',
    '56989512808@chatroom': '牛马AI灰度测试群',
}

def get_table(uname):
    return f'Msg_{hashlib.md5(uname.encode()).hexdigest()}'

# ===== 工具函数 =====
def decompress_zstd(blob):
    if blob is None: return None
    try: return dctx.decompress(blob).decode('utf-8', errors='replace')
    except: return None

def clean_text(xml_str, msg_type):
    if not xml_str: return ''
    text = xml_str

    if msg_type in (3,):
        md5_m = re.search(r'md5[= "]+([a-f0-9]+)', text, re.IGNORECASE)
        cdn_m = re.search(r'cdnattachurl[= "]+([^"]+)', text, re.IGNORECASE)
        parts = ['[图片]']
        if md5_m: parts.append(f'MD5:{md5_m.group(1)}')
        if cdn_m:
            fn_m = re.search(r'[?&]filename=([^&]+)', cdn_m.group(1))
            if fn_m: parts.append(f'文件:{fn_m.group(1)}')
        return ' '.join(parts)
    if msg_type == 43:
        md5 = re.search(r'md5[= "]+([a-f0-9]+)', text, re.IGNORECASE)
        return f'[视频] MD5:{md5.group(1)}' if md5 else '[视频]'
    if msg_type == 49:
        title = re.search(r'<title>(.*?)</title>', text, re.DOTALL)
        if title: return f'[链接] {title.group(1).strip()}'
        desc = re.search(r'<des>(.*?)</des>', text, re.DOTALL)
        if desc: return f'[文件] {desc.group(1).strip()}'
        return '[文件/链接]'
    if msg_type == 34: return '[语音]'
    if msg_type == 47:
        emoji = re.search(r'md5[= "]+([a-f0-9]+)', text, re.IGNORECASE)
        return f'[表情]' if not emoji else f'[表情 {emoji.group(1)[:8]}]'
    if msg_type == 10000:
        cdata = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
        if cdata:
            cleaned = ' '.join(cdata).strip()
            return f'[系统] {cleaned[:200]}'
        return '[系统消息]'
    if msg_type in (436207665,): return '[红包]'
    if msg_type == 48:
        label = re.search(r'label[= "]+([^"]+)', text, re.IGNORECASE)
        return f'[位置] {label.group(1)}' if label else '[位置]'
    if msg_type == 57:
        cdata = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
        return f'[引用回复] {" ".join(cdata)[:100]}' if cdata else '[引用回复]'
    if msg_type == 42: return '[名片]'
    if msg_type == 62: return '[视频号]'
    if msg_type == 44: return '[直播]'

    if text.startswith('<msg>') or text.startswith('<?xml'):
        cdata = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
        if cdata: return ' '.join(cdata).strip()
        cleaned = re.sub(r'<[^>]+>', '', text)
        if cleaned.strip(): return cleaned.strip()[:500]

    return text.strip()

def extract_content(msg_type, content, compressed):
    if compressed:
        decompressed = decompress_zstd(compressed)
        if decompressed: return clean_text(decompressed, msg_type)
    if content: return clean_text(content, msg_type)
    return ''

def get_sender_for_group(raw, real_sid):
    if raw is None: return f'wxid_{real_sid}'
    if isinstance(raw, bytes):
        try: raw = raw.decode('utf-8', errors='replace')
        except: return f'wxid_{real_sid}'
    if isinstance(raw, str) and '<?xml' in raw:
        for tag in ['username', 'displayname', 'nickname']:
            m = re.search(f'<{tag}><!\[CDATA\[(.*?)\]\]>', raw)
            if m: return m.group(1)
    return f'wxid_{real_sid}'

# ===== 主导出 =====
from datetime import datetime

def export_private(db, uname, cfg):
    display = cfg['display']
    smap = cfg['senders']
    table = get_table(uname)
    out = os.path.join(TARGET_DIR, f'{display}.md')

    # 检查表是否存在
    cur = db.execute("SELECT name FROM sqlite_master WHERE name=?", (table,))
    if not cur.fetchone():
        print(f'[私聊] {display}: 表 {table} 不存在')
        return None, 0

    cur = db.execute(f'''
        SELECT create_time, local_type, message_content, compress_content, real_sender_id, status
        FROM {table}
        ORDER BY create_time ASC
    ''')

    rows = cur.fetchall()
    lines = [f'# {display}', '',
             f'> 对象: {display}',
             f'> 消息总数: {len(rows)}',
             f'> 导出时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             '', '---', '']

    last_date = ''; valid = 0
    for row in rows:
        t, mtype, content, compressed, real_sid, status = row
        if t is None: continue
        dt = datetime.fromtimestamp(t)
        ds = dt.strftime('%Y-%m-%d'); ts = dt.strftime('%H:%M:%S')

        skey = str(real_sid) if real_sid else str(status)
        sender = smap.get(skey, f'用户{real_sid or status}')

        text = extract_content(mtype, content, compressed)
        if not text or not text.strip(): continue
        if 'revokemsg' in text.lower() or '撤回' in text:
            text = '[消息已撤回]'

        if ds != last_date:
            lines.extend(['', f'## {ds}', ''])
            last_date = ds
        lines.append(f'**[{ts}] {sender}**：{text}')
        valid += 1

    lines.extend(['', '---', f'*共 {valid} 条有效消息*'])
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    sz = os.path.getsize(out)
    print(f'[私聊] {display}: {valid}条, {sz/1024:.0f}KB')
    return out, valid


def export_group(db, uname, display):
    table = get_table(uname)
    out = os.path.join(TARGET_DIR, f'{display}.md')

    cur = db.execute("SELECT name FROM sqlite_master WHERE name=?", (table,))
    if not cur.fetchone():
        print(f'[群聊] {display}: 表 {table} 不存在')
        return None, 0

    cur = db.execute(f'''
        SELECT create_time, local_type, message_content, compress_content, real_sender_id, status
        FROM {table}
        ORDER BY create_time ASC
    ''')
    rows = cur.fetchall()

    # 建群成员映射
    member_map = {}
    for row in rows:
        t, mtype, content, compressed, real_sid, status = row
        raw = decompress_zstd(compressed) if compressed else content
        name = get_sender_for_group(raw, real_sid)
        if real_sid and real_sid != 0:
            if real_sid not in member_map or 'wxid_' not in name:
                member_map[real_sid] = name

    lines = [f'# {display}', '',
             f'> 群聊: {display}',
             f'> 消息总数: {len(rows)}',
             f'> 识别成员: {len(member_map)} 人',
             f'> 导出时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             '']

    if member_map:
        lines.append('## 群成员'); lines.append('')
        for sid, name in sorted(member_map.items()):
            lines.append(f'- {name}')
        lines.append('')

    lines.extend(['---', ''])
    last_date = ''; valid = 0

    for row in rows:
        t, mtype, content, compressed, real_sid, status = row
        if t is None: continue
        dt = datetime.fromtimestamp(t)
        ds = dt.strftime('%Y-%m-%d'); ts = dt.strftime('%H:%M:%S')

        # 发送者
        if real_sid == 0 and status == 2:
            sender = '小黎'
        elif real_sid == 0:
            continue
        else:
            sender = member_map.get(real_sid, f'wxid_{real_sid}')

        text = extract_content(mtype, content, compressed)
        if not text or not text.strip(): continue

        if ds != last_date:
            lines.extend(['', f'## {ds}', ''])
            last_date = ds
        lines.append(f'**[{ts}] {sender}**：{text}')
        valid += 1

    lines.extend(['', '---', f'*共 {valid} 条有效消息*'])
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    sz = os.path.getsize(out)
    print(f'[群聊] {display}: {valid}条, {sz/1024:.0f}KB')
    return out, valid


# ===== 执行 =====
db = sqlite3.connect(DB_PATH)
results = {}

for uname, cfg in PRIVATE_CHATS.items():
    try:
        p, c = export_private(db, uname, cfg)
        if p: results[cfg['display']] = (p, c)
    except Exception as e:
        print(f'[私聊] {cfg["display"]}: FAIL - {e}')

for uname, dname in GROUP_CHATS.items():
    try:
        p, c = export_group(db, uname, dname)
        if p: results[dname] = (p, c)
    except Exception as e:
        print(f'[群聊] {dname}: FAIL - {e}')

db.close()

total = sum(c for _, c in results.values())
print(f'\n===== 导出完成 =====')
for name, (path, count) in sorted(results.items()):
    print(f'  {name}: {count} 条')
print(f'  总计: {total} 条, {len(results)} 个文件')
print(f'  目录: {TARGET_DIR}')
