# 生成流程指令

> **核心原则**：每条输出必须有一个从真实获奖/精选作品中提取的核心创意手法作为"设计锚点"，用纯 HTML/CSS/JS 在工具限制内最大程度复现。
> **Prompt 必须像产品PRD**：具体到精确 CSS 数值、三态交互文档（Normal/Hover/Active）、布局系统表、组件清单、动画时序表。禁止模糊描述，越复杂越好。
> **字数底线**：全篇 Prompt **总字符数 ≥ 5500**（安全线）；优秀区间 8000~12000；< 4000 字符铁定不通过。每一轮单独计算有效内容 **≥ 900 词**（中文按字符数，英文/代码按空格分词）。两项都必须满足，总量优先。
> **防凑字禁令**：以下内容**不计入有效字数**，出现即视为劣质 Prompt 必须重写——
> - 重复上一轮已写过的内容（即使换了说法）
> - 空洞评价词（"高质量"/"现代感"/"优雅"/"简洁"/"流畅"等无信息量形容词单独出现）
> - 宽泛指令（"添加适当的动画"/"注意颜色搭配"/"确保响应式"等未给具体参数的句子）
> - 结构框架标题行本身（如"## Hero区域"单独占一行，不含实质内容）
> **合格字数 = 总字符数 - 以上无效内容估算字符数 ≥ 900**。写不够宁可继续展开某个组件的三态细节、写出具体的 CSS 数值区间、列出 JS 逻辑伪代码，而不是堆砌形容词。
> **创意优先**：强烈追求趣味性和个性化风格（手绘/赛博朋克/废土/卡通/霓虹等）。现代功能风格不应是默认选择，除非品牌气质明确需要。
> Prompt 风格为指令式，具体、有设计指导性，**四轮递进**（结构→功能交互→响应式→打磨验收），不拟人化叙述。

---

## 强制步骤 0：读取获奖作品创意技法

**每次生成前，必须从下方"可复现技法库"中选取 1 个主技法 + 2 个辅技法（A+B），写入确认卡，并在 Prompt 三轮中体现。**

选取原则：
- 主技法决定这个页面的**核心差异化记忆点**（视觉上最抢眼的那一个）
- 辅技法 A（视觉/排版/背景维度）强化整体质感
- 辅技法 B（交互/物理/动效维度）承担趣味互动或触感强化
- A 和 B 必须来自不同技法分类，且不能与主技法功能重叠
- 同一主技法不能在连续 3 条中重复使用

---

## 可复现技法库

> **来源**：Awwwards SOTD/SOTY / Godly / Codrops Tympanus / Olivier Larose / Land-book / freefrontend / CSS-Tricks / Smashing Magazine
> **原则**：所有技法均可用纯 HTML + CSS + Vanilla JS 实现，无需 WebGL/Three.js
> **总数**：T-01 到 T-68，共 68 个技法，覆盖交互、排版、背景、导航、滚动五大维度

**分类速查（选技法时参考）**：
- **排版/文字**：T-01 T-02 T-11 T-18 T-25 T-29 T-33 T-36 T-40 T-46 T-56 T-64 T-65 T-66
- **鼠标/光标交互**：T-03 T-07 T-08 T-16 T-17 T-19 T-28 T-35 T-39 T-43 T-51 T-52 T-53 T-59
- **滚动/视差**：T-04 T-06 T-12 T-24 T-30 T-31 T-34 T-37 T-44 T-58 T-60 T-61 T-62
- **背景/纹理/Canvas**：T-09 T-21 T-41 T-45 T-49 T-54
- **SVG/形状变换**：T-05 T-14 T-20 T-23 T-26 T-32
- **页面结构/UI组件**：T-10 T-13 T-15 T-22 T-27 T-38 T-42 T-47 T-48 T-55 T-57 T-63 T-67 T-68

> **总数**：T-01 到 T-68，共 68 个技法，覆盖交互、排版、背景、导航、滚动五大维度

**光标技法变体一览（连续5条内不得使用同一变体）**：
| 变体代码 | 技法 | 外观描述 | 适用气质 |
|---------|------|---------|---------|
| CUR-A | T-28 dot+ring | 8px实心点 + 30px圆圈，lerp跟随 | 通用精致感 |
| CUR-B | T-07 blend | 实心圆 mix-blend-mode:difference 反色 | 暗色页/艺术感 |
| CUR-C | T-51 crosshair | 全屏十字准星线 | 工业/精密/设计工具 |
| CUR-D | T-52 orbit | 旋转文字圆轨 | 创意机构/奢侈品 |
| CUR-E | T-53 ghost | 6环残影彗星尾 | 游戏/速度/科技 |
| CUR-F | T-39 glow | 400px环境光晕（无自定义形状） | 暗色AI/SaaS |
| CUR-G | T-43 particles | Canvas 粒子拖尾 | 游戏/NFT/魔法感 |
| CUR-X | 无自定义光标 | 原生光标，用极致三态hover代替 | 极简/内容优先品牌 |

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

## 多样性核心约束（全局生效）

**禁止在连续作品中重复的元素（任意5条内最多出现1次）**：
- 交互：scroll reveal fade-up（作为主要动效）
- 结构：Hero + Bento Grid + Stats Bar + Preorder 固定四段式
- 组件：视频播放 modal、星级评分、订阅输入框（不能同时出现在一条）
- 字体：Bebas Neue（连续2条内不重复）

**主技法多样性约束**：
- 同一技法编号不能在连续 3 条中作为主技法使用
- 连续 5 条内主技法的分类（排版/鼠标/滚动/背景/SVG/组件）不能全部相同
- T-16 图片拖尾 + T-17 聚光灯揭示 不能在同一条同时使用（竞争焦点）

**🚨 光标冷却系统（严格执行）**：
> 用户反馈：dot+ring 圆圈光标已在超过10个网页中出现，必须强制轮换

- 每条网页**必须**在确认卡中声明光标变体代码（CUR-A 到 CUR-X）
- **CUR-A（dot+ring lerp）连续3条内最多使用1次**——这是最核心规则
- 所有光标变体（CUR-A 到 CUR-G）在任意**5条内不得重复同一变体**
- CUR-X（无自定义光标）也是合法选择，适合极简/文字优先品牌
- 同一条中不能同时使用两种光标技法（T-28 + T-07、T-43 + T-52 等）
- **生成前检查**：last 5 条用了哪些光标变体，挑一个没用过的

**确认卡中光标变体声明格式**（强制新增字段）：
```
光标变体：CUR-C（T-51 全屏十字准星）
```

---

## 组件大类冷却系统（Component Rotation）

> **核心规则**：同一大类的组件，**连续 3 条内最多出现 1 次**。生成前必须对照已用记录选择。
> 组件冷却在确认卡中声明，HTML 生成时严格执行。

| 大类代码 | 大类名称 | 包含的具体组件（任选其一） |
|---------|---------|------------------------|
| C-A | 数字/数据展示 | 计数器动画 / 实时Ticker / 圆环SVG进度 / 柱状图/折线图 / 数字翻牌 |
| C-B | 内容展开 | FAQ手风琴 / Tab切换面板 / 粘滞卡片叠层(T-12) / 侧边详情抽屉 / 步骤向导 |
| C-C | 弹出覆盖 | 居中Modal / 全屏覆盖 / 侧滑面板 / Bottom Sheet / Tooltip延展卡片 |
| C-D | 图片/媒体展示 | Bento网格 / 图片轮播 / 灯箱放大(T-38) / 水平拖拽轨道 / 马赛克悬停揭示 |
| C-E | 表单/输入 | 预订/注册表单 / 价格拨动器 / 多步骤向导 / 实时验证 / 搜索输入+过滤 |
| C-F | 导航形态 | 汉堡全屏菜单 / SPA侧边导航 / Tab顶部栏 / 浮动球导航 / 全屏叠加导航 |
| C-G | 趣味互动 | Canvas涂鸦板 / 拖拽排序(T-47) / 物理弹跳(T-42) / 分屏对比滑块 / 实时颜色主题切换 / 均衡器可视化(T-48) |

**使用规则细则**：
- 每页必须使用 **≥ 3 个大类**（不能只用 C-A + C-B + C-C 固定组合）
- C-G 趣味互动层：每页 **≥ 1 次**，鼓励 2 次
- C-A 数字展示：连续 3 条内最多 1 次（打破"每页必有计数器"惯例）
- C-F 导航形态：连续 3 条内最多 1 次，且每次必须选**不同的导航形态**
- 连续 5 条内 C-G 的具体组件不得重复（拖拽排序用过就换Canvas涂鸦）

**在确认卡中声明格式**：
```
组件选用：
  C-A 数字展示 → 圆环SVG进度图
  C-C 弹出覆盖 → 侧滑面板
  C-F 导航形态 → Tab顶部栏（SPA）
  C-G 趣味互动 → 分屏对比滑块 + 物理弹跳按钮
```

---

## 🃏 W码 — Wild Card 创意互动（每条强制 ≥ 2 个，且必须新颖）

> **核心规则（2026强制版）**：每条网页必须包含 **≥ 2 个** 完全不在 T-01~T-60 技法库和 C-G 组件系统内的大型互动创意。这是本系统持续扩张创意边界的引擎。
>
> **🚨 新颖性强制约束**：
> - 两个W码必须来自**不同大类**（见下方大类分组）
> - **两个W码都必须在 `logs/used_types.json` 的历史记录中从未出现过**（无论全局历史，不只看近10条）
> - 已出现过的W码原则上禁止重复使用；若实在难以凑齐，须自行发明W-NEW替代（自行发明优先级最高）
> - 鼓励每次自行发明W-NEW（无编号的全新互动概念），无编号新发明在确认卡中写 `W-NEW: 互动名称`
>
> **W码互动必须占据页面中一个明显可见的独立区域，不能藏在折叠或 modal 里。**
> **每个W码互动区域高度 ≥ 50vh，是页面的核心内容之一，不是装饰性附件。**

