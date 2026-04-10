# 技术约束与质量底线（所有生成任务共用）

> 本文件只定义**不可逾越的硬约束**。设计决策、区块组合、视觉风格、动效实现方式均不在此规定，由 generator.md 的迭代流程自主决定。

---

## 一、文件交付约束（100%强制）

- 输出严格为单一 `index.html`，CSS 和 JS 全部内联
- 禁止任何 JS 框架（jQuery / React / Vue / Alpine 等）
- 禁止外部 CSS 文件（Google Fonts CDN 除外）
- 图片只使用 `https://images.unsplash.com/` URL
- 图标只使用内联 SVG（参考 Lucide / Heroicons），禁止 icon font / CDN 图标库
- 禁止引用 `cdn.tailwindcss.com` 或任何 Tailwind CDN
- 禁止 Cloudflare `cdn-cgi` 代码
- 双击 `index.html` 可直接在浏览器运行，无需编译

---

## 二、代码质量约束

- 语义化 HTML 标签（`<nav>` `<section>` `<article>` `<footer>` 等）
- CSS 变量统一管理所有颜色、字体、间距（`:root { --xxx: }`)
- 禁止使用纯原始色（#FF0000 / #0000FF / #00FF00 等）
- 必须使用 Google Fonts 专业字体，禁止系统默认字体
- 浏览器控制台无 JS 报错
- 文件末尾必须有完整的 `</body></html>` 闭合标签
- 注释清晰分区，每个主要区块必须有分区注释（`/* ====== HERO ====== */`）

---

## 三、交互动效底线（必须至少满足8项）

以下为**最低要求**，不是实现清单。具体实现方式、创意程度由生成流程自由发挥：

---

### ⚠️ 功能性交互强制规范（一票否决项）

> **来源：Benchmark v3 甲方反审意见（17条通过 vs 56条不合格案例分析）**
>
> 以下交互是**硬性验收条件**，缺少任意一项即判不通过，无论 Prompt 多长、视觉多精美。

| 功能交互 | 不合格率 | 最低要求 | Prompt 中必须写明的内容 |
|---------|:------:|---------|----------------------|
| **Modal 弹窗** | 92% 缺失 | ≥ 1 个 | 触发元素 + 弹窗内容 + ESC键关闭 + backdrop点击关闭 + focus trap + `aria-modal="true"` |
| **FAQ Accordion** | 87% 缺失 | ≥ 5 题 | smooth height 动画（JS 动态 scrollHeight）+ 图标旋转 180deg + 互斥展开 + `aria-expanded` |
| **Toast 通知** | 96% 缺失 | ≥ 1 处 | CTA 点击触发 + 通知内容文字 + 自动消失时长（≥ 3s）+ 关闭按钮 + 进退场动画 |
| **Tab 切换** | 高频缺失 | ≥ 1 组(≥3 tab) | 滑动指示线 + 内容 fade 切换 + `role="tablist"` + 键盘左右箭头切换 |
| **数字计数** | 83% 缺失 | ≥ 3 个数字 | `requestAnimationFrame` + `easeOutExpo` + 视口触发 + duration 2s |
| **Scroll Reveal** | 全页 | 全页覆盖 | `IntersectionObserver` + threshold 0.15 + stagger delay 150ms/card |
| **导航栏滚动态** | 必须 | 必须 | 80px 阈值 + `backdrop-filter:blur` + shadow + 300ms transition |

**"不算功能交互"的清单**（以下只是视觉效果，不能用于满足上表要求）：

| ❌ 不算交互 | ✅ 算交互 |
|-----------|---------|
| scroll reveal 渐入 | Modal 弹窗（有内容、可关闭） |
| hover 变色/阴影/位移 | Tab 切换（内容实际变化） |
| 进度条/技能条动画 | Accordion 展开/收起 |
| 文字打字/scramble 效果 | 筛选/过滤（数据变化） |
| 背景粒子/光晕浮动 | Toast 操作反馈 |
| 锚点跳转 | 图片画廊 prev/next 切换 |
| 遮罩透明度切换 | 表单验证 + 提交反馈 |
| 短暂缩放/形变 hover 反馈 | 排序（列表重排） |

**完整交互链路定义**（每条链路必须 ≥ 3 步）：
```
触发           →    系统反馈           →    后续可操作
─────              ──────────              ──────────
点击卡片      →    弹出 Modal 详情层   →    可查看详情 / 关闭
点击筛选按钮  →    列表数据实时过滤    →    可清除筛选
点击 Tab      →    内容区切换 + 动画   →    可切换其他 Tab
展开 FAQ      →    内容滑出 + 图标旋转 →    可收起
提交表单      →    Toast 确认反馈      →    表单重置
```

> **反面教材**：写了 17514 字符的 Prompt 因功能交互缺位仍不通过（fdu_052）。写了"7 种交互类型"但全是 hover 效果、点击无反应（fdu_137）。

---

**基础层（必须全部满足）：**
1. 所有卡片/内容块 hover：必须同时改变**位置+尺寸+颜色**三个维度（禁止单维度hover）
2. 所有按钮 hover / active / focus-visible **四态**均有视觉反馈（default → hover → active → focus-visible）
3. 至少三处不同的 CSS `@keyframes` 动画
4. 导航栏滚动后有背景变化（`backdrop-filter` 或背景色过渡）+ 链接hover下划线动效

**进阶层（至少满足4项）：**
5. 光标体验——必须从【光标变体表】（CUR-A 到 CUR-X）中选一种，且受冷却约束（连续5条不重复；CUR-A dot+ring 连续3条最多1次）；CUR-X 无自定义光标也是合法选项，此时必须用极致三态 hover 补偿
6. 功能组件——从【组件大类表】中轮换选取（连续3条不得重复同大类，详见generator.md）
7. 数据/数字展示——计数器 / 实时Ticker / 圆环进度 / SVG图表，任选其一（非每页强制）
8. 无限滚动轨道或主技法对应的核心交互（必须在主内容区明显可见）
9. 滚动进度条（适合叙事/内容/SaaS页面）或 滚动驱动动画；**游戏/全互动型页面此项可跳过**，改用其他进阶项（第7、8、10项之一）作为替代满足计数
10. 表单/输入框 focus 状态 + 交互反馈（success toast / 按钮状态变化）

**趣味互动层（必须满足1项，鼓励2项）：**
11. 可玩 Canvas（涂鸦板 / 刮刮卡 / 点击粒子爆炸 / 噪点生成器）
12. 物理/弹性互动（弹跳卡片 / 可拖拽重排 / 磁吸按钮群 / 弹簧吸附效果）
13. 实时视觉化（均衡器频谱 / 鼠标响应粒子场 / SVG手绘路径触发 / 波浪文字变形）
14. 功能性互动 Demo（拖拽排序 / 实时搜索过滤 / 颜色主题切换器 / 分屏对比滑块）
15. 叙事式触发（滚动驱动多帧故事 / 聚光灯揭示区域 / 卡片翻转解锁剧情）
16. 隐藏触发彩蛋（Konami码 / 连续点击 / hover序列——可选，不再强制）

> **趣味互动层规则**：选择的互动必须与品牌气质匹配，不是为了加而加。每项互动须在页面中占据一个可见区域，不能藏在折叠内容里。

**交互密度规则（新增）：**
- 每200px高度至少1个可交互元素
- 所有hover必须是"三维度联动"：位置（translate）+ 尺寸（scale/shadow）+ 颜色（background/border/color）同时变化
- SPA多页面：每个子页面必须有独立的入场动画

**Scroll Reveal 实现规范（防黑屏）：**

根据页面风格选择一种揭示变体（**连续3条不得使用相同变体**）：

| 变体 | `.reveal.hidden` 状态 | 适用气质 |
|------|----------------------|---------|
| fade-up（默认）| `opacity:0; transform:translateY(32px)` | 通用 |
| fade-right | `opacity:0; transform:translateX(-24px)` | 横向叙事/时间线 |
| scale-up | `opacity:0; transform:scale(0.94)` | 卡片/产品图 |
| blur-in | `opacity:0; filter:blur(8px); transform:scale(0.98)` | 摄影/wellness/奢侈品 |
| clip-down | `clip-path:inset(0 0 100% 0); opacity:0`（父元素需 overflow:hidden） | 标题揭示/剧场感 |

`.reveal` 显示态统一为 `opacity:1; transform:none; filter:none; clip-path:none`，transition 统一：
```css
.reveal { opacity: 1; transform: none; filter: none; clip-path: none; transition: opacity 0.85s cubic-bezier(0.16,1,0.3,1), transform 0.85s cubic-bezier(0.16,1,0.3,1), filter 0.85s, clip-path 0.85s; }
```
JS：用双重 `requestAnimationFrame` 初始化，先加 `.hidden` 再 observe，防止首屏黑屏。

---

## 四、按钮功能约束（禁止死按钮）

- 每个 `<section>` 必须有正确的 `id` 属性
- CTA 按钮必须有实际跳转目标（锚点滚动 / modal / Toast）
- 功能性按钮（Tab切换 / FAQ手风琴 / 轮播箭头）必须有 JS 响应

**按钮标签规范（防状态栏弹出）：**

> **核心原则**：鼠标悬停任何可点击元素时，浏览器左下角**不得出现任何文字**。只要 `<a>` 标签带有 `href`，浏览器就会显示其值——无论是 `#`、`#section-id`、还是 `javascript:goSlide(1)`，全部会污染状态栏。

**唯一正确做法：所有页内交互一律用 `<button>`，永远不用 `<a href>`。**

```js
// 定义统一滚动函数（不能命名 scrollTo，与原生冲突）
function navTo(id) {
  document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}
// 正确: <button onclick="navTo('hero')">Home</button>
// 正确: <button onclick="showPanel(2)">Gallery</button>
// 正确: <button onclick="goSlide(1)">Next</button>   ← 函数名随意，但必须是 button
```

**绝对禁止的所有写法**（无论是导航、占位、footer 还是任何交互）：

| 禁止写法 | 状态栏显示 |
|---------|-----------|
| `<a href="#">` | `#` |
| `<a href="#hero">` | `#hero` |
| `<a href="javascript:void(0)">` | `javascript:void(0)` |
| `<a href="javascript:goSlide(1)">` | `javascript:goSlide(1)` |
| `<a href="javascript:0">` | `javascript:0` |
| `<a href="#" onclick="...">` | 显示 `#`，onclick 无法消除 |
| `<a onclick="..." href="#id">` | 显示 `#id` |

**合法的 `<a>` 用法**（仅此一种）：
```html
<!-- 只有真实外链才能用 <a>，必须有 target="_blank" -->
<a href="https://instagram.com/brand" target="_blank" rel="noopener">Instagram</a>
```

**footer / 隐私 / 条款等占位链接**：用 `<button>` 或纯文本 `<span>`，不加任何 href：
```html
<button class="footer-link">Privacy Policy</button>
<button class="footer-link">Terms of Service</button>
```

- 所有 `<button>` 必须在 CSS **最顶部**（紧接 `*, *::before, *::after` 重置之后）加入全局 reset：
```css
button {
  background: none;
  border: none;
  padding: 0;
  font: inherit;
  color: inherit;
  cursor: pointer;
}
```
- 之后在此基础上叠加设计样式，外观与原设计完全一致

**⚠️ CSS 选择器双覆盖规则（高频漏写点）：**
导航链接、移动端菜单、页脚链接的 CSS 选择器，**必须同时覆盖 `a` 和 `button`**，否则用 `<button>` 实现的导航将显示为浏览器默认样式（灰色方块）：
```css
/* ✅ 正确写法 — 同时覆盖 a 和 button */
.nav-links a,
.nav-links button { font-size: 14px; color: var(--text); ... }

.nav-links a:hover,
.nav-links button:hover { color: var(--accent); }

.mobile-menu a,
.mobile-menu button { font-size: 1.2rem; color: var(--text); ... }

.footer-col a,
.footer-col button { color: rgba(255,255,255,0.5); ... }

/* ❌ 错误写法 — 只写 a，button 会显示为默认样式 */
.nav-links a { ... }        /* button 不受影响，仍是灰色方块 */
.mobile-menu a { ... }      /* 同上 */
```

**移动端菜单关闭监听器也必须同时覆盖 `button`：**
```js
// ✅ 正确
mobileMenu.querySelectorAll('a, button').forEach(el => {
  el.addEventListener('click', closeMobileMenu);
});
// ❌ 错误 — button 点击后菜单不会关闭
mobileMenu.querySelectorAll('a').forEach(a => { ... });
```

---

## 五、视觉质量底线

- 禁止图片裂图（提交前必须验证 Unsplash URL 可访问）
- 禁止五角星评分组件（`★★★★★`），用引言/媒体logo/数字成就替代
- 禁止通用三列 Features 卡片作为**唯一**内容展示形式
- **Features 冷却规则（新增）**：连续 2 条内 Features 板块不得以"三列/四列矩形卡片 + 图标 + 标题 + 说明文" 的标准形式出现。若必须展示功能点，必须选择下方替代布局之一（见 §十二）
- 禁止原生滚动条样式，必须自定义 `::-webkit-scrollbar`
- section 之间不得无任何视觉过渡（细线 / 渐变 / 色块均可）
- **禁止纯黑背景（`#000000` / `#000` / `rgb(0,0,0)`）**：暗色主题必须使用有色深色调，例如深蓝（`#0a0f1e`）、深紫（`#12081e`）、深绿（`#071a12`）、深棕（`#1a0f08`）等，令画面有温度和质感
- **叙事风格频率约束**：连续 3 条内不得以"品牌故事/叙事长滚动页（Narrative Scroll）"作为主要形式；功能型、工具型、游戏型、互动展示型页面应占比 ≥ 50%

---

## 六、响应式底线

- **390px（iPhone 14 标准宽度）**：无横向滚动（`body { overflow-x: hidden }`），汉堡菜单，按钮 full-width —— **甲方验收必查项**
- 768px：单列布局，隐藏桌面导航链接，卡片堆叠
- 1024px：中间过渡布局，Grid 变 2 列
- 移动端字体层级需保持合理（不得过小或过大）
- Tab 栏在移动端改为 `overflow-x: auto; white-space: nowrap`（可横向滚动，隐藏滚动条）
- Modal 在移动端：`width: 95vw; max-height: 92vh; padding: 28px`

---

## 七、禁止事项汇总

| 禁止项 | 原因 |
|--------|------|
| `./images/xxx.png` 本地路径 | 无法运行 |
| jQuery / React 等 CDN 框架 | 需编译/依赖 |
| `cdn.tailwindcss.com` | 外部CSS框架 |
| Cloudflare `cdn-cgi` | 邮件混淆代码 |
| `★★★★★` 星级评分 | 视觉低质 |
| 无响应死按钮 | 交互规范违规 |
| `href="#"` / `href="#id"` / `href="javascript:..."` | 状态栏污染，视觉观感差 |
| 控制台 JS 报错 | 代码质量 |
| 图片裂图 | 提交被驳回 |
| 缺少 `</body></html>` | 代码不完整 |
| 全屏十字准心光标（竖线/横线覆盖全视口） | 视觉低质，参见 §十一 §11.4 |

---

## 八、动画系统强制规范（Animation System — 必须完整实现）

> 每条 HTML 都必须实现下方列出的**完整动画系统**。不是可选项，是底线。

### 8.1 必须包含的 5 类 @keyframes（或主题等效版本）

```css
/* 1. 按钮点击闪光 */
@keyframes btn-flash {
  0%   { opacity: 1; }
  20%  { opacity: 0.15; }
  40%  { opacity: 1; }
  60%  { opacity: 0.4; }
  100% { opacity: 1; }
}

/* 2. 按钮点击颤抖 */
@keyframes btn-shake {
  0%,100% { transform: translateX(0); }
  20%     { transform: translateX(-6px); }
  40%     { transform: translateX(6px); }
  60%     { transform: translateX(-4px); }
  80%     { transform: translateX(4px); }
}

/* 3. 点击涟漪扩散（配合 JS 注入 .ripple 元素） */
@keyframes ripple-expand {
  0%   { transform: translate(-50%,-50%) scale(0); opacity: 0.55; }
  100% { transform: translate(-50%,-50%) scale(4); opacity: 0; }
}
/* .ripple { position:absolute; width:16px; height:16px; border-radius:50%;
   background:rgba(accent,0.35); pointer-events:none; animation:ripple-expand 0.6s ease-out forwards; } */

/* 4. 卡片点击弹跳 */
@keyframes card-bounce {
  0%,100% { transform: translateY(0) scale(1); }
  35%     { transform: translateY(-14px) scale(1.06); }
  65%     { transform: translateY(-6px) scale(1.02); }
}

/* 5. 光晕呼吸（Logo/高亮元素常驻动画） */
@keyframes glow-pulse {
  0%,100% { box-shadow: 0 0 8px var(--accent), 0 0 16px var(--accent); }
  50%     { box-shadow: 0 0 20px var(--accent), 0 0 40px var(--accent), 0 0 60px rgba(accent,0.3); }
}
/* text版：text-shadow: 0 0 8px var(--accent) ↔ 0 0 32px var(--accent) */
```

> **主题等效**：以上 keyframe 名称可根据品牌风格改名（如 `@keyframes pixel-flash`），但**效果必须存在**。

### 8.2 JS 全局涟漪系统（必须实现）

所有 `<button>`、`<a>`、`.card`、`.interactive` 元素必须在 click 事件时注入涟漪：

```javascript
// 全局涟漪 — 放在 </script> 前
document.addEventListener('click', e => {
  const target = e.target.closest('button, a, [class*="card"], [class*="btn"], [class*="interactive"]');
  if (!target) return;
  const r = document.createElement('div');
  r.className = 'ripple';
  const rect = target.getBoundingClientRect();
  r.style.left = (e.clientX - rect.left) + 'px';
  r.style.top  = (e.clientY - rect.top)  + 'px';
  target.style.overflow = 'hidden';
  target.style.position = 'relative';
  target.appendChild(r);
  setTimeout(() => r.remove(), 650);
});
```

### 8.3 按钮必须实现的三态动画

```css
/* 所有主CTA按钮 */
.btn-primary:hover  { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(accent,0.35); }
.btn-primary:active { animation: btn-flash 0.4s ease; transform: translateY(0) scale(0.96); }

/* 所有次要按钮/ghost */
.btn-secondary:hover  { transform: scale(1.04); }
.btn-secondary:active { animation: btn-shake 0.45s ease; }
```

