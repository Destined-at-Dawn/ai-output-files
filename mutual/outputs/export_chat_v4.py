#!/usr/bin/env python3
"""
WeChat Chat Exporter v4 — with zstd decompression + image/file path extraction
================================================================================
Fixes the garbled text issue caused by zstd-compressed message_content.

Usage:
    python export_chat_v4.py

Output:
    - chat_{name}.md: clean markdown with timestamps and sender labels
    - contact_map.json: wxid to display name mapping
    - File path references embedded in markdown

Key improvements over v3:
    1. Proper zstd decompression of message_content
    2. Image/file XML parsing for media references
    3. Contact name resolution from contact.db
"""

import os
import re
import json
import sqlite3
import hashlib
import zstandard
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

DB_DIR = r"C:\Users\13975\AppData\Local\Temp\wechat-decrypted-wxid_3nvidmluot0a22"
OUTPUT_DIR = r"E:\ai产出文件\牛马\创作\创作\output\wechat_exports_v4"
WECHAT_FILES_DIR = r"D:\data\wechat\xwechat_files\wxid_3nvidmluot0a22_72ff"
FILE_STORAGE_DIR = os.path.join(WECHAT_FILES_DIR, "FileStorage")

# Contacts to export: (wxid, display_name, remark)
TARGET_CONTACTS = [
    ("wxid_bfgr9dxq2o6m22", "Camellia", ""),
    ("wxid_4afm4lnos29o12", "米蛋糕", "陈雅婷 11.27"),
]

# Known sender mapping: { (wxid_hash, real_sender_id): display_name }
# Will be filled dynamically
SENDER_MAP = {}


def get_msg_table_hash(wxid):
    """Get the Msg_{hash} table name for a wxid."""
    return hashlib.md5(wxid.encode()).hexdigest()


def decompress_content(raw):
    """Decompress zstd-compressed message content.

    Handles both bytes (from sqlite3 text_factory=bytes) and str inputs.

    Returns (text, is_compressed) tuple.
    """
    if raw is None:
        return "", False

    # Convert to bytes for processing
    if isinstance(raw, bytes):
        blob = raw
    elif isinstance(raw, str):
        # Try to detect: if the string contains only latin-1 chars,
        # it might be zstd binary that was mis-decoded
        try:
            blob = raw.encode('latin-1')
        except UnicodeEncodeError:
            # Contains real wide chars — it's actual text
            return raw, False
    else:
        return str(raw), False

    # Check for zstd magic bytes: 28 B5 2F FD
    if len(blob) >= 4 and blob[:4] == b'\x28\xb5\x2f\xfd':
        try:
            dctx = zstandard.ZstdDecompressor()
            decompressed = dctx.decompress(blob)
            return decompressed.decode('utf-8', errors='replace'), True
        except Exception:
            # Try skipping magic bytes
            try:
                dctx = zstandard.ZstdDecompressor()
                decompressed = dctx.decompress(blob[4:])
                return decompressed.decode('utf-8', errors='replace'), True
            except Exception:
                return blob.decode('utf-8', errors='replace'), False

    # Not compressed
    try:
        return blob.decode('utf-8', errors='replace'), False
    except Exception:
        return str(blob), False


def extract_media_from_xml(xml_text):
    """Extract image/file/video references from message XML content.

    Returns dict with: images[], files[], videos[], links[]
    """
    result = {"images": [], "files": [], "videos": [], "links": [], "quoted_text": ""}

    if not xml_text:
        return result

    # Try to parse XML
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        # Try cleaning up the XML
        cleaned = xml_text.replace('&', '&amp;').replace('<br/>', '\n')
        try:
            root = ET.fromstring(cleaned)
        except:
            return result

    # Extract image references
    for img in root.iter('img'):
        src = img.get('src', '')
        md5 = img.get('md5', '')
        if src:
            result["images"].append({"src": src, "md5": md5})

    # Extract video references
    for video in root.iter('videomsg'):
        result["videos"].append({
            "length": video.get('length', ''),
            "md5": video.get('md5', ''),
        })

    # Extract appmsg (shared links/articles)
    for appmsg in root.iter('appmsg'):
        title_elem = appmsg.find('title')
        url_elem = appmsg.find('url')
        des_elem = appmsg.find('des')
        if title_elem is not None and title_elem.text:
            result["links"].append({
                "title": title_elem.text,
                "url": url_elem.text if url_elem is not None else "",
                "desc": des_elem.text if des_elem is not None else "",
            })

    # Extract quoted text (reply context)
    for quote in root.iter('appmsg'):
        title = quote.find('title')
        if title is not None and title.text:
            des = quote.find('des')
            if des is not None and des.text:
                result["quoted_text"] = f"[引用: {des.text[:100]}]"

    return result


