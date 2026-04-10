# 技术约束 — 动画系统与排版艺术篇（八~九）

> 从 `base.md` 拆分。核心约束见 `base_core.md`，组件库见 `base_components.md`。

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

