# -*- coding: utf-8 -*-
"""全量数据提取：群成员 + 收入 + 联系人映射"""
import sqlite3, json, os, sys

# 设置stdout为utf-8
sys.stdout.reconfigure(encoding='utf-8')

CONTACT_DB = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\contact.db'
GENERAL_DB = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\general.db'
MSG_DB = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22\message_0.db'
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 1. 群成员提取
# ============================================================
print("=" * 60)
print("[Phase 1] 提取群成员信息...")
conn = sqlite3.connect(CONTACT_DB)

# 群列表 + 成员数
groups_raw = conn.execute('''
    SELECT cr.id, cr.username, cr.owner, count(cm.member_id) as cnt
    FROM chatroom_member cm
    JOIN chat_room cr ON cr.id = cm.room_id
    GROUP BY cr.username
    ORDER BY cnt DESC
''').fetchall()

# 联系人ID→信息映射
contacts = {}
for row in conn.execute('SELECT id, username, nick_name, remark, alias FROM contact'):
    cid, wxid, nick, remark, alias = row
    contacts[cid] = {
        'wxid': wxid,
        'nick_name': nick or '',
        'remark': remark or '',
        'alias': alias or '',
        'display': remark or nick or wxid
    }

# 提取每个群的成员详情
groups = {}
for room_id, username, owner, cnt in groups_raw:
    members = conn.execute('''
        SELECT c.id, c.username, c.nick_name, c.remark, c.alias
        FROM chatroom_member cm
        JOIN contact c ON c.id = cm.member_id
        WHERE cm.room_id = ?
    ''', (room_id,)).fetchall()

    member_list = []
    for mid, m_wxid, m_nick, m_remark, m_alias in members:
        member_list.append({
            'wxid': m_wxid,
            'nick_name': m_nick or '',
            'remark': m_remark or '',
            'alias': m_alias or '',
            'display': m_remark or m_nick or m_wxid
        })

    groups[username] = {
        'room_id': room_id,
        'username': username,
        'owner': owner,
        'member_count': cnt,
        'members': member_list
    }

conn.close()

# 保存群成员
group_members_path = os.path.join(OUTPUT_DIR, 'group_members_full.json')
with open(group_members_path, 'w', encoding='utf-8') as f:
    json.dump(groups, f, ensure_ascii=False, indent=2)
print(f"  群数量: {len(groups)}")
print(f"  总成员记录: {sum(g['member_count'] for g in groups.values())}")
print(f"  保存到: {group_members_path}")

# ============================================================
# 2. 收入数据提取
# ============================================================
print("\n[Phase 2] 提取收入数据...")
conn = sqlite3.connect(GENERAL_DB)

# 转账记录
print("  提取转账记录...")
transfer_cols = conn.execute('PRAGMA table_info(transferTable)').fetchall()
print(f"  transferTable 列: {[c[1] for c in transfer_cols]}")

transfers = conn.execute('SELECT * FROM transferTable').fetchall()
transfer_list = []
for row in transfers:
    record = {}
    for i, col in enumerate(transfer_cols):
        val = row[i]
        if isinstance(val, bytes):
            record[col[1]] = val.hex()
        else:
            record[col[1]] = val
    transfer_list.append(record)

transfer_path = os.path.join(OUTPUT_DIR, 'transfers_full.json')
with open(transfer_path, 'w', encoding='utf-8') as f:
    json.dump(transfer_list, f, ensure_ascii=False, indent=2, default=str)
print(f"  转账记录: {len(transfer_list)} 笔")

# 红包记录
print("  提取红包记录...")
env_cols = conn.execute('PRAGMA table_info(redEnvelopeTable)').fetchall()
print(f"  redEnvelopeTable 列: {[c[1] for c in env_cols]}")

envelopes = conn.execute('SELECT * FROM redEnvelopeTable').fetchall()
envelope_list = []
for row in envelopes:
    record = {}
    for i, col in enumerate(env_cols):
        val = row[i]
        if isinstance(val, bytes):
            record[col[1]] = val.hex()
        else:
            record[col[1]] = val
    envelope_list.append(record)

envelope_path = os.path.join(OUTPUT_DIR, 'envelopes_full.json')
with open(envelope_path, 'w', encoding='utf-8') as f:
    json.dump(envelope_list, f, ensure_ascii=False, indent=2, default=str)
print(f"  红包记录: {len(envelope_list)} 条")

conn.close()

# ============================================================
# 3. 联系人映射（Msg表名→wxid）
# ============================================================
print("\n[Phase 3] 建立Msg表名→联系人映射...")
import hashlib

conn_msg = sqlite3.connect(MSG_DB)
tables = conn_msg.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
msg_tables = [t[0] for t in tables if t[0].startswith('Msg_')]
conn_msg.close()

# 重新打开contact_db获取完整联系人
conn = sqlite3.connect(CONTACT_DB)
all_contacts = {}
for row in conn.execute('SELECT id, username, nick_name, remark, alias FROM contact'):
    cid, wxid, nick, remark, alias = row
    if wxid and '@' not in wxid:  # 排除系统账号
        all_contacts[wxid] = {
            'nick_name': nick or '',
            'remark': remark or '',
            'alias': alias or '',
            'display': remark or nick or wxid
        }
    elif wxid and '@chatroom' in wxid:
        all_contacts[wxid] = {
            'nick_name': nick or '',
            'remark': remark or '',
            'display': remark or nick or wxid
        }
conn.close()

# 用MD5匹配
table_mapping = {}
for table_name in msg_tables:
    suffix = table_name.replace('Msg_', '')
    for wxid, info in all_contacts.items():
        md5 = hashlib.md5(wxid.encode('utf-8')).hexdigest()
        if md5 == suffix:
            table_mapping[table_name] = {
                'wxid': wxid,
                'display': info['display'],
                'nick_name': info['nick_name'],
                'remark': info['remark']
            }
            break
    if table_name not in table_mapping:
        table_mapping[table_name] = {'wxid': suffix, 'display': 'UNKNOWN', 'nick_name': '', 'remark': ''}

mapping_path = os.path.join(OUTPUT_DIR, 'msg_table_mapping.json')
with open(mapping_path, 'w', encoding='utf-8') as f:
    json.dump(table_mapping, f, ensure_ascii=False, indent=2)

known = sum(1 for v in table_mapping.values() if v['display'] != 'UNKNOWN')
print(f"  Msg表总数: {len(msg_tables)}")
print(f"  已匹配: {known}")
print(f"  未匹配: {len(msg_tables) - known}")

# ============================================================
# 4. 汇总统计
# ============================================================
print("\n" + "=" * 60)
print("[完成] 全量数据提取完成")
print(f"  群成员: {group_members_path}")
print(f"  转账: {transfer_path} ({len(transfer_list)} 笔)")
print(f"  红包: {envelope_path} ({len(envelope_list)} 条)")
print(f"  表映射: {mapping_path} ({known}/{len(msg_tables)} 已匹配)")