**W码互动的定义标准**：
- 用户需要主动参与（点击 / 拖拽 / 输入 / 键盘），而不是被动观看动画
- 有状态变化（数据更新 / 视觉变形 / 音效 / 随机结果）
- 与品牌内容相关，不是为了加互动而加
- **实现复杂度 ≥ 50行JS**（确保是真正的大型互动，不是美化过的简单切换）

**W码大类分组（两个W码必须来自不同大类）**：
| 大类 | 包含W码 | 核心形式 |
|------|---------|---------|
| 🎮 游戏类 | W-06 W-07 W-09 W-13 W-16 W-17 W-24 W-25 | 有规则/得分/状态机 |
| 🧪 探索/测试类 | W-01 W-12 W-14 W-18 W-19 W-26 | 用户输入→结果反馈 |
| 🛠 工具/创作类 | W-02 W-03 W-04 W-08 W-10 W-15 W-20 W-21 | 实时操控→可见变化 |
| 🎭 沉浸/叙事类 | W-05 W-11 W-22 W-23 W-27 W-28 W-29 W-30 | 视觉/物理/空间感知 |

**种子灵感池（W-01 ~ W-30，每次生成可从此选取，但强烈鼓励自行发明）**：

| W码 | 互动名称 | 实现思路 | 适配气质 |
|-----|---------|---------|---------|
| W-01 | 人格测试/选择题 | 多步骤选项，JS记录选择，最终输出品牌相关"结果卡" | App/wellness/娱乐 |
| W-02 | 虚拟调色台 | 多个滑块/色轮实时更新页面配色方案，可"保存"截图 | 设计工具/时尚 |
| W-03 | 代码终端模拟器 | 可输入命令的假终端，预设响应内容（help/about/etc） | 开发者工具/黑客松 |
| W-04 | 文字生成器 | 输入词语实时生成品牌相关随机句子/诗歌/口号 | AI/创意/文学 |
| W-05 | 3D旋转产品展示 | CSS perspective鼠标拖拽旋转模型（纯CSS 3D，无Three.js） | 电商/硬件/球鞋 |
| W-06 | 投票/实时排行 | localStorage模拟实时投票，每次刷新随机涨跌 | 游戏/音乐/社区 |
| W-07 | 摩斯密码解码器 | 点击按钮发送·-，实时显示解码字母，满足条件触发彩蛋 | 游戏/密室/科技 |
| W-08 | 噪音合成器 | 多个旋钮（`<input range>`）控制CSS动画频率/振幅，视觉+伪音效 | 音乐/电子/SaaS |
| W-09 | 记忆翻牌游戏 | 品牌相关图标的配对记忆游戏，计时+步数 | 儿童/教育/游戏 |
| W-10 | 拖拽配色板 | 将色块拖入"品牌搭配区"，自动计算对比度并给出评分 | 设计工具/时尚 |
| W-11 | 字体大小响应鼠标距离 | 标题字符随鼠标靠近而膨胀，形成3D凸出效果（非repulsion） | 创意机构/奢侈品 |
| W-12 | 实时天气/时间主题切换 | 根据本地时间/随机天气状态切换背景色调+文案 | 旅游/餐饮/outdoor |
| W-13 | 积木搭建器 | 点击添加CSS方块，可自由拼搭，有重力坠落动效 | 儿童/游戏/创意 |
| W-14 | 打字机互动速度测试 | 用户复现品牌口号，实时高亮已打字符，完成有奖励动画 | 开发者/教育/SaaS |
| W-15 | 镜像涂鸦 | Canvas涂鸦自动镜像（4轴对称），可导出 | 艺术/设计/手工 |
| W-16 | 反应力测试 | 随机倒计时后高亮按钮，测试用户点击反应速度ms，排行榜 | 游戏/运动/健身 |
| W-17 | 单词Wordle克隆 | 品牌相关词汇猜词游戏，颜色反馈提示正确/位置/错误 | 文化/娱乐/教育 |
| W-18 | 知识问答Quiz | 品牌/行业相关问答，分数动画，错误答案显示知识卡 | 教育/媒体/旅游 |
| W-19 | 滑动价值偏好调研 | 多维度滑块输入用户偏好，实时生成个性化推荐结果卡 | SaaS/wellness/金融 |
| W-20 | SVG路径编辑器 | 可拖拽控制点的贝塞尔曲线编辑，实时展示品牌Logo变形 | 设计工具/创意机构 |
| W-21 | 实时代码预览器 | 左侧编辑简单CSS，右侧实时渲染预览，预设几个有趣snippet | 开发者工具/教育 |
| W-22 | 目的地悬停切换器 | 悬停左侧列表项→右侧全屏图片淡入，点击确认加入行程 | 旅游/酒店/体验 |
| W-23 | 行程/愿望清单构建器 | 点选项目加入汇总面板，总计天数/费用，一键"发送请求" | 旅游/活动/产品定制 |
| W-24 | 弹弓物理小游戏 | Canvas弹弓发射，命中目标得分，有物理弹跳+重力 | 游戏/运动/品牌活动 |
| W-25 | 贪吃蛇/打砖块迷你版 | Canvas mini game，品牌元素替换经典方块/食物图案 | 游戏/怀旧/趣味品牌 |
| W-26 | 星座/MBTI性格匹配 | 选择性格标签，输出与品牌匹配的角色类型+个性化文案 | App/娱乐/社区 |
| W-27 | 悬停目标跟踪器 | 多个运动中的目标（品牌关键词），用户光标"狩猎"命中高亮 | 游戏/科技/狩猎感品牌 |
| W-28 | 产品配置计算器 | 选配件/功能 → 实时更新价格+3D产品图层（CSS层叠变化） | 电商/硬件/定制产品 |
| W-29 | 情绪色彩映射 | 根据用户点击的色块"情绪"，实时生成个性化品牌故事段落 | wellness/艺术/AI品牌 |
| W-30 | 光标绘制星座 | 鼠标在黑色画布上移动留下星点，停止1s后连线成星座图案 | 天文/奢侈品/神秘感品牌 |

**W码在确认卡中的声明格式（2个，必须来自不同大类）**：
```
Wild Card 1：W-03 代码终端模拟器 [🛠工具类] — 可输入 help/status/deploy 命令，deploy触发品牌动画
Wild Card 2：W-09 记忆翻牌游戏 [🎮游戏类] — 品牌图标配对，计时+3步骤难度选择
```

**W码强制求新规则（取代原冷却机制）**：
- **无冷却窗口概念**——改为全局历史去重：已出现过的W码（无论第几条）原则上不得重复
- 相同互动概念换品牌包装**不算新互动**（W-09记忆游戏就是W-09，换主题也禁止重用）
- 生成前必须检查 `used_types.json` 的 `wild_card` **全部历史记录**，确认两个W码均从未出现
- 若W-01~W-30种子池已耗尽或不满足条件，**必须自行发明W-NEW**，在prompt中详细描述实现思路（≥100字）
- W-NEW 鼓励程度 > 种子池已有W码，每次优先考虑发明全新互动形态

---

**每次生成必须自问**：
1. 主技法（T-xx）在视觉上是否真的是这个页面的"第一记忆点"？
2. 这个设计的区块顺序和组合，和上5条有没有本质区别？
3. 如果截一张 Hero 区的图放到 Godly，会被收录吗？
4. 技法是服务于品牌气质的，还是为了"加技法"而加？
5. **Wild Card 是否有 ≥ 2 个？两个是否来自不同大类？**
6. **两个W码是否都在 used_types.json 全局历史中从未出现过？若任意一个出现过，必须改成W-NEW自行发明。**
7. **动画系统是否完整？是否包含 btn-flash/btn-shake/ripple-expand/card-bounce/glow-pulse 这5类？**
8. **排版是否有艺术性？Hero是否跳出"居中大标题+副文案"的平庸布局？有无不规则几何/3D层叠/多层叠加等手法？**
9. **所有组件hover是否都有"位置+尺寸+颜色"三维度联动？有无 :active 弹跳态？**

---

## P 风格人格系统（Style Personality Code）

> 每条网页必须选取一个 P 码作为"视觉人格锚点"，决定整体审美气质（配色逻辑、字体选择、装饰元素风格）。
> P 码同样受冷却限制：连续 3 条内同一 P 码不可重复。记录在 `logs/used_types.json` 的 `style_personality` 字段。

