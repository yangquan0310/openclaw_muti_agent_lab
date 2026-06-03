---
name: quarto-ppt
description: "Quarto 演示文稿制作技能。Use whenever the user wants to create a PowerPoint or HTML presentation (slides/deck/课件/PPT) using Quarto (.qmd) instead of python-pptx or pptxgenjs. Triggers: '用 Quarto 做 PPT'、'Quarto 幻灯片'、'.qmd 演示文稿'、'RevealJS 课件'、'生成 .pptx 用 Quarto'. 输出格式支持 pptx（可二次编辑的 PowerPoint）和 revealjs（HTML 演示文稿）。覆盖：模板搭建、布局系统、主题定制、参考模板、Pandoc 兼容、嵌入图表/公式/代码、演讲者备注、品牌一致性。"
license: MIT
version: 1.0.0
metadata:
  openclaw:
    emoji: 🎞️
    requires:
      bins: ["quarto"]
---

# Quarto PPT 制作技能

> 一切 PPT 都从 `.qmd` (Quarto Markdown) 出发。两种核心输出：
> - **pptx**：可二次编辑的 PowerPoint 文件
> - **revealjs**：HTML 演示文稿，主题丰富、可打印 PDF

---

## 0. 速查决策表

| 场景 | 推荐格式 | 原因 |
|------|----------|------|
| 需要 `.pptx` 给学员 / 老师二次编辑 | `pptx` | 标准 Office 格式 |
| 内部技术分享，演示效果优先 | `revealjs` | 主题丰富、动画、可打印 PDF |
| 公司有现成 PowerPoint 母版 | `pptx` + `reference-doc` | 直接套品牌 |
| 需要做"代码 + 公式 + 图"混合课件 | `revealjs` | 渲染更灵活 |
| 课程多页、有大量配图 | `pptx` + 自定义模板 | 排版稳定、字体兼容好 |
| 客户要求 PDF | `revealjs` → 打印 PDF | 唯一靠谱方式 |
| 学员要 Word/PPT 里批注 | `pptx` | 原生可批注 |

---

## 1. 环境

```bash
# 验证 Quarto 已安装
quarto --version          # ≥ 1.5 即可
quarto check              # 体检

# 若需要 Python 计算块（图表/数据），还要装 Jupyter
conda install jupyter nbformat  # 或 pip install notebook nbformat
```

> 已验证：本机 Quarto 1.7.34 + 系统未装 Pandoc 也可渲染（Quarto 自带）。

---

## 2. 最小可运行示例

### 2.1 PowerPoint（pptx）

```markdown
---
title: "我的课件"
author: "杨权"
date: "2026-06-04"
format:
  pptx:
    incremental: true
    slide-level: 2
---

# 课程总览

## 这是分隔页

`#` 标题 → Section Header 布局。

## 这是内容页

- 要点 1
- 要点 2
- 要点 3

## 两列

:::: {.columns}
::: {.column width="50%"}
**左**
:::
::: {.column width="50%"}
**右**
:::
::::

## 演讲者备注

::: {.notes}
这页是给演讲者看的。
:::
```

```bash
quarto render my-deck.qmd --to pptx
# → my-deck.pptx
```

### 2.2 RevealJS（HTML）

```markdown
---
title: "我的演示"
format:
  revealjs:
    theme: simple       # 内置主题
    incremental: true
    slide-number: true
    chalkboard: true    # 白板
---

## 第一页

- 内容

## 第二页

公式 $E=mc^2$

```python
print("代码高亮")
```
```

```bash
quarto render my-deck.qmd --to revealjs
# → my-deck.html
```

---

## 3. 核心语法

### 3.1 幻灯片分隔

| 语法 | 用途 |
|------|------|
| `# 一级标题` | 分隔页（Section Header） |
| `## 二级标题` | 普通幻灯片（默认） |
| `---` (水平线) | 强制分隔一张幻灯片 |
| 标题后 `{.section}` | 显式声明为分隔页 |
| 标题后 `{.inverse}` | 反色（深色背景） |

> **重要**：YAML 里 `slide-level` 决定哪一级标题对应新幻灯片。pptx 默认是 2，revealjs 默认是 1。要让 `#` 在 revealjs 里是"分级标题"而非"新幻灯片"，用 `slide-level: 2`。

### 3.2 列表

```markdown
- 普通列表
- 列表项二
  - 嵌套项
- 列表项三
```

配合 `incremental: true` → 逐条出现（默认 revealjs 关闭，pptx 关闭）。

### 3.3 两列布局

```markdown
:::: {.columns}
::: {.column width="50%"}
左列
:::
::: {.column width="50%"}
右列
:::
::::
```

`width` 可写 `40%` / `300px` / `5em`。

### 3.4 代码块

````markdown
```python
# 纯语法高亮，不执行
def f(x): return x**2
```
````

> ```{python} 这种带引擎的块需要 Jupyter 引擎（要装 nbformat）。仅做语法高亮用三反引号即可。

### 3.5 公式

```markdown
行内：$E=mc^2$

