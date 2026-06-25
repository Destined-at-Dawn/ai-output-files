"""
全量微信数据提取脚本 v2.0 — WCDB Schema
修复：使用正确的 WCDB 列名（local_id, create_time, real_sender_id, message_content等）
关键发现：
- 私聊中 real_sender_id=2 永远是你（小黎）
- 群聊中消息内容前缀为 sender_wxid:\n 格式
- zstd 压缩内容以 magic bytes \\x28\\xb5\\x2f\\xfd 开头

用法: python extract_full_data.py [--db-dir PATH] [--output PATH]
"""

import sqlite3, json, os, sys, hashlib, datetime, re
from collections import defaultdict

# ====== 配置 ======
DB_DIR = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22'
OUTPUT_DIR = r'E:\ai产出文件\牛马\创作\创作\output\wechat_analysis'
YOUR_WXID = 'wxid_3nvidmluot0a22'

# 尝试加载 zstd
try:
    import zstandard as zstd
    ZSTD_AVAILABLE = True
    dctx = zstd.ZstdDecompressor()
    ZSTD_MAGIC = b'\x28\xb5\x2f\xfd'
except ImportError:
    ZSTD_AVAILABLE = False
    ZSTD_MAGIC = b'\x28\xb5\x2f\xfd'

def decompress(msg_content):
    """解压 zstd 压缩内容"""
    if not ZSTD_AVAILABLE or not msg_content or not isinstance(msg_content, bytes):
        return msg_content
    try:
        if msg_content[:4] == ZSTD_MAGIC:
            return dctx.decompress(msg_content).decode('utf-8', errors='replace')
    except:
        pass
    return msg_content

def get_display_name(wxid, contact_map, chatroom_map):
    """获取联系人或群的显示名"""
    if '@chatroom' in str(wxid) or '@openim' in str(wxid):
        return chatroom_map.get(wxid, wxid)
    if wxid in contact_map:
        c = contact_map[wxid]
        return c.get('display') or c.get('remark') or c.get('nick_name') or wxid
    return wxid

def load_contacts(contact_db_path):
    """加载联系人映射"""
    if not os.path.exists(contact_db_path):
        print(f'[WARN] contact.db not found: {contact_db_path}')
        return {}, {}, {}

    conn = sqlite3.connect(contact_db_path)
    c = conn.cursor()

    # 1. contact 表
    contact_map = {}
    c.execute("SELECT id, username, alias, remark, nick_name, local_type FROM contact")
    for row in c.fetchall():
        id_, username, alias, remark, nick_name, local_type = row
        display = remark or alias or nick_name or username
        contact_map[username] = {
            'id': id_, 'username': username, 'alias': alias,
            'remark': remark, 'nick_name': nick_name, 'display': display,
        }

    # 2. chatroom_member
    c.execute("SELECT room_id, member_id FROM chatroom_member")
    chatroom_members = defaultdict(list)
    for room_id, member_id in c.fetchall():
        chatroom_members[room_id].append(member_id)

    # 3. chat_room
    chatroom_map = {}
    chat_rooms = {}
    c.execute("SELECT id, username, owner FROM chat_room")
    for id_, username, owner in c.fetchall():
        chat_rooms[id_] = (username, owner)
        chatroom_map[username] = contact_map.get(username, {}).get('display', username)

    # 4. 构建 member_id -> wxid 映射
    id_to_wxid = {}
    for wxid, info in contact_map.items():
        id_to_wxid[info['id']] = wxid

    # 5. 群成员
    group_members = {}
    for room_id, member_ids in chatroom_members.items():
        if room_id not in chat_rooms:
            continue
        room_username = chat_rooms[room_id][0]
        members = []
        for mid in member_ids:
            wxid = id_to_wxid.get(mid, f'unknown_{mid}')
            display = contact_map.get(wxid, {}).get('display', wxid)
            members.append({'wxid': wxid, 'display': display})
        group_members[room_username] = members

    conn.close()
    print(f'[OK] Contacts: {len(contact_map)}, ChatRooms: {len(chat_rooms)}, Members: {sum(len(v) for v in group_members.values())}')
    return contact_map, chatroom_map, group_members