| P码 | 风格名称 | 关键词 | 最适配主技法 | 适配页面类型 |
|-----|--------|--------|------------|------------|
| P01 | 手绘涂鸦 | 手绘笔触、素描线条、蜡笔色调、涂鸦字体 | T-41 T-45 T-09 | 儿童教育、创意工作室、有机食品、博客 |
| P02 | 卡通插画 | 扁平插画、圆润造型、高饱和配色、活泼动效 | T-42 T-50 T-20 | App推广、儿童/青少年品牌、游戏休闲 |
| P03 | 赛博朋克 | 霓虹色差、故障艺术、网格线条、暗黑底色 | T-49 T-43 T-21 | 游戏、NFT/Web3、黑客松、科技品牌 |
| P04 | 霓虹蒸汽波 | 渐变粉紫、复古霓虹灯管、荧光色、合成器质感 | T-32 T-43 T-48 | 音乐/娱乐、派对、80s复古品牌 |
| P05 | 废土末日 | 锈迹纹理、哑光土黄、破损感、工业字体 | T-49 T-09 T-05 | 户外/生存品牌、游戏、极限运动 |
| P06 | 像素8-bit | 像素字体、格子纹理、低分辨率色块、像素动画 | T-02 T-50 T-21 | 游戏怀旧、开发者工具、独立项目 |
| P07 | 孟菲斯撞色 | 几何拼贴、强对比配色、随机图案、无衬线粗体 | T-07 T-26 T-50 | 创意机构、潮流品牌、活动/发布会 |
| P08 | 复古印刷 | 哑光纸感、衬线体、限制色版印刷质感、复古插图 | T-09 T-05 T-33 | 咖啡/食品、出版、精酿啤酒、工匠品牌 |
| P09 | Y2K千禧 | 镀铬金属、塑料质感、泡泡字体、银色渐变 | T-35 T-43 T-32 | 时尚品牌、App推广、潮流电商 |
| P10 | 故障艺术 | RGB分离、数字噪点、扭曲切片、闪烁动效 | T-49 T-02 T-46 | 赛博/暗黑品牌、音乐、NFT艺术 |
| P11 | Art Deco | 对称几何、金色线条、棱角装饰、衬线优雅 | T-23 T-33 T-05 | 奢侈品、高端餐厅、珠宝、金融 |
| P12 | 暗黑哥特 | 深紫/墨黑、哥特字体、蜘蛛网纹样、血红强调 | T-17 T-49 T-43 | 密室逃脱、游戏、纹身/暗黑文化 |
| P13 | 迷幻解构 | 扭曲排版、混乱网格、超现实主义、非线性布局 | T-18 T-46 T-26 | 艺术项目、概念设计、创意机构 |
| P14 | 自然有机 | 大地色系、流体形状、植物纹理、手写体 | T-09 T-41 T-40 | Wellness、有机食品、环保品牌 |
| P15 | 极简禅风 | 大量留白、单一强调色、极细线条、汉字美学 | T-40 T-13 T-01 | 高端餐厅、日系品牌、冥想/SPA |
| P16 | 现代功能风 | 清晰网格、系统色板、精密排版、功能优先 | T-29 T-21 T-10 | SaaS、开发者工具、数据平台 |
| **奇幻 / 超自然** |||||
| P17 | 克苏鲁深渊 | 触手纹理、深海墨绿、扭曲几何、不可名状感 | T-17 T-49 T-46 | 恐怖游戏、TRPG、暗黑文化 |
| P18 | 史诗奇幻 | 羊皮纸质感、金色纹章、哥特衬线、中世纪地图 | T-09 T-33 T-23 | 游戏官网、奇幻小说、桌游 |
| P19 | 暗黑奇幻 | 深紫雾气、骷髅装饰、锈铁色、暗焰橙 | T-17 T-43 T-49 | 暗黑游戏、哥特品牌、纹身工作室 |
| P20 | 蒸汽朋克 | 黄铜齿轮、维多利亚衬线、旧地图色调、铆钉装饰 | T-35 T-09 T-05 | 机械品牌、复古游戏、钟表 |
| P21 | 生物朋克 | 有机绿+脉络纹、DNA螺旋、半透明膜质感、荧光体液 | T-40 T-43 T-46 | 生物科技、医疗创新、基因品牌 |
| P22 | 柴油朋克 | 工业灰+铁锈橙、重型机械、粗粝金属、战争海报风 | T-05 T-49 T-09 | 军事游戏、工业品牌、极限运动 |
| P23 | 原子朋克 | 50年代原子时代配色、射线标志、圆润复古未来造型 | T-35 T-32 T-50 | 复古未来、核能主题、怀旧游戏 |
| P24 | 太阳朋克 | 翠绿+暖金、藤蔓纹理、可持续图标、阳光渐变 | T-40 T-14 T-09 | 环保品牌、可持续设计、绿色科技 |
| P25 | 海洋朋克 | 深蓝+铜绿、贝壳纹理、潜水面罩、生锈船体 | T-17 T-40 T-05 | 海洋探索、潜水品牌、航海 |
| P26 | 洛夫克拉夫特 | 墨黑+暗紫、古籍字体、星图纹样、非欧几何 | T-17 T-46 T-18 | 神秘学、恐怖文学、密室逃脱 |
| P27 | 深海恐怖 | 极深蓝黑、生物发光点、水压感渐变、气泡粒子 | T-17 T-43 T-14 | 深海探索、恐怖游戏、海洋科研 |
| P28 | 都市奇幻 | 霓虹+魔法符文、城市夜景+超自然元素混搭 | T-43 T-49 T-21 | 都市奇幻游戏、现代魔法品牌 |
| P29 | 闪光朋克 | 金属亮片+宝石色、华丽衬线、disco光球、棱镜折射 | T-32 T-35 T-23 | 时尚品牌、派对、珠宝、演出 |
| **童话 / 梦幻** |||||
| P30 | 童话仙境 | 柔粉+丁香紫、花体字、蕾丝边框、星尘粒子 | T-41 T-14 T-50 | 儿童品牌、婚礼、甜品店 |
| P31 | 糖果甜美 | 高饱和糖果色、圆润字体、气泡装饰、糖霜纹理 | T-42 T-50 T-20 | 甜品品牌、儿童App、美妆 |
| P32 | 魔法少女 | 粉紫渐变、星形+月牙装饰、变身动效、闪光粒子 | T-32 T-43 T-50 | 动漫周边、cosplay、偶像 |
| P33 | 森林精灵 | 苔绿+暖棕、树叶纹理、手写花体、光斑粒子 | T-40 T-09 T-41 | 有机品牌、SPA、自然疗法 |
| P34 | 梦核异境 | 低对比粉雾、模糊边缘、怀旧照片滤镜、超现实场景 | T-18 T-46 T-13 | 艺术项目、音乐、实验品牌 |
| P35 | 粉彩云朵 | 粉+蓝+薰衣草渐变、柔焦光晕、蓬松阴影 | T-14 T-40 T-41 | Wellness、冥想App、母婴品牌 |
| P36 | 迷幻幻觉 | 液态渐变、万花筒对称、hue-rotate循环、莫尔条纹 | T-46 T-32 T-18 | 音乐节、迷幻艺术、创意机构 |
| P37 | 星云宇宙 | 深紫+星云粉、星点粒子、银河渐变、发光雾气 | T-14 T-43 T-17 | 占星、VR体验、宇宙探索 |
| **末世 / 荒野** |||||
| P38 | 废土末世 | 锈橙+哑光军绿、破损纹理、涂鸦字体、弹孔装饰 | T-49 T-05 T-09 | 生存游戏、户外极限、军事 |
| P39 | 核爆荒原 | 辐射黄+焦黑、辐射标志、灰烬粒子、CRT扫描线 | T-49 T-02 T-43 | 末世游戏、科幻品牌 |
| P40 | 赛博废土 | 霓虹残光+锈迹、破碎屏幕、数据噪点+工业废墟 | T-49 T-43 T-05 | 赛博游戏、暗黑科技 |
| P41 | 残骸美学 | 混凝土灰+苔绿、裂缝纹理、废墟照片底图、铁丝网 | T-05 T-09 T-18 | 建筑、摄影、实验艺术 |
| P42 | 熵增美学 | 渐变衰变（色彩从鲜艳到灰）、像素溶解、时间侵蚀感 | T-46 T-49 T-18 | 概念艺术、哲学、实验品牌 |
| **科技 / 未来** |||||
| P43 | 全息科技 | 全息彩虹渐变、透明玻璃层叠、光谱折射、极细线条 | T-35 T-43 T-32 | AI产品、XR/VR、科技发布会 |
| P44 | 矩阵黑客 | 绿色代码雨、终端字体、黑底荧光、代码片段装饰 | T-02 T-43 T-21 | 安全工具、开发者、黑客松 |
| P45 | 量子未来 | 深蓝+青色、粒子连线、波函数可视化、精密网格 | T-14 T-29 T-21 | 量子计算、AI研究、数据平台 |
| P46 | 机甲硬核 | 钛金属灰+警告橙、HUD界面、六角网格、液压线条 | T-29 T-49 T-35 | 机甲游戏、军工品牌、电竞 |
| P47 | 纳米微观 | 极浅蓝灰+荧光点、分子结构、极小粒子、放大镜效果 | T-14 T-43 T-29 | 生物纳米、医疗科技、科研 |
| P48 | 外星文明 | 暗紫+生物绿、象形文字装饰、有机科技混合、异形纹理 | T-17 T-46 T-43 | 外星主题游戏、科幻品牌 |
| **历史 / 传统** |||||
| P49 | 敦煌飞天 | 土红+石青+金箔、飞天纹样、藻井几何、古朴衬线 | T-23 T-09 T-33 | 文创产品、博物馆、中式品牌 |
| P50 | 水墨书法 | 黑白+宣纸底、水墨渐淡、书法字体、印章红点缀 | T-13 T-41 T-40 | 中式茶道、书法品牌、文人空间 |
| P51 | 浮世绘和风 | 靛蓝+朱红+金、浮世绘描边风格、和纸纹理、樱花装饰 | T-07 T-09 T-33 | 日料、日式旅馆、和风文化 |
| P52 | 古埃及神殿 | 金+蓝宝石+沙色、象形文字边框、几何对称、法老装饰 | T-23 T-33 T-05 | 博物馆、珠宝、奢侈品 |
| P53 | 维京符文 | 深铁灰+血红、符文字体、编织纹样、斧头/盾牌图标 | T-17 T-05 T-09 | 游戏、精酿啤酒、户外品牌 |
| P54 | 文艺复兴 | 赭石+暗金、古典衬线、雕塑/穹顶参考、对称构图 | T-33 T-23 T-09 | 美术馆、高端餐厅、葡萄酒 |
| P55 | 巴洛克宫廷 | 金+深红+象牙白、繁复花纹边框、卷叶装饰、优雅衬线 | T-23 T-33 T-05 | 奢侈品、歌剧院、酒店 |
| P56 | 洛可可精致 | 粉+浅蓝+金、贝壳C形曲线装饰、细腻花卉、柔和阴影 | T-41 T-23 T-33 | 香水、甜品、高端美妆 |
| P57 | 波斯纹样 | 青金石蓝+金+玫瑰红、几何星形纹、阿拉伯花纹、拱门 | T-23 T-07 T-33 | 地毯品牌、中东餐厅、旅游 |
| P58 | 拜占庭镶嵌 | 金+深紫+猩红、马赛克拼贴纹理、十字/圆拱、厚重阴影 | T-07 T-23 T-33 | 宗教艺术、博物馆、高端酒店 |
| **年代 / 流行文化** |||||
| P59 | 80年代霓虹 | 粉+电蓝+铬银、合成器网格、夕阳渐变、粗体无衬线 | T-32 T-43 T-48 | 音乐/DJ、复古派对、电子品牌 |
| P60 | 70年代复古 | 橙+棕+芥末黄、圆角、花朵图案、粗衬线字体 | T-09 T-50 T-05 | 复古服饰、家居、黑胶唱片 |
| P61 | 60年代嬉皮 | 彩虹扎染渐变、和平符号、迷幻字体、波浪线条 | T-46 T-32 T-18 | 音乐节、波西米亚品牌、艺术 |
| P62 | VHS胶片感 | 彩色噪点+扫描线、模糊色溢出、失真字体、时间码 | T-49 T-02 T-48 | 摄影、独立电影、怀旧品牌 |
| P63 | 像素街机 | 8-bit色板、像素字体、CRT弯曲、街机按钮造型 | T-02 T-50 T-21 | 游戏怀旧、独立游戏、电竞 |
| P64 | 贝壳机Y2K | 半透明塑料+果冻色、泡泡字体、星星装饰、闪粉渐变 | T-35 T-43 T-32 | 潮流品牌、Z世代、美妆App |
| **自然 / 生态** |||||
| P65 | 极地冰原 | 冰蓝+纯白+银灰、冰晶纹理、极光渐变、几何雪花 | T-14 T-43 T-40 | 户外品牌、环保、北欧旅游 |
| P66 | 珊瑚深海 | 珊瑚橙+海蓝+沙色、水波纹理、气泡粒子、流体曲线 | T-40 T-14 T-17 | 海洋保育、潜水、水族馆 |
| P67 | 沙漠荒原 | 土黄+赭红+天青蓝、沙丘纹理、干裂质感、极简几何 | T-09 T-05 T-40 | 旅游、建筑、户外品牌 |
| P68 | 植物标本 | 米白+暗绿+棕褐、植物线描、标本标签字体、纸质底纹 | T-09 T-41 T-40 | 植物园、有机品牌、自然教育 |
| P69 | 星空天文 | 深黑+星点白+星云蓝紫、星座连线、天文数据字体 | T-14 T-43 T-17 | 天文馆、太空品牌、科普 |
| **奢华 / 精致** |||||
| P70 | 黑金权贵 | 纯黑+金箔纹理、细金线边框、高对比、奢华衬线 | T-23 T-33 T-05 | 金融、奢侈品、高端会所 |
| P71 | 大理石殿堂 | 白色大理石纹理+金脉、古典比例、雕塑参考 | T-33 T-23 T-09 | 建筑事务所、高端酒店、珠宝 |
| P72 | 皮革手工 | 深棕+鞍黄+金扣、皮革纹理、缝线装饰、烫金字体 | T-09 T-05 T-33 | 手工皮具、高端箱包、雪茄 |
| **街头 / 亚文化** |||||
| P73 | 涂鸦街头 | 喷漆色彩、砖墙底纹、涂鸦字体、贴纸装饰、滴漆 | T-41 T-07 T-26 | 街头品牌、滑板、嘻哈 |
| P74 | ZINE独立 | 黑白+荧光粉、打字机字体、撕纸边缘、胶带拼贴 | T-09 T-18 T-26 | 独立杂志、地下音乐、反文化 |
| P75 | 噪音朋克 | 高对比黑白+刺眼红、破碎网格、涂抹字体、粗暴排版 | T-18 T-49 T-26 | 朋克乐队、地下文化、独立品牌 |
| **情绪 / 氛围** |||||
| P76 | 忧郁雾蓝 | 灰蓝+淡紫+雾白、柔焦模糊、极细线条、低饱和度 | T-13 T-40 T-14 | 文学杂志、音乐、心理咨询 |
| P77 | 甜蜜残酷 | 粉红+血红、蕾丝+荆棘、甜美与暴力并存、对比字重 | T-41 T-49 T-18 | 时尚品牌、前卫艺术、独立游戏 |
| P78 | 存在主义 | 灰白+黑+一点暗红、大量留白、哲学引文排版、极简 | T-13 T-01 T-18 | 哲学出版、实验电影、概念品牌 |
| **艺术流派** |||||
| P79 | 达达解构 | 随机拼贴、错位排版、反逻辑色彩、剪切字母 | T-18 T-26 T-46 | 实验艺术、创意机构、前卫品牌 |
| P80 | 超现实主义 | 梦境色调、不合逻辑的尺度、融化/变形元素 | T-46 T-18 T-40 | 艺术展、概念品牌、创意机构 |
| P81 | 构成主义 | 红+黑+白、几何色块、斜线分割、无衬线粗体 | T-07 T-26 T-29 | 设计展、建筑、教育机构 |
| P82 | 立体主义 | 多视角拼合、几何碎片、土色+蓝、折面阴影 | T-07 T-18 T-26 | 艺术画廊、创意品牌、设计事务所 |
| P83 | 点描印象 | 圆点纹理+印象派色调、柔和光感、模糊边缘渐变 | T-14 T-41 T-40 | 艺术展、花店、有机品牌 |
| P84 | 新拟物 | 淡灰+柔和阴影、凹凸投影、柔和渐变、圆润控件 | T-29 T-40 T-10 | App展示、设计工具、Dashboard |
| P85 | 液态渐变 | 多色液态blob、流体渐变背景、模糊玻璃叠层 | T-14 T-40 T-32 | 科技品牌、创意App、音乐 |
| P86 | 低多边形 | 三角面片拼合、facet阴影、线框叠加、渐变面 | T-07 T-14 T-29 | 游戏、3D工具、科技品牌 |

