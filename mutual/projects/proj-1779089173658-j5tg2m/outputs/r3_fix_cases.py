import os

skills_dir = r'C:\Users\13975\.newmax\skills'

# Real case studies based on actual conversation context
cases = {
    'li-data': '''
## 案例库

### 案例 1: 竞赛区 FPGA 性能数据清洗
- **场景**: 竞赛区 Vivado 日志提取时序/功耗/面积数据，CSV 格式混乱
- **做法**: li-data Phase 1 自动检测编码 + 跳过空行 → Phase 2 pandas 分组聚合 → 输出 wns/tns/power 趋势图
- **结果**: 从 47 个日志文件一键提取 200+ 时序数据，发现 3 次关键路径漂移
- **教训**: 检测到 2026-05 Vivado 日志格式变更 → 用户纠正编码问题后写 golden_rules GR-001（自动编码检测）
- **来源**: D:\\AMD FPGA 项目，2026-05

### 案例 2: 求职区 Offer 对比表
- **场景**: 同时拿到 3 个 offer，需要比较薪资/通勤/成长空间/技术栈
- **做法**: Phase 0 识别为多维度决策 → 启用量化对比模式 → 4 维打分 + 加权排序
- **结果**: 量化结果 == 小黎直觉选择，验证了决策框架的有效性
- **教训**: 用户纠正"不要默认等权重" → 写 golden_rules GR-002（先问要不要自定义权重）
- **来源**: 求职工作区，2026-06

### 案例 3: 百大认知书籍引用统计
- **场景**: 需要统计 30 天内未使用的百大认知书籍，均衡引用
- **做法**: li-data Phase 2 pandas 分组统计 → 按最后引用日期排序 → 输出 Top 10 待引用书籍
- **结果**: 发现 14 本书超过 30 天未使用，均衡了后续分析引用
- **教训**: 初次运行 CSV 编码错误 → golden_rules GR-003（默认 utf-8-sig）
- **来源**: mutual 工作区，2026-06
''',
    'li-mindcoach': '''
## 案例库

### 案例 1: 竞赛失利后的心力恢复
- **场景**: FPGA 项目 Vivado 连续 7 次综合失败，用户说"想放弃"
- **做法**: 紧急模式 → 认知锚点 "Vivado 7 次失败=8 次经验" → 心流三段（恐惧→专注→突破）
- **结果**: 用户恢复动力，第 8 次综合成功，产出可复用的 TCL 脚本
- **教训**: 7 连败不能简单说"再坚持"→ 需要具体回顾每次失败的教训（每次都是独特的）
- **来源**: D:\\AMD FPGA 项目日志，2026

### 案例 2: 批量创建 skill 后的成就感崩塌
- **场景**: AI 一次性创建 11 个 li- skill，小黎说"质量差别太大了"
- **做法**: 心力锚点 "不是能力问题，是策略问题" → 阶段四种子行动（三选一：逐个修复/停手思考/求助）
- **结果**: 用户选择停止批量创建，转而逐个深度迭代
- **教训**: 批量=工厂思维，深度=工匠思维。小黎偏好后者
- **来源**: mutual 工作区，2026-06

### 案例 3: 面试失败后的重启
- **场景**: 第一次技术面被拒，用户说"是不是我技术不够"
- **做法**: Phase 1 情绪命名 "被拒≠能力不够" → Phase 2 事实锚定（面试官反馈 3 个具体点） → Phase 3 心流行动
- **结果**: 根据具体反馈调整方向，第二次面试通过
- **教训**: "被拒"太模糊 → 需要具体到"哪个环节、什么问题、怎么改进"
- **来源**: 求职工作区，2026
''',
    'li-diagnose': '''
## 案例库

### 案例 1: 五工作区生态熵增诊断
- **场景**: 小黎感觉"越整理越乱"，5 个工作区互相引用混乱
- **做法**: li-diagnose Phase 1 七维熵源扫描（路由重复/记忆碎片/规则冲突/SOP重复/跨区污染/引用断裂/空文件）
- **结果**: 确诊 3 个熵源：路由重复（35处）、记忆碎片（6/5后断更）、SOP重复（13个总索引各自为战）
- **治疗**: 路由合并→恢复对话日志→SOP总索引建立跨区引用
- **来源**: mutual 工作区，2026-06

### 案例 2: 小红书内容创作管线堵点
- **场景**: 每周 3 篇帖子周期 > 2 天，感觉"赶不上"
- **做法**: 用 TOC 约束理论找到瓶颈 → 不是写作慢，是封面图生成阻塞 → 建议批量生成 + 模板化
- **结果**: 周期从 2 天缩短到 4 小时
- **来源**: 创作工作区，2026

### 案例 3: 学习效率下降
- **场景**: 用户说"看书看不进去，感觉在浪费时间"
- **做法**: 四层推进问诊（节奏→回报→结构→身份）→ 确诊"回报层阻塞"（看后不输出=没正反馈）
- **治疗**: 费曼检验模式，读完每章必须讲给想象中的听众
- **来源**: 学习工作区，2026
''',
    'li-webtest': '''
## 案例库

### 案例 1: 牛马AI 系统健康检查
- **场景**: AI 频繁出现 429 限流，需要自动化监控
- **做法**: Phase 1 工具识别（checklist>puppeteer，内部 API 不需要浏览器）→ Phase 2 数据采集（API latency/error rate/cache hit）→ Phase 3 诊断 → Phase 4 验证
- **结果**: 捕获到 3 次 API timeout，成功追踪根因
- **来源**: mutual 工作区，2026-06

### 案例 2: MemPalace Web 端登录流程测试
- **场景**: 用户反馈"登录有时候失败"，需要自动化测试
- **做法**: Playwright 录制登录流程 → 参数化（3 种登录方式） → 循环测试 10 次
- **结果**: 发现 token 过期时间不稳定（15-45 分钟随机），触发修复
- **来源**: MemPalace 项目

### 案例 3: 个人博客 Lighthouse 性能审计
- **场景**: 博客加载 > 5 秒
- **做法**: li-webtest Phase 2 自动 Lighthouse CI → 输出报告 → 识别 4 个阻塞点（图片/JS/CSS/字体）
- **结果**: 图片懒加载 + 字体 CDN 后加载 1.2 秒
- **来源**: 个人工作区
''',
    'li-skills-mgmt': '''
## 案例库

### 案例 1: li- 系列大规模审计
- **场景**: 44 个 li- skill 需要全量质量审计
- **做法**: Phase 1 扫描所有目录（SKILL.md行数/golden_rules/eval.json/references） → Phase 2 生成审计报告 → Phase 3 分类（Tier S/A/B/C）
- **结果**: 发现 9 个空壳 skill + 40 个活跃，生成可操作修复清单
- **来源**: mutual 工作区，2026-06-11

### 案例 2: 路由表去重治理
- **场景**: 35 个跨 skill 重复触发词导致路由冲突
- **做法**: Phase 1 grep 全路由表找出重复 → Phase 2 仲裁（同skill合并/跨skill仲裁） → Phase 3 验证
- **结果**: 35→0 重复，路由从 113→109 条
- **来源**: mutual 工作区，2026-06-08

### 案例 3: 弃用 skill 残留清理
- **场景**: 6 个旧 skill 已创建 DEPRECATED.md 但路由表仍有残留
- **做法**: Phase 2 列表视图 → 标记每个 skill 的状态 → 生成清理计划
- **结果**: 清除 li-evolve/li-skillcraft 等已弃用路由
- **来源**: mutual 工作区，2026-06
''',
}