### 8.4 卡片必须实现的三维度联动 hover

```css
/* 每张卡片 hover 必须同时改变：位置 + 尺寸/阴影 + 颜色 — 三个维度缺一不可 */
.card:hover {
  transform: translateY(-8px) scale(1.02);        /* 位置 + 尺寸 */
  box-shadow: 0 24px 48px rgba(0,0,0,0.2);        /* 立体感 */
  border-color: var(--accent);                    /* 颜色 */
  background: var(--card-hover-bg);               /* 颜色2（可选） */
}
/* active 点击弹跳 */
.card:active { animation: card-bounce 0.5s cubic-bezier(0.34,1.56,0.64,1); }
```

### 8.5 入场动画必须有交错延迟（Stagger）

```css
/* 网格/列表中的子元素必须有 CSS 变量控制 stagger delay */
.grid-item:nth-child(1)  { transition-delay: 0ms;   animation-delay: 0ms; }
.grid-item:nth-child(2)  { transition-delay: 80ms;  animation-delay: 80ms; }
.grid-item:nth-child(3)  { transition-delay: 160ms; animation-delay: 160ms; }
/* ... 以此类推，或用 JS: el.style.transitionDelay = (idx % 4) * 100 + 'ms' */
```

### 8.6 导航栏滚动动效（必须实现）

```javascript
window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');
  if (window.scrollY > 60) {
    nav.style.backdropFilter = 'blur(16px)';
    nav.style.background = 'rgba(bg-color, 0.85)';
    nav.style.boxShadow = '0 1px 0 rgba(accent, 0.1)';
  } else {
    nav.style.backdropFilter = 'blur(0)';
    nav.style.background = 'transparent';
    nav.style.boxShadow = 'none';
  }
}, { passive: true });
```

### 8.7 特效组件常驻动画清单（视情况选用 ≥ 3 个）

| 动画名 | 触发条件 | 效果 |
|--------|---------|------|
| `@keyframes float` | 常驻 | `translateY(0→-12px→0)` 漂浮感，配hero装饰元素 |
| `@keyframes rotate-slow` | 常驻 | 旋转徽章/Badge装饰，`transform:rotate(0→360deg)` |
| `@keyframes shimmer` | 常驻 | 骨架屏扫光或按钮高光，`background-position` 移动 |
| `@keyframes marquee` | 常驻 | 无限横向跑马灯 |
| `@keyframes blink-cursor` | 常驻 | Terminal/打字机光标 `opacity 1→0 step-end` |
| `@keyframes glitch` | 定时/hover | 故障闪烁，`clip-path` 切片 + 色差位移 |
| `@keyframes neon-flicker` | 常驻/慢速 | 霓虹灯管闪烁，`opacity 1→0.8→1→0.6→1` |
| `@keyframes draw-border` | IO触发 | 边框从0→100%绘制，`border-width` 或 `clip-path` |

---

## 九、艺术性排版强制规范（Typography Artistry）

> **禁止平庸排版**：连续 3 条不得出现相同的 Hero 标题布局。必须从下方艺术手法中为每条选取 ≥ 1 个。

### 9.1 艺术排版手法库（每条必须选 ≥ 1 个）

**A. 不规则几何排版**
```css
/* 文字排列打破矩形 — 倾斜、错位、旋转 */
.hero-h1 { transform: rotate(-3deg); transform-origin: left bottom; }
.hero-subtitle { margin-left: 15%; }  /* 刻意错位 */
.text-angled { clip-path: polygon(0 0, 100% 8%, 100% 100%, 0 92%); }

/* 文字沿斜线排列（伪元素辅助） */
.slanted-label {
  writing-mode: vertical-rl;
  transform: rotate(180deg);
  letter-spacing: 4px;
  position: absolute;
}
```

**B. 3D 文字层叠**
```css
/* CSS 3D 透视文字堆叠 */
.text-3d {
  transform: perspective(400px) rotateX(15deg) rotateY(-5deg);
  transform-style: preserve-3d;
}
/* 文字阴影制造3D纵深 */
.text-depth {
  text-shadow:
    1px 1px 0 rgba(accent,0.8),
    2px 2px 0 rgba(accent,0.6),
    3px 3px 0 rgba(accent,0.4),
    4px 4px 0 rgba(accent,0.2);
}
/* hover时3D翻转 */
.flip-text:hover { transform: perspective(400px) rotateY(180deg); transition: transform 0.6s; }
```

**C. 多层叠加排版（Layered Typography）**
```css
/* 巨型背景文字 + 前景内容叠加 */
.bg-text {
  position: absolute;
  font-size: clamp(80px,15vw,200px);
  font-weight: 900;
  color: rgba(accent, 0.04);
  letter-spacing: -5px;
  white-space: nowrap;
  z-index: 0;
  pointer-events: none;
}
/* 描边文字 + 实心文字交叉叠加 */
.outline-text {
  -webkit-text-stroke: 2px var(--accent);
  color: transparent;
  position: absolute;
}
.fill-text {
  color: var(--accent);
  position: relative;
  mix-blend-mode: difference;  /* 与背景混合 */
}
```

**D. 混排/拼贴排版（Collage Typography）**
```css
/* 不同字体/字重混排在同一行 — 打破单调 */
/* HTML示例: <h1>WE <em>MAKE</em> <strong>THINGS</strong> <span class="light">happen</span></h1> */
h1 em     { font-style: italic; font-weight: 300; font-size: 1.2em; }
h1 strong { font-weight: 900; color: var(--accent); }
h1 .light { font-weight: 100; letter-spacing: 0.3em; font-size: 0.7em; vertical-align: middle; }

/* 竖排日文/装饰文字辅助 */
.vertical-label {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 11px;
  letter-spacing: 4px;
  color: var(--accent);
  opacity: 0.6;
}
```

**E. 超大字号剪裁（Oversized Crop）**
```css
/* 字号超出容器，用 overflow:hidden 剪裁 — 只显示字母局部 */
.oversized-crop {
  overflow: hidden;
  height: 200px;  /* 只显示字母的一部分 */
}
.oversized-crop h1 {
  font-size: 25vw;
  line-height: 0.8;
  margin-top: -40px;  /* 向上偏移，只露出中部 */
  white-space: nowrap;
}

/* 图片/渐变作为文字填充 */
.gradient-text {
  background: linear-gradient(135deg, var(--color1), var(--color2), var(--color3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### 9.2 特殊装饰元素（每条必须选 ≥ 2 个）

```css
/* 1. 对角线分割线 */
.diagonal-rule {
  width: 100%;
  height: 2px;
  background: var(--accent);
  transform: rotate(-3deg);
  transform-origin: left;
}

/* 2. 旋转徽章装饰 */
.spin-badge {
  position: absolute;
  width: 120px; height: 120px;
  animation: rotate-slow 12s linear infinite;
}

/* 3. 浮动几何形状 */
.geo-circle {
  position: absolute;
  width: 200px; height: 200px;
  border: 1px solid rgba(accent, 0.2);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}
.geo-square {
  position: absolute;
  width: 80px; height: 80px;
  border: 2px solid var(--accent);
  transform: rotate(45deg);
  animation: float 4s ease-in-out infinite reverse;
}

/* 4. 噪点/颗粒感叠加 */
.grain-overlay::after {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none; z-index: 1;
}

/* 5. 渐变分割带 */
.gradient-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  margin: 3rem 0;
}
```

### 9.3 在确认卡中声明排版艺术手法

```
排版艺术：C. 多层叠加排版 — 巨型背景字"BRAND"低透明度 + 前景内容叠加；E. 超大字号剪裁 — Hero标题裁切只露出字母下半部分
```

### 9.4 艺术排版多样性约束

- 连续 3 条内同一排版艺术手法（A/B/C/D/E）不得重复作为主手法
- 每 5 条内必须至少出现 1 次 B（3D文字）和 1 次 C（多层叠加）
- 禁止连续 2 条都使用标准居中大标题 + 副文案 + 双CTA 的 Hero 布局

---

## 十、按钮造型系统强制规范（Button Shape System）

> **禁止矩形默认按钮**：每条 HTML 的主要 CTA 区域（Hero / CTA Section / Feature 行动按钮）必须从下方造型库中选取 **≥ 2 种不同造型**，Feature 卡片/功能组件中的次要按钮至少选 1 种。普通矩形无装饰按钮只允许出现在表单内联按钮、标签页切换等功能性场景。

### 10.1 造型类型库（BTN-A 到 BTN-L）

**BTN-A：切角几何（Chamfered / Clip-path）**
```css
/* 四角切角 — 科技感、暗黑系 */
.btn-chamfer {
  clip-path: polygon(12px 0%, 100% 0%, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0% 100%, 0% 12px);
  background: var(--accent);
  padding: 14px 36px;
  position: relative;
}
/* hover: clip-path 变形 */
.btn-chamfer:hover {
  clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%);
  transition: clip-path 0.35s cubic-bezier(0.16,1,0.3,1);
}