def load_financial(general_db_path):
    """加载转账和红包记录"""
    if not os.path.exists(general_db_path):
        return [], []

    conn = sqlite3.connect(general_db_path)
    c = conn.cursor()

    c.execute('SELECT transfer_id, session_name, pay_sub_type, pay_receiver, pay_payer, begin_transfer_time FROM transferTable')
    transfers = []
    for row in c.fetchall():
        tid, sess, pst, receiver, payer, begin_time = row
        transfers.append({
            'transfer_id': tid, 'session': sess, 'sub_type': pst,
            'receiver': receiver, 'payer': payer,
            'time': datetime.datetime.fromtimestamp(begin_time).strftime('%Y-%m-%d %H:%M'),
            'is_income': receiver == YOUR_WXID,
        })

    c.execute('SELECT message_server_id, session_name, sender_user_name, hb_status, hb_type, receive_status FROM redEnvelopeTable')
    red_envelopes = []
    for row in c.fetchall():
        mid, sess, sender, status, hb_type, recv_status = row
        red_envelopes.append({
            'msg_id': mid, 'session': sess, 'sender': sender,
            'hb_status': status, 'hb_type': hb_type, 'receive_status': recv_status,
            'is_from_me': sender == YOUR_WXID,
        })

    conn.close()
    print(f'[OK] Transfers: {len(transfers)}, RedEnvelopes: {len(red_envelopes)}')
    return transfers, red_envelopes

def extract_session_stats(msg_db_path, contact_map, chatroom_map):
    """提取所有会话统计 - WCDB Schema"""
    if not os.path.exists(msg_db_path):
        return {}

    conn = sqlite3.connect(msg_db_path)
    c = conn.cursor()

    c.execute("SELECT user_name, is_session FROM Name2Id")
    name2id = {row[0]: row[1] for row in c.fetchall()}

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Msg_%'")
    msg_tables = set(r[0] for r in c.fetchall())

    sessions = {}

    for user_name in name2id:
        h = hashlib.md5(user_name.encode()).hexdigest()
        table_name = f'Msg_{h}'
        if table_name not in msg_tables:
            continue

        try:
            c.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            msg_count = c.fetchone()[0]
            if msg_count == 0:
                continue

            # 时间范围 (使用 create_time)
            c.execute(f'SELECT MAX(create_time), MIN(create_time) FROM "{table_name}"')
            max_ts, min_ts = c.fetchone()
            if max_ts is None or min_ts is None:
                continue

            is_group = '@chatroom' in user_name

            # 发言统计
            c.execute(f'SELECT real_sender_id, COUNT(*) FROM "{table_name}" GROUP BY real_sender_id')
            sender_counts = dict(c.fetchall())

            # 私聊: sender_id=2 是你
            your_msgs = sender_counts.get(2, 0)
            other_msgs = msg_count - your_msgs

            # 文本消息统计
            c.execute(f'SELECT COUNT(*) FROM "{table_name}" WHERE local_type = 1')
            text_count = c.fetchone()[0]

            # 平均文本长度
            avg_len = 0
            if text_count > 0:
                c.execute(f'SELECT AVG(LENGTH(message_content)) FROM "{table_name}" WHERE local_type = 1 AND message_content IS NOT NULL AND message_content != \'\'')
                result = c.fetchone()[0]
                avg_len = result or 0

            display = get_display_name(user_name, contact_map, chatroom_map)
            days_span = max(1, (max_ts - min_ts) / 86400 + 1)

            # 提取群聊中的发言人
            group_senders = {}
            if is_group and ZSTD_AVAILABLE:
                try:
                    c.execute(f'''SELECT message_content, compress_content, real_sender_id, local_type
                                  FROM "{table_name}" WHERE local_type = 1
                                  AND (message_content IS NOT NULL OR compress_content IS NOT NULL)
                                  LIMIT 5000''')
                    for row in c.fetchall():
                        content = row[0]
                        compressed = row[1]
                        # 尝试从 message_content 提取 sender
                        if content:
                            # 群聊消息格式: "wxid:\nmessage" 或 "wxid: message"
                            if isinstance(content, bytes):
                                content = content.decode('utf-8', errors='replace')

                            # 解压 compress_content
                            if compressed and isinstance(compressed, bytes):
                                try:
                                    if compressed[:4] == ZSTD_MAGIC:
                                        content = dctx.decompress(compressed).decode('utf-8', errors='replace')
                                except:
                                    pass

                            if content and ':\n' in content[:100]:
                                parts = content.split(':\n', 1)
                                sender = parts[0]
                                group_senders[sender] = group_senders.get(sender, 0) + 1
                except Exception as e:
                    pass

            sessions[user_name] = {
                'display': display,
                'raw_name': user_name,
                'is_group': is_group,
                'total_msgs': msg_count,
                'your_msgs': your_msgs,
                'other_msgs': other_msgs,
                'text_msgs': text_count,
                'avg_text_len': round(avg_len, 1),
                'first_msg': datetime.datetime.fromtimestamp(min_ts).strftime('%Y-%m-%d') if min_ts else 'N/A',
                'last_msg': datetime.datetime.fromtimestamp(max_ts).strftime('%Y-%m-%d %H:%M') if max_ts else 'N/A',
                'days_span': int(days_span),
                'daily_avg': round(msg_count / days_span, 1),
                'table_name': table_name,
                'group_senders_top': dict(sorted(group_senders.items(), key=lambda x: x[1], reverse=True)[:10]),
                'sender_counts': sender_counts,
            }
        except Exception as e:
            print(f'  [SKIP] {table_name} ({user_name[:30]}): {e}')

    conn.close()
    return sessions

