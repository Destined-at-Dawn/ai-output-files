
"""
v8 Final: 聊天记录精确导出到个人区交往目录
修复:
1. zstd解压所有message_content（不只是compress_content）
2. local_type=10000 永远标为系统消息
3. 大二进制消息类型(244813135921等)的解压和XML解析
"""
import sqlite3, json, re, os, sys, hashlib, zstandard as zstd

DB_PATH = r'C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22\message_0.db'
TARGET_DIR = r'E:\ai产出文件\牛马\个人\个人\projects\20260425-成长历程\成长历程\交往'
os.makedirs(TARGET_DIR, exist_ok=True)

dctx = zstd.ZstdDecompressor()
ZSTD_MAGIC = b'\x28\xb5\x2f\xfd'

PRIVATE_CHATS = {
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
}

def to_str(data):
    if data is None: return None
    if isinstance(data, str): return data
    if isinstance(data, bytes):
        try: return data.decode('utf-8', errors='replace')
        except: return data.decode('latin-1', errors='replace')
    return str(data)

def try_decompress(data):
    """尝试zstd解压，失败返回None"""
    if data is None: return None
    if isinstance(data, str): data = data.encode('latin-1', errors='replace')
    if not isinstance(data, bytes): return None
    # 检查zstd magic
    if len(data) < 4 or data[:4] != ZSTD_MAGIC:
        return None
    try:
        result = dctx.decompress(data)
        if isinstance(result, bytes):
            # 找到XML起始位置
            s = result.decode('utf-8', errors='replace')
            idx = s.find('<?xml')
            if idx > 0:
                s = s[idx:]  # 跳过前缀垃圾数据
            elif idx == -1:
                # 没有XML，可能是纯文本
                # 去掉前缀二进制垃圾
                clean = re.sub(r'[^\x20-\x7e一-鿿　-〿＀-￯\n\r\t，。！？、；：""''（）【】《》…—\U0001f300-\U0001f9ff]+', '', s)
                if len(clean) > 5:
                    s = clean.strip()
                else:
                    s = s.strip()
            return s
        return result
    except:
        return None

def clean_text(xml_str, msg_type):
    if not xml_str: return ''
    text = xml_str

    # 图片
    if msg_type in (3,):
        md5_m = re.search(r'md5[= "]+([a-f0-9]+)', text, re.IGNORECASE)
        cdn_m = re.search(r'cdnattachurl[= "]+([^"]+)', text, re.IGNORECASE)
        parts = ['[图片]']
        if md5_m: parts.append(f'MD5:{md5_m.group(1)}')
        if cdn_m:
            fn_m = re.search(r'[?&]filename=([^&]+)', cdn_m.group(1))
            if fn_m: parts.append(f'{fn_m.group(1)}')
        return ' '.join(parts)

    # 视频
    if msg_type == 43:
        md5 = re.search(r'md5[= "]+([a-f0-9]+)', text, re.IGNORECASE)
        return f'[视频] MD5:{md5.group(1)}' if md5 else '[视频]'

    # 文件/链接/appmsg (type=49, type=5, and custom types like 244813135921)
    if msg_type == 49 or msg_type == 5:
        title = re.search(r'<title>(.*?)</title>', text, re.DOTALL)
        if title:
            t = title.group(1).strip()
            if t: return f'[链接] {t}'
        desc = re.search(r'<des>(.*?)</des>', text, re.DOTALL)
        if desc:
            d = desc.group(1).strip()
            if d: return f'[文件] {d}'
        return '[文件/链接]'

    # AppMsg with embedded type (quote replies, shared moments etc)
    # type=57 inside appmsg = quote reply
    if msg_type not in (1, 3, 34, 42, 43, 44, 47, 48, 49, 57, 62, 10000, 436207665) and msg_type > 100:
        # Custom/large types - try to extract appmsg
        title = re.search(r'<title>(.*?)</title>', text, re.DOTALL)
        inner_type = re.search(r'<type>(\d+)</type>', text)
        if title:
            t = title.group(1).strip()
            if inner_type:
                it = inner_type.group(1)
                if it == '57':
                    return f'[引用回复] {t[:200]}'
                return f'[{msg_type}/{it}] {t[:200]}'
            return f'[{msg_type}] {t[:200]}'
        # Extract CData
        cdata = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
        if cdata:
            return ' '.join(cdata)[:300].strip()
        return f'[{msg_type}]'

    # 语音
    if msg_type == 34: return '[语音]'

    # 表情
    if msg_type == 47:
        emoji = re.search(r'md5[= "]+([a-f0-9]+)', text, re.IGNORECASE)
        return f'[表情]' if not emoji else f'[表情 {emoji.group(1)[:8]}]'

    # 系统消息
    if msg_type == 10000:
        # 已经解压过的内容
        if 'revokemsg' in text.lower():
            return '[消息已撤回]'
        if '<?xml' in text:
            cdata = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
            if cdata: return f'[系统] {" ".join(cdata)[:200]}'
            return '[系统消息]'
        return f'[系统] {text[:200]}'

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

    # 纯XML
    if text.startswith('<msg>') or text.startswith('<?xml'):
        cdata = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.DOTALL)
        if cdata: return ' '.join(cdata).strip()
        cleaned = re.sub(r'<[^>]+>', '', text)
        if cleaned.strip(): return cleaned.strip()[:500]

    return text.strip()

def extract_content(msg_type, content):
    """提取消息文本 - 先尝试zstd解压，再解析"""
    if content is None:
        return ''

    # 尝试zstd解压
    decompressed = try_decompress(content)
    if decompressed:
        return clean_text(decompressed, msg_type)

    # 非zstd的bytes/string
    s = to_str(content)
    if s:
        return clean_text(s, msg_type)
    return ''

