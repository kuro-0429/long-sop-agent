# 可复现技法库（T-01 ~ T-80）

> 从 `generator.md` 拆分。选技法时读取此文件。
> 生成流程见 `generator_flow.md`，W码/P码/架构见 `generator_wildcards.md`。

---

### 【T-01】文字遮罩揭示（Text Clip Reveal）
**来源参考**：Lusion v3、众多 Awwwards SOTD agency 页面
**效果**：标题文字从被遮罩的状态（clip-path 或 overflow:hidden + translateY）滚动进入视口时"撕裂"揭示
**CSS/JS 实现**：
```
/* 每行文字包裹在 .line-wrap(overflow:hidden) 内 */
.line-inner { transform: translateY(105%); transition: transform 0.9s cubic-bezier(0.16,1,0.3,1); }
.revealed .line-inner { transform: translateY(0); }
/* JS：IntersectionObserver 触发 .revealed，每行 stagger 80-120ms */
```
**适用类型**：创意机构、奢侈品、游戏、艺术项目

---

### 【T-02】文字扰码效果（Text Scramble on Hover）
**来源参考**：Cuberto、众多 Godly 精选作品
**效果**：hover 或页面加载时，文字字母随机乱码后"解码"还原为正确文字
**JS 实现**：
```javascript
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%';
function scramble(el) {
  let iter = 0;
  const original = el.dataset.value;
  const interval = setInterval(() => {
    el.textContent = original.split('').map((c, i) =>
      i < iter ? original[i] : chars[Math.floor(Math.random() * chars.length)]
    ).join('');
    if (iter >= original.length) clearInterval(interval);
    iter += 1/3;
  }, 30);
}
```
**适用类型**：AI工具、开发者工具、科技品牌、游戏

---

### 【T-03】磁性按钮（Magnetic Button）
**来源参考**：Locomotive、Cuberto、Olivier Larose 教程
**效果**：鼠标靠近按钮时，按钮被"吸引"向鼠标偏移，移开时弹回
**JS 实现**：
```javascript
btn.addEventListener('mousemove', (e) => {
  const rect = btn.getBoundingClientRect();
  const x = e.clientX - rect.left - rect.width/2;
  const y = e.clientY - rect.top - rect.height/2;
  btn.style.transform = `translate(${x * 0.35}px, ${y * 0.35}px)`;
});
btn.addEventListener('mouseleave', () => {
  btn.style.transform = 'translate(0,0)';
  btn.style.transition = 'transform 0.5s cubic-bezier(0.16,1,0.3,1)';
});
```
**适用类型**：创意机构、品牌电商、SaaS CTA 区域

---

### 【T-04】水平固定滚动区（Horizontal Pinned Section）
**来源参考**：大量 Awwwards SOTD、Olivier Larose 教程
**效果**：垂直滚动时，某个 section 固定在屏幕，内部元素水平平移，制造"横向旅程"感
**JS 实现**：
```javascript
const section = document.querySelector('.h-scroll');
const inner = section.querySelector('.h-inner');
window.addEventListener('scroll', () => {
  const rect = section.getBoundingClientRect();
  if (rect.top <= 0 && rect.bottom >= window.innerHeight) {
    const progress = Math.abs(rect.top) / (rect.height - window.innerHeight);
    const maxShift = inner.scrollWidth - window.innerWidth;
    inner.style.transform = `translateX(${-progress * maxShift}px)`;
  }
});
/* section height 设为 300vh，position:sticky top:0 */
```
**适用类型**：作品集、时间线、产品对比、旅游体验

---

### 【T-05】SVG 路径描边动画（SVG Stroke Draw on Scroll）
**来源参考**：Lusion、众多 Awwwards 获奖作品
**效果**：SVG 线条/图形随滚动进度逐渐"被绘制出来"
**CSS/JS 实现**：
```javascript
// 计算总路径长度
const path = document.querySelector('.draw-path');
const length = path.getTotalLength();
path.style.strokeDasharray = length;
path.style.strokeDashoffset = length;
window.addEventListener('scroll', () => {
  const progress = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  path.style.strokeDashoffset = length * (1 - progress);
});
```
**适用类型**：品牌叙事、硬件产品、流程展示、时间线

---

### 【T-06】视差图层分离（Multi-layer Parallax）
**来源参考**：大量 Godly 精选、Awwwards 评委高分作品
**效果**：Hero 区域分为 3-4 层，滚动时各层以不同速率移动，产生真实景深
**JS 实现**：
```javascript
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  document.querySelector('.layer-bg').style.transform = `translateY(${y * 0.1}px)`;
  document.querySelector('.layer-mid').style.transform = `translateY(${y * 0.25}px)`;
  document.querySelector('.layer-fg').style.transform = `translateY(${y * 0.5}px)`;
  document.querySelector('.layer-text').style.transform = `translateY(${y * 0.15}px)`;
});
```
**适用类型**：游戏、自然/环保品牌、旅游、奢侈品、叙事型页面

---

### 【T-07】光标跟随自定义光标（Custom Cursor with Blend Mode）
**来源参考**：Cuberto、Locomotive、众多 Godly 收录作品
**效果**：替换浏览器默认光标为自定义图形，悬停特定元素时光标变形/扩大/反色
**CSS/JS 实现**：
```javascript
const cursor = document.createElement('div');
cursor.className = 'cursor';
document.body.appendChild(cursor);
document.addEventListener('mousemove', e => {
  cursor.style.left = e.clientX + 'px';
  cursor.style.top = e.clientY + 'px';
});
// Hover 状态：添加 .cursor-expand 类
document.querySelectorAll('a, button').forEach(el => {
  el.addEventListener('mouseenter', () => cursor.classList.add('expand'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('expand'));
});
/* CSS: cursor { mix-blend-mode: difference; } 实现反色效果 */
```
**适用类型**：创意机构、奢侈品、游戏、艺术项目

---

### 【T-08】图片悬停视差偏移（Image Hover Parallax Shift）
**来源参考**：Awwwards agency portfolios、Olivier Larose 教程
**效果**：鼠标在图片容器内移动时，图片内容随鼠标位置轻微偏移，产生3D倾斜感
**JS 实现**：
```javascript
cards.forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;   // -0.5 to 0.5
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    const img = card.querySelector('img');
    img.style.transform = `scale(1.08) translate(${x * 20}px, ${y * 20}px)`;
    card.style.transform = `perspective(800px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg)`;
  });
  card.addEventListener('mouseleave', () => {
    card.querySelector('img').style.transform = 'scale(1) translate(0,0)';
    card.style.transform = 'perspective(800px) rotateY(0) rotateX(0)';
  });
});
```
**适用类型**：作品集、电商、游戏、旅游

---

### 【T-09】渐变噪点纹理背景（Grainy Gradient）
**来源参考**：大量 Godly 精选、2024-2025 最流行的背景处理手法
**效果**：在渐变背景上叠加 SVG 噪点滤镜，产生胶片/有机质感，消除数字感
**CSS 实现**：
```css
.grainy-bg::after {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
}
```
**适用类型**：wellness、咖啡/食品、设计机构、奢侈品、生活方式品牌

---

### 【T-10】折叠展开卡片（Accordion / Expandable Cards）
**来源参考**：大量 Land-book 高分 SaaS 页面
**效果**：FAQ 或功能列表以折叠卡片形式呈现，点击展开，高度从0平滑过渡，内容渐显
**CSS/JS 实现**：
```javascript
items.forEach(item => {
  const header = item.querySelector('.acc-header');
  const body = item.querySelector('.acc-body');
  header.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    items.forEach(i => { i.classList.remove('open'); i.querySelector('.acc-body').style.maxHeight = 0; });
    if (!isOpen) { item.classList.add('open'); body.style.maxHeight = body.scrollHeight + 'px'; }
  });
});
/* CSS: .acc-body { max-height: 0; overflow: hidden; transition: max-height 0.5s ease; } */
```
**适用类型**：SaaS、企业官网、文档工具、定价页

---

### 【T-11】滚动驱动数字/文字变色（Scroll-driven Opacity Gradient on Text）
**来源参考**：Awwwards SOTD 2023-2024 多个叙事型页面、Olivier Larose 教程
**效果**：长段文字中，已滚动过的部分高亮（不透明），未到达的部分半透明，随滚动实时更新
**JS 实现**：
```javascript
const words = para.querySelectorAll('.word');
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    e.target.style.opacity = e.isIntersecting ? '1' : '0.2';
  });
}, { threshold: 0.5, rootMargin: '0px 0px -30% 0px' });
words.forEach(w => obs.observe(w));
```
**适用类型**：叙事型品牌、Manifesto 页面、创意机构、AI/哲学类产品

---

### 【T-12】Sticky 卡片叠层（Stacking Cards on Scroll）
**来源参考**：众多 Awwwards 创意机构网站
**效果**：多张卡片依次 sticky 定位，后一张滚入时叠在前一张上方，形成牌堆叠加效果
**CSS 实现**：
```css
.card { position: sticky; top: 80px; }
.card:nth-child(1) { top: 80px; }
.card:nth-child(2) { top: 96px; }
.card:nth-child(3) { top: 112px; }
/* 每张卡片 margin-bottom 足够大，触发 sticky 滚动 */
```
**适用类型**：流程展示、功能对比、时间线、步骤引导

---

### 【T-13】模糊/虚化过渡区（Section Blur Transition）
**来源参考**：Apple 风格、大量 Godly 精选
**效果**：两个 section 之间不是硬切，而是上一区块边缘逐渐 blur + fade，下一区块从清晰中浮现
**CSS 实现**：
```css
.section-end {
  mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
}
```
**适用类型**：所有类型均适用，尤其是 dark mode 页面

---

### 【T-14】倾斜分割线（Diagonal Section Divider）
**来源参考**：Awwwards 众多品牌落地页
**效果**：section 之间用 CSS clip-path 制造斜角分割，打破横向水平切割的单调感
**CSS 实现**：
```css
.section-diagonal {
  clip-path: polygon(0 0, 100% 4vw, 100% 100%, 0 100%);
  margin-top: -4vw;
}
/* 或用 ::before 伪元素 */
```
**适用类型**：电商、旅游、游戏、健身、品牌活动

---

### 【T-15】Ticker 式文字滚动标注（Live Data Ticker）
**来源参考**：金融/数据类 Awwwards 作品、Screenlane 精选
**效果**：类似股票行情 ticker，实时（或模拟）滚动展示数字/指标/状态，配合微小绿/红变化动效
**JS 实现**：
```javascript
function updateTicker() {
  items.forEach(item => {
    const val = parseFloat(item.dataset.base) + (Math.random() - 0.5) * 0.1;
    const change = val > parseFloat(item.dataset.prev) ? 'up' : 'down';
    item.className = 'ticker-item ' + change;
    item.querySelector('.val').textContent = val.toFixed(2);
    item.dataset.prev = val;
  });
}
setInterval(updateTicker, 2000);
```
**适用类型**：金融工具、数据平台、加密货币、AI监控产品

---

### 【T-16】图片拖尾跟随（Image Trail on Mouse Move）
**来源参考**：VLNC Studio（Awwwards SOTD）、Codrops Image Trail Effects、Cuberto 等 Godly 精选机构站
**效果**：鼠标在指定区域移动时，沿轨迹依次浮现一系列图片缩略图并自动淡出消失，形成视觉拖尾
**JS 实现（纯 Vanilla）**：
```javascript
const images = [...document.querySelectorAll('.trail-img')];
let index = 0, lastX = 0, lastY = 0;
document.addEventListener('mousemove', e => {
  const dist = Math.hypot(e.clientX - lastX, e.clientY - lastY);
  if (dist < 60) return;            // 每移动60px触发一张
  lastX = e.clientX; lastY = e.clientY;
  const img = images[index % images.length];
  img.style.left = e.clientX + 'px';
  img.style.top  = e.clientY + 'px';
  img.style.opacity = '1';
  img.style.transform = 'translate(-50%,-50%) scale(1)';
  setTimeout(() => {
    img.style.opacity = '0';
    img.style.transform = 'translate(-50%,-50%) scale(0.7)';
  }, 600);
  index++;
});
/* CSS: .trail-img { position:fixed; pointer-events:none; width:160px; aspect-ratio:3/4;
   object-fit:cover; opacity:0; transition: opacity 0.4s, transform 0.6s cubic-bezier(0.16,1,0.3,1); } */
```
**适用类型**：创意机构作品集、时尚品牌、摄影师、游戏/娱乐、艺术项目

