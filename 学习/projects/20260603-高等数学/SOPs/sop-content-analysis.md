# SOP: Content Analysis Pipeline

## Trigger Intent
用户发送 URL/链接/文章 + 包含"读/看看/分析/解读/总结"等意图词

## Input Resolution
```
IF message contains URL:
  1. IF weixin/公众号 URL → baoyu-url-to-markdown
  2. IF xiaohongshu URL → xhs-rpa-content-scraper
  3. IF youtube URL → baoyu-youtube
  4. IF github URL → WebFetch + li-research
  5. IF generic URL → WebFetch
  SAVE output to: {workspace}/outputs/article-{date}-{topic}.md
```

## Skill Chain
```
Step 1: Input Resolution (above)
Step 2: li-analyze Phase 1 — 道法术器拆解 + 百大认知注入
Step 3: li-analyze Phase 2 — 知行合一评估 + 行动建议
Step 4: li-memory Phase 1 — 事实提取（key facts, decisions, techniques）
Step 5: li-devil — 对核心结论泼冷水（optional, auto if high-confidence claims）
Step 6: li-improve — 记录本次模式 + 用户反馈
```

## Output Format
结论先行 → 原因 → 道法术器四层 → 百大认知引用 → 行动建议

## Feedback Loop
- 用户说"好/不错/有用" → 记录正模式到 golden_rules
- 用户说"不好/不对/太浅" → 采集失败模式 + 追问具体哪里差
- 每 3 次同类分析 → 自动检查是否需要升级 SOP

## Historical Precedent
- 2026-06-10: 公众号文章 → baoyu-url-to-markdown + li-analyze 道法术器
- 2026-06-10: 小红书帖子 → xhs-rpa + li-analyze 案例拆解
