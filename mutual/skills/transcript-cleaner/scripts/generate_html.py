#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道法术器HTML生成器
功能：将Markdown格式的道法术器内容转换为带"树根蔓延"动画的HTML网页
"""

import re
import sys
import io

# 修复Windows控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def parse_markdown_to_structure(md_content: str) -> dict:
    """将Markdown内容解析为结构化数据"""
    structure = {
        'title': '',
        'dao': [],
        'fa': [],
        'shu': [],
        'qi': []
    }

    lines = md_content.split('\n')
    current_section = None
    current_item = {'title': '', 'content': []}
    current_subitems = []

    for line in lines:
        line = line.strip()

        # 解析标题
        if line.startswith('# ') and not structure['title']:
            structure['title'] = line[2:].strip()
            continue

        # 解析各个部分
        if '道（底层认知' in line or line == '### 道（底层认知，跨场景复用）':
            current_section = 'dao'
            continue
        if '法（方法论框架' in line or line == '### 法（方法论框架，可迁移）':
            current_section = 'fa'
            continue
        if '术（具体执行' in line or line == '### 术（具体执行，可直接上手）':
            current_section = 'shu'
            continue
        if '器（工具与资源' in line or line == '### 器（工具与资源）':
            current_section = 'qi'
            continue

        # 解析每个部分的内容
        if current_section and line.startswith('**'):
            # 保存上一个项目
            if current_item['title']:
                structure[current_section].append({
                    'title': current_item['title'],
                    'content': current_item['content'],
                    'subitems': current_subitems
                })
                current_item = {'title': '', 'content': []}
                current_subitems = []

            # 新项目
            current_item['title'] = line.replace('**', '').replace('：', ':').strip()
        elif current_section and line.startswith('-'):
            content = line[1:].strip()
            if content.startswith('**'):
                # 子项目
                subitem = content.replace('**', '').replace('：', ':').strip()
                current_subitems.append(subitem)
            else:
                current_item['content'].append(content)
        elif current_section and current_item['title'] and line:
            current_item['content'].append(line)

    # 保存最后一个项目
    if current_item['title']:
        structure[current_section].append({
            'title': current_item['title'],
            'content': current_item['content'],
            'subitems': current_subitems
        })

    return structure


def generate_html(structure: dict, md_content: str) -> str:
    """生成HTML代码"""

    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB',
                'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #F8F5F0 0%, #E8E0D5 100%);
            min-height: 100vh;
            display: flex;
        }}

        /* 左侧导航栏 */
        .sidebar {{
            width: 280px;
            background: linear-gradient(180deg, #8B6B4C 0%, #6B4F38 100%);
            padding: 40px 20px;
            position: fixed;
            height: 100vh;
            left: 0;
            top: 0;
            box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
        }}

        .sidebar h1 {{
            color: #F8F5F0;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 40px;
            text-align: center;
            line-height: 1.4;
        }}

        .nav-button {{
            background: rgba(248, 245, 240, 0.1);
            border: 1px solid rgba(248, 245, 240, 0.2);
            color: #F8F5F0;
            padding: 18px 24px;
            margin-bottom: 16px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}

        .nav-button:hover {{
            background: rgba(248, 245, 240, 0.2);
            transform: translateX(5px);
        }}

        .nav-button.active {{
            background: #F8F5F0;
            color: #8B6B4C;
            box-shadow: 0 4px 15px rgba(139, 107, 76, 0.3);
        }}

        /* 右侧内容区 */
        .content {{
            margin-left: 280px;
            padding: 60px 80px;
            flex: 1;
        }}

        .content-title {{
            font-size: 36px;
            font-weight: 700;
            color: #8B6B4C;
            margin-bottom: 40px;
            opacity: 0;
            animation: fadeInUp 0.6s ease forwards;
        }}

        /* 玻璃拟态卡片 */
        .card {{
            background: rgba(248, 245, 240, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(212, 181, 158, 0.3);
            border-radius: 20px;
            padding: 30px 40px;
            margin-bottom: 24px;
            opacity: 0;
            transform: translateX(-30px);
            box-shadow: 0 8px 32px rgba(139, 107, 76, 0.1);
        }}

        .card-title {{
            font-size: 22px;
            font-weight: 600;
            color: #8B6B4C;
            margin-bottom: 16px;
            padding-left: 20px;
            position: relative;
        }}

        .card-title::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 8px;
            height: 8px;
            background: #8B6B4C;
            border-radius: 50%;
        }}

        .card-content {{
            color: #5A4A3A;
            line-height: 1.8;
            margin-left: 28px;
            margin-bottom: 16px;
        }}

        .card-content ul {{
            list-style: none;
            padding-left: 0;
        }}

        .card-content li {{
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
        }}

        .card-content li::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 16px;
            width: 6px;
            height: 6px;
            background: #D4B59E;
            border-radius: 50%;
        }}

        /* 树根连接线 */
        .tree-line {{
            position: absolute;
            left: 280px;
            top: 0;
            width: 3px;
            height: 0;
            background: linear-gradient(180deg, #8B6B4C 0%, #D4B59E 100%);
            transition: height 0.5s ease;
        }}

        /* 动画 */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes growTree {{
            from {{
                opacity: 0;
                transform: translateX(-50px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        .card.animate {{
            animation: growTree 0.6s ease forwards;
        }}

        /* 响应式 */
        @media (max-width: 1024px) {{
            .sidebar {{
                width: 240px;
            }}

            .content {{
                margin-left: 240px;
                padding: 40px 50px;
            }}
        }}

        @media (max-width: 768px) {{
            .sidebar {{
                width: 200px;
                padding: 30px 15px;
            }}

            .content {{
                margin-left: 200px;
                padding: 30px 20px;
            }}

            .content-title {{
                font-size: 28px;
            }}
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <h1>{title}</h1>
        <button class="nav-button active" data-section="dao">道（底层认知）</button>
        <button class="nav-button" data-section="fa">法（方法论）</button>
        <button class="nav-button" data-section="shu">术（具体执行）</button>
        <button class="nav-button" data-section="qi">器（工具资源）</button>
    </div>

    <div class="content">
        <h2 class="content-title" id="section-title">道（底层认知，跨场景复用）</h2>
        <div class="cards-container" id="cards-container">
            <!-- 卡片内容将通过JavaScript动态生成 -->
        </div>
    </div>

    <div class="tree-line" id="tree-line"></div>

    <script>
        const data = {json_data};

        const cardsContainer = document.getElementById('cards-container');
        const sectionTitle = document.getElementById('section-title');
        const treeLine = document.getElementById('tree-line');
        const navButtons = document.querySelectorAll('.nav-button');

        const sectionNames = {{
            'dao': '道（底层认知，跨场景复用）',
            'fa': '法（方法论框架，可迁移）',
            'shu': '术（具体执行，可直接上手）',
            'qi': '器（工具与资源）'
        }};

        function renderCards(section) {{
            cardsContainer.innerHTML = '';
            const items = data[section];

            if (items.length === 0) {{
                cardsContainer.innerHTML = '<div class="card"><p>暂无内容</p></div>';
                return;
            }}

            items.forEach((item, index) => {{
                const card = document.createElement('div');
                card.className = 'card';
                card.style.animationDelay = `${{index * 0.15}}s`;

                let contentHtml = `<div class="card-title">${{item.title}}</div>`;

                if (item.content && item.content.length > 0) {{
                    contentHtml += '<div class="card-content"><ul>';
                    item.content.forEach(c => {{
                        contentHtml += `<li>${{c}}</li>`;
                    }});
                    contentHtml += '</ul></div>';
                }}

                if (item.subitems && item.subitems.length > 0) {{
                    contentHtml += '<div class="card-content"><ul>';
                    item.subitems.forEach(s => {{
                        contentHtml += `<li>${{s}}</li>`;
                    }});
                    contentHtml += '</ul></div>';
                }}

                card.innerHTML = contentHtml;
                cardsContainer.appendChild(card);

                // 触发动画
                setTimeout(() => {{
                    card.classList.add('animate');
                }}, 50 + index * 150);
            }});
        }}

        function switchSection(section) {{
            // 更新标题
            sectionTitle.textContent = sectionNames[section];

            // 更新按钮状态
            navButtons.forEach(btn => {{
                btn.classList.remove('active');
                if (btn.dataset.section === section) {{
                    btn.classList.add('active');
                }}
            }});

            // 重置树根线
            treeLine.style.height = '0';

            // 渲染卡片
            renderCards(section);

            // 设置树根线高度
            setTimeout(() => {{
                const containerHeight = cardsContainer.offsetHeight;
                treeLine.style.height = `${{containerHeight}}px`;
            }}, 100);
        }}

        // 绑定按钮事件
        navButtons.forEach(btn => {{
            btn.addEventListener('click', () => {{
                switchSection(btn.dataset.section);
            }});
        }});

        // 初始化
        switchSection('dao');
    </script>
</body>
</html>'''

    import json
    json_data = json.dumps(structure, ensure_ascii=False)

    return html_template.format(
        title=structure['title'],
        json_data=json_data
    )


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_html.py <markdown文件路径>")
        print("示例: python generate_html.py transcript_cleaned.md")
        sys.exit(1)

    md_file = sys.argv[1]

    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 解析Markdown
        structure = parse_markdown_to_structure(md_content)

        # 生成HTML
        html = generate_html(structure, md_content)

        # 输出文件
        output_file = md_file.replace('.md', '.html').replace('_cleaned', '')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ HTML生成完成！")
        print(f"📁 输出文件: {output_file}")
        print(f"🌐 请在浏览器中打开该文件查看效果")

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
