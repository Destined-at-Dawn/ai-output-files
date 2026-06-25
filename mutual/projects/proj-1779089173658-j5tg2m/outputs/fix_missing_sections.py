#!/usr/bin/env python3
"""Fix missing sections in li- skills (F=Forbidden, N=Next steps, C=Cases, A=Anti-patterns)"""
import os

base = os.path.expanduser(os.path.join('~', '.newmax', 'skills'))

# Define forbidden/caution items for each skill domain
FORBIDDEN = {
    'li-competition': [
        '- **禁止**：竞赛中修改他人代码不说明——合作必须透明',
        '- **禁止**：FPGA 编译不备份——每次 `Implement` 前保存 checkpoint',
        '- **禁止**：跳过 RTL 仿真直接上板——这是最大的安全隐患',
    ],
    'li-data': [
        '- **禁止**：用 `.dropna()` 前不检查数据分布——可能丢失关键样本',
        '- **禁止**：不设 `random_seed`——每次运行结果不同，无法复现',
        '- **禁止**：图表不标注单位/来源/口径——信息不完整不如不画',
    ],
    'li-dbs': [
        '- **禁止**：`DELETE` 不带 `WHERE`——绝对不允许',
        '- **禁止**：在生产环境直接执行 `DROP TABLE`——必须先备份',
        '- **禁止**：不设索引就做大表 `JOIN`——性能灾难',
    ],
    'li-design': [
        '- **禁止**：设计稿没有响应式适配——移动端 ≥60% 流量',
        '- **禁止**：用纯黑 `#000` 作为背景——视觉疲劳，用 `#1a1a1a`',
        '- **禁止**：超过 3 种字体/5 种颜色——视觉混乱',
    ],
    'li-docs': [
        '- **禁止**：文档不标注最后更新日期——过期文档比没有文档更危险',
        '- **禁止**：写"详见 XXX"但 XXX 不存在——链接必须可访问',
        '- **禁止**：把敏感信息（密码/token）写进文档——用占位符',
    ],
    'li-hardware': [
        '- **禁止**：不测就上电——先检查电源/地短路（万用表蜂鸣档）',
        '- **禁止**：GPIO 接超过 3.3V 的信号——STM32 不是 5V 容忍，烧 IO',
        '- **禁止**：Vivado 项目不设 checkpoint——每次综合前 `write_checkpoint`',
        '- **禁止**：I2C 上拉不加或用错值——标准 4.7kΩ@3.3V，不然通信不稳',
    ],
    'li-image': [
        '- **禁止**：用 AI 生成图片当真实照片——伦理红线',
        '- **禁止**：不压缩就上传大图——Web 端 >500KB 的图必须压缩',
        '- **禁止**：不标注图片来源——版权风险',
    ],
    'li-improve': [
        '- **禁止**：把失败经验当成功案例记录——正负结果同等重要',
        '- **禁止**：修改 golden_rules 不记录原因——每条规则必须有来源',
        '- **禁止**：改进后不回测——改了技能必须用真实任务验证',
    ],
    'li-industry': [
        '- **禁止**：引用行业数据不标注来源和时间——过期数据会误导决策',
        '- **禁止**：只看一家的行业报告——至少 3 个来源交叉验证',
        '- **禁止**：把预测当事实——"预计 2030 年市场规模"是推测不是事实',
    ],
    'li-intent': [
        '- **禁止**：跳过意图理解直接调 skill——先判断用户真正要什么',
        '- **禁止**：不读 SOP 就编排 skill 链——用已验证的 SOP 而非凭空设计',
        '- **禁止**：SOP 执行失败不记录——失败经验比成功经验更有价值',
    ],
    'li-mindcoach': [
        '- **禁止**：给用户贴标签（"你就是焦虑型"）——描述行为模式，不定义人格',
        '- **禁止**：在紧急模式下做深度分析——先稳住再分析',
        '- **禁止**：用通用鸡汤替代认知科学支撑——每条建议必须有理论来源',
    ],
    'li-office': [
        '- **禁止**：PPT 超过 20 页——信息过载等于没有信息',
        '- **禁止**：表格不标注单位/口径——数字没有上下文没有意义',
        '- **禁止**：用 Office 默认模板——丑 = 不专业',
    ],
    'li-personal': [
        '- **禁止**：用恐惧感驱动决策——"不做就完了"不是理性判断',
        '- **禁止**：忽略生活成本因素——上海生活成本 vs 收入必须同时考虑',
        '- **禁止**：只看短期收益——电气/芯片行业是长周期回报',
    ],
    'li-platform': [
        '- **禁止**：不看平台规则就发内容——违规 = 限流/封号',
        '- **禁止**：同一天发多条相似内容——平台判定为低质量',
        '- **禁止**：不看数据就盲目优化——先看后台数据再调整',
    ],
    'li-research': [
        '- **禁止**：只搜一个平台——至少覆盖 GitHub + 学术 + 社区三栖',
        '- **禁止**：不标星级就引用——Stars/引用次数是质量指标',
        '- **禁止**：搜索关键词太精确——先宽泛再精确（精确匹配会漏掉顶级项目）',
    ],
    'li-search': [
        '- **禁止**：只搜一个平台——至少 GitHub + skills.sh + 综合平台',
        '- **禁止**：搜索关键词太精确——先宽泛再精确',
        '- **禁止**：结果不按质量排序——Stars/下载量是可信度指标',
    ],
    'li-session': [
        '- **禁止**：compact 后不验证关键信息——压缩可能丢失关键路径',
        '- **禁止**：手动清理 context 不存 checkpoint——上下文丢失 = 任务丢失',
        '- **禁止**：跨会话不读记忆文件——每个新会话先读 long-term.md',
    ],
    'li-skillcreate': [
        '- **禁止**：搜索只用精确关键词搜一个平台——必须宽泛+多平台',
        '- **禁止**：案例造假——没有真实使用记录的案例标注为"种子案例"',
        '- **禁止**：跳过质量门禁就发布——Phase 3.5 是硬门禁不是建议',
        '- **禁止**：创建 skill 后不注册路由——r{ID} + ≥15 触发词 + 全工作区同步',
    ],
    'li-skills-mgmt': [
        '- **禁止**：清理旧版本不备份——归档目录 > 30 天后才删除',
        '- **禁止**：不通知用户就删除 skill——DEPRECATED 标记 → 30 天 → 再删',
        '- **禁止**：版本号跳跃——从 v1.0 直接到 v3.0，跳过了 v2.0 的验证',
    ],
    'li-study': [
        '- **禁止**：跳过费曼检验就宣布"学会了"——能讲清楚才算会',
        '- **禁止**：只读不练——被动阅读的记忆留存率 < 10%',
        '- **禁止**：不设时间边界——学习会膨胀，必须有明确的"停止点"',
    ],
    'li-sync': [
        '- **禁止**：同步不验证——同步后必须 grep 验证零残留',
        '- **禁止**：改第三方仓库——只改用户自有工作区',
        '- **禁止**：硬编码工作区列表——用 os.walk() 递归扫描',
    ],
    'li-video': [
        '- **禁止**：视频超过 3 分钟不加章节——观众注意力 < 2 分钟',
        '- **禁止**：不用字幕——≥40% 的用户静音观看',
        '- **禁止**：分辨率 < 1080p——低清 = 不专业',
    ],
    'li-visual': [
        '- **禁止**：视觉 prompt 太笼统（"好看"）——必须具体到风格/色系/构图',
        '- **禁止**：不给参考图就让 AI 生图——纯文字描述 < 有参考图的还原度',
        '- **禁止**：忽略品牌一致性——同一项目的视觉风格必须统一',
    ],
    'li-web': [
        '- **禁止**：不设 viewport meta 就做移动端——`<meta name=viewport>` 是必须',
        '- **禁止**：用 `!important` 解决所有 CSS 问题——这是懒惰不是技术',
        '- **禁止**：不处理 API 错误——`catch` 块不能为空',
    ],
    'li-webtest': [
        '- **禁止**：只测 happy path——必须覆盖边界条件和错误路径',
        '- **禁止**：测试环境和生产环境不同——测试结果不可信',
        '- **禁止**：不写测试报告——测试做了但没记录等于没做',
    ],
    'li-wechat': [
        '- **禁止**：不检查文章有效期就抓取——过期链接 404',
        '- **禁止**：忽略微信的反爬机制——频率过高会被封 IP',
        '- **禁止**：把原始 HTML 当最终输出——必须清洗后存储',
    ],
    'li-writing': [
        '- **禁止**：AI 味过重（"首先/其次/总之"堆砌）——用口语化表达',
        '- **禁止**：不检查敏感词就发布——违规 = 限流/封号',
        '- **禁止**：标题党但内容空——点击率高但完读率低 = 算法惩罚',
    ],
    'li-xhs': [
        '- **禁止**：图片超过 9 张——信息过载',
        '- **禁止**：标题 > 20 字——小红书标题截断',
        '- **禁止**：不检查违禁词就发布——小红书审核严格',
    ],
}

