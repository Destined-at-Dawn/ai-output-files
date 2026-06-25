#!/usr/bin/env python3
"""
WeChat Chat Log Analyzer
================================
Reads decrypted WeChat databases and generates structured summary reports.

Usage:
    python analyze_wechat.py --db-dir "C:\path\to\decrypted" --out-dir "E:\output"

Input: Directory containing decrypted message_0.db, session.db, contact.db
Output: MD + JSON summary reports

Author: Newmax AI (2026-06-07)
Source: 1780809307229-Pasted-8.txt Section 7
"""

import os
import re
import json
import sqlite3
import hashlib
import argparse
from datetime import datetime
from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CATEGORIES = {
    "待办/请求/截止": [
        "帮我", "麻烦", "需要", "能不能", "可以吗",
        "安排", "截止", "ddl", "DDL", "提交", "报名",
        "提醒", "明天", "今天", "今晚", "下周",
        "尽快", "记得", "发我", "给我", "确认", "通知"
    ],
    "学习/课程/考试/作业": [
        "考试", "作业", "课程", "上课", "复习",
        "预习", "老师", "课堂", "绩点", "GPA",
        "论文", "文献", "课设", "实验", "报告",
        "题目", "答案", "高考", "考研", "学习", "笔记"
    ],
    "AI/代码/项目/工具": [
        "AI", "agent", "Agent", "GPT", "Claude", "Codex", "prompt", "提示词",
        "代码", "项目", "GitHub", "github", "仓库", "脚本",
        "数据库", "Python", "模型", "自动化", "知识库",
        "飞书", "Notion"
    ],
    "竞赛/机器人/电气": [
        "ROS", "机器人", "竞赛", "电控", "视觉",
        "机械", "调试", "仿真", "电气", "集成电路",
        "硬件", "PCB", "单片机", "传感器", "队长", "比赛"
    ],
    "文件/链接/资料": [
        "http://", "https://", "www.", "链接", "文件", "文档",
        "资料", "PDF", "图片", "视频", "网盘",
        "飞书", "腾讯文档", "附件"
    ],
    "生活/社交/杂事": [
        "吃饭", "宿舍", "快递", "外卖", "睡觉",
        "明天见", "哈哈", "笑死", "可以", "好的",
        "谢谢", "没事", "回去", "学校", "班级", "群聊"
    ],
    "交易/钱/兼职": [
        "钱", "付款", "收款", "红包", "转账",
        "订单", "价格", "兼职", "副业", "工资",
        "预算", "买", "卖", "支付"
    ],
}

STOP_WORDS = set("""
这个 那个 一个 一下 不是 没有 可以 还是
什么 怎么 就是 现在 今天 明天 我们 你们 他们
自己 真的 可能 因为 所以 然后 如果 但是
直接 已经 还有 这样 这里 那里
""".split())