独立：
$$
\int_0^{\infty} e^{-x^2}dx = \frac{\sqrt{\pi}}{2}
$$
```

### 3.6 图片

```markdown
![替代文字](path/to/image.png){width=80%}

# 或用 figure 块（带标题、可交叉引用）
![图](image.png){width=70% fig-align="center"}
```

支持本地路径、URL；推荐放 `images/` 子目录。

### 3.7 表格

```markdown
| 列1 | 列2 | 列3 |
|----:|----:|----:|
|  12 |  34 |  56 |
|  78 |  90 |  12 |
```

### 3.8 演讲者备注

```markdown
## 幻灯片标题

可见内容

::: {.notes}
这些只在演讲者视图出现，不会上屏。
:::
```

> pptx 输出会生成"备注页"；revealjs 按 `s` 键进入演讲者视图。

### 3.9 片段动画（revealjs 专享）

```markdown
::: {.fragment}
第一段
:::

::: {.fragment .fade-in}
第二段（淡入）
:::

::: {.fragment .highlight-red}
第三段（高亮红色）
:::
```

### 3.10 背景图 / 视频（revealjs）

```markdown
## 背景图 {background-image="images/bg.jpg" background-size="cover"}

## 视频背景 {background-video="videos/loop.mp4" background-loop=true}
```

---

## 4. 主题与样式

### 4.1 RevealJS 主题

内置 11 套：`beige` `blood` `dark` `default` `dracula` `league` `moon` `night` `serif` `simple` `sky` `solarized`

```yaml
format:
  revealjs:
    theme: dracula
```

**自适应亮/暗**：

```yaml
format:
  revealjs:
    theme:
      light: [default, custom-light.scss]
      dark: [dark, custom-dark.scss]
```

### 4.2 自定义主题（SCSS）

```yaml
format:
  revealjs:
    theme: [default, custom.scss]
```

`custom.scss`：

```scss
/*-- scss:defaults --*/
$body-bg: #fafafa;
$body-color: #222;
$link-color: #c0392b;
$heading-color: #2c3e50;

/*-- scss:rules --*/
.reveal .slide-title {
  font-weight: 700;
  letter-spacing: -0.02em;
}
```

> 关键变量：`$body-bg` `$body-color` `$link-color` `$presentation-font-size-root` `$code-color`

### 4.3 PPTX 主题：用 reference-doc

PowerPoint 没有"主题"概念，要用**母版模板**：

```yaml
format:
  pptx:
    reference-doc: templates/brand-template.pptx
```

模板里 Slide Master 必须包含这些布局名（Pandoc 按名字匹配）：

- `Title Slide`
- `Title and Content`
- `Section Header`
- `Two Content`
- `Comparison`
- `Content with Caption`
- `Blank`

**生成默认模板做起点**：

```bash
quarto pandoc -o template.pptx --print-default-data-file reference.pptx
# 用 PowerPoint 打开 template.pptx → 修改 Slide Master → 保存
```

### 4.4 品牌颜色（PPT 端）

由于 Pandoc 渲染 .pptx 的 CSS 能力有限，**颜色字体改在 reference-doc 的 Slide Master 里做**最稳。
临时文字颜色可内联 HTML：

```html
<span style="color:#c0392b">红字</span>
```

---

## 5. 嵌入图表

### 5.1 静态图（最常用）

```markdown
![趋势图](charts/trend.png){width=80%}
```

> 优先用 PNG/JPG 静态图，跨平台稳定。

### 5.2 动态图（需 Jupyter）

````markdown
```{python}
#| echo: false
#| fig-width: 8
#| fig-height: 4
import matplotlib.pyplot as plt
import numpy as np
x = np.linspace(0, 2*np.pi, 100)
plt.plot(x, np.sin(x))
plt.title("Sine wave")
plt.show()
```
````

> 需要 `conda install jupyter nbformat`。

### 5.3 Mermaid / Graphviz 流程图

````markdown
```{mermaid}
flowchart LR
  A[开始] --> B{判断}
  B -->|是| C[执行]
  B -->|否| D[结束]
```
````

需要 `npm install -g @mermaid-js/mermaid-cli` 或 Quarto 1.5+ 自带。

---

## 6. 命令行

```bash
# 渲染
quarto render deck.qmd                    # 默认按 YAML 渲染所有格式
quarto render deck.qmd --to pptx          # 只输出 pptx
quarto render deck.qmd --to revealjs      # 只输出 revealjs

# 预览（带热重载）
quarto preview deck.qmd

# 输出到指定目录
quarto render deck.qmd --to pptx --output-dir output/

# 清理
quarto clean deck.qmd
```

---

## 7. 文件组织建议

```
project/
├── deck.qmd                 # 主编排文件
├── chapters/                # 可拆分子文件
│   ├── 01-intro.qmd
│   └── 02-content.qmd
├── images/                  # 图片
├── charts/                  # 图表（PNG/SVG）
├── templates/
│   └── brand-template.pptx  # 公司品牌母版
├── custom.scss              # 自定义主题（revealjs）
├── _quarto.yml              # 项目级 YAML（可选）
└── output/                  # 渲染产物
```

`deck.qmd` 引用子文件：

```yaml
---
title: "..."
format:
  pptx:
    reference-doc: templates/brand-template.pptx