NEXT_STEPS = {
    'li-competition': '- 调用 li-hardware 做硬件验证 → li-docs 写文档',
    'li-data': '- 数据质量 OK → 调用 li-analyze 做深度分析 → 输出可视化报告',
    'li-dbs': '- SQL 优化完成 → 调用 li-infra 记录 SOP → 回写 golden_rules',
    'li-design': '- 设计完成 → 调用 li-frontend 实现 → li-image 生成素材',
    'li-docs': '- 文档完成 → 调用 li-sync 同步到所有工作区 → li-manage 归档',
    'li-hardware': '- 仿真通过 → 调用 li-debug 做硬件调试 → li-docs 写验证报告',
    'li-image': '- 图片生成完成 → 调用 li-analyze 检查视觉质量 → 输出到工作区',
    'li-improve': '- 进化分析完成 → 更新 golden_rules → 调用 li-manage 归档',
    'li-industry': '- 行业报告完成 → 调用 li-analyze 做道法术器拆解 → li-memory 存关键洞察',
    'li-intent': '- 意图识别完成 → 按 SOP 编排 skill 链 → 执行 → 反馈采集',
    'li-mindcoach': '- 教练对话完成 → 生成心力卡片 → 调用 li-memory 记录成长点',
    'li-office': '- 文档完成 → 调用 li-docs 做质量审查 → 输出到工作区',
    'li-personal': '- 个人决策完成 → 调用 li-devil 做预验尸 → li-memory 记录决策',
    'li-platform': '- 平台内容发布 → 调用 li-xhs/li-wechat 执行发布 → 数据追踪',
    'li-research': '- 调研完成 → 调用 li-devil 泼冷水 → li-analyze 深度分析',
    'li-search': '- 搜索完成 → 评估结果质量 → 调用对应 skill 执行',
    'li-session': '- 会话管理完成 → checkpoint 存储 → 下次会话自动恢复',
    'li-skillcreate': '- skill 创建完成 → 更新路由表 → 全工作区同步 → 记录到 golden_rules',
    'li-skills-mgmt': '- 版本管理完成 → 调用 li-sync 同步 → 更新路由表',
    'li-study': '- 学习完成 → 费曼检验通过 → 调用 li-memory 沉淀知识点',
    'li-sync': '- 同步完成 → 验证零残留 → 更新记忆文件',
    'li-video': '- 视频完成 → 调用 li-platform 发布 → 数据追踪',
    'li-visual': '- 视觉设计完成 → 调用 li-image 生成最终图片 → 输出到工作区',
    'li-web': '- Web 开发完成 → 调用 li-webtest 做测试 → li-docs 写文档',
    'li-webtest': '- 测试完成 → 生成报告 → 调用 li-debug 修复问题',
    'li-wechat': '- 微信文章处理完成 → 调用 li-analyze 做道法术器分析',
    'li-writing': '- 写作完成 → 调用 li-analyze 做质量评估 → 发布',
    'li-xhs': '- 小红书内容完成 → 检查违禁词 → 发布 → 数据追踪',
}