def format_message(msg_row, sender_names, include_media=True):
    """Format a single message as Markdown.

    msg_row = (local_id, create_time, local_type, real_sender_id, status,
               message_content, compress_content, source)
    """
    local_id, create_time, local_type, real_sender_id, status, raw_content, compress_content, source = msg_row

    # Convert timestamp
    try:
        dt = datetime.fromtimestamp(create_time)
        time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        time_str = str(create_time)

    # Get sender name
    sender_name = sender_names.get(real_sender_id, f"用户{real_sender_id}")

    # Decompress content
    text, is_compressed = decompress_content(raw_content)

    # Also check compress_content column
    if not text.strip() and compress_content:
        text, is_compressed = decompress_content(compress_content)

    # Handle different message types
    type_labels = {
        1: "",  # text
        3: "[图片]",
        34: "[语音]",
        43: "[视频]",
        47: "[表情]",
        49: "[文件/链接]",
        10000: "[系统消息]",
        10002: "[系统消息]",
    }

    type_label = type_labels.get(local_type, f"[类型{local_type}]")

    # Extract media for rich content
    media = {}
    if include_media and text and ('<msg>' in text or '<img' in text or '<appmsg' in text):
        media = extract_media_from_xml(text)

    # Build the markdown line
    parts = []
    parts.append(f"**[{time_str}]** **{sender_name}**")

    if type_label:
        # For media types, show type label instead of garbled XML
        if local_type == 3 and media.get("images"):
            img_info = ", ".join(f"![]({img['src']})" for img in media["images"])
            parts.append(f" {img_info}")
        elif local_type == 49 and media.get("links"):
            for link in media["links"]:
                parts.append(f"\n  > 📎 [{link['title']}]({link['url']})")
        elif local_type == 49 and media.get("files"):
            for fref in media["files"]:
                parts.append(f"\n  > 📄 {fref}")
        else:
            parts.append(f" {type_label}")

    # Add text content (clean up XML)
    if text:
        # Skip pure XML blobs
        if not (text.strip().startswith('<?xml') and local_type != 1):
            # Clean up embedded XML
            cleaned = re.sub(r'<[^>]+>', '', text)
            cleaned = re.sub(r'&[a-z]+;', '', cleaned)
            if cleaned.strip():
                parts.append(f"  \n{cleaned.strip()}")

    # Add quoted text
    if media.get("quoted_text"):
        parts.append(f"\n  {media['quoted_text']}")

    return "> " + "".join(parts) + "\n\n"


def format_plain_text(msg_row, sender_names):
    """Format a single message as plain text (for analysis)."""
    local_id, create_time, local_type, real_sender_id, status, raw_content, compress_content, source = msg_row
    try:
        dt = datetime.fromtimestamp(create_time)
        time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        time_str = str(create_time)
    sender_name = sender_names.get(real_sender_id, f"用户{real_sender_id}")
    text, _ = decompress_content(raw_content)
    if not text.strip() and compress_content:
        text, _ = decompress_content(compress_content)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&[a-z]+;', '', text)
    return f"[{time_str}] {sender_name}: {text.strip()}\n" if text.strip() else ""


def resolve_sender_names(db_conn, msg_table, contact_conn, self_wxid="wxid_3nvidmluot0a22"):
    """Map real_sender_id to display names."""
    c = db_conn.cursor()
    sender_names = {}

    # Get unique senders
    c.execute(f'''
        SELECT DISTINCT real_sender_id
        FROM \"{msg_table}\"
    ''')
    senders = [row[0] for row in c.fetchall()]

    # In WeChat DB, real_sender_id is an integer index.
    # For 1-on-1 chats, there are typically only 2-3 unique IDs:
    # - One maps to self (usually determined by checking the self wxid)
    # - One maps to the other person
    # The key insight from earlier analysis:
    #   real_sender_id=2 → often the account owner (小黎)
    #   Other IDs → contact

    # Try to get sender info from contact.db chatroom_member or similar
    try:
        cc = contact_conn.cursor()
        for sid in senders:
            # Check if this sender has a username mapping
            cc.execute('''
                SELECT username, alias, nick_name, remark
                FROM contact
                WHERE username = ?
            ''', (f"wxid_{sid}",))
            row = cc.fetchone()
            if row:
                sender_names[sid] = row[3] or row[2] or f"wxid_{sid}"
    except:
        pass

    # Fallback: heuristic mapping
    # For the contacts we're targeting:
    # - Camellia (table e72ae18): senders [2, 6] — 2=小黎, 6=Camellia
    # - 米蛋糕 (table b35297d): senders [2, 3026] — 2=小黎, 3026=米蛋糕
    if msg_table.endswith('b35297daf9c0eccd6a495ff3cb4f63ec'):
        # 米蛋糕
        sender_names[2] = "小黎"
        sender_names[3026] = "米蛋糕"
    elif msg_table.endswith('e72ae1877ad9f9cf7892b6b6a3b6daf3'):
        # Camellia
        sender_names[2] = "小黎"
        sender_names[6] = "Camellia"
        sender_names[7] = "[系统-撤回]"

    return sender_names