---

### 【T-17】镜头聚光灯揭示（Spotlight Cursor Reveal）
**来源参考**：Awwwards SOTD 多个沉浸式页面、CodePen Spotlight Cursor by Caroline Artz
**效果**：页面背景被暗色遮罩覆盖，只有鼠标位置的圆形区域（radial-gradient）照亮内容，像手电筒扫过黑暗
**CSS/JS 实现**：
```javascript
const overlay = document.querySelector('.spotlight-overlay');
document.addEventListener('mousemove', e => {
  overlay.style.background =
    `radial-gradient(circle 200px at ${e.clientX}px ${e.clientY}px,
     transparent 0%, rgba(0,0,0,0.92) 100%)`;
});
/* CSS: .spotlight-overlay { position:fixed; inset:0; pointer-events:none; z-index:10;
   background: rgba(0,0,0,0.92); transition: background 0.05s; } */
```
**适用类型**：密室/解谜游戏、恐怖/悬疑品牌、创意机构 Hero 区、极简暗黑美学

---

### 【T-18】可变字重波浪（Variable Font Weight Wave）
**来源参考**：Awwwards "Variable font hover interaction" / "Variable font weight on scroll" (Krew)、Godly typography-focused 精选
**效果**：使用 Google Variable Font（如 Inter/Roboto Flex），字母的 `font-variation-settings` 随鼠标X位置或滚动进度动态变化，thin→black 产生呼吸/波浪感
**CSS/JS 实现**：
```javascript
// 鼠标临近字符时，该字符字重变重，邻近字符次之（近似高斯衰减）
const chars = [...el.querySelectorAll('.char')];
el.addEventListener('mousemove', e => {
  const rect = el.getBoundingClientRect();
  const relX = (e.clientX - rect.left) / rect.width;  // 0→1
  chars.forEach((c, i) => {
    const pos = i / chars.length;
    const dist = Math.abs(relX - pos);
    const weight = 100 + Math.round(Math.max(0, 1 - dist * 6) * 700);
    c.style.fontVariationSettings = `'wght' ${weight}`;
  });
});
el.addEventListener('mouseleave', () => {
  chars.forEach(c => c.style.fontVariationSettings = `'wght' 100`);
});
/* 字体：Inter Variable / Roboto Flex / Plus Jakarta Sans (Google Fonts variable) */
/* CSS: .char { display:inline-block; transition: font-variation-settings 0.3s ease; } */
```
**适用类型**：设计机构、排版工具、字体/字体设计品牌、创意 SaaS、现代 Web3 项目

---

### 【T-19】方向感知悬停（Direction-Aware Hover）
**来源参考**：Codrops / CSS-Tricks Direction-Aware Hover Effects、众多 Awwwards agency 网站
**效果**：鼠标从哪个方向进入卡片，背景/遮罩就从该方向滑入；从哪个方向离开，就从该方向退出
**JS 实现**：
```javascript
function getDirection(e, el) {
  const { width, height, left, top } = el.getBoundingClientRect();
  const x = (e.clientX - left - width/2)  * (width  > height ? height/width  : 1);
  const y = (e.clientY - top  - height/2) * (height > width  ? width/height  : 1);
  return Math.round((Math.atan2(y, x) * (180/Math.PI) + 180) / 90 + 3) % 4;
  // 0=top 1=right 2=bottom 3=left
}
const dirMap = ['top','right','bottom','left'];
cards.forEach(card => {
  const overlay = card.querySelector('.dir-overlay');
  card.addEventListener('mouseenter', e => {
    const dir = dirMap[getDirection(e, card)];
    overlay.style.transform = startTransforms[dir];
    requestAnimationFrame(() => { overlay.style.transition='none'; requestAnimationFrame(()=>{
      overlay.style.transition='transform 0.4s cubic-bezier(0.16,1,0.3,1)';
      overlay.style.transform = 'translate(0,0)';
    });});
  });
  card.addEventListener('mouseleave', e => {
    const dir = dirMap[getDirection(e, card)];
    overlay.style.transform = startTransforms[dir];
  });
});
const startTransforms = { top:'translateY(-100%)', right:'translateX(100%)', bottom:'translateY(100%)', left:'translateX(-100%)' };
```
**适用类型**：作品集项目展示、服务卡片、电商产品网格、游戏角色选择

---

### 【T-20】SVG 粘性/果冻菜单（Gooey SVG Filter Menu）
**来源参考**：Codrops Gooey Menu、Godly 精选 navigation experiments
**效果**：菜单项 hover 时背景形状像果冻/液体一样拉伸变形，使用 SVG `feGaussianBlur` + `feColorMatrix` 实现粘连效果
**CSS/JS 实现**：
```html
<svg style="position:absolute;width:0;height:0">
  <filter id="gooey">
    <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur"/>
    <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 20 -8" result="goo"/>
    <feComposite in="SourceGraphic" in2="goo" operator="atop"/>
  </filter>
</svg>
/* CSS: .nav-gooey { filter: url(#gooey); }
   .nav-item-bg { position:absolute; width:100%; height:100%;
     background: var(--accent); border-radius:50px;
     transform: scaleX(0); transition: transform 0.4s cubic-bezier(0.34,1.56,0.64,1); }
   .nav-item:hover .nav-item-bg { transform: scaleX(1); } */
```
**适用类型**：创意机构导航、游戏 UI、活泼品牌（wellness/儿童/食品）、个人作品集

---

### 【T-21】Canvas 粒子/点阵背景（Canvas Particle / Dot Grid Background）
**来源参考**：Awwwards SOTD 科技类页面、GSAP InertiaPlugin Dot Grid Demo（Codrops 2025）、freefrontend Canvas 背景合集
**效果**：Canvas 绘制等距点阵或粒子群；鼠标靠近时点被排斥/吸引/发光，移开后弹回原位
**JS 实现**：
```javascript
const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
const dots = []; const COLS = 40, ROWS = 25;
for (let i = 0; i < COLS; i++) for (let j = 0; j < ROWS; j++) {
  dots.push({ ox: i*(canvas.width/COLS), oy: j*(canvas.height/ROWS), x:0, y:0, vx:0, vy:0 });
}
dots.forEach(d => { d.x = d.ox; d.y = d.oy; });
let mx = -999, my = -999;
canvas.addEventListener('mousemove', e => { const r=canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; });
function tick() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  dots.forEach(d => {
    const dx=d.x-mx, dy=d.y-my, dist=Math.sqrt(dx*dx+dy*dy), force=Math.max(0,80-dist)/80;
    d.vx += force * (dx/dist||0) * 3;
    d.vy += force * (dy/dist||0) * 3;
    d.vx += (d.ox-d.x)*0.06;  // spring back
    d.vy += (d.oy-d.y)*0.06;
    d.vx *= 0.82; d.vy *= 0.82;
    d.x += d.vx; d.y += d.vy;
    const alpha = 0.15 + force * 0.85;
    ctx.beginPath(); ctx.arc(d.x, d.y, 2, 0, Math.PI*2);
    ctx.fillStyle = `rgba(var(--accent-rgb), ${alpha})`; ctx.fill();
  });
  requestAnimationFrame(tick);
}
tick();
```
**适用类型**：AI/科技工具、开发者工具、数据平台、NFT/Web3、游戏

---

### 【T-22】页面预加载器（Branded Preloader）
**来源参考**：Awwwards SOTD 几乎所有顶级机构站（Locomotive、Resn 等）、Codrops Preloader 精选
**效果**：页面加载时显示全屏品牌预加载动画：数字从0%递增到100%，logo 渐显，完成后遮罩向上/分裂退场露出页面
**JS/CSS 实现**：
```javascript
const counter = document.querySelector('.preload-num');
const overlay = document.querySelector('.preload-overlay');
let count = 0;
const interval = setInterval(() => {
  count += Math.floor(Math.random() * 8) + 1;
  if (count >= 100) { count = 100; clearInterval(interval);
    setTimeout(() => {
      overlay.classList.add('exit'); // CSS: translateY(-100%) 1s cubic-bezier(0.76,0,0.24,1)
      document.body.classList.remove('loading');
    }, 400);
  }
  counter.textContent = count + '%';
}, 40);
/* CSS: body.loading { overflow:hidden; }
   .preload-overlay { position:fixed; inset:0; z-index:9999; background:var(--bg);
     display:flex; align-items:center; justify-content:center; transition:transform 1s cubic-bezier(0.76,0,0.24,1); }
   .preload-overlay.exit { transform: translateY(-100%); } */
```
**适用类型**：创意机构、游戏、奢侈品、作品集——任何想要制造"登场仪式感"的品牌

---

### 【T-23】旋转文字标签（Circular / Rotating Text Badge）
**来源参考**：Awwwards / Godly 精选中大量出现的装饰性旋转文字圆圈
**效果**：圆形排列的文字（SVG textPath 或 CSS transform）持续缓慢旋转，作为装饰性徽章或CTA辅助元素
**CSS/SVG 实现**：
```html
<svg viewBox="0 0 200 200" class="rotate-badge">
  <defs><path id="circle-path" d="M 100,100 m -80,0 a 80,80 0 1,1 160,0 a 80,80 0 1,1 -160,0"/></defs>
  <text font-size="11" fill="currentColor" letter-spacing="3">
    <textPath href="#circle-path">SCROLL DOWN ✦ EXPLORE MORE ✦ </textPath>
  </text>
</svg>
/* CSS: .rotate-badge { animation: spin 12s linear infinite; width:120px; height:120px; }
   @keyframes spin { to { transform: rotate(360deg); } } */
```
**适用类型**：创意机构、奢侈品、游戏、艺术项目——尤其适合作为 Hero 区装饰 CTA

---

### 【T-24】错列列滚动（Offset Column Scroll / Scattered Grid）
**来源参考**：Awwwards SOTD 作品集类网站、Codrops "scroll effect where each column moves at different speed"
**效果**：图片/卡片网格的不同列以不同速度滚动（奇数列向下、偶数列向上），形成"散落"立体感
**JS 实现**：
```javascript
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  document.querySelectorAll('.col-odd').forEach(c => {
    c.style.transform = `translateY(${-y * 0.12}px)`;
  });
  document.querySelectorAll('.col-even').forEach(c => {
    c.style.transform = `translateY(${y * 0.12}px)`;
  });
});
/* CSS 初始：.col-even { margin-top: 80px; } 制造初始错位 */
```
**适用类型**：摄影作品集、时尚/服装、艺术、旅游、NFT 画廊

---

### 【T-25】文字逐词/逐字母入场（Per-Character Stagger Reveal）
**来源参考**：FUTURE THREE® 案例研究（Codrops 2025）、GSAP SplitText 官方示例、大量 Awwwards 机构站
**效果**：标题拆分成单独 `<span>` 字符，每个字符附 CSS 变量 `--char` 控制 transition-delay，实现左→右精确错开入场
**CSS/JS 实现**：
```javascript
// 拆分字符并注入 CSS 变量（无需 GSAP SplitText）
function splitChars(el) {
  const text = el.textContent;
  el.innerHTML = text.split('').map((c, i) =>
    `<span style="--char:${i+1}; display:inline-block">${c === ' ' ? '&nbsp;' : c}</span>`
  ).join('');
}
/* CSS: 父元素 overflow:hidden
   .split-el span { transform: translateY(110%); opacity:0;
     transition: transform 0.6s calc(var(--char)*0.024s) cubic-bezier(0.16,1,0.3,1),
                 opacity 0.4s calc(var(--char)*0.024s) ease; }
   .split-el.revealed span { transform: translateY(0); opacity:1; } */
```
**适用类型**：创意机构 Hero、品牌宣言、游戏标题、奢侈品——任何需要"字幕入场"仪式感的场景

---

