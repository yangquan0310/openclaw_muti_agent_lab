---
name: presenter
description: >
  呈现师：所有视觉传达工作的设计师。
  核心职责是 PPT/课件/演示文稿制作（首选 Quarto + .qmd，输出 .pptx 或 RevealJS HTML）；
  兼顾脚本编写、图片制作、图表设计、UI 视觉、品牌视觉执行、文档排版。
  工具原则：PPT 一律用 Quarto，禁用 python-pptx / pptxgenjs 起步。
  当用户要求"做 PPT"、"做课件"、"做演示文稿"、"写脚本"、"做信息图"、"做海报"、"做流程图"、"做界面设计"等视觉任务时激活。
version: 1.8.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🎨
    requires:
      bins: ["quarto"]
---

# presenter（呈现师技能）

> **所有视觉传达工作的设计师**。核心职责：PPT/课件（首选 Quarto + .qmd），辅以脚本、图片、图表、UI、品牌、文档。

---

## 触发条件

| 场景 | 触发关键词 |
|------|------------|
| **PPT / 课件** | 做 PPT、做课件、做幻灯片、写 deck、写 presentation、生成 .pptx |
| **演示文稿** | 培训、技术分享、答辩、述职、汇报 |
| 脚本编写 | 写视角脚本、写分镜头、写演示脚本 |
| 图片 | 做信息图、做插图、做海报、做封面图 |
| 图表 | 流程图、思维导图、知识图谱、架构图 |
| UI 视觉 | 做界面、画图标、配色规范、视觉规范 |
| 品牌 | 配色、字体、Logo 布局、品牌一致性 |
| 文档排版 | 排版文档、调整字体、优化版式 |

---

## 工具原则

### 铁律：PPT 一律用 Quarto

凡是接到"制作 PPT / 课件 / 幻灯片"的任务，**第一步就是用 Quarto（.qmd）**。

| 任务 | 工具 | 备注 |
|------|------|------|
| **PPT/课件** | **Quarto（.qmd）** | 默认 `pptx`，演示场景 `revealjs` |
| 脚本 | Markdown（结构化）| 输出 .qmd 或 .md |
| 图片 | 图像生成工具 | 见下方「图片制作」|
| 图表 | Mermaid / Graphviz / 静态图 | 见下方「图表设计」|
| UI | Figma / 静态稿 | 见 references/ui-guide.md |
| 品牌 | 按公司 brand.yml | 见 references/brand-guide.md |
| 文档 | Quarto / pandoc | 见 references/doc-guide.md |

**严禁**：
- ❌ 不用 python-pptx / pptxgenjs 起步
- ❌ 不写 PowerPoint XML 拼装代码
- ❌ 不在 `pptx-2` / `pptx-generator` 技能上做新工作

**回退旧工具**（必须满足其一）：维护既有 python-pptx 资产 / 客户要求保留旧 .pptx 宏 / 需要逐像素控制。

---

## 核心职责 1：PPT / 课件（默认 Quarto）

> 这是呈现师最核心的工作。一切从 `.qmd` 出发，两种输出：
> - **`pptx`**：可二次编辑的 PowerPoint 文件
> - **`revealjs`**：HTML 演示文稿，主题丰富、可打印 PDF

### 1.1 速查决策表

| 场景 | 推荐格式 | 原因 |
|------|----------|------|
| 需要 `.pptx` 给学员 / 老师二次编辑 | `pptx` | 标准 Office 格式 |
| 内部技术分享，演示效果优先 | `revealjs` | 主题丰富、动画、可打印 PDF |
| 公司有现成 PowerPoint 母版 | `pptx` + `reference-doc` | 直接套品牌 |
| 需要做"代码 + 公式 + 图"混合课件 | `revealjs` | 渲染更灵活 |
| 课程多页、有大量配图 | `pptx` + 自定义模板 | 排版稳定、字体兼容好 |
| 客户要求 PDF | `revealjs` → 打印 PDF | 唯一靠谱方式 |
| 学员要 Word/PPT 里批注 | `pptx` | 原生可批注 |

### 1.2 环境

```bash
quarto --version          # ≥ 1.5 即可（本机验证 1.7.34）
quarto check              # 体检

# 若需要 Python 计算块（图表/数据），还要装 Jupyter
conda install jupyter nbformat
```

> Quarto 自带 Pandoc，系统不装 Pandoc 也能渲染。

### 1.3 最小可运行示例

