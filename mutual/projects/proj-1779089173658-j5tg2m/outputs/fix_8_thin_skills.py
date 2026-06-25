import os

skills_dir = os.path.expanduser('~/.newmax/skills')

fixes = {
    'li-docs': {
        'anti': True,
        'anti_content': """## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|----------|
| AP-1 | 不检查文件编码就解析 | 中文乱码，内容丢失 | 先用 chardet 检测编码再读取 |
| AP-2 | PDF OCR 用默认参数 | 表格/公式识别率低 | 根据文档类型选 zerox vs pdf |
| AP-3 | 不去水印/页眉页脚就输出 | 噪音污染后续分析 | Phase 2 必须清洗 |
| AP-4 | 把整个 PDF 一次喂给 AI | 超出上下文窗口 | 按章节分段提取再汇总 |
| AP-5 | 假设 DOCX 结构一致 | 样式不同导致解析失败 | 先读取文档结构再选择解析策略 |
""",
        'cases': True,
        'cases_content': """## 案例库

- Case 1: 200 页学术 PDF 全文喂给 AI 导致截断。正确：按 Abstract/Method/Result/Discussion 分段提取后汇总。
- Case 2: DOCX 合同含表格+签名图片，python-docx 只提取文字。补充：ppocrv5 提取图片文字再合并。
- Case 3: HTML 转 Markdown 嵌套列表丢失层级。解决：BeautifulSoup 递归解析 ul/ol 嵌套保留缩进。
"""
    },
    'li-frontend': {
        'anti': True,
        'anti_content': """## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|----------|
| AP-1 | 用 JS 实现 CSS 能做的动画 | 性能差，掉帧 | CSS transition/animation 优先 |
| AP-2 | 不做移动端适配 | 小屏乱版 | 移动优先 + 响应式断点 |
| AP-3 | 一次性生成完整页面代码 | 超长难调试 | 拆组件逐个生成再组装 |
| AP-4 | 不考虑可访问性 | 部分用户无法使用 | 语义化标签 + alt + ARIA |
| AP-5 | 品牌色/字体凭感觉选 | 视觉不一致 | 先确认品牌规范再实现 |
""",
    },
    'li-personal': {
        'anti': True,
        'anti_content': """## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|----------|
| AP-1 | 简历堆砌所有经历 | 重点不突出 | 5 维工程语言检查 + 岗位匹配 |
| AP-2 | 面试准备只背答案 | 遇变体就慌 | STAR 框架 + 模拟追问 |
| AP-3 | 职业规划只看薪资 | 3 年后迷失方向 | 技术栈+行业趋势+个人兴趣 |
| AP-4 | 自我介绍念简历 | 面试官失去兴趣 | 故事线设计（问题->行动->结果） |
| AP-5 | 不做考研/求职双线评估 | 单点失败无后路 | 杠铃策略：保守端+激进端 |
""",
    },
    'li-platform': {
        'anti': True,
        'anti_content': """## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|----------|
| AP-1 | 微信文章直接复制粘贴 | 格式丢失/图片断裂 | wechat-article-collector 完整提取 |
| AP-2 | 公众号发文不做排版 | 阅读体验差 | baoyu-post-to-wechat 自动排版 |
| AP-3 | 跨平台内容不改格式 | 各平台风格不匹配 | 每个平台独立适配 |
| AP-4 | 不备份微信数据库 | 数据丢失 | wechat-exporter 定期导出 |
| AP-5 | 发布前不检查敏感词 | 被限流/删除 | 发布前扫描敏感词 |
""",
    },
    'li-search': {
        'anti': True,
        'anti_content': """## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|----------|
| AP-1 | 关键词太窄（加平台限定） | 漏掉高质量结果 | 先宽泛搜核心概念再精确补充 |
| AP-2 | 只搜一个平台 | 信息不全面 | 四阶段全覆盖 |
| AP-3 | 不按 Stars/质量排序 | 低质量结果 | GitHub 必须 &s=stars&o=desc |
| AP-4 | 只看 README 不看实现 | 空壳项目 | 至少读核心源码 3 个文件 |
| AP-5 | 搜到 0 结果就放弃 | 换词可能有结果 | 最高 <100 Stars = 关键词太窄 |
""",
    },
    'li-session': {
        'anti': True,
        'anti_content': """## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|----------|
| AP-1 | 摘要太长（>500字） | 没人会读 | 30秒版+2分钟版分层 |
| AP-2 | 只记成功不记失败 | 下次重蹈覆辙 | 失败路径同等记录 |
| AP-3 | 知识不确认就写入 | 污染长期记忆 | memory-candidate-protocol |
| AP-4 | 会话结束不总结 | 关键决策丢失 | 每次对话强制 Phase 0-2 |
| AP-5 | 审计只看"是否完成" | 忽略质量维度 | 审计含质量评分+改进建议 |
""",
    },
    'li-voice': {
        'anti': True,
        'anti_content': """## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|----------|
| AP-1 | 全文替换AI套路词 | 丧失语境 | 只替换高频词保留用户习惯 |
| AP-2 | 不保留口语化特征 | 失去人格感 | 口语连接词是品牌资产 |
| AP-3 | Voice DNA 只看1篇 | 样本太小 | 至少分析5篇不同场景 |
| AP-4 | 去AI味过度 | 从太假变太糙 | 目标是像用户写的 |
| AP-5 | IP人设和真实性格矛盾 | 演不下去 | 基于真实特质放大 |
""",
    },
    'li-writing': {
        'cases': True,
        'cases_content': """## 案例库

- Case 1: 小红书帖子。用户说"写电气考研经验帖" -> Phase 0 识别平台+受众 -> Phase 1 结构:痛点共鸣->干货->互动引导 -> 用户评价好 -> golden_rules 记录"小红书用 emoji+口语化"。
- Case 2: 公众号长文。用户说"写AI工具测评" -> Phase 0 识别:公众号,3000字 -> Phase 1:问题-方案-对比-推荐 -> Phase 2:SEO标题优化 -> li-memory 记录"公众号标题用数字+问句效果好"。
- Case 3: 学术润色。用户说"改论文摘要" -> Phase 0:学术,正式 -> Phase 1:逻辑清晰化+术语标准化 -> 不改学术语气只优化精度。
""",
        'anti': True,
        'anti_content': """## 反模式

| # | 反模式 | 后果 | 正确做法 |
|---|--------|------|----------|
| AP-1 | 所有平台用同一风格 | 小红书像论文 | Phase 0 必须识别平台和受众 |
| AP-2 | 开头铺垫太长 | 读者流失 | 结论先行前3句抓注意力 |
| AP-3 | AI味只改表面词 | 被读者识破 | 结构+节奏+口语化综合调整 |
| AP-4 | 写完不读一遍 | 病句/逻辑断裂 | Phase 2 强制通读 |
| AP-5 | 不考虑平台算法 | 内容好也没曝光 | 标题/tag/发布时间适配平台 |
""",
    },
}

for skill_name, content in fixes.items():
    skill_path = os.path.join(skills_dir, skill_name, 'SKILL.md')
    if not os.path.exists(skill_path):
        print(f'SKIP {skill_name}: not found')
        continue

    with open(skill_path, 'r', encoding='utf-8') as f:
        text = f.read()

    additions = ''
    if content.get('cases') and '## 案例库' not in text and '## 案例' not in text:
        additions += '\n' + content['cases_content'] + '\n'
    if content.get('anti') and '## 反模式' not in text and '## Anti' not in text:
        additions += '\n' + content['anti_content'] + '\n'

    if additions:
        insert_point = text.rfind('## 设计哲学')
        if insert_point == -1:
            insert_point = text.rfind('## Progressive Disclosure')
        if insert_point == -1:
            insert_point = len(text)
        text = text[:insert_point] + additions + text[insert_point:]
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(text)
        lines = len(text.split('\n'))
        print(f'FIXED {skill_name}: {lines} lines')
    else:
        print(f'OK {skill_name}: already has sections')
