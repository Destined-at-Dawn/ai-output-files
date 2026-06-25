# 2026-06-19 Codex 交接：li-webstyle

## 结论

已创建 `li-webstyle`：网页风格学习与多样化 HTML 生成 skill。

## 背景

用户要求参考 `li-transcript`，并“用 li-skills”设计一个能不断学习他人网页制作方式、仿照风格样式、快速生成多种不同网站和 HTML 的 skill。参考样本为：

- `https://dkfile.istester.com/Oranges/MBTIv1.27.10zhengshiban.html`

## 已完成

- Skill 已同步到：
  - `C:\Users\13975\.codex\skills\li-webstyle`
  - `C:\Users\13975\.newmax\skills\li-webstyle`
  - `C:\Users\13975\.claude\skills\li-webstyle`
- 已注册路由：
  - `C:\Users\13975\.newmax\skills\skill-routing-table.json` → `r319`
  - `C:\Users\13975\.newmax\skill-routing-table.json` → `r243`
  - `C:\Users\13975\.claude\skills\skill-routing-table.json` → `r327`
- 已生成参考页截图：
  - `F:\work\网页设计\verification\mbti-reference-page.png`
- 已生成参考页风格抽取结果：
  - `F:\work\网页设计\verification\mbti-style-brief.json`

## 重要判断

MBTI 参考页不是深色赛博风，而是浅色大留白、蓝色系统感、双模式选择卡、测评问答流、结果报告流。这个判断来自浏览器截图，不只来自 HTML 文本。

## 技能结构

- `SKILL.md`：主流程，约 102 行。
- `references/style-learning-protocol.md`：风格学习边界与八步提取法。
- `references/website-style-bank.md`：内置风格卡，含 BlueBerry 轻测评系统风。
- `references/prompt-templates.md`：DESIGN.md、单文件 HTML、多版本生成提示词。
- `references/quality-gate.md`：视觉、交互、多版本、验收门禁。
- `scripts/extract_html_style.py`：从 URL 或本地 HTML 抽取轻量风格 brief。
- `golden_rules.md`：本次经验固化。

## 注意事项

- 以后遇到“参考这个网站做 HTML / 学习这个网页风格 / 多个学生不能一样”应触发 `li-webstyle`。
- 生成多个版本时不能只换姓名或颜色，必须同时改变结构、交互、色彩、字体、文案气质。
- 单文件 HTML 动画必须渐进增强，内容默认可见。
