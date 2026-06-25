# 跨工具状态追踪

> 监控 handoffs/ 目录，记录工具间交接状态。
> handoff 超过 7 天未消费 → 提醒用户。

---

## Handoff 记录

| 日期 | 来源工具 | 目标工具 | 任务 | 文件路径 | 状态 |
|------|---------|---------|------|---------|------|
| 2026-06-08 | 竞赛/Codex | Hermes | 竞赛区交接文档 | `竞赛/outputs/handoff-20260608.md` | ✅ 已处理（2026-06-15 归档，内容已过时） |
| 2026-06-13 | Codex | Hermes | Skill/SOP 生产工作流能力补装 + 协作规则建立 | `05-每日记忆/2026-06-13-Codex-skill-sop-hermes-handoff.md` | ✅ 已消费 |
| 2026-06-18 | Codex | Hermes | SOP-13 残留引用修复（2 处断链定位 + patch 生成） | `05-每日记忆/2026-06-18-Hermes-SOP13残留引用修复建议.md` | ✅ 已消费（patch 已执行并验证） |
|| 2026-06-17 | Codex | Hermes | li-cicc-robei-fpga Skill 创建 + Robei 对标分析 | `05-每日记忆/2026-06-17-Codex-Robei集创赛Skill优化.md` | ✅ 已消费（2026-06-20 事实提取） |
|| 2026-06-18 | Codex | Hermes | 电路分析复习 PDF 证据逻辑纠偏（用户偏好） | `05-每日记忆/2026-06-18-Codex-电路PDF证据逻辑纠偏.md` | ✅ 已消费（2026-06-20 事实提取） |
|| 2026-06-19 | Codex | Hermes | li-webstyle Skill 创建 + 三工具同步 | `05-每日记忆/2026-06-19-Codex-li-webstyle.md` | ✅ 已消费（2026-06-20 事实提取） |
|| 2026-06-19 | Codex | Hermes | study-review-kit image_gen 口径更新 | `05-每日记忆/2026-06-19-Codex-study-review-kit-imagegen.md` | ✅ 已消费（2026-06-20 事实提取） |
|| 2026-06-19 | Codex | Hermes | study-review-kit 介绍页符合性审计 | `05-每日记忆/2026-06-19-Codex-study-review-kit审计.md` | ✅ 已消费（2026-06-20 事实提取） |
||| 2026-06-20 | Codex | Hermes | 高要求复习PDF改为image_gen直出唯一主路径 | `05-每日记忆/2026-06-20-Codex-study-review-pdf-imagegen-sop-skill.md` | ✅ 已消费（2026-06-21 周巡检事实提取） |
||| 2026-06-14 | Hermes | 多工具 | 教训闭环执行清单（动手前检查门禁） | `05-每日记忆/2026-06-14-Hermes-教训闭环-执行清单.md` | ✅ 已消费（2026-06-21 auto-consumed，任务已验证完成） |
||| 2026-06-14 | unknown | Claude Code | 教训闭环-路由表和检查规则 | `05-每日记忆/给ClaudeCode-教训闭环-路由表和检查规则.md` | ✅ 已消费（2026-06-21 auto-consumed，pre-action-check 已部署，路由表文件不存在已标记） |
||| 2026-06-14 | Hermes | Claude Code | 追加 Hermes 协作规则 | `05-每日记忆/给ClaudeCode-追加Hermes协作规则.md` | ✅ 已消费（2026-06-21 auto-consumed，.claude/CLAUDE.md 已验证） |
||| 2026-06-14 | Codex | Codex | 追加 Hermes 协作规则 | `05-每日记忆/给Codex-追加Hermes协作规则.md` | ✅ 已消费（2026-06-21 auto-consumed，.codex/AGENTS.md 已验证） |
||| 2026-06-14 | Hermes | Marvis | 追加 Hermes 协作规则 | `05-每日记忆/给Marvis-追加Hermes协作规则.md` | ⚠️ auto-consumed（2026-06-21），Marvis rules.md 未验证 |
||| 2026-06-14 | Newmax | Newmax | 创建 CLAUDE.md | `05-每日记忆/给Newmax-创建CLAUDE.md.md` | ✅ 已消费（2026-06-21 auto-consumed，.newmax/CLAUDE.md 已验证） |
||| 2026-06-14 | Newmax | Newmax | 教训闭环-创作SOP更新 | `05-每日记忆/给Newmax-教训闭环-创作SOP更新.md` | ✅ 已消费（2026-06-21 auto-consumed） |
||| 2026-06-14 | WorkBuddy | WorkBuddy | 创建 CLAUDE.md | `05-每日记忆/给WorkBuddy-创建CLAUDE.md.md` | ✅ 已消费（2026-06-21 auto-consumed，.workbuddy/CLAUDE.md 已验证） |

