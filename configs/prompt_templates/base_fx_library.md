# 技术约束 — 特效扩展库篇（十三）

> 从 `base.md` 拆分。可选增强特效，按需查阅。

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