**P 码在确认卡中的格式**：
```
风格人格：P03 赛博朋克 — 霓虹色差 + 故障动效 + 网格线条底纹
```

**P 码多样性约束（硬规则）**：
- 连续 3 条内同一 P 码不可重复
- 连续 5 条内 P16（现代功能风）不超过 1 次——强制追求视觉多样性
- P 码必须与页面类型逻辑匹配（不允许为 SaaS 数据平台强行套用 P01 手绘风格）
- 每 10 条内至少覆盖 3 个不同大类（奇幻/童话/末世/科技/历史/年代/自然/奢华/街头/情绪/艺术/基础16）
- 优先选用 P17+ 新风格，避免前16个被过度使用

---

## 页面架构类型（Architecture Type）

> 每条网页必须在确认卡中声明架构类型，影响 JS 结构设计和导航方式。
> **🚨 A01 单页滚动频率上限：每 10 条最多出现 1 次（≤ 10%）。其余架构类型轮流使用，连续 3 条内不得重复同一 A 码。**

| A码 | 类型名称 | 核心导航机制 | 适配页面类型 |
|-----|--------|------------|------------|
| A01 | 单页滚动 | 传统长滚动，navbar + section id 锚点平滑滚动 | 极少数标准落地页（受限高频） |
| A02 | SPA 多页按钮切换 | JS show/hide 切换，顶部/侧边按钮组导航，每页独立入场 | 作品集、博客、工具套件、App展示 |
| A03 | 交互式单页 | 以大型可操作组件为核心，不依赖滚动叙事 | 小游戏、Canvas工具、物理互动 |
| A04 | 全屏几何过渡SPA | 按钮触发全屏几何动画切换场景：圆形扩展 / 对角线划入 / 幕布分裂 / 墨水扩散 | 创意机构、游戏、奢侈品、NFT |
| A05 | 幻灯片演示模式 | 键盘方向键 + 屏幕箭头翻页，每屏铺满视口，页码指示器，入/出方向动画 | 品牌宣言、活动/演讲、产品发布会 |
| A06 | CSS滚动吸附 | `scroll-snap-type: y mandatory`，每section = 100vh，自然滚动吸附定位，配合进度点导航 | 旅游、故事叙事、产品展示 |
| A07 | 水平轨道SPA | 内容面板横向排列，左右箭头/键盘导航，translateX切换，进度条 | 时间线、产品系列、作品展示 |
| A08 | ~~竖向抽屉推入~~ **🚫 已废弃** | **禁止使用**。sticky 面板 + spacer 的空隙滑窗结构已废弃，截图时产生大片空白且难以调试。替代方案见 A10 / A11 / A12 | 已废弃，不得选用 |
| A09 | 3D翻页书 | CSS perspective + rotateY(-180deg) 模拟书页翻动，前后页同时旋转 | 杂志/出版、咖啡菜单、作品册 |
| A10 | 分屏叙事（Split Narrative） | 视口左右各占50%；左侧内容正常滚动，右侧固定展示对应视觉（JS IntersectionObserver 切换）；或左右同时各自独立滚动 | 产品对比、设计工作室、奢侈品、摄影作品集 |
| A11 | 视觉章节卷轴（Chapter Reveal） | 普通滚动但每个 section 配超强入场过渡：clip-path 揭示 / scale爆炸 / 颜色洪流扩散 / 文字撕裂；章节间无 sticky，纯滚动驱动视觉跃迁 | 品牌叙事、游戏官网、活动页、音乐发行 |
| A12 | 径向中心导航（Radial Hub） | 中央 Hub 图标，6-8 个面板沿圆形分布；点击扇区旋转展开对应面板（rotateZ + scale）；用 CSS perspective 制造深度感 | 创意机构、产品功能矩阵、角色选择 |

---

**各架构技术规范**：

**A02 SPA多页按钮切换**：
- 每个 `.page` 默认 `display:none`，激活页 `display:block`
- 切换动画：旧页 `translateX(0) → translateX(-60px) + opacity:0`，新页 `translateX(60px) + opacity:0 → 正常`，duration 0.45s
- 每个子页面有独立入场动画，active 导航项有明显标记

**A04 全屏几何过渡SPA**：
- 遮罩层 `position:fixed; inset:0; z-index:9999` 做过渡载体
- 圆形扩展：`clip-path: circle(0% at X Y) → circle(150% at X Y)` transition 0.6s
- 对角线划入：`clip-path: polygon(100% 0,100% 0,100% 100%,100% 100%) → polygon(0 0,100% 0,100% 100%,0 100%)`
- 幕布分裂：左右两个 `::before/::after` 各 `scaleX(0→1)` 再 `scaleX(1→0)`
- 颜色取品牌 accent 色或反色，切换完毕后遮罩退场