def export_chat(db_conn, msg_table, contact_conn,
                display_name, output_dir, include_media=True):
    """Export all messages from a chat table to Markdown."""
    c = db_conn.cursor()

    # Resolve sender names
    sender_names = resolve_sender_names(db_conn, msg_table, contact_conn)

    print(f"\n{'='*60}")
    print(f"Exporting: {display_name}")
    print(f"Table: {msg_table}")
    print(f"Senders: {sender_names}")

    # Count messages
    c.execute(f'SELECT COUNT(*) FROM \"{msg_table}\"')
    total = c.fetchone()[0]
    print(f"Total messages: {total}")

    # Helper: bytes to str
    def b2s(b):
        return b.decode('utf-8', errors='replace') if isinstance(b, bytes) else (str(b) if b else "")

    # Read all messages ordered by time
    c.execute(f'''
        SELECT local_id, create_time, local_type, real_sender_id, status,
               message_content, compress_content, source
        FROM \"{msg_table}\"
        ORDER BY create_time ASC, local_id ASC
    ''')

    # Generate output files
    safe_name = re.sub(r'[^\w一-鿿]', '_', display_name)
    md_path = os.path.join(output_dir, f"chat_{safe_name}.md")
    text_path = os.path.join(output_dir, f"chat_{safe_name}_plain.txt")

    stats = defaultdict(int)
    media_refs = []

    with open(md_path, 'w', encoding='utf-8') as md_f, \
         open(text_path, 'w', encoding='utf-8') as txt_f:

        # Header
        md_f.write(f"# {display_name} — 聊天记录\n\n")
        md_f.write(f"- 消息总数: {total}\n")
        md_f.write(f"- 参与人: {', '.join(sender_names.values())}\n")
        md_f.write(f"- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        md_f.write("---\n\n")

        txt_f.write(f"# {display_name} — 聊天记录 (纯文本)\n")
        txt_f.write(f"# 消息总数: {total}\n\n")

        prev_date = None
        msg_count = 0

        for row in c.fetchall():
            msg_count += 1

            local_id, create_time, local_type, real_sender_id, status, \
                raw_content, compress_content, source = row

            # Track stats
            stats[f"sender_{real_sender_id}"] += 1

            try:
                # create_time is integer
                ct_val = create_time if isinstance(create_time, int) else int(create_time)
                dt = datetime.fromtimestamp(ct_val)
                date_key = dt.strftime('%Y-%m-%d')
                time_str = dt.strftime('%H:%M:%S')
            except:
                date_key = str(create_time)[:10]
                time_str = str(create_time)

            # Add date separator
            if date_key != prev_date:
                md_f.write(f"\n## {date_key}\n\n")
                txt_f.write(f"\n--- {date_key} ---\n\n")
                prev_date = date_key

            # Build message tuple (with raw bytes for content)
            msg_tuple = (local_id, create_time, local_type, real_sender_id,
                        status, raw_content, compress_content, source)

            # Write markdown
            md_line = format_message(msg_tuple, sender_names, include_media)
            md_f.write(md_line)

            # Write plain text
            txt_line = format_plain_text(msg_tuple, sender_names)
            if txt_line:
                txt_f.write(txt_line)

            # Progress
            if msg_count % 5000 == 0:
                print(f"  Progress: {msg_count}/{total} ({100*msg_count//total}%)")

        # Footer
        md_f.write(f"\n---\n\n*导出完成。{total} 条消息。*\n")

    # Print stats
    print(f"  Done! {msg_count} messages exported")
    print(f"  MD: {md_path}")
    print(f"  TXT: {text_path}")

    # Type stats
    type_labels = {1: "文本", 3: "图片", 34: "语音", 43: "视频", 47: "表情", 49: "文件/链接", 10000: "系统"}
    for k, v in sorted(stats.items()):
        if k.startswith("type_"):
            t = int(k.split("_")[1])
            label = type_labels.get(t, f"类型{t}")
            print(f"    {label}: {v}")

    return md_path, text_path, dict(stats)


def build_contact_map(db_dir, output_dir):
    """Build a comprehensive contact map from all DBs."""
    contact_map = {}

    # From contact.db
    try:
        conn = sqlite3.connect(os.path.join(db_dir, "contact.db"))
        conn.text_factory = bytes
        c = conn.cursor()
        c.execute('''
            SELECT username, alias, encrypt_username, nick_name, remark, local_type
            FROM contact
        ''')
        for row in c.fetchall():
            def _b2s(b):
                return b.decode('utf-8', errors='replace') if isinstance(b, bytes) else str(b)
            username = _b2s(row[0])
            alias = _b2s(row[1]) if row[1] else ""
            enc = _b2s(row[2]) if row[2] else ""
            nick = _b2s(row[3]) if row[3] else ""
            remark = _b2s(row[4]) if row[4] else ""
            ltype = row[5]
            contact_map[username] = {
                "wxid": username,
                "alias": alias,
                "nickname": nick,
                "remark": remark,
                "type": ltype,
                "msg_hash": get_msg_table_hash(username),
            }
        conn.close()
    except Exception as e:
        print(f"Warning: Could not read contact.db: {e}")

    # Write
    map_path = os.path.join(output_dir, "contact_map.json")
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(contact_map, f, ensure_ascii=False, indent=2)

    print(f"\nContact map: {len(contact_map)} contacts -> {map_path}")
    return contact_map


def main():
    parser = argparse.ArgumentParser(description="WeChat Chat Exporter v4")
    parser.add_argument("--db-dir", default=DB_DIR, help="Decrypted DB directory")
    parser.add_argument("--output", default=OUTPUT_DIR, help="Output directory")
    parser.add_argument("--contacts", nargs="*", help="Specific wxids to export (default: all TARGET_CONTACTS)")
    parser.add_argument("--no-media", action="store_true", help="Skip media extraction")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    # Connect to databases
    msg_db = os.path.join(args.db_dir, "message_0.db")
    contact_db = os.path.join(args.db_dir, "contact.db")

    if not os.path.exists(msg_db):
        print(f"ERROR: message_0.db not found at {msg_db}")
        return

    # Use text_factory=bytes to get raw bytes, avoiding encoding issues
    msg_conn = sqlite3.connect(msg_db)
    msg_conn.text_factory = bytes
    contact_conn = sqlite3.connect(contact_db) if os.path.exists(contact_db) else None
    if contact_conn:
        contact_conn.text_factory = bytes

    # Build contact map
    contact_map = build_contact_map(args.db_dir, args.output)

    # Export targeted contacts
    results = []
    for wxid, display_name, remark in TARGET_CONTACTS:
        table_hash = get_msg_table_hash(wxid)
        table_name = f"Msg_{table_hash}"

        # Verify table exists
        c = msg_conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE name = ?", (table_name,))
        if not c.fetchone():
            print(f"WARNING: Table {table_name} not found for {display_name} ({wxid})")
            continue

        md_path, txt_path, stats = export_chat(
            msg_conn, table_name, contact_conn,
            display_name, args.output, not args.no_media
        )

        results.append({
            "wxid": wxid,
            "display_name": display_name,
            "remark": remark,
            "md_path": md_path,
            "txt_path": txt_path,
            "total_messages": stats.get("total", sum(
                v for k, v in stats.items() if k.startswith("sender_")
            )),
            "senders": {k: v for k, v in stats.items() if k.startswith("sender_")},
            "types": {k: v for k, v in stats.items() if k.startswith("type_")},
        })

    # Write summary
    summary_path = os.path.join(args.output, "export_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"Export complete!")
    print(f"Output directory: {args.output}")
    print(f"Summary: {summary_path}")
    for r in results:
        print(f"  {r['display_name']}: {r['total_messages']} messages -> {os.path.basename(r['md_path'])}")

    msg_conn.close()
    if contact_conn:
        contact_conn.close()


if __name__ == "__main__":
    main()
