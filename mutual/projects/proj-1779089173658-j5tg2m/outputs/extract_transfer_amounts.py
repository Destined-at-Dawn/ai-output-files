#!/usr/bin/env python3
"""从微信数据库提取转账金额 - 2026-06-15"""

import sqlite3, json, zstandard as zstd, re, os, sys
from datetime import datetime

MY_WXID = 'wxid_3nvidmluot0a22'
OUTPUT_DIR = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs'

# 1. Get contact name map
contact_db = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\contact.db'
conn = sqlite3.connect(contact_db)
cur = conn.cursor()
contacts = {}
for row in cur.execute('SELECT username, nick_name, remark, alias FROM contact'):
    uname, nick, remark, alias = row
    name = remark if remark else (nick if nick else (alias if alias else uname))
    contacts[uname] = name
conn.close()

# 2. Get all transfers from general.db
gen_db = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\general.db'
conn = sqlite3.connect(gen_db)
cur = conn.cursor()
transfers = cur.execute('''
    SELECT transfer_id, message_server_id, second_message_server_id,
           session_name, pay_sub_type, pay_receiver, pay_payer, begin_transfer_time
    FROM transferTable ORDER BY begin_transfer_time
''').fetchall()
conn.close()

# 3. Search message_0.db for transfer content and extract amount
msg_db = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\message_0.db'
conn = sqlite3.connect(msg_db)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE name LIKE 'Msg_%'").fetchall()]

decompressor = zstd.ZstdDecompressor()

results = []
raw_snippets = []  # For debugging

for t in transfers:
    tid, mid, mid2, session, stype, receiver, payer, ts = t
    is_income = (receiver == MY_WXID)

    # Find message content
    content = None
    for tname in tables:
        for m in [mid, mid2]:
            if m == 0:
                continue
            try:
                row = cur.execute(f'SELECT message_content FROM {tname} WHERE server_id = ?', (m,)).fetchone()
                if row and row[0]:
                    raw = row[0]
                    if isinstance(raw, bytes) and len(raw) > 4 and raw[:4] == b'(\xb5/\xfd':
                        try:
                            content = decompressor.decompress(raw).decode('utf-8', errors='replace')
                        except Exception as e:
                            content = None
                    elif isinstance(raw, bytes):
                        content = raw.decode('utf-8', errors='replace')
                    else:
                        content = raw
                    break
            except:
                pass
        if content:
            break

    # Extract amount from content
    amount = None
    if content:
        # Try multiple patterns
        patterns = [
            r'<feedesc><!\[CDATA\[(\d+(?:\.\d+)?)]]></feedesc>',
            r'<feedesc>(\d+(?:\.\d+)?)</feedesc>',
            r'<feedesc>(\d+)',
            r'total_fee[^>]*>(\d+(?:\.\d+)?)<',
            r'<paymsgvalue>(\d+)</paymsgvalue>',
            r'<desc>(\d+(?:\.\d+)?)</desc>',
            r'(\d+(?:\.\d+)?)元',  # 元
            r'\xa5(\d+(?:\.\d+)?)',  # ¥ encoded
            r'"feedesc":"(\d+(?:\.\d+)?)"',
            r'"total_fee":"(\d+(?:\.\d+)?)"',
            r'"fee":"(\d+(?:\.\d+)?)"',
        ]
        for pat in patterns:
            m = re.search(pat, content)
            if m:
                amount = m.group(1)
                break

    dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
    session_name = contacts.get(session, session)

    results.append({
        'transfer_id': tid,
        'date': dt,
        'timestamp': ts,
        'session': session_name,
        'session_wxid': session,
        'direction': 'income' if is_income else 'outcome',
        'sub_type': stype,
        'amount': amount,
        'has_content': content is not None,
    })

    if content and not amount:
        raw_snippets.append({
            'transfer_id': tid,
            'session': session_name,
            'content_first_500': content[:500],
        })

conn.close()

# Output
output = {
    'extract_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total': len(results),
    'income_count': sum(1 for r in results if r['direction'] == 'income'),
    'outcome_count': sum(1 for r in results if r['direction'] == 'outcome'),
    'amount_found': sum(1 for r in results if r['amount']),
    'amount_missing': sum(1 for r in results if not r['amount']),
    'transfers': results,
    'debug_snippets': raw_snippets[:5],  # First 5 for debugging
}

# Save JSON
json_path = os.path.join(OUTPUT_DIR, 'transfers_with_amounts.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

# Print summary to stdout (ASCII-safe)
print(f"Total: {output['total']}")
print(f"Income: {output['income_count']}, Outcome: {output['outcome_count']}")
print(f"Amount found: {output['amount_found']}, Amount missing: {output['amount_missing']}")
print(f"Debug snippets: {len(raw_snippets)}")
print(f"Saved to: {json_path}")

# Print income summary
print("\n=== INCOME ===")
for r in results:
    if r['direction'] == 'income':
        amt = f"Y{r['amount']}" if r['amount'] else "(unknown)"
        print(f"  {r['date']} | {r['session']} | {amt}")

print("\n=== OUTCOME ===")
for r in results:
    if r['direction'] == 'outcome':
        amt = f"Y{r['amount']}" if r['amount'] else "(unknown)"
        print(f"  {r['date']} | {r['session']} | {amt}")