**A05 幻灯片演示模式**：
- `slides` 容器 `overflow:hidden`，每张 `position:absolute; width:100%; height:100vh`
- 切换方向：→进入 `translateX(100%→0)`，←退出 `translateX(0→-100%)`，支持反向
- 进度指示：右下角 `01 / 05` 格式 + 细线进度条
- 键盘监听：`ArrowRight/ArrowDown` 下一张，`ArrowLeft/ArrowUp` 上一张

**A06 CSS滚动吸附**：
- `html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }`
- 每个 section `scroll-snap-align: start; height: 100vh;`
- 右侧导航点：固定定位，点击 `scrollIntoView({behavior:'smooth'})`，当前section active 点高亮

**A07 水平轨道SPA**：
- `.track-container { overflow:hidden; }` `.track { display:flex; transition: transform 0.5s cubic-bezier(0.77,0,0.175,1); }`
- 每个面板 `min-width:100vw; height:100vh`，currentIndex × 100vw 偏移
- 左右箭头按钮，边界时禁用并灰化

**A08 竖向抽屉推入**：
- 每个区块 `position:sticky; top:0; height:100vh`，堆叠顺序通过 `z-index` 管理
- **z-index 必须升序**：第1面板最低（如 z-index:5），最后一张最高（如 z-index:10）；后入场面板覆盖前一张，切勿倒序
- 后一区块推入时，前一区块 `transform:scale(0.95) translateY(-20px)` + `filter:blur(2px)` 渐出
- 用 IntersectionObserver 触发，threshold: [0, 0.5, 1]
- **Spacer 强制规则（仅 A08/滑窗类页面适用）**：面板之间的 spacer div 高度必须**等于单面板高度（100vh）**，不得随意设置 200~500vh 的大数值；等比 spacer 可保证全屏截图时面板与空隙比例正常，不会出现大片空白
  ```css
  /* 正确：spacer = 面板高度 */
  .drawer-spacer { height: 100vh; }
  /* 如使用 margin-top:-100vh 缩进面板，spacer 仍保持 100vh */
  ```

**A09 3D翻页书**：
- `.book { perspective: 1500px; }` `.page { transform-style: preserve-3d; transition: transform 0.8s cubic-bezier(0.645,0.045,0.355,1.0); }`
- `.front/.back { backface-visibility: hidden; position: absolute; }`
- 翻开：`rotateY(-180deg)`，翻回：`rotateY(0deg)`
- 书脊阴影：`box-shadow: inset -10px 0 30px rgba(0,0,0,0.3)`

**A10 分屏叙事（Split Narrative）**：
- 布局：左右各 `width:50vw; height:100vh`；左侧 `overflow-y:auto`，右侧 `position:fixed; right:0; top:0`
- JS：`IntersectionObserver` 监测左侧各 section（`threshold:0.5`），触发时切换右侧 `data-panel` 对应内容
- 右侧面板切换动画：`clip-path: inset(0 0 100% 0)` → `inset(0 0 0% 0)`，`transition: clip-path 0.6s ease`
- 移动端降级：`@media(max-width:768px){ right-panel: position:static; width:100vw; height:50vh }`
- 右侧内容类型举例：产品大图切换 / 数据可视化切换 / 颜色主题切换 / 3D模型视角切换（CSS perspective）

**A11 视觉章节卷轴（Chapter Reveal）**：
- 纯普通滚动（无 sticky、无 SPA），每个 section 靠强入场动画区分
- 必选4种入场技法之一，且相邻 section 不重复：
  1. `clip-path: polygon(0 0, 100% 0, 100% 0, 0 0)` → `polygon(0 0, 100% 0, 100% 100%, 0 100%)` 揭示
  2. `transform: scale(0.6); filter:blur(20px); opacity:0` → 正常（爆炸式放大）
  3. 背景颜色扩散：`::before { clip-path: circle(0% at 50% 50%) }` → `circle(150% at 50% 50%)`
  4. 文字撕裂：每行 `<span>` 各自从不同方向飞入（奇行左、偶行右）
- `IntersectionObserver` 监测每个 section，进入视口时添加 `.revealed` class 触发动画
- section 最小高度 `min-height: 100vh`，背景不得连续 2 段完全相同

**A12 径向中心导航（Radial Hub）**：
- 布局：`position:fixed; width:100vw; height:100vh; overflow:hidden`，单屏无滚动
- 中央 Hub：`width:120px; height:120px; border-radius:50%` 绝对居中
- 面板分布：6-8 个扇形按钮沿 `conic-gradient` 或 CSS `transform: rotate(Xdeg) translateX(200px)` 分布
- 点击扇区：选中面板 `transform: scale(1) rotateZ(0)` 扩展至全屏，其他面板 `scale(0) rotateZ(180deg)` 收回
- 面板切换动画：`transition: transform 0.5s cubic-bezier(0.34,1.56,0.64,1), opacity 0.4s`
- 深度感：Hub 容器 `perspective: 800px`；面板初始 `rotateX(15deg)`，激活后 `rotateX(0deg)`
- 最少 6 个内容面板，每个面板独立主题/颜色

---

## Step 1：确立设计方向

查阅 `logs/used_types.json`，自主决定本条的网页类型与整体设计方向。

**类型多样性约束（硬规则）：**
- 同一细分网页类型间隔至少 10 条才能重复
- 同一大类（20大类之一）连续不超过 3 条 → 第 4 条强制切换到不同大类
- 每 10 条内至少覆盖 6 个不同大类
- 每 10 条内至少出现 1 次：App客户端界面、游戏/娱乐类、科技/开发者类、创意/作品集类
- SaaS落地页 / 个人作品集 / 企业官网 每 5 条最多 1 次
- 每 10 条内至少出现 1 次非传统落地页类型（App界面、小游戏、交互工具、数据看板、社区平台）

**架构类型频率约束（硬规则）：**
- **A01 单页滚动：每 10 条最多出现 1 次**（上限 10%）——打破"默认长滚动"惯式
- A02～A07 / A09～A12：平等轮用，**连续 3 条内不得重复同一 A 码**（A08 已废弃，不得选用）
- 每 5 条内 A04/A05/A06/A07/A09/A10/A11/A12 至少出现 2 种（强制非标准架构）
- A10/A11/A12 新架构：前 20 条内每种至少出现 1 次（强制推广）
- 在确认卡中必须声明 A 码，格式：`架构：A10 分屏叙事 — 左滚右固定IntersectionObserver`

**完整网页类型库（共20大类，200+细分类型）**：

> 从以下类型库中选取。同一细分类型间隔至少10条才能重复，同一大类连续不超过3条。
> 除「工具/功能型」中的404页面、维护中页面、空状态页面外，所有类型均可选用。

**1. 企业 / 品牌**：
- 企业官网、品牌官网、集团官网、上市公司官网、初创公司官网
- NGO/非营利官网、政府机构官网、大使馆官网

**2. 产品落地页**：
- SaaS落地页、APP落地页、硬件产品落地页、游戏落地页
- 浏览器插件落地页、开源项目落地页、AI产品落地页、API服务落地页

**3. 营销 / 活动**：
- 活动落地页、大促落地页、限时优惠页、预售页、发布会页
- 倒计时页、邀请函页、联名活动页、赞助商页、抽奖活动页

**4. 电商 / 零售**：
- 综合电商首页、品牌独立站、闪购页、产品详情页、购物车页
- 结算页、会员中心页、积分商城页、礼品卡页、二手交易页

**5. 餐饮 / 食品**：
- 豪华餐厅官网、快餐品牌官网、咖啡品牌官网、烘焙品牌官网
- 外卖平台首页、食谱网站、葡萄酒酒庄官网、精酿啤酒官网、食品订阅盒子页

**6. 生活方式 / 消费品**：
- 时尚品牌官网、奢侈品官网、美妆品牌官网、香水品牌官网、家居品牌官网
- 户外运动品牌官网、宠物品牌官网、母婴品牌官网、珠宝品牌官网、眼镜品牌官网

**7. 内容 / 媒体**：
- 新闻资讯网站、博客、个人专栏、播客官网、视频平台
- 纪录片专题页、杂志官网、数字出版平台、订阅通讯页（Newsletter）

**8. 创意 / 作品集**：
- 设计师作品集、摄影师作品集、插画师作品集、导演/摄影师作品集
- 建筑师作品集、音乐人官网、艺术家个人站、3D艺术家展示页、创意工作室官网

**9. 教育 / 学习**：
- 在线课程平台、课程落地页、大学院校官网、培训机构官网、知识付费页
- 题库网站、学习管理系统（LMS）、语言学习平台、儿童教育平台、职业认证页

**10. 医疗 / 健康**：
- 医院官网、诊所官网、医疗SaaS官网、心理健康平台、健康科普网站
- 药品品牌官网、医美机构官网、健康险落地页、营养品牌官网、远程问诊平台

**11. 金融 / 商业服务**：
- 银行官网、数字银行官网、支付产品官网、加密货币/Web3官网、投资平台官网
- 保险产品落地页、会计/财税SaaS官网、律所官网、咨询公司官网、招聘平台官网

**12. 科技 / 开发者**：
- 开发者工具官网、云服务官网、DevOps产品官网、安全产品官网
- 数据分析平台官网、开源社区官网、技术文档站、CLI工具官网、嵌入式/IoT产品官网

**13. 旅游 / 出行**：
- 旅游目的地官网、酒店官网、精品民宿官网、航空公司官网、租车平台官网
- 游轮官网、旅行攻略站、签证服务官网、户外探险预订页

**14. 娱乐 / 游戏**：
- 游戏官网、游戏赛事官网、电竞战队官网、电影/剧集官网、综艺节目官网
- 音乐专辑官网、演唱会售票页、漫画/动画官网、主题公园官网
- 密室逃脱/沉浸式体验官网、独立游戏/Indie Game落地页