def extract_corpus(msg_db_path, sessions, max_per_session=500):
    """提取用户语料 - WCDB Schema"""
    conn = sqlite3.connect(msg_db_path)
    c = conn.cursor()
    all_msgs = []

    for user_name, sess_info in sessions.items():
        if sess_info['total_msgs'] < 10:
            continue
        table_name = sess_info['table_name']

        try:
            # 私聊: sender_id=2 是你的消息
            if not sess_info['is_group']:
                c.execute(f'''
                    SELECT create_time, message_content, compress_content, local_type
                    FROM "{table_name}"
                    WHERE real_sender_id = 2 AND local_type = 1
                    AND (message_content IS NOT NULL OR compress_content IS NOT NULL)
                    ORDER BY create_time DESC
                    LIMIT {max_per_session}
                ''')
            else:
                # 群聊: 取所有文本消息
                c.execute(f'''
                    SELECT create_time, message_content, compress_content, local_type
                    FROM "{table_name}"
                    WHERE local_type = 1
                    AND (message_content IS NOT NULL OR compress_content IS NOT NULL)
                    ORDER BY create_time DESC
                    LIMIT {max_per_session}
                ''')

            for ts, content, compressed, ltype in c.fetchall():
                # 解压
                text = content
                if isinstance(text, bytes):
                    text = text.decode('utf-8', errors='replace')
                if compressed and isinstance(compressed, bytes):
                    try:
                        if compressed[:4] == ZSTD_MAGIC and ZSTD_AVAILABLE:
                            text = dctx.decompress(compressed).decode('utf-8', errors='replace')
                    except:
                        pass
                if not text:
                    continue

                # 群聊消息去掉前缀 sender_id:
                if sess_info['is_group'] and ':\n' in (text or '')[:100]:
                    parts = text.split(':\n', 1)
                    if len(parts) == 2:
                        text = parts[1]

                all_msgs.append({
                    'time': datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M'),
                    'content': text,
                    'session': sess_info['display'],
                    'is_group': sess_info['is_group'],
                })
        except Exception as e:
            pass

    conn.close()
    return all_msgs