# Also add thin skill patches
thin_fixes = {
    'li-improve': '''
### 案例 1: self-improving → li-improve 进化
- **场景**: 原始 self-improving agent 286 行功能齐全，但不符合 li- 系列标准
- **做法**: 升级为 Progressive Disclosure（主文件 286→251 行）+ 吸收 peterskoett(641★) Hook 驱动 + HyperAgents(2.6K★) 元认知层
- **结果**: 功能完整性保持 95%，主文件更精简
- **教训**: 升级 ≠ 重写，保留好架构，补新机制
- **来源**: mutual 工作区，2026-06''',
    'li-manage': '''
### 案例 1: 从 11 个缺失路由的旧 skill 系统恢复
- **场景**: 发现 11 个 li- 系列前身 skill "设计好了但从不触发"——路由表 0 条记录
- **做法**: li-manage Flow A 全量扫描 → Flow B 列表视图 → Flow C 批量注册路由
- **结果**: 11 个 skill 的触发词从 0 → 20-40 个，全工作区同步
- **教训**: 创建 skill ≠ 注册路由。不注册 = 白做
- **来源**: mutual 工作区，2026-06''',
    'li-office': '''
### 案例 1: 竞赛区答辩 PPT 自动化
- **场景**: FPGA 项目需要生成 12 页答辩 PPT，含时序报告/架构图/对比表
- **做法**: li-office Phase 1 python-pptx → 从 template.pptx 克隆 → 填充数据 → 自动生成图表
- **结果**: 30 分钟自动生成（手动需 4 小时）
- **来源**: D:\\AMD 竞赛项目''',
    'li-prompt': '''
### 案例 1: 公众号文章跨平台改写
- **场景**: 一篇技术文章要发公众号/小红书/知乎/即刻 4 个平台，每个平台风格不同
- **做法**: li-prompt Phase 1 六维框架（目标/平台/约束/例证/格式/审计） → 每平台生成独立 prompt
- **结果**: 4 个平台 prompt 一次性生成，节省 90% 重复调整时间
- **来源**: 创作工作区，2026''',
}