**15. 社区 / 平台型**：
- 论坛/社区首页、问答平台、兴趣社群页、会员制社区落地页
- DAO/去中心化社区页、粉丝俱乐部页

**16. 工具 / 功能型页面**：
- ~~404页面~~ ~~维护中页面~~ ~~空状态页面~~（禁用）
- 引导注册/Onboarding页、定价页、比较页（对比竞品）
- 更新日志页（Changelog）、路线图页（Roadmap）、帮助中心/FAQ页、状态监控页（Status Page）
- 交互式小游戏（Canvas + 物理引擎模拟）
- AI工具/生成器界面、数据可视化Dashboard

**17. 公益 / 政务**：
- 慈善募款页、公益项目介绍页、政府服务门户
- 政策宣传页、公共卫生宣传页、选举竞选官网

**18. 个人**：
- 个人主页/简历页、个人品牌官网、婚礼/纪念日页
- 个人博客、数字名片页、独立开发者个人主页（A02 SPA）

**19. App客户端网页界面（模拟真实App UI）**：
> 模拟移动端/桌面端App的Web版界面，不是推广落地页，而是App本身的操作界面。
> 必须包含完整的UI交互：Tab栏/侧边栏导航、列表/卡片内容、播放/操作控件、搜索/筛选等。
> 推荐架构：A02（多页切换）/ A03（交互式单页）/ A07（水平轨道）。

- 音乐播放器App界面（如网易云音乐/Spotify风格：播放条+歌单+发现页+歌词）
- 社交媒体App界面（如Instagram/小红书风格：Feed流+Stories+个人主页+消息）
- 即时通讯App界面（如微信/Telegram风格：聊天列表+对话窗+联系人）
- 短视频App界面（如TikTok/抖音风格：全屏视频卡+侧边操作栏+底部导航）
- 电商App界面（如淘宝/Amazon风格：商品网格+购物车+商品详情+搜索）
- 外卖/餐饮App界面（如美团/Uber Eats风格：餐厅列表+菜单+购物车+地图）
- 地图/导航App界面（如高德/Google Maps风格：地图+搜索+路线+POI详情）
- 天气App界面（如iOS天气风格：天气动画+逐时预报+多日预报+空气质量）
- 笔记/效率App界面（如Notion/Bear风格：侧边栏+编辑器+Markdown渲染）
- 健身/运动App界面（如Keep/Nike Run风格：运动数据+训练计划+社区+记录）
- 阅读器App界面（如Kindle/微信读书风格：书架+阅读页+笔记+目录）
- 金融/银行App界面（如支付宝/Revolut风格：余额卡片+交易列表+转账+理财）
- 相册/摄影App界面（如Google Photos风格：照片网格+相册+编辑+回忆）
- 日历/待办App界面（如Fantastical风格：月/周视图+事件详情+快速添加）
- 播客App界面（如小宇宙/Pocket Casts风格：订阅列表+播放器+发现+搜索）
- 代码编辑器App界面（如VS Code风格：文件树+编辑区+终端+Tab栏）
- 设计工具App界面（如Figma/Canva风格：画布+工具栏+图层面板+属性面板）
- 数据看板App界面（如Grafana/Datadog风格：图表网格+时间选择+告警列表）

**20. 特殊主题**：
- AI角色/虚拟伴侣推广页、线下活动/音乐节官网
- 手工艺/工匠品牌官网、潮流球鞋/时尚品牌落地页
- 暗黑美食/特色餐厅落地页、创意写作/诗歌/艺术杂志页

**设计方向由 Claude 自主判断，参考标准为**：
- 同类型在 Awwwards SOTD / Godly / Dribbble 上什么风格被收录最多？
- 这个品牌的气质、目标用户、情感调性决定什么颜色/字体/节奏是对的？
- 和前 5 条有没有本质的视觉差异（不只是换色换字，而是整体气质不同）？

**设计多样性约束（硬规则）：**
- 整体色调：连续 2 条不能都是深色系，连续 2 条不能都是浅色系
- 主视觉语言：连续 3 条不能同属一种风格（如同是极简留白、同是霓虹暗黑）
- 布局：连续 3 条不能都是 Hero 全屏 + 卡片网格的标准结构
- 字体：Bebas Neue 连续 2 条内不重复；不得连续 3 条都用无衬线 Display 字体

---

## Step 2：构思品牌与核心设计概念

自主创造品牌，输出确认卡：

```
---
类型：[具体网页类型]
架构：[Axx 架构名称] — [一句话说明导航方式/切换动效，如"A04 全屏几何过渡SPA — 按钮触发对角线划入"]
风格人格：[Pxx 风格名称] — [一句话说明视觉人格如何体现]
光标变体：[CUR-X 变体代码] — [说明选择理由]
品牌名：[xxx]
Slogan：[xxx]
核心情绪：[用2-3个形容词描述，如"冷峻 / 精密 / 未来感"]
色彩方向：[自由描述，精确到色值，如"#0A0A0F 深黑底 + #FF2D78 霓虹粉强调 + #E8E8E8 正文"]
布局结构：[自由描述，如"全屏叙事型，左侧固定文字，右侧滚动图像；4列不等宽 Bento Grid"]
字体方向：[Display字体 + Body字体，说明搭配理由，如 "Space Grotesk 标题 + DM Mono 数据 — 科技感配码农质感"]
视觉参考气质：[类比1-2个获奖作品或品牌，如"接近 Lusion 的流体暗黑 + Stripe 的精密排版"]
主技法：[Txx 技法名称] — [一句话说明如何服务这个品牌]
辅技法 A：[Txx 技法名称] — [视觉/排版维度，与主技法分类不同]
辅技法 B：[Txx 技法名称] — [交互/动效维度，与辅A分类不同]
排版艺术：[手法字母 A/B/C/D/E] — [一句话说明具体如何实现，如"C. 多层叠加 — 巨型背景字BRAND低透明叠底 + E. 超大裁切 — Hero首字母局部裁切"]
按钮造型：[主CTA用BTN-X] + [ghost/次要按钮用BTN-X] + [Feature卡片用CARD-X，如"BTN-C（3D挤出）主CTA + BTN-E（扫描填充）ghost + CARD-B（偏移双边框）"]
光标增强：[CUR-X变体] + [EFF-X上下文效果，如"CUR-B blend反色 + EFF-2点击爆炸 + 3个上下文状态：hover/view/text"]
Features替代方案：[必须说明是否用Features，若用则附加形式变体；若不用则说明替代布局，如"跳过Features，改用横向时间线 + 数字气泡组合"]
Wild Card 1：[W-xx 互动名称] [大类emoji] — [实现说明，如"W-09 记忆翻牌 [🎮游戏] — 品牌元素配对，3难度，计时"]
Wild Card 2：[W-xx 互动名称] [大类emoji] — [实现说明，必须与WC1不同大类]
组件选用：
  [C-X 大类] → [具体组件名称]
  [C-X 大类] → [具体组件名称]
  [C-X 大类] → [具体组件名称]
  C-G 趣味互动 → [具体互动1] + [具体互动2（可选）]
趣味互动说明：[一句话描述C-G互动的实现方式和用户体验]
---
```

**技法选取参考（非强制，根据品牌气质自主判断）**：

| 品牌气质方向 | 适合的主技法 | 适合的辅技法 |
|---|---|---|
| 创意机构 / 作品集 | T-16 T-28 T-22 T-01 | T-23 T-07 T-13 |
| 游戏 / 沉浸娱乐 | T-02 T-17 T-30 T-26 T-49 | T-21 T-22 T-14 T-43 |
| AI工具 / 生产力SaaS | T-29 T-21 T-04 T-30 | T-25 T-09 T-10 |
| 开发者工具 / 技术产品 | T-02 T-21 T-15 T-11 | T-09 T-13 T-29 |
| 硬件 / 科技发布 | T-06 T-05 T-30 T-04 | T-21 T-02 T-23 |
| NFT / Web3 / 加密 | T-17 T-21 T-02 T-26 T-43 | T-16 T-28 T-49 |
| 创意设计工作室 | T-16 T-28 T-18 T-08 | T-23 T-09 T-13 |
| 摄影 / 视觉作品集 | T-24 T-16 T-19 T-08 | T-09 T-23 T-13 |
| 奢侈品 / 高端品牌 | T-18 T-19 T-08 T-01 | T-09 T-23 T-27 |
| 时尚 / 美妆 / 香水 | T-24 T-18 T-08 T-19 | T-09 T-23 T-13 |
| 餐饮 / 咖啡 / 食品 | T-20 T-09 T-27 T-14 | T-18 T-19 T-23 |
| 健康 / Wellness / 运动 | T-27 T-09 T-10 T-29 | T-20 T-13 T-24 |
| 旅游 / 酒店 / 建筑 | T-06 T-24 T-05 T-30 | T-09 T-23 T-13 |
| 数据 / 金融 / 投资 | T-15 T-21 T-05 T-04 | T-10 T-09 T-27 |
| 教育 / 媒体 / 内容 | T-11 T-25 T-29 T-01 | T-27 T-10 T-13 |
| 叙事型 / 品牌宣言 | T-11 T-30 T-25 T-01 | T-23 T-13 T-26 |
| 活动 / 发布会 / 黑客松 | T-22 T-02 T-17 T-26 | T-21 T-25 T-14 |
| 手绘插画风格 | T-41 T-45 T-09 | T-42 T-50 T-20 |
| 赛博朋克 / 废土风格 | T-49 T-43 T-21 | T-32 T-17 T-46 |
| 音乐 / 娱乐 / 夜生活 | T-48 T-46 T-43 | T-32 T-27 T-22 |
| 潮流 / Y2K / 孟菲斯 | T-32 T-35 T-26 | T-50 T-43 T-07 |
| 儿童 / 青少年 / 教育游戏 | T-42 T-50 T-20 | T-41 T-46 T-09 |
| 小游戏 / 互动体验 | T-45 T-47 T-42 | T-50 T-43 T-21 |
| 个人博客 / 独立开发者 | T-11 T-01 T-37 | T-09 T-41 T-23 |
| 摄影 / 作品集 / 大图展示 | T-60 T-58 T-08 | T-55 T-04 T-09 |
| 奢侈品 / 剧场感品牌 | T-55 T-01 T-11 | T-52 T-57 T-09 |
| 工业 / 精密 / 设计工具 | T-51 T-05 T-21 | T-58 T-30 T-32 |
| 有机 / wellness / 美妆 | T-54 T-09 T-11 | T-58 T-59 T-45 |
| 创意机构 / 互动排版 | T-56 T-01 T-26 | T-52 T-03 T-55 |

