"""
文风DNA蒸馏脚本：基于全量语料重新提取风格特征
对比私聊 vs 群聊用语差异
"""
import json, os, re
from collections import Counter, defaultdict

CORPUS_PATH = r'E:\ai产出文件\牛马\创作\创作\output\wechat_analysis\corpus.json'
SESSIONS_PATH = r'E:\ai产出文件\牛马\创作\创作\output\wechat_analysis\top_private.json'

def load_corpus():
    with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze():
    corpus = load_corpus()
    private_msgs = [m for m in corpus if not m['is_group']]
    group_msgs = [m for m in corpus if m['is_group']]

    print(f'总消息: {len(corpus)}')
    print(f'私聊消息: {len(private_msgs)}')
    print(f'群聊消息: {len(group_msgs)}')

    # 1. 消息长度分析
    def msg_lengths(msgs):
        lengths = [len(m['content']) for m in msgs if m['content']]
        if not lengths:
            return {'min': 0, 'max': 0, 'avg': 0, 'median': 0}
        lengths.sort()
        return {
            'min': min(lengths), 'max': max(lengths),
            'avg': round(sum(lengths) / len(lengths), 1),
            'median': lengths[len(lengths)//2],
            'lt_10': round(sum(1 for l in lengths if l < 10) / len(lengths) * 100, 1),
            'lt_20': round(sum(1 for l in lengths if l < 20) / len(lengths) * 100, 1),
            'lt_50': round(sum(1 for l in lengths if l < 50) / len(lengths) * 100, 1),
        }

    print('\n=== 消息长度 ===')
    print(f'私聊: {msg_lengths(private_msgs)}')
    print(f'群聊: {msg_lengths(group_msgs)}')

    # 2. 高频词分析
    def get_words(msgs, top=50):
        word_counter = Counter()
        for m in msgs:
            content = m['content']
            if not content:
                continue
            # 简单分词（中文按字符，英文按词）
            # 提取2-4字的常见组合
            for i in range(len(content)-1):
                bigram = content[i:i+2]
                if re.match(r'[一-鿿]{2}', bigram):
                    word_counter[bigram] += 1
        return word_counter.most_common(top)

    print('\n=== 高频2字词（私聊 Top 30）===')
    for w, c in get_words(private_msgs, 30):
        print(f'  {w}: {c}')

    print('\n=== 高频2字词（群聊 Top 30）===')
    for w, c in get_words(group_msgs, 30):
        print(f'  {w}: {c}')

    # 3. 表情/符号使用
    def count_pattern(msgs, pattern, label):
        count = sum(1 for m in msgs if m['content'] and pattern in m['content'])
        return count

    patterns = [
        ('哈哈|hh|笑死|笑死我了|😂|🤣', '笑声'),
        ('捂脸|😅|🤦|😅', '捂脸'),
        ('好的|好滴|好嘞|okk|ok', '确认'),
        ('谢谢|感谢|多谢', '感谢'),
        ('对不起|抱歉|不好意思', '道歉'),
        ('!!!|！！！', '感叹号'),
        ('？？|？', '问号'),
        ('……|\.\.\.', '省略号'),
        ('～|~', '波浪号'),
        ('嗯嗯|emmm|呃|哦哦', '语气词'),
    ]

    print('\n=== 表情/符号频率 ===')
    for pattern, label in patterns:
        p_cnt = count_pattern(private_msgs, pattern, label)
        g_cnt = count_pattern(group_msgs, pattern, label)
        p_rate = round(p_cnt / len(private_msgs) * 100, 1) if private_msgs else 0
        g_rate = round(g_cnt / len(group_msgs) * 100, 1) if group_msgs else 0
        print(f'  {label}: 私聊 {p_rate}% ({p_cnt}) | 群聊 {g_rate}% ({g_cnt})')

    # 4. 第一人称使用
    def count_pronouns(msgs):
        total = len(msgs)
        results = {}
        for pronoun in ['我', '你', '他', '她', '我们', '你们', '他们', '她们']:
            cnt = sum(1 for m in msgs if m['content'] and pronoun in m['content'])
            results[pronoun] = {'count': cnt, 'rate': round(cnt/total*100, 1)}
        return results

    print('\n=== 人称代词使用率 ===')
    print('私聊:', count_pronouns(private_msgs))
    print('群聊:', count_pronouns(group_msgs))

    # 5. 句式分析
    # 判断句、感叹句、疑问句的比例
    def sentence_types(msgs):
        total = len(msgs)
        exclaim = sum(1 for m in msgs if m['content'] and ('！' in m['content'] or '!' in m['content']))
        question = sum(1 for m in msgs if m['content'] and ('？' in m['content'] or '?' in m['content']))
        ellipsis = sum(1 for m in msgs if m['content'] and ('…' in m['content'] or '...' in m['content']))
        return {
            'exclamation': round(exclaim/total*100, 1),
            'question': round(question/total*100, 1),
            'ellipsis': round(ellipsis/total*100, 1),
        }

    print('\n=== 句式标记 ===')
    print('私聊:', sentence_types(private_msgs))
    print('群聊:', sentence_types(group_msgs))

    # 6. 按会话分析独特用词
    print('\n=== 按会话分析特征词 ===')
    session_words = defaultdict(Counter)
    for m in corpus:
        if not m['content']:
            continue
        # Extract all 4-gram Chinese phrases
        for i in range(len(m['content'])-3):
            phrase = m['content'][i:i+4]
            if re.match(r'^[一-鿿]{4}$', phrase):
                session_words[m['session']][phrase] += 1

    # Show top distinctive words per top session
    all_words = Counter()
    for session, wc in session_words.items():
        all_words.update(wc)

    for session, wc in sorted(session_words.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]:
        # Find words that are distinctive to this session
        distinctive = []
        for word, count in wc.most_common(100):
            global_count = all_words[word]
            if count > 5 and count / global_count > 0.3:
                distinctive.append((word, count))
        if distinctive:
            print(f'\n  {session}:')
            for w, c in distinctive[:10]:
                print(f'    {w}: {c}')

if __name__ == '__main__':
    analyze()