---

{{< include chapters/01-intro.qmd >}}
{{< include chapters/02-content.qmd >}}
```

---

## 8. 与 python-pptx 的对比

| 维度 | Quarto (qmd) | python-pptx |
|------|--------------|-------------|
| **作者友好度** | ⭐⭐⭐⭐⭐ Markdown | ⭐⭐ Python API |
| **公式/代码/图表** | ⭐⭐⭐⭐⭐ 原生 | ⭐⭐ 需手动 |
| **可二次编辑** | ⭐⭐⭐（pptx）| ⭐⭐⭐⭐⭐ |
| **精确像素控制** | ⭐⭐（受限）| ⭐⭐⭐⭐⭐ |
| **自动化（数据驱动）** | ⭐⭐⭐⭐ 模板循环 | ⭐⭐⭐⭐⭐ |
| **主题复用** | ⭐⭐⭐⭐⭐ reference-doc | ⭐⭐ 复制代码 |
| **Git diff 友好** | ⭐⭐⭐⭐⭐ | ⭐ 代码 diff |
| **学习曲线** | 1 小时上手 | 1 天上手 |

**结论**：能用 Quarto 就用 Quarto，**只有需要逐像素控制 / 程序化拼装 / 已有 python-pptx 资产时才退回 python-pptx**。

---

## 9. 常见问题

### Q1. 中文 / 字体乱码
- 在 reference-doc 的 Slide Master 里把"亚洲字体"设为"微软雅黑"或"思源黑体"
- YAML 加上 `lang: zh-CN`

### Q2. 渲染 .pptx 后配色丢了
- Pandoc 不会读 SCSS；颜色全在 reference-doc 里配
- 在 qmd 里用 `<span style="color:#xxx">` 临时覆盖

### Q3. 图片不显示
- 路径用相对路径（相对于 .qmd）
- 远程 URL 要带扩展名 `?text=...` 不行就用 `https://placehold.co/600x300`

### Q4. revealjs 的 Python 代码块报错 "no module nbformat"
- 装 Jupyter：`conda install jupyter nbformat`
- 或改用三反引号纯语法高亮

### Q5. 一份 .qmd 同时输出 pptx 和 revealjs
```yaml
format:
  pptx: default
  revealjs: default
```
然后 `quarto render deck.qmd` 同时得到两个文件。

### Q6. 打印 revealjs 为 PDF
浏览器打开 → `?print-pdf` 后缀 → Ctrl+P → 另存 PDF。
Quarto 自带：`quarto render deck.qmd --to revealjs --embed-resources` 便于单文件分发。

---

## 10. 模板清单

| 文件 | 用途 |
|------|------|
| [`templates/basic-pptx.qmd`](templates/basic-pptx.qmd) | 最小 PPTX 模板 |
| [`templates/basic-revealjs.qmd`](templates/basic-revealjs.qmd) | 最小 RevealJS 模板 |
| [`templates/lesson-pptx.qmd`](templates/lesson-pptx.qmd) | 课程用 PPTX 模板（封面+目录+章节+小结） |
| [`examples/demo-pptx.qmd`](examples/demo-pptx.qmd) | PPTX 完整示例 |
| [`examples/demo-revealjs.qmd`](examples/demo-revealjs.qmd) | RevealJS 完整示例 |

---

## 11. 制作流程（推荐）

1. **明确场景**：要 pptx 还是 revealjs？
2. **选模板**：从 `templates/` 复制起点
3. **写 Markdown 内容**：用 H2 分页、列表、两列、代码、公式
4. **首次渲染**：`quarto render deck.qmd --to pptx`，看效果
5. **调样式**：
   - revealjs：编辑 `custom.scss`（颜色 / 字体）
   - pptx：编辑 `templates/brand-template.pptx`（母版 / 配色 / 字体）
6. **嵌入资产**：图片放 `images/`，代码块改语法高亮
7. **演讲者备注**：每页加 `::: {.notes} :::`
8. **最终渲染**：`quarto preview` 实时检查，`quarto render` 出成品
9. **交付**：`output/deck.pptx` 或 `output/deck.html`

---

## 12. 关键文档

- Quarto Presentations 概览：https://quarto.org/docs/presentations/
- PowerPoint 格式：https://quarto.org/docs/presentations/powerpoint.html
- RevealJS 格式：https://quarto.org/docs/presentations/revealjs/
- 主题定制：https://quarto.org/docs/presentations/revealjs/themes.html
- PPTX 选项参考：https://quarto.org/docs/reference/formats/presentations/pptx.html
- RevealJS 选项参考：https://quarto.org/docs/reference/formats/presentations/revealjs.html
