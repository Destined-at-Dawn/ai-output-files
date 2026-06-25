# -*- coding: utf-8 -*-
"""
批量为百大认知书籍添加 Obsidian frontmatter。
- 无 frontmatter 的文件：插入完整 YAML 头部
- 有 frontmatter 的文件：修正 number 格式（035→35）
- 跳过非书籍文件（000-总索引、问题拆解、框架-数据映射表等）
"""
import os, re, glob

VAULT = os.path.dirname(os.path.abspath(__file__))

# ── 域分类规则 ──
# 基于每本书的领域标签关键词自动判断
DOMAIN_RULES = [
    ("D1", "决策与判断", [
        "决策", "行为经济学", "判断", "框架", "博弈", "战略", "管理系统",
        "项目管理", "敏捷", "协作", "人工智能", "人机协作", "组织管理"
    ]),
    ("D2", "认知科学基础", [
        "认知科学", "神经科学", "学习科学", "记忆", "注意力", "认知心理",
        "认知负荷", "认知神经", "神经生物", "脑科学", "具身认知",
        "教育神经", "神经可塑"
    ]),
    ("D3", "个人成长与行动力", [
        "习惯", "生产力", "专注力", "时间管理", "拖延", "执行功能",
        "优先级", "时间块", "自我管理", "行为心理", "行为改变",
        "动机", "毅力", "目标", "自我效能"
    ]),
    ("D4", "系统思维与方法论", [
        "系统思维", "系统工程", "复杂系统", "反脆弱", "风险管理",
        "概率", "算法", "非线性", "演化", "进化", "基因",
        "延伸表型", "社会动物"
    ]),
    ("D5", "社会与人文", [
        "社会学", "教育社会", "文化资本", "阶层", "政治社会",
        "组织行为", "差序格局", "科层", "权力", "家庭", "养育",
        "童年", "个体化", "私人生活", "积极心理学", "情绪",
        "奖励", "惩罚"
    ]),
    ("D6", "生命哲学与世界观", [
        "哲学", "意义", "世界观", "认识论", "道德", "自由",
        "人工智能伦理", "意识", "心灵", "体验", "时间感知",
        "物理", "经济", "宏观"
    ]),
    ("D7", "工具与实践方法", [
        "思维工具", "方法论", "实践", "应用", "工具", "技术",
        "NLP", "编程", "数学思维", "可视化", "笔记",
        "知识管理", "写作", "沟通"
    ]),
]

def detect_domain(tags_line: str) -> tuple:
    """根据领域标签行判断域归属，返回 (code, name)"""
    best = ("D2", "认知科学基础")  # 默认
    best_score = 0
    for code, name, keywords in DOMAIN_RULES:
        score = sum(1 for kw in keywords if kw in tags_line)
        if score > best_score:
            best_score = score
            best = (code, name)
    return best

def extract_author(content: str) -> str:
    """从文件内容提取作者"""
    # 匹配 **作者：** 或 > **作者：** 后面的内容
    m = re.search(r'\*{2}作者[：:]\*{2}\s*(.+?)(?:\n|$)', content)
    if m:
        author = m.group(1).strip()
        # 去掉尾部的逗号、顿号
        author = author.rstrip('，,、')
        return author
    return ""

def extract_tags(content: str) -> str:
    """从文件内容提取领域标签行"""
    m = re.search(r'\*{2}领域标签[：:]\*{2}\s*(.+?)(?:\n|$)', content)
    if m:
        return m.group(1).strip()
    return ""

