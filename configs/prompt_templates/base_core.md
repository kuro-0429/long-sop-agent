# 技术约束与质量底线 — 核心篇（一~七）

> 本文件包含 §一~§七 的硬约束。拆分后的其他文件：
> - `base_animation.md` — §八 动画系统 + §九 排版艺术
> - `base_components.md` — §十 BTN造型 + §十一 CUR/EFF光标 + §十二 Features替代
> - `base_fx_library.md` — §十三 动画特效扩展库
> - `visual_continuity.md` — Section间色彩过渡规范（新）

---

## 一、文件交付约束（100%强制）

- 输出严格为单一 `index.html`，CSS 和 JS 全部内联
- 禁止任何 JS 框架（jQuery / React / Vue / Alpine 等）
- 禁止外部 CSS 文件（Google Fonts CDN 除外）
- 图片只使用 `https://images.unsplash.com/` URL
- **同一页面内所有图片URL必须唯一，禁止同一张图片在不同section重复使用**（如Collection和Limited不得共用同一张手表图）
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
- section 之间不得无任何视觉过渡（细线 / 渐变 / 色块均可）；**单页滚动页面必须遵守 `visual_continuity.md` 的色彩过渡规范**
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