/* 单角切 — 斜刃感 */
.btn-slash {
  clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 16px 100%, 0 calc(100% - 16px));
}
```

**BTN-B：新布鲁特主义偏移阴影（Neobrutalism Hard Shadow）**
```css
/* 实色厚重阴影，hover 时阴影消失+位移 */
.btn-brutal {
  background: var(--accent);
  border: 2px solid #000;
  color: #000;
  padding: 14px 40px;
  font-weight: 800;
  box-shadow: 4px 4px 0 #000;
  transition: transform 0.15s, box-shadow 0.15s;
}
.btn-brutal:hover {
  transform: translate(4px, 4px);
  box-shadow: 0 0 0 #000;
}
.btn-brutal:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 #000;
}
/* 变体: 彩色阴影 */
.btn-brutal-color {
  box-shadow: 5px 5px 0 var(--accent2);
  border-color: var(--accent2);
}
```

**BTN-C：3D 挤出层叠（CSS 3D Extrusion）**
```css
/* 多层 box-shadow 模拟3D挤出厚度 */
.btn-3d {
  background: var(--accent);
  color: #fff;
  padding: 15px 42px;
  border: none;
  box-shadow:
    0 4px 0 rgba(0,0,0,0.4),
    0 8px 0 rgba(0,0,0,0.15),
    0 12px 20px rgba(0,0,0,0.25);
  transform: translateY(0);
  transition: transform 0.15s, box-shadow 0.15s;
}
.btn-3d:hover {
  transform: translateY(-3px);
  box-shadow:
    0 7px 0 rgba(0,0,0,0.4),
    0 14px 0 rgba(0,0,0,0.1),
    0 20px 30px rgba(0,0,0,0.3);
}
.btn-3d:active {
  transform: translateY(4px);
  box-shadow: 0 1px 0 rgba(0,0,0,0.4), 0 3px 10px rgba(0,0,0,0.2);
}
```

**BTN-D：双层叠加边框（Stacked Border Offset）**
```css
/* 按钮本身 + 伪元素偏移框构成双层视觉 */
.btn-stacked {
  position: relative;
  background: transparent;
  border: 2px solid var(--accent);
  color: var(--accent);
  padding: 13px 38px;
  transition: transform 0.25s, color 0.25s, background 0.25s;
}
.btn-stacked::before {
  content: '';
  position: absolute;
  inset: -5px;
  border: 2px solid var(--accent);
  opacity: 0.35;
  transition: inset 0.3s cubic-bezier(0.16,1,0.3,1), opacity 0.3s;
}
.btn-stacked:hover {
  background: var(--accent);
  color: #000;
}
.btn-stacked:hover::before {
  inset: -9px;
  opacity: 0.15;
}
/* 变体: 旋转外框 */
.btn-stacked-spin::before {
  animation: rotate-slow 4s linear infinite;
  border-style: dashed;
}
```

**BTN-E：填充扫描动画（Fill Sweep）**
```css
/* 背景从左/角/中心扩散填充 */
.btn-sweep {
  position: relative;
  overflow: hidden;
  background: transparent;
  border: 2px solid var(--accent);
  color: var(--accent);
  padding: 14px 40px;
  transition: color 0.4s;
}
.btn-sweep::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--accent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s cubic-bezier(0.16,1,0.3,1);
  z-index: -1;
}
.btn-sweep:hover { color: #000; }
.btn-sweep:hover::after { transform: scaleX(1); }

/* 变体: 从中心扩散 */
.btn-sweep-center::after {
  transform: scale(0);
  transform-origin: center;
  border-radius: 50%;
  transition: transform 0.5s cubic-bezier(0.16,1,0.3,1);
}
.btn-sweep-center:hover::after { transform: scale(4); }
```

**BTN-F：磁性形变（Morphing Pill）**
```css
/* 普通状态: 胶囊形，hover变矩形或反向 */
.btn-morph {
  border-radius: 999px;
  background: var(--accent);
  padding: 14px 44px;
  transition: border-radius 0.4s cubic-bezier(0.34,1.56,0.64,1), transform 0.3s;
}
.btn-morph:hover {
  border-radius: 4px;
  transform: scaleX(1.05);
}
/* 变体: 方转圆 */
.btn-morph-reverse {
  border-radius: 6px;
}
.btn-morph-reverse:hover { border-radius: 999px; }
```

**BTN-G：分裂箭头复合（Split Arrow Compound）**
```css
/* 文字区 + 箭头图标区分两段，hover时箭头区展开 */
.btn-split {
  display: inline-flex;
  align-items: center;
  overflow: hidden;
  border: 2px solid var(--accent);
}
.btn-split-text {
  padding: 12px 24px;
  background: var(--accent);
  color: #fff;
  font-weight: 700;
}
.btn-split-icon {
  padding: 12px 14px;
  background: transparent;
  color: var(--accent);
  transition: background 0.3s, padding 0.35s cubic-bezier(0.16,1,0.3,1);
}
.btn-split:hover .btn-split-icon {
  background: var(--accent);
  color: #fff;
  padding: 12px 22px;
}
```

**BTN-H：故障叠加（Glitch Offset Layers）**
```css
/* 按钮文字后两个伪元素偏移制造色差故障感 */
.btn-glitch {
  position: relative;
  background: transparent;
  border: 2px solid var(--accent);
  color: var(--accent);
  padding: 14px 40px;
  font-weight: 800;
  overflow: hidden;
}
.btn-glitch::before,
.btn-glitch::after {
  content: attr(data-text);
  position: absolute;
  inset: 0;
  display: flex; align-items: center; justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}
.btn-glitch::before {
  color: var(--red, #FF2D55);
  transform: translate(-3px, 0);
}
.btn-glitch::after {
  color: var(--cyan, #00F5FF);
  transform: translate(3px, 0);
}
.btn-glitch:hover::before,
.btn-glitch:hover::after { opacity: 0.7; }
.btn-glitch:hover { animation: btn-shake 0.3s ease; }
```

**BTN-I：扫光高亮（Shimmer Shine）**
```css
/* 常驻扫光动画，Premium感 */
.btn-shimmer {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, var(--accent), var(--accent2, #fff));
  padding: 15px 42px;
}
.btn-shimmer::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent);
  transform: skewX(-20deg);
  animation: shimmer-sweep 2.5s ease-in-out infinite;
}
@keyframes shimmer-sweep {
  0% { left: -100%; }
  60%, 100% { left: 150%; }
}
```

**BTN-J：点阵/像素边框（Pixel / Dotted Frame）**
```css
/* 像素游戏风格，点阵边框 */
.btn-pixel {
  position: relative;
  background: var(--accent);
  color: #fff;
  padding: 13px 36px;
  font-family: 'Press Start 2P', monospace;
  font-size: 11px;
  image-rendering: pixelated;
  /* 像素角装饰 */
  box-shadow:
    -3px 0 0 #fff, 3px 0 0 #fff,
    0 -3px 0 #fff, 0 3px 0 #fff,
    inset -3px 0 0 rgba(0,0,0,0.2),
    inset 0 -3px 0 rgba(0,0,0,0.3);
}
.btn-pixel:hover {
  background: var(--accent2, #fff);
  color: var(--accent);
}
```

**BTN-K：边框绘制入场（Border Draw In）**
```css
/* 鼠标进入时边框从左上角顺序绘制 */
.btn-draw {
  position: relative;
  background: transparent;
  color: var(--accent);
  padding: 14px 40px;
}
.btn-draw::before, .btn-draw::after {
  content: '';
  position: absolute;
  inset: 0;
}
.btn-draw::before {
  border-top: 2px solid var(--accent);
  border-right: 2px solid var(--accent);
  transform: scaleX(0) scaleY(0);
  transform-origin: top right;
  transition: transform 0.35s cubic-bezier(0.16,1,0.3,1);
}
.btn-draw::after {
  border-bottom: 2px solid var(--accent);
  border-left: 2px solid var(--accent);
  transform: scaleX(0) scaleY(0);
  transform-origin: bottom left;
  transition: transform 0.35s cubic-bezier(0.16,1,0.3,1) 0.1s;
}
.btn-draw:hover::before, .btn-draw:hover::after {
  transform: scaleX(1) scaleY(1);
}
```

**BTN-L：磁性吸引偏移（Magnetic Attract）**
```javascript
/* 鼠标靠近时按钮整体被"吸引"偏移 — 配合 T-03 */
document.querySelectorAll('.btn-magnetic').forEach(btn => {
  btn.addEventListener('mousemove', e => {
    const r = btn.getBoundingClientRect();
    const x = (e.clientX - r.left - r.width/2) * 0.4;
    const y = (e.clientY - r.top  - r.height/2) * 0.4;
    btn.style.transform = `translate(${x}px,${y}px)`;
    btn.style.transition = 'transform 0.1s';
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = 'translate(0,0)';
    btn.style.transition = 'transform 0.6s cubic-bezier(0.16,1,0.3,1)';
  });
});
```

---

### 10.2 Feature 卡片形状规范（禁止纯矩形卡片）

每条 HTML 的 Feature/功能区卡片必须从以下形式选 ≥ 1 个，与按钮造型风格保持一致：

| 形式代码 | 实现方式 | 适用风格 |
|---------|---------|---------|
| CARD-A | `clip-path` 切角四边形 | 科技/游戏 |
| CARD-B | 偏移双边框（伪元素右下叠加） | 布鲁特/设计感 |
| CARD-C | `border-radius` 混合（一角大圆弧） | 现代SaaS |
| CARD-D | 卡片 `transform: rotate(-1deg)` 微倾斜 | 创意/手作 |
| CARD-E | 卡片顶部彩色条 `::before` 斜线装饰 | 商务/工具 |
| CARD-F | `box-shadow` 多层叠加颜色（彩色阴影） | NFT/艺术 |
| CARD-G | 边框渐变 (`border-image: linear-gradient`) | AI/高科技 |

```css
/* CARD-A 示例 */
.card-chamfer {
  clip-path: polygon(16px 0%, 100% 0%, 100% calc(100% - 16px), calc(100% - 16px) 100%, 0% 100%, 0% 16px);
}

/* CARD-B 示例 */
.card-offset {
  position: relative;
}
.card-offset::after {
  content: '';
  position: absolute;
  inset: 6px -6px -6px 6px;  /* 右下偏移 */
  border: 2px solid var(--accent);
  opacity: 0.4;
  z-index: -1;
  transition: inset 0.3s;
}
.card-offset:hover::after { inset: 8px -8px -8px 8px; }

/* CARD-F 彩色阴影叠加 */
.card-color-shadow {
  box-shadow:
    0 0 0 1px rgba(accent, 0.2),
    6px 6px 0 rgba(accent, 0.15),
    12px 12px 0 rgba(accent, 0.07);
  transition: box-shadow 0.3s, transform 0.3s;
}
.card-color-shadow:hover {
  transform: translate(-4px, -4px);
  box-shadow:
    0 0 0 1px var(--accent),
    10px 10px 0 rgba(accent, 0.2),
    20px 20px 0 rgba(accent, 0.08);
}

/* CARD-G 渐变边框 */
.card-gradient-border {
  border: 2px solid transparent;
  background-clip: padding-box;
  position: relative;
}
.card-gradient-border::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: inherit;
  z-index: -1;
}
```

---

### 10.3 强制选用规则

- 每条 HTML 主 CTA 按钮必须使用 BTN-A / BTN-B / BTN-C / BTN-D 中的至少 1 个
- 每条 HTML 次要/ghost 按钮必须使用 BTN-E / BTN-F / BTN-H / BTN-K 中的至少 1 个
- Feature 卡片必须使用 CARD-A 到 CARD-G 中的至少 1 个
- 连续 3 条内同一 BTN 类型不得作为主 CTA 重复使用
- 在确认卡中声明选用的按钮造型：`按钮造型：BTN-C（3D挤出）主CTA + BTN-E（扫描填充）ghost + CARD-B（偏移双边框）`

---

## 十一、光标增强系统强制规范（Cursor Enhancement System）

> 在现有 CUR-A 到 CUR-G 基本变体基础上，所有光标必须额外实现 **≥ 2 个上下文状态变化**（context-aware cursor states）。仅跟随鼠标移动不算完整实现。

### 11.1 光标上下文状态库

```javascript
// 状态 1: 悬停可点击元素 — 光标放大 + 文字提示
document.querySelectorAll('button, .card, [data-cursor]').forEach(el => {
  el.addEventListener('mouseenter', () => {
    cursor.classList.add('cur-hover');
    // 显示 data-cursor 属性文字（如 "VIEW" / "CLICK" / "PLAY"）
    if (el.dataset.cursor) {
      cursorLabel.textContent = el.dataset.cursor;
      cursorLabel.style.opacity = '1';
    }
  });
  el.addEventListener('mouseleave', () => {
    cursor.classList.remove('cur-hover');
    cursorLabel.style.opacity = '0';
  });
});

// 状态 2: 悬停图片 — 光标变成图片预览圆圈
document.querySelectorAll('img, .img-wrap').forEach(el => {
  el.addEventListener('mouseenter', () => cursor.classList.add('cur-view'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('cur-view'));
});

// 状态 3: 悬停文字区域 — 光标变为 I-beam 细线
document.querySelectorAll('p, h1, h2, h3, blockquote').forEach(el => {
  el.addEventListener('mouseenter', () => cursor.classList.add('cur-text'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('cur-text'));
});

// 状态 4: 页面加载动画 — 光标隐藏直到 DOMContentLoaded
document.documentElement.style.cursor = 'none';
```

```css
/* 基础光标尺寸变化三态 */
.cursor { transition: width 0.3s, height 0.3s, background 0.3s, opacity 0.3s; }
.cursor.cur-hover { width: 52px; height: 52px; background: transparent; border: 2px solid var(--accent); mix-blend-mode: normal; }
.cursor.cur-view  { width: 80px; height: 80px; background: rgba(255,255,255,0.08); backdrop-filter: blur(4px); }
.cursor.cur-text  { width: 2px; height: 28px; border-radius: 1px; }

/* 光标文字标签 */
.cursor-label {
  position: fixed; pointer-events: none; z-index: 10001;
  font-size: 9px; letter-spacing: 2px; text-transform: uppercase;
  color: var(--accent); opacity: 0;
  transition: opacity 0.2s;
  transform: translate(12px, 12px);  /* 跟随光标偏移 */
}
```

### 11.2 高级光标效果（选 ≥ 1 个）

**EFF-1：光标拖尾文字轨道（Text Orbit）**
```javascript
// 光标周围旋转一段品牌文字
const orbitText = 'EXPLORE · DISCOVER · CREATE · ';
// 用 SVG textPath 实现文字沿圆弧排列，跟随鼠标
// 适配 CUR-D orbit 变体的增强版
```

**EFF-2：光标点击爆炸（Click Burst）**
```javascript
// 每次点击在光标位置生成 6-8 个发散粒子
document.addEventListener('click', e => {
  for (let i = 0; i < 8; i++) {
    const p = document.createElement('div');
    p.className = 'click-burst';
    const angle = (i / 8) * Math.PI * 2;
    const dist = 30 + Math.random() * 20;
    p.style.cssText = `left:${e.clientX}px;top:${e.clientY}px;
      --dx:${Math.cos(angle)*dist}px;--dy:${Math.sin(angle)*dist}px;`;
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 600);
  }
});
```
```css
.click-burst {
  position: fixed; width: 4px; height: 4px; border-radius: 50%;
  background: var(--accent); pointer-events: none; z-index: 9999;
  animation: burst-out 0.6s ease-out forwards;
}
@keyframes burst-out {
  0%   { transform: translate(-50%,-50%) translate(0,0); opacity: 1; }
  100% { transform: translate(-50%,-50%) translate(var(--dx),var(--dy)); opacity: 0; }
}
```

**EFF-3：光标磁场涟漪（Proximity Ripple）**
```javascript
// 鼠标靠近按钮时，按钮内产生涟漪而非点击时才产生
document.querySelectorAll('.btn-magnetic, .btn-ripple-proximity').forEach(btn => {
  btn.addEventListener('mousemove', e => {
    const r = btn.getBoundingClientRect();
    btn.style.setProperty('--rx', (e.clientX - r.left) + 'px');
    btn.style.setProperty('--ry', (e.clientY - r.top) + 'px');
  });
});
```
```css
.btn-ripple-proximity::after {
  content: '';
  position: absolute;
  left: var(--rx, 50%); top: var(--ry, 50%);
  width: 0; height: 0;
  border-radius: 50%;
  background: rgba(255,255,255,0.15);
  transform: translate(-50%,-50%);
  transition: width 0.4s, height 0.4s, opacity 0.4s;
  pointer-events: none;
}
.btn-ripple-proximity:hover::after {
  width: 200px; height: 200px; opacity: 0;
}
```

**EFF-4：光标颜色区域感知（Color Zone）**
```javascript
// 根据光标所在 section 的背景色，自动切换光标颜色
const zones = document.querySelectorAll('section[data-cursor-color]');
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      document.documentElement.style.setProperty('--cursor-color', e.target.dataset.cursorColor);
    }
  });
}, { threshold: 0.5 });
zones.forEach(z => observer.observe(z));
```

### 11.3 在确认卡中声明

```
光标增强：CUR-B（blend反色）+ EFF-2（点击爆炸）+ EFF-4（颜色区域感知）
按钮造型：BTN-A（切角几何）主CTA + BTN-E（扫描填充）ghost + CARD-B（偏移双边框）
```

### 11.4 扩展光标变体库（CUR-H 到 CUR-T）

> 在原有 CUR-A~CUR-G + CUR-X 基础上新增 12 种光标变体，全部合法可用，受冷却约束（连续5条不重复同一CUR代号）。

---

**CUR-H：液态水滴形变（Liquid Blob）**
```javascript
// 光标是一个椭圆blob，移动时根据速度方向拉伸变形
let px = 0, py = 0, vx = 0, vy = 0;
const blob = document.getElementById('cursor-blob');
document.addEventListener('mousemove', e => {
  vx = e.clientX - px; vy = e.clientY - py;
  px = e.clientX; py = e.clientY;
  const speed = Math.sqrt(vx*vx + vy*vy);
  const angle = Math.atan2(vy, vx) * 180 / Math.PI;
  const scaleX = 1 + Math.min(speed * 0.04, 0.6);
  const scaleY = 1 - Math.min(speed * 0.02, 0.3);
  blob.style.transform = `translate(${px}px,${py}px) translate(-50%,-50%) rotate(${angle}deg) scale(${scaleX},${scaleY})`;
});
```
```css
#cursor-blob {
  position: fixed; pointer-events: none; z-index: 9999;
  width: 20px; height: 20px; border-radius: 50%;
  background: var(--accent); mix-blend-mode: difference;
  transition: transform 0.05s linear, border-radius 0.2s;
  will-change: transform;
}
/* hover时变成大水滴 */
body.cursor-hover #cursor-blob { width: 40px; height: 40px; border-radius: 40% 60% 60% 40% / 40% 40% 60% 60%; }
```

---

**CUR-I：弹性橡皮筋拖尾（Elastic Tail）**
```javascript
// 两个元素：一个点精确跟随，一个圆圈用弹性插值跟随（视觉上像橡皮筋）
let tx = 0, ty = 0, rx = 0, ry = 0;
const dot = document.getElementById('cur-dot');
const ring = document.getElementById('cur-ring');
document.addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; });
(function loop() {
  // 弹性系数0.08，越小越"弹"
  rx += (tx - rx) * 0.08; ry += (ty - ry) * 0.08;
  // 拉伸：点与环距离决定连线倾斜
  const dist = Math.sqrt((tx-rx)**2 + (ty-ry)**2);
  const angle = Math.atan2(ty-ry, tx-rx) * 180/Math.PI;
  ring.style.transform = `translate(${rx-20}px,${ry-20}px) rotate(${angle}deg) scaleX(${1 + dist*0.015})`;
  dot.style.transform = `translate(${tx-4}px,${ty-4}px)`;
  requestAnimationFrame(loop);
})();
```
```css
#cur-dot { position:fixed; width:8px; height:8px; border-radius:50%; background:var(--accent); pointer-events:none; z-index:9999; }
#cur-ring { position:fixed; width:40px; height:40px; border:2px solid var(--accent); border-radius:50%; pointer-events:none; z-index:9998; opacity:0.6; transform-origin:center; }
```

---

**CUR-J：像素马赛克光标（Pixel Trail）**
```javascript
// 鼠标移动时在经过的路径上留下短暂的像素色块
const colors = ['#ff006e','#fb5607','#ffbe0b','#8338ec','#3a86ff'];
document.addEventListener('mousemove', e => {
  if (Math.random() > 0.4) return; // 控制密度
  const px = document.createElement('div');
  px.className = 'pixel-crumb';
  px.style.cssText = `left:${e.clientX + (Math.random()-0.5)*16}px;top:${e.clientY + (Math.random()-0.5)*16}px;background:${colors[Math.floor(Math.random()*colors.length)]};width:${4+Math.random()*6}px;height:${4+Math.random()*6}px`;
  document.body.appendChild(px);
  setTimeout(() => px.remove(), 600);
});
```
```css
.pixel-crumb {
  position: fixed; pointer-events: none; z-index: 9997;
  image-rendering: pixelated; border-radius: 0; /* 像素感：无圆角 */
  animation: pixel-fade 0.6s ease-out forwards;
}
@keyframes pixel-fade {
  0%   { opacity: 1; transform: scale(1) rotate(0deg); }
  100% { opacity: 0; transform: scale(0) rotate(45deg); }
}
```
适用气质：Y2K / 游戏 / 像素风 / 潮牌

---

**CUR-K：磁性多点吸附群（Magnetic Swarm）**
```javascript
// 8个小卫星围绕主光标旋转，靠近按钮时集体被吸入按钮内
const NUM = 8;
const satellites = Array.from({length: NUM}, (_, i) => {
  const el = document.createElement('div');
  el.className = 'swarm-dot';
  document.body.appendChild(el);
  return { el, angle: (i/NUM)*Math.PI*2, dist: 24, x: 0, y: 0 };
});
let mx = 0, my = 0, t = 0;
document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
(function loop() {
  t += 0.05;
  satellites.forEach((s, i) => {
    const a = s.angle + t + i * 0.3;
    const tx = mx + Math.cos(a) * s.dist;
    const ty = my + Math.sin(a) * s.dist;
    s.x += (tx - s.x) * 0.15; s.y += (ty - s.y) * 0.15;
    s.el.style.transform = `translate(${s.x - 3}px, ${s.y - 3}px)`;
  });
  requestAnimationFrame(loop);
})();
```
```css
.swarm-dot {
  position: fixed; width: 6px; height: 6px; border-radius: 50%;
  pointer-events: none; z-index: 9998;
  background: var(--accent); opacity: 0.7;
}
.swarm-dot:nth-child(odd)  { background: var(--accent2, #fff); opacity: 0.5; }
```
适用气质：科技 / 粒子宇宙 / 赛博 / AI

---

**CUR-L：霓虹光晕描边（Neon Halo）**
```javascript
// 光标：一个透明填充的圆，边框有强烈的彩色发光
// 鼠标静止时边框匀速变色（hue rotate）；移动时边框变细变亮
let moving = false, moveTimer;
const halo = document.getElementById('neon-halo');
document.addEventListener('mousemove', e => {
  halo.style.left = e.clientX + 'px'; halo.style.top = e.clientY + 'px';
  halo.classList.add('moving');
  clearTimeout(moveTimer);
  moveTimer = setTimeout(() => halo.classList.remove('moving'), 150);
});
```
```css
#neon-halo {
  position: fixed; width: 36px; height: 36px; border-radius: 50%;
  border: 2px solid var(--accent);
  box-shadow: 0 0 8px var(--accent), 0 0 20px var(--accent), inset 0 0 8px rgba(255,255,255,0.05);
  pointer-events: none; z-index: 9999;
  transform: translate(-50%,-50%);
  animation: halo-rotate 3s linear infinite;
  transition: width 0.2s, height 0.2s, box-shadow 0.2s;
}
#neon-halo.moving {
  width: 20px; height: 20px;
  box-shadow: 0 0 16px var(--accent), 0 0 40px var(--accent);
}
@keyframes halo-rotate {
  0%   { filter: hue-rotate(0deg); }
  100% { filter: hue-rotate(360deg); }
}
```
适用气质：霓虹赛博 / 电子音乐 / 夜店 / 游戏

---

**CUR-M：书法墨迹拖尾（Ink Brush）**
```javascript
// 鼠标移动时在Canvas上绘制渐变墨迹，每帧轻微fade
const inkCanvas = document.getElementById('ink-canvas');
inkCanvas.width = window.innerWidth; inkCanvas.height = window.innerHeight;
const ic = inkCanvas.getContext('2d');
let lx, ly, drawing = false;
ic.globalCompositeOperation = 'source-over';
document.addEventListener('mousemove', e => {
  if (!lx) { lx = e.clientX; ly = e.clientY; return; }
  const speed = Math.sqrt((e.clientX-lx)**2 + (e.clientY-ly)**2);
  ic.beginPath();
  ic.moveTo(lx, ly);
  ic.lineTo(e.clientX, e.clientY);
  ic.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
  ic.lineWidth = Math.max(1, 8 - speed * 0.3); // 速度快则线细
  ic.lineCap = 'round'; ic.lineJoin = 'round';
  ic.globalAlpha = Math.min(1, 0.6 + 0.4 * (1 - speed/100));
  ic.stroke();
  lx = e.clientX; ly = e.clientY;
});
// 每帧fade
(function fade() {
  ic.globalCompositeOperation = 'destination-out';
  ic.globalAlpha = 0.015;
  ic.fillRect(0, 0, inkCanvas.width, inkCanvas.height);
  ic.globalCompositeOperation = 'source-over';
  requestAnimationFrame(fade);
})();
```
```css
#ink-canvas {
  position: fixed; inset: 0; pointer-events: none; z-index: 9996;
}
```
适用气质：书法 / 日式 / 奢侈品 / 手工艺 / 艺术工作室

---

**CUR-N：弹跳果冻光标（Jelly Bounce）**
```javascript
// 光标跟随鼠标，但有弹性过冲：超过目标位置再弹回
// 用弹簧物理：加速度 = k*(目标-位置) - 阻尼*速度
let cx=0,cy=0,cvx=0,cvy=0, mx=0,my=0;
const jelly = document.getElementById('jelly-cursor');
document.addEventListener('mousemove', e=>{mx=e.clientX;my=e.clientY;});
(function loop(){
  const k=0.18, damp=0.75; // 弹性系数/阻尼
  cvx += (mx-cx)*k; cvy += (my-cy)*k;
  cvx *= damp; cvy *= damp;
  cx += cvx; cy += cvy;
  const speed = Math.sqrt(cvx*cvx+cvy*cvy);
  const squish = Math.min(speed*0.03, 0.3);
  jelly.style.transform=`translate(${cx}px,${cy}px) translate(-50%,-50%) scaleX(${1+squish}) scaleY(${1-squish*0.5})`;
  requestAnimationFrame(loop);
})();
```
```css
#jelly-cursor {
  position: fixed; width: 24px; height: 24px; border-radius: 50%;
  background: var(--accent); pointer-events: none; z-index: 9999;
  mix-blend-mode: difference; will-change: transform;
  transition: background 0.3s;
}
```
适用气质：儿童 / 玩具 / 创意工作室 / 可爱品牌

---

**CUR-O：雷达扫描环（Radar Sweep）**
```javascript
// 光标中心 + 一个不断旋转的扇形扫描线
const radar = document.getElementById('radar-cursor');
const sweep = radar.querySelector('.radar-sweep');
let rx=0, ry=0, angle=0;
document.addEventListener('mousemove', e=>{rx=e.clientX;ry=e.clientY;});
(function loop(){
  radar.style.transform=`translate(${rx}px,${ry}px) translate(-50%,-50%)`;
  angle = (angle+2) % 360;
  sweep.style.transform=`rotate(${angle}deg)`;
  requestAnimationFrame(loop);
})();
```
```html
<!-- HTML结构 -->
<div id="radar-cursor">
  <canvas class="radar-rings" width="60" height="60"></canvas>
  <div class="radar-sweep"></div>
  <div class="radar-dot"></div>