**PowerPoint（pptx）**：

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

**RevealJS（HTML）**：

```markdown
---
title: "我的演示"
format:
  revealjs:
    theme: simple
    incremental: true
    slide-number: true
    chalkboard: true
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

### 1.4 核心语法

**幻灯片分隔**：

| 语法 | 用途 |
|------|------|
| `# 一级标题` | 分隔页（Section Header） |
| `## 二级标题` | 普通幻灯片（默认） |
| `---`（水平线）| 强制分隔一张幻灯片 |
| 标题后 `{.section}` | 显式声明为分隔页 |
| 标题后 `{.inverse}` | 反色（深色背景）|

> YAML 里 `slide-level` 决定哪一级标题对应新幻灯片。pptx 默认 2，revealjs 默认 1。

**列表**：

```markdown
- 普通列表
- 列表项二
  - 嵌套项
- 列表项三
```

配合 `incremental: true` → 逐条出现。

**两列布局**：

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

**代码块**：

````markdown
```python
# 纯语法高亮，不执行
def f(x): return x**2
```
````

> ```{python} 这种带引擎的块需要 Jupyter 引擎。仅做语法高亮用三反引号即可。

**公式**：

```markdown
行内：$E=mc^2$

独立：
$$
\int_0^{\infty} e^{-x^2}dx = \frac{\sqrt{\pi}}{2}
$$
```

**图片**：

```markdown
![替代文字](path/to/image.png){width=80%}
```

支持本地路径、URL；推荐放 `images/` 子目录。

**表格**：

```markdown
| 列1 | 列2 | 列3 |
|----:|----:|----:|
|  12 |  34 |  56 |
|  78 |  90 |  12 |
```

**演讲者备注**：

```markdown
## 幻灯片标题

可见内容

::: {.notes}
这些只在演讲者视图出现，不会上屏。
:::
```

**片段动画**（revealjs 专享）：

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

**背景图 / 视频**（revealjs）：

```markdown
## 背景图 {background-image="images/bg.jpg" background-size="cover"}

## 视频背景 {background-video="videos/loop.mp4" background-loop=true}
```

### 1.5 主题与样式

**RevealJS 内置 11 套主题**：`beige` `blood` `dark` `default` `dracula` `league` `moon` `night` `serif` `simple` `sky` `solarized`

```yaml
format:
  revealjs:
    theme: dracula
```

**自定义主题（SCSS）**：

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

**PPTX 用 reference-doc 套品牌**：

```yaml
format:
  pptx:
    reference-doc: templates/brand-template.pptx
```

模板 Slide Master 必须包含这些布局名（Pandoc 按名字匹配）：
`Title Slide` / `Title and Content` / `Section Header` / `Two Content` / `Comparison` / `Content with Caption` / `Blank`

**生成默认模板做起点**：

```bash
quarto pandoc -o template.pptx --print-default-data-file reference.pptx
# 用 PowerPoint 打开 template.pptx → 修改 Slide Master → 保存
```

> 颜色字体改在 reference-doc 的 Slide Master 里做最稳。临时颜色用 `<span style="color:#xxx">`。

### 1.6 嵌入图表

**静态图**（最常用）：

```markdown
![趋势图](charts/trend.png){width=80%}
```

**动态图**（需 Jupyter）：

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

**Mermaid 流程图**：

````markdown
```{mermaid}
flowchart LR
  A[开始] --> B{判断}
  B -->|是| C[执行]
  B -->|否| D[结束]
```
````

### 1.7 命令行

```bash
quarto render deck.qmd                    # 按 YAML 渲染所有格式
quarto render deck.qmd --to pptx          # 只输出 pptx
quarto render deck.qmd --to revealjs      # 只输出 revealjs
quarto preview deck.qmd                   # 热重载预览
quarto clean deck.qmd                     # 清理中间产物

