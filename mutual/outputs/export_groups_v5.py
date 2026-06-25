#!/usr/bin/env python3
"""WeChat Group Chat Exporter v5 — exports group chats with sender names"""
import os, re, json, sqlite3, hashlib, zstandard
from datetime import datetime
from collections import defaultdict

DB_DIR = r"C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22"
OUTPUT_DIR = r"E:\ai产出文件\牛马\创作\创作\output\wechat_exports_v5"

# Group chats to export: (wxid, display_name, note)
GROUPS = [
    ("50267796386@chatroom", "青柠同频轻创圈", "社群运营"),
    ("22631410325@chatroom", "B2然然分享", "资源分享"),
    ("44207639527@chatroom", "终成大学生涯规划课十八群", "学习社群"),
    ("56989512808@chatroom", "牛马AI灰度测试群", "AI开发"),
    ("45375846863@chatroom", "OPC启动计划1.0", "OPC创业"),
    ("56820316831@chatroom", "破界青年OPC会员", "OPC社群"),
]

def get_table(wxid):
    return f"Msg_{hashlib.md5(wxid.encode()).hexdigest()}"

def decompress(raw):
    if raw is None: return "", False
    if isinstance(raw, bytes): blob = raw
    elif isinstance(raw, str):
        try: blob = raw.encode('latin-1')
        except: return raw, False
    else: return str(raw), False
    if len(blob) >= 4 and blob[:4] == b'\x28\xb5\x2f\xfd':
        try:
            dctx = zstandard.ZstdDecompressor()
            return dctx.decompress(blob).decode('utf-8', errors='replace'), True
        except:
            try:
                return zstandard.ZstdDecompressor().decompress(blob[4:]).decode('utf-8', errors='replace'), True
            except:
                return blob.decode('utf-8', errors='replace'), False
    try: return blob.decode('utf-8', errors='replace'), False
    except: return str(blob), False

def clean_xml(t):
    if not t: return ""
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'<\?xml[^?]*\?>', '', t)
    t = re.sub(r'&[a-z]+;', '', t)
    return t.strip()

def resolve_chatroom_members(contact_conn, wxid):
    """Get sender display names from chatroom_member table."""
    senders = {}
    try:
        cc = contact_conn.cursor()
        cc.execute('''
            SELECT chat_room_member_list FROM chat_room
            WHERE username = ?
        ''', (wxid.encode('utf-8') if isinstance(wxid, str) else wxid,))
        row = cc.fetchone()
        if row and row[0]:
            # chat_room_member_list is XML or encoded member list
            data = row[0]
            if isinstance(data, bytes):
                data = data.decode('utf-8', errors='replace')
            # Parse member list - format varies, try common patterns
            # Format: "wxid_xxx:;wxid_yyy:;"
            members = re.findall(r'(wxid_[a-z0-9]+)', data)
            for mid in members:
                # Get display name
                cc.execute('''
                    SELECT nick_name, remark FROM contact
                    WHERE username = ?
                ''', (mid,))
                crow = cc.fetchone()
                if crow:
                    def b2s(b): return b.decode('utf-8', errors='replace') if isinstance(b, bytes) else str(b or '')
                    nick = b2s(crow[0]) if crow[0] else ''
                    remark = b2s(crow[1]) if crow[1] else ''
                    if remark:
                        senders[mid] = remark
                    elif nick:
                        senders[mid] = nick
    except Exception as e:
        print(f"  Note: chatroom member resolution limited: {e}")

    return senders

TYPE_LABELS = {1: "", 3: "[图片]", 34: "[语音]", 43: "[视频]", 47: "[表情]", 49: "[文件/链接]", 10000: "[系统]"}

