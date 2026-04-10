# 视觉连续性规范（Visual Continuity Rules）

> 本文件定义单页滚动型页面（A01/A02/A11 等）的 section 间色彩过渡与视觉一体性要求。

---

## 一、核心原则

**单页滚动页面中，section 之间的背景色切换必须有视觉连续性。**

用户滚动页面时，不应感到"突然跳到了另一个网站"。相邻 section 的色调变化必须是渐变过渡的、有节奏的、或通过明确的设计手法（撞色/分割线/clip-path）进行有意识的衔接。

**多面板/SPA 页面（A03-A07/A09/A12）不受此规则限制** — 每个 panel 是独立页面，允许大色差。

---

## 二、色调统一优先（强烈推荐）

### 2.1 优先使用策略 A：全深色同色族

**这是最安全、效果最好的方案。** 深浅交替（策略B）极易产生撞色突兀感，除非设计师有充分把握，否则默认选择策略A。

所有 section 统一在同一色族的深色调内，通过**色温和明度的微妙变化**创造节奏感：

```
Section 1: #12100a (深焦炭)
Section 2: #1a1508 (深琥珀，稍暖)
Section 3: #181208 (深古铜，稍红)
Section 4: #1e1608 (深蜂蜜，更暖)
Section 5: #161008 (深焦糖，回落)
Section 6: #1c1408 (深核桃)
```

**关键要点：**
- 相邻 section 的 HSL 明度差 ≤ 5%，色相差 ≤ 15°
- 色温变化代替明度变化：偏红/偏黄/偏绿微调，而非亮/暗跳跃
- 整页像一条连续的深色暖调河流，用户几乎感知不到 section 边界
- 纹理（SVG几何/点阵/线条）提供 section 间的视觉区分，而非背景色

### 2.2 策略 B：明暗交替韵律（谨慎使用）

深色和浅色 section 交替出现。**风险高，容易产生撞色感。**

仅在以下情况使用：
- 品牌调性明确要求明暗对比（如报纸/杂志排版风格）
- 每次跳跃都有 200px 伪元素渐变过渡带
- 深色与浅色section的色相必须一致（如都是暖棕色族）

### 2.3 策略 C：自然撞色设计（需要明确手法）

允许大色差，但**必须通过明确的设计手法**让撞色看起来是有意为之。

**合法手法：** 粗分割线 / 几何clip-path / 全宽图片过渡 / 色块叠加层

**禁止：** 无任何过渡手法的大色差直接相邻。

---

## 三、渐变过渡实现方式

### 3.1 唯一推荐方式：伪元素渐变遮罩

**禁止在 section 的 `background` 的 `linear-gradient` 最后一层直接做过渡色！** 这会导致渐变色影响到 section 内的卡片、文字等内容的视觉感受。

正确做法 — 使用 `::after` 伪元素：

```css
/* 基础设施 */
.section[data-fade-to]::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 200px;          /* 200px 足够柔和 */
  pointer-events: none;
  z-index: 0;             /* 背景层 */
}
.section > * {
  position: relative;
  z-index: 1;             /* 内容在渐变之上 */
}

/* 每个 section 单独定义渐变终点色 = 下一个 section 的背景色 */
#sec-hero::after    { background: linear-gradient(to bottom, transparent, #1a1508); }
#sec-story::after   { background: linear-gradient(to bottom, transparent, #181208); }
#sec-craft::after   { background: linear-gradient(to bottom, transparent, #1e1608); }
```

**要点：**
- `z-index: 0` 确保渐变只在背景层，不影响卡片/文字颜色
- `z-index: 1` 在 `.section > *` 上，让所有内容浮在渐变之上
- 每个 section 的 HTML 上加 `data-fade-to="xxx"` 属性触发 `::after`
- 高度 200px（同色族微调时足够）；如果色差较大可增至 300px

### 3.2 禁止的写法

```css
/* 错误！渐变直接写在 background 里会污染内容颜色 */
#sec-dark {
  background: linear-gradient(180deg,
    #1a1508 0%,
    #1a1508 82%,
    #f0e8d4 100%   /* 这个过渡色会透过卡片背景影响视觉 */
  );
}
```

---

## 四、背景纹理规范

### 4.1 纹理提供 section 区分

当所有 section 使用相近的深色背景时，**装饰性纹理是区分不同 section 的主要手段**：

```
Story:      交叉线纹理（repeating-linear-gradient ±45deg）
Craft:      圆形蓝图网格（SVG circle + line）
Heritage:   水平横线（repeating-linear-gradient 0deg）
Specs:      等距三角网格（linear-gradient 60deg + 120deg）
Collection: 六边形蜂窝（SVG hexagon path）
Boutique:   三角形图案（SVG triangle path）
```

### 4.2 纹理一致性规则
- 整页纹理不超过 **3 种族类**（线条类/网格类/几何形状类）
- 所有纹理的 stroke/fill 颜色统一使用 `rgba(主题色, 0.04-0.08)`
- 深色 section：`rgba(accent, 0.04-0.07)` — 足够细微但可感知
- 纹理密度可变化，但同页内保持视觉权重一致

### 4.3 纹理与背景色配合
- SVG 几何背景的 `stroke` 颜色必须与 section 主色调同色族
- 深色背景用金色/暖色 rgba：`rgba(200,149,42, 0.05)`
- 冷色背景用蓝色/银色 rgba：`rgba(100,150,220, 0.05)`
- 禁止在暖色背景上用冷色纹理（反之亦然）

---

## 五、色彩节奏禁令

### 5.1 禁止频繁明暗跳跃
以下模式**严格禁止**：
```
深 → 亮 → 亮 → 深 → 亮 → 深 → 深 → 深 → 深 → 亮 → 亮 → 深
```
这种无规律跳跃让页面看起来像拼凑的色块。

### 5.2 如果必须有明暗变化，只允许以下节奏
```
模式1：深 → 深 → 深 → 深（全深色，推荐）
模式2：深 → 亮 → 深 → 亮（严格交替，每次都有过渡带）
模式3：深 → 深 → 亮 → 亮 → 深 → 深（分组，每组内同调）
```

### 5.3 冷暖色混用规则
- 同一页内不得出现 3 种以上色族（如暖棕 + 冷蓝 + 暖绿 = 3种，上限）
- 冷暖切换处必须有中性色过渡（灰色/深炭色作为缓冲 section）

---

## 六、确认卡中声明

每条确认卡必须包含：
```
色彩策略：[A/B/C] — 具体说明（如 "A 全深色暖棕同色族，SVG纹理区分section"）
```

---

## 七、验收标准

1. 以 Chrome DevTools 截长图，缩放到 25% 查看整页缩略图
2. 在缩略图视角下，section 之间不应出现"色块拼接"的突兀感
3. 每对相邻 section 的交界处应有可见的过渡处理（200px伪元素渐变）
4. 全页色调应有明确的节奏感 — 如同一首曲子的起伏，而非随机色块
5. 渐变过渡不得影响 section 内的卡片、文字等内容元素的颜色
