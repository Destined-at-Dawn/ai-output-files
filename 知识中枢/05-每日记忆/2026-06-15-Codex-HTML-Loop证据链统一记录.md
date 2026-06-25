# 2026-06-15 Codex 交接：HTML 个人站 Loop 证据链统一记录

## 事件

Codex 已将“小黎个人站”这次验证过的 HTML 风格、交互、证据链和部署经验，从单次经验升级为可复用规则。

## 已落盘

- 当前工作区 SOP：`E:\ai产出文件\牛马\创作\创作\SOPs\25_HTML个人站Loop证据链复刻SOP.md`
- 知识中枢全局 SOP：`E:\ai产出文件\牛马\知识中枢\04-SOP\sop-html-loop-proof-personal-site.md`
- 当前工作区规则：`E:\ai产出文件\牛马\创作\创作\AGENTS.md` 第 22 节
- li-transcript 风格：`C:\Users\13975\.newmax\skills\li-transcript\styles\style_015_loop_proof.json`
- li-transcript 模板：`C:\Users\13975\.newmax\skills\li-transcript\styles\templates\style_015_loop_proof.template.html`

## 需要 Hermes 记住的原子事实

- [事实] HTML 个人站/作品集/社群入口页应优先使用“定位 -> 证据 -> 交付 -> 商业闭环 -> 联系入口”的 Loop 证据链结构。[来源: E:\ai产出文件\牛马\知识中枢\04-SOP\sop-html-loop-proof-personal-site.md#12] [置信度: 高] [时间: 2026-06-15]
- [事实] 个人站详情展开必须采用按钮-only 触发，`data-detail` 只能挂在“展开细节”按钮上，禁止整张卡片触发展开。[来源: E:\ai产出文件\牛马\知识中枢\04-SOP\sop-html-loop-proof-personal-site.md#45] [置信度: 高] [时间: 2026-06-15]
- [事实] 个人站详情层应采用 FLIP 动效，从来源卡片放大到居中详情层，避免硬切 Modal。[来源: E:\ai产出文件\牛马\知识中枢\04-SOP\sop-html-loop-proof-personal-site.md#61] [置信度: 高] [时间: 2026-06-15]
- [事实] 面向大陆用户的 HTML 站点不能只给 Vercel，主入口优先 devfile.cn，surge.sh 备用，飞书文档兜底，Vercel 作为海外/技术备用。[来源: E:\ai产出文件\牛马\知识中枢\04-SOP\sop-html-loop-proof-personal-site.md#88] [置信度: 高] [时间: 2026-06-15]
- [事实] li-transcript 已新增 `loop_proof_personal_site` 风格，用于逐字稿转个人站/作品集/项目展示页。[来源: C:\Users\13975\.newmax\skills\li-transcript\references\style-guide.md#357] [置信度: 高] [时间: 2026-06-15]

## 给后续 AI 的启动注入

如果用户要求“做 HTML 个人站 / 作品集 / 个人介绍页 / 社群入口页 / 项目展示页”，先读：

1. `E:\ai产出文件\牛马\知识中枢\04-SOP\sop-html-loop-proof-personal-site.md`
2. `E:\ai产出文件\牛马\创作\创作\SOPs\25_HTML个人站Loop证据链复刻SOP.md`
3. `C:\Users\13975\.newmax\skills\li-transcript\references\style-guide.md` 中的 `Loop证据链个人站（style_015）`

不要直接写入 Hermes 专属目录 `hermes-memory/`，由 Hermes 后续扫描本文件并提取原子事实。