def extract_title_from_heading(content: str) -> str:
    """从 # NNN《标题》格式提取标题"""
    m = re.search(r'^#\s+\d+《(.+?)》', content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""

def has_frontmatter(content: str) -> bool:
    """检查文件是否已有 frontmatter"""
    return content.startswith('---\n') or content.startswith('---\r\n')

def fix_number_in_frontmatter(content: str, correct_num: int) -> str:
    """修正已有 frontmatter 中的 number 格式"""
    # 将 number: "035" 或 number: '035' 改为 number: 35
    content = re.sub(
        r'number:\s*["\']?0*(\d+)["\']?',
        f'number: {correct_num}',
        content,
        count=1
    )
    # 如果 number 行不存在，在 domain 后添加
    if 'number:' not in content.split('---')[1]:
        # 在第一个 --- 后的 frontmatter 中添加
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # 在 frontmatter 末尾添加 number
            fm = parts[1].rstrip('\n').rstrip('\r')
            fm += f'\nnumber: {correct_num}\n'
            content = fm.join(['---', '---']) + parts[2] if len(parts) > 2 else fm.join(['---', '---'])
    return content

def build_frontmatter(num: int, title: str, author: str, domain_code: str, domain_name: str, tags_line: str, filename: str) -> str:
    """构建 YAML frontmatter"""
    # 从领域标签提取 tag 列表
    tag_list = [t.strip() for t in tags_line.split('/') if t.strip()]
    # 去重并限制数量
    seen = set()
    clean_tags = []
    for t in tag_list:
        t = t.strip(' .')
        if t and t not in seen and len(t) < 20:
            seen.add(t)
            clean_tags.append(t)
    if len(clean_tags) > 5:
        clean_tags = clean_tags[:5]

    # 构建 aliases（英文名从文件名提取）
    # 文件名格式：016-习惯的力量-The-Power-of-Habit.md
    parts = filename.replace('.md', '').split('-', 1)
    alias_en = ""
    if len(parts) > 1:
        rest = parts[1]
        # 去掉中文名部分，保留英文名
        # 格式：中文名-English-Name
        # 找到第一个英文字母开头的位置
        en_match = re.search(r'[A-Z]', rest)
        if en_match:
            en_start = en_match.start()
            # 往前找到分隔符
            while en_start > 0 and rest[en_start-1] not in ('-', '—', '（', '('):
                en_start -= 1
            alias_en = rest[en_start:].strip('-').replace('-', ' ')

    lines = ['---']
    lines.append(f'title: "{title}"')
    if author:
        # 截断过长的作者描述
        author_short = author[:80] if len(author) > 80 else author
        lines.append(f'author: "{author_short}"')
    lines.append(f'number: {num}')
    lines.append(f'domain: "{domain_code}"')
    if clean_tags:
        tags_str = ', '.join(f'"{t}"' for t in clean_tags)
        lines.append(f'tags: [{tags_str}]')
    lines.append(f'status: "已分析"')
    if alias_en:
        lines.append(f'aliases: ["{alias_en}"]')
    lines.append(f'source: "百大认知书籍/{filename}"')
    lines.append('---')
    lines.append('')
    return '\n'.join(lines)

def process_file(filepath: str) -> dict:
    """处理单个文件，返回处理结果"""
    filename = os.path.basename(filepath)

    # 跳过非书籍文件
    if not re.match(r'^\d{3}-', filename):
        return {"file": filename, "action": "skipped", "reason": "not a book file"}

    # 提取编号
    num = int(filename[:3])

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_frontmatter(content):
        # 已有 frontmatter，修正 number
        if re.search(r'number:\s*["\']?0*\d+["\']?', content):
            new_content = fix_number_in_frontmatter(content, num)
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return {"file": filename, "action": "fixed_number", "number": num}
        return {"file": filename, "action": "already_has_fm", "reason": "number OK"}

    # 无 frontmatter，添加
    title = extract_title_from_heading(content)
    if not title:
        # 从文件名提取
        m = re.match(r'^\d{3}-(.+?)(?:-[A-Z].*)?\.md$', filename)
        title = m.group(1).replace('-', ' ') if m else filename.replace('.md', '')

    author = extract_author(content)
    tags_line = extract_tags(content)
    domain_code, domain_name = detect_domain(tags_line)

    fm = build_frontmatter(num, title, author, domain_code, domain_name, tags_line, filename)
    new_content = fm + content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return {
        "file": filename,
        "action": "added",
        "number": num,
        "domain": f"{domain_code} {domain_name}",
        "title": title,
        "author": author[:40] if author else "(none)"
    }

def main():
    files = glob.glob(os.path.join(VAULT, '*.md'))
    results = {"added": 0, "fixed": 0, "skipped": 0, "already": 0}

    for fp in sorted(files):
        r = process_file(fp)
        act = r["action"]
        if act == "added":
            results["added"] += 1
            print(f"  + {r['file'][:40]:40s} → {r['domain']}")
        elif act == "fixed_number":
            results["fixed"] += 1
            print(f"  # {r['file'][:40]:40s} → number={r['number']}")
        elif act == "skipped":
            results["skipped"] += 1
        elif act == "already_has_fm":
            results["already"] += 1

    print(f"\n{'='*50}")
    print(f"新增 frontmatter: {results['added']}")
    print(f"修正 number:      {results['fixed']}")
    print(f"已有(无需改):     {results['already']}")
    print(f"跳过(非书籍):     {results['skipped']}")

if __name__ == '__main__':
    main()
