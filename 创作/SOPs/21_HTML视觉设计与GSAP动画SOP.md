# SOP-21：HTML 视觉设计与 GSAP 动画 SOP v1.0

> **适用范围**：所有 HTML 页面制作（嘉宾笔记、品牌页、产品页、落地页、社群展示页）
> **前置依赖**：html-to-notes SKILL.md（内容结构）、本 SOP（视觉设计）
> **创建日期**：2026-06-10
> **来源**：6 个参考 HTML 文件深度分析 + 3 个 GSAP 仓库学习（greensock/GSAP、gsap-skills、gsap-cc-starter）

---

## §一 设计规则总表（从 6 个参考文件提取）

> 每条规则标注来源文件（br=brand_page, bn=brand_notes, pg=product, ec=echarts, js=js_features, ag=agent），标注当前 SKILL.md 是否已覆盖。

### 1.1 配色系统

| # | 规则 | 来源 | SKILL.md 已有？ |
|---|------|------|----------------|
| C1 | 深色主题：`#0a0a0f` 主背景（非纯黑） | br, pg, ec | ✅ 已有 |
| C2 | 强调色金色渐变：`linear-gradient(135deg, #d4a853, #f0d78c)` | br, pg, ag | ❌ **新增** |
| C3 | 强调色备选蓝紫：`linear-gradient(135deg, #667eea, #764ba2)` | bn | ❌ **新增** |
| C4 | 发光效果用 `rgba(212,168,83,0.6)` 配合 `blur` | br, pg, ag | ❌ **新增** |
| C5 | 卡片背景透明度：`rgba(20,20,30,0.6)` ~ `rgba(255,255,255,0.03)` | 全部 | ⚠️ 部分 |
| C6 | 边框发光：`border: 1px solid rgba(212,168,83,0.2)` | br, pg | ❌ **新增** |
| C7 | 滚动条样式化（WebKit + Firefox） | br, pg | ❌ **新增** |

### 1.2 玻璃拟态（Glassmorphism）

| # | 规则 | 来源 | SKILL.md 已有？ |
|---|------|------|----------------|
| G1 | 卡片必须用 `backdrop-filter: blur(20px)` | 全部 | ✅ 已有 |
| G2 | 容器用半透明背景 + 圆角 + 微妙边框 | 全部 | ⚠️ 部分 |
| G3 | 发光边框用 `::before` 伪元素 + 渐变 | pg, ag | ❌ **新增** |
| G4 | 高级卡片用双层发光（`::before` 主光 + `::after` 柔和光） | pg, ag | ❌ **新增** |

### 1.3 动画与过渡

| # | 规则 | 来源 | SKILL.md 已有？ |
|---|------|------|----------------|
| A1 | 卡片 hover：`translateY(-8px)` + 边框变亮 + 阴影增强 | 全部 | ✅ 已有 |
| A2 | 全局过渡：`transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1)` | 全部 | ✅ 已有 |
| A3 | 文字光泽动画：`@keyframes shimmer` 背景渐变移动 | br, ec | ❌ **新增** |
| A4 | 旋转光环：`@keyframes rotate` + 边框渐变 | br, pg | ❌ **新增** |
| A5 | 滚动渐入：Intersection Observer + `opacity/transform` | js | ❌ **新增** |
| A6 | 数字递增动画：目标值递增 + `Intl.NumberFormat` 格式化 | js | ❌ **新增** |
| A7 | GSAP ScrollTrigger 视差滚动 | GSAP 仓库 | ❌ **新增** |
| A8 | GSAP TextPlugin 逐字/逐行文字动画 | GSAP 仓库 | ❌ **新增** |
| A9 | 卡片 shine 光扫效果：`::after` + `translateX` hover 动画 | bn | ❌ **新增** |

### 1.4 布局与响应式