**辅技法双选规则**：
- 辅技法 A 优先选**视觉/背景/排版**类：T-09 T-13 T-23 T-27 T-32 T-36 T-40 T-41 T-44 T-46 T-49 T-54 T-55 T-58 T-60
- 辅技法 B 优先选**交互/鼠标/物理**类：T-03 T-07 T-08 T-16 T-19 T-35 T-42 T-43 T-47 T-48 T-50 T-51 T-52 T-53 T-56 T-57 T-59
- A 和 B 不能属于同一技法分类（不能两个都是"鼠标交互"）
- 辅技法与主技法之间不能功能重叠（如主技法已用 T-17，辅 B 不再用 T-07）

**辅技法 A 通用选项**（任何主技法都可搭配）：
- T-09 渐变噪点纹理 → 提升背景质感
- T-13 Section 虚化过渡 → 平滑区块边界
- T-23 旋转文字徽章 → Hero 区装饰性 CTA
- T-27 无限自动滚动 → Logo墙 / 媒体报道横幅
- T-41 手绘SVG路径 → 区块装饰性描边动画
- T-44 多层视差景深 → Hero 层次感

**辅技法 B 通用选项**（趣味互动维度）：
- T-42 物理弹跳 → CTA 按钮弹性反馈
- T-43 光标粒子拖尾 → 增强鼠标存在感
- T-47 拖拽排序 → 产品功能 Demo 区
- T-48 均衡器可视化 → 装饰性 Hero 元素
- T-50 点击涟漪 → 全页按钮触感强化

---

## Step 3：生成 Round 1 Prompt（整体框架）

**格式要求**：英文指令式，具体有设计指导性，不拟人化叙述，不写"I want"/"Please create"式开场。**有效内容 ≥ 900 词**，每项写满，禁止省略。每个页面区块最少 8~12 行描述（布局 / 内容 / 视觉 / 交互 / 响应式），只写一两行等于没写。

**必须包含（顺序如下）**：

**① Style Manifesto（风格宣言）**：2-3句极具冲击力的视觉方向声明。例："This is not a landing page. It's a digital manifesto — brutalist grid chaos meets acid-colored punk zines. Nothing is symmetrical. Everything is deliberate."

**② 网页类型与品牌定位**：品牌名、slogan、目标用户、情感调性。

**③ 色彩系统**（精确到色值）：
- 背景色（Primary BG）：`#XXXXX`
- 表面色（Surface/Card）：`#XXXXX`
- 强调色（Accent/CTA）：`#XXXXX`
- 正文色（Body Text）：`#XXXXX`
- 每色标注用途

**④ 字体系统**：Display字体（Google Fonts）+ Body字体，标注 Hero H1 的具体尺寸（clamp 表达式）和 letter-spacing。

**⑤ Architecture Declaration（架构声明）**：说明 A01/A02/A03，若是 A02 SPA 需列出所有子页面名称。

**⑥ Layout System Table（布局系统表）**：
```
| Section | 布局方式 | 列数 | 特殊处理 |
|---------|---------|-----|---------|
| HERO    | Full-viewport | 1 | ... |
| ...     | ...     | ... | ... |
```

**⑦ Component Inventory（组件清单）**：列出所有 UI 组件：
- 必选功能性视觉组件（根据类型）：
  - App推广 → CSS手机mockup（border-radius:36px，刘海，内部UI层次）
  - SaaS/工具 → 浏览器mockup 或 Dashboard预览卡片
  - 开发工具 → 代码编辑器mockup，语法高亮span
  - 数据产品 → SVG折线图 / 柱状图 / 圆环进度图
  - 社交/通讯 → 聊天气泡 / 通知卡片
  - 游戏 → 特性卡片 Bento Grid，每格内容异质
  - 音乐 → 均衡器条 / 播放控制条 CSS mockup
  - 手绘风格 → SVG 手绘路径装饰元素

**⑧ 主技法声明**：说明 T-xx 用在哪个区块、产生什么视觉效果、核心代码结构。

**⑨ 区块顺序（禁止每次都是标准结构）**：按品牌叙事逻辑组织，命名要有个性（不用 "Features" / "Testimonials" 等泛称）。

**排版底线**（必须写入）：
- H1 ≥ 72px，Hero 标题行高 ≤ 1.0
- Section 标题入口自由选择（**连续3条不得全部使用相同结构**）：
  - **A 编号型**：`01 / 02 / 03` monospace 小标签 + 大标题（默认，适合 SaaS/工具/通用品牌）
  - **B 直冲型**：单行大标题无编号，直接视觉冲击（适合运动/游戏/极简品牌）
  - **C 纯视觉型**：无文字区块标题，靠色彩/图形/空间区分 section（适合作品集/摄影/奢侈品）

---

## Step 4：生成 Round 2 Prompt（功能性交互系统）

**有效内容 ≥ 900 词**，每项写满，以 PRD 文档精度描述。**本轮是最关键的一轮**：视觉描述 ≤ 40%，交互行为描述 ≥ 40%，结构+验收 ≥ 20%。

> [!IMPORTANT]
> **本轮必须优先写明所有功能性交互的完整行为规格**，这是通过/不通过的核心差异。仅描述 hover 状态、CSS 动效参数不算完成本轮。

**⓪ 功能性交互强制规格（必须全部写明，每项至少 5~8 行）**：

**Modal 弹窗**（96%不合格案例的核心缺陷）：
- 触发元素：指明哪些卡片/按钮点击后弹出
- 弹窗内容：具体内容结构（标题/图片/描述/按钮等）
- 尺寸布局：`width: min(90vw, 720px); max-height: 88vh; overflow-y: auto`
- backdrop：`position:fixed; inset:0; backdrop-filter:blur(8px); background:rgba(...,0.6)`
- 关闭方式：ESC 键 + backdrop 点击 + 关闭按钮（三种必须全部实现）
- 进退场动画：opacity 0→1 + scale(0.96)→scale(1)，200ms cubic-bezier
- Focus trap：打开后 focus 第一个可聚焦元素，Tab 键循环内部
- ARIA：`role="dialog" aria-modal="true" aria-labelledby="modal-title"`

**FAQ Accordion**（87%不合格案例缺失）：
- 题数：≥ 5 题，逐题写出完整问题和答案文字
- 动画：`max-height` 从 0 → `element.scrollHeight` px，transition 400ms cubic-bezier
- 图标：展开时旋转 180deg（或 ×），transition 300ms
- 互斥：展开新项时关闭其他已展开项
- ARIA：`aria-expanded="false/true"` 动态切换，`aria-controls="panel-id"`
- 默认状态：第一题默认展开

**Toast 通知**（96%不合格案例缺失）：
- 触发时机：点击主 CTA 按钮后触发
- 位置：`position:fixed; top:24px; right:24px; z-index:300`
- 内容：具体的通知文字（中英均可）
- 进场：`translateX(120%) → translateX(0)`，350ms ease-out
- 自动消失：3~5s 后触发退场动画，退场后 `remove()`
- 关闭按钮：右上角 ×，点击立即退场

**Tab 切换**：
- Tab 数量：≥ 3 个，逐一列出 Tab 名称和对应内容
- 指示线：绝对定位金线，JS 读取激活 Tab 的 `offsetLeft/offsetWidth`，`transition: left/width 350ms`
- 内容切换：`opacity: 0 → 1`，150ms fade
- ARIA：`role="tablist"`，每个 tab `role="tab" aria-selected="true/false"`
- 键盘：左右箭头键切换 Tab

**数字计数**（视口触发 + rAF）：
- `easeOutExpo` 缓动函数
- duration: 2000ms，`requestAnimationFrame` 驱动
- IntersectionObserver threshold: 0.3 触发，触发后 unobserve
- 含小数的数字用 `.toFixed(1)` 处理

**导航栏滚动态**：
- 阈值：`window.scrollY > 80`
- 效果：`backdrop-filter:blur(16px)` + 背景色半透明 + bottom border/shadow 出现
- 向下滚动隐藏、向上滚动显示（可选，但写了要实现）

**必须包含**：

**① 主技法精确实现参数**（参照技法库代码，给出所有具体数值）：
- transition duration、easing function（完整 cubic-bezier 参数）
- stagger delay 计算公式、偏移量（px 或 vw）
- JS 触发条件（IntersectionObserver threshold / scroll position）

**② 辅技法 A + B 精确实现**：
- 辅技法 A（视觉维度）：说明位置、CSS 关键参数、与主技法的视觉互补关系
- 辅技法 B（交互维度）：说明触发方式、JS 实现思路、用户感知到的反馈
- 两者必须在页面中有明确的、可见的区域——不能仅作为"全局小细节"

**③ Interaction State Matrix（三态交互矩阵）**：
```
| 组件 | Normal | Hover | Active/Focus |
|------|--------|-------|--------------|
| CTA按钮 | bg:#XXX border:none | bg:#YYY scale(1.02) shadow | scale(0.97) bg:#ZZZ |
| 卡片 | ... | translateY(-6px) border-color... | ... |
| 导航链接 | ... | underline scaleX(0→1) | color变化 |
```

**④ Animation Timing Sheet（动画时序表）**：
```
| 动画名 | 触发时机 | duration | easing | delay |
|--------|---------|----------|--------|-------|
| Hero字符入场 | 页面加载 | 0.6s | cubic-bezier(0.16,1,0.3,1) | char*0.04s |
| 计数器 | IO threshold:0.5 | 1700ms | easeOutExpo | 0 |
| 卡片reveal | IO threshold:0.15 | 0.85s | cubic-bezier(0.16,1,0.3,1) | i*0.12s |
```

