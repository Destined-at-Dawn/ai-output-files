# SOP：HTML 个人站 Loop 证据链复刻

> 版本：v1.0  
> 创建：2026-06-15  
> 适用：所有 HTML 个人站、作品集、能力展示页、社群入口页、项目展示页。  
> 源经验：小黎个人站 `E:\personal_information\html自介\netlify-site\index.html`

---

## 一、核心结论

个人站不是“好看的简历墙”，而是“定位 -> 证据 -> 交付 -> 商业闭环 -> 联系入口”的证据系统。

任何 AI 复刻这个风格时，必须先解决三个问题：

1. 用户一眼知道你到底解决什么问题。
2. 用户能看到真实项目、GitHub、飞书文档、上线链接等证据。
3. 用户知道下一步点哪里、找谁、怎么合作。

---

## 二、信息架构

页面按固定链路组织：

1. Hero：身份 + 一句话定位 + 最强数据。
2. 01 Positioning：我解决什么问题。
3. 02 Proof：具体成果证据，不空讲能力。
4. 03 Delivery：我能交付什么转变。
5. 04 Business System：免费信任到付费转化的闭环。
6. 05 Connect：飞书、社群、合作、GitHub 等入口。

推荐主叙事：

```text
我在做一件事：写循环，让 AI 自己跑。
```

禁止退回旧标签堆：

- `current focus`
- `AI onboarding`
- `career expression`
- `competition delivery`
- `OPC product ladder`
- `Harness Engineering`

---

## 三、交互规则

### 3.1 按钮-only 展开

`data-detail` 只能挂在“展开细节”按钮上。

禁止：

- 整张卡片都能点击展开。
- 卡片本身加 `role="button"`。
- 卡片本身加 `tabindex`。

原因：整卡点击会让用户误触，且破坏“浏览卡片 -> 明确选择展开”的节奏。

### 3.2 FLIP 详情动效

详情层必须从来源卡片位置放大到居中详情层，不能硬切 Modal。

最低实现要求：

1. 点击按钮时读取来源卡片 `getBoundingClientRect()`。
2. 创建详情层后设置初始 `translate/scale` 到来源卡片位置。
3. 下一帧过渡到居中状态。
4. 关闭时反向回到来源卡片位置。
5. `prefers-reduced-motion` 下保留可理解的轻量过渡，不让内容突然硬跳。

---

## 四、证据嵌入规则

GitHub / 飞书 / 项目链接必须放进对应成果卡片，不做“链接墙”。

推荐映射：

- `career-breakthrough`：求职表达链路、面试/简历/表达项目。
- `research-daily`：科研日报、信息流自动化、资料筛选。
- `niuma-engine`：牛马 AI 小白配置包、工具链配置、入门系统。
- 飞书主群文档：作为“所有福利和资料”的主入口。
- 飞书小白入群指南：作为新人低门槛入口。

---

## 五、大陆入口规则

Vercel 不能作为大陆用户唯一入口。

推荐顺序：

1. `devfile.cn`：大陆主入口，适合直接发给国内用户。
2. `surge.sh`：备用入口，当前经验中大陆可直开，但仍需实测。
3. 飞书文档：兜底入口，承接资料、福利、群介绍。
4. Vercel：海外/技术备用，适合开发预览和国际访问。

每次上线后必须验证：

- HTTP 200。
- 关键文本存在。
- 桌面和移动端截图正常。
- 展开详情动效可用。
- 清理 `_codex-*`、`test-results` 等临时文件。

---

## 六、统一记录规则

这类经验必须同步四处：

1. 当前工作区：项目内 `SOPs/` 或 `AGENTS.md`，给正在执行的 AI 用。
2. 知识中枢：`E:\ai产出文件\牛马\知识中枢\04-SOP\`，给所有工作区复用。
3. Hermes 交接：写入 `E:\ai产出文件\牛马\知识中枢\05-每日记忆\YYYY-MM-DD-Codex-{主题}.md`，不要直接写 Hermes 专属 memory。
4. Skill 风格库：写入相关 skill 的 style/template/routing/golden rules。

---

## 七、关联文件

- 当前工作区 SOP：`E:\ai产出文件\牛马\创作\创作\SOPs\25_HTML个人站Loop证据链复刻SOP.md`
- 当前工作区规则：`E:\ai产出文件\牛马\创作\创作\AGENTS.md`
- li-transcript 风格：`C:\Users\13975\.newmax\skills\li-transcript\styles\style_015_loop_proof.json`
- li-transcript 模板：`C:\Users\13975\.newmax\skills\li-transcript\styles\templates\style_015_loop_proof.template.html`
- Hermes 扫描入口：`E:\ai产出文件\牛马\知识中枢\05-每日记忆\`