| # | 规则 | 来源 | SKILL.md 已有？ |
|---|------|------|----------------|
| L1 | CSS Grid 自适应网格（`auto-fill, minmax(280px, 1fr)`） | bn, js, ec | ✅ 已有 |
| L2 | 强制响应式（`@media` 断点：1200/768/480px） | 全部 | ✅ 已有 |
| L3 | CSS `clamp()` 流体排版 | js, ec | ❌ **新增** |
| L4 | 混合布局：`display: flex` + `flex-wrap` | js | ✅ 已有 |
| L5 | Hero 区域全屏 `min-height: 100vh` + 居中 | pg, ag | ❌ **新增** |
| L6 | 导航栏固定 + 滚动变色（`scrollY > 50` 添加类） | js, ag | ❌ **新增** |

### 1.5 组件模式

| # | 规则 | 来源 | SKILL.md 已有？ |
|---|------|------|----------------|
| P1 | 统计数字卡片（大字号 + 标签 + 发光边框） | pg, ec | ❌ **新增** |
| P2 | 功能卡片（图标 + 标题 + 描述 + hover 发光） | pg, ag | ⚠️ 部分 |
| P3 | 模态框（点击遮罩关闭 + 动画进入/退出） | js | ❌ **新增** |
| P4 | Tab 切换面板（类名切换 + `display` 控制） | js | ❌ **新增** |
| P5 | 进度条动画（`IntersectionObserver` 触发） | js | ❌ **新增** |
| P6 | 工具展示区域（R2 网格 + 全宽横幅） | ec | ❌ **新增** |
| P7 | 引用容器高亮（金色渐变左边框 + 半透明背景） | pg, ag | ❌ **新增** |
| P8 | 迷你图（Sparkline）用 SVG `polyline` | ec | ❌ **新增** |

### 1.6 内容区渲染

| # | 规则 | 来源 | SKILL.md 已有？ |
|---|------|------|----------------|
| R1 | h1 只出现一次 | 全部 | ✅ 已有 |
| R2 | 数据表格 `overflow-x: auto` | ec, pg | ✅ 已有 |
| R3 | 表格横向可滑动（移动端） | ec | ⚠️ 部分 |
| R4 | `pre/code` 不换行 `white-space: pre` | 全部 | ✅ 已有 |
| R5 | a 标签自动 `_blank` + `noopener noreferrer` | 全部 | ✅ 已有 |

---

## §二 GSAP 核心集成规则

> 来源：greensock/GSAP (v3.13)、gsap-skills（官方插件库）、gsap-cc-starter（Cloudflare Workers 全栈模板）

### 2.1 GSAP 核心概念

**GSAP = GreenSock Animation Platform**，业界最专业的 JS 动画库。

```
核心对象：gsap.to() / gsap.from() / gsap.fromTo() / gsap.timeline()
核心插件：ScrollTrigger / TextPlugin / Flip / Draggable / MorphSVG
CDN 引入：<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js">
```

**与 CSS 动画的区别**：
- CSS 动画：声明式、简单过渡、性能好、但控制力有限
- GSAP：命令式、精确控制时间线、复杂序列、ScrollTrigger 滚动驱动

**选择原则**：
- 简单 hover/过渡 → 用 CSS（零依赖）
- 滚动驱动/复杂序列/文字动画 → 用 GSAP
- 两者可以共存（CSS 做基础状态，GSAP 做高级效果）

### 2.2 GSAP 必会模式（5 种）

#### 模式 1：元素渐入（ScrollTrigger）

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

<style>
.animate-in {
  opacity: 0;
  transform: translateY(40px);
  transition: none; /* GSAP 接管，关掉 CSS transition */
}
</style>

<script>
gsap.registerPlugin(ScrollTrigger);

// 卡片依次渐入
gsap.utils.toArray('.animate-in').forEach((el, i) => {
  gsap.to(el, {
    opacity: 1,
    y: 0,
    duration: 0.8,
    delay: i * 0.1,
    ease: 'power2.out',
    scrollTrigger: {
      trigger: el,
      start: 'top 85%',
      toggleActions: 'play none none none'
    }
  });
});
</script>
```

#### 模式 2：文字逐字/逐行动画（TextPlugin）

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/TextPlugin.min.js"></script>

<script>
gsap.registerPlugin(TextPlugin);

// 逐字出现
gsap.to('.hero-title', {
  text: { value: '用 AI 驱动知识生产', delimiter: '' },
  duration: 2,
  ease: 'none'
});

// 逐行渐入
gsap.from('.hero-subtitle', {
  opacity: 0,
  y: 20,
  duration: 1,
  delay: 2.5
});
</script>
```