### 【T-26】clip-path 形状变换过渡（Clip-Path Morph Transition）
**来源参考**：Codrops Clip-Path 系列教程、Awwwards 页面过渡实验
**效果**：Section 背景或图片使用 clip-path polygon 定义不规则形状，hover 或滚动时形状平滑变形
**CSS 实现**：
```css
.shape-card {
  clip-path: polygon(0 0, 100% 5%, 95% 100%, 5% 95%);
  transition: clip-path 0.6s cubic-bezier(0.34,1.56,0.64,1);
}
.shape-card:hover {
  clip-path: polygon(5% 5%, 95% 0, 100% 95%, 0 100%);
}
/* 更戏剧化版本：圆形 → 矩形 */
.reveal-circle { clip-path: circle(0% at 50% 50%); transition: clip-path 1s cubic-bezier(0.16,1,0.3,1); }
.reveal-circle.active { clip-path: circle(150% at 50% 50%); }
```
**适用类型**：品牌 Hero 图片、页面过渡遮罩、游戏角色卡片、艺术项目

---

### 【T-27】无限自动滚动画廊（Infinite Auto-scroll Gallery）
**来源参考**：Codrops "Getting Creative with Infinite Loop Scrolling" (Bureau DAM)、大量 Godly 精选落地页
**效果**：一排图片/logo/卡片水平无缝循环滚动，鼠标 hover 时暂停，支持双向 + 速度渐变
**CSS/JS 实现**：
```css
.gallery-track { display:flex; gap:20px; animation: slide 20s linear infinite; width: max-content; }
.gallery-track:hover { animation-play-state: paused; }
@keyframes slide { to { transform: translateX(-50%); } }
/* HTML: 内容复制一遍，总宽度x2，动画移动-50%实现无缝 */
```
**适用类型**：Logo墙、产品图展示、媒体报道横幅、用户评价卡片轮播——几乎任何类型

---

### 【T-28】惰性跟随光标（Lagging / Lerp Cursor Follow）
**来源参考**：Locomotive Studio 官网、众多 Awwwards SOTD 创意机构站
**效果**：自定义圆形光标以 lerp（线性插值）的方式延迟跟随鼠标，产生"拖拽感"流体运动。悬停按钮/链接时光标膨胀变形
**JS 实现**：
```javascript
const cursor = document.querySelector('.cursor');
const follower = document.querySelector('.cursor-follower'); // 延迟更大的外圈
let mx=0, my=0, fx=0, fy=0, lx=0, ly=0;
document.addEventListener('mousemove', e => { mx=e.clientX; my=e.clientY; });
(function loop() {
  fx += (mx - fx) * 0.18;  // 内圈快
  fy += (my - fy) * 0.18;
  lx += (mx - lx) * 0.08;  // 外圈慢（惰性更强）
  ly += (my - ly) * 0.08;
  cursor.style.transform = `translate(${fx}px,${fy}px)`;
  follower.style.transform = `translate(${lx}px,${ly}px)`;
  requestAnimationFrame(loop);
})();
// hover 交互元素时：cursor.classList.add('expanded') → scale(3) + mix-blend-mode:difference
document.querySelectorAll('a,button').forEach(el => {
  el.addEventListener('mouseenter', () => cursor.classList.add('expanded'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('expanded'));
});
/* cursor { position:fixed; width:8px; height:8px; border-radius:50%; background:white; pointer-events:none; z-index:9999; margin:-4px 0 0 -4px; }
   cursor-follower { position:fixed; width:36px; height:36px; border:1px solid rgba(255,255,255,0.5); border-radius:50%; pointer-events:none; z-index:9998; margin:-18px 0 0 -18px; }
   cursor.expanded { transform: scale(3)!important; mix-blend-mode:difference; background:white; } */
```
**适用类型**：创意机构、奢侈品、作品集——一切需要"精致感"的品牌

---

### 【T-29】旋转词语标题（Rotating Word Hero）
**来源参考**：Godly 精选中大量 SaaS / AI 工具落地页，Awwwards SOTD agency 首页
**效果**：Hero 标题中某个关键词持续循环替换（fade/slide/clip 动画），传达品牌多维价值
**CSS/JS 实现**：
```javascript
const words = ['Faster', 'Smarter', 'Effortless', 'Beautiful'];
const el = document.querySelector('.rotating-word');
let i = 0;
function swap() {
  el.classList.add('exit');        // CSS: translateY(-100%) + opacity:0, duration 0.4s
  setTimeout(() => {
    el.textContent = words[i % words.length];
    el.classList.remove('exit');
    el.classList.add('enter');     // CSS: translateY(100%)→0 + opacity:0→1, duration 0.5s
    setTimeout(() => el.classList.remove('enter'), 500);
    i++;
  }, 400);
}
setInterval(swap, 2400);
/* CSS: .rotating-word { display:inline-block; overflow:hidden; vertical-align:bottom; color:var(--accent); }
   .rotating-word.exit { animation: wordOut 0.4s cubic-bezier(0.4,0,1,1) forwards; }
   .rotating-word.enter { animation: wordIn 0.5s cubic-bezier(0,0,0.2,1) forwards; }
   @keyframes wordOut { to { transform:translateY(-110%); opacity:0; } }
   @keyframes wordIn { from { transform:translateY(110%); opacity:0; } to { transform:translateY(0); opacity:1; } } */
```
**适用类型**：SaaS、AI 工具、开发者平台、设计工具——任何有多个核心价值的产品

---

### 【T-30】视口锁定滚动叙事（Scroll-Locked Storytelling Section）
**来源参考**：Apple 产品页、众多 Awwwards 最佳叙事类网站、Codrops "Pinning: Lock Elements in Place"
**效果**：某个 section 高度设为 300vh，内容 sticky 固定，随用户滚动在同一视口内依次播放 3 个内容面板（文字/图片变化），制造"电影帧"感
**JS 实现**：
```javascript
const section = document.querySelector('.story-lock');
const panels = section.querySelectorAll('.story-panel');
window.addEventListener('scroll', () => {
  const rect = section.getBoundingClientRect();
  if (rect.top > 0 || rect.bottom < window.innerHeight) return;
  const progress = Math.abs(rect.top) / (rect.height - window.innerHeight); // 0→1
  const activeIndex = Math.min(Math.floor(progress * panels.length), panels.length - 1);
  panels.forEach((p, i) => {
    p.style.opacity = i === activeIndex ? '1' : '0';
    p.style.transform = i === activeIndex ? 'translateY(0)' : i < activeIndex ? 'translateY(-40px)' : 'translateY(40px)';
  });
});
/* CSS: .story-lock { height:300vh; } .story-lock-inner { position:sticky; top:0; height:100vh; }
   .story-panel { position:absolute; inset:0; opacity:0; transition:opacity 0.5s, transform 0.6s cubic-bezier(0.16,1,0.3,1); } */
```
**适用类型**：产品功能展示、硬件/科技品牌、游戏叙事、AI工具步骤演示

---

### 【T-31】弹性网格列滚动（Elastic Grid Scroll）
**来源参考**：Codrops `ElasticGridScroll`（2024）、Awwwards 多列错速滚动站点
**效果**：多列图片网格中，各列以不同速度滚动，产生弹性/错位的视觉张力
**JS 实现**：
```javascript
const cols = document.querySelectorAll('.grid-col');
const speeds = [0.6, 1.0, 0.75, 1.15];
let lastY = 0;
window.addEventListener('scroll', () => {
  const dy = window.scrollY - lastY; lastY = window.scrollY;
  cols.forEach((col, i) => {
    const current = parseFloat(col.dataset.offset || 0);
    const target = current + dy * (speeds[i % speeds.length] - 1);
    col.dataset.offset = target;
    col.style.transform = `translateY(${target * 0.4}px)`;
  });
});
/* CSS: .grid-col { transition: transform 0.8s cubic-bezier(0.16,1,0.3,1); } */
```
**适用类型**：摄影作品集、时尚品牌、NFT画廊、创意机构图片展示区

---

### 【T-32】动态渐变边框（Animated Gradient Border）
**来源参考**：Godly 精选 SaaS 卡片、Codrops border-gradient 技巧、Awwwards 2024-25 卡片组件
**效果**：卡片或按钮边框为旋转渐变色，hover 时加速旋转；也可用作 section 分割线动画
**CSS 实现**：
```css
.grad-border {
  position: relative; border-radius: 12px; padding: 1px;
  background: linear-gradient(var(--angle, 135deg), #6366f1, #ec4899, #06b6d4);
  animation: rotate-border 4s linear infinite;
}
@property --angle { syntax: '<angle>'; initial-value: 0deg; inherits: false; }
@keyframes rotate-border { to { --angle: 360deg; } }
.grad-border-inner { background: var(--bg); border-radius: 11px; padding: 24px; }
```
**适用类型**：SaaS 定价卡片高亮、AI 工具功能卡、NFT/Web3、游戏卡片

---

### 【T-33】文字描边扫光（SVG Text Stroke Sweep）
**来源参考**：Awwwards SOTD 奢侈品/艺术类页面、Codrops SVG text stroke 系列
**效果**：标题文字为空心描边，hover 或滚动触发时渐变"扫光"填充，产生刻字质感
**CSS/JS 实现**：
```css
.stroke-text {
  -webkit-text-stroke: 1.5px currentColor;
  color: transparent;
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent) 50%, transparent 50%);
  background-size: 200% 100%;
  background-position: 100% 0;
  -webkit-background-clip: text;
  transition: background-position 0.8s cubic-bezier(0.16,1,0.3,1);
}
.stroke-text.active, .stroke-text:hover { background-position: 0% 0; }
```
**适用类型**：奢侈品 Hero 标题、创意机构大字标语、时尚/美妆品牌、游戏章节标题

---

### 【T-34】滚动触发横向滑动（Horizontal Scroll Section）
**来源参考**：Apple Mac Pro 产品页、Codrops "Horizontal Scroll with GSAP"、Awwwards 产品发布页
**效果**：某个 section 固定视口，竖向滚动驱动内部卡片横向移动，营造"相机拉镜"感
**JS 实现**：
```javascript
const section = document.querySelector('.h-scroll');
const inner = section.querySelector('.h-scroll-inner');
window.addEventListener('scroll', () => {
  const rect = section.getBoundingClientRect();
  if (rect.top > 0 || rect.bottom < window.innerHeight) return;
  const progress = Math.abs(rect.top) / (rect.height - window.innerHeight);
  const maxX = inner.scrollWidth - window.innerWidth;
  inner.style.transform = `translateX(${-progress * maxX}px)`;
});
/* CSS: .h-scroll { height: 400vh; } .h-scroll-sticky { position:sticky; top:0; height:100vh; overflow:hidden; }
   .h-scroll-inner { display:flex; width:max-content; } */
```
**适用类型**：产品功能横向展示、时间轴、游戏关卡介绍、品牌历史叙事

---

### 【T-35】鼠标跟随 3D 卡片倾斜（Mouse-Tracked 3D Card Tilt）
**来源参考**：Codrops "3D Card Tilt Effect"、Godly SaaS 精选、Awwwards 产品展示卡片
**效果**：卡片随鼠标位置在 X/Y 轴微微倾斜（perspective 3D），光泽层跟随鼠标，产生实体感
**JS 实现**：
```javascript
document.querySelectorAll('.tilt-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    card.style.transform = `perspective(600px) rotateY(${x * 12}deg) rotateX(${-y * 12}deg) scale(1.02)`;
    const glare = card.querySelector('.glare');
    if (glare) glare.style.background = `radial-gradient(circle at ${(x+0.5)*100}% ${(y+0.5)*100}%, rgba(255,255,255,0.15), transparent 70%)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(600px) rotateY(0) rotateX(0) scale(1)';
  });
});
/* CSS: .tilt-card { transition: transform 0.4s cubic-bezier(0.16,1,0.3,1); transform-style: preserve-3d; }
   .glare { position:absolute; inset:0; border-radius:inherit; pointer-events:none; } */
```
**适用类型**：SaaS 功能卡片、产品展示、游戏角色卡、NFT 卡片、App 推广 mockup

---

### 【T-36】文字模糊聚焦入场（Text Blur Focus Reveal）
**来源参考**：Codrops "Blur In" 系列、Godly 精选 AI 工具落地页、Awwwards 品牌叙事页
**效果**：标题从极度模糊（blur(20px) + opacity:0）状态渐渐清晰聚焦入场，比普通 fade-up 更戏剧
**CSS/JS 实现**：
```css
.blur-reveal { opacity: 0; filter: blur(20px); transform: scale(1.05);
  transition: opacity 1s ease, filter 1s ease, transform 1s cubic-bezier(0.16,1,0.3,1); }
