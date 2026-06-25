#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信聊天记录自动化分析脚本
基于同辈互助群数据，提供文风DNA优化、私域运营诊断、社群增长策略等服务

使用方式：
  python analyze_chat.py [--mode quick|detailed|voice|operation]

模式说明：
  quick: 快速诊断（默认）
  detailed: 详细分析
  voice: 文风DNA分析
  operation: 运营策略分析
"""

import sqlite3
import hashlib
import os
import re
import glob
import argparse
from datetime import datetime
from collections import defaultdict, Counter

try:
    import zstandard as zstd
except ImportError:
    zstd = None

# 配置
DB_PATH = r'E:\ai产出文件\牛马\创作\创作\output\databases\wxid_3nvidmluot0a22'
CONTACT_DB = os.path.join(DB_PATH, 'contact.db')
GROUP_WXID = '43423164031@chatroom'
OUTPUT_DIR = r'E:\ai产出文件\牛马\mutual\mutual\projects\proj-1779089173658-j5tg2m\outputs\wechat-groups'


def safe_decompress(data):
    """安全解压zstd数据"""
    if data is None:
        return ''
    try:
        if isinstance(data, bytes) and zstd:
            dctx = zstd.ZstdDecompressor()
            return dctx.decompress(data).decode('utf-8', errors='ignore')
    except Exception:
        pass
    return str(data) if data else ''


def ts_to_date(ts):
    """时间戳转日期时间"""
    try:
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
    except Exception:
        return str(ts)


def ts_to_day(ts):
    """时间戳转日期"""
    try:
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    except Exception:
        return str(ts)


def load_contacts():
    """加载联系人和群成员信息"""
    conn = sqlite3.connect(CONTACT_DB)
    contacts = {}
    for username, nick_name, remark in conn.execute(
        'SELECT username, nick_name, remark FROM contact'
    ):
        contacts[username] = {
            'nick_name': nick_name or '',
            'remark': remark or ''
        }

    room_info = conn.execute(
        "SELECT id FROM chat_room WHERE username=?", (GROUP_WXID,)
    ).fetchone()
    if not room_info:
        print(f"未找到群 {GROUP_WXID}")
        conn.close()
        return {}, contacts

    room_id = room_info[0]
    member_ids = [
        r[0] for r in conn.execute(
            "SELECT member_id FROM chatroom_member WHERE room_id=?",
            (room_id,)
        ).fetchall()
    ]

    members = {}
    if member_ids:
        placeholders = ','.join(['?' for _ in member_ids])
        for row in conn.execute(
            f'SELECT id, username, nick_name, remark FROM contact WHERE id IN ({placeholders})',
            member_ids
        ):
            members[row[0]] = {
                'username': row[1],
                'nick_name': row[2] or '',
                'remark': row[3] or ''
            }

    conn.close()
    return members, contacts


def load_messages():
    """加载消息数据"""
    hash_id = hashlib.md5(GROUP_WXID.encode()).hexdigest()
    table_name = f'Msg_{hash_id}'

    conn = None
    for db_file in sorted(glob.glob(os.path.join(DB_PATH, 'message_*.db'))):
        conn = sqlite3.connect(db_file)
        tables = [
            t[0] for t in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Msg_%'"
            ).fetchall()
        ]
        if table_name in tables:
            break
        conn.close()
        conn = None

    if conn is None:
        print(f"未找到消息表 {table_name}")
        return []

    rows = conn.execute(
        f'SELECT local_id, local_type, create_time, compress_content, message_content '
        f'FROM [{table_name}] ORDER BY create_time'
    ).fetchall()
    conn.close()
    return rows


TOPICS = {
    '求职与实习': ['offer', '简历', '实习', '求职', '面试', '投递', '找工作'],
    'AI工具': ['gemini', 'claude', 'ai', 'chatgpt', '提示词', 'cursor', 'deepseek', '知识库'],
    '竞赛与项目': ['竞赛', '比赛', '巡检', 'yolo', '视觉', '项目', '作品'],
    '内容变现': ['小红书', '公众号', '抖音', '知识付费', '变现'],
    '牛马AI': ['牛马', 'newmax', 'cc', 'claude code', 'mimo'],
    'PPT与设计': ['ppt', '排版', '图表'],
    '考研学习': ['考研', '期末', '复习', '绩点', '学习'],
}


def parse_messages(rows, contacts):
    """解析消息，返回发送者统计、每日消息、全部文本、按话题分组"""
    senders = Counter()
    daily_msgs = Counter()
    all_text = []
    topic_msgs = defaultdict(list)

    for row in rows:
        local_id, local_type, create_time, cc, mc = row
        content = safe_decompress(cc)
        msg = safe_decompress(mc)
        full_text = content or msg or ''
        day = ts_to_day(create_time)

        if local_type != 1 or not full_text.strip():
            continue

        m = re.match(r'(wxid_[a-z0-9]+)(?::|\\n)(.*)', full_text, re.DOTALL)
        if m:
            sender_wxid = m.group(1)
            info = contacts.get(sender_wxid, {})
            sender_name = info.get('remark') or info.get('nick_name') or sender_wxid
            text = m.group(2).strip()
        else:
            sender_name = '小黎'
            text = full_text.strip()

        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'eyJ[A-Za-z0-9+/=]+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        if not text:
            continue

        senders[sender_name] += 1
        daily_msgs[day] += 1
        entry = {'time': ts_to_date(create_time), 'day': day, 'sender': sender_name, 'text': text}
        all_text.append(entry)

        for topic, kws in TOPICS.items():
            if any(kw in text.lower() for kw in kws):
                topic_msgs[topic].append(entry)

    return senders, daily_msgs, all_text, topic_msgs


def analyze_voice_dna(my_msgs):
    """分析小黎的文风DNA"""
    analysis = {
        'sentence_patterns': Counter(),
        'tone_words': Counter(),
        'structure_markers': Counter(),
        'examples': []
    }

    for msg in my_msgs:
        text = msg['text']

        if '？' in text or '?' in text:
            analysis['sentence_patterns']['疑问句'] += 1
        if '！' in text or '!' in text:
            analysis['sentence_patterns']['感叹句'] += 1
        if '...' in text or '……' in text:
            analysis['sentence_patterns']['省略句'] += 1

        for word in ['是吧', '对吧', '没错', '可以', '行', '好', 'ok', 'OK']:
            if word in text.lower():
                analysis['tone_words'][word] += 1

        if text.startswith(('1.', '2.', '3.', '•', '-', '*')):
            analysis['structure_markers']['列表式'] += 1
        if len(text) > 100:
            analysis['structure_markers']['长段落'] += 1

        if 50 < len(text) < 200:
            analysis['examples'].append(text)

    return analysis


def analyze_operation(my_msgs, others_msgs):
    """分析运营策略"""
    operation = {
        'content_types': Counter(),
        'resource_sharing': [],
        'engagement_triggers': Counter(),
    }

    for msg in my_msgs:
        text = msg['text'].lower()

        if any(w in text for w in ['飞书', '知识库', 'github', '激活码']):
            operation['content_types']['资源分享'] += 1
        if any(w in text for w in ['嘉宾', '分享', '主讲', '计划']):
            operation['content_types']['活动策划'] += 1
        if any(w in text for w in ['面试', '求职', '简历', 'offer']):
            operation['content_types']['求职指导'] += 1
        if any(w in text for w in ['ai', 'gemini', 'claude', 'cursor']):
            operation['content_types']['AI工具'] += 1
        if any(w in text for w in ['学习', '考研', '绩点']):
            operation['content_types']['学习方法'] += 1

        if 'http' in text or 'www' in text:
            operation['resource_sharing'].append(msg)

        if '？' in text or '?' in text:
            operation['engagement_triggers']['提问'] += 1
        if any(w in text for w in ['大家可以', '建议', '推荐']):
            operation['engagement_triggers']['建议/推荐'] += 1

    others_engagement = Counter()
    for msg in others_msgs:
        text = msg['text'].lower()
        if any(w in text for w in ['谢谢', '感谢', '太棒了', '厉害']):
            others_engagement['感谢/认可'] += 1
        if any(w in text for w in ['请问', '怎么', '如何', '什么']):
            others_engagement['提问'] += 1
        if any(w in text for w in ['分享', '我也', '我之前']):
            others_engagement['经验分享'] += 1

    return operation, others_engagement


def generate_report(mode='quick'):
    """生成分析报告"""
    print("加载数据...")
    members, contacts = load_contacts()
    rows = load_messages()

    print("解析消息...")
    senders, daily_msgs, all_text, topic_msgs = parse_messages(rows, contacts)

    my_msgs = [m for m in all_text if m['sender'] == '小黎']
    others_msgs = [m for m in all_text if m['sender'] != '小黎']

    active_count = len([
        v for v in members.values()
        if senders.get(v['remark'] or v['nick_name'], 0) > 0
    ])

    print(f"\n分析完成:")
    print(f"  群成员数: {len(members)}")
    print(f"  总消息数: {len(all_text)}")
    print(f"  活跃成员: {active_count}")
    print(f"  小黎发言: {len(my_msgs)}")

    if mode == 'voice':
        print("\n--- 文风DNA分析 ---")
        voice = analyze_voice_dna(my_msgs)
        print(f"  疑问句: {voice['sentence_patterns'].get('疑问句', 0)} 次")
        print(f"  感叹句: {voice['sentence_patterns'].get('感叹句', 0)} 次")
        print(f"  列表式: {voice['structure_markers'].get('列表式', 0)} 次")
        print(f"  长段落: {voice['structure_markers'].get('长段落', 0)} 次")
        if voice['tone_words']:
            print(f"  高频语气词: {dict(voice['tone_words'].most_common(5))}")
        print(f"\n  典型语句示例 ({len(voice['examples'])} 条):")
        for i, ex in enumerate(voice['examples'][:5], 1):
            print(f"    {i}. {ex[:80]}...")

    elif mode == 'operation':
        print("\n--- 运营策略分析 ---")
        op, engagement = analyze_operation(my_msgs, others_msgs)
        print(f"  内容类型分布: {dict(op['content_types'].most_common())}")
        print(f"  资源分享次数: {len(op['resource_sharing'])}")
        print(f"  互动触发器: {dict(op['engagement_triggers'].most_common())}")
        print(f"  群友互动模式: {dict(engagement.most_common())}")

    else:
        print("\n--- 综合报告 ---")
        voice = analyze_voice_dna(my_msgs)
        op, engagement = analyze_operation(my_msgs, others_msgs)

        active_rate = active_count / len(members) * 100 if members else 0
        center_idx = len(my_msgs) / len(all_text) * 100 if all_text else 0

        print(f"  活跃率: {active_rate:.1f}%")
        print(f"  中心化指数: {center_idx:.1f}%")
        topic_dist = {t: len(msgs) for t, msgs in topic_msgs.items()}
        print(f"  话题分布: {dict(Counter(topic_dist).most_common(5))}")
        print(f"  活跃日期数: {len(daily_msgs)}")

        if mode == 'detailed':
            print("\n  文风简析:")
            print(f"    疑问句: {voice['sentence_patterns'].get('疑问句', 0)} 次")
            print(f"    高频语气词: {dict(voice['tone_words'].most_common(3))}")
            print(f"\n  运营简析:")
            print(f"    内容类型: {dict(op['content_types'].most_common(3))}")
            print(f"    群友互动: {dict(engagement.most_common(3))}")


def main():
    parser = argparse.ArgumentParser(description='微信聊天记录自动化分析')
    parser.add_argument(
        '--mode', choices=['quick', 'detailed', 'voice', 'operation'],
        default='quick', help='分析模式'
    )
    parser.add_argument(
        '--output', choices=['markdown', 'json'],
        default='markdown', help='输出格式'
    )
    args = parser.parse_args()

    print(f"开始分析 (模式: {args.mode})")
    generate_report(args.mode)
    print("\n分析完成!")


if __name__ == '__main__':
    main()