def get_sender_for_group(content, real_sid):
    """从群聊消息XML提取发送者名称"""
    raw = try_decompress(content)
    if raw is None:
        raw = to_str(content)
    if not raw: return f'wxid_{real_sid}'
    if isinstance(raw, str) and '<?xml' in raw:
        for tag in ['username', 'displayname', 'nickname']:
            m = re.search(f'<{tag}><!\[CDATA\[(.*?)\]\]>', raw)
            if m: return m.group(1)
    return f'wxid_{real_sid}'

from datetime import datetime

def export_private(db, uname, cfg):
    display = cfg['display']
    smap = cfg['senders']
    table = f'Msg_{hashlib.md5(uname.encode()).hexdigest()}'
    out = os.path.join(TARGET_DIR, f'{display}.md')

    cur = db.execute("SELECT name FROM sqlite_master WHERE name=?", (table,))
    if not cur.fetchone():
        print(f'[SKIP] {display}: table not found')
        return None, 0

    cur = db.execute(f'SELECT create_time, local_type, message_content, real_sender_id, status FROM {table} ORDER BY create_time ASC')
    rows = cur.fetchall()
    if not rows:
        print(f'[SKIP] {display}: 0 rows')
        return None, 0

    lines = [f'# {display}', '',
             f'> ID: {uname}',
             f'> 总消息: {len(rows)}',
             f'> 导出: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             '', '---', '']
    last_date = ''; v = 0
    for row in rows:
        t, mtype, content, real_sid, status = row
        if t is None: continue

        # 系统消息永远标为[系统]
        if mtype == 10000:
            sender = '[系统]'
        else:
            skey = str(real_sid) if real_sid else str(status)
            sender = smap.get(skey, f'用户{real_sid or status}')

        text = extract_content(mtype, content)
        if not text or not text.strip(): continue

        dt = datetime.fromtimestamp(t)
        ds = dt.strftime('%Y-%m-%d'); ts = dt.strftime('%H:%M:%S')

        if ds != last_date:
            lines.extend(['', f'## {ds}', ''])
            last_date = ds
        lines.append(f'**[{ts}] {sender}**：{text}')
        v += 1

    lines.extend(['', '---', f'*{v} 条有效消息*'])
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'[OK] {display}: {v}条, {os.path.getsize(out)/1024:.0f}KB')
    return out, v


def export_group(db, uname, display):
    table = f'Msg_{hashlib.md5(uname.encode()).hexdigest()}'
    out = os.path.join(TARGET_DIR, f'{display}.md')

    cur = db.execute("SELECT name FROM sqlite_master WHERE name=?", (table,))
    if not cur.fetchone():
        print(f'[SKIP] {display}: table not found')
        return None, 0

    cur = db.execute(f'SELECT create_time, local_type, message_content, real_sender_id, status FROM {table} ORDER BY create_time ASC')
    rows = cur.fetchall()
    if not rows:
        print(f'[SKIP] {display}: 0 rows')
        return None, 0

    # 建群成员映射
    member_map = {}
    for row in rows:
        t, mtype, content, real_sid, status = row
        name = get_sender_for_group(content, real_sid)
        if real_sid and real_sid != 0:
            if real_sid not in member_map or 'wxid_' not in name:
                member_map[real_sid] = name

    # 小黎的real_sender_id通常是0（自己发的消息）
    # 需要通过status=2来识别

    lines = [f'# {display}', '',
             f'> 群聊: {display}',
             f'> ID: {uname}',
             f'> 总消息: {len(rows)}',
             f'> 成员: {len(member_map)} 人',
             f'> 导出: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             '']
    if member_map:
        lines.append('## 群成员'); lines.append('')
        for sid, name in sorted(member_map.items()):
            lines.append(f'- {name}')
        lines.append('')
    lines.extend(['---', ''])
    last_date = ''; v = 0
    for row in rows:
        t, mtype, content, real_sid, status = row
        if t is None: continue

        # 群聊发送者识别
        if real_sid == 0 and status == 2:
            sender = '小黎'
        elif real_sid == 0:
            continue  # 未知发送者
        else:
            sender = member_map.get(real_sid, f'wxid_{real_sid}')

        text = extract_content(mtype, content)
        if not text or not text.strip(): continue

        dt = datetime.fromtimestamp(t)
        ds = dt.strftime('%Y-%m-%d'); ts = dt.strftime('%H:%M:%S')

        if ds != last_date:
            lines.extend(['', f'## {ds}', ''])
            last_date = ds
        lines.append(f'**[{ts}] {sender}**：{text}')
        v += 1

    lines.extend(['', '---', f'*{v} 条有效消息*'])
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'[OK] {display}: {v}条, {os.path.getsize(out)/1024:.0f}KB')
    return out, v


# ===== 执行 =====
db = sqlite3.connect(DB_PATH)
results = {}
for uname, cfg in PRIVATE_CHATS.items():
    try:
        p, c = export_private(db, uname, cfg)
        if p: results[cfg['display']] = (p, c)
    except Exception as e:
        print(f'[FAIL] {cfg["display"]}: {e}')
        import traceback; traceback.print_exc()
for uname, dname in GROUP_CHATS.items():
    try:
        p, c = export_group(db, uname, dname)
        if p: results[dname] = (p, c)
    except Exception as e:
        print(f'[FAIL] {dname}: {e}')
        import traceback; traceback.print_exc()
db.close()

total = sum(c for _, c in results.values())
print(f'\n===== DONE =====')
for name, (path, count) in sorted(results.items()):
    sz = os.path.getsize(path)
    print(f'  {name}: {count} 条, {sz/1024:.0f}KB')
print(f'  Total: {total} 条, {len(results)} files')
print(f'  Dir: {TARGET_DIR}')