.blur-reveal.active { opacity: 1; filter: blur(0); transform: scale(1); }
/* 逐词版：将文字拆成 span，transition-delay 按 index * 80ms 错开 */
```
**适用类型**：AI工具品牌核心 Slogan、奢侈品/香水 Hero、游戏开场字幕、叙事型品牌宣言

---

### 【T-37】滚动驱动进度条（Scroll-Driven Progress Bar）
**来源参考**：CSS `animation-timeline: scroll()` 原生规范（Chrome 115+）、Codrops 2024 Scroll-Driven Animations 系列
**效果**：页面顶部固定细线进度条随用户滚动自动增长，纯 CSS 实现无需 JS
**CSS 实现**：
```css
@keyframes progress { from { transform: scaleX(0); } to { transform: scaleX(1); } }
.scroll-progress {
  position: fixed; top: 0; left: 0; right: 0; height: 2px;
  background: var(--accent); transform-origin: left;
  animation: progress linear;
  animation-timeline: scroll(root block);
}
/* 降级JS版（Safari兼容）：
   window.addEventListener('scroll', () => {
     const p = window.scrollY / (document.body.scrollHeight - window.innerHeight);
     bar.style.transform = `scaleX(${p})`;
   }); */
```
**适用类型**：长文章/博客、叙事型落地页、产品发布页、个人作品集

---

### 【T-38】图片展开覆盖过渡（Image Expand Overlay Transition）
**来源参考**：Codrops `SlideshowAnimations`、Awwwards 作品集页面图片点击展开效果
**效果**：点击缩略图时以 clip-path 从原位扩展覆盖整个视口，形成无缝过渡
**JS 实现**：
```javascript
document.querySelectorAll('.expandable').forEach(img => {
  img.addEventListener('click', () => {
    const r = img.getBoundingClientRect();
    const overlay = document.querySelector('.img-overlay');
    overlay.style.backgroundImage = `url(${img.src})`;
    overlay.style.clipPath = `inset(${r.top}px ${window.innerWidth - r.right}px ${window.innerHeight - r.bottom}px ${r.left}px)`;
    overlay.style.display = 'block';
    requestAnimationFrame(() => {
      overlay.style.transition = 'clip-path 0.7s cubic-bezier(0.16,1,0.3,1)';
      overlay.style.clipPath = 'inset(0px 0px 0px 0px)';
    });
  });
});
/* CSS: .img-overlay { position:fixed; inset:0; z-index:999; background-size:cover; background-position:center; } */
```
**适用类型**：摄影作品集、时装品牌 Lookbook、游戏截图展示、创意机构案例页

---

### 【T-39】环境光标跟随光晕（Ambient Cursor Glow）
**来源参考**：Linear、Vercel 等 AI/SaaS 产品暗色页、Codrops 2024 光效实验
**效果**：暗色背景上鼠标周围有大半径（400px）极淡径向渐变光晕随鼠标移动，营造"环境光"氛围感；比 T-17 更微妙不遮挡内容
**JS 实现**：
```javascript
const glow = document.createElement('div');
glow.className = 'ambient-glow';
document.body.appendChild(glow);
document.addEventListener('mousemove', e => {
  glow.style.left = e.clientX + 'px';
  glow.style.top = e.clientY + 'px';
});
/* CSS: .ambient-glow {
  position:fixed; pointer-events:none; z-index:0;
  width:500px; height:500px; border-radius:50%;
  transform:translate(-50%,-50%);
  background:radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
  transition: left 0.3s ease, top 0.3s ease;
} */
```
**适用类型**：AI工具、SaaS、开发者工具、NFT/Web3——所有暗色系页面质感提升

---

### 【T-40】文字行间距呼吸动画（Line Height Breathing）
**来源参考**：Codrops 排版实验、Awwwards 2025 极简主义 agency 页面
**效果**：Hero 大标题对 line-height 和 letter-spacing 做极微小的呼吸式变化，用户下意识感受到"活"的质感；可与 T-18 可变字体联动
**CSS 实现**：
```css
.breathing-text {
  animation: breathe 4s cubic-bezier(0.45,0,0.55,1) infinite alternate;
}
@keyframes breathe {
  from { letter-spacing: -0.02em; line-height: 0.95; }
  to   { letter-spacing:  0.01em; line-height: 1.05; }
}
/* 配合 variable font：
@keyframes breathe {
  from { font-variation-settings: 'wght' 300, 'wdth' 90; }
  to   { font-variation-settings: 'wght' 700, 'wdth' 110; }
} */
```
**适用类型**：奢侈品 Hero、叙事型品牌宣言、wellness/冥想品牌、个人作品集大标题

---

### 【T-41】手绘SVG路径动画（Hand-drawn SVG Path Animation）
**来源参考**：手绘风格 Awwwards 站点、Dribbble 插画类 landing page、Codrops SVG stroke 系列
**效果**：SVG 路径以 stroke-dasharray 动画模拟手绘"边描边出现"效果，配合不规则、有轻微抖动感的路径造型
**CSS/JS 实现**：
```javascript
const paths = document.querySelectorAll('.hand-path');
paths.forEach(path => {
  const len = path.getTotalLength();
  path.style.strokeDasharray = len;
  path.style.strokeDashoffset = len;
});
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(0.16,1,0.3,1)';
      e.target.style.strokeDashoffset = '0';
    }
  });
}, { threshold: 0.3 });
paths.forEach(p => obs.observe(p));
/* CSS: .hand-path { fill: none; stroke: var(--accent); stroke-width: 2.5; stroke-linecap: round; } */
```
**适用类型**：手绘/插画风格品牌、儿童教育、创意工作室、有机食品、wellness、个人博客

---

### 【T-42】物理弹跳效果（Physics Bounce / Spring Animation）
**来源参考**：Framer Motion 弹跳演示、iOS spring 动画参考、Codrops 弹性 UI 实验
**效果**：元素在交互时呈现真实弹簧物理感——点击按钮时 scale 先过冲（>1.1）再回弹至正常，或卡片拖拽松手后弹回原位
**JS 实现**：
```javascript
function springAnimate(el, targetScale, { stiffness = 200, damping = 15 } = {}) {
  let current = parseFloat(el.dataset.scale || 1), velocity = 0;
  function step() {
    const force = (targetScale - current) * stiffness;
    velocity = (velocity + force / 60) * (1 - damping / 60);
    current += velocity / 60;
    el.style.transform = `scale(${current})`;
    el.dataset.scale = current;
    if (Math.abs(velocity) > 0.001 || Math.abs(current - targetScale) > 0.001)
      requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
document.querySelectorAll('.spring-btn').forEach(btn => {
  btn.addEventListener('mousedown', () => springAnimate(btn, 1.12));
  btn.addEventListener('mouseup',   () => springAnimate(btn, 1.0));
  btn.addEventListener('mouseleave',() => springAnimate(btn, 1.0));
});
```
**适用类型**：App 推广页、游戏UI、卡通/儿童品牌、趣味互动类页面、移动端友好的 SaaS

---

### 【T-43】光标粒子拖尾（Cursor Particle Trail）
**来源参考**：Codrops particle cursor demos、Godly 精选炫酷光标特效、freefrontend canvas cursor
**效果**：鼠标移动时在路径上散落小粒子（发光点、星尘或品牌色点），每个粒子逐渐缩小淡出，产生"仙尘"或"电光"拖尾效果
**JS 实现**：
```javascript
const canvas = document.createElement('canvas');
canvas.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:9999';
document.body.appendChild(canvas);
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth; canvas.height = window.innerHeight;
const particles = [];
document.addEventListener('mousemove', e => {
  for (let i = 0; i < 3; i++) {
    particles.push({
      x: e.clientX, y: e.clientY, size: Math.random() * 5 + 2,
      alpha: 1, vx: (Math.random()-0.5)*3, vy: (Math.random()-0.5)*3
    });
  }
  if (particles.length > 120) particles.splice(0, particles.length - 120);
});
(function draw() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  particles.forEach(p => {
    p.x += p.vx; p.y += p.vy; p.size *= 0.93; p.alpha *= 0.91;
    ctx.globalAlpha = p.alpha;
    ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#fff';
    ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
  });
  ctx.globalAlpha = 1;
  requestAnimationFrame(draw);
})();
```
**适用类型**：游戏官网、NFT/Web3、赛博朋克风格、魔法/奇幻主题、视觉炫技类页面

---

### 【T-44】多层视差景深（Multi-layer Depth Parallax）
**来源参考**：Awwwards SOTD 多层视差经典案例、Codrops "Parallax Depth Effect"、游戏官网景深处理
**效果**：Hero 区域分为 4-6 个绝对定位层（远景/中景/主体/前景/粒子），每层 scroll 速率不同，配合 transform-origin 制造强烈3D空间感
**JS 实现**：
```javascript
const layerConfig = [
  { sel: '.layer-sky',  speed: 0.02 },
  { sel: '.layer-far',  speed: 0.06 },
  { sel: '.layer-mid',  speed: 0.12 },
  { sel: '.layer-near', speed: 0.22 },
  { sel: '.layer-text', speed: 0.08 },
  { sel: '.layer-dust', speed: 0.35 },
];
const layers = layerConfig.map(c => ({ el: document.querySelector(c.sel), speed: c.speed }))
  .filter(l => l.el);
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  layers.forEach(({ el, speed }) => {
    el.style.transform = `translateY(${y * speed}px)`;
  });
});
/* 各层 position:absolute，z-index 按远近排序，父容器 overflow:hidden position:relative */
```
**适用类型**：游戏官网、旅游目的地、自然/环保品牌、奇幻叙事、沉浸式体验页面

---

### 【T-45】Canvas 涂鸦互动（Interactive Canvas Doodle）
**来源参考**：Codrops Canvas 交互实验、Creative Coding 刮刮卡效果、Excalidraw 风格 UI
**效果**：页面某区域嵌入可涂鸦的 Canvas——用户可用鼠标自由绘制，提供颜色选择和清除按钮；或实现"刮刮卡"揭示隐藏内容
**JS 实现**：
```javascript
const canvas = document.querySelector('.doodle-canvas');
const ctx = canvas.getContext('2d');
let drawing = false, color = '#FF6B35', lineSize = 4;
function getPos(e, el) {
  const r = el.getBoundingClientRect();
  return [e.clientX - r.left, e.clientY - r.top];
}
canvas.addEventListener('mousedown', e => {
  drawing = true; ctx.beginPath();
  const [x, y] = getPos(e, canvas); ctx.moveTo(x, y);
});
canvas.addEventListener('mousemove', e => {
  if (!drawing) return;
  const [x, y] = getPos(e, canvas);
  ctx.lineTo(x, y);
  ctx.strokeStyle = color; ctx.lineWidth = lineSize;
  ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.stroke();
});
canvas.addEventListener('mouseup', () => { drawing = false; });
canvas.addEventListener('mouseleave', () => { drawing = false; });
document.querySelector('.clear-doodle')?.addEventListener('click', () =>
  ctx.clearRect(0, 0, canvas.width, canvas.height)
);
```
**适用类型**：儿童教育、创意工具、手绘风格品牌、黑客松/比赛页、互动型个人作品集

---

### 【T-46】文字波浪变形（Text Wave Deformation）
**来源参考**：Awwwards typography experiments、Codrops "Wavey Text Effect"、Three.js 平替方案
**效果**：文字字母沿 sin 波动曲线做 Y 轴位移，每个字母有不同相位偏移；hover 或滚动触发后波浪持续扩散
**JS 实现**：
```javascript
function waveText(el) {
  const chars = [...el.querySelectorAll('.char')];
  let phase = 0;
  (function animate() {
    chars.forEach((c, i) => {
      const y = Math.sin(phase + i * 0.45) * 10; // 10px 振幅
      c.style.transform = `translateY(${y}px)`;
    });
    phase += 0.055;
    requestAnimationFrame(animate);
  })();
}
// 先用 T-25 的 splitChars() 拆分字符，再调用 waveText()
document.querySelectorAll('.wave-text').forEach(el => {
  splitChars(el); // inline-block + --char variable
  waveText(el);
});
/* CSS: .wave-text .char { display:inline-block; } */
```
**适用类型**：音乐/娱乐品牌、游戏、赛博朋克、活力/运动品牌、潮流文化

---

### 【T-47】拖拽排序交互（Drag-to-Sort Interaction）
**来源参考**：SortableJS 原理、Trello/Notion 卡片拖拽 UX、Codrops 原生拖拽实验
**效果**：卡片列表支持鼠标拖拽重新排序，被拖拽卡片半透明悬浮，放下时平滑入位——作为产品功能的现场 Demo
**JS 实现（原生，不依赖库）**：
```javascript
let dragSrc = null;
document.querySelectorAll('.sortable-item').forEach(item => {
  item.setAttribute('draggable', true);
  item.addEventListener('dragstart', () => {
    dragSrc = item;
    setTimeout(() => item.classList.add('dragging'), 0);
  });
  item.addEventListener('dragend', () => {
    item.classList.remove('dragging');
    document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
  });
  item.addEventListener('dragover', e => {
    e.preventDefault(); item.classList.add('drag-over');
  });
  item.addEventListener('dragleave', () => item.classList.remove('drag-over'));
  item.addEventListener('drop', e => {
    e.preventDefault(); item.classList.remove('drag-over');
    if (dragSrc && dragSrc !== item) {
      const list = item.parentNode;
      const srcIdx = [...list.children].indexOf(dragSrc);
      const tgtIdx = [...list.children].indexOf(item);
      list.insertBefore(dragSrc, srcIdx > tgtIdx ? item : item.nextSibling);
    }
  });
});
/* CSS: .dragging { opacity:0.4; transform:scale(1.04); box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
   .drag-over { outline: 2px dashed var(--accent); outline-offset: 4px; } */