## 断链告警

- [已处理] 竞赛/Codex → Hermes：竞赛区交接文档（2026-06-08），已归档到 `归档/2026-06-15-proj-1777084456942-异常文件清理/`。
-

## 项目卡状态追踪

| 项目 ID | 项目名 | 状态 | 工作区 | 最后更新 | 关闭条件 |
|---------|--------|------|--------|---------|---------|
| PROJ-20260528-001 | 牛马AI 生态系统持续优化 | Active | mutual | 2026-05-28 | 五区规则零重复+启动序列实测+量化指标7天正常 |

### PROJ-20260528-001 待推进项

- [ ] 五区 CLAUDE.md 共享内容提取到根目录（减少 40% 重复）
- [ ] 启动序列在实际长会话中通过验证
- [ ] 量化指标连续 7 天正常采集
- [ ] Codex CLI 评审完成并落地可行建议
- [ ] 三件套使用 1 周无重大问题
- [ ] Hooks + 量化指标向其他 4 区部署（当前仅 mutual 完成）

### 新增项目追踪（2026-06-15）

| 项目 ID | 项目名 | 状态 | 工作区 | 最后更新 | 备注 |
|---------|--------|------|--------|---------|------|
| — | ljg-skills 融合 | 分析完成 | mutual | 2026-06-15 | v2 报告产出，4 个高价值融合点待验证 |
| — | SkVM 信息差内容 | 已产出 | 创作 | 2026-06-15 | 三件内容待发布 |
-

## 待跟进事项（2026-06-11 记录）

| # | 事项 | 优先级 | 所属工作区 | 负责工具 |
|---|------|--------|-----------|---------|
| 1 | li-data 补案例库+golden_rules | P0 | mutual | Newmax |
| 2 | li-study 补 eval.json | P0 | mutual | Newmax |
| 3 | conversation-journal 恢复自动更新 | P0 | mutual | Newmax |
| 4 | li-mindcoach 案例库验证 | P1 | mutual | Newmax |
| 5 | SOP 编排引擎实际连通 | P1 | mutual | Codex |
| 6 | baoyu 工具链评估是否需要 li- wrapper | P2 | mutual | Newmax |
| 7 | 触发词增强扩展到剩余 28 个 li- skill | P2 | mutual | Newmax |

---

## 5 工作区注册表空缺清单

### 个人工作区 — 应登记产出

| 产出路径 | 摘要 | 建议状态 |
|---------|------|---------|
| `projects/20260425-成长历程/` | 个人成长历程项目 | usable |
| `projects/20260504-数字先知升级/` | 数字先知系统升级 | usable |
| `projects/20260525-心理机制深度分析/` | 心理机制分析报告 | usable |
| `大学规划/` | 升学/求职/学习/校园/AI课程笔记 | usable |
| `百大认知书籍/` | 62 本认知书籍全量读取+问题拆解映射表 v2.0 | usable |
| `career-breakthrough/` | 职业突破项目 | usable |

### 创作工作区 — 应登记产出