def analyze_transfers(transfers, contact_map, chatroom_map):
    """分析转账记录"""
    income, outcome = [], []
    for t in transfers:
        session_display = get_display_name(t['session'], contact_map, chatroom_map)
        record = {**t, 'session_display': session_display}
        (income if t['is_income'] else outcome).append(record)

    income_by_session = defaultdict(list)
    for t in income:
        income_by_session[t['session_display']].append(t)

    return {
        'income_count': len(income), 'outcome_count': len(outcome),
        'income_by_session': {k: len(v) for k, v in income_by_session.items()},
        'income_details': income, 'outcome_details': outcome,
    }

def generate_report(sessions, top_private, top_groups, transfer_analysis, group_members):
    """生成 Markdown 格式数据摘要"""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    total_msgs = sum(s['total_msgs'] for s in sessions.values())
    private = {k: v for k, v in sessions.items() if not v['is_group']}
    groups = {k: v for k, v in sessions.items() if v['is_group']}

    lines = [
        f'# 微信数据全量提取报告',
        f'> 提取时间: {now}',
        f'> 数据截止: 2026-06-07（待更新至最新）',
        f'',
        f'## 总览',
        f'| 指标 | 数值 |',
        f'|------|------|',
        f'| 总会话数 | {len(sessions)} |',
        f'| 私聊会话 | {len(private)} |',
        f'| 群聊会话 | {len(groups)} |',
        f'| 总消息数 | {total_msgs:,} |',
        f'| 转账收入 | {transfer_analysis["income_count"]} 笔 |',
        f'| 转账支出 | {transfer_analysis["outcome_count"]} 笔 |',
        f'',
        f'## Top 20 私聊',
        f'| 排名 | 联系人 | 消息数 | 你发 | 日均 | 首条 | 末条 |',
        f'|------|--------|--------|------|------|------|------|',
    ]
    for i, (wxid, info) in enumerate(top_private, 1):
        d = info['display']; t = info['total_msgs']; y = info['your_msgs']
        da = info['daily_avg']; f = info['first_msg']; l = info['last_msg']
        lines.append(f'| {i} | {d} | {t:,} | {y:,} | {da:.1f} | {f} | {l} |')

    lines.extend([
        f'## Top 20 群聊',
        f'| 排名 | 群名 | 消息数 | 你发 | 日均 | 首条 | 末条 |',
        f'|------|------|--------|------|------|------|------|',
    ])
    for i, (wxid, info) in enumerate(top_groups, 1):
        d = info['display']; t = info['total_msgs']; y = info['your_msgs']
        da = info['daily_avg']; f = info['first_msg']; l = info['last_msg']
        lines.append(f'| {i} | {d} | {t:,} | {y:,} | {da:.1f} | {f} | {l} |')

    lines.extend([
        f'## 收入记录（转账）',
        f'| 联系人 | 笔数 |',
        f'|--------|------|',
    ])
    for session, count in sorted(transfer_analysis['income_by_session'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f'| {session} | {count} |')

    lines.extend([
        f'## 群成员统计（Top 20）',
        f'| 群名 | 人数 |',
        f'|------|------|',
    ])
    for display, info in sorted(group_members.items(), key=lambda x: x[1]['member_count'], reverse=True)[:20]:
        mc = info['member_count']
        lines.append(f'| {display} | {mc} |')

    lines.append(f'\n---\n*由 extract_full_data.py v2.0 自动生成*')
    return '\n'.join(lines)

def main():
    msg_db = os.path.join(DB_DIR, 'message_0.db')
    contact_db = os.path.join(DB_DIR, 'contact.db')
    general_db = os.path.join(DB_DIR, 'general.db')
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print('=' * 60)
    print('微信全量数据提取 v2.0 (WCDB Schema)')
    print(f'数据源: {DB_DIR}')
    print(f'zstd 可用: {ZSTD_AVAILABLE}')
    print('=' * 60)

    print('\n[1/5] 加载联系人 & 群成员...')
    contact_map, chatroom_map, group_members = load_contacts(contact_db)

    print('\n[2/5] 加载转账 & 红包...')
    transfers, red_envelopes = load_financial(general_db)
    transfer_analysis = analyze_transfers(transfers, contact_map, chatroom_map)

    print('\n[3/5] 提取会话统计...')
    sessions = extract_session_stats(msg_db, contact_map, chatroom_map)

    private_sessions = {k: v for k, v in sessions.items() if not v['is_group']}
    group_sessions = {k: v for k, v in sessions.items() if v['is_group']}
    top_private = sorted(private_sessions.items(), key=lambda x: x[1]['total_msgs'], reverse=True)[:20]
    top_groups = sorted(group_sessions.items(), key=lambda x: x[1]['total_msgs'], reverse=True)[:20]

    print('\n[4/5] 提取用户语料...')
    corpus = extract_corpus(msg_db, sessions, max_per_session=300)

    print('\n[5/5] 写入输出文件...')

    # all_sessions.json
    all_sessions_list = [{
        'wxid': wxid, 'display': info['display'], 'is_group': info['is_group'],
        'total_msgs': info['total_msgs'], 'your_msgs': info['your_msgs'],
        'daily_avg': info['daily_avg'], 'first_msg': info['first_msg'],
        'last_msg': info['last_msg'], 'days_span': info['days_span'],
    } for wxid, info in sessions.items()]

    with open(os.path.join(OUTPUT_DIR, 'all_sessions.json'), 'w', encoding='utf-8') as f:
        json.dump(all_sessions_list, f, ensure_ascii=False, indent=2)
    print(f'  [OK] all_sessions.json ({len(all_sessions_list)} sessions)')

    with open(os.path.join(OUTPUT_DIR, 'top_private.json'), 'w', encoding='utf-8') as f:
        json.dump([{'wxid': w, **i} for w, i in top_private], f, ensure_ascii=False, indent=2)
    print(f'  [OK] top_private.json')

    with open(os.path.join(OUTPUT_DIR, 'top_groups.json'), 'w', encoding='utf-8') as f:
        json.dump([{'wxid': w, **i} for w, i in top_groups], f, ensure_ascii=False, indent=2)
    print(f'  [OK] top_groups.json')

    with open(os.path.join(OUTPUT_DIR, 'transfers.json'), 'w', encoding='utf-8') as f:
        json.dump(transfer_analysis, f, ensure_ascii=False, indent=2)
    print(f'  [OK] transfers.json')

    # 群成员（简化版）
    gm_summary = {}
    for room_username, members in group_members.items():
        display = get_display_name(room_username, contact_map, chatroom_map)
        gm_summary[display] = {
            'username': room_username, 'member_count': len(members),
            'members': members[:100],
        }
    with open(os.path.join(OUTPUT_DIR, 'group_members.json'), 'w', encoding='utf-8') as f:
        json.dump(gm_summary, f, ensure_ascii=False, indent=2)
    print(f'  [OK] group_members.json ({len(gm_summary)} groups)')

    with open(os.path.join(OUTPUT_DIR, 'corpus.json'), 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    print(f'  [OK] corpus.json ({len(corpus)} messages)')

    # MD 报告
    report = generate_report(sessions, top_private, top_groups, transfer_analysis, gm_summary)
    with open(os.path.join(OUTPUT_DIR, 'data_summary.md'), 'w', encoding='utf-8') as f:
        f.write(report)
    print(f'  [OK] data_summary.md')

    total_msgs = sum(s['total_msgs'] for s in sessions.values())
    print(f'\n===== 完成 =====')
    print(f'私聊: {len(private_sessions)}, 群聊: {len(group_sessions)}, 总消息: {total_msgs:,}')
    ic = transfer_analysis['income_count']; oc = transfer_analysis['outcome_count']
    re_cnt = len(red_envelopes)
    print(f'转账收入: {ic} 笔, 支出: {oc} 笔, 红包: {re_cnt} 条')
    print(f'输出目录: {OUTPUT_DIR}')

if __name__ == '__main__':
    for i, arg in enumerate(sys.argv):
        if arg == '--db-dir' and i + 1 < len(sys.argv):
            DB_DIR = sys.argv[i + 1]
        elif arg == '--output' and i + 1 < len(sys.argv):
            OUTPUT_DIR = sys.argv[i + 1]
    main()