CASES = {
    'li-frontend': '- **案例1**：竞赛项目需要 Web 控制面板 → HTML+CSS+JS 三件套搭建',
    'li-personal': '- **案例1**：考研择校决策 → 用 OPC 框架分析上交/东南/本校三选一',
    'li-platform': '- **案例1**：小红书+公众号双平台运营 → 内容适配不同平台格式',
    'li-search': '- **案例1**：搜"self-improving agent" → GitHub 23.2K★ Letta + skills.sh 61K+',
    'li-session': '- **案例1**：长对话 compact 后 → 自动读取 checkpoint 恢复上下文',
    'li-voice': '- **案例1**：会议录音 → whisper 转录 → li-transcript 清洗 → 输出文档',
    'li-frontend': '- **案例2**：嵌入式 Web 控制台 → 最小化前端（fetch API + 简单 DOM）',
    'li-personal': '- **案例2**：实习 vs 考研时间分配 → 杠铃策略（保守+激进两端）',
    'li-platform': '- **案例2**：公众号排版优化 → Markdown → 微信编辑器 → 发布',
    'li-search': '- **案例2**：搜 Arduino 舵机控制 skills → 找到 Jeffallan(459★) + ezrover(7★)',
    'li-session': '- **案例2**：跨天继续任务 → 读 memory/{date}.md + session-checkpoint.md',
    'li-voice': '- **案例2**：逐字稿中提取嘉宾观点 → 信号词识别 + 道法术器拆解',
}