# 封装好的渲染脚本（本仓库）
bash scripts/render.sh deck.qmd pptx
bash scripts/render.sh deck.qmd revealjs
bash scripts/render.sh deck.qmd both      # 同时输出两种
```

### 1.8 项目文件组织

```
project/
├── deck.qmd                 主编排文件
├── chapters/                可拆分子文件
│   ├── 01-intro.qmd
│   └── 02-content.qmd
├── images/                  图片
├── charts/                  图表（PNG/SVG）
├── templates/               模板起点（从本技能 templates/ 复制）
├── custom.scss              自定义主题（revealjs）
└── output/                  渲染产物
```

引用子文件：

```markdown
{{< include chapters/01-intro.qmd >}}
{{< include chapters/02-content.qmd >}}
```

### 1.9 与 python-pptx 的对比

| 维度 | Quarto (qmd) | python-pptx |
|------|--------------|-------------|
| 作者友好度 | ⭐⭐⭐⭐⭐ Markdown | ⭐⭐ Python API |
| 公式/代码/图表 | ⭐⭐⭐⭐⭐ 原生 | ⭐⭐ 需手动 |
| 可二次编辑 | ⭐⭐⭐（pptx）| ⭐⭐⭐⭐⭐ |
| 精确像素控制 | ⭐⭐（受限）| ⭐⭐⭐⭐⭐ |
| 自动化（数据驱动）| ⭐⭐⭐⭐ 模板循环 | ⭐⭐⭐⭐⭐ |
| 主题复用 | ⭐⭐⭐⭐⭐ reference-doc | ⭐⭐ 复制代码 |
| Git diff 友好 | ⭐⭐⭐⭐⭐ | ⭐ 代码 diff |
| 学习曲线 | 1 小时上手 | 1 天上手 |

**结论**：能用 Quarto 就用 Quarto，**只有需要逐像素控制 / 程序化拼装 / 已有 python-pptx 资产时才退回 python-pptx**（用 `scripts/ppt/` 旧工具，本仓库已标 DEPRECATED）。

### 1.10 常见问题

**Q1. 中文 / 字体乱码？**
reference-doc 的 Slide Master 把"亚洲字体"设为"微软雅黑"或"思源黑体"；YAML 加 `lang: zh-CN`。

**Q2. 渲染 .pptx 后配色丢了？**
Pandoc 不会读 SCSS；颜色全在 reference-doc 里配。在 qmd 里用 `<span style="color:#xxx">` 临时覆盖。

**Q3. 图片不显示？**
路径用相对路径（相对于 .qmd）。远程 URL 要带扩展名；调试可用 `https://placehold.co/600x300`。

**Q4. revealjs 的 Python 代码块报错 "no module nbformat"？**
装 Jupyter：`conda install jupyter nbformat`。或改用三反引号纯语法高亮。

**Q5. 一份 .qmd 同时输出 pptx 和 revealjs？**

```yaml
format:
  pptx: default
  revealjs: default
```

`quarto render deck.qmd` 同时得到两个文件。

**Q6. 打印 revealjs 为 PDF？**
浏览器打开 → `?print-pdf` 后缀 → Ctrl+P → 另存 PDF。
或 `quarto render deck.qmd --to revealjs --embed-resources` 单文件分发。

### 1.11 模板清单（本仓库）

| 文件 | 用途 |
|------|------|
| `templates/basic-pptx.qmd` | 最小 PPTX 模板 |
| `templates/basic-revealjs.qmd` | 最小 RevealJS 模板 |
| `templates/lesson-pptx.qmd` | 课程用 PPTX 模板（封面+目录+章节+小结+思考题）|
| `templates/brand-template.pptx` | PowerPoint 母版（可在 PowerPoint 里改色/字体）|
| `examples/demo-pptx.qmd` | PPTX 完整示例 |
| `examples/demo-revealjs.qmd` | RevealJS 完整示例 |
| `examples/demo-with-template.qmd` | PPTX + reference-doc 示例 |

### 1.12 PPT 任务标准工作流

1. 明确场景：pptx 还是 revealjs？
2. 选模板：从 `templates/` 复制起点
3. 写 Markdown 内容：H2 分页、列表、两列、代码、公式、图片
4. 首次渲染：`quarto render deck.qmd --to pptx`，看效果
5. 调样式：
   - revealjs → 写 `custom.scss`（颜色、字体）
   - pptx → 改 `templates/brand-template.pptx`（母版、配色、字体）
6. 嵌入资产：图片放 `images/`；代码块改语法高亮
7. 演讲者备注：每页加 `::: {.notes} :::`
8. 最终渲染：`bash scripts/render.sh deck.qmd both`
9. 交付 + 提交督导审核

### 1.13 关键外部文档

- Quarto Presentations 概览：https://quarto.org/docs/presentations/
- PowerPoint 格式：https://quarto.org/docs/presentations/powerpoint.html
- RevealJS 格式：https://quarto.org/docs/presentations/revealjs/
- 主题定制：https://quarto.org/docs/presentations/revealjs/themes.html
- PPTX 选项参考：https://quarto.org/docs/reference/formats/presentations/pptx.html
- RevealJS 选项参考：https://quarto.org/docs/reference/formats/presentations/revealjs.html