**⑤ 趣味互动规格（Fun Interaction Spec）**：
针对 C-G 选用的每一个趣味互动，必须描述：
- **用户旅程**：用户在什么场景下发现/触发它？（滚动到某区域 / 点击特定元素 / 鼠标进入区域）
- **交互机制**：具体的 JS/CSS 实现逻辑（关键函数、事件类型、状态变量）
- **视觉反馈**：触发后用户看到/感受到什么？（动画描述 + duration + easing）
- **品牌契合度**：为什么这个互动适合这个品牌？（一句话说明）
若选择隐藏彩蛋（可选）：额外描述触发序列 + 解锁内容

**⑥ 导航栏精细化**：hover 下划线动效（scaleX 从中心展开）、滚动后 backdrop-filter blur + 具体 rgba 值、CTA 按钮 ::before translateX 填充扫过。

**⑦ 组件清单（按冷却系统选取，每页 ≥ 3 个大类）**：
- 对照确认卡中声明的 C-X 组件，逐一描述 JS 逻辑 + 动画细节
- C-G 趣味互动层必须重点描述：用户如何发现它、如何触发、视觉反馈是什么
- 禁止：在没有冷却位的情况下重复上一条用过的同类组件
- 每个组件给出至少 3 个具体参数（duration、easing、触发条件 / 元素尺寸 / 颜色变化等）

**Footer newsletter 规则（强制）**：
- **允许**含 newsletter 订阅框的类型：SaaS产品、在线教育、内容媒体、健康wellness、开发者工具
- **禁止**含 newsletter 的类型：餐饮/咖啡、游戏、作品集/摄影师、奢侈品/香水、NFT/Web3、运动品牌
- 禁止类型的 Footer 改用：品牌社交媒体链接 + 联系/预约入口 + 版权信息（允许加入邮件联系地址但不做订阅表单）

---

## Step 5：生成 Round 3 Prompt（响应式 + 可访问性）

**有效内容 ≥ 900 词**，以断点规格 + ARIA 清单精度描述。

**必须包含**：

**① Three-Second Memory Test（三秒记忆测试）**：
用一句话描述：如果用户只看三秒截图，他们会记住什么？这个记忆点必须是技法 + 风格 + 品牌的三重叠加。例："记住的是：全屏故障闪烁的赛博朋克标题 + 霓虹粉的冲击感 + CIPHER 这个品牌名"。

**② Delight Details（取悦细节）**：至少列出 5 个让用户惊喜的微细节：
- 按钮按下时的弹性回弹
- 数字从 0 跳动到终值时的 easeOutExpo 弹跳
- 某个图标在 hover 时轻微旋转
- 特定文字有光扫过动效
- 滚动条 thumb 是品牌色渐变

**③ 响应式规范**：
- **390px（甲方验收必查）**：无横向滚动（`body { overflow-x:hidden }`）、汉堡菜单、按钮 full-width、Modal `width:95vw`
- 768px 断点：单列布局、汉堡菜单全屏覆盖（translateX -100%→0）、padding 减半、Tab 栏改横向滚动
- 1024px：Grid 变 2 列，间距缩小
- 触屏设备：取消磁性按钮 / 自定义光标（CSS `@media (hover:none)` 检测）

**④ 标准交互完善**：
- 所有交互状态：hover / active / focus（表单 focus border-color 变化、outline 替换为 box-shadow）
- 间距系统：section padding 120px 80px → 80px 24px on mobile
- 阴影层级（3级）：卡片 shadow-sm / 浮层 shadow-md / modal shadow-xl
- 圆角系统：全局统一选择 0px / 4px / 8px / 12px 其中一个为基准

**⑤ 动效技术规范**：
- Scroll Reveal：双层 rAF 初始化防闪（`.reveal` 默认 opacity:1，JS 加 `.hidden`），stagger delay `(i%3)*0.12s`
- 数字计数器：easeOutExpo 曲线，1700ms，IO threshold 0.5
- 自定义滚动条：3-4px，品牌色 thumb，transparent track

**⑥ 质量检查清单**：
- 所有 section 有 id，导航锚点一一对应
- SPA 多页：每个子页面入场动画独立，active 状态标记正确

**结尾必须写入**（固定格式，不要省略）：
```
Final checks required:
- No console errors
- All images use valid Unsplash URLs
- .reveal elements default to opacity:1 (hidden class added via JS, not CSS)
- Closing </body></html> present
- No Tailwind CDN, no cdn-cgi Cloudflare code
- All buttons functional, no dead href="#" links
- Every section id matches navbar anchor href
```

---

## Step 5.5：生成 Round 4 Prompt（打磨细节 + Acceptance Criteria）

**有效内容 ≥ 900 词**。本轮核心任务：打磨边界细节 + 写出逐条可验证的验收清单。

**必须包含**：

**① 边界状态与性能保障**：
- 数字计数器越界处理：加载时已在视口 → `getBoundingClientRect().top < window.innerHeight` 立即触发
- Scroll Reveal 防黑屏：双重 rAF（`requestAnimationFrame(() => requestAnimationFrame(() => { /* 添加 .hidden */ }))`)
- 图片兜底：所有 `<img>` 加 `onerror` 防止裂图破坏布局
- Modal 焦点返回：关闭 modal 时 focus 回触发该 modal 的原始元素
- `will-change` 限制：仅在动画持续期间设置，`transitionend` 后移除

**② 完整交互类型清单**（≥ 8 种不同交互，列表形式逐一确认）：

| # | 交互类型 | 触发区域 | 可观察结果 |
|---|---------|---------|----------|
| 1 | Modal 弹窗 | ... | ... |
| 2 | Accordion 展开/收起 | ... | ... |
| 3 | Toast 通知 | ... | ... |
| 4 | Tab 切换 + 指示线 | ... | ... |
| 5 | 数字计数 | ... | rAF 从 0 计数 |
| 6 | Scroll Reveal Stagger | ... | 150ms 错峰渐入 |
| 7 | 导航栏滚动态 | ... | 玻璃化 + shadow |
| 8 | 汉堡菜单 | Mobile | 展开/收起全屏菜单 |
（根据实际页面填写触发区域和可观察结果）

**③ Acceptance Criteria（验收标准清单，最后一轮必须写，格式固定）**：

```
功能验收：
- [ ] 所有交互元素有 default / hover / active / focus-visible 四个状态
- [ ] 移动端 390px 下无横向滚动
- [ ] 功能卡片 ≥ 6 个，点击每张弹出详情 Modal
- [ ] Modal 可通过 ESC / backdrop 点击 / 关闭按钮三种方式关闭
- [ ] FAQ 手风琴 ≥ 5 题，点击展开/收起有 smooth height 动画，图标旋转，互斥
- [ ] CTA 点击弹出 Toast 通知，自动消失（≥ 3s）
- [ ] Tab 切换 ≥ 3 个，内容有过渡动画，指示线平滑滑动
- [ ] Stats 数字在进入视口时从 0 计数至目标值（rAF 驱动）
- [ ] 导航栏滚动超过 80px 后出现玻璃化背景和底部 border/shadow
- [ ] 移动端汉堡菜单可正常展开/收起，展开时 body 不可滚动
- [ ] 页面可观察到 ≥ 8 种不同交互反馈类型

交付验收：
- [ ] 单文件 index.html，CSS / JS 全部 inline（Google Fonts link 除外）
- [ ] 零 console 错误
- [ ] 图片来源：https://images.unsplash.com/ 或 inline SVG
- [ ] 压缩包顶层结构正确：fd_XXX.zip → fd_XXX/src/index.html
- [ ] 语义化 HTML：<nav> <main> <section aria-label="..."> <footer>
- [ ] 无 href="#" / href="#id" 死链
- [ ] Footer 版权年份使用 JS new Date().getFullYear() 动态填充
```

---

## Step 6：生成 HTML

用**四轮 Prompt** 作为完整上下文，生成最终 `index.html`，放入 `src/` 目录。

生成后立即运行质检：
```
python qc.py output/fd_XXX
```
所有 `[FAIL]` 清零后，在 `logs/used_types.json` 中记录本条网页类型。

**创建截图文件夹（根据架构判断）：**
- A01 / A02（滚动页）：不创建额外文件夹，用户手动添加 `preview.png`
- A03–A07 / A09–A12（SPA / 多面板 / 分屏 / 径向）：立即执行 `mkdir output/fd_XXX/preview`，提醒用户每个 Panel 单独截图放入该文件夹，命名 `preview_01.png`、`preview_02.png`……

**生成 description 文件：**
在 `output/description/fd_XXX_des.md` 中，用自然语言描述该页面静态截图**无法体现**的内容，按以下维度（无则省略）：

```markdown
## 交互效果
"..."

## 隐藏功能
"..."

## 状态变化
"..."

## 数据流
"..."
```

提醒用户后打包为 `fd_XXX.zip`（结构遵守 rules.md 一）。

---

## 输出格式约定

**prompt.md 严格格式**：

```
## Round 1

[英文指令式内容，角色定义 + 设计系统 + 页面区块结构，每区块 ≥ 8 行]

## Round 2

[英文，功能性交互系统 — Modal / Accordion / Toast / Tab 逐一写明触发+行为+关闭+ARIA]

## Round 3

[英文，响应式断点（含 390px）+ 可访问性 + 动效技术规范]

## Round 4

[英文，打磨细节 + 完整 Acceptance Criteria 验收清单（功能验收 ≥ 10 项 + 交付验收 ≥ 7 项）]
```

**Round 1 之前绝对不允许出现任何内容**（无标题行、无品牌信息卡、无中文注释、无空行）。

**字数自查**：保存 prompt.md 后确认总字符数 ≥ 5500。写不够时继续展开 Modal 内容细节 / Accordion 题目文字 / 验收清单条目，禁止堆砌形容词。