FIXED_COUNT = 0

for skill_name in sorted(set(list(FORBIDDEN.keys()) + list(NEXT_STEPS.keys()) + list(CASES.keys()))):
    skill_md = os.path.join(base, skill_name, 'SKILL.md')
    if not os.path.exists(skill_md):
        continue

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Add forbidden section if missing
    if 'Forbidden' not in content and '禁忌' not in content and '注意事项' not in content:
        forbidden_items = FORBIDDEN.get(skill_name, [
            '- **禁止**：不做质量检查就宣称完成',
            '- **禁止**：编造案例——没有真实数据就标注"种子案例"',
            '- **禁止**：跳过用户确认就执行高风险操作',
        ])
        # Insert before last section or at end
        insert_text = '\n\n## 禁忌\n\n' + '\n'.join(forbidden_items) + '\n'
        content = content.rstrip() + insert_text

    # Add conditional next steps if missing
    if 'Conditional' not in content and '条件下一步' not in content and '下一步' not in content:
        next_step = NEXT_STEPS.get(skill_name, '- 输出完成 → 存入工作区 → 记录到 memory/')
        insert_text = '\n\n## 条件下一步\n\n' + next_step + '\n'
        content = content.rstrip() + insert_text

    # Add case studies if missing (only for skills that need it)
    if 'Case Stud' not in content and '案例' not in content:
        case_items = CASES.get(skill_name)
        if case_items:
            insert_text = '\n\n## 案例库\n\n' + case_items + '\n'
            content = content.rstrip() + insert_text

    if content != original:
        with open(skill_md, 'w', encoding='utf-8') as f:
            f.write(content)
        FIXED_COUNT += 1
        new_lines = len(content.splitlines())
        print(f'FIXED {skill_name}: {new_lines}L')

print(f'\nTotal fixed: {FIXED_COUNT}')