| 产出路径 | 摘要 | 建议状态 |
|---------|------|---------|
| `outputs/AI企业服务的本质与个体突围路径.md` | AI 企业服务分析 | usable |
| `outputs/Obsidian+AI新手入门指南-v4.md` | Obsidian+AI 入门指南（最新版） | usable |
| `outputs/形势与政策-学习心得体会-李兰源-v15.md` | 形势与政策心得（最终版） | usable |
| `outputs/实习群直播-AI模拟面试-小黎实战复盘-v2.md` | AI 模拟面试复盘 | usable |
| `outputs/法学生AI公众号全链路解决方案-小黎出品.md` | 法学生 AI 方案 | usable |
| `outputs/飞书批量上传文档教程.md` | 飞书上传教程 | usable |
| `outputs/5篇文章深度分析与SOP融入-2026-05-28.md` | 文章深度分析 | usable |
| `outputs/三大AI工具集成方案-MiroFish-MemPalace-PaddleOCR.md` | AI 工具集成方案 | usable |
| `outputs/品读分析-技能生态与Agent治理-2026-06-09.md` | 技能生态分析 | usable |
| `技能注册表.md` | 创作区技能全景（核心引擎/内容生产/输入闸门） | usable |
| `公众号/` | 公众号文章库 | usable |
| `projects/20260609-小黎个人网站/` | 个人网站项目 | active |

### 学习工作区 — 应登记产出

| 产出路径 | 摘要 | 建议状态 |
|---------|------|---------|
| `projects/20260603-高等数学/` | 高等数学学习项目 | active |
| `projects/20260603-大学物理/` | 大学物理学习项目 | active |
| `projects/20260603-电路分析/` | 电路分析学习项目 | active |
| `projects/20260603-大学英语/` | 大学英语学习项目 | active |
| `projects/20260603-英语四六级/` | CET-4/6 备考项目 | active |

### 求职工作区 — 应登记产出

| 产出路径 | 摘要 | 建议状态 |
|---------|------|---------|
| `outputs/C++后端求职技能包/` | 6 篇 C++ 求职指南（心法/简历/题库/自我介绍/项目/竞赛包装） | usable |
| `outputs/AI芯片与AI应用海投_30题面试题库_20260606.md` | AI 芯片面试题库 | usable |
| `outputs/AI芯片算法岗模拟面试_20260606.md` | AI 芯片模拟面试 | usable |
| `outputs/分享会技能包/` | 分享会核心知识+HTML 演示+直播海报 | usable |
| `outputs/网易面试技能包/` | 网易运营面试准备 | usable |
| `outputs/简历研究/` | 6 轮简历迭代研究（小红书/Reddit/半导体/国企） | usable |
| `最终简历/` | 最终版简历（打印版 docx+pdf） | usable |
| `简历修改/` | 简历修改系统（SKILL.md+SOPs+经验库+模板） | usable |
| `决策/` | 求职决策系统 | usable |

### 竞赛工作区 — 应登记产出

| 产出路径 | 摘要 | 建议状态 |
|---------|------|---------|
| `outputs/CICC1001313_final_submission.zip` | 集创赛最终提交 | archived |
| `outputs/CICC1001313_竞赛最终提交材料.zip` | 集创赛提交材料 | archived |
| `outputs/2026跨校协作新场景赛项.zip` | 跨校协作赛项材料 | usable |
| `outputs/C919-皮影控制代码/` | C919 皮影戏控制代码+3D 模型 | active |
| `outputs/2026-05-30_四旋翼无人机简历STAR改写与平台调研.md` | 无人机简历 STAR 改写 | usable |
| `outputs/github_repos_watchlist.md` | GitHub 仓库监控清单 | usable |
| `projects/2026跨校协作新场景赛项/` | 跨校协作赛项（调研/方案/设备/笔记/提交） | active |
| `projects/20260609-FPGA安全通信优化规划/` | FPGA 安全通信规划 | active |
| `projects/20260609-YOLO绝缘子检测竞赛/` | YOLO 绝缘子检测 | active |
| `projects/Yolo算法比赛/` | YOLO 算法比赛 | active |

---

> 创建：2026-06-11 | Hermes v1.0 初始化
> 最后更新：2026-06-18

> 最后更新：2026-06-21（auto-consume 8 个过期 handoff）