---

## 核心职责 2：脚本编写

输出 **.qmd**（Quarto Markdown）结构化脚本，描述每个画面的呈现方式。

详见 [references/script-writing-guide.md](references/script-writing-guide.md)

---

## 核心职责 3：图片制作

| 类型 | 工具 | 输出 |
|------|------|------|
| 信息图 | 图像生成（image_generate）| PNG/JPG |
| 插图 | 图像生成 | PNG/JPG |
| 海报 | 图像生成 + 排版 | PNG/PDF |

详见 [references/image-guide.md](references/image-guide.md) / [image-generation-guide.md](references/image-generation-guide.md)

---

## 核心职责 4：图表设计

| 类型 | 工具 |
|------|------|
| 流程图 | Mermaid / Graphviz |
| 思维导图 | Markdown 嵌套列表 / Mermaid mindmap |
| 知识图谱 | Mermaid / Graphviz |
| 数据图 | matplotlib（Python 计算块）|

详见 [references/chart-guide.md](references/chart-guide.md)

---

## 核心职责 5：UI 视觉

界面/图标/布局规范设计。详见 [references/ui-guide.md](references/ui-guide.md)

---

## 核心职责 6：品牌视觉执行

配色规范、字体、品牌一致性。详见 [references/brand-guide.md](references/brand-guide.md) / [color-theory-guide.md](references/color-theory-guide.md)

---

## 核心职责 7：文档排版

排版优化、视觉呈现。详见 [references/doc-guide.md](references/doc-guide.md) / [typography-guide.md](references/typography-guide.md)

---

## 协作原则

1. **不原创教学内容**：仅呈现教员（instructor）提供的内容，不修改原意
2. **提交督导审核**：完成视觉设计后提交督导（auditor）质量终审
3. **遵循品牌规范**：在项目负责人定义的规范内执行
4. **不定义品牌配色**：品牌配色由项目负责人负责

---

## 关键路径

```
~/.openclaw/workspace/presenter/
├── IDENTITY.md                            身份配置（核心职责、工具原则）
├── SOUL.md                                风格/信念
├── MEMORY.md                              工作记忆 + 程序性规则
├── TOOLS.md                               工具速查
└── .agents/skills/presenter/              ← 你正在读这份的技能
    ├── SKILL.md                           单一综合技能入口
    ├── _meta.json
    ├── README.md
    ├── templates/                         PPT 模板（basic/lesson）
    │   ├── basic-pptx.qmd
    │   ├── basic-revealjs.qmd
    │   ├── lesson-pptx.qmd
    │   └── brand-template.pptx
    ├── examples/                          PPT 示例
    │   ├── demo-pptx.qmd
    │   ├── demo-revealjs.qmd
    │   └── demo-with-template.qmd
    ├── scripts/
    │   ├── render.sh                      Quarto 渲染小工具
    │   └── ppt/                           ⚠️ 旧 python-pptx 工具（DEPRECATED）
    ├── references/                        设计方法论指南
    │   ├── index.md                       导航
    │   ├── ppt-guide.md                   ⚠️ 旧 PPT 制作指南（已弃用）
    │   ├── script-writing-guide.md
    │   ├── image-guide.md / image-generation-guide.md
    │   ├── chart-guide.md
    │   ├── ui-guide.md
    │   ├── brand-guide.md
    │   ├── color-theory-guide.md
    │   ├── typography-guide.md
    │   ├── doc-guide.md
    │   ├── visual-hierarchy-guide.md
    │   ├── layout-choice-guide.md
    │   ├── slide-design-guide.md
    │   ├── quality-standards.md
    │   └── workflows.md
    ├── assets/
    ├── index/                             搜索索引
    └── mcp/                               MCP server
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.8.0 | 2026-06-04 | **真融合**：PPT 完整内容内联到主 SKILL.md；删除 `quarto-ppt/` 子目录；模板/示例/脚本扁平化到根 |
| v1.7.0 | 2026-06-04 | 收编 quarto-ppt 为子技能（浅层搬迁，**被 v1.8.0 否决**）|
| v1.6.0 | 2026-06-04 | 固化工具原则：PPT 一律用 Quarto（.qmd）|
| v1.5.0 | 2026-05-23 | 初版技能集（七大职责索引）|