#### 模式 3：时间线序列（Timeline）

```javascript
const tl = gsap.timeline({ defaults: { ease: 'power2.out' } });

tl.from('.hero-badge', { opacity: 0, y: -20, duration: 0.6 })
  .from('.hero-title', { opacity: 0, y: 30, duration: 0.8 }, '-=0.3')
  .from('.hero-subtitle', { opacity: 0, y: 20, duration: 0.6 }, '-=0.4')
  .from('.hero-cta', { opacity: 0, scale: 0.8, duration: 0.5 }, '-=0.2');
```

#### 模式 4：视差滚动（Parallax）

```javascript
gsap.to('.parallax-bg', {
  yPercent: -30,
  ease: 'none',
  scrollTrigger: {
    trigger: '.hero',
    start: 'top top',
    end: 'bottom top',
    scrub: true
  }
});
```

#### 模式 5：数字递增动画

```javascript
function animateCounter(el) {
  const target = parseInt(el.dataset.count);
  gsap.fromTo(el,
    { textContent: 0 },
    {
      textContent: target,
      duration: 2,
      ease: 'power1.out',
      snap: { textContent: 1 },
      onUpdate() {
        el.textContent = new Intl.NumberFormat().format(
          Math.round(el.textContent)
        );
      }
    }
  );
}

document.querySelectorAll('[data-count]').forEach(el => {
  ScrollTrigger.create({
    trigger: el,
    start: 'top 80%',
    once: true,
    onEnter: () => animateCounter(el)
  });
});
```

### 2.3 GSAP 插件清单

| 插件 | 用途 | CDN | 场景 |
|------|------|-----|------|
| **ScrollTrigger** | 滚动驱动动画 | 内置 | 渐入、视差、固定 |
| **TextPlugin** | 文字替换动画 | 内置 | 打字机效果 |
| **Flip** | 布局变化动画 | 内置 | 排序、过滤 |
| **ScrollSmoother** | 平滑滚动 | Club | 高级滚动体验 |
| **Draggable** | 拖拽交互 | 内置 | 可拖拽卡片 |
| **MorphSVG** | SVG 形变 | Club | 图标动画 |
| **DrawSVG** | SVG 描边动画 | Club | 路径绘制 |
| **SplitText** | 文字拆分 | Club | 逐字/逐行动画 |

> **Club 插件**需要 GSAP Club 会员。免费项目只用内置插件。
> **gsap-skills** 仓库提供官方示例代码，可直接参考。

### 2.4 GSAP 与 GSAP-CC-Starter（Cloudflare Workers 部署）

**gsap-cc-starter** 展示了如何用 Cloudflare Workers 部署 GSAP 动画页面：

```
架构：Hono (后端框架) + GSAP (前端动画) + Cloudflare Workers (部署)
特点：零服务器、全球 CDN、边缘计算
适用：产品落地页、品牌展示页
```

**对我们有用的部分**：
- 动画页面可以纯前端部署到 Cloudflare Pages（免费）
- GSAP + ScrollTrigger 做首屏动画，不需要后端
- 配合 `baoyu-markdown-to-html` 生成的静态页面可以直接部署

---

## §三 CSS 代码模式库（从参考文件提取的可复用片段）

### 3.1 全局基础样式

```css
/* ============ 基础重置 + 全局变量 ============ */
:root {
  --bg-primary: #0a0a0f;
  --bg-secondary: #12121a;
  --bg-card: rgba(255, 255, 255, 0.03);
  --accent-gold: linear-gradient(135deg, #d4a853, #f0d78c);
  --accent-blue: linear-gradient(135deg, #667eea, #764ba2);
  --accent-gold-solid: #d4a853;
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --text-muted: rgba(255, 255, 255, 0.4);
  --border-subtle: rgba(255, 255, 255, 0.1);
  --border-gold: rgba(212, 168, 83, 0.2);
  --glass-blur: 20px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --shadow-glow: 0 0 30px rgba(212, 168, 83, 0.1);
  --shadow-glow-strong: 0 4px 30px rgba(212, 168, 83, 0.2);
  --transition-default: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
```