```
**适用类型**：SaaS 工作流工具、项目管理平台、教育平台课程排序、设计工具功能展示

---

### 【T-48】均衡器频谱可视化（Equalizer / Audio Visualizer）
**来源参考**：音乐 App 落地页、Spotify/Apple Music 风格 UI、Codrops audio visualizer demos
**效果**：纯CSS/JS模拟音频频谱柱状动画——多根竖条随机高度变化（@keyframes 不同 delay），营造音乐律动感；可作为装饰性 Hero 元素或 App mockup 内部组件
**CSS 实现**：
```css
.eq-bars { display: flex; align-items: flex-end; gap: 3px; height: 40px; }
.eq-bar { width: 3px; border-radius: 2px; background: var(--accent); transform-origin: bottom; }
.eq-bar:nth-child(1) { animation: eq 0.8s ease-in-out 0.00s infinite alternate; }
.eq-bar:nth-child(2) { animation: eq 0.6s ease-in-out 0.10s infinite alternate; }
.eq-bar:nth-child(3) { animation: eq 1.0s ease-in-out 0.20s infinite alternate; }
.eq-bar:nth-child(4) { animation: eq 0.7s ease-in-out 0.15s infinite alternate; }
.eq-bar:nth-child(5) { animation: eq 0.9s ease-in-out 0.05s infinite alternate; }
.eq-bar:nth-child(6) { animation: eq 0.65s ease-in-out 0.25s infinite alternate; }
.eq-bar:nth-child(7) { animation: eq 0.85s ease-in-out 0.08s infinite alternate; }
@keyframes eq {
  from { transform: scaleY(0.12); }
  to   { transform: scaleY(1); }
}
```
**适用类型**：音乐/播客 App、音频工具、娱乐平台、派对/活动页面、夜生活品牌

---

### 【T-49】故障闪烁效果（Glitch / Digital Distortion Effect）
**来源参考**：赛博朋克/废土风格 Awwwards 站点、Codrops "Glitch Effect"、游戏UI故障艺术、Dribbble 故障艺术精选
**效果**：文字或图片定时触发 CSS clip-path 故障切片 + RGB色差位移，产生"信号失真"视觉冲击；hover 时也可触发
**CSS 实现**：
```css
.glitch { position: relative; display: inline-block; }
.glitch::before, .glitch::after {
  content: attr(data-text); position: absolute; top: 0; left: 0;
  width: 100%; height: 100%; background: inherit;
}
.glitch::before {
  color: #ff0055; left: 2px;
  clip-path: polygon(0 15%, 100% 15%, 100% 35%, 0 35%);
  animation: glitch-a 3.5s steps(2) infinite;
}
.glitch::after {
  color: #00ffcc; left: -2px;
  clip-path: polygon(0 60%, 100% 60%, 100% 75%, 0 75%);
  animation: glitch-b 3.5s steps(2) 0.3s infinite;
}
@keyframes glitch-a {
  0%,85%,100% { transform: translate(0); opacity: 0; }
  87% { transform: translate(-3px, 1px); opacity: 0.8; }
  89% { transform: translate(3px, -1px); opacity: 0.8; }
  91% { transform: translate(0); opacity: 0; }
}
@keyframes glitch-b {
  0%,88%,100% { transform: translate(0); opacity: 0; }
  90% { transform: translate(4px, 0); opacity: 0.8; }
  92% { transform: translate(-2px, 2px); opacity: 0.8; }
  94% { transform: translate(0); opacity: 0; }
}
```
**适用类型**：赛博朋克、废土/末日风格、黑客松、游戏、NFT/Web3、暗黑哥特美学

---

### 【T-50】点击涟漪扩散（Click Ripple Effect）
**来源参考**：Material Design ripple、Google Inbox 交互反馈、iOS tap feedback
**效果**：点击任意按钮或卡片时，以点击位置为圆心扩散半透明光圈并快速消散——增强触感反馈，替代 :active 的生硬状态
**JS 实现**：
```javascript
document.querySelectorAll('.ripple-target').forEach(el => {
  el.style.position = 'relative';
  el.style.overflow = 'hidden';
  el.addEventListener('click', e => {
    const r = el.getBoundingClientRect();
    const size = Math.max(el.offsetWidth, el.offsetHeight) * 2.2;
    const ripple = document.createElement('span');
    ripple.className = 'ripple-wave';
    ripple.style.cssText = `
      width:${size}px; height:${size}px;
      left:${e.clientX - r.left - size/2}px;
      top:${e.clientY - r.top - size/2}px;
    `;
    el.appendChild(ripple);
    setTimeout(() => ripple.remove(), 800);
  });
});
/* CSS: .ripple-wave {
  position:absolute; border-radius:50%;
  background: rgba(255,255,255,0.25);
  transform: scale(0); pointer-events:none;
  animation: rippleOut 0.8s cubic-bezier(0,0,0.2,1) forwards;
}
@keyframes rippleOut { to { transform: scale(1); opacity: 0; } } */
```
**适用类型**：所有类型通用；尤其强化 CTA 按钮、功能卡片的点击感；卡通/App 风格页面必用

---

### 【T-51】全屏十字准星光标（Crosshair Cursor）
**来源参考**：设计工具 UI（Figma/Sketch）、狙击/瞄准美学、Awwwards 工业/科技风格站
**效果**：用两条全屏细线（横 + 竖）替代浏览器光标，随鼠标实时移动；hover 交互元素时线条变色变粗，并在交叉点出现品牌色小圆点。视觉完全颠覆 dot+ring 形态，适合设计工具/军事/精密仪器等品牌
**CSS/JS 实现**：
```javascript
const ch = document.createElement('div');
const cv = document.createElement('div');
ch.className = 'xhair-h'; cv.className = 'xhair-v';
document.body.append(ch, cv);
document.addEventListener('mousemove', e => {
  ch.style.top = e.clientY + 'px';
  cv.style.left = e.clientX + 'px';
});
document.querySelectorAll('a,button,.card').forEach(el => {
  el.addEventListener('mouseenter', () => { ch.classList.add('hot'); cv.classList.add('hot'); });
  el.addEventListener('mouseleave', () => { ch.classList.remove('hot'); cv.classList.remove('hot'); });
});
/* CSS:
.xhair-h,.xhair-v { position:fixed; pointer-events:none; z-index:9999; background:rgba(255,255,255,0.12); transition:background 0.2s, height 0.2s, width 0.2s; }
.xhair-h { height:1px; width:100vw; left:0; transform:translateY(-50%); }
.xhair-v { width:1px; height:100vh; top:0; transform:translateX(-50%); }
.xhair-h.hot { background:var(--accent); height:2px; }
.xhair-v.hot { background:var(--accent); width:2px; }
*/
```
**适用类型**：设计工具、精密仪器/科技品牌、军事/战术品牌、金融数据平台、开发者工具、摄影工作室

---

### 【T-52】旋转文字光标（Orbit Text Cursor）
**来源参考**：Awwwards 创意机构个人作品集（如 Bruno Simon portfolio 风格）、Godly 特效光标精选
**效果**：光标中心有一个小点，外圈 SVG textPath 文字沿圆形路径持续旋转（"BRAND · CLICK · EXPLORE ·"），lerp 延迟跟随鼠标。hover 交互元素时文字旋转加速或暂停 + 变色。形态与圆圈 dot+ring 完全不同：圆圈是静态轮廓，这是动态文字轨道
**CSS/JS 实现**：
```javascript
const orbit = document.createElement('div');
orbit.id = 'orbit-cursor';
orbit.innerHTML = `
  <svg viewBox="0 0 100 100" width="110" height="110" overflow="visible">
    <path id="op" d="M50,10 a40,40 0 1,1 -0.01,0" fill="none"/>
    <text font-size="8.5" fill="var(--accent)" letter-spacing="3.5" font-family="inherit" font-weight="600">
      <textPath href="#op">
        <animate attributeName="startOffset" from="0%" to="100%" dur="5s" repeatCount="indefinite" id="orbit-anim"/>
        HOVER · CLICK · EXPLORE ·
      </textPath>
    </text>
  </svg>
  <div class="orbit-dot"></div>`;
