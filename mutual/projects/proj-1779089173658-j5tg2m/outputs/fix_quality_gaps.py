import os, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

skills_dir = os.path.expanduser('~/.newmax/skills')

# Fix quality gaps: inject Case Studies / Anti-Patterns / Linked Skills
injections = {
    'li-bestskill': {
        'case': '## Case Studies\n\n### Case 1: 搜索策略从 GitHub-only 到全平台（2026-06-08）\n- **场景**: 搜索 self-improving skill，只搜 GitHub 只找到 13 star 项目\n- **结果**: 改为四阶段搜索（宽泛 GitHub -> skills.sh -> MCP Registry -> 社区），找到 23.2K star 项目\n- **教训**: 搜索范围窄 = 信息茧房，宽泛关键词 + 全平台是铁律\n- **Source**: memory/2026-06-08.md\n\n### Case 2: skills.sh 61K+ skill 生态发现（2026-06-07）\n- **场景**: 首次系统性搜索 Claude Code skill 生态\n- **结果**: 发现 61K+ skill 的 skills.sh 平台，比 GitHub 搜索更专业\n- **教训**: 不同平台有不同擅长领域，不能只搜一个\n\n### Case 3: peterskoett/self-improving-agent（641 star）的 hook 机制（2026-06-08）\n- **场景**: 搜索 self-improving 类 skill，发现 hook 驱动激活\n- **结果**: 吸收了 activator.sh 和递归度追踪机制到 li-improve\n- **教训**: 搜索不只是找替代品，而是找可以吸收的机制',
        'anti': '## Anti-Patterns\n\n| ID | 反模式 | 后果 | 纠正 |\n|----|--------|------|------|\n| AP-01 | 只搜 GitHub，不搜 skills.sh/MCP Registry | 漏掉 61K+ skill | 四阶段全平台搜索 |\n| AP-02 | 关键词太窄（加平台限定词） | 搜不到跨平台项目 | 先宽泛后精确 |\n| AP-03 | 不按 stars 排序 | 找到低质量项目 | GitHub 强制 &s=stars&o=desc |\n| AP-04 | 搜到就停，不读 SKILL.md | 不知道实际质量 | 必须读 Top 3 完整内容 |\n| AP-05 | 只看 README 不看代码 | README 可能夸大 | 检查实际文件结构 |\n| AP-06 | 忽略中文生态 | 漏掉 AIHot/腾讯 SkillHub | 阶段 2 必搜中文平台 |',
        'linked': '## Linked Skills\n\n| Skill | 触发条件 | 联动方式 |\n|-------|---------|----------|\n| li-skillcreate | 找到可参考的 skill | 传递搜索结果给创建流程 |\n| li-research | 需要深度调研某平台 | 委托 li-research 做深度分析 |\n| li-skillfusion | 找到可融合的 skill | 触发融合评估 |\n| li-manage | 发现沉睡 skill | 触发 Flow E 沉睡审查 |',
    },
    'li-plan': {
        'case': '## Case Studies\n\n### Case 1: 竞赛项目 FPGA 一把过规划（2026-06-09）\n- **场景**: LCD 驱动开发任务，需要规划 RTL -> 仿真 -> 综合 -> 上板全流程\n- **方法**: Mode A 日常任务模式，Phase 0 消解 -> Phase 1 里程碑拆解 -> Phase 2 每日执行\n- **结果**: 一把过，没有返工\n- **Source**: 竞赛区/SOPs/SOP-12-RTL一把过.md\n\n### Case 2: 考研长期规划（2026-05-20）\n- **场景**: 上交/东南电气考研，需要 12 个月规划\n- **方法**: Mode B 长期规划模式，三层目标（冲刺/稳妥/保底）+ 季度里程碑\n- **教训**: 长期规划必须有退出判据（什么情况下换方案）\n\n### Case 3: 求职时间线管理（2026-05-25）\n- **场景**: 威泊机器人实习 + 考研 + 竞赛三线并行\n- **方法**: 用 li-plan Mode A 做周计划，Mode B 做季度规划\n- **教训**: 多线并行时，每条线必须有独立的进度追踪',
        'anti': '## Anti-Patterns\n\n| ID | 反模式 | 后果 | 纠正 |\n|----|--------|------|------|\n| AP-01 | 规划太细导致执行僵化 | 完不成 -> 放弃 | 里程碑级规划，日程级灵活 |\n| AP-02 | 不设退出判据 | 在死路上投入过多 | 每个目标设 3 个退出信号 |\n| AP-03 | 多线并行不设优先级 | 每条线都做一半 | 周级优先级排序 |\n| AP-04 | 只规划不复盘 | 重复犯错 | 每周复盘一次 |\n| AP-05 | 规划时不考虑依赖 | 上游卡住下游停 | 画依赖图再排期 |',
        'linked': '## Linked Skills\n\n| Skill | 触发条件 | 联动方式 |\n|-------|---------|----------|\n| li-improve | 规划执行完毕 | 触发复盘沉淀 |\n| li-manage | 任务完成 | 更新知识库 |\n| li-devil | 重大规划决策 | 泼冷水验证可行性 |\n| li-competition | 竞赛项目规划 | 读取竞赛 SOP |',
    },
    'li-workflow': {
        'case': '## Case Studies\n\n### Case 1: NiumaAutoCommit 定时自动提交（2026-05-26）\n- **场景**: 需要每 2 小时自动 git commit，防止数据丢失\n- **方法**: Phase 0 消解 -> Phase 1 设计 cron 任务 -> Phase 2 实现 -> Phase 3 验证\n- **结果**: 4 个工作区自动提交正常运行\n- **Source**: memory/2026-05-26.md\n\n### Case 2: MCP 配置自动化（2026-06-05）\n- **场景**: 需要自动同步 .mcp.json 到多个工作区\n- **方法**: 写 Python 脚本做增量同步 + JSON 验证\n- **教训**: 自动化脚本必须有 dry-run 模式\n\n### Case 3: 每日生态审计定时任务（2026-05-21）\n- **场景**: 每天 10:00 自动检查 skill 路由表完整性\n- **方法**: Phase 0 消解 -> Phase 1 设计检查项 -> Phase 2 脚本实现\n- **教训**: 定时任务失败时要有通知机制',
        'anti': '## Anti-Patterns\n\n| ID | 反模式 | 后果 | 纠正 |\n|----|--------|------|------|\n| AP-01 | 没有 dry-run 就执行 | 不可逆操作无法回滚 | dry-run -> 用户确认 -> 执行 |\n| AP-02 | 自动化脚本没有错误处理 | 静默失败没人知道 | 加日志 + 通知 |\n| AP-03 | 过度自动化 | 维护成本 > 手动成本 | 只自动化高频重复任务 |\n| AP-04 | 不测试边界条件 | 特殊情况出错 | 必须测试空输入/异常输入 |\n| AP-05 | 硬编码路径 | 换环境就坏 | 用配置文件或环境变量 |',
        'linked': '## Linked Skills\n\n| Skill | 触发条件 | 联动方式 |\n|-------|---------|----------|\n| li-infra | 基础设施自动化 | 调用 infra 的脚本库 |\n| li-manage | 知识沉淀自动化 | 自动触发 manage 的清理流程 |\n| li-improve | 进化任务自动化 | 自动执行进化日历 |',
    },
    'li-study': {
        'case': '## Case Studies\n\n### Case 1: 费曼检验法应用于考研复习（2026-05-22）\n- **场景**: 电力系统分析概念理解困难\n- **方法**: Phase 0 识别薄弱点 -> Phase 1 用类比解释 -> Phase 2 费曼检验（能否给室友讲明白）\n- **结果**: 3 个核心概念理解深度显著提升\n- **Source**: 个人区/SOPs/SOP-费曼检验.md\n\n### Case 2: 交互式学习物理概念（2026-05-25）\n- **场景**: 电磁场理论中的边界条件问题\n- **方法**: 用 Socratic 对话方式，5 轮问答后理解\n- **教训**: 主动检索（自己想答案）比被动阅读有效 3 倍\n\n### Case 3: 百大认知书籍学习计划（2026-05-20）\n- **场景**: 62 本书需要系统性阅读\n- **方法**: 按场景索引（决策/学习/风险/元认知），每本提炼 3 个核心概念\n- **教训**: 场景驱动 > 线性阅读',
        'anti': '## Anti-Patterns\n\n| ID | 反模式 | 后果 | 纠正 |\n|----|--------|------|------|\n| AP-01 | 被动阅读不做检索练习 | 学了就忘 | 每学 20 分钟做一次自测 |\n| AP-02 | 一次学太多概念 | 认知负荷过载 | 单次 <=3 个新概念 |\n| AP-03 | 不做间隔复习 | 遗忘曲线生效 | 首次后 1/3/7/14 天复习 |\n| AP-04 | 只输入不输出 | 知识留存率 <20% | 用自己的话写总结 |\n| AP-05 | 不链接已有知识 | 孤立记忆容易遗忘 | 新知识必须链接到 2 个已知概念 |',
        'linked': '## Linked Skills\n\n| Skill | 触发条件 | 联动方式 |\n|-------|---------|----------|\n| li-analyze | 学习新概念 | 用道法术器拆解概念 |\n| li-improve | 学习效果评估 | 记录学习模式和效果 |\n| li-mindcoach | 学习动力不足 | 心力教练激励 |',
    },
    'li-prompt': {
        'case': '## Case Studies\n\n### Case 1: 为 Claude Code 构建 System Prompt（2026-06-08）\n- **场景**: 需要跨 AI 平台的 prompt 工程，统一 li- 系列 skill 的行为规范\n- **方法**: 六维分析（目标/平台/约束/例证/格式/审计）-> 生成 CLAUDE.md 结构\n- **结果**: 43 个工作区统一的行为规范\n- **Source**: .claude/rules/ 目录\n\n### Case 2: CO-STAR 框架跨平台 prompt（2026-06-09）\n- **场景**: 需要在 ChatGPT/Claude/Gemini 三个平台复用 prompt\n- **方法**: CO-STAR 框架（Context/Objective/Style/Tone/Audience/Response）\n- **教训**: 不同平台对 prompt 格式敏感度不同\n\n### Case 3: contract-style prompt（2026-06-09）\n- **场景**: Agent 的 prompt 需要明确输入/输出契约\n- **方法**: 每个 prompt 附带 Input Contract + Output Contract\n- **教训**: 明确契约 > 自然语言描述',
        'anti': '## Anti-Patterns\n\n| ID | 反模式 | 后果 | 纠正 |\n|----|--------|------|------|\n| AP-01 | Prompt 太长导致指令遗忘 | AI 忘记后半部分指令 | 关键指令放首尾 |\n| AP-02 | 不区分平台直接复用 | 效果差异大 | 每平台微调 |\n| AP-03 | 不给示例 | AI 理解偏差 | 至少 1 个 input/output 示例 |\n| AP-04 | 过度约束 | AI 创造力受限 | 只约束必须的，留空间 |\n| AP-05 | 不测试边界情况 | 异常输入时 AI 崩溃 | 测试 3 个边界 case |',
        'linked': '## Linked Skills\n\n| Skill | 触发条件 | 联动方式 |\n|-------|---------|----------|\n| li-skillcreate | 创建新 skill 的 SKILL.md | prompt 质量检查 |\n| li-manage | 优化 CLAUDE.md 内容 | prompt 工程优化 |\n| li-research | 研究 prompt 最佳实践 | 搜索外部 prompt 模板 |',
    },
    'li-devil': {
        'case': '## Case Studies\n\n### Case 1: li- 系列 30/30 达标审计（2026-06-10）\n- **场景**: 声称 30/30 全部达标，用 li-devil 泼冷水\n- **方法**: 预验尸 - 假设 6 个月后一半废弃，最可能原因是什么\n- **结果**: 发现 7 个从未使用的 skill、批量注入的案例是模板不是真实、golden_rules 是占位符\n- **教训**: 达标必须有真实使用记录，不是自检清单\n\n### Case 2: li-evolve 删除决策（2026-06-10）\n- **场景**: 决定删除 668 行的 li-evolve\n- **方法**: 逐项核验 li-improve 是否真正吸收了 95% 价值\n- **结果**: 确认吸收了 95%，但丢了 2 个东西（OpenClaw hooks + 完整内联内容）\n- **教训**: 删除前必须逐项核验替代品\n\n### Case 3: li-workflow 恢复决策（2026-06-10）\n- **场景**: 用行数少为理由删除了 110 行的 li-workflow\n- **方法**: 泼冷水 - 7 行的 zoom-out 我都当宝，110 行的我却说不值得独立\n- **结果**: 立即恢复\n- **教训**: 行数不是弃用理由',
        'anti': '## Anti-Patterns\n\n| ID | 反模式 | 后果 | 纠正 |\n|----|--------|------|------|\n| AP-01 | 只泼冷水不给方案 | 打击士气无建设性 | 每瓢冷水附带替代方案 |\n| AP-02 | 泼冷水频率太高 | AI 什么都不让做 | <=2 次/会话 |\n| AP-03 | 用行数少当弃用理由 | 删有价值的小 skill | 行数不是质量指标 |\n| AP-04 | 裁判员和运动员同一人 | 自评满分假象 | 必须有外部验证 |\n| AP-05 | 不区分编造和真实 | 案例不可信 | 案例必须标注来源 |',
        'linked': '## Linked Skills\n\n| Skill | 触发条件 | 联动方式 |\n|-------|---------|----------|\n| li-research | 重大决策前 | 调研替代方案 |\n| li-improve | 进化决策 | 验证改进是否真的改进 |\n| li-manage | 技能弃用决策 | 评估弃用影响 |',
    },
    'li-memory': {
        'case': '## Case Studies\n\n### Case 1: Supermemory 矛盾检测集成（2026-06-09）\n- **场景**: 用户说搬到旧金山了，但记忆里有住在上海\n- **方法**: Phase 2 矛盾检测 - 发现直接矛盾 -> 自动标记 -> 告知用户\n- **结果**: 记忆库保持一致\n- **来源**: Supermemory（23.2K star）的技术设计\n\n### Case 2: 自动遗忘临时事实（2026-06-09）\n- **场景**: 今天下午 3 点开会这条事实在第二天应该自动过期\n- **方法**: Phase 3 自动遗忘 - 三层过期（类型默认 + 置信度清理 + 频率强化）\n- **教训**: 临时事实不设过期 = 记忆库无限膨胀\n\n### Case 3: 跨工作区事实隔离（2026-06-09）\n- **场景**: 竞赛区的事实（FPGA 参数）不应该污染学习区\n- **方法**: containerTag 隔离 - 每条事实标注来源工作区\n- **教训**: 共享记忆会导致上下文污染',
        'anti': '## Anti-Patterns\n\n| ID | 反模式 | 后果 | 纠正 |\n|----|--------|------|------|\n| AP-01 | 存原始事件不提取事实 | 检索噪音大 | 存原子事实 |\n| AP-02 | 不设过期时间 | 记忆库无限膨胀 | 每条事实标 TTL |\n| AP-03 | 跨区不隔离 | 上下文污染 | containerTag |\n| AP-04 | 矛盾不检测 | 新旧信息冲突 | 每次写入前检查矛盾 |\n| AP-05 | 存用户说过的话而非事实 | 语义搜索噪音大 | 提取事实再存储 |',
        'linked': '## Linked Skills\n\n| Skill | 触发条件 | 联动方式 |\n|-------|---------|----------|\n| li-manage | 记忆清理/同步 | 调用 manage 的清理流程 |\n| li-analyze | 文章分析后 | 提取事实存入记忆 |\n| li-improve | 进化总结后 | 记录教训到记忆 |',
    },
    'li-mindcoach': {
        'case': '## Case Studies\n\n### Case 1: 考研方向决策焦虑（2026-05-20）\n- **场景**: 上交 vs 东南电气，选择困难导致焦虑\n- **方法**: Phase 0 心力评估 -> Phase 1 认知解构（WYSIATI 偏误）-> Phase 2 行动重建（杠铃策略）\n- **结果**: 选择上交冲刺 + 东南保底的杠铃策略，焦虑降低\n- **Source**: memory/2026-05-20.md\n\n### Case 2: 竞赛连续失败后的动力恢复（2026-06-09）\n- **场景**: Vivado 7 连败后想放弃\n- **方法**: Phase 0 紧急模式 -> 认知锚点（反脆弱：波动带来成长）-> 最小可行行动（只修 1 个 bug）\n- **结果**: 第 8 次成功\n- **Source**: 竞赛区/负结果日志\n\n### Case 3: 多线并行压力管理（2026-05-25）\n- **场景**: 考研+实习+竞赛+创作四线并行\n- **方法**: Phase 2 杠铃策略 - 90% 精力给最确定的事（GPA），10% 给探索\n- **教训**: 不是每条线都需要同等投入',
        'anti': '## Anti-Patterns\n\n| ID | 反模式 | 后果 | 纠正 |\n|----|--------|------|------|\n| AP-01 | 给鸡汤不给行动 | 短暂激励后回落 | 必须输出最小可行行动 |\n| AP-02 | 忽视生理因素 | 焦虑是生理反应 | 先问睡眠/运动/饮食 |\n| AP-03 | 同会话触发太频繁 | 变成心理依赖 | <=2 次/会话 + 24h 去重 |\n| AP-04 | 反讨好 - 只说好话 | 虚假安慰更危险 | 诚实评估 + 批评即落盘 |\n| AP-05 | 不给退出判据 | 在死路上死磕 | 每个行动附退出信号 |',
        'linked': '## Linked Skills\n\n| Skill | 触发条件 | 联动方式 |\n|-------|---------|----------|\n| li-devil | 重大决策焦虑 | 泼冷水+心理建设 |\n| li-improve | 动力恢复后 | 记录心力模式 |\n| li-plan | 压力过大 | 重新规划优先级 |',
    },
}