</div>
```
```css
#radar-cursor { position:fixed; width:60px; height:60px; pointer-events:none; z-index:9999; }
.radar-rings {
  position:absolute; inset:0; border-radius:50%;
  border: 1px solid rgba(0,255,136,0.3);
  box-shadow: 0 0 0 10px rgba(0,255,136,0.08), 0 0 0 20px rgba(0,255,136,0.05);
}
.radar-sweep {
  position:absolute; top:50%; left:50%; width:50%; height:1px;
  background:linear-gradient(90deg, rgba(0,255,136,0.8), transparent);
  transform-origin: left center;
}
.radar-dot { position:absolute; top:50%; left:50%; width:4px; height:4px; border-radius:50%; background:#00ff88; transform:translate(-50%,-50%); }
```
适用气质：军事 / 科技监控 / 黑客 / 数据平台 / 赛博

---

**CUR-P：摄影取景框（Viewfinder）**
```javascript
// 光标是一个取景框（四角L形）+ 中心点，悬停图片时取景框放大
const vf = document.getElementById('viewfinder');
document.addEventListener('mousemove', e => {
  vf.style.transform = `translate(${e.clientX}px,${e.clientY}px) translate(-50%,-50%)`;
});
document.querySelectorAll('img,.card').forEach(el => {
  el.addEventListener('mouseenter', () => vf.classList.add('vf-open'));
  el.addEventListener('mouseleave', () => vf.classList.remove('vf-open'));
});
```
```css
#viewfinder {
  position:fixed; width:40px; height:40px; pointer-events:none; z-index:9999;
  transition: width 0.3s cubic-bezier(0.16,1,0.3,1), height 0.3s cubic-bezier(0.16,1,0.3,1);
}
/* 四角L形用四个伪+子元素拼合 */
#viewfinder::before, #viewfinder::after,
#viewfinder .vf-bl, #viewfinder .vf-br {
  content:''; position:absolute; width:10px; height:10px;
  border-color: var(--accent); border-style: solid; border-width: 0;
}
#viewfinder::before  { top:0;    left:0;   border-top-width:2px; border-left-width:2px; }
#viewfinder::after   { top:0;    right:0;  border-top-width:2px; border-right-width:2px; }
#viewfinder .vf-bl   { bottom:0; left:0;   border-bottom-width:2px; border-left-width:2px; }
#viewfinder .vf-br   { bottom:0; right:0;  border-bottom-width:2px; border-right-width:2px; }
/* 中心点 */
#viewfinder .vf-center { position:absolute; top:50%; left:50%; width:4px; height:4px; border-radius:50%; background:var(--accent); transform:translate(-50%,-50%); }
#viewfinder.vf-open { width:70px; height:70px; }
```
适用气质：摄影 / 电影 / 作品集 / 时尚大片

---

**CUR-Q：燃烧火焰拖尾（Fire Trail）**
```javascript
// 移动时在路径上生成橙红色上升粒子
document.addEventListener('mousemove', e => {
  if (Math.random() > 0.5) return;
  const f = document.createElement('div');
  f.className = 'flame-particle';
  const hue = 10 + Math.random()*40; // 10~50 橙黄
  const size = 4 + Math.random() * 8;
  f.style.cssText = `left:${e.clientX}px;top:${e.clientY}px;width:${size}px;height:${size}px;background:hsl(${hue},100%,${50+Math.random()*20}%);--dx:${(Math.random()-0.5)*30}px;--dy:${-20-Math.random()*30}px`;
  document.body.appendChild(f);
  setTimeout(() => f.remove(), 700);
});
```
```css
.flame-particle {
  position:fixed; border-radius:50%; pointer-events:none; z-index:9997;
  filter: blur(2px);
  animation: flame-rise 0.7s ease-out forwards;
}
@keyframes flame-rise {
  0%   { transform:translate(-50%,-50%) translate(0,0) scale(1); opacity:0.9; }
  100% { transform:translate(-50%,-50%) translate(var(--dx),var(--dy)) scale(0); opacity:0; filter:blur(6px); }
}
```
适用气质：极限运动 / 烈酒 / 音乐节 / 竞技游戏

---

**CUR-R：星尘彗星拖尾（Comet Stardust）**
```javascript
// 主光标为小星形，拖尾为逐渐缩小的星点串
const history = [];
const MAX = 15;
const comet = document.getElementById('comet-cursor');
document.addEventListener('mousemove', e => {
  history.push({x: e.clientX, y: e.clientY});
  if (history.length > MAX) history.shift();
  comet.style.transform = `translate(${e.clientX}px,${e.clientY}px) translate(-50%,-50%)`;
  // 更新拖尾点
  document.querySelectorAll('.comet-trail').forEach((el,i) => {
    const p = history[history.length - 1 - i*2];
    if (p) { el.style.transform=`translate(${p.x}px,${p.y}px) translate(-50%,-50%)`; el.style.opacity = (1 - i/8) * 0.7; el.style.width = el.style.height = (8 - i) + 'px'; }
  });
});
```
```css
#comet-cursor {
  position:fixed; width:12px; height:12px; pointer-events:none; z-index:9999;
  background:var(--accent); clip-path:polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%); /* 星形 */
  filter: drop-shadow(0 0 6px var(--accent));
}
.comet-trail {
  position:fixed; border-radius:50%; background:var(--accent);
  pointer-events:none; z-index:9998; transition: opacity 0.1s;
}
```
适用气质：宇宙 / VR / 魔幻 / 奢侈品 / 占星

---

**CUR-S：文字打印机光标（Terminal Caret）**
```javascript
// 光标样式是竖向的 Terminal 插入符，带闪烁；悬停按钮时变成>_ 提示符
const caret = document.getElementById('terminal-caret');
const caretText = document.getElementById('caret-text');
document.addEventListener('mousemove', e => {
  caret.style.transform = `translate(${e.clientX}px,${e.clientY - 14}px)`;
});
document.querySelectorAll('button').forEach(btn => {
  btn.addEventListener('mouseenter', () => { caretText.textContent = '>_'; caret.classList.add('cmd-mode'); });
  btn.addEventListener('mouseleave', () => { caretText.textContent = ''; caret.classList.remove('cmd-mode'); });
});
```
```css
#terminal-caret {
  position:fixed; pointer-events:none; z-index:9999;
  font-family: 'Share Tech Mono', monospace; font-size: 20px; color: var(--accent);
  line-height:1; animation: caret-blink 1s step-end infinite;
}
#terminal-caret::before { content: '|'; }
#terminal-caret.cmd-mode::before { content: ''; }
@keyframes caret-blink { 0%,100%{opacity:1} 50%{opacity:0} }
```
适用气质：开发者工具 / 黑客终端 / SaaS / 代码平台

---

**CUR-T：音乐均衡器波形光标（Equalizer）**
```javascript
// 光标旁边有3-5根短竖条，高度随时间正弦波动，模拟均衡器律动
const bars = Array.from(document.querySelectorAll('.eq-bar'));
let eqX=0, eqY=0, eqT=0;
document.addEventListener('mousemove', e=>{ eqX=e.clientX; eqY=e.clientY; });
const eqContainer = document.getElementById('eq-cursor');
(function loop(){
  eqT += 0.12;
  eqContainer.style.transform = `translate(${eqX+10}px,${eqY-15}px)`;
  bars.forEach((b,i)=>{
    const h = 4 + 10 * Math.abs(Math.sin(eqT * (1+i*0.4) + i));
    b.style.height = h + 'px';
  });
  requestAnimationFrame(loop);
})();
```
```html
<div id="eq-cursor">
  <div class="eq-bar"></div><div class="eq-bar"></div>
  <div class="eq-bar"></div><div class="eq-bar"></div>
  <div class="eq-bar"></div>