document.body.appendChild(orbit);
let ox=0, oy=0, tx=0, ty=0;
document.addEventListener('mousemove', e => { tx=e.clientX; ty=e.clientY; });
(function loop(){ ox+=(tx-ox)*0.10; oy+=(ty-oy)*0.10; orbit.style.left=(ox-55)+'px'; orbit.style.top=(oy-55)+'px'; requestAnimationFrame(loop); })();
document.querySelectorAll('a,button').forEach(el=>{
  el.addEventListener('mouseenter',()=>{ document.querySelector('#orbit-anim').setAttribute('dur','1.5s'); });
  el.addEventListener('mouseleave',()=>{ document.querySelector('#orbit-anim').setAttribute('dur','5s'); });
});
/* CSS:
#orbit-cursor { position:fixed; pointer-events:none; z-index:9999; }
.orbit-dot { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:7px; height:7px; background:var(--accent); border-radius:50%; }
*/
```
**适用类型**：创意机构、奢侈品牌、个人作品集、音乐/艺术项目、互动体验官网

---

### 【T-53】速度感残影光标（Velocity Ghost Trail Cursor）
**来源参考**：Codrops cursor effect experiments、Dribbble 高赞光标特效
**效果**：不显示传统圆圈，而是保存鼠标历史位置，渲染 6 个逐渐放大+透明度递减的残影圈。快速移动时残影间距大（彗星尾），慢速移动时残影叠合（静止聚焦感）。完全不同于 dot+ring：没有实时跟随的外圈，而是运动历史的痕迹
**JS 实现**：
```javascript
const ghosts = Array.from({length: 6}, (_, i) => {
  const g = document.createElement('div');
  const size = 8 + i * 7;
  g.style.cssText = `position:fixed;pointer-events:none;z-index:${9995-i};border-radius:50%;
    border:1.5px solid var(--accent);width:${size}px;height:${size}px;
    margin:${-size/2}px;opacity:${0.55 - i*0.08};left:-100px;top:-100px;`;
  document.body.appendChild(g); return g;
});
const history = Array(6).fill({x:-200,y:-200});
let histIdx = 0;
document.addEventListener('mousemove', e => {
  history[histIdx % 6] = {x: e.clientX, y: e.clientY};
  histIdx++;
});
(function loop(){
  ghosts.forEach((g, i) => {
    const pos = history[(histIdx - 1 - i * 1 + 60) % 6] || {x:-200,y:-200};
    g.style.left = pos.x + 'px'; g.style.top = pos.y + 'px';
  });
  requestAnimationFrame(loop);
})();
```
**适用类型**：游戏、赛车/运动速度感品牌、赛博朋克、视觉炫技类落地页、创意代理商

---

### 【T-54】液态 Blob 网格渐变背景（Liquid Blob Mesh Background）
**来源参考**：2024-2025 Figma 社区流行的 Mesh Gradient、Godly 精选暖色品牌站、Framer 模板 blob 风格
**效果**：3-4 个模糊的彩色 div blob（各自有 `border-radius` 形变动画）叠加在背景上，组合成"活的"渐变网格。比静态渐变有呼吸感，比 CSS gradient 更有机。可搭配 `mix-blend-mode: multiply` 或 `screen`
**CSS 实现**：
```css
.blob-wrap { position:absolute; inset:0; overflow:hidden; pointer-events:none; filter:blur(80px); opacity:0.6; }
.blob { position:absolute; border-radius:50%; }
.b1 { width:55vw; height:55vw; background:var(--accent); top:-10%; left:-5%; animation:blobA 14s ease-in-out infinite; }
.b2 { width:45vw; height:45vw; background:var(--secondary-color); bottom:-15%; right:-8%; animation:blobB 18s ease-in-out infinite; }
.b3 { width:40vw; height:40vw; background:var(--tertiary-color); top:35%; left:38%; animation:blobC 11s ease-in-out infinite; }
@keyframes blobA {
  0%,100% { transform:translate(0,0) scale(1); border-radius:50% 60% 40% 70%/60% 40% 70% 50%; }
  40%  { transform:translate(7vw,-5vw) scale(1.06); border-radius:70% 40% 60% 50%/40% 70% 50% 60%; }
  75%  { transform:translate(-4vw,8vw) scale(0.94); border-radius:40% 70% 50% 60%/70% 50% 60% 40%; }
}
@keyframes blobB {
  0%,100% { transform:translate(0,0) scale(1); border-radius:60% 40% 70% 50%/40% 70% 50% 60%; }
  50%  { transform:translate(-8vw,6vw) scale(1.08); border-radius:40% 60% 50% 70%/60% 40% 70% 50%; }
}
@keyframes blobC {
  0%,100% { transform:translate(0,0); border-radius:50%; }
  33%  { transform:translate(6vw,-7vw) scale(1.04); border-radius:65% 35% 55% 45%/45% 65% 35% 55%; }
  66%  { transform:translate(-5vw,5vw) scale(0.96); border-radius:35% 65% 45% 55%/65% 35% 55% 45%; }
}
```
**适用类型**：wellness、美妆、AI 产品（暖色系）、创意工作室、儿童教育、音乐/艺术

---

### 【T-55】幕帘分裂入场（Curtain Split Reveal）
**来源参考**：Locomotive Studio 入场动画、Cuberto 经典双幕帘、Awwwards SOTD agency 首页翻页感
**效果**：页面加载时，两块全屏黑色遮罩（左半 + 右半）向外分裂滑走，露出下方真实内容。品牌名/Logo 显示在幕帘中央，随幕帘消失。制造"大幕拉开"的剧场感，整个过程1.2-1.5s完成
**CSS/JS 实现**：
```javascript
// HTML结构: <div id="curtain"><div class="ct-l">BRAND</div><div class="ct-r"></div></div>
window.addEventListener('DOMContentLoaded', () => {
  const curtain = document.getElementById('curtain');
  requestAnimationFrame(() => requestAnimationFrame(() => {
    curtain.classList.add('open');
    setTimeout(() => { curtain.style.pointerEvents='none'; curtain.remove(); }, 1400);
  }));
});
/* CSS:
#curtain { position:fixed; inset:0; display:flex; z-index:10000; }
.ct-l, .ct-r { flex:1; background:var(--dark); transition:transform 1.2s cubic-bezier(0.16,1,0.3,1); display:flex; align-items:center; justify-content:center; }
.ct-l { transform-origin:left; }
.ct-r { transform-origin:right; }
#curtain.open .ct-l { transform:translateX(-100%); }
#curtain.open .ct-r { transform:translateX(100%); }
.ct-l .brand-name { font-family:var(--font-display); font-size:clamp(32px,5vw,72px); font-weight:700; color:#fff; letter-spacing:-2px; white-space:nowrap; }
*/
```
**适用类型**：奢侈品、高端品牌发布、游戏官网、剧院/演出、NFT/艺术画廊、任何需要"戏剧性入场"的品牌

---

### 【T-56】鼠标邻域文字排斥（Cursor Text Repulsion）
**来源参考**：Codrops "Repulsion Field" 实验、Awwwards 互动排版获奖作品、Bruno Simon 教程衍生
**效果**：标题或某段文字拆分为单字符，鼠标进入该区域时，临近的字符被"推开"（向光标的反方向平移），远离后弹回。产生"磁场排斥"的动态排版效果，光标像一块反磁铁穿过文字
**JS 实现**：
```javascript
function initRepulsion(el) {
  const chars = el.querySelectorAll('.char');
  document.addEventListener('mousemove', e => {
    chars.forEach(char => {
      const r = char.getBoundingClientRect();
      const cx = r.left + r.width/2, cy = r.top + r.height/2;
      const dist = Math.hypot(e.clientX - cx, e.clientY - cy);
      const radius = 90;
      if (dist < radius) {
        const force = (1 - dist/radius) * 28;
        const angle = Math.atan2(cy - e.clientY, cx - e.clientX);
        char.style.transform = `translate(${Math.cos(angle)*force}px,${Math.sin(angle)*force}px)`;
        char.style.transition = 'transform 0.12s ease';
      } else {
        char.style.transform = 'translate(0,0)';
        char.style.transition = 'transform 0.6s cubic-bezier(0.16,1,0.3,1)';
      }
    });
  });
}
// 先用 T-25 splitChars() 拆分目标文字，再调用 initRepulsion(el)
```
**适用类型**：创意机构标题、个人作品集、互动艺术项目、音乐品牌、任何有强排版标题的页面

---

### 【T-57】CSS 3D 翻转卡片（3D Flip Card Reveal）
**来源参考**：Codrops "Flipping Cards" 经典教程、Awwwards team/product 展示页、Godly 精选动效卡片
**效果**：卡片正面 hover 后做 `rotateY(180deg)` 完整翻转，背面显示详情/CTA/报价。与 T-35（倾斜tilt）完全不同：T-35 是小角度摇摆，T-57 是180°翻转揭示隐藏内容，有强烈"解锁"感
**CSS 实现**：
```css
.flip-card { perspective: 800px; }
.flip-inner {
  transform-style: preserve-3d;
  transition: transform 0.7s cubic-bezier(0.4,0,0.2,1);
  position: relative;
}
.flip-card:hover .flip-inner { transform: rotateY(180deg); }
.flip-front, .flip-back {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}
.flip-back {
  transform: rotateY(180deg);
  position: absolute; inset: 0;
  background: var(--accent);
  color: #fff;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  border-radius: inherit;
  padding: 24px;
}
/* 可选：hover 卡片外部有 glow 提示可翻转 */
.flip-card::after { content:'↻'; position:absolute; top:12px; right:12px; font-size:14px; opacity:0.3; transition:opacity 0.3s; }
.flip-card:hover::after { opacity:0; }
```
**适用类型**：团队介绍（正面=照片，背面=简介）、产品功能（正面=图片，背面=规格+CTA）、价格卡片、技能展示

---

### 【T-58】模糊聚焦滚动揭示（Blur Focus Scroll Reveal）
**来源参考**：Awwwards "focus" 风格叙事页、Codrops scroll-based blur 实验、摄影作品集常见手法
**效果**：元素初始为 `filter:blur(14px) + opacity:0 + scale(0.96)`，滚动进入视口时"聚焦"为清晰——模拟镜头对焦的感觉。比普通 fade-up reveal 更有质感，尤其适合摄影/产品大图
**CSS/JS 实现**：
```css
.blur-reveal {
  filter: blur(14px);
  opacity: 0;
  transform: scale(0.96);
  transition: filter 0.9s ease, opacity 0.9s ease, transform 0.9s cubic-bezier(0.16,1,0.3,1);
}
.blur-reveal.focused { filter: blur(0); opacity: 1; transform: scale(1); }
```
```javascript
const blurObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('focused'); blurObs.unobserve(e.target); }
  });
}, { threshold: 0.1, rootMargin: '-20px' });
document.querySelectorAll('.blur-reveal').forEach(el => blurObs.observe(el));
```
**适用类型**：摄影师作品集、奢侈品/香水、wellness、高端餐厅、任何以"视觉沉浸"为核心的品牌

---

### 【T-59】磁性浮动标签群（Magnetic Floating Tag Cluster）
**来源参考**：Awwwards skill tag 交互、Godly 精选 tag cloud、Framer 技术栈展示
**效果**：多个标签/技能/关键词 chip 以自由漂浮状态排列，鼠标靠近时被"吸引"轻微位移（半径120px内有磁力拉拽感），整体组合形成活的"技能星座"或"品牌关键词场"。与 T-03 磁性按钮不同：那是单个按钮，这是整个标签群的集体磁场反应
**JS 实现**：
```javascript
document.querySelectorAll('.mag-tag').forEach(tag => {
  const baseX = parseFloat(tag.dataset.x || 0);
  const baseY = parseFloat(tag.dataset.y || 0);
  document.addEventListener('mousemove', e => {
    const rect = tag.getBoundingClientRect();
    const cx = rect.left + rect.width/2, cy = rect.top + rect.height/2;
    const dist = Math.hypot(e.clientX - cx, e.clientY - cy);
    const radius = 120;
    if (dist < radius) {
      const force = (1 - dist/radius) * 18;
      const dx = (e.clientX - cx) / dist * force; // 吸引（同向）
      const dy = (e.clientY - cy) / dist * force;
      tag.style.transform = `translate(${dx}px, ${dy}px) scale(1.08)`;
      tag.style.transition = 'transform 0.15s ease';
    } else {
      tag.style.transform = 'translate(0,0) scale(1)';
      tag.style.transition = 'transform 0.7s cubic-bezier(0.16,1,0.3,1)';
    }
  });
});
/* 配合 CSS float 动画: @keyframes tagFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
   .mag-tag { animation: tagFloat calc(3s + var(--delay)) ease-in-out infinite; } */
```
**适用类型**：个人作品集（技术栈展示）、创意机构（服务/关键词）、SaaS功能点、开发者工具、品牌宣言

---

### 【T-60】幕布式图片遮罩展开（Image Curtain Wipe Reveal）
**来源参考**：Awwwards photo portfolio reveal、Codrops "Image Reveal on Scroll"、Lusion gallery page
**效果**：图片初始被 CSS `clip-path: inset(0 100% 0 0)` 遮住（完全隐藏），滚动进入视口时从左向右展开，同时图片轻微从右向左平移（制造视差感）。比淡入更有力量感，适合大图展示
**CSS/JS 实现**：
```css
.wipe-wrap { overflow: hidden; }
.wipe-img {
  clip-path: inset(0 100% 0 0);
  transform: translateX(4%);
  transition: clip-path 1.1s cubic-bezier(0.16,1,0.3,1),
              transform 1.4s cubic-bezier(0.16,1,0.3,1);
}
.wipe-img.wiped { clip-path: inset(0 0% 0 0); transform: translateX(0); }
```
```javascript
const wipeObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('wiped'); wipeObs.unobserve(e.target); }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.wipe-img').forEach(el => wipeObs.observe(el));
// 可配合 stagger: 多张图片依次 wipe，transitionDelay: i * 0.15s
```
**适用类型**：摄影师作品集、创意机构案例页、时尚/服装电商、旅游目的地、任何以"大图说话"为核心的品牌

---

### 【T-61】反向列滚动（Reverse-Scrolling Columns）
**来源参考**：scroll-driven-animations.style 官方 Demo、CSS Scroll-Driven Animations 规范
**效果**：三列布局中，中间列正常滚动，左右两列反向滚动（向上），产生强烈视差拉伸感，纯 CSS 实现
**CSS 实现**：
```css
@keyframes scroll-up { from { transform: translateY(0); } to { transform: translateY(-100%); } }
@keyframes scroll-down { from { transform: translateY(-100%); } to { transform: translateY(0); } }
.col-left, .col-right {
  animation: scroll-up linear;
  animation-timeline: scroll(root);
}
.col-center {
  animation: scroll-down linear;
  animation-timeline: scroll(root);
}
/* JS降级版：window.addEventListener('scroll', () => {
  const p = window.scrollY;
  colLeft.style.transform = `translateY(${-p * 0.3}px)`;
  colRight.style.transform = `translateY(${-p * 0.3}px)`;
  colCenter.style.transform = `translateY(${p * 0.15}px)`;
}); */
```
**适用类型**：摄影画廊、作品集首页、时尚品牌、NFT 展示、创意机构 Hero 区

---

### 【T-62】封面收缩导航栏（Cover-to-Fixed Header Shrink）
**来源参考**：scroll-driven-animations.style Cover Card Demo、Apple 产品页导航行为
**效果**：页面顶部 Hero 区域随滚动从全屏高度收缩，平滑变形为固定的小导航栏，品牌名缩小留在左侧
**CSS/JS 实现**：
```javascript
const hero = document.querySelector('.hero-header');
const nav = document.querySelector('.fixed-nav');
window.addEventListener('scroll', () => {
  const progress = Math.min(window.scrollY / 300, 1); // 0→1 over 300px scroll
  hero.style.height = `${100 - progress * 94}vh`;     // 100vh → 6vh
  hero.style.fontSize = `${1 - progress * 0.6}em`;
  if (progress > 0.9) nav.classList.add('visible');
  else nav.classList.remove('visible');
});
/* CSS: .hero-header { position:sticky; top:0; transition: height 0.1s linear; overflow:hidden; }
   .fixed-nav { position:fixed; top:0; opacity:0; transition:opacity 0.3s; }
   .fixed-nav.visible { opacity:1; } */