TYPE_NAME = {
    1: "文本",
    3: "图片",
    34: "语音",
    43: "视频",
    47: "表情",
    48: "位置",
    49: "链接/文件/卡片/合并转发",
    50: "通话",
    10000: "系统",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ts(value):
    """Convert Unix timestamp to human-readable string."""
    try:
        if not value:
            return ""
        return datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(value)


def clean_text(s, limit=180):
    """Clean message content: strip XML, collapse whitespace, truncate."""
    if s is None:
        return ""
    if isinstance(s, bytes):
        try:
            s = s.decode("utf-8", errors="ignore")
        except Exception:
            s = ""
    s = str(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > limit:
        s = s[:limit] + "..."
    return s


def table_for_username(username):
    """Map WeChat username to Msg_<md5> table name."""
    return "Msg_" + hashlib.md5(username.encode("utf-8")).hexdigest()


def safe_sql_name(name):
    """Quote SQL identifier safely."""
    return "[" + name.replace("]", "]]") + "]"


# ---------------------------------------------------------------------------
# Core Analysis
# ---------------------------------------------------------------------------

def analyze(db_dir, out_dir, report_date, top_n=30):
    """Main analysis pipeline."""
    os.makedirs(out_dir, exist_ok=True)

    msg_db = os.path.join(db_dir, "message_0.db")
    session_db = os.path.join(db_dir, "session.db")
    contact_db = os.path.join(db_dir, "contact.db")

    report_md = os.path.join(out_dir, f"wechat_chat_summary_{report_date}.md")
    report_json = os.path.join(out_dir, f"wechat_chat_summary_{report_date}.json")

    # ------------------------------------------------------------------
    # Connect to databases
    # ------------------------------------------------------------------
    msg_con = sqlite3.connect(msg_db)
    msg_con.row_factory = sqlite3.Row
    session_con = sqlite3.connect(session_db)
    session_con.row_factory = sqlite3.Row
    contact_con = sqlite3.connect(contact_db)
    contact_con.row_factory = sqlite3.Row

    # ------------------------------------------------------------------
    # Discover Msg_* tables
    # ------------------------------------------------------------------
    msg_tables = {
        r[0] for r in msg_con.execute(
            "select name from sqlite_master where type='table' and name like 'Msg_%'"
        )
    }

    # ------------------------------------------------------------------
    # Load contacts for display name resolution
    # ------------------------------------------------------------------
    contacts = {}
    try:
        for r in contact_con.execute(
            "select username, remark, nick_name, alias, verify_flag from contact"
        ):
            display = (r["remark"] or r["nick_name"] or r["alias"] or r["username"] or "").strip()
            contacts[r["username"]] = {
                "display": display,
                "verify_flag": r["verify_flag"],
            }
    except Exception:
        pass

    # ------------------------------------------------------------------
    # Load sessions from session.db
    # ------------------------------------------------------------------
    sessions = []
    for r in session_con.execute("""
        select username, type, unread_count, summary, last_timestamp, sort_timestamp,
               last_msg_type, last_msg_sender, last_sender_display_name
        from SessionTable
        order by last_timestamp desc
    """):
        username = r["username"]
        if not username or username.startswith("@placeholder"):
            continue
        table = table_for_username(username)
        if table not in msg_tables:
            continue
        c = contacts.get(username, {})
        display = c.get("display") or username
        kind = (
            "群聊" if username.endswith("@chatroom")
            else "公众号/服务号" if username.startswith("gh_")
            else "个人/其他"
        )
        sessions.append({
            "username": username,
            "display": display,
            "kind": kind,
            "table": table,
            "unread_count": int(r["unread_count"] or 0),
            "summary": clean_text(r["summary"], 120),
            "last_timestamp": int(r["last_timestamp"] or 0),
            "last_time": ts(r["last_timestamp"]),
            "last_sender_display_name": r["last_sender_display_name"] or "",
        })

    # ------------------------------------------------------------------
    # Initialize accumulators
    # ------------------------------------------------------------------
    overall = {
        "session_count": len(sessions),
        "message_total": 0,
        "text_total": 0,
        "type_counter": Counter(),
        "first_time": None,
        "last_time": None,
    }

    category_hits = {
        cat: {"message_count": 0, "session_counter": Counter(), "snippets": []}
        for cat in CATEGORIES
    }
    session_summaries = []
    keyword_counter = Counter()

    # ------------------------------------------------------------------
    # Scan every session's message table
    # ------------------------------------------------------------------
    for idx, s in enumerate(sessions, 1):
        table = s["table"]
        qtable = safe_sql_name(table)
        try:
            cnt = msg_con.execute(f"select count(*) from {qtable}").fetchone()[0]
            bounds = msg_con.execute(
                f"select min(create_time), max(create_time) from {qtable}"
            ).fetchone()
        except Exception:
            continue

        s["message_count"] = int(cnt or 0)
        s["first_time"] = ts(bounds[0])
        s["last_msg_time"] = ts(bounds[1])
        overall["message_total"] += int(cnt or 0)

        if bounds[0] and (overall["first_time"] is None or bounds[0] < overall["first_time"]):
            overall["first_time"] = bounds[0]
        if bounds[1] and (overall["last_time"] is None or bounds[1] > overall["last_time"]):
            overall["last_time"] = bounds[1]

        per_type = Counter()
        text_count = 0
        recent_text = []

        rows = msg_con.execute(f"""
            select local_type, create_time, real_sender_id, message_content, compress_content
            from {qtable}
            order by create_time desc
        """)
        for row_i, r in enumerate(rows):
            lt = int(r["local_type"] or 0)
            per_type[lt] += 1
            overall["type_counter"][lt] += 1

            text = clean_text(r["message_content"], 220)
            if text:
                text_count += 1
                if len(recent_text) < 5:
                    recent_text.append({
                        "time": ts(r["create_time"]),
                        "text": text,
                    })

                # Keyword extraction
                for word in re.findall(r"[一-鿿A-Za-z0-9_+#.-]{2,}", text):
                    if word not in STOP_WORDS and len(word) <= 18:
                        keyword_counter[word] += 1

                # Category matching
                for cat, kws in CATEGORIES.items():
                    if any(kw in text for kw in kws):
                        category_hits[cat]["message_count"] += 1
                        category_hits[cat]["session_counter"][s["display"]] += 1
                        if len(category_hits[cat]["snippets"]) < 18:
                            category_hits[cat]["snippets"].append({
                                "session": s["display"],
                                "kind": s["kind"],
                                "time": ts(r["create_time"]),
                                "text": text,
                            })

        s["text_count"] = text_count
        s["type_counter"] = dict(per_type)
        s["recent_text"] = recent_text
        session_summaries.append(s)

    # ------------------------------------------------------------------
    # Compute derived stats
    # ------------------------------------------------------------------
    overall["text_total"] = sum(s.get("text_count", 0) for s in session_summaries)
    overall["first_time_text"] = ts(overall["first_time"])
    overall["last_time_text"] = ts(overall["last_time"])
    overall["type_counter_named"] = {
        TYPE_NAME.get(k, str(k)): v
        for k, v in overall["type_counter"].most_common()
    }

    top_active = sorted(
        session_summaries, key=lambda x: x.get("message_count", 0), reverse=True
    )[:top_n]
    top_unread = sorted(
        [s for s in session_summaries if s.get("unread_count", 0) > 0],
        key=lambda x: x["unread_count"], reverse=True
    )[:top_n]
    top_keywords = keyword_counter.most_common(80)

    # ------------------------------------------------------------------
    # Build result
    # ------------------------------------------------------------------
    result = {
        "overall": overall,
        "top_active": top_active,
        "top_unread": top_unread,
        "categories": {
            cat: {
                "message_count": data["message_count"],
                "top_sessions": data["session_counter"].most_common(12),
                "snippets": data["snippets"],
            }
            for cat, data in category_hits.items()
        },
        "top_keywords": top_keywords,
    }

    # ------------------------------------------------------------------
    # Write JSON
    # ------------------------------------------------------------------
    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Write Markdown report
    # ------------------------------------------------------------------
    lines = []
    lines.append(f"# 微信聊天记录分类汇总报告（自动提取）")
    lines.append("")
    lines.append("## 总览")
    lines.append("")
    lines.append(f"- 会话数：{overall['session_count']}")
    lines.append(f"- 消息总数：{overall['message_total']}")
    lines.append(f"- 可解析文本/内容消息数：{overall['text_total']}")
    lines.append(f"- 时间范围：{overall['first_time_text']} ~ {overall['last_time_text']}")
    lines.append("")
    lines.append("## 消息类型分布")
    lines.append("")
    for name, count in overall["type_counter_named"].items():
        lines.append(f"- {name}: {count}")
    lines.append("")

    lines.append(f"## 最活跃会话 Top {top_n}")
    lines.append("")
    for i, s in enumerate(top_active, 1):
        lines.append(f"{i}. {s['display']}（{s['kind']}）")
        lines.append(f"   - 消息数：{s.get('message_count', 0)}；未读：{s.get('unread_count', 0)}；最近：{s.get('last_msg_time', '')}")
        if s.get("summary"):
            lines.append(f"   - 最近摘要：{s['summary']}")
        if s.get("recent_text"):
            lines.append(f"   - 近期片段：{s['recent_text'][0]['text']}")
    lines.append("")

    lines.append(f"## 未读/待处理会话 Top {top_n}")
    lines.append("")
    if top_unread:
        for i, s in enumerate(top_unread, 1):
            lines.append(f"{i}. {s['display']}（{s['kind']}）")
            lines.append(f"   - 未读：{s.get('unread_count', 0)}；最近：{s.get('last_time', '')}")
            if s.get("summary"):
                lines.append(f"   - 摘要：{s['summary']}")
    else:
        lines.append("- 未发现未读会话。")
    lines.append("")

    lines.append("## 主题分类")
    lines.append("")
    for cat, data in result["categories"].items():
        lines.append(f"### {cat}")
        lines.append("")
        lines.append(f"- 命中消息数：{data['message_count']}")
        if data["top_sessions"]:
            lines.append("- 主要会话：")
            for name, count in data["top_sessions"][:8]:
                lines.append(f"  - {name}: {count}")
        if data["snippets"]:
            lines.append("- 代表片段：")
            for sn in data["snippets"][:8]:
                lines.append(f"  - {sn['time']}｜{sn['session']}｜{sn['text']}")
        lines.append("")

    lines.append("## 高频词 Top 80")
    lines.append("")
    for word, count in top_keywords:
        lines.append(f"- {word}: {count}")
    lines.append("")

    lines.append("## 后续建议")
    lines.append("")
    lines.append("- 先看“未读/待处理会话”和“待办/请求/截止”，这是最有行动价值的部分。")
    lines.append("- 如果要做更精细总结，下一步可以对某个高价值会话单独导出最近 500 条文本，再做人工/AI摘要。")
    lines.append("- 当前报告只做本地离线分析，没有调用外部大模型上传聊天内容。")

    with open(report_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Close connections
    msg_con.close()
    session_con.close()
    contact_con.close()

    return report_md, report_json, result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="WeChat Chat Log Analyzer - Generate summary reports from decrypted DB"
    )
    parser.add_argument(
        "--db-dir", required=True,
        help="Path to directory containing decrypted message_0.db, session.db, contact.db"
    )
    parser.add_argument(
        "--out-dir", default="./output",
        help="Output directory for reports (default: ./output)"
    )
    parser.add_argument(
        "--date", default=datetime.now().strftime("%Y%m%d"),
        help="Date string for report filename (default: today YYYYMMDD)"
    )
    parser.add_argument(
        "--top-n", type=int, default=30,
        help="Number of top sessions to show (default: 30)"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.db_dir):
        print(f"ERROR: DB directory not found: {args.db_dir}")
        print("Expected files: message_0.db, session.db, contact.db")
        return 1

    required = ["message_0.db", "session.db", "contact.db"]
    missing = [f for f in required if not os.path.isfile(os.path.join(args.db_dir, f))]
    if missing:
        print(f"ERROR: Missing required DB files: {missing}")
        return 1

    print(f"Analyzing databases in: {args.db_dir}")
    print(f"Output directory: {args.out_dir}")
    print(f"Report date: {args.date}")
    print(f"Top N: {args.top_n}")
    print()

    md_path, json_path, result = analyze(args.db_dir, args.out_dir, args.date, args.top_n)

    print(f"Done! Reports written:")
    print(f"  MD   : {md_path} ({os.path.getsize(md_path):,} bytes)")
    print(f"  JSON : {json_path} ({os.path.getsize(json_path):,} bytes)")
    print()
    print(f"Sessions: {result['overall']['session_count']}")
    print(f"Messages: {result['overall']['message_total']}")
    print(f"Time range: {result['overall']['first_time_text']} ~ {result['overall']['last_time_text']}")

    return 0


if __name__ == "__main__":
    exit(main())