</div>
```
```css
#eq-cursor { position:fixed; display:flex; align-items:flex-end; gap:2px; pointer-events:none; z-index:9999; height:20px; }
.eq-bar { width:3px; background:var(--accent); border-radius:1px 1px 0 0; box-shadow:0 0 4px var(--accent); transition:height 0.05s; }
```
适用气质：音乐 / 播客 / 音频平台 / 演出活动

---

### 11.4b 扩展光标变体库（CUR-U 到 CUR-AH）

> 在 CUR-A~CUR-T + CUR-X 基础上再新增 14 种光标变体。实现时参考已有变体代码风格，以下为核心逻辑说明。

---

**CUR-U：墨水晕染（Ink Bleed）**
```javascript
// 点击时在光标处创建一个墨水圆圈，scale(0)→scale(1) + opacity:0.5→0
document.addEventListener('click', e => {
  const ink = document.createElement('div');
  ink.className = 'ink-bleed';
  ink.style.left = e.clientX + 'px'; ink.style.top = e.clientY + 'px';
  document.body.appendChild(ink);
  setTimeout(() => ink.remove(), 800);
});
```
```css
.ink-bleed { position:fixed; width:80px; height:80px; border-radius:50%; background:radial-gradient(circle,var(--ink) 0%,transparent 70%); pointer-events:none; z-index:9997; transform:translate(-50%,-50%) scale(0); animation:ink-spread 0.8s ease-out forwards; }
@keyframes ink-spread { to { transform:translate(-50%,-50%) scale(1); opacity:0; } }
```
适用气质：水墨 / 书法 / 日式 / 文人风

---

**CUR-V：棱镜折射（Prism Refract）**
```javascript
// 光标周围6条彩虹色线段，随鼠标角度旋转
const prism = document.getElementById('prism-cursor');
let pmx=0,pmy=0;
document.addEventListener('mousemove', e => {
  pmx=e.clientX; pmy=e.clientY;
  prism.style.transform = `translate(${pmx-25}px,${pmy-25}px)`;
});
```
```css
#prism-cursor { position:fixed; width:50px; height:50px; pointer-events:none; z-index:9999; }
#prism-cursor::before { content:''; position:absolute; inset:0; background:conic-gradient(red,orange,yellow,green,blue,violet,red); border-radius:50%; mask:radial-gradient(circle 18px,transparent 95%,black 100%); -webkit-mask:radial-gradient(circle 18px,transparent 95%,black 100%); animation:prism-spin 3s linear infinite; }
@keyframes prism-spin { to { transform:rotate(360deg); } }
```
适用气质：闪光朋克 / 全息 / 科技 / 珠宝

---

**CUR-W：重力井（Gravity Well）**
```javascript
// 光标200px范围内的按钮/卡片微微偏向光标
let gwx=0, gwy=0;
document.addEventListener('mousemove', e => { gwx=e.clientX; gwy=e.clientY; });
(function gravLoop(){
  document.querySelectorAll('button,.card,a').forEach(el=>{
    const r=el.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
    const dx=gwx-cx, dy=gwy-cy, dist=Math.sqrt(dx*dx+dy*dy);
    if(dist<200&&dist>20){ const f=Math.min(8,(200-dist)*0.04); el.style.transform=`translate(${dx/dist*f}px,${dy/dist*f}px)`; }
    else { el.style.transform=''; }
  });
  requestAnimationFrame(gravLoop);
})();
```
适用气质：科技 / 物理 / 太空 / AI

---

**CUR-Y：音符飘落（Music Notes）**
```javascript
const notes = ['♪','♫','♩','♬','♭'];
document.addEventListener('mousemove', e => {
  if(Math.random()>0.3) return;
  const n = document.createElement('span');
  n.className='note-float'; n.textContent=notes[Math.floor(Math.random()*notes.length)];
  n.style.left=e.clientX+'px'; n.style.top=e.clientY+'px';
  document.body.appendChild(n);
  setTimeout(()=>n.remove(),1200);
});
```
```css
.note-float { position:fixed; pointer-events:none; z-index:9997; font-size:16px; color:var(--accent); animation:note-up 1.2s ease-out forwards; }
@keyframes note-up { 0%{opacity:1;transform:translateY(0) rotate(0)} 100%{opacity:0;transform:translateY(-60px) rotate(20deg)} }
```
适用气质：音乐 / 播客 / 派对 / 乐器品牌

---

**CUR-Z：蝴蝶翅膀（Butterfly Wings）**
```javascript
// 两片翅膀随移动速度扇动——速度快时展开，慢时合拢
const bfly = document.getElementById('butterfly-cursor');
let bx=0,by=0,bpx=0,bpy=0;
document.addEventListener('mousemove',e=>{bx=e.clientX;by=e.clientY;});
(function bloop(){
  const speed=Math.sqrt((bx-bpx)**2+(by-bpy)**2);
  bpx+=(bx-bpx)*0.15; bpy+=(by-bpy)*0.15;
  const wing=Math.min(45,speed*3);
  bfly.style.transform=`translate(${bpx-20}px,${bpy-12}px)`;
  bfly.querySelector('.wing-l').style.transform=`rotateY(${wing}deg)`;
  bfly.querySelector('.wing-r').style.transform=`rotateY(-${wing}deg)`;
  requestAnimationFrame(bloop);
})();
```
适用气质：自然 / 童话 / 花店 / 蝴蝶园

---

**CUR-AA：水波涟漪（Water Ripple）**
```javascript
// 光标处持续产生扩散同心圆
setInterval(()=>{
  const rp=document.createElement('div');
  rp.className='water-ripple';
  rp.style.left=curX+'px'; rp.style.top=curY+'px';
  document.body.appendChild(rp);
  setTimeout(()=>rp.remove(),1000);
},400);
```
```css
.water-ripple { position:fixed; width:10px; height:10px; border:1.5px solid var(--accent); border-radius:50%; pointer-events:none; z-index:9996; transform:translate(-50%,-50%) scale(0); animation:ripple-out 1s ease-out forwards; opacity:0.6; }
@keyframes ripple-out { to { transform:translate(-50%,-50%) scale(6); opacity:0; } }
```
适用气质：海洋 / SPA / 自然 / 水主题

---

**CUR-AB：指南针（Compass）**
```javascript
// 圆形罗盘光标，指针指向最近的button/a元素
const compass=document.getElementById('compass-cursor');
const needle=compass.querySelector('.needle');
document.addEventListener('mousemove',e=>{
  compass.style.transform=`translate(${e.clientX-20}px,${e.clientY-20}px)`;
  let nearest=null, minD=Infinity;
  document.querySelectorAll('button,a,.card').forEach(el=>{
    const r=el.getBoundingClientRect(), d=Math.hypot(e.clientX-r.left-r.width/2,e.clientY-r.top-r.height/2);
    if(d<minD){minD=d;nearest=el;}
  });
  if(nearest){
    const r=nearest.getBoundingClientRect();
    const angle=Math.atan2(r.top+r.height/2-e.clientY,r.left+r.width/2-e.clientX)*180/Math.PI;
    needle.style.transform=`rotate(${angle+90}deg)`;
  }
});
```
适用气质：旅行 / 导航 / 探索 / 户外

---

**CUR-AC：DNA双螺旋（DNA Helix）**
```javascript
// 两条由小点组成的螺旋线绕光标旋转
const NUM_DOTS=12; let dnaT=0, dnax=0, dnay=0;
const dots=Array.from({length:NUM_DOTS*2},(_,i)=>{const d=document.createElement('div');d.className='dna-dot';document.body.appendChild(d);return d;});
document.addEventListener('mousemove',e=>{dnax=e.clientX;dnay=e.clientY;});
(function dnaLoop(){
  dnaT+=0.05;
  for(let i=0;i<NUM_DOTS;i++){
    const a=dnaT+i*0.5, r=16;
    dots[i].style.transform=`translate(${dnax+Math.cos(a)*r-3}px,${dnay+Math.sin(a)*r*0.3+i*2-NUM_DOTS-3}px)`;
    dots[i+NUM_DOTS].style.transform=`translate(${dnax-Math.cos(a)*r-3}px,${dnay-Math.sin(a)*r*0.3+i*2-NUM_DOTS-3}px)`;
    dots[i].style.opacity=Math.abs(Math.cos(a))*0.7+0.3;
    dots[i+NUM_DOTS].style.opacity=Math.abs(Math.cos(a+Math.PI))*0.7+0.3;
  }
  requestAnimationFrame(dnaLoop);
})();
```
适用气质：生物科技 / 医疗 / 基因 / 科研

---

**CUR-AD：烟雾缭绕（Smoke Trail）**
```javascript
document.addEventListener('mousemove', e => {
  if(Math.random()>0.4) return;
  const s=document.createElement('div');
  s.className='smoke-puff';
  s.style.left=e.clientX+'px'; s.style.top=e.clientY+'px';
  s.style.setProperty('--dx',(Math.random()-0.5)*30+'px');
  document.body.appendChild(s);
  setTimeout(()=>s.remove(),1200);
});
```
```css
.smoke-puff { position:fixed; width:12px; height:12px; border-radius:50%; background:rgba(180,180,180,0.4); pointer-events:none; z-index:9996; filter:blur(4px); animation:smoke-rise 1.2s ease-out forwards; }
@keyframes smoke-rise { 0%{opacity:0.6;transform:translate(-50%,-50%) scale(1)} 100%{opacity:0;transform:translate(calc(-50% + var(--dx)),-80px) scale(3)} }
```
适用气质：香氛 / 雪茄 / 烟花 / 神秘

---

**CUR-AE：电弧放电（Arc Discharge）**
```javascript
// Canvas绘制光标到附近元素的闪烁电弧
const arcCvs=document.getElementById('arc-canvas');
const actx=arcCvs.getContext('2d');
arcCvs.width=innerWidth; arcCvs.height=innerHeight;
let arcx=0,arcy=0;
document.addEventListener('mousemove',e=>{arcx=e.clientX;arcy=e.clientY;});
(function arcLoop(){
  actx.clearRect(0,0,arcCvs.width,arcCvs.height);
  document.querySelectorAll('button,.card').forEach(el=>{
    const r=el.getBoundingClientRect(),ex=r.left+r.width/2,ey=r.top+r.height/2;
    const d=Math.hypot(arcx-ex,arcy-ey);
    if(d<150){
      actx.beginPath(); actx.moveTo(arcx,arcy);
      for(let i=1;i<5;i++){const t=i/5; actx.lineTo(arcx+(ex-arcx)*t+(Math.random()-0.5)*20,arcy+(ey-arcy)*t+(Math.random()-0.5)*20);}
      actx.lineTo(ex,ey); actx.strokeStyle=`rgba(100,200,255,${(150-d)/150*0.8})`; actx.lineWidth=1.5; actx.stroke();
    }
  });
  requestAnimationFrame(arcLoop);
})();
```
适用气质：赛博 / 电力 / 科幻 / 特斯拉

---

**CUR-AF：齿轮旋转（Gear Spin）**
```javascript
const gear=document.getElementById('gear-cursor');
let gearAngle=0;
document.addEventListener('mousemove',e=>{
  gear.style.left=e.clientX-20+'px'; gear.style.top=e.clientY-20+'px';
});
(function gearSpin(){ gearAngle+=2; gear.style.transform=`rotate(${gearAngle}deg)`; requestAnimationFrame(gearSpin); })();
```
```css
#gear-cursor { position:fixed; width:40px; height:40px; pointer-events:none; z-index:9999; }
#gear-cursor::before,#gear-cursor::after { content:''; position:absolute; border:3px solid var(--accent); border-radius:50%; }
#gear-cursor::before { inset:4px; } /* 外齿轮 */
#gear-cursor::after { inset:12px; background:var(--accent); } /* 内轴 */
```
适用气质：蒸汽朋克 / 机械 / 工业 / 钟表

---

**CUR-AG：符文刻印（Rune Trail）**
```javascript
const runes='ᚠᚢᚦᚨᚱᚲᚷᚹᛃᛈᛇᛉᛊᛏᛒᛗᛚᛜᛞᛟ';
document.addEventListener('mousemove', e => {
  if(Math.random()>0.3) return;
  const r=document.createElement('span');
  r.className='rune-mark'; r.textContent=runes[Math.floor(Math.random()*runes.length)];
  r.style.left=e.clientX+'px'; r.style.top=e.clientY+'px';
  document.body.appendChild(r);
  setTimeout(()=>r.remove(),1500);
});
```
```css
.rune-mark { position:fixed; pointer-events:none; z-index:9996; font-size:14px; color:var(--accent); text-shadow:0 0 8px var(--accent); animation:rune-fade 1.5s ease-out forwards; }
@keyframes rune-fade { 0%{opacity:0.8;transform:translate(-50%,-50%) scale(1)} 100%{opacity:0;transform:translate(-50%,-50%) scale(1.5)} }
```
适用气质：奇幻 / 维京 / 魔法 / 北欧神话

---

**CUR-AH：像素十字（Pixel Cross）**
```javascript
// CSS绘制像素风十字光标，点击时闪烁hit marker
const pxCur=document.getElementById('pixel-cross');
document.addEventListener('mousemove',e=>{pxCur.style.transform=`translate(${e.clientX-8}px,${e.clientY-8}px)`;});
document.addEventListener('click',()=>{pxCur.classList.add('hit');setTimeout(()=>pxCur.classList.remove('hit'),200);});
```
```css
#pixel-cross { position:fixed; width:16px; height:16px; pointer-events:none; z-index:9999; image-rendering:pixelated; }
#pixel-cross::before,#pixel-cross::after { content:''; position:absolute; background:var(--accent); }
#pixel-cross::before { left:7px; top:0; width:2px; height:16px; }
#pixel-cross::after { left:0; top:7px; width:16px; height:2px; }
#pixel-cross.hit { filter:brightness(2); transform:scale(1.5)!important; }
```
适用气质：像素 / 街机 / 游戏 / 8-bit

---

### 11.5 扩展特效库（EFF-5 到 EFF-10）

**EFF-5：重力沙砾拖尾（Gravity Sand）**
```javascript
// 路径上散落带重力的沙粒，小颗粒受重力下落后消失
document.addEventListener('mousemove', e => {
  if (Math.random() > 0.35) return;
  const g = document.createElement('div');
  g.className = 'sand-grain';
  const vx = (Math.random()-0.5)*3, vy = -Math.random()*2;
  let gx=e.clientX, gy=e.clientY, gvy=vy, life=1;
  document.body.appendChild(g);
  (function drop(){
    gvy += 0.15; gx += vx; gy += gvy; life -= 0.03;
    g.style.cssText=`left:${gx}px;top:${gy}px;opacity:${life}`;
    if (life > 0) requestAnimationFrame(drop); else g.remove();
  })();
});
```
```css
.sand-grain { position:fixed; width:3px; height:3px; border-radius:50%; background:var(--accent); pointer-events:none; z-index:9996; transform:translate(-50%,-50%); }
```
适用气质：沙漠 / 奢侈品 / 旅行 / 建筑

**EFF-6：磁场力线（Field Lines）**
```javascript
// 鼠标周围实时绘制向外辐射的磁力线（SVG动态更新）
const svg = document.getElementById('field-svg');
let fx=0,fy=0;
document.addEventListener('mousemove', e=>{ fx=e.clientX; fy=e.clientY; updateField(); });
function updateField(){
  const lines = svg.querySelectorAll('line');
  lines.forEach((l,i)=>{
    const a = (i/lines.length)*Math.PI*2;
    const len = 30+Math.random()*15;
    l.setAttribute('x1',fx); l.setAttribute('y1',fy);
    l.setAttribute('x2',fx+Math.cos(a)*len); l.setAttribute('y2',fy+Math.sin(a)*len);
  });
}
```
```css
#field-svg { position:fixed; inset:0; pointer-events:none; z-index:9997; }
#field-svg line { stroke:var(--accent); stroke-width:1; opacity:0.4; }
```
适用气质：科技 / AI / 磁场主题 / 物理实验

**EFF-7：光圈快门（Aperture Iris）**
```javascript
// 悬停可点击元素时，光圈叶片合拢动画（类相机快门）
document.querySelectorAll('button,.card').forEach(el=>{
  el.addEventListener('mouseenter',()=>document.getElementById('iris').classList.add('iris-close'));
  el.addEventListener('mouseleave',()=>document.getElementById('iris').classList.remove('iris-close'));
  el.addEventListener('mousemove',e=>{
    const iris=document.getElementById('iris');
    iris.style.left=e.clientX+'px'; iris.style.top=e.clientY+'px';
  });
});
```
```css
#iris { position:fixed; width:50px; height:50px; pointer-events:none; z-index:9999; transform:translate(-50%,-50%); }
/* 6叶片用 conic-gradient + clip-path 模拟；实际实现可用SVG polygon旋转 */
#iris svg { animation: iris-rotate 4s linear infinite; }
#iris.iris-close svg { animation-play-state:paused; }
@keyframes iris-rotate { to { transform: rotate(360deg); } }
```
适用气质：摄影 / 电影 / 光学品牌

**EFF-8：拖影残影（Motion Blur Ghost）**
```javascript
// 鼠标后方留下3个渐变残影，透明度和尺寸递减
const ghosts = Array.from({length:4}, ()=> {
  const g=document.createElement('div'); g.className='motion-ghost'; document.body.appendChild(g); return g;
});
const trail=[];
document.addEventListener('mousemove', e=>{
  trail.push({x:e.clientX,y:e.clientY}); if(trail.length>16) trail.shift();
  ghosts.forEach((g,i)=>{
    const p=trail[trail.length-1-(i+1)*3];
    if(p){g.style.transform=`translate(${p.x}px,${p.y}px) translate(-50%,-50%)`;g.style.opacity=0.25-i*0.05;}
  });
});
```
```css
.motion-ghost { position:fixed; width:16px; height:16px; border-radius:50%; background:var(--accent); pointer-events:none; z-index:9996; filter:blur(3px); transition:opacity 0.1s; }
```
适用气质：速度 / 极限运动 / 赛车 / 科技

**EFF-9：光谱彩虹环（Chromatic Ring）**
```javascript
// 光标是一个彩虹渐变的旋转环，颜色随时间hue-rotate
const ring = document.getElementById('chroma-ring');
let hue=0;
document.addEventListener('mousemove', e=>{ ring.style.left=e.clientX+'px'; ring.style.top=e.clientY+'px'; });
(function loop(){ hue=(hue+1)%360; ring.style.filter=`hue-rotate(${hue}deg)`; requestAnimationFrame(loop); })();
```
```css
#chroma-ring {
  position:fixed; width:44px; height:44px; border-radius:50%; pointer-events:none; z-index:9999;
  transform:translate(-50%,-50%);
  border: 3px solid transparent;
  background: linear-gradient(var(--bg,#000),var(--bg,#000)) padding-box,
              linear-gradient(135deg,#ff0080,#ff8c00,#40e0d0,#8b00ff) border-box;
  box-shadow: 0 0 12px rgba(255,0,128,0.5), 0 0 24px rgba(64,224,208,0.3);
}
```
适用气质：彩虹 / Pride / 艺术 / 时尚 / 多巴胺配色

**EFF-10：声波可视化光标（Sound Wave）**
```javascript
// 鼠标周围Canvas绘制实时震荡声波圆圈，移动越快振幅越大
const waveCanvas = document.getElementById('wave-cursor-canvas');
const wc = waveCanvas.getContext('2d');
let wx=0,wy=0,wAmp=0,wt=0;
document.addEventListener('mousemove', e=>{ wAmp=Math.min(Math.hypot(e.movementX,e.movementY)*0.5, 20); wx=e.clientX; wy=e.clientY; });
(function draw(){
  waveCanvas.width=waveCanvas.width; // clear
  wt+=0.12; wAmp*=0.9;
  for(let r=15;r<=45;r+=10){
    wc.beginPath();
    for(let a=0;a<Math.PI*2;a+=0.05){
      const wave = wAmp * Math.sin(a*4 + wt + r*0.1);
      const x=wx+(r+wave)*Math.cos(a), y=wy+(r+wave)*Math.sin(a);
      a===0 ? wc.moveTo(x,y) : wc.lineTo(x,y);
    }
    wc.closePath();
    wc.strokeStyle=`hsla(${180+r*4},100%,70%,${0.5-r*0.008})`;
    wc.lineWidth=1; wc.stroke();
  }
  requestAnimationFrame(draw);
})();
```
```css
#wave-cursor-canvas { position:fixed; inset:0; pointer-events:none; z-index:9997; }
```
适用气质：音乐 / 科技 / 声音品牌 / 播客

---

### 11.5b 扩展特效库（EFF-11 到 EFF-20）

**EFF-11：引力场偏移（Gravity Field）**
```javascript
// 光标200px范围内，文字/标题微微向光标偏移
document.addEventListener('mousemove', e => {
  document.querySelectorAll('h1,h2,h3,p,.card-title').forEach(el => {
    const r=el.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
    const dx=e.clientX-cx, dy=e.clientY-cy, dist=Math.hypot(dx,dy);
    if(dist<200){ const f=Math.min(4,(200-dist)*0.02); el.style.transform=`translate(${dx/dist*f}px,${dy/dist*f}px)`; }
    else { el.style.transform=''; }
  });
});
```

**EFF-12：霜冻结晶（Frost Crystal）**
```javascript
// 悬停卡片时，卡片表面渐生半透明霜冻纹理overlay
document.querySelectorAll('.card').forEach(el => {
  const frost=document.createElement('div');
  frost.className='frost-overlay'; el.style.position='relative'; el.appendChild(frost);
  el.addEventListener('mouseenter',()=>frost.style.opacity='1');
  el.addEventListener('mouseleave',()=>frost.style.opacity='0');
});
```
```css
.frost-overlay { position:absolute; inset:0; background:url("data:image/svg+xml,...") repeat; opacity:0; transition:opacity 0.6s; pointer-events:none; border-radius:inherit; mix-blend-mode:overlay; }
```

**EFF-13：墨水扩散（Ink Splash）**
```javascript
document.addEventListener('click', e => {
  const ink=document.createElement('div'); ink.className='ink-splash';
  ink.style.left=e.clientX+'px'; ink.style.top=e.clientY+'px';
  document.body.appendChild(ink);
  setTimeout(()=>ink.remove(),900);
});
```
```css
.ink-splash { position:fixed; width:0; height:0; border-radius:50%; background:radial-gradient(circle,var(--ink) 0%,transparent 70%); pointer-events:none; z-index:9996; transform:translate(-50%,-50%); animation:ink-expand 0.9s ease-out forwards; }
@keyframes ink-expand { 0%{width:0;height:0;opacity:0.6} 100%{width:120px;height:120px;opacity:0} }
```

**EFF-14：热力图（Heat Map）**
```javascript
// 鼠标停留区域渐变显示热度色斑（Canvas实现）
const heatCvs=document.getElementById('heat-canvas'), hctx=heatCvs.getContext('2d');
heatCvs.width=innerWidth; heatCvs.height=innerHeight;
document.addEventListener('mousemove', e => {
  hctx.beginPath();
  const grad=hctx.createRadialGradient(e.clientX,e.clientY,0,e.clientX,e.clientY,40);
  grad.addColorStop(0,'rgba(255,0,0,0.03)'); grad.addColorStop(1,'transparent');
  hctx.fillStyle=grad; hctx.arc(e.clientX,e.clientY,40,0,Math.PI*2); hctx.fill();
});
// 每5秒整体淡化一次
setInterval(()=>{ hctx.fillStyle='rgba(255,255,255,0.05)'; hctx.fillRect(0,0,heatCvs.width,heatCvs.height); },5000);
```

**EFF-15：元素裂解（Crack Light）**
```javascript
// 悬停卡片时表面出现发光裂纹
document.querySelectorAll('.card').forEach(el => {
  el.addEventListener('mouseenter',()=>el.classList.add('cracked'));
  el.addEventListener('mouseleave',()=>el.classList.remove('cracked'));
});
```
```css
.card.cracked::after { content:''; position:absolute; inset:0; background:linear-gradient(135deg,transparent 40%,rgba(255,200,50,0.3) 50%,transparent 60%); clip-path:polygon(20% 0,22% 35%,45% 50%,40% 80%,60% 100%,58% 65%,80% 50%,75% 20%); opacity:1; transition:opacity 0.3s; }
```

**EFF-16：镜像倒影（Mirror Reflect）**
```javascript
// 光标下方生成半透明镜像
const mirror=document.getElementById('cursor-mirror');
document.addEventListener('mousemove', e => {
  mirror.style.transform=`translate(${e.clientX-10}px,${e.clientY+15}px) scaleY(-0.6)`;
});
```
```css
#cursor-mirror { position:fixed; width:20px; height:20px; border-radius:50%; background:var(--accent); opacity:0.2; pointer-events:none; z-index:9996; filter:blur(2px); }
```

**EFF-17：虫洞漩涡（Wormhole Vortex）**
```javascript
document.addEventListener('click', e => {
  const v=document.createElement('div'); v.className='vortex';
  v.style.left=e.clientX+'px'; v.style.top=e.clientY+'px';
  document.body.appendChild(v);
  setTimeout(()=>v.remove(),800);
});
```
```css
.vortex { position:fixed; width:60px; height:60px; border:2px solid var(--accent); border-radius:50%; pointer-events:none; z-index:9996; transform:translate(-50%,-50%) scale(0) rotate(0); animation:vortex-spin 0.8s ease-in forwards; }
@keyframes vortex-spin { 0%{transform:translate(-50%,-50%) scale(2) rotate(0);opacity:0.8} 100%{transform:translate(-50%,-50%) scale(0) rotate(720deg);opacity:0} }
```

**EFF-18：静电吸附（Static Attract）**
```javascript
// 靠近元素时小粒子从元素飞向光标
document.querySelectorAll('button,.card').forEach(el => {
  el.addEventListener('mouseenter', e => {
    for(let i=0;i<5;i++){
      const p=document.createElement('div'); p.className='static-dot';
      const r=el.getBoundingClientRect();
      p.style.left=r.left+Math.random()*r.width+'px';
      p.style.top=r.top+Math.random()*r.height+'px';
      p.style.setProperty('--tx',e.clientX-parseFloat(p.style.left)+'px');
      p.style.setProperty('--ty',e.clientY-parseFloat(p.style.top)+'px');
      document.body.appendChild(p);
      setTimeout(()=>p.remove(),500);
    }
  });
});
```
```css
.static-dot { position:fixed; width:3px; height:3px; border-radius:50%; background:var(--accent); pointer-events:none; z-index:9996; animation:static-fly 0.5s ease-in forwards; }
@keyframes static-fly { to { transform:translate(var(--tx),var(--ty)); opacity:0; } }
```

**EFF-19：路径描绘（Path Draw）**
```javascript
// SVG实时绘制鼠标移动路径后渐隐
const pathSvg=document.getElementById('path-svg');
let pathD='', lastPx=0, lastPy=0, pathEl=null;
document.addEventListener('mousemove', e => {
  if(!pathEl||Math.hypot(e.clientX-lastPx,e.clientY-lastPy)>200){
    pathEl=document.createElementNS('http://www.w3.org/2000/svg','path');
    pathEl.setAttribute('fill','none'); pathEl.setAttribute('stroke','var(--accent)');
    pathEl.setAttribute('stroke-width','1.5'); pathEl.setAttribute('opacity','0.5');
    pathSvg.appendChild(pathEl); pathD=`M${e.clientX} ${e.clientY}`;
    setTimeout(()=>{pathEl.style.transition='opacity 1s';pathEl.style.opacity='0';setTimeout(()=>pathEl.remove(),1000);},2000);
  } else { pathD+=` L${e.clientX} ${e.clientY}`; }
  pathEl.setAttribute('d',pathD);
  lastPx=e.clientX; lastPy=e.clientY;
});
```

**EFF-20：脉冲波纹（Pulse Ring）**
```javascript
document.addEventListener('click', e => {
  for(let i=0;i<3;i++){
    const ring=document.createElement('div'); ring.className='pulse-ring';
    ring.style.left=e.clientX+'px'; ring.style.top=e.clientY+'px';
    ring.style.animationDelay=i*0.15+'s';
    document.body.appendChild(ring);
    setTimeout(()=>ring.remove(),1000);
  }
});
```
```css
.pulse-ring { position:fixed; width:10px; height:10px; border:2px solid var(--accent); border-radius:50%; pointer-events:none; z-index:9996; transform:translate(-50%,-50%); animation:pulse-out 0.8s ease-out forwards; }
@keyframes pulse-out { to { width:100px; height:100px; opacity:0; transform:translate(-50%,-50%); } }
```

---

### 11.6 扩展后完整光标速查表

| 代号 | 名称 | 核心效果 | 最适气质 |
|------|------|---------|---------|
| CUR-A | 圆点+延迟环 | 8px点+36px弹性跟随环 | 通用奢侈品/设计 |
| CUR-B | Blend反色 | mix-blend-mode:difference 圆形 | 极简/摄影/黑白 |
| CUR-C | 文字环绕 | 品牌文字沿圆弧旋转跟随 | 品牌/奢侈品 |
| CUR-D | 粒子轨迹 | 彩色粒子从光标喷出 | 创意/艺术 |
| CUR-E | 磁性吸附 | 光标被最近按钮磁吸 | SaaS/工具 |
| CUR-F | SVG图形 | 自定义≤40px SVG跟随 | 任意 |
| CUR-G | Canvas粒子拖尾 | Canvas重力粒子流 | 科技/宇宙 |
| CUR-H | 液态水滴 | 按速度方向拉伸变形的blob | 时尚/wellness |
| CUR-I | 弹性橡皮筋 | 弹簧物理拖尾+拉伸 | 玩具/运动 |
| CUR-J | 像素马赛克 | 彩色像素块拖尾 | Y2K/游戏/潮牌 |
| CUR-K | 磁性卫星群 | 8个小点绕光标旋转 | 科技/AI/宇宙 |
| CUR-L | 霓虹光晕 | hue-rotate彩色发光环 | 赛博/电音/游戏 |
| CUR-M | 墨迹拖尾 | Canvas书法墨迹渐fade | 日式/书法/奢侈品 |
| CUR-N | 果冻弹跳 | 弹簧过冲+压扁变形 | 儿童/创意/可爱 |
| CUR-O | 雷达扫描 | 旋转扇形+同心圆 | 军事/数据/黑客 |
| CUR-P | 取景框 | 四角L形取景框+悬停放大 | 摄影/电影/时尚 |
| CUR-Q | 火焰拖尾 | 橙红粒子上升燃烧 | 极限运动/烈酒/游戏 |
| CUR-R | 星尘彗星 | 星形头+星点串拖尾 | 宇宙/VR/占星 |
| CUR-S | 终端光标 | 闪烁插入符+>_提示符 | 开发者/终端/SaaS |
| CUR-T | 均衡器 | 5根动态波动竖条 | 音乐/播客/活动 |
| CUR-X | 无自定义形状 | 系统光标+EFF效果补偿 | 任意（补偿型） |
| **扩展光标变体（CUR-U ~ CUR-AH）** ||||
| CUR-U | 墨水晕染 | 点击处墨水圆圈向外扩散晕染 | 水墨/书法/日式 |
| CUR-V | 棱镜折射 | 光标周围三棱镜分光彩虹条纹 | 闪光朋克/全息/科技 |
| CUR-W | 重力井 | 光标附近DOM元素微微被吸引偏移 | 科技/物理/太空 |
| CUR-X2 | 时钟指针 | 小型钟面+旋转指针跟随鼠标方向 | 复古/奢华/钟表 |
| CUR-Y | 音符飘落 | 移动时散出音符符号粒子上浮 | 音乐/播客/派对 |
| CUR-Z | 蝴蝶翅膀 | 两片翅膀随速度开合扇动 | 自然/童话/花店 |
| CUR-AA | 水波涟漪 | 光标处持续圆形水波纹扩散 | 海洋/SPA/自然 |
| CUR-AB | 指南针 | 圆形罗盘+指针指向最近可交互元素 | 旅行/导航/探索 |
| CUR-AC | DNA双螺旋 | 两条螺旋线围绕光标旋转上升 | 生物科技/医疗/科研 |
| CUR-AD | 烟雾缭绕 | 半透明烟雾粒子从光标升起飘散 | 香氛/雪茄/神秘 |
| CUR-AE | 电弧放电 | 光标与附近元素间闪烁电弧线条 | 赛博/电力/科幻 |
| CUR-AF | 齿轮旋转 | 两个咬合齿轮围绕光标转动 | 蒸汽朋克/机械/工业 |
| CUR-AG | 符文刻印 | 移动路径上留下发光符文渐隐 | 奇幻/维京/魔法 |
| CUR-AH | 像素十字 | 像素风格十字光标+击中特效 | 像素/街机/游戏 |

| EFF代号 | 名称 | 触发条件 |
|--------|------|---------|
| EFF-1 | 文字轨道 | 悬停元素时文字绕圆旋转 |
| EFF-2 | 点击爆炸 | 每次点击粒子爆散 |
| EFF-3 | 磁场涟漪 | 鼠标靠近按钮产生涟漪 |
| EFF-4 | 颜色区域感知 | 进入不同section变色 |
| EFF-5 | 重力沙砾 | 路径上散落受重力下落的沙粒 |
| EFF-6 | 磁场力线 | 鼠标周围辐射状力线 |
| EFF-7 | 光圈快门 | 悬停时相机叶片合拢 |
| EFF-8 | 运动残影 | 高速移动留下ghost残像 |
| EFF-9 | 光谱彩虹环 | 持续hue-rotate彩虹边框 |
| EFF-10 | 声波可视化 | 移动速度驱动Canvas声波圆圈 |
| **扩展特效（EFF-11 ~ EFF-20）** |||
| EFF-11 | 引力场偏移 | 光标附近文字/元素微微向光标偏移 |
| EFF-12 | 霜冻结晶 | 悬停区域表面渐生冰霜纹理 |
| EFF-13 | 墨水扩散 | 点击处墨水圆圈扩散染色后淡出 |
| EFF-14 | 热力图 | 鼠标停留区域渐变显示热度色斑 |
| EFF-15 | 元素裂解 | 悬停卡片时表面出现裂纹光线 |
| EFF-16 | 镜像倒影 | 光标下方生成半透明镜像倒影 |
| EFF-17 | 虫洞漩涡 | 点击处旋转螺旋吸入动画 |
| EFF-18 | 静电吸附 | 靠近元素时小粒子从元素飞向光标 |
| EFF-19 | 路径描绘 | 移动路径实时绘制SVG线条后渐隐 |
| EFF-20 | 脉冲波纹 | 每次点击发出雷达式扩散脉冲环 |

> **冷却规则（更新）**：CUR-A~CUR-AH + CUR-X 共35种，连续5条内同一CUR代号不重复；EFF-1~EFF-20 共20种，每条必选 ≥ 1 个 EFF，连续3条内同一EFF不重复。

---

### 11.7 禁止光标形态（硬性禁止）

> **禁止全屏十字准心光标**：即以竖线从顶延伸到底、横线从左延伸到右，两线交叉构成全屏级"瞄准镜/准心"形态的光标（如 `fdu_496` 同款）。

**判定标准**：以下任意一点成立即判为违规：
- 竖线或横线长度超过 `100px`，且以鼠标坐标为中心跟随移动
- 使用 `position:fixed; top:0; bottom:0`（即 `height:100vh`）的竖线元素作为光标组成部分
- 使用 `position:fixed; left:0; right:0`（即 `width:100vw`）的横线元素作为光标组成部分

所有合法光标变体的最大有效尺寸不得超过 **80px × 80px**。

---

## 十二、Features 板块替代规范（Anti-Generic Features）

> **核心问题**：三列矩形卡片 + emoji图标 + 功能标题 + 描述文字 是最泛滥、最低质的版式，数据集中频繁出现会被平台降权。**每条必须在确认卡中声明 Features 处理方案**。

### 12.1 冷却规则

- 连续 **2 条**内，标准三/四列 Features 卡片网格不得作为独立 Section 出现
- 即使使用 Features，形式必须有实质差异（见 §12.2）
- 在确认卡的 `Features替代方案` 字段中声明方案代号（F-00 到 F-10）

### 12.2 Features 替代方案库

| 代号 | 名称 | 实现思路 | 适用气质 |
|-----|------|---------|---------|
| **F-00** | 标准卡片（受限使用） | 三/四列矩形，图标+标题+描述。**连续2条内最多1次** | 通用，但受冷却约束 |
| **F-01** | 横向滚动时间线 | 功能点排列在水平轨道上，鼠标/触摸横向拖拽；每个节点展开详情 | 流程/步骤类功能 |
| **F-02** | 手风琴展开列表 | 竖向折叠列表，每行是一个功能；hover/click 展开 200px 的图示和详情 | SaaS/工具/内容密集 |
| **F-03** | 宾托网格（Bento Grid） | 大小不一的非等比格子，1大+2中+4小的不规则布局；重要功能占大格 | 现代SaaS/App推广 |
| **F-04** | 数字气泡对照 | 每个功能配一个大数字指标（如 "3× faster" "99.9%"）；数字+描述竖排，无卡片边框 | 性能工具/数据型产品 |
| **F-05** | 交互式功能演示 | 用Tab/Radio切换，每个功能有对应的动态预览区域（mockup/图示） | 软件产品/SaaS |
| **F-06** | 悬停揭示列表 | 平时只显示功能名 + 序号，hover 时整行展开并变色显示详情 | 极简/设计感/奢侈品 |
| **F-07** | 倾斜/错位卡片排布 | 卡片用 `rotate(±2deg)` + 负margin错位排列，打破网格感 | 创意/手作/娱乐 |
| **F-08** | 分栏对比叙述 | 左侧大标题/痛点描述，右侧解决方案特性逐条出现（苹果风格） | 硬件/企业/信任构建 |
| **F-09** | 环形/雷达图展示 | 功能分布在圆形轨道上，鼠标悬停激活对应节点展示详情 | 数据/AI/技术品牌 |
| **F-10** | 完全跳过，分散植入 | 不设 Features Section，将功能点拆解融入 Hero/Stats/Quote/W码互动中 | 叙事型/游戏/沉浸式 |

### 12.3 使用规则细则

```
✅ 允许：
  - F-00 标准卡片，但加上 CARD-A 到 CARD-G 的非矩形造型（如切角、偏移阴影）
  - F-00 标准卡片，但图标改为纯 SVG line art 或数字序号，禁止 emoji 图标
  - F-03 Bento 网格（不受 F-00 冷却约束，可连续使用）
  - F-10 完全跳过（最鼓励的做法，特别是游戏/沉浸式/叙事型页面）

❌ 禁止：
  - 连续2条都用 F-00 标准矩形卡片
  - F-00 卡片中使用 emoji 作为图标（改用内联SVG或文字序号 01/02/03）
  - Features Section 超过 6 个卡片且无交互（静态信息墙）
  - Features 作为页面第二个 Section 且内容与 Hero 高度重叠
```

### 12.4 Bento Grid 实现规范（F-03，推荐方案）

```css
/* 不规则 Bento 布局 */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  grid-template-rows: auto;
  gap: 16px;
}
/* 大格（主功能）*/
.bento-large  { grid-column: span 4; grid-row: span 2; }
/* 中格 */
.bento-medium { grid-column: span 2; grid-row: span 2; }
/* 小格 */
.bento-small  { grid-column: span 2; grid-row: span 1; }
/* 宽格（横幅）*/
.bento-wide   { grid-column: span 6; grid-row: span 1; }

/* 每格必须有独立主题色/渐变背景，禁止所有格颜色相同 */
.bento-card:nth-child(odd)  { background: var(--surface); }
.bento-card:nth-child(even) { background: linear-gradient(135deg, var(--accent-dim), var(--surface)); }
```

### 12.5 悬停揭示列表实现规范（F-06，极简风推荐）

```css
.feat-list-item {
  display: flex; align-items: baseline;
  padding: 20px 0;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  cursor: none; overflow: hidden;
  transition: padding 0.35s cubic-bezier(0.16,1,0.3,1), background 0.3s;
}
.feat-num {
  font-size: 11px; letter-spacing: 3px;
  color: var(--accent); min-width: 48px;
  font-family: monospace;
}
.feat-title {
  font-size: clamp(18px, 2.5vw, 28px); font-weight: 700;
  flex: 1;
  transition: transform 0.3s, color 0.3s;
}
.feat-detail {
  max-height: 0; opacity: 0; overflow: hidden;
  font-size: 14px; color: var(--text-dim); line-height: 1.8;
  transition: max-height 0.5s cubic-bezier(0.16,1,0.3,1), opacity 0.4s;
}
.feat-list-item:hover {
  padding: 20px 16px;
  background: rgba(255,255,255,0.03);
}
.feat-list-item:hover .feat-title { transform: translateX(8px); color: var(--accent); }
.feat-list-item:hover .feat-detail { max-height: 120px; opacity: 1; }
```

---

## 十三、酷炫动画与交互特效扩展库（Animation & Interaction FX Library）

> 以下特效均为可选增强项，按气质匹配选用。每条 HTML 建议从以下库中选取 **≥ 3 个**额外特效，以提升视觉差异度和记忆点。在确认卡的 `特效选用` 字段中声明代号。

---

### 13.1 文字动效（TEXT EFFECTS）

**TX-01：文字粒子解体重组（Text Particle Disintegrate）**
```javascript
// 点击/hover 标题时，文字分解为粒子飞散，再重新聚合
function disintegrateText(el) {
  const text = el.textContent;
  const chars = text.split('').map(c => {
    const span = document.createElement('span');
    span.textContent = c; span.style.display = 'inline-block';
    return span;
  });
  el.innerHTML = ''; chars.forEach(s => el.appendChild(s));
  chars.forEach((s, i) => {
    const tx = (Math.random()-0.5)*200, ty = (Math.random()-0.5)*200;
    s.style.transition = `transform ${0.4+Math.random()*0.3}s cubic-bezier(0.55,0,1,0.45) ${i*0.02}s, opacity 0.4s ${i*0.02}s`;
    requestAnimationFrame(() => { s.style.transform=`translate(${tx}px,${ty}px) rotate(${Math.random()*360}deg) scale(0)`; s.style.opacity='0'; });
    setTimeout(() => {
      s.style.transition = `transform 0.6s cubic-bezier(0.16,1,0.3,1) ${i*0.03}s, opacity 0.4s ${i*0.03}s`;
      s.style.transform = 'translate(0,0) rotate(0deg) scale(1)'; s.style.opacity='1';
    }, 800);
  });
}
```
适用：Hero标题点击 / 页面载入动画 / 品牌揭示

---

**TX-02：数字乱码Scramble（Glitch Number Scramble）**
```javascript
// 数字/字母从随机字符快速滚动到目标值
function scramble(el, target, duration=1200) {
  const chars = '0123456789ABCDEFX@#$%';
  const start = performance.now();
  const targetText = String(target);
  (function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const resolved = Math.floor(progress * targetText.length);
    let result = '';
    for (let i = 0; i < targetText.length; i++) {
      result += i < resolved ? targetText[i] : chars[Math.floor(Math.random()*chars.length)];
    }
    el.textContent = result;
    if (progress < 1) requestAnimationFrame(tick);
    else el.textContent = targetText;
  })(start);
}
```
```css
.scramble-text { font-variant-numeric: tabular-nums; letter-spacing: 0.1em; }
```
适用：统计数字/数据面板/科技页面

---

**TX-03：液态文字变形（Liquid Text Morph）**
```css
/* 两个文字标签叠放，通过 SVG feDisplacementMap + feTurbulence 制造液态扭曲过渡 */
.liquid-text-wrap {
  position: relative;
  filter: url(#liquid-filter);
}
@keyframes liquid-in {
  0%   { filter: url(#liquid-filter) blur(4px); opacity: 0; transform: scale(0.95); }
  60%  { filter: url(#liquid-filter); opacity: 1; }
  100% { filter: none; opacity: 1; transform: scale(1); }
}
```
```html
<svg style="position:absolute;width:0;height:0">
  <defs>
    <filter id="liquid-filter">
      <feTurbulence type="turbulence" baseFrequency="0.015" numOctaves="2" seed="2" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="30" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
</svg>
```
适用：wellness/奢侈品/水墨/有机品牌 section切换

---

**TX-04：打字机逐字揭示+光标（Typewriter with Caret）**
```javascript
function typewriter(el, text, speed=40, cursor=true) {
  el.textContent = '';
  if (cursor) { el.style.borderRight = '2px solid var(--accent)'; el.style.animation = 'caret-blink 1s step-end infinite'; }
  let i = 0;
  const timer = setInterval(() => {
    el.textContent += text[i++];
    if (i >= text.length) {
      clearInterval(timer);
      setTimeout(() => { el.style.borderRight = 'none'; el.style.animation = 'none'; }, 2000);
    }
  }, speed);
}
```
```css
@keyframes caret-blink { 0%,100%{border-color:var(--accent)} 50%{border-color:transparent} }
```
适用：Hero副标题 / 终端输出 / 加载状态 / FAQ答案揭示

---

**TX-05：文字描边填充动画（SVG Text Stroke Draw）**
```html
<svg viewBox="0 0 800 120" class="svg-text-hero">
  <text x="50%" y="80%" text-anchor="middle"
    font-family="'Orbitron'" font-size="80" font-weight="900"
    fill="none" stroke="var(--accent)" stroke-width="2"
    stroke-dasharray="2000" stroke-dashoffset="2000"
    style="animation: stroke-draw 2s cubic-bezier(0.16,1,0.3,1) 0.5s forwards">
    BRAND
  </text>
</svg>
```
```css
@keyframes stroke-draw { to { stroke-dashoffset: 0; } }
/* 延迟后填充颜色 */
@keyframes fill-in { to { fill: var(--accent); } }
```
适用：Hero主标题 / 品牌揭示 / 章节标题

---

**TX-06：文字水平滚动跑马灯（Marquee Track）**
```css
.marquee-track {
  overflow: hidden; white-space: nowrap;
  border-top: 1px solid rgba(255,255,255,0.1);
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding: 12px 0;
}
.marquee-inner {
  display: inline-block;
  animation: marquee-scroll 20s linear infinite;
}
.marquee-inner:hover { animation-play-state: paused; }
@keyframes marquee-scroll { from{transform:translateX(0)} to{transform:translateX(-50%)} }
/* 双份内容保证无缝：<div class="marquee-inner">内容 &nbsp;· 内容 · &nbsp; 内容 · (重复一遍)</div> */
```
```css
/* 变体：纵向滚动 */
@keyframes marquee-vertical { from{transform:translateY(0)} to{transform:translateY(-50%)} }
/* 变体：鼠标方向反向 */
.marquee-track:hover .marquee-inner { animation-direction: reverse; }
```
适用：品牌合作logo墙 / 技术标签 / 社会证明 / 滚动公告

---

**TX-07：文字视差分层（Text Parallax Depth）**
```javascript
// 多行标题按不同速率响应鼠标移动，制造视差层次感
document.addEventListener('mousemove', e => {
  const cx = window.innerWidth/2, cy = window.innerHeight/2;
  const dx = (e.clientX-cx)/cx, dy = (e.clientY-cy)/cy;
  document.querySelectorAll('[data-depth]').forEach(el => {
    const depth = parseFloat(el.dataset.depth);
    el.style.transform = `translate(${dx*depth*20}px, ${dy*depth*10}px)`;
  });
});
```
```html
<!-- 不同data-depth值产生视差层次 -->
<h1 data-depth="0.2" class="hero-line-1">DISCOVER</h1>
<h2 data-depth="0.5" class="hero-line-2">THE FUTURE</h2>
<p  data-depth="0.8" class="hero-sub">Next generation platform</p>
```
适用：Hero区 / 全屏banner / 沉浸式叙事

---

**TX-08：字符随机跳动（Character Jitter）**
```javascript
// hover标题时每个字符随机上下跳动形成律动感
function jitterText(el) {
  const chars = el.querySelectorAll('.jitter-char');
  chars.forEach((c, i) => {
    c.style.animation = `jitter-hop 0.4s ${i*0.04}s cubic-bezier(0.34,1.56,0.64,1) both`;
  });
}
```
```css
@keyframes jitter-hop {
  0%,100% { transform: translateY(0) rotate(0deg); }
  30%     { transform: translateY(-12px) rotate(-5deg); }
  60%     { transform: translateY(-6px) rotate(3deg); }
}
.jitter-char { display: inline-block; }
```
适用：游戏/儿童/创意/玩具品牌 导航hover / Logo hover

---

### 13.2 背景与氛围特效（BACKGROUND EFFECTS）

**BG-01：CSS Noise 颗粒纹理叠加层（Grain Overlay）**
```css
/* 全页面颗粒感叠层，提升质感，常驻 */
body::after {
  content: '';
  position: fixed; inset: 0;
  pointer-events: none; z-index: 9990;
  opacity: 0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  animation: grain-shift 0.5s steps(2) infinite;
}
@keyframes grain-shift {
  0%   { transform: translate(0,0); }
  25%  { transform: translate(-1%,1%); }
  50%  { transform: translate(1%,-1%); }
  75%  { transform: translate(-1%,-1%); }
  100% { transform: translate(1%,1%); }
}
```
适用：几乎所有高端品牌页面，增加胶片/印刷质感

---

**BG-02：极光渐变背景（Aurora Gradient）**
```css
/* 三个大色块缓慢互相渗透，形成极光效果 */
.aurora-bg {
  position: absolute; inset: 0; overflow: hidden;
  background: var(--bg-dark);
}
.aurora-blob {
  position: absolute; border-radius: 50%;
  filter: blur(80px); opacity: 0.35;
  animation: aurora-drift 12s ease-in-out infinite alternate;
}
.aurora-blob:nth-child(1) { width:600px; height:600px; background:var(--color1); top:-20%; left:-10%; animation-delay:0s; }
.aurora-blob:nth-child(2) { width:500px; height:500px; background:var(--color2); top:20%; right:-15%; animation-delay:-4s; }
.aurora-blob:nth-child(3) { width:400px; height:700px; background:var(--color3); bottom:-20%; left:30%; animation-delay:-8s; }
@keyframes aurora-drift {
  0%   { transform: translate(0,0) scale(1) rotate(0deg); }
  33%  { transform: translate(60px,-40px) scale(1.1) rotate(15deg); }
  66%  { transform: translate(-40px,60px) scale(0.9) rotate(-10deg); }
  100% { transform: translate(30px,20px) scale(1.05) rotate(5deg); }
}
```
适用：wellness/AI/创意工作室/播客 暗色主题

---

**BG-03：网格扫描线（Cyber Grid Scan）**
```css
.cyber-grid {
  position: absolute; inset: 0; pointer-events: none;
  background-image:
    linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
}
/* 水平扫描线从上到下匀速划过 */
.scan-line {
  position: absolute; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent 0%, rgba(0,229,255,0.6) 50%, transparent 100%);
  animation: scan-sweep 6s linear infinite;
  pointer-events: none;
}
@keyframes scan-sweep { from{top:-2px} to{top:100%} }
/* 变体：斜向扫描 */
.scan-diagonal { transform: rotate(-15deg) scaleX(1.5); }
```
适用：赛博/科技/游戏/VR/AI 页面

---

**BG-04：流动渐变网格（Mesh Gradient Flow）**
```css
/* CSS变量驱动的8色渐变网格，缓慢流动 */
.mesh-gradient {
  background:
    radial-gradient(ellipse at 20% 20%, var(--g1) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 10%, var(--g2) 0%, transparent 50%),
    radial-gradient(ellipse at 10% 80%, var(--g3) 0%, transparent 50%),
    radial-gradient(ellipse at 90% 80%, var(--g4) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, var(--g5) 0%, transparent 60%);
  animation: mesh-flow 15s ease-in-out infinite alternate;
}
@keyframes mesh-flow {
  0%   { background-size: 100% 100%; background-position: 0% 0%, 100% 0%, 0% 100%, 100% 100%, 50% 50%; }
  50%  { background-size: 120% 120%; background-position: 10% 20%, 90% 10%, 5% 90%, 95% 85%, 55% 45%; }
  100% { background-size: 110% 110%; background-position: 5% 10%, 85% 5%, 15% 80%, 90% 90%, 45% 55%; }
}
```
适用：AI/创意/设计/渐变美学主题

---

**BG-05：粒子连线网络（Particle Network Canvas）**
```javascript
// 全屏Canvas粒子网络：粒子漂浮 + 距离内连线 + 鼠标排斥
function initParticleNetwork(canvas, opts = {}) {
  const ctx = canvas.getContext('2d');
  const N = opts.count || 80, CONN = opts.connectDist || 120, REP = opts.repelDist || 100;
  const accent = opts.color || '#00e5ff';
  let W, H, particles = [], mx = -999, my = -999;
  function resize() { W = canvas.width = canvas.offsetWidth; H = canvas.height = canvas.offsetHeight; }
  resize(); window.addEventListener('resize', resize);
  canvas.addEventListener('mousemove', e => { const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; });
  for (let i = 0; i < N; i++) particles.push({ x:Math.random()*W, y:Math.random()*H, vx:(Math.random()-.5)*.4, vy:(Math.random()-.5)*.4, r:Math.random()*2+1 });
  (function draw() {
    ctx.clearRect(0,0,W,H);
    particles.forEach(p => {
      const dx=p.x-mx, dy=p.y-my, d=Math.sqrt(dx*dx+dy*dy);
      if (d < REP) { p.vx += dx/d*.5; p.vy += dy/d*.5; }
      p.vx *= 0.98; p.vy *= 0.98;
      p.x = (p.x+p.vx+W)%W; p.y = (p.y+p.vy+H)%H;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle = accent; ctx.globalAlpha = 0.7; ctx.fill();
    });
    ctx.globalAlpha = 1;
    for (let i=0;i<particles.length;i++) for(let j=i+1;j<particles.length;j++) {
      const dx=particles[i].x-particles[j].x, dy=particles[i].y-particles[j].y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if (d < CONN) {
        ctx.beginPath(); ctx.moveTo(particles[i].x,particles[i].y); ctx.lineTo(particles[j].x,particles[j].y);
        ctx.strokeStyle = accent; ctx.globalAlpha = (1-d/CONN)*0.2; ctx.lineWidth=.5; ctx.stroke();
      }
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  })();
}
```
适用：科技/AI/VR/数据平台 全屏背景或Hero背景

---

**BG-06：星空视差滚动（Star Parallax Scroll）**
```javascript
// 三层星星按不同速率随滚动移动，制造深度感
function initStarParallax() {
  const layers = [0.1, 0.3, 0.6].map((speed, li) => {
    const canvas = document.getElementById(`star-layer-${li}`);
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    const stars = Array.from({length: 60+li*40}, () => ({
      x: Math.random()*canvas.width, y: Math.random()*canvas.height,
      r: 0.5+Math.random()*(li+0.5), a: Math.random()
    }));
    return { ctx, stars, speed, canvas };
  });
  let scrollY = 0;
  window.addEventListener('scroll', () => { scrollY = window.scrollY; });
  (function draw() {
    layers.forEach(({ctx, stars, speed, canvas}) => {
      ctx.clearRect(0,0,canvas.width,canvas.height);
      const offset = scrollY * speed % canvas.height;
      stars.forEach(s => {
        const y = (s.y + offset) % canvas.height;
        ctx.beginPath(); ctx.arc(s.x, y, s.r, 0, Math.PI*2);
        ctx.fillStyle = `rgba(255,255,255,${s.a})`; ctx.fill();
      });
    });
    requestAnimationFrame(draw);
  })();
}
```
适用：宇宙/VR/奢侈品/夜间主题 滚动页面

---

**BG-07：数字雨（Matrix Rain）**
```javascript
// 绿色字符从上往下流淌，Matrix风格
function matrixRain(canvas) {
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  const cols = Math.floor(canvas.width / 16);
  const drops = Array(cols).fill(0).map(() => Math.random() * canvas.height);
  const chars = '01アイウエオカキクケコABCDEF0123456789';
  function draw() {
    ctx.fillStyle = 'rgba(0,0,0,0.04)'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = '#00ff41'; ctx.font = '14px monospace';
    drops.forEach((y, i) => {
      const char = chars[Math.floor(Math.random()*chars.length)];
      ctx.fillText(char, i*16, y);
      if (y > canvas.height && Math.random() > 0.975) drops[i] = 0;
      drops[i] += 16;
    });
  }
  setInterval(draw, 50);
}
```
适用：黑客/赛博/程序员/密室逃脱/反乌托邦 主题

---

**BG-08：有机流动Blob（Organic Morphing Blob）**
```css
/* CSS纯实现：border-radius不规则变形制造有机流动感 */
.organic-blob {
  position: absolute;
  width: 500px; height: 500px;
  background: radial-gradient(circle at 40% 40%, var(--accent), var(--accent2));
  filter: blur(40px); opacity: 0.3;
  animation: blob-morph 10s ease-in-out infinite alternate;
}
@keyframes blob-morph {
  0%   { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: rotate(0deg) scale(1); }
  25%  { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; transform: rotate(90deg) scale(1.05); }
  50%  { border-radius: 50% 50% 40% 60% / 40% 50% 60% 50%; transform: rotate(180deg) scale(0.95); }
  75%  { border-radius: 40% 60% 50% 50% / 70% 30% 50% 40%; transform: rotate(270deg) scale(1.08); }
  100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; transform: rotate(360deg) scale(1); }
}
```
适用：wellness/AI/创意/有机品牌 背景装饰

---

### 13.3 卡片与容器特效（CARD & CONTAINER EFFECTS）

**CD-01：全息镭射折射（Holographic Foil）**
```css
/* hover时卡片出现彩虹光谱移动，模拟镭射卡效果 */
.holo-card {
  position: relative; overflow: hidden;
  transition: transform 0.3s;
}
.holo-card::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(
    105deg,
    transparent 40%, rgba(255,219,112,0.3) 45%,
    rgba(132,50,255,0.3) 50%, rgba(0,229,255,0.3) 55%,
    transparent 60%
  );
  background-size: 200% 200%;
  opacity: 0; transition: opacity 0.3s;
  pointer-events: none;
  mix-blend-mode: color-dodge;
}
.holo-card:hover::before {
  opacity: 1;
  animation: holo-shift 3s linear infinite;
}
@keyframes holo-shift {
  0%   { background-position: 0% 0%; }
  100% { background-position: 200% 200%; }
}
/* JS增强：鼠标位置影响光谱角度 */
```
```javascript
document.querySelectorAll('.holo-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX-r.left)/r.width*100;
    const y = (e.clientY-r.top)/r.height*100;
    card.style.setProperty('--hx', x+'%');
    card.style.setProperty('--hy', y+'%');
    card.style.transform = `perspective(600px) rotateX(${(y-50)*0.1}deg) rotateY(${(x-50)*0.15}deg)`;
  });
  card.addEventListener('mouseleave', () => { card.style.transform = ''; });
});
```
适用：NFT/游戏卡牌/潮牌/收藏品页面

---

**CD-02：卡片翻转揭示（3D Card Flip）**
```css
.flip-card { perspective: 800px; }
.flip-card-inner {
  position: relative; width: 100%; height: 100%;
  transition: transform 0.7s cubic-bezier(0.16,1,0.3,1);
  transform-style: preserve-3d;
}
.flip-card:hover .flip-card-inner { transform: rotateY(180deg); }
.flip-card-front, .flip-card-back {
  position: absolute; inset: 0;
  backface-visibility: hidden; -webkit-backface-visibility: hidden;
}
.flip-card-back {
  transform: rotateY(180deg);
  background: var(--card-back-bg, var(--accent));
  display: flex; align-items: center; justify-content: center;
}
/* 变体：纵向翻转 */
.flip-vertical:hover .flip-card-inner { transform: rotateX(180deg); }
/* 变体：对角翻转 */
.flip-diagonal:hover .flip-card-inner { transform: rotateY(180deg) rotateX(10deg); }
```
适用：产品展示/功能卡片/人物介绍/FAQ

---

**CD-03：卡片堆叠展开（Stack Spread）**
```javascript
// 默认状态卡片叠放，hover展开成扇形或横排
const stack = document.querySelector('.card-stack');
const cards = stack.querySelectorAll('.stack-card');
stack.addEventListener('mouseenter', () => {
  cards.forEach((c, i) => {
    const spread = (i - (cards.length-1)/2) * 60;
    const rotate = (i - (cards.length-1)/2) * 8;
    c.style.transform = `translateX(${spread}px) rotate(${rotate}deg) translateY(-20px)`;
    c.style.zIndex = i;
    c.style.transition = `transform 0.4s cubic-bezier(0.34,1.56,0.64,1) ${i*0.05}s`;
  });
});
stack.addEventListener('mouseleave', () => {
  cards.forEach((c, i) => {
    c.style.transform = `translateX(${i*4}px) translateY(${-i*4}px) rotate(${(i-(cards.length-1)/2)*2}deg)`;
  });
});
```
适用：画廊/作品集/产品多色版/照片墙

---

**CD-04：磁力卡片吸附（Magnetic Card Grid）**
```javascript
// 鼠标靠近卡片时，卡片被轻微"吸引"向鼠标方向偏移
document.querySelectorAll('.mag-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const cx = r.left + r.width/2, cy = r.top + r.height/2;
    const dx = (e.clientX-cx) * 0.12, dy = (e.clientY-cy) * 0.08;
    card.style.transform = `translate(${dx}px,${dy}px) scale(1.02)`;
    // 内部内容向反方向偏移制造视差
    card.querySelector('.card-content')?.style.setProperty('transform', `translate(${-dx*0.3}px,${-dy*0.3}px)`);
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    card.querySelector('.card-content')?.style.setProperty('transform','');
  });
});
```
```css
.mag-card, .card-content { transition: transform 0.4s cubic-bezier(0.16,1,0.3,1); }
```
适用：网格布局/产品矩阵/团队成员/功能展示

---

**CD-05：毛玻璃浮层滑入（Frosted Glass Reveal）**
```css
.glass-card {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(16px) saturate(150%);
  -webkit-backdrop-filter: blur(16px) saturate(150%);
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
}
/* 悬停时玻璃变亮 + 边框加强 */
.glass-card:hover {
  background: rgba(255,255,255,0.1);
  border-color: rgba(255,255,255,0.2);
  box-shadow: 0 16px 48px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.2);
  transform: translateY(-4px);
}
/* 侧边光反射伪元素 */
.glass-card::before {
  content: '';
  position: absolute; top: 0; left: -60%;
  width: 40%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
  transform: skewX(-20deg);
  transition: left 0.6s cubic-bezier(0.16,1,0.3,1);
  pointer-events: none;
}
.glass-card:hover::before { left: 120%; }
```
适用：几乎所有暗色主题，通用性最强

---

**CD-06：展开抽屉面板（Drawer Panel）**
```javascript
// 点击触发区域，面板从底部/右侧展开，支持嵌套内容
function initDrawer(trigger, drawer) {
  let open = false;
  trigger.addEventListener('click', () => {
    open = !open;
    drawer.style.height = open ? drawer.scrollHeight + 'px' : '0';
    drawer.style.opacity = open ? '1' : '0';
    trigger.setAttribute('aria-expanded', open);
    trigger.querySelector('.drawer-icon')?.style.setProperty('transform', open ? 'rotate(180deg)' : '');
  });
}
```
```css
.drawer-panel {
  height: 0; opacity: 0; overflow: hidden;
  transition: height 0.5s cubic-bezier(0.16,1,0.3,1), opacity 0.4s;
}
.drawer-icon { transition: transform 0.3s cubic-bezier(0.16,1,0.3,1); }
```
适用：FAQ/产品详情/规格表/移动端菜单

---

### 13.4 页面过渡与切换特效（PAGE & SECTION TRANSITIONS）

**PT-01：页面遮帘入场（Curtain Wipe）**
```javascript
// 页面载入时，一个全屏色块从下往上划出，露出内容
function curtainReveal() {
  const curtain = document.getElementById('page-curtain');
  curtain.style.transform = 'translateY(0)';
  requestAnimationFrame(() => requestAnimationFrame(() => {
    curtain.style.transition = 'transform 0.9s cubic-bezier(0.16,1,0.3,1)';
    curtain.style.transform = 'translateY(-100%)';
    setTimeout(() => curtain.remove(), 1000);
  }));
}
window.addEventListener('load', curtainReveal);
```
```css
#page-curtain {
  position: fixed; inset: 0; z-index: 99999;
  background: var(--accent);
  transform: translateY(0);
}
/* 变体：斜切遮帘 */
#curtain-diagonal { clip-path: polygon(0 0,100% 0,100% 100%,0 100%); }
```
适用：任何需要仪式感入场的品牌页面

---

**PT-02：章节过渡爆炸（Section Explosion Reveal）**
```css
/* 滚动到新section时，内容从中心向四周爆炸展开 */
.section-explode {
  clip-path: circle(0% at 50% 50%);
  opacity: 0;
  transition: clip-path 0.8s cubic-bezier(0.16,1,0.3,1), opacity 0.4s;
}
.section-explode.revealed {
  clip-path: circle(150% at 50% 50%);
  opacity: 1;
}
/* 变体：从角落展开 */
.explode-corner { clip-path: circle(0% at 0% 0%); }
.explode-corner.revealed { clip-path: circle(200% at 0% 0%); }
```
适用：SPA面板切换/章节转场/高戏剧感揭示

---

**PT-03：滚动驱动进度锁定（Scroll Lock Section）**
```javascript
// 某section停留期间内容分步骤出现，完成后才继续滚动
// 适合产品功能逐条揭示（苹果风格）
let locked = false;
const lockSection = document.getElementById('scroll-lock-section');
const steps = lockSection.querySelectorAll('.lock-step');
let currentStep = 0;
const observer = new IntersectionObserver(([e]) => {
  if (e.isIntersecting && !locked) { locked = true; revealSteps(); }
}, { threshold: 0.8 });
observer.observe(lockSection);
function revealSteps() {
  if (currentStep < steps.length) {
    steps[currentStep].classList.add('visible');
    currentStep++;
    setTimeout(revealSteps, 600);
  } else { locked = false; }
}
```
```css
.lock-step { opacity:0; transform:translateY(24px); transition:opacity 0.5s,transform 0.5s; }
.lock-step.visible { opacity:1; transform:none; }
```
适用：产品功能逐步演示/故事叙述/操作流程

---

**PT-04：视差剪切面（Clip-Path Parallax）**
```javascript
// 滚动时，section边界用clip-path斜切，相邻section错位滑动
window.addEventListener('scroll', () => {
  const sy = window.scrollY;
  document.querySelectorAll('[data-clip-parallax]').forEach(el => {
    const speed = parseFloat(el.dataset.clipParallax) || 0.3;
    const offset = sy * speed;
    el.style.clipPath = `polygon(0 ${offset}px, 100% ${offset*0.6}px, 100% calc(100% - ${offset*0.4}px), 0 calc(100% - ${offset*0.7}px))`;
  });
}, { passive: true });
```
适用：创意工作室/摄影/时尚 章节分割

---

### 13.5 交互反馈特效（INTERACTION FEEDBACK）

**IF-01：按钮液态填充（Liquid Button Fill）**
```css
/* 点击后背景从点击点向外液态扩散填充 */
.btn-liquid {
  position: relative; overflow: hidden;
  isolation: isolate;
}
.btn-liquid::after {
  content: '';
  position: absolute;
  left: var(--click-x, 50%); top: var(--click-y, 50%);
  width: 0; height: 0; border-radius: 50%;
  background: var(--fill-color, rgba(255,255,255,0.3));
  transform: translate(-50%,-50%);
  transition: width 0.6s cubic-bezier(0.16,1,0.3,1), height 0.6s cubic-bezier(0.16,1,0.3,1), opacity 0.6s;
  opacity: 1; pointer-events: none; z-index: -1;
}
.btn-liquid.filling::after { width: 400px; height: 400px; opacity: 0; }
```
```javascript
document.querySelectorAll('.btn-liquid').forEach(btn => {
  btn.addEventListener('click', e => {
    const r = btn.getBoundingClientRect();
    btn.style.setProperty('--click-x', (e.clientX-r.left)+'px');
    btn.style.setProperty('--click-y', (e.clientY-r.top)+'px');
    btn.classList.remove('filling');
    requestAnimationFrame(() => requestAnimationFrame(() => btn.classList.add('filling')));
    setTimeout(() => btn.classList.remove('filling'), 650);
  });
});
```
适用：任何主CTA按钮

---

**IF-02：长按蓄力进度（Press & Hold Progress）**
```javascript
// 按住按钮时，环形/线性进度条蓄力，满后触发动作
function holdToAction(btn, duration=1500, onComplete) {
  const ring = btn.querySelector('.hold-ring');
  let timer, start;
  btn.addEventListener('mousedown', () => {
    start = Date.now();
    timer = setInterval(() => {
      const p = Math.min((Date.now()-start)/duration*100, 100);
      ring.style.background = `conic-gradient(var(--accent) ${p*3.6}deg, transparent 0)`;
      if (p >= 100) { clearInterval(timer); onComplete(); }
    }, 16);
  });
  btn.addEventListener('mouseup', () => { clearInterval(timer); ring.style.background=''; });
}
```
```css
.hold-ring {
  position: absolute; inset: -4px; border-radius: 50%;
  pointer-events: none;
  /* background由JS动态设置 */
}
```
适用：危险操作确认/游戏技能/沉浸式体验

---

**IF-03：输入框聚焦粒子（Input Focus Particles）**
```javascript
// input获得焦点时，边框上喷出小粒子
document.querySelectorAll('input, textarea').forEach(input => {
  input.addEventListener('focus', () => {
    const r = input.getBoundingClientRect();
    for (let i = 0; i < 12; i++) {
      const p = document.createElement('div');
      p.className = 'input-particle';
      const x = r.left + Math.random()*r.width;
      const y = r.top + r.height;
      p.style.cssText = `left:${x}px;top:${y}px;--dx:${(Math.random()-.5)*40}px;--dy:${-20-Math.random()*30}px`;
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 800);
    }
  });
});
```
```css
.input-particle {
  position:fixed; width:4px; height:4px; border-radius:50%;
  background:var(--accent); pointer-events:none; z-index:9999;
  animation: input-burst 0.8s ease-out forwards;
}
@keyframes input-burst {
  0%   { transform:translate(-50%,-50%) translate(0,0); opacity:1; }
  100% { transform:translate(-50%,-50%) translate(var(--dx),var(--dy)); opacity:0; }
}
```
适用：联系表单/搜索框/Newsletter订阅

---

**IF-04：悬停磁力标签（Hover Magnetic Tag）**
```javascript
// 一组标签，鼠标靠近时最近的标签被磁吸偏向鼠标方向
const tags = document.querySelectorAll('.mag-tag');
document.addEventListener('mousemove', e => {
  tags.forEach(tag => {
    const r = tag.getBoundingClientRect();
    const cx = r.left+r.width/2, cy = r.top+r.height/2;
    const dist = Math.sqrt((e.clientX-cx)**2+(e.clientY-cy)**2);
    if (dist < 80) {
      const force = (80-dist)/80;
      const dx = (e.clientX-cx)*force*0.4;
      const dy = (e.clientY-cy)*force*0.4;
      tag.style.transform = `translate(${dx}px,${dy}px) scale(${1+force*0.1})`;
    } else { tag.style.transform = ''; }
  });
});
```
```css
.mag-tag { transition: transform 0.3s cubic-bezier(0.16,1,0.3,1), background 0.2s; display:inline-block; }
```
适用：技术标签云/兴趣标签/分类过滤器

---

**IF-05：拖拽排序（Drag & Reorder）**
```javascript
// 列表/网格支持鼠标拖拽重新排序
function initDragSort(container) {
  let dragging = null;
  container.querySelectorAll('.drag-item').forEach(item => {
    item.draggable = true;
    item.addEventListener('dragstart', () => { dragging = item; item.classList.add('dragging'); });
    item.addEventListener('dragend', () => { dragging = null; item.classList.remove('dragging'); });
    item.addEventListener('dragover', e => {
      e.preventDefault();
      if (dragging && dragging !== item) {
        const r = item.getBoundingClientRect();
        const mid = r.top + r.height/2;
        item.parentNode.insertBefore(dragging, e.clientY < mid ? item : item.nextSibling);
      }
    });
  });
}
```
```css
.drag-item { cursor: grab; transition: opacity 0.2s, transform 0.2s; }
.drag-item.dragging { opacity: 0.4; transform: scale(0.95); cursor: grabbing; }
.drag-item:not(.dragging):hover { transform: translateY(-2px); }
```
适用：看板/优先级排序/个性化设置/游戏道具

---

**IF-06：悬停聚光灯（Spotlight Follow）**
```javascript
// 鼠标在section内移动，聚光灯圆形高亮区域跟随
document.querySelectorAll('.spotlight-zone').forEach(zone => {
  zone.addEventListener('mousemove', e => {
    const r = zone.getBoundingClientRect();
    zone.style.setProperty('--sx', (e.clientX-r.left)+'px');
    zone.style.setProperty('--sy', (e.clientY-r.top)+'px');
  });
});
```
```css
.spotlight-zone {
  position: relative; overflow: hidden;
}
.spotlight-zone::before {
  content: '';
  position: absolute;
  width: 400px; height: 400px; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
  left: var(--sx, -200px); top: var(--sy, -200px);
  transform: translate(-50%,-50%);
  pointer-events: none; transition: left 0.1s, top 0.1s;
}
```
适用：暗色主题卡片区/定价表/功能列表

---

**IF-07：倒计时/实时Ticker（Live Data Ticker）**
```javascript
// 数字实时跳动，模拟股票/用户数/收益实时更新
function initTicker(el, baseVal, variance=5, interval=2000) {
  const fmt = n => n.toLocaleString();
  setInterval(() => {
    const delta = Math.floor((Math.random()-.3) * variance);
    baseVal += delta;
    const old = el.textContent;
    el.style.animation = 'none';
    requestAnimationFrame(() => {
      el.style.animation = 'tick-flip 0.3s ease';
      el.textContent = fmt(baseVal);
    });
    // 颜色反馈
    el.style.color = delta >= 0 ? 'var(--green, #00ff88)' : 'var(--red, #ff4444)';
    setTimeout(() => el.style.color = '', 500);
  }, interval);
}
```
```css
@keyframes tick-flip {
  0%   { transform: translateY(-8px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
```
适用：SaaS数据面板/电商销量/社区活跃度

---

### 13.6 视觉叙事特效（VISUAL STORYTELLING）

**VS-01：图片视差分层（Image Layer Parallax）**
```javascript
// 一张图片被分为前景/中景/背景，鼠标移动时各层按不同速率移动
document.querySelectorAll('.parallax-scene').forEach(scene => {
  scene.addEventListener('mousemove', e => {
    const r = scene.getBoundingClientRect();
    const x = (e.clientX-r.left)/r.width - 0.5;
    const y = (e.clientY-r.top)/r.height - 0.5;
    scene.querySelectorAll('[data-layer]').forEach(layer => {
      const depth = parseFloat(layer.dataset.layer);
      layer.style.transform = `translate(${x*depth*30}px, ${y*depth*20}px)`;
    });
  });
  scene.addEventListener('mouseleave', () => {
    scene.querySelectorAll('[data-layer]').forEach(l => l.style.transform = '');
  });
});
```
```css
[data-layer] { transition: transform 0.6s cubic-bezier(0.16,1,0.3,1); will-change: transform; }
```
适用：英雄配图/产品展示/旅游目的地/游戏场景

---

**VS-02：进度揭示蒙版（Reveal Mask Wipe）**
```css
/* 图片从左到右被"擦出"，类似视频划像效果 */
.mask-reveal {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 1.2s cubic-bezier(0.16,1,0.3,1);
}
.mask-reveal.revealed { clip-path: inset(0 0% 0 0); }
/* 变体：对角线划出 */
.mask-diagonal { clip-path: polygon(0 0, 0 0, 0 100%, 0 100%); }
.mask-diagonal.revealed { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
/* 变体：圆形扩散 */
.mask-circle { clip-path: circle(0% at 50% 50%); }
.mask-circle.revealed { clip-path: circle(75% at 50% 50%); }
```
适用：图片画廊/产品展示图/章节图片/横幅

---

**VS-03：时间线步进（Timeline Step Reveal）**
```javascript
// 横向或纵向时间线，滚动到视口时按顺序步进揭示每个节点
const timelineItems = document.querySelectorAll('.timeline-item');
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const idx = [...timelineItems].indexOf(e.target);
      setTimeout(() => {
        e.target.classList.add('tl-visible');
        // 连接线从上一节点延伸到当前节点
        e.target.querySelector('.tl-line')?.style.setProperty('transform', 'scaleY(1)');
      }, idx * 150);
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });
timelineItems.forEach(item => io.observe(item));
```
```css
.timeline-item { opacity:0; transform:translateX(-20px); transition:opacity 0.6s,transform 0.6s; }
.timeline-item.tl-visible { opacity:1; transform:none; }
.tl-line { transform:scaleY(0); transform-origin:top; transition:transform 0.4s ease; }
```
适用：公司历史/产品迭代/工作流程/路线图

---

**VS-04：数字仪表盘（Gauge / Speedometer）**
```javascript
// SVG圆弧进度条，支持动画fill + 指针旋转
function animateGauge(el, value, max=100) {
  const circle = el.querySelector('.gauge-fill');
  const radius = 54; const circumference = 2*Math.PI*radius * 0.75; // 270度弧
  const offset = circumference * (1 - value/max);
  circle.style.strokeDasharray = circumference;
  circle.style.strokeDashoffset = circumference;
  setTimeout(() => { circle.style.transition = 'stroke-dashoffset 1.5s cubic-bezier(0.16,1,0.3,1)'; circle.style.strokeDashoffset = offset; }, 200);
  // 数字计数
  const num = el.querySelector('.gauge-num');
  let n = 0; const inc = value/60;
  const t = setInterval(() => { n=Math.min(n+inc,value); num.textContent=Math.round(n); if(n>=value)clearInterval(t); }, 25);
}
```
```html
<svg class="gauge" viewBox="0 0 120 120">
  <circle class="gauge-track" cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="8" stroke-linecap="round" stroke-dasharray="254 340" transform="rotate(135 60 60)"/>
  <circle class="gauge-fill" cx="60" cy="60" r="54" fill="none" stroke="var(--accent)" stroke-width="8" stroke-linecap="round" transform="rotate(135 60 60)"/>
  <text class="gauge-num" x="60" y="65" text-anchor="middle" font-size="22" fill="var(--accent)">0</text>
</svg>
```
适用：技能/性能/评分/兼容度 数据展示

---

**VS-05：交互式图表（Interactive Bar/Area Chart）**
```javascript
// 纯Canvas折线/柱状图，hover高亮数据点并显示tooltip
function drawBarChart(canvas, data, opts={}) {
  const ctx = canvas.getContext('2d');
  const W=canvas.width=canvas.offsetWidth, H=canvas.height=canvas.offsetHeight;
  const max=Math.max(...data.map(d=>d.val));
  const barW=(W-60)/(data.length*1.5);
  data.forEach((d,i)=>{
    const x=40+i*(W-60)/data.length, h=(d.val/max)*(H-60);
    // 动画：高度从0到h
    let anim=0;
    const grow=()=>{ anim=Math.min(anim+h/20,h); ctx.clearRect(x-2,0,barW+4,H); ctx.fillStyle=`hsla(${180+i*15},80%,60%,0.8)`; ctx.fillRect(x,H-40-anim,barW,anim); if(anim<h)requestAnimationFrame(grow); };
    setTimeout(grow, i*80);
  });
  // hover tooltip
  canvas.addEventListener('mousemove', e => {
    const r=canvas.getBoundingClientRect(), mx=e.clientX-r.left;
    data.forEach((d,i)=>{ const x=40+i*(W-60)/data.length; if(mx>x&&mx<x+barW) console.log(d.label,d.val); });
  });
}
```
适用：数据仪表板/统计页面/SaaS分析/运营报告

---

### 13.7 特效速查表

| 代号 | 类型 | 名称 | 适用气质 |
|------|------|------|---------|
| TX-01 | 文字 | 粒子解体重组 | Hero/品牌揭示 |
| TX-02 | 文字 | 数字乱码Scramble | 科技/数据 |
| TX-03 | 文字 | 液态文字变形 | 有机/wellness |
| TX-04 | 文字 | 打字机逐字揭示 | 终端/SaaS |
| TX-05 | 文字 | SVG描边填充 | 品牌标题 |
| TX-06 | 文字 | 跑马灯轨道 | 合作品牌/标签 |
| TX-07 | 文字 | 视差分层 | Hero沉浸感 |
| TX-08 | 文字 | 字符随机跳动 | 游戏/玩具 |
| BG-01 | 背景 | 颗粒噪点叠层 | 高端品牌通用 |
| BG-02 | 背景 | 极光渐变blob | wellness/AI |
| BG-03 | 背景 | 网格扫描线 | 赛博/科技 |
| BG-04 | 背景 | 流动渐变网格 | AI/创意 |
| BG-05 | 背景 | 粒子连线网络 | 科技/AI |
| BG-06 | 背景 | 星空视差滚动 | 宇宙/VR |
| BG-07 | 背景 | 数字雨 | 黑客/赛博 |
| BG-08 | 背景 | 有机流动Blob | wellness/有机 |
| CD-01 | 卡片 | 全息镭射折射 | NFT/游戏卡牌 |
| CD-02 | 卡片 | 3D翻转揭示 | 产品/人物/FAQ |
| CD-03 | 卡片 | 堆叠展开扇形 | 画廊/作品集 |
| CD-04 | 卡片 | 磁力吸附 | 网格/产品矩阵 |
| CD-05 | 卡片 | 毛玻璃浮层 | 暗色主题通用 |
| CD-06 | 卡片 | 展开抽屉面板 | FAQ/详情/规格 |
| PT-01 | 过渡 | 页面遮帘入场 | 品牌仪式感 |
| PT-02 | 过渡 | 章节爆炸展开 | SPA/高对比度 |
| PT-03 | 过渡 | 滚动锁定步进 | 产品演示/叙事 |
| PT-04 | 过渡 | 视差剪切面 | 创意/摄影 |
| IF-01 | 交互 | 液态填充按钮 | 任意CTA |
| IF-02 | 交互 | 长按蓄力进度 | 游戏/危险操作 |
| IF-03 | 交互 | 输入框粒子 | 表单/搜索 |
| IF-04 | 交互 | 磁力标签云 | 标签/分类 |
| IF-05 | 交互 | 拖拽排序 | 看板/设置 |
| IF-06 | 交互 | 聚光灯跟随 | 暗色卡片区 |
| IF-07 | 交互 | 实时Ticker | SaaS/数据 |
| VS-01 | 叙事 | 图片多层视差 | 英雄图/产品 |
| VS-02 | 叙事 | 进度揭示蒙版 | 图片/画廊 |
| VS-03 | 叙事 | 时间线步进 | 历史/路线图 |
| VS-04 | 叙事 | SVG仪表盘 | 评分/性能/技能 |
| VS-05 | 叙事 | 交互式图表 | 数据/分析 |

> **使用原则**：每条在确认卡的 `特效选用` 字段声明代号（如 `BG-02 + CD-01 + IF-06 + TX-05`）。同气质优先搭配（科技类→BG-03/BG-05/TX-02；奢侈品→BG-01/CD-05/TX-03；游戏→BG-07/CD-01/IF-02）。所有Canvas特效均有`window resize`事件重置画布尺寸，不引发横向滚动。