```
**适用类型**：品牌官网、奢侈品、酒店、产品发布页、作品集——任何有强烈 Hero 的页面

---

### 【T-63】OS 桌面拟真界面（Desktop OS Skeuomorphic UI）
**来源参考**：PostHog 官网、Figma 早期官网风格、Awwwards 创意开发者工具类 SOTD
**效果**：整个页面或某个 section 模拟操作系统桌面——有菜单栏、文件图标、可点击的"窗口"卡片，导航链接用文件名格式（`about.md`、`work.fig`），营造强烈开发者/极客气质
**CSS/JS 实现**：
```css
/* Menubar */
.os-menubar { height:28px; background:rgba(255,255,255,0.85); backdrop-filter:blur(20px);
  display:flex; align-items:center; gap:16px; padding:0 16px; font-size:13px; }
.os-menubar .apple { font-size:16px; }
/* File icon */
.file-icon { display:flex; flex-direction:column; align-items:center; gap:4px; cursor:pointer; }
.file-icon:hover .icon-img { transform:scale(1.08); }
/* Window card */
.os-window { border-radius:10px; box-shadow:0 20px 60px rgba(0,0,0,0.3);
  overflow:hidden; background:var(--bg); }
.os-window-titlebar { height:28px; background:#2d2d2d; display:flex; align-items:center; gap:8px; padding:0 12px; }
.os-dot { width:12px; height:12px; border-radius:50%; }
.os-dot.red{background:#ff5f56;} .os-dot.yellow{background:#ffbd2e;} .os-dot.green{background:#27c93f;}
```
**适用类型**：开发者工具、技术产品、黑客松、个人作品集（极客风）、SaaS Dashboard 展示

---

### 【T-64】章节编号叙事布局（Numbered Chapter Scroll Layout）
**来源参考**：africa.climatemobility.org、McKinsey 深度报告页、The Pudding 数据叙事文章
**效果**：左侧固定竖向章节导航（01/02/03 + 标题），右侧内容区滚动；当前可见章节高亮左侧对应编号；图片与文字强烈交替，超大统计数字作为排版元素插入段落
**JS 实现**：
```javascript
const sections = document.querySelectorAll('.chapter');
const navItems = document.querySelectorAll('.chapter-nav-item');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navItems.forEach(n => n.classList.remove('active'));
      const id = entry.target.dataset.chapter;
      document.querySelector(`[data-nav="${id}"]`)?.classList.add('active');
    }
  });
}, { threshold: 0.4 });
sections.forEach(s => observer.observe(s));
/* CSS: .chapter-nav { position:sticky; top:0; height:100vh; width:200px; }
   .chapter-nav-item { opacity:0.3; transition:opacity 0.3s; }
   .chapter-nav-item.active { opacity:1; }
   .stat-callout { font-size:clamp(60px,8vw,120px); font-weight:800; line-height:1; } */
```
**适用类型**：深度报告/白皮书落地页、NGO/公益机构、媒体内容页、品牌年报、教育机构

---

### 【T-65】贴纸/徽章式导航（Sticker Badge Navigation）
**来源参考**：The Pudding 导航系统、Awwwards 创意个人作品集、Godly 趣味品牌站
**效果**：导航按钮做成实体贴纸/徽章样式——有轻微倾斜（rotate(-2deg)）、撕边阴影、纸张质感背景，hover 时"撕起来"（scale + 恢复正位），让页面充满手工趣味感
**CSS 实现**：
```css
.sticker-btn {
  background: var(--accent); border-radius: 4px;
  transform: rotate(-2deg);
  box-shadow: 2px 3px 0 rgba(0,0,0,0.15), 0 1px 0 rgba(255,255,255,0.4) inset;
  padding: 8px 16px; font-weight:700; letter-spacing:0.02em;
  transition: transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.2s;
  cursor: pointer;
}
.sticker-btn:nth-child(2n) { transform: rotate(1.5deg); }
.sticker-btn:hover {
  transform: rotate(0deg) scale(1.06);
  box-shadow: 4px 6px 0 rgba(0,0,0,0.2);
}
/* 纸张纹理版：background-image: url("data:image/svg+xml,...") 叠加噪点 */
```
**适用类型**：创意个人作品集、设计工作室、食品/咖啡品牌、教育/儿童平台、Pudding 风格媒体

---

### 【T-66】非矩形图片排版（Non-Rectangular Image Shapes）
**来源参考**：arts.ac.uk、ayana.com 酒店页、Awwwards 2024-25 有机形状设计趋势
**效果**：图片不局限于矩形，用 clip-path 裁成圆形/椭圆/菱形/不规则多边形/波浪形，作为排版元素与文字互动；hover 时形状变形过渡到另一个 clip-path 值
**CSS 实现**：
```css
/* 圆形 */
.img-circle { clip-path: circle(50% at 50% 50%); }
/* 菱形 */
.img-diamond { clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%); }
/* 有机斑点 */
.img-blob { clip-path: polygon(30% 0%, 70% 5%, 95% 30%, 100% 65%, 75% 95%, 35% 100%, 5% 80%, 0% 40%); }
/* hover 变形 */
.img-blob { transition: clip-path 0.6s cubic-bezier(0.34,1.56,0.64,1); }
.img-blob:hover { clip-path: polygon(20% 5%, 80% 0%, 100% 50%, 85% 90%, 50% 100%, 10% 95%, 0% 55%, 5% 20%); }
/* 波浪底边 section */
.wave-section::after { content:''; display:block; height:80px;
  background: var(--next-bg);
  clip-path: ellipse(55% 100% at 50% 100%); }
```
**适用类型**：旅游/酒店、wellness、艺术学院、时尚品牌、个人作品集——任何需要打破矩形束缚的设计

---

### 【T-67】FLIP 布局切换动画（FLIP Layout Transition）
**来源参考**：Motion.dev Layout Animation、Google FLIP 技术、Awwwards 网格↔列表视图切换
**效果**：点击切换按钮时，卡片在网格布局和列表布局之间平滑过渡——每张卡片记住自己的起始位置，用 transform 动画到终止位置，实现真实的位移动画而非淡入淡出
**JS 实现**：
```javascript
function flip(container) {
  const items = [...container.querySelectorAll('.card')];
  // 1. 记录 First 位置
  const first = items.map(el => el.getBoundingClientRect());
  // 2. 切换 class（改变布局）
  container.classList.toggle('grid-view');
  // 3. 记录 Last 位置
  const last = items.map(el => el.getBoundingClientRect());
  // 4. Invert + Play
  items.forEach((el, i) => {
    const dx = first[i].left - last[i].left;
    const dy = first[i].top - last[i].top;
    const dw = first[i].width / last[i].width;
    el.style.transform = `translate(${dx}px,${dy}px) scale(${dw})`;
    el.style.transition = 'none';
    requestAnimationFrame(() => {
      el.style.transition = 'transform 0.5s cubic-bezier(0.16,1,0.3,1)';
      el.style.transform = '';
    });
  });
}
```
**适用类型**：作品集网格/列表切换、电商产品视图、SaaS Dashboard 卡片重排、游戏卡牌排列

---

### 【T-68】元素退场动画（Exit / Leave Animation）
**来源参考**：Motion.dev AnimatePresence、Awwwards 模态框/通知消失动效、Godly SaaS 微交互
**效果**：元素消失时有明确的退场动画（向上飞出、缩小消失、向侧滑出），而不是简单的 display:none 或 opacity:0；toast 消失、modal 关闭、tab 切换都适用
**JS 实现**：
```javascript
function animateOut(el, onComplete) {
  el.style.transition = 'opacity 0.3s ease, transform 0.3s cubic-bezier(0.4,0,1,1)';
  el.style.opacity = '0';
  el.style.transform = 'translateY(-12px) scale(0.95)';
  el.addEventListener('transitionend', () => {
    el.style.display = 'none';
    onComplete?.();
  }, { once: true });
}
function animateIn(el) {
  el.style.display = 'block';
  el.style.opacity = '0';
  el.style.transform = 'translateY(12px) scale(0.97)';
  requestAnimationFrame(() => {
    el.style.transition = 'opacity 0.4s ease, transform 0.4s cubic-bezier(0.16,1,0.3,1)';
    el.style.opacity = '1';
    el.style.transform = 'translateY(0) scale(1)';
  });
}
```
**适用类型**：所有有 modal / toast / dropdown / tab 切换的页面——通用微交互质量提升

---

### 【T-69】Cover Flow 3D 封面翻转轮播（Cover Flow Carousel）
**来源参考**：scroll-driven-animations.style Cover Flow Demo（源自 Apple iTunes 经典效果）
**效果**：横向可滚动卡片列表，每张卡片随自身进出视口在 Y 轴透视旋转（两侧倾斜、居中朝正面），配合 `-webkit-box-reflect` 倒影，scroll snapping 保证每次停在正中央
**CSS 实现**：
```css
.coverflow-list { display:flex; overflow-x:scroll; scroll-snap-type:x mandatory; perspective:600px; }
.coverflow-item { scroll-snap-align:center; flex-shrink:0; width:200px; aspect-ratio:1; }
.coverflow-item img {
  width:100%; height:auto;
  -webkit-box-reflect: below 0.5em linear-gradient(transparent, rgba(0,0,0,0.2));
  animation: rotate-cover linear both;
  animation-timeline: view(x);
}
@keyframes rotate-cover {
  0%   { transform: translateX(-60%) rotateY(-45deg); }
  35%  { transform: translateX(0)    rotateY(-45deg); }
  50%  { transform: rotateY(0deg)    translateZ(1em) scale(1.4); }
  65%  { transform: translateX(0)    rotateY(45deg);  }
  100% { transform: translateX(60%)  rotateY(45deg);  }
}
```
**适用类型**：音乐/播客平台、电商产品展示、NFT 画廊、游戏截图轮播、作品集展示

---

### 【T-70】帘幕式 clip-path 图片揭示（Curtain Clip-path Image Reveal on Scroll）
**来源参考**：scroll-driven-animations.style Image Reveal Demo
**效果**：图片以 clip-path 从中心向四周展开（`inset(45% 20% 45% 20%)` → `inset(0%)`）配合 opacity，在滚动进入视口时触发，比普通 fade-up 更具仪式感
**CSS 实现**：
```css
@keyframes reveal-curtain {
  from { opacity:0; clip-path: inset(45% 20% 45% 20%); }
  to   { opacity:1; clip-path: inset(0% 0% 0% 0%); }
}
.curtain-reveal {
  animation: linear reveal-curtain both;
  animation-timeline: view();
  animation-range: entry 25% cover 50%;
}
/* JS 降级版（Safari兼容）：
   IntersectionObserver 触发时 el.classList.add('revealed')
   .curtain-reveal.revealed { animation: reveal-curtain 0.8s cubic-bezier(0.16,1,0.3,1) forwards; } */