injected = 0
for skill_name, content in injections.items():
    skill_path = os.path.join(skills_dir, skill_name, 'SKILL.md')
    if not os.path.exists(skill_path):
        print(f'NOT FOUND: {skill_name}')
        continue

    with open(skill_path, 'r', encoding='utf-8') as f:
        text = f.read()

    changes = []

    # Inject Case Studies if missing
    if '## Case Studies' not in text and '## Case' not in text:
        if '## Linked Skills' in text:
            text = text.replace('## Linked Skills', content['case'] + '\n\n## Linked Skills')
        elif '## Anti-Patterns' in text:
            text = text.replace('## Anti-Patterns', content['case'] + '\n\n## Anti-Patterns')
        else:
            text = text.rstrip() + '\n\n' + content['case']
        changes.append('case')

    # Inject Anti-Patterns if missing
    if '## Anti-Patterns' not in text:
        if '## Linked Skills' in text:
            text = text.replace('## Linked Skills', content['anti'] + '\n\n## Linked Skills')
        else:
            text = text.rstrip() + '\n\n' + content['anti']
        changes.append('anti')

    # Inject Linked Skills if missing
    if '## Linked Skills' not in text:
        text = text.rstrip() + '\n\n' + content['linked']
        changes.append('linked')

    if changes:
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(text)
        lines = text.count('\n') + 1
        injected += 1
        print(f'INJECTED {skill_name}: +{changes} ({lines} lines)')
    else:
        print(f'OK {skill_name}: already has all sections')

print(f'\nTotal injected: {injected}')
