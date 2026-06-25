#!/usr/bin/env python3
"""
文风DNA提取 + 人格蒸馏分析
=============================
Analyzes exported chat text to extract:
1. 小黎's 文风DNA (writing style fingerprint)
2. Camellia and 米蛋糕's psychological profiles (distillation)

Input: chat_{name}_plain.txt from v5 export
Output: personality_profiles/ directory with analysis reports
"""
import os, re, json
from collections import Counter, defaultdict
from datetime import datetime

CHAT_DIR = r"E:\ai产出文件\牛马\创作\创作\output\wechat_exports_v5"
OUTPUT_DIR = r"E:\ai产出文件\牛马\创作\创作\output\personality_profiles"

# Chinese punctuation
CN_PUNCT = set("，。！？、；：""''（）【】《》…—～·")

def load_messages(plain_path):
    """Load plain text chat messages, grouped by sender."""
    messages = defaultdict(list)
    current_sender = None

    with open(plain_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('---'):
                continue
            # Format: "[HH:MM:SS] SenderName: message"
            match = re.match(r'\[([^\]]+)\]\s+([^:]+):\s*(.*)', line)
            if match:
                timestamp = match.group(1)
                sender = match.group(2).strip()
                text = match.group(3).strip()
                if text:
                    messages[sender].append({
                        'time': timestamp,
                        'text': text
                    })
    return messages

def analyze_sender(name, msgs):
    """Comprehensive analysis of one sender's messages."""
    if not msgs:
        return {}

    texts = [m['text'] for m in msgs]

    # 1. Basic stats
    total_msgs = len(texts)
    total_chars = sum(len(t) for t in texts)
    avg_length = total_chars / total_msgs if total_msgs > 0 else 0

    # 2. Sentence structure
    sentence_lengths = []
    for t in texts:
        # Split by Chinese/English punctuation
        sentences = re.split(r'[。！？!?\n]+', t)
        for s in sentences:
            s = s.strip()
            if s:
                sentence_lengths.append(len(s))

    avg_sentence_len = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

    # 3. Message length distribution
    len_bins = {"极短(<10字)": 0, "短(10-30字)": 0, "中(30-80字)": 0, "长(80-200字)": 0, "超长(>200字)": 0}
    for t in texts:
        l = len(t)
        if l < 10: len_bins["极短(<10字)"] += 1
        elif l < 30: len_bins["短(10-30字)"] += 1
        elif l < 80: len_bins["中(30-80字)"] += 1
        elif l < 200: len_bins["长(80-200字)"] += 1
        else: len_bins["超长(>200字)"] += 1

    # 4. Punctuation analysis
    punct_counts = Counter()
    for t in texts:
        for c in t:
            if c in CN_PUNCT:
                punct_counts[c] += 1
            elif c in ".!?,\"';:-":
                punct_counts[c] += 1

    # 5. Emoji/emoticon analysis
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]|[☀-➿]|[︀-️]|[\U0001FA00-\U0001FA6F]|[\U0001FA70-\U0001FAFF]')
    emoji_counts = Counter()
    for t in texts:
        for m in emoji_pattern.finditer(t):
            emoji_counts[m.group()] += 1

    # Also count Chinese brackets like [微笑] [裂开] [强]
    bracket_emoji = re.findall(r'\[([^\]]{1,8})\]', ' '.join(texts))
    bracket_counts = Counter(b for b in bracket_emoji if len(b) <= 6)

    # 6. Question ratio
    question_count = sum(1 for t in texts if '?' in t or '？' in t)
    question_ratio = question_count / total_msgs if total_msgs > 0 else 0

    # 7. Common starter words (first 2 chars of messages)
    starter_words = Counter()
    for t in texts:
        if len(t) >= 2:
            starter_words[t[:2]] += 1

    # 8. Common words/phrases (2-4 char ngrams)
    skip_chars_2 = CN_PUNCT | set(' \n\r\t')
    word_freq = Counter()
    for t in texts:
        # Simple character bigrams (for Chinese)
        for i in range(len(t)-1):
            bigram = t[i:i+2]
            if not any(c in skip_chars_2 for c in bigram):
                word_freq[bigram] += 1

    # 9. Common unique phrases (3-char trigrams)
    skip_chars = CN_PUNCT | set(' \n\r\t[]()（）')
    trigram_freq = Counter()
    for t in texts:
        for i in range(len(t)-2):
            trigram = t[i:i+3]
            if not any(c in skip_chars for c in trigram):
                trigram_freq[trigram] += 1

    # 10. Reply patterns
    reply_starters = Counter()
    for t in texts:
        if t.startswith('那') or t.startswith('但是') or t.startswith('所以') or t.startswith('因为'):
            reply_starters['转折/因果开头'] += 1
        if '我也' in t[:8] or '我也是' in t[:8]:
            reply_starters['共情回应'] += 1
        if '？' in t or '?' in t:
            reply_starters['提问'] += 1
        if t.startswith('我觉得') or t.startswith('我认为'):
            reply_starters['观点陈述'] += 1
        if '哈哈' in t or '笑死' in t or 'hhhh' in t.lower():
            reply_starters['笑点'] += 1

    # 11. Topic keywords detection
    topic_keywords = {
        '学习/技术': ['学', '项目', '代码', 'AI', '知识', '后端', '前端', '算法', '数据'],
        '情感/关系': ['喜欢', '爱', '想', '感觉', '心', '关系', '朋友'],
        '工作/职业': ['实习', '工作', '面试', '简历', '公司', '岗位'],
        '生活/日常': ['吃饭', '睡觉', '学校', '回家', '图书馆', '宿舍'],
        '自我反思': ['我觉得', '应该', '可能', '或许', '其实', '说实话'],
        '鼓励/支持': ['加油', '你可以', '没事', '慢慢来', '坚持'],
    }
    topic_scores = {}
    for topic, keywords in topic_keywords.items():
        score = 0
        for t in texts:
            for kw in keywords:
                score += t.count(kw)
        topic_scores[topic] = score / max(total_msgs, 1)

    return {
        'total_messages': total_msgs,
        'total_chars': total_chars,
        'avg_message_length': round(avg_length, 1),
        'avg_sentence_length': round(avg_sentence_len, 1),
        'length_distribution': len_bins,
        'top_punctuation': punct_counts.most_common(10),
        'top_emojis': emoji_counts.most_common(15),
        'top_bracket_emojis': bracket_counts.most_common(15),
        'question_ratio': round(question_ratio, 3),
        'top_starters': starter_words.most_common(15),
        'top_bigrams': [(bg, c) for bg, c in word_freq.most_common(20) if c > 10 and len(bg.strip()) == 2],
        'top_trigrams': [(tg, c) for tg, c in trigram_freq.most_common(15) if c > 5],
        'reply_patterns': dict(reply_starters),
        'topic_scores': {k: round(v, 3) for k, v in topic_scores.items()},
    }