### 3.2 滚动条样式化

```css
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(212, 168, 83, 0.3);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(212, 168, 83, 0.5); }
* { scrollbar-width: thin; scrollbar-color: rgba(212, 168, 83, 0.3) transparent; }
```

### 3.3 卡片发光边框（伪元素法）

```css
.glow-card {
  position: relative;
  background: var(--bg-card);
  backdrop-filter: blur(var(--glass-blur));
  border-radius: var(--radius-lg);
  overflow: hidden;
}

/* 发光边框 */
.glow-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-lg);
  padding: 1px;
  background: linear-gradient(
    135deg,
    rgba(212, 168, 83, 0.3),
    transparent,
    rgba(102, 126, 234, 0.2)
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

/* 柔和外发光 */
.glow-card::after {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, rgba(212, 168, 83, 0.1), transparent);
  filter: blur(15px);
  opacity: 0;
  transition: opacity 0.4s;
  pointer-events: none;
  z-index: -1;
}

.glow-card:hover::after { opacity: 1; }
```

### 3.4 文字光泽动画（Shimmer）

```css
.shimmer-text {
  background: linear-gradient(90deg, #d4a853, #f0d78c, #d4a853);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

### 3.5 旋转光环

```css
.rotating-ring {
  position: relative;
  display: inline-block;
}

