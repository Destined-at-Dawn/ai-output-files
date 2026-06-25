#!/usr/bin/env python3
"""
WeChat Chat Exporter v5 — clean implementation with zstd decompression
Usage: python export_chat_v5.py
Output: chat_{name}.md in wechat_exports_v5/
"""
import os, re, json, sqlite3, hashlib, zstandard
from datetime import datetime
from collections import defaultdict

DB_DIR = r"C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22"
OUTPUT_DIR = r"E:\ai产出文件\牛马\创作\创作\output\wechat_exports_v5"

# Contacts: (wxid, display_name)
CONTACTS = [
    ("wxid_bfgr9dxq2o6m22", "Camellia", {2: "小黎", 6: "Camellia", 7: "[系统]"}),
    ("wxid_4afm4lnos29o12", "米蛋糕", {2: "小黎", 3026: "米蛋糕"}),
]

def get_table(wxid):
    return f"Msg_{hashlib.md5(wxid.encode()).hexdigest()}"

def decompress(raw):
    """Decompress zstd content. Handles bytes from sqlite3 text_factory=bytes."""
    if raw is None:
        return "", False
    if isinstance(raw, bytes):
        blob = raw
    elif isinstance(raw, str):
        try: blob = raw.encode('latin-1')
        except: return raw, False
    else:
        return str(raw), False
    if len(blob) >= 4 and blob[:4] == b'\x28\xb5\x2f\xfd':
        try:
            dctx = zstandard.ZstdDecompressor()
            return dctx.decompress(blob).decode('utf-8', errors='replace'), True
        except:
            try:
                return zstandard.ZstdDecompressor().decompress(blob[4:]).decode('utf-8', errors='replace'), True
            except:
                return blob.decode('utf-8', errors='replace'), False
    try:
        return blob.decode('utf-8', errors='replace'), False
    except:
        return str(blob), False

def clean_xml(text):
    """Remove XML tags from text."""
    if not text: return ""
    t = re.sub(r'<[^>]+>', '', text)
    t = re.sub(r'<\?xml[^?]*\?>', '', t)
    t = re.sub(r'&[a-z]+;', '', t)
    return t.strip()

TYPE_LABELS = {1: "", 3: "[图片]", 34: "[语音]", 43: "[视频]", 47: "[表情]", 49: "[文件/链接]", 10000: "[系统]"}

def export_one(msg_conn, table, display_name, sender_names, output_dir):
    """Export one chat."""
    c = msg_conn.cursor()
    c.execute(f'SELECT COUNT(*) FROM "{table}"')
    total = c.fetchone()[0]
    print(f"\n{display_name}: {total} msgs, senders={sender_names}")

    safe = re.sub(r'[<>:\"/\\|?*]', '_', display_name)
    md_path = os.path.join(output_dir, f"chat_{safe}.md")
    txt_path = os.path.join(output_dir, f"chat_{safe}_plain.txt")

    c.execute(f'''
        SELECT local_id, create_time, local_type, real_sender_id,
               message_content, compress_content
        FROM "{table}" ORDER BY create_time ASC, local_id ASC
    ''')

    sender_counts = defaultdict(int)
    prev_date = None
    count = 0

    with open(md_path, 'w', encoding='utf-8') as md_f, \
         open(txt_path, 'w', encoding='utf-8') as txt_f:

        md_f.write(f"# {display_name} — 聊天记录\n\n")
        md_f.write(f"- 消息总数: {total}\n")
        md_f.write(f"- 参与人: {', '.join(sender_names.values())}\n")
        md_f.write(f"- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")

        for row in c.fetchall():
            count += 1
            lid, ct, ltype, rsid = row[0], int(row[1] or 0), int(row[2] or 0), int(row[3] or 0)
            raw_content, compress_content = row[4], row[5]

            text, _ = decompress(raw_content)
            if not text.strip() and compress_content:
                text, _ = decompress(compress_content)

            sender_counts[rsid] += 1

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

            sname = sender_names.get(rsid, f"ID{rsid}")
            tlabel = TYPE_LABELS.get(ltype, "")

            # Markdown line
            line = f"**[{ts}] {sname}**"
            if ltype == 1:  # text
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
                    if url:
                        line += f" | {url.group(2)}"
            elif tlabel:
                line += f" {tlabel}"
                ct2 = clean_xml(text)
                if ct2 and len(ct2) > 2:
                    line += f"  \n{ct2[:200]}"

            md_f.write(line + "\n\n")

            # Plain text
            if ltype == 1 and text.strip():
                ct3 = clean_xml(text)
                if ct3:
                    txt_f.write(f"[{ts}] {sname}: {ct3}\n")

            if count % 10000 == 0:
                print(f"  {count}/{total}")

        md_f.write(f"\n---\n\n*{count} 条消息。*\n")

    print(f"  Done: {count} msgs -> {os.path.basename(md_path)}")
    for sid, cnt in sorted(sender_counts.items(), key=lambda x: -x[1]):
        print(f"    {sender_names.get(sid, f'ID{sid}')}: {cnt}")
    return md_path, txt_path

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    msg_db = os.path.join(DB_DIR, "message_0.db")

    if not os.path.exists(msg_db):
        print(f"ERROR: {msg_db} not found")
        return

    msg_conn = sqlite3.connect(msg_db)
    msg_conn.text_factory = bytes  # Critical: raw bytes

    results = []
    for wxid, name, senders in CONTACTS:
        table = get_table(wxid)
        c = msg_conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE name=?", (table,))
        if not c.fetchone():
            print(f"SKIP: table {table} not found for {name}")
            continue
        md_path, txt_path = export_one(msg_conn, table, name, senders, OUTPUT_DIR)
        results.append({"name": name, "wxid": wxid, "md": md_path, "txt": txt_path})

    summary_path = os.path.join(OUTPUT_DIR, "summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n=== Done! ===")
    for r in results:
        print(f"  {r['name']}: {os.path.basename(r['md'])}")
    print(f"  Output: {OUTPUT_DIR}")

    msg_conn.close()

if __name__ == "__main__":
    main()