def generate_dna_report(name, analysis, output_dir):
    """Generate a human-readable 文风DNA report."""
    a = analysis
    if not a:
        return

    report_path = os.path.join(output_dir, f"DNA_{name}.md")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# {name} 文风DNA分析报告\n\n")
        f.write(f"- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- 消息总数: {a['total_messages']}\n")
        f.write(f"- 总字符数: {a['total_chars']}\n\n")

        f.write("---\n\n## 1. 消息特征\n\n")
        f.write(f"- **平均消息长度**: {a['avg_message_length']} 字\n")
        f.write(f"- **平均句长**: {a['avg_sentence_length']} 字\n")
        f.write(f"- **提问比例**: {a['question_ratio']*100:.1f}%\n")

        len_dist = a['length_distribution']
        f.write(f"\n### 消息长度分布\n\n")
        for k, v in len_dist.items():
            pct = v / a['total_messages'] * 100
            bar = '█' * int(pct / 2)
            f.write(f"- {k}: {v} ({pct:.1f}%) {bar}\n")

        # Punctuation
        if a['top_punctuation']:
            f.write(f"\n## 2. 标点习惯\n\n")
            f.write("| 标点 | 次数 |\n|------|------|\n")
            for p, c in a['top_punctuation'][:8]:
                f.write(f"| `{p}` | {c} |\n")

        # Emojis
        if a['top_emojis'] or a['top_bracket_emojis']:
            f.write(f"\n## 3. 表情/emoji偏好\n\n")
            if a['top_emojis']:
                f.write("### Unicode Emoji\n\n")
                for e, c in a['top_emojis'][:10]:
                    f.write(f"- {e}: {c}次\n")
            if a['top_bracket_emojis']:
                f.write("\n### 微信表情 [xxx]\n\n")
                for e, c in a['top_bracket_emojis'][:10]:
                    f.write(f"- `[{e}]`: {c}次\n")

        # Common phrases
        if a['top_bigrams']:
            f.write(f"\n## 4. 高频词组合 (Bigram)\n\n")
            f.write("| 词组合 | 次数 |\n|--------|------|\n")
            for bg, c in a['top_bigrams'][:15]:
                f.write(f"| {bg} | {c} |\n")

        if a['top_trigrams']:
            f.write(f"\n## 5. 标志性短语 (Trigram)\n\n")
            f.write("| 短语 | 次数 |\n|------|------|\n")
            for tg, c in a['top_trigrams'][:15]:
                f.write(f"| {tg} | {c} |\n")

        # Reply patterns
        if a['reply_patterns']:
            f.write(f"\n## 6. 对话模式\n\n")
            for pattern, count in sorted(a['reply_patterns'].items(), key=lambda x: -x[1]):
                f.write(f"- {pattern}: {count}次\n")

        # Topic focus
        f.write(f"\n## 7. 话题偏好 (关键词密度)\n\n")
        topics = sorted(a['topic_scores'].items(), key=lambda x: -x[1])
        for topic, score in topics:
            bar = '█' * int(score * 200)
            f.write(f"- {topic}: {score:.3f} {bar}\n")

        # Top starters
        if a['top_starters']:
            f.write(f"\n## 8. 消息开头习惯\n\n")
            for s, c in a['top_starters'][:10]:
                f.write(f"- `{s}`... → {c}次\n")

        # Style summary
        f.write(f"\n---\n\n## 9. 文风概括\n\n")

        # Auto-generate style summary based on data
        style_notes = []

        if a['avg_message_length'] < 20:
            style_notes.append("**简洁型**：消息偏短，倾向于快速回应")
        elif a['avg_message_length'] < 50:
            style_notes.append("**中等型**：消息长度适中，有话则长无话则短")
        else:
            style_notes.append("**长篇型**：倾向于展开说明，信息密度高")

        if a['question_ratio'] > 0.3:
            style_notes.append("**提问倾向强**：经常提出问题，对话主导性强")
        elif a['question_ratio'] > 0.15:
            style_notes.append("**适度提问**：提问和陈述均衡")
        else:
            style_notes.append("**陈述为主**：更倾向于表达观点而非提问")

        reply = a['reply_patterns']
        if reply.get('共情回应', 0) > a['total_messages'] * 0.05:
            style_notes.append("**共情能力强**：经常使用'我也'等共情表达")
        if reply.get('笑点', 0) > a['total_messages'] * 0.03:
            style_notes.append("**幽默风趣**：高频使用'哈哈'等笑点表达")
        if reply.get('观点陈述', 0) > a['total_messages'] * 0.05:
            style_notes.append("**观点明确**：经常以'我觉得'开头表达观点")
        if reply.get('转折/因果开头', 0) > a['total_messages'] * 0.03:
            style_notes.append("**逻辑性强**：常用转折/因果连词组织思考")

        for note in style_notes:
            f.write(f"- {note}\n")

    return report_path