def export_group(msg_conn, contact_conn, table, display_name, wxid, output_dir):
    """Export a group chat."""
    c = msg_conn.cursor()
    c.execute(f'SELECT COUNT(*) FROM "{table}"')
    total = c.fetchone()[0]
    print(f"\n{display_name}: {total} msgs")

    # Resolve member names
    member_names = resolve_chatroom_members(contact_conn, wxid) if contact_conn else {}
    print(f"  Resolved {len(member_names)} members")

    safe = re.sub(r'[<>:\"/\\|?*]', '_', display_name)
    md_path = os.path.join(output_dir, f"group_{safe}.md")
    txt_path = os.path.join(output_dir, f"group_{safe}_plain.txt")

    c.execute(f'''
        SELECT local_id, create_time, local_type, real_sender_id,
               message_content, compress_content, source
        FROM "{table}" ORDER BY create_time ASC, local_id ASC
    ''')

    sender_counts = defaultdict(int)
    prev_date = None; count = 0

    # Try to get sender mapping from source field
    # In group chats, source contains "wxid_xxx:\nmessage" format
    sender_from_source = {}

    with open(md_path, 'w', encoding='utf-8') as md_f, \
         open(txt_path, 'w', encoding='utf-8') as txt_f:

        md_f.write(f"# {display_name} — 群聊记录\n\n")
        md_f.write(f"- 消息总数: {total}\n")
        md_f.write(f"- 群ID: {wxid}\n")
        md_f.write(f"- 已解析群成员: {len(member_names)}\n")
        md_f.write(f"- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")

        for row in c.fetchall():
            count += 1
            lid = row[0]
            ct = int(row[1] or 0)
            ltype = int(row[2] or 0)
            rsid = int(row[3] or 0)
            raw_content = row[4]
            compress_content = row[5]
            source = row[6]

            text, _ = decompress(raw_content)
            if not text.strip() and compress_content:
                text, _ = decompress(compress_content)

            sender_counts[rsid] += 1

            # Try to get sender from source field (group chat format)
            sender_wxid = None
            sender_display = f"成员{rsid}"

            if source and isinstance(source, bytes):
                source_str = source.decode('utf-8', errors='replace')
                # Group chat source format: "wxid_xxx:\n" or "<msgsource>...</msgsource>"
                src_match = re.match(r'(wxid_[a-z0-9]+)', source_str)
                if src_match:
                    sender_wxid = src_match.group(1)
                    if sender_wxid in member_names:
                        sender_display = member_names[sender_wxid]
                    else:
                        sender_display = sender_wxid[-8:] or sender_wxid
                else:
                    # Try XML
                    xml_src = re.search(r'<username>([^<]+)</username>', source_str)
                    if xml_src:
                        sender_wxid = xml_src.group(1)
                        sender_display = member_names.get(sender_wxid, sender_wxid[-8:] if sender_wxid else f"成员{rsid}")

            # Cache the mapping
            if sender_wxid and rsid not in sender_from_source:
                sender_from_source[rsid] = sender_wxid

            try:
                dt = datetime.fromtimestamp(ct)
                dk = dt.strftime('%Y-%m-%d')
                ts = dt.strftime('%H:%M:%S')
            except:
                dk = str(ct)[:10]
                ts = str(ct)

            if dk != prev_date:
                md_f.write(f"\n## {dk}\n\n")
                prev_date = dk

            tlabel = TYPE_LABELS.get(ltype, "")
            line = f"**[{ts}] {sender_display}**"

            if ltype == 1 and text.strip():
                ct2 = clean_xml(text)
                if ct2:
                    line += f"  \n{ct2}"
            elif ltype == 3:
                line += f" [图片]"
            elif ltype == 34:
                line += f" [语音]"
            elif ltype == 43:
                line += f" [视频]"
            elif ltype == 47:
                line += f" [表情]"
            elif ltype == 49:
                title = re.search(r'<title>([^<]*)</title>', text)
                url = re.search(r'<url>(?:<!\[CDATA\[)?([^<\]]+)', text)
                if title:
                    line += f"  \n> 📎 {title.group(1)}"
                    if url: line += f" | {url.group(2)}"
            elif tlabel:
                line += f" {tlabel}"
                ct2 = clean_xml(text)
                if ct2 and len(ct2) > 2:
                    line += f"  \n{ct2[:200]}"

            md_f.write(line + "\n\n")

            if ltype == 1 and text.strip():
                ct3 = clean_xml(text)
                if ct3:
                    txt_f.write(f"[{ts}] {sender_display}: {ct3}\n")

            if count % 10000 == 0:
                print(f"  {count}/{total}")

        md_f.write(f"\n---\n\n*{count} 条消息。*\n")

    print(f"  Done: {count} msgs -> {os.path.basename(md_path)}")
    for sid, cnt in sorted(sender_counts.items(), key=lambda x: -x[1])[:10]:
        name = sender_from_source.get(sid, f"ID{sid}")
        print(f"    {name}: {cnt}")

    # Save sender map
    with open(os.path.join(output_dir, f"group_{safe}_senders.json"), 'w', encoding='utf-8') as f:
        json.dump({str(k): v for k, v in sender_from_source.items()}, f, ensure_ascii=False, indent=2)

    return md_path

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    msg_db = os.path.join(DB_DIR, "message_0.db")
    contact_db = os.path.join(DB_DIR, "contact.db")

    msg_conn = sqlite3.connect(msg_db)
    msg_conn.text_factory = bytes

    contact_conn = sqlite3.connect(contact_db) if os.path.exists(contact_db) else None
    if contact_conn:
        contact_conn.text_factory = bytes

    for wxid, name, note in GROUPS:
        table = get_table(wxid)
        c = msg_conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE name=?", (table,))
        if not c.fetchone():
            print(f"SKIP: {name} ({wxid}) - table not found")
            continue
        try:
            export_group(msg_conn, contact_conn, table, f"{name}({note})", wxid, OUTPUT_DIR)
        except Exception as e:
            print(f"ERROR exporting {name}: {e}")
            continue

    msg_conn.close()
    if contact_conn: contact_conn.close()
    print(f"\nDone! Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
