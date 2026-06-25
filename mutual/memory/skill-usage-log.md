# 技能使用日志（Skill Usage Log）

> 由 li-local-search Layer 3 自动维护。每次 skill 被激活后追加一行。
> li-manage Flow E 每周六读取此文件做技能生态优化分析。

---

## 调用记录

| 日期 | 时间 | 工作区 | Skill | 触发词/场景 | 结果 | 备注 |
|------|------|--------|-------|------------|------|------|
| 2026-06-05 | 14:00 | mutual | li-bestskill | "优化find-skills"/"去外部平台找skill" | ✅ 成功 | 扫描 6 平台，发现 browse.sh 高价值工具 |
| 2026-06-05 | 14:30 | mutual | li-skillcreate | "创建li系列skill" | ✅ 成功 | 创建 li-bestskill/li-manage/li-skillfusion 三个 SKILL.md |
| 2026-06-05 | 15:00 | mutual | li-manage | "接管telos"/"个人信息处理" | ✅ 成功 | 首次执行 Flow B 全局画像初始化 |
| 2026-06-05 | 15:30 | mutual | li-local-search | "本地找skill"/"有什么技能" | ✅ 成功 | 搜索本地 196+ skill 索引 |
| 2026-06-05 | 16:00 | mutual | humanizer-zh | "去AI味" | ✅ 成功 | 新安装，首次使用 |
| 2026-06-05 | 16:00 | mutual | short-video-production | "短视频制作" | ⏳ 已安装未调用 | 等待首次真实场景使用 |
| 2026-06-05 | 16:00 | mutual | copywriting-skills | "小红书文案" | ⏳ 已安装未调用 | 等待首次真实场景使用 |
| 2026-06-05 | 16:00 | mutual | image-editing | "小红书图片" | ⏳ 已安装未调用 | 等待首次真实场景使用 |
| 2026-06-05 | 16:00 | mutual | jiaying-tool | "剪映" | ⏳ 已安装未调用 | 等待首次真实场景使用 |
| 2026-06-05 | 17:00 | mutual | li-local-search | "skill数据采集"/"调用记录" | ✅ 成功 | Layer 3 数据采集层升级 |
| 2026-06-05 | 17:00 | mutual | li-manage | "技能生态优化"/"Flow E" | ✅ 成功 | 新增 Flow E/F 模块 |

---

## 漏调记录（应调未调）

| 日期 | 任务 | 应调 Skill | 未调原因 | 原始处理方式 |
|------|------|-----------|---------|-------------|
| 2026-06-05 | 安装外部 skill | li-bestskill | 用了 find-skills 而非 li-bestskill | find-skills 搜索（已修复路由） |
| 2026-06-05 | 社群运营内容规划 | copywriting-skills | 刚安装，还没来得及调用 | 原生能力分析 |

---

## 每日统计

### 2026-06-05
- 总调用：11 次
- 成功：9 次 / 待验证：2 次（已安装未调用）
- 成功率：100%（已执行的调用）
- Top 3 高频：li-local-search(2次), li-manage(2次), li-bestskill(1次)
- 漏调：2 次
- 失败：0 次
- 新安装 skill：5 个（humanizer-zh, short-video-production, copywriting-skills, image-editing, jiaying-tool）
- 新发现需求：社群运营专项技能链（已部分解决）

---

## 月度分析

（2026-06-05 初始化，月底自动生成首份月度报告）

---

## SOP 候选

### 候选 1：社群运营内容生产链
- **指令模式**：社群运营相关（群公告/小红书引流/干货分享）
- **出现次数**：3 次（本次对话中的多个变体）
- **最近一次**：2026-06-05 — "给社群运营文件夹建立对应的技能调用"
- **现有 skill 覆盖**：humanizer-zh + copywriting-skills + image-editing + short-video-production（已安装但未串联）
- **建议**：创建"社群运营技能调用 SOP"，串联 4 个已安装 skill
- **状态**：✅ 已创建 SOP（outputs/community-ops-skill-call-sop-2026-06-05.md）
