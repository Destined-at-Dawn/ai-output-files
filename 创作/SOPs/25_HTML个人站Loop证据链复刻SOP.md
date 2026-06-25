# SOP-25：HTML 个人站 Loop 证据链复刻 SOP

> 适用范围：个人网站、作品集、社群入口页、能力展示页、AI 项目介绍页。
> 目标：让任何 HTML 制作 AI 都能复刻“小黎个人站”这次验证过的风格、交互、证据链和大陆入口策略。

---

## 一、定位原则

### 1.1 一句话定位

个人站不是简历墙，而是一个“能力如何转成结果”的证据系统。

推荐表达：

```text
我在做一件事：写循环，让 AI 自己跑。
```

禁止回退到旧标签堆叠：

- `current focus`
- `AI onboarding`
- `career expression`
- `competition delivery`
- `OPC product ladder`
- `Harness Engineering`

### 1.2 信息架构

页面必须按这条链路组织：

1. Hero：身份 + 一句话定位 + 最强数据
2. 01 POSITIONING：我到底解决什么问题
3. 02 PROOF：结果样本，不空讲能力
4. 03 DELIVERY：我能交付什么转变
5. 04 BUSINESS SYSTEM：免费信任到付费转变的闭环
6. 05 CONNECT：明确入口，用户知道下一步做什么

### 1.3 证据优先级

证据必须具体，优先级如下：

1. 已上线链接 / GitHub 项目
2. 已发生结果：面试通过、赛事入围、社群破百
3. 可复用资产：SOP、模板、配置包、日报系统
4. 未来计划

GitHub 项目必须自然嵌入对应卡片：

- `career-breakthrough` → 求职表达链路
- `research-daily` → 科研日报 / 信息流自动化
- `niuma-engine` → 牛马 AI 小白配置包

---

## 二、视觉规范

### 2.1 基础气质

使用“浅色证据链 + 克制科技感”：

```css
:root {
  --ink: #171717;
  --ink-soft: #3f3f3f;
  --muted: #6f6f68;
  --canvas: #fbfbf8;
  --surface: #ffffff;
  --surface-soft: #f4f2ec;
  --gold: #b88a25;
  --copper: #b95724;
  --cyan: #23a9b7;
  --blue: #0a72ef;
  --radius: 8px;
}
```

必须：

- 卡片圆角 8px 左右，禁止大圆角糖果风。
- 主色不能单一紫蓝/米色/深蓝，必须有黑、铜、蓝、青的轻度对比。
- 页面留白克制，像工作台，不像营销落地页。
- 链接蓝色半粗下划线，不抢标题。

### 2.2 卡片动效

卡片只负责“质感反馈”，不要承担隐藏点击逻辑。

推荐：

```css
.glow-card {
  position: relative;
  overflow: hidden;
  transition: transform .26s cubic-bezier(.33,1,.68,1), box-shadow .3s ease;
}
.glow-card::after {
  content: "";
  position: absolute;
  left: 0; top: 0;
  height: 2px; width: 100%;
  background: linear-gradient(90deg, transparent, var(--copper), var(--gold), var(--cyan), transparent);
  transform: scaleX(0);
  transition: transform .6s cubic-bezier(.33,1,.68,1);
}
.glow-card:hover::after { transform: scaleX(1); }
```

---

## 三、展开交互铁律

### 3.1 触发范围

必须只让“展开细节”按钮触发详情，不得整张卡片都能点开。

禁止：

```html
<article data-detail="career" role="button" tabindex="0">
```

正确：

```html
<article class="proof-card glow-card">
  ...
  <button class="text-button" type="button" data-detail="career">展开细节</button>
</article>
```

原因：整卡点击误触高，用户不知道点击范围；按钮点击更符合“明确动作入口”。

### 3.2 详情层动效

详情层必须像“灵动岛”一样从来源卡片放大，不要硬切弹窗。

实现原则：

