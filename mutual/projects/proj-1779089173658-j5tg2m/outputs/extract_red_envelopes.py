#!/usr/bin/env python3
"""从微信数据库提取红包金额 - 2026-06-15"""

import sqlite3, json, zstandard as zstd, re, os
from datetime import datetime
from collections import defaultdict

MY_WXID = 'wxid_3nvidmluot0a22'
OUTPUT_DIR = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs'

# 1. Contact name map
contact_db = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\contact.db'
conn = sqlite3.connect(contact_db)
cur = conn.cursor()
contacts = {}
for row in cur.execute('SELECT username, nick_name, remark, alias FROM contact'):
    uname, nick, remark, alias = row
    name = remark if remark else (nick if nick else (alias if alias else uname))
    contacts[uname] = name
conn.close()

# 2. Get all red envelopes
gen_db = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\general.db'
conn = sqlite3.connect(gen_db)
cur = conn.cursor()
envelopes = cur.execute('''
    SELECT message_server_id, session_name, sender_user_name,
           native_url, send_id, scene_id, hb_status, hb_type, receive_status
    FROM redEnvelopeTable
''').fetchall()
conn.close()

# 3. Find messages and extract amounts
msg_db = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\message_0.db'
conn = sqlite3.connect(msg_db)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE name LIKE 'Msg_%'").fetchall()]

decompressor = zstd.ZstdDecompressor()

results = []
amount_found = 0
amount_missing = 0
debug_samples = []

for env in envelopes:
    mid, session, sender, native_url, send_id, scene, hb_status, hb_type, recv_status = env
    is_mine = (sender == MY_WXID)
    is_group = '@chatroom' in (session or '')
    session_name = contacts.get(session, session)
    sender_name = contacts.get(sender, sender)

    # Find message content
    content = None
    for tname in tables:
        try:
            row = cur.execute(f'SELECT message_content, create_time FROM {tname} WHERE server_id = ?', (mid,)).fetchone()
            if row and row[0]:
                raw = row[0]
                ts = row[1]
                if isinstance(raw, bytes) and len(raw) > 4 and raw[:4] == b'(\xb5/\xfd':
                    try:
                        content = decompressor.decompress(raw).decode('utf-8', errors='replace')
                    except:
                        pass
                elif isinstance(raw, bytes):
                    content = raw.decode('utf-8', errors='replace')
                else:
                    content = raw
                break
        except:
            pass

    # Extract amount
    amount = None
    if content:
        # Try multiple patterns for red envelope amount
        patterns = [
            r'<feedesc><!\[CDATA\[(\d+(?:\.\d+)?)]]></feedesc>',
            r'<feedesc>(\d+(?:\.\d+)?)</feedesc>',
            r'<feedesc>(\d+)',
            r'"fee":"(\d+(?:\.\d+)?)"',
            r'"total_amount":"(\d+(?:\.\d+)?)"',
            r'"amount":"(\d+(?:\.\d+)?)"',
            r'<total_amount>(\d+(?:\.\d+)?)</total_amount>',
            r'total_amount[^>]*>(\d+(?:\.\d+)?)<',
            r'<wishing><!\[CDATA\[(.+?)]]></wishing>',
            r'(\d+(?:\.\d+)?)元',
            r'\xa5(\d+(?:\.\d+)?)',
        ]
        for pat in patterns:
            m = re.search(pat, content)
            if m:
                val = m.group(1)
                try:
                    fval = float(val)
                    if fval > 0 and fval < 100000:  # reasonable amount
                        amount = val
                        break
                except:
                    pass

    if amount:
        amount_found += 1
    else:
        amount_missing += 1

    dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M') if content and ts else 'unknown'

    results.append({
        'message_server_id': mid,
        'session': session_name,
        'session_wxid': session,
        'sender': sender_name,
        'sender_wxid': sender,
        'is_mine': is_mine,
        'is_group': is_group,
        'amount': amount,
        'hb_status': hb_status,
        'hb_type': hb_type,
        'receive_status': recv_status,
        'scene_id': scene,
        'date': dt,
    })

    if content and not amount and len(debug_samples) < 5:
        # Find interesting patterns
        debug_samples.append({
            'mid': mid,
            'session': session_name,
            'sender': sender_name,
            'content_first_300': content[:300],
        })

conn.close()

# Save
output = {
    'extract_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total': len(results),
    'amount_found': amount_found,
    'amount_missing': amount_missing,
    'envelopes': results,
    'debug_samples': debug_samples,
}

json_path = os.path.join(OUTPUT_DIR, 'red_envelopes_full.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# Summary
print(f"Total: {output['total']}")
print(f"Amount found: {amount_found}, Missing: {amount_missing}")

# Classify
sent_by_me = [r for r in results if r['is_mine']]
received_by_me = [r for r in results if not r['is_mine'] and r['receive_status'] == 1]
unreceived = [r for r in results if not r['is_mine'] and r['receive_status'] != 1]

print(f"\nSent by me: {len(sent_by_me)}")
print(f"Received by me: {len(received_by_me)}")
print(f"Not received: {len(unreceived)}")

# Sent totals
sent_total = sum(float(r['amount']) for r in sent_by_me if r['amount'])
received_total = sum(float(r['amount']) for r in received_by_me if r['amount'])
print(f"\nSent total: Y{sent_total:.2f}")
print(f"Received total: Y{received_total:.2f}")

# Group by session for received
print("\n=== RECEIVED BY ME (grouped by sender) ===")
by_sender = defaultdict(lambda: {'count': 0, 'total': 0, 'amounts': []})
for r in received_by_me:
    sender = r['sender']
    amt = float(r['amount']) if r['amount'] else 0
    by_sender[sender]['count'] += 1
    by_sender[sender]['total'] += amt
    if r['amount']:
        by_sender[sender]['amounts'].append(amt)

for sender, data in sorted(by_sender.items(), key=lambda x: -x[1]['total']):
    print(f"  {sender}: Y{data['total']:.2f} ({data['count']}个)")

print(f"\n=== SENT BY ME (grouped by session) ===")
by_session = defaultdict(lambda: {'count': 0, 'total': 0})
for r in sent_by_me:
    sess = r['session']
    amt = float(r['amount']) if r['amount'] else 0
    by_session[sess]['count'] += 1
    by_session[sess]['total'] += amt

for sess, data in sorted(by_session.items(), key=lambda x: -x[1]['total']):
    print(f"  {sess}: Y{data['total']:.2f} ({data['count']}个)")
