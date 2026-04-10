# 技术约束 — 组件造型库篇（十~十二）

> 从 `base.md` 拆分。包含 BTN按钮造型(A-L) / CUR光标变体(A-AH,X) / EFF光标特效(1-20) / CARD卡片形状(A-G) / Features替代(F-00~F-10)。
> 核心约束见 `base_core.md`，动画规范见 `base_animation.md`。

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