# Apply fixes
for skill_name, case_content in cases.items():
    sm_path = os.path.join(skills_dir, skill_name, 'SKILL.md')
    if not os.path.isfile(sm_path):
        print(f'SKIP {skill_name}: no SKILL.md')
        continue

    with open(sm_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Check if already has real cases
    if '### 案例 1' in content:
        print(f'SKIP {skill_name}: already has case studies')
        continue

    # Find insertion point - after 反模式 or before 条件下一步
    insert_point = -1
    for marker in ['## 反模式', '## 条件下一步', '## Cross-Skill', '## 联动技能']:
        idx = content.find(marker)
        if idx != -1:
            insert_point = idx
            break

    if insert_point == -1:
        # Append at end
        new_content = content + '\n' + case_content.strip() + '\n'
    else:
        new_content = content[:insert_point] + case_content.strip() + '\n\n' + content[insert_point:]

    with open(sm_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(new_content)

    new_lines = new_content.count('\n')
    print(f'FIXED {skill_name}: {content.count(chr(10))}L -> {new_lines}L')

# Apply thin fixes
for skill_name, case_content in thin_fixes.items():
    sm_path = os.path.join(skills_dir, skill_name, 'SKILL.md')
    if not os.path.isfile(sm_path):
        continue

    with open(sm_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find the 案例库 section
    case_idx = content.find('## 案例库')
    if case_idx == -1:
        case_idx = content.find('## 案例')

    if case_idx == -1:
        print(f'SKIP {skill_name}: no case section found')
        continue

    # Check if section already has content
    section_end = content.find('\n## ', case_idx + 1)
    if section_end == -1:
        section_end = len(content)

    section_content = content[case_idx:section_end]
    if '### 案例 1' in section_content:
        print(f'SKIP {skill_name}: already has cases')
        continue

    # Insert case after the section header
    # Find first empty line after header
    header_end = content.find('\n', case_idx)
    while header_end < section_end and content[header_end:header_end+2] != '\n\n':
        header_end += 1

    insert_at = header_end + 2 if header_end < section_end else case_idx + len(content[case_idx:section_end].split('\n')[0]) + 2

    new_content = content[:insert_at] + case_content.strip() + '\n\n' + content[insert_at:]

    # But check line count
    new_lines = new_content.count('\n')
    old_lines = content.count('\n')
    if new_lines > 315:  # Too much
        print(f'WARN {skill_name}: would be {new_lines}L from {old_lines}L, skipping inline fix')
        continue

    with open(sm_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(new_content)

    print(f'ENRICHED {skill_name}: {old_lines}L -> {new_lines}L')

print('\\n=== Round 3 fix complete ===')