```
**适用类型**：摄影作品集、奢侈品/时尚图片区、旅游酒店、建筑事务所、任何图片密集型页面

---

### 【T-71】双向飞入飞出列表（Fly-in / Fly-out Scroll List）
**来源参考**：scroll-driven-animations.style Contact List Demo
**效果**：列表项进入视口时从下方飞入（translateY(100%) → 0），离开视口时向上飞出（0 → translateY(-100%）），单套 keyframes 同时处理两段动画，营造"存在感"而非静态渐变
**CSS 实现**：
```css
@keyframes fly-in-out {
  entry 0%   { opacity:0; transform: translateY(80px); }
  entry 100% { opacity:1; transform: translateY(0); }
  exit  0%   { opacity:1; transform: translateY(0); }
  exit  100% { opacity:0; transform: translateY(-60px); }
}
.fly-item {
  animation: linear fly-in-out both;
  animation-timeline: view();
}
/* JS 降级版：
   IntersectionObserver + 监听 isIntersecting 分别加 .entered / .exited class */
```
**适用类型**：功能列表、时间轴、团队成员行、价格表行、任何垂直列表型 section

---

### 【T-72】SVG 路径运动（Motion Path Along SVG）
**来源参考**：GSAP MotionPath Plugin、CSS `offset-path` 原生规范（Chrome/Firefox 已支持）
**效果**：元素沿预定义 SVG 路径运动（如曲线、波浪、螺旋），可用于装饰性动画或引导视线
**CSS/JS 实现**：
```css
/* 纯 CSS offset-path 版 */
.motion-element {
  offset-path: path('M 0,100 C 50,0 150,200 200,100 S 350,0 400,100');
  animation: move-along 3s linear infinite;
}
@keyframes move-along {
  from { offset-distance: 0%; }
  to   { offset-distance: 100%; }
}
/* JS 控制版（滚动驱动）：
window.addEventListener('scroll', () => {
  const p = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  el.style.offsetDistance = (p * 100) + '%';
}); */
```
**适用类型**：品牌叙事页路线图、产品流程可视化、装饰性飞行元素、游戏路径引导

---

### 【T-73】Grid 中心扩散 Stagger（Grid Center Stagger Reveal）
**来源参考**：anime.js stagger grid demo、Awwwards 2024-25 点阵/网格动画
**效果**：一组网格元素以网格中心为起点向外扩散依次入场（或收缩消失），比线性 stagger 更具震撼的空间感
**JS 实现**：
```javascript
const grid = [8, 4]; // 列数 × 行数
const items = document.querySelectorAll('.grid-item');
const center = [Math.floor(grid[0]/2), Math.floor(grid[1]/2)];
items.forEach((el, i) => {
  const col = i % grid[0];
  const row = Math.floor(i / grid[0]);
  const dist = Math.sqrt(Math.pow(col - center[0], 2) + Math.pow(row - center[1], 2));
  el.style.transitionDelay = dist * 60 + 'ms';
  el.style.opacity = '0';
  el.style.transform = 'scale(0.5)';
});
// IntersectionObserver 触发：
observer.observe(container);
// callback：items.forEach(el => { el.style.opacity='1'; el.style.transform='scale(1)'; });
/* CSS: .grid-item { transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.34,1.56,0.64,1); } */
```
**适用类型**：功能图标网格、Logo 墙、NFT 画廊缩略图、Bento Grid 入场、作品集预览网格

---

### 【T-74】Skeleton 骨架屏扫光（Skeleton Shimmer Loading）
**来源参考**：Motion.dev Skeleton Shimmer Example、Facebook/LinkedIn 加载态、众多 SaaS Dashboard
**效果**：内容加载中显示灰色占位块，上面有从左到右扫过的渐变光泽动画，加载完成后内容淡入替换
**CSS 实现**：
```css
.skeleton {
  background: linear-gradient(90deg,
    var(--skeleton-base, #e0e0e0) 25%,
    var(--skeleton-shine, #f5f5f5) 50%,
    var(--skeleton-base, #e0e0e0) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}
@keyframes shimmer {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}
/* 暗色版：--skeleton-base: #2a2a2a; --skeleton-shine: #3a3a3a; */
/* JS：数据加载完成后 el.classList.remove('skeleton') 并 fadeIn 真实内容 */
```
**适用类型**：SaaS Dashboard、数据分析页、内容平台、任何有异步加载内容的页面

---

### 【T-75】Toast 堆叠通知（Stacked Toast Notifications）
**来源参考**：Motion.dev Toast Stack Example、Vercel/Linear 通知系统、Radix UI Toast
**效果**：多条通知出现时后面的通知缩小/压缩堆在下方（scale + translateY），最新通知在最上层；关闭时有弹出退场；超出数量后自动清除最旧的一条
**JS/CSS 实现**：
```javascript
const toasts = [];
function addToast(msg) {
  const el = document.createElement('div');
  el.className = 'toast'; el.textContent = msg;
  document.querySelector('.toast-container').prepend(el);
  toasts.unshift(el);
  if (toasts.length > 3) { const old = toasts.pop(); animateOut(old, () => old.remove()); }
  toasts.forEach((t, i) => {
    t.style.transform = `translateY(${i * 8}px) scale(${1 - i * 0.05})`;
    t.style.zIndex = 100 - i;
    t.style.opacity = i < 3 ? 1 - i * 0.15 : 0;
  });
  setTimeout(() => animateOut(el, () => el.remove()), 4000);
}
/* CSS: .toast { position:fixed; bottom:24px; right:24px; min-width:280px; padding:16px;
   background:var(--bg); border:1px solid rgba(255,255,255,0.1); border-radius:8px;
   transition: transform 0.4s cubic-bezier(0.16,1,0.3,1), opacity 0.3s; } */
```
**适用类型**：SaaS、开发者工具、电商下单确认、任何有操作反馈的产品——通用微交互组件

---

### 【T-76】PJAX 风格页面过渡（Page Transition Overlay）
**来源参考**：io3000 top tag（277 个日本优质网站使用）、Awwwards 获奖作品页面切换效果
**效果**：点击内部链接时，一个全屏遮罩层从某方向（上/下/左/右/圆心）滑入覆盖页面，然后滑出揭示新内容，比直接跳转有强烈品牌感；单页面内模拟：点击 section 导航时触发
**CSS/JS 实现**：
```javascript
const overlay = document.querySelector('.page-overlay');
document.querySelectorAll('a[data-transition]').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = link.href;
    // Phase 1: 遮罩滑入
    overlay.classList.add('entering');
    overlay.addEventListener('transitionend', () => {
      window.location.href = target;
    }, { once: true });
  });
});
/* 也可用于单页 section 切换：遮罩入→内容切换→遮罩出 */
/* CSS: .page-overlay { position:fixed; inset:0; background:var(--accent); z-index:9999;
   transform: translateY(100%); transition: transform 0.6s cubic-bezier(0.76,0,0.24,1); }
   .page-overlay.entering { transform: translateY(0); }
   .page-overlay.leaving { transform: translateY(-100%); } */
```
**适用类型**：创意机构、作品集、奢侈品牌、游戏官网——任何追求品牌感的页面跳转体验

---

### 【T-77】Pictogram 微动效图标系统（Animated Pictogram Icons）
**来源参考**：io3000 pictogram tag（229 个优质日本网站）、Stripe 功能图标、Linear icon animations
**效果**：SVG 图标不是静止的，hover 或滚动入场时有微动效——描边逐渐绘制、元素弹入、颜色填充、路径变形；每个图标讲述自己的"一句话故事"
**CSS/JS 实现**：
```css
/* 描边绘制式 */
.icon-svg path {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  transition: stroke-dashoffset 0.6s cubic-bezier(0.16,1,0.3,1);
}
.icon-svg:hover path, .icon-svg.active path { stroke-dashoffset: 0; }

/* 弹入式 */
.icon-part { transform: scale(0); transform-origin: center;
  transition: transform 0.4s cubic-bezier(0.34,1.56,0.64,1); }
.icon-svg:hover .icon-part, .icon-svg.active .icon-part { transform: scale(1); }
/* stagger：nth-child(n) 增加 transition-delay */

/* 颜色填充式 */
.icon-fill { fill: transparent; transition: fill 0.3s ease; }
.icon-svg:hover .icon-fill { fill: var(--accent); }
```
**适用类型**：SaaS 功能区、企业服务列表、产品特性说明、开发者工具——任何有图标的功能展示区

---

### 【T-78】CSS 波浪形状分割（Wave Shape Divider）
**来源参考**：io3000 wave tag（94 个优质网站）、Awwwards 有机形状趋势 2024-25
**效果**：Section 之间用 SVG 或 CSS clip-path 波浪曲线分割，替代直线分割；波浪可静态或有缓慢漂移动画；多层波浪叠加产生海浪感
**CSS 实现**：
```css
/* SVG 波浪分割线 */
.wave-divider { position:relative; }
.wave-divider::after {
  content:''; display:block; position:absolute; bottom:-1px; left:0; right:0; height:60px;
  background: var(--next-section-bg);
  clip-path: ellipse(55% 100% at 50% 100%);
}
/* 多层动态波浪背景 */
.wave-bg::before, .wave-bg::after {
  content:''; position:absolute; bottom:0; left:-50%; width:200%; height:120px;
  background: rgba(255,255,255,0.05);
  border-radius: 50% 50% 0 0;
  animation: wave-drift 6s ease-in-out infinite;
}
.wave-bg::after { animation-delay:-3s; opacity:0.5; }
@keyframes wave-drift {
  0%, 100% { transform: translateX(0) scaleY(1); }
  50%       { transform: translateX(5%) scaleY(0.8); }
}
```
**适用类型**：wellness/健康、咖啡/食品、旅游、儿童教育、任何需要"柔和过渡"的品牌

---

### 【T-79】圆形构成布局（Circle-based Layout）
**来源参考**：io3000 circle tag（99 个优质网站）、Awwwards 几何极简趋势
**效果**：以圆形作为核心设计语言——圆形头像/产品图、圆形 CTA 按钮、圆形进度环、圆形背景装饰；hover 时圆形扩散/收缩；多个圆形形成构成感布局
**CSS 实现**：
```css
/* 圆形图片 hover 扩散 */
.circle-img { border-radius:50%; overflow:hidden; transition: transform 0.4s cubic-bezier(0.34,1.56,0.64,1); }
.circle-img:hover { transform: scale(1.06); }

/* 圆形 CTA 大按钮 */
.circle-cta { width:120px; height:120px; border-radius:50%; display:flex; align-items:center;
  justify-content:center; text-align:center; font-size:12px; letter-spacing:0.1em;
  border: 1px solid currentColor; transition: all 0.3s ease; }
.circle-cta:hover { background: var(--accent); color: var(--bg); transform: scale(1.05); }

/* 圆形进度环 */
.progress-ring circle {
  stroke-dasharray: 314; /* 2π×50 */
  stroke-dashoffset: calc(314 - 314 * var(--progress));
  transition: stroke-dashoffset 1.2s cubic-bezier(0.16,1,0.3,1);
  transform-origin: center; transform: rotate(-90deg);
}
```
**适用类型**：作品集、时尚/美妆、wellness、设计工作室、摄影师——追求"精致圆润"气质的品牌

---

### 【T-80】背景纹理/图案叠加（CSS Pattern Texture Overlay）
**来源参考**：io3000 texture/pattern tag（各 179/119 个网站）、Awwwards 2025 材质感趋势、Stripe 背景处理
**效果**：用纯 CSS 生成背景纹理——点阵、网格、斜线、噪点（SVG feTurbulence）、纸张感，作为 section 背景叠加，增加"材质感"而非纯色背景
**CSS 实现**：
```css
/* 点阵纹理 */
.dot-pattern { background-image: radial-gradient(rgba(255,255,255,0.15) 1px, transparent 1px);
  background-size: 24px 24px; }

/* 细网格线 */
.grid-pattern { background-image:
  linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
  linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
  background-size: 40px 40px; }

/* 45度斜线 */
.stripe-pattern { background-image: repeating-linear-gradient(
  45deg, transparent, transparent 4px,
  rgba(255,255,255,0.04) 4px, rgba(255,255,255,0.04) 5px); }

/* SVG 噪点（比 CSS filter:grainy 更精确）*/
.noise-overlay::after { content:''; position:absolute; inset:0; opacity:0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  pointer-events:none; }
```
**适用类型**：科技/开发者工具（网格）、奢侈品（噪点）、复古品牌（斜线）、日系设计（点阵）——通用质感提升

---