def generate_psychology_report(name, msgs, output_dir):
    """Generate psychological distillation report for a contact."""
    texts = [m['text'] for m in msgs]
    if not texts:
        return

    report_path = os.path.join(output_dir, f"PSY_{name}.md")
    total = len(texts)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# {name} 心理分析报告（蒸馏）\n\n")
        f.write(f"- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- 分析消息数: {total}\n\n")
        f.write("---\n\n")

        # 1. 沟通风格
        f.write("## 1. 沟通风格\n\n")

        avg_len = sum(len(t) for t in texts) / max(total, 1)
        question_ratio = sum(1 for t in texts if '?' in t or '？' in t) / max(total, 1)
        laugh_ratio = sum(1 for t in texts if '哈哈' in t or '笑死' in t or 'hh' in t.lower()) / max(total, 1)

        f.write(f"- 平均消息长度: {avg_len:.1f} 字\n")
        f.write(f"- 提问频率: {question_ratio*100:.1f}%\n")
        f.write(f"- 笑点频率: {laugh_ratio*100:.1f}%\n")

        # 2. 情感模式
        f.write(f"\n## 2. 情感关键词\n\n")

        emotion_words = {
            '积极': ['开心', '好', '喜欢', '棒', '不错', '哈哈', '笑', '太', '厉害', '优秀', '加油', '可以'],
            '消极': ['烦', '累', '难', '哭', '焦虑', '压力', '不会', '不好', '不行', '无语', '崩溃'],
            '不确定': ['可能', '也许', '大概', '不知道', '不确定', '或许', '感觉'],
            '亲近': ['想', '爱', '喜欢', '思念', '想你了', '一起'],
            '担忧': ['害怕', '担心', '怕', '万一', '如果'],
        }

        for category, words in emotion_words.items():
            score = sum(sum(t.count(w) for w in words) for t in texts)
            f.write(f"- **{category}**: {score}次命中 ({score/max(total,1)*100:.1f}%)\n")

        # 3. 核心关注点
        f.write(f"\n## 3. 核心关注话题\n\n")

        topics = {
            '技术/学习': ['学', '项目', '代码', '编程', 'AI', '后端', '前端', '算法', '知识', '技术', '岗位', '面试'],
            '自我成长': ['我觉得', '应该', '想', '尝试', '改变', '规划', '目标', '方向', '选择'],
            '关系/社交': ['朋友', '同学', '认识', '一起', '帮忙', '联系'],
            '情绪表达': ['感觉', '觉得', '心情', '状态', '心态'],
            '求助/请教': ['帮我', '能不能', '可以吗', '请问', '麻烦', '问一下'],
        }

        for topic, keywords in topics.items():
            count = sum(sum(t.count(kw) for kw in keywords) for t in texts)
            f.write(f"- **{topic}**: {count}次\n")

        # 4. 时间线分析（按月）
        f.write(f"\n## 4. 时间线活跃度\n\n")
        # Group messages by date
        date_msgs = defaultdict(int)
        for m in msgs:
            date_key = m['time'][:7] if len(m['time']) >= 7 else m['time']
            date_msgs[date_key] += 1

        for dk in sorted(date_msgs.keys())[:12]:
            cnt = date_msgs[dk]
            bar = '█' * max(1, cnt // max(1, max(date_msgs.values()) // 30))
            f.write(f"- {dk}: {cnt} {bar}\n")

        # 5. 典型表达样本
        f.write(f"\n## 5. 典型表达样本\n\n")

        # Find representative sentences (medium length, content-rich)
        representative = []
        for t in texts:
            if 15 < len(t) < 100 and not any(w in t for w in ['wxid_', 'http', 'www.']):
                representative.append(t)
                if len(representative) >= 10:
                    break

        if representative:
            for i, t in enumerate(representative[:7], 1):
                f.write(f"{i}. {t}\n\n")

        # 6. 初步人格画像
        f.write(f"\n## 6. 初步人格画像\n\n")

        traits = []
        if avg_len > 30: traits.append("表达欲较强，倾向于详细说明")
        elif avg_len > 15: traits.append("表达适中")
        else: traits.append("简洁型表达")

        if question_ratio > 0.25: traits.append("主动提问者，对话发起方")
        elif question_ratio > 0.12: traits.append("双向交流型")
        else: traits.append("倾听回应型")

        # Check for self-reflection
        self_reflect = sum(1 for t in texts if '我觉得' in t[:10] or '我感觉' in t[:10] or '可能' in t)
        if self_reflect / max(total, 1) > 0.2:
            traits.append("自我觉察度高，经常反思自己的状态")
        else:
            traits.append("务实直接，少自我剖析")

        # Check for support-seeking
        support = sum(1 for t in texts if '帮' in t or '怎么办' in t or '不知道怎么' in t)
        if support / max(total, 1) > 0.05:
            traits.append("适度的求助倾向，不排斥表达困惑")

        for t in traits:
            f.write(f"- {t}\n")

        f.write(f"\n> ⚠️ 注：以上分析基于WeChat聊天记录的自动化统计，仅供了解沟通模式参考。真实人格远比文字数据复杂。\n")

    return report_path

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Analyze each chat
    chats = [
        ("Camellia", "chat_Camellia_plain.txt"),
        ("米蛋糕", "chat_米蛋糕_plain.txt"),
    ]

    all_analyses = {}

    for name, filename in chats:
        path = os.path.join(CHAT_DIR, filename)
        if not os.path.exists(path):
            print(f"SKIP: {path} not found")
            continue

        print(f"\n{'='*60}")
        print(f"Analyzing: {name}")

        msgs = load_messages(path)
        print(f"  Senders: {list(msgs.keys())}")
        for sender, msgs_list in msgs.items():
            print(f"    {sender}: {len(msgs_list)} messages")

        for sender, msgs_list in msgs.items():
            if len(msgs_list) < 100:
                continue

            print(f"\n  --- {sender} ({len(msgs_list)} msgs) ---")

            # DNA analysis
            analysis = analyze_sender(sender, msgs_list)
            all_analyses[f"{name}/{sender}"] = analysis

            # Generate DNA report
            dna_path = generate_dna_report(f"{sender}({name})", analysis, OUTPUT_DIR)
            print(f"  DNA report: {dna_path}")

        # Generate psychology report for the OTHER person (not 小黎)
        for sender, msgs_list in msgs.items():
            if sender == "小黎":
                continue
            if len(msgs_list) < 100:
                continue
            psy_path = generate_psychology_report(f"{sender}({name})", msgs_list, OUTPUT_DIR)
            print(f"  Psychology report: {psy_path}")

    # Write combined analysis JSON
    json_path = os.path.join(OUTPUT_DIR, "all_analyses.json")
    # Convert non-serializable types
    clean = {}
    for k, v in all_analyses.items():
        clean[k] = {kk: (dict(vv) if isinstance(vv, Counter) else vv) for kk, vv in v.items()}
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"Analysis complete! Output: {OUTPUT_DIR}")
    for name in ['Camellia', '米蛋糕']:
        for sender in ['小黎', name]:
            key = f"{name}/{sender}"
            if key in all_analyses:
                a = all_analyses[key]
                print(f"  {key}: {a['total_messages']} msgs, avg_len={a['avg_message_length']}字, questions={a['question_ratio']*100:.0f}%")

if __name__ == "__main__":
    main()