.rotating-ring::before {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  background: conic-gradient(from 0deg, #d4a853, transparent, #d4a853);
  animation: rotate 3s linear infinite;
  z-index: -1;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

### 3.6 卡片 Shine 光扫效果

```css
.shine-card {
  position: relative;
  overflow: hidden;
}

.shine-card::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 50%;
  height: 200%;
  background: linear-gradient(
    to right,
    transparent,
    rgba(255, 255, 255, 0.05),
    transparent
  );
  transform: rotate(25deg) translateX(-150%);
  transition: transform 0.6s;
  pointer-events: none;
}

.shine-card:hover::after {
  transform: rotate(25deg) translateX(200%);
}
```

### 3.7 统计数字组件

```css
.stat-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-gold);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: center;
}

.stat-number {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 700;
  background: var(--accent-gold);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-top: 4px;
}
```

### 3.8 引用容器高亮

```css
blockquote, .callout {
  background: rgba(212, 168, 83, 0.05);
  border-left: 3px solid;
  border-image: linear-gradient(to bottom, #d4a853, #f0d78c) 1;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: 16px 20px;
  margin: 16px 0;
}
```

### 3.9 Hero 区域

```css
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 80px 24px 40px;
  position: relative;
  overflow: hidden;
}

.hero-title {
  font-size: clamp(2rem, 6vw, 4rem);
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 20px;
}

.hero-subtitle {
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 32px;
}
```

### 3.10 固定导航栏 + 滚动变色

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 16px 40px;
  transition: var(--transition-default);
}

.navbar.scrolled {
  background: rgba(10, 10, 15, 0.9);
  backdrop-filter: blur(20px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}
```

```javascript
window.addEventListener('scroll', () => {
  document.querySelector('.navbar')
    .classList.toggle('scrolled', window.scrollY > 50);
});
```

### 3.11 Tab 切换

```css
.tab-btn {
  background: transparent;
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  padding: 8px 20px;
  border-radius: 20px;
  cursor: pointer;
  transition: var(--transition-default);
}

.tab-btn.active {
  background: var(--accent-gold);
  color: #000;
  border-color: transparent;
}

.tab-panel { display: none; }
.tab-panel.active { display: block; }
```

### 3.12 模态框

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.modal-overlay.active { display: flex; }

.modal-content {
  background: var(--bg-secondary);
  border: 1px solid var(--border-gold);
  border-radius: var(--radius-xl);
  padding: 32px;
  max-width: 600px;
  width: 90%;
  animation: modalIn 0.3s ease;
}

@keyframes modalIn {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
```

---

## §四 响应式断点标准

```css
/* 桌面端（默认） */
/* 平板 */  @media (max-width: 1200px) { ... }
/* 手机 */  @media (max-width: 768px) { ... }
/* 小手机 */ @media (max-width: 480px) { ... }
```

### 断点内必查项

| 断点 | 必查 |
|------|------|
| 1200px | Grid 列数是否减少？侧边栏是否隐藏？ |
| 768px | 导航是否折叠？字体是否用 `clamp()`？表格是否可横滑？ |
| 480px | 按钮是否全宽？卡片是否单列？内边距是否减小？ |

### 流体排版公式

```css
/* clamp(最小值, 首选值, 最大值) */
h1 { font-size: clamp(1.8rem, 5vw, 3rem); }
h2 { font-size: clamp(1.4rem, 3vw, 2rem); }
body { font-size: clamp(0.9rem, 2vw, 1rem); }
```

---

## §五 自审 Checklist（14 项，交付前逐项打勾）

| # | 检查项 | 来源 |
|---|--------|------|
| 1 | `<head>` 含 charset、viewport、title、description | §三 |
| 2 | 所有样式内联在 `<style>` 中 | §三 |
| 3 | 深色背景 + 无外部字体/图片依赖 | §三 |
| 4 | 代码区深色独立背景 + `white-space: pre` | §三 |
| 5 | 链接均 `target="_blank"` + `noopener noreferrer` | §三 |
| 6 | h1 只出现一次 | §三 |
| 7 | CSS 渐变用 4-8 色（非默认 3 色） | §五-CSS |
| 8 | 背景含渐变噪点纹理层（noise texture） | §五-CSS |
| 9 | 配色不超过 3 种（背景+强调+中性） | §五 |
| 10 | 视觉层次 > 内容准确性（顺序：大标题→结构→正文→校对） | §五 |
| 11 | 卡片 hover 有 `translateY(-8px)` + 边框变亮 | §七 |
| 12 | 全局过渡用 `cubic-bezier(0.4, 0, 0.2, 1)` | §七 |
| 13 | 响应式三个断点均已测试 | §四 |
| 14 | 自然语言描述（非代码注释）标注可选/未验证部分 | §七 |

---

## §六 参考文件索引

| 编号 | 文件 | 定位 | 规则数 |
|------|------|------|--------|
| br | brand_page.html | 品牌页 CSS 模式库 | 12 |
| bn | brand_notes.html | 笔记页布局模板 | 10 |
| pg | product_page.html | 产品页完整示例 | 15 |
| ec | echarts_brand.html | 数据可视化页 | 8 |
| js | js_features.html | JS 交互组件 | 20 |
| ag | agent_brand_page.html | 复杂动画页 | 14 |

---

## §七 与 html-to-notes SKILL.md 的关系

```
SOP-21（视觉设计）  ← 你在这里
    ↓ 提供
html-to-notes SKILL.md Step 4（CSS 渲染规则）
    ↓ 输出
最终 HTML 文件
```

**分工**：
- SKILL.md 管**内容结构**（章节骨架、块级元素规范、嵌套规则）
- SOP-21 管**视觉设计**（配色、动画、组件、GSAP、响应式）
- 两者在 Step 4（CSS 渲染规则）交汇

**升级路径**：SOP-21 的新增规则应同步写入 SKILL.md Step 4 的对应小节。

---

## 变更记录

| 日期 | 版本 | 变更摘要 |
|------|------|---------|
| 2026-06-10 | v1.0 | 初始创建。从 6 个参考 HTML 文件提取 47 条设计规则 + 3 个 GSAP 仓库学习（核心概念 + 5 种必会模式 + 插件清单 + Cloudflare 部署），整合为 SOP-21（7 章节 + 14 项自审 checklist）。 |