1. 点击按钮时，找到最近的卡片 `closest(".proof-card, .track, .ladder-card, .glow-card")`
2. 记录卡片 `getBoundingClientRect()`
3. modal 先缩放到卡片位置
4. 下一帧恢复到居中大面板
5. 关闭时反向收回

关键 CSS：

```css
.modal {
  transform-origin: top left;
  transition:
    transform .62s cubic-bezier(.18,.95,.22,1),
    opacity .28s ease,
    border-radius .62s cubic-bezier(.18,.95,.22,1),
    box-shadow .62s cubic-bezier(.18,.95,.22,1);
}
```

---

## 四、链接与入口策略

### 4.1 大陆入口优先级

不得把 Vercel 当作大陆用户唯一入口。

推荐排序：

1. `devfile.cn` 预览/托管链接：大陆主入口
2. `*.surge.sh`：大陆备用入口
3. 飞书文档：兜底入口，承载主群文档、小白指南、资料
4. Vercel：海外/技术备用

### 4.2 飞书链接放法

联系区必须直接放可点击飞书链接：

- 主群主文档
- 小白入群指南
- 同辈互助群详细介绍

链接写法：

```html
<a href="https://..." target="_blank" rel="noopener noreferrer">主群主文档</a>
```

---

## 五、部署验证清单

每次部署后必须验证：

1. 本地 HTML：能打开，无白屏
2. JS 语法：`new Function(script)` 不报错
3. 线上 HTTP：状态码 200
4. 内容标记：包含 `Loop Engineering` 和 GitHub 项目链接
5. 截图验证：至少检查 `#proof`、`#system`、`#contact`
6. 临时文件：删除 `_codex-*`、`test-results`

Vercel 上传前建议 `.vercelignore`：

```text
.claude
test-results
_codex-*
netlify.toml
部署说明.md
```

大陆上传包建议只包含：

```text
index.html
assets/
```

---

## 六、复刻提示词骨架

```text
请按“小黎 Loop 证据链个人站”风格制作 HTML：
1. 页面链路：Hero → 01定位 → 02成果证据 → 03交付方向 → 04商业闭环 → 05联系入口。
2. 视觉：浅色证据链、8px圆角、克制科技感、铜金青蓝细线动效。
3. 交互：只有“展开细节”按钮能展开；详情层用 FLIP 从来源卡片放大到 modal。
4. 证据：GitHub/项目链接嵌入具体成果卡，不堆项目墙。
5. 入口：大陆主入口优先 devfile.cn / surge.sh，Vercel 只做海外备用；飞书做兜底。
6. 验证：本地打开、JS解析、线上200、截图检查、清理临时文件。
```

---

## 七、反模式

- ❌ 整张卡片都能点开展开详情。
- ❌ 弹窗硬切出现，没有来源卡片放大过渡。
- ❌ 把 GitHub 项目堆成列表墙。
- ❌ Vercel 链接当大陆主入口。
- ❌ 卡片 hover 效果过重，像模板站。
- ❌ 不做线上 200 和截图验证就说部署完成。

---

## 八、统一记录协议

这类经验不能只留在当前项目里。凡是后续继续优化 HTML 个人站、作品集、社群入口页，必须同步检查四处：

1. 当前工作区：`AGENTS.md` 和本 SOP。
2. 知识中枢：`E:\ai产出文件\牛马\知识中枢\04-SOP\sop-html-loop-proof-personal-site.md`。
3. Hermes 交接：`E:\ai产出文件\牛马\知识中枢\05-每日记忆\YYYY-MM-DD-Codex-{主题}.md`。
4. Skill 风格库：`C:\Users\13975\.newmax\skills\li-transcript\` 的 style/template/routing/golden rules。

禁止直接写入 Hermes 专属目录：

```text
E:\ai产出文件\牛马\知识中枢\01-工作区记忆\hermes-memory\
```

原因：Hermes 是记忆中枢，其他工具只把事实交到每日记忆，由 Hermes 扫描、抽取、去重和检测矛盾。
