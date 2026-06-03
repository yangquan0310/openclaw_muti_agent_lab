---
name: presenter
description: >
  呈现师：所有视觉传达工作的设计师。
  核心职责是 PPT/课件/演示文稿制作（首选 Quarto + .qmd，输出 .pptx 或 RevealJS HTML）；
  兼顾脚本编写、图片制作、图表设计、UI 视觉、品牌视觉执行、文档排版。
  工具原则：PPT 一律用 Quarto，禁用 python-pptx / pptxgenjs 起步。
  当用户要求"做 PPT"、"做课件"、"做演示文稿"、"写脚本"、"做信息图"、"做海报"、"做流程图"、"做界面设计"等视觉任务时激活。
version: 1.9.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🎨
    requires:
      bins: ["quarto"]
---

# presenter（呈现师技能）

> **所有视觉传达工作的设计师**。L2 指令层：执行必需的指令在主文档，详细内容下沉到 `references/ppt/`。

---

## 1. 触发条件

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

## 2. 工具原则

### 铁律：PPT 一律用 Quarto

凡是接到"制作 PPT / 课件 / 幻灯片"的任务，**第一步就是用 Quarto（.qmd）**。

| 任务 | 工具 |
|------|------|
| **PPT/课件** | **Quarto（.qmd）** — 默认 `pptx`，演示场景 `revealjs` |
| 脚本 | Markdown（结构化） |
| 图片 | 图像生成 |
| 图表 | Mermaid / Graphviz / 静态图 |
| UI | Figma / 静态稿 |
| 品牌 | 按公司 brand.yml |
| 文档 | Quarto / pandoc |

**严禁**：
- ❌ 不用 python-pptx / pptxgenjs 起步
- ❌ 不写 PowerPoint XML 拼装代码
- ❌ 不在 `pptx-2` / `pptx-generator` 技能上做新工作

**回退旧工具**（必须满足其一）：维护既有 python-pptx 资产 / 客户要求保留旧 .pptx 宏 / 需要逐像素控制。

详见 IDENTITY.md「工具原则」章节。

---

## 3. 核心职责 1：PPT / 课件（默认 Quarto）

> 一切从 `.qmd` 出发，输出 `pptx`（可二次编辑）或 `revealjs`（HTML 演示文稿）。

### 3.1 速查决策表

| 场景 | 推荐格式 |
|------|----------|
| 给学员/老师二次编辑 | `pptx` |
| 内部技术分享、动画 | `revealjs` |
| 公司有现成 PPT 母版 | `pptx` + `reference-doc` |
| 代码 + 公式 + 图混合 | `revealjs` |
| 课程多页、图多 | `pptx` + 自定义模板 |
| 客户要 PDF | `revealjs` → 打印 PDF |
| 学员要 Word/PPT 批注 | `pptx` |

### 3.2 最小示例（速查）

**PPTX**：

```markdown
---
title: "我的课件"
format:
  pptx:
    incremental: true
    slide-level: 2
---

# 课程总览

## 第一页

- 要点 1
- 要点 2

## 两列

:::: {.columns}
::: {.column width="50%"}
左
:::
::: {.column width="50%"}
右
:::
::::

## 演讲者备注

::: {.notes}
给演讲者看的备注。
:::
```

**RevealJS**：

```markdown
---
title: "我的演示"
format:
  revealjs:
    theme: simple
    incremental: true
    slide-number: true
---

## 第一页

- 内容

## 第二页

公式 $E=mc^2$

```python
print("代码高亮")
```
```

### 3.3 核心语法速查

| 语法 | 用途 |
|------|------|
| `# 一级` | 分隔页（Section Header）|
| `## 二级` | 普通幻灯片 |
| `---` | 强制分隔 |
| `{.inverse}` | 反色背景 |
| `:::: {.columns}` `::: {.column}` | 两列 |
| `![图](path){width=80%}` | 图片 |
| `\| 列 \| 列 \|` | 表格 |
| `::: {.notes}` | 演讲者备注 |
| `::: {.fragment}` | 片段动画（revealjs）|
| `{background-image="..."}` | 背景图（revealjs）|

**完整语法**：[references/ppt/quarto-syntax.md](references/ppt/quarto-syntax.md)

### 3.4 主题与样式速查

**revealjs 内置 11 套**：`beige` `blood` `dark` `default` `dracula` `league` `moon` `night` `serif` `simple` `sky` `solarized`

```yaml
format:
  revealjs:
    theme: dracula
```

**pptx 套品牌母版**：

```yaml
format:
  pptx:
    reference-doc: assets/templates/brand-template.pptx
```

**详细文档**：[references/ppt/quarto-theme.md](references/ppt/quarto-theme.md)

### 3.5 命令行速查

```bash
quarto render deck.qmd --to pptx
quarto render deck.qmd --to revealjs
quarto render deck.qmd                 # 同时输出两种
quarto preview deck.qmd                # 实时预览

bash scripts/render.sh deck.qmd pptx      # 封装好的渲染
bash scripts/render.sh deck.qmd revealjs
bash scripts/render.sh deck.qmd both
```

**详细文档**：[references/ppt/ppt-workflow.md](references/ppt/ppt-workflow.md) 第 4 节

### 3.6 PPT 任务工作流（速查）

1. 选模板：复制 `assets/templates/{basic,lesson}-pptx.qmd`
2. 写内容：H2 分页、列表、两列、代码、公式、图片
3. 首次渲染：`quarto render deck.qmd --to pptx`
4. 调样式：revealjs 改 `custom.scss`；pptx 改 `assets/templates/brand-template.pptx`
5. 加演讲者备注：每页 `::: {.notes} :::`
6. 最终渲染：`bash scripts/render.sh deck.qmd both`
7. 交付 + 提交督导审核

**详细文档**：[references/ppt/ppt-workflow.md](references/ppt/ppt-workflow.md)

### 3.7 与 python-pptx 对比（速查）

| 维度 | Quarto | python-pptx |
|------|--------|-------------|
| 作者友好度 | ⭐⭐⭐⭐⭐ Markdown | ⭐⭐ Python API |
| 公式/代码/图表 | ⭐⭐⭐⭐⭐ 原生 | ⭐⭐ 需手动 |
| 可二次编辑 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 精确像素控制 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 主题复用 | ⭐⭐⭐⭐⭐ reference-doc | ⭐⭐ |
| Git diff 友好 | ⭐⭐⭐⭐⭐ | ⭐ |

**结论**：能用 Quarto 就用 Quarto。

**详细对比**：[references/ppt/quarto-vs-pptx.md](references/ppt/quarto-vs-pptx.md)

### 3.8 常见问题速查

| 问题 | 解决 |
|------|------|
| 中文乱码 | reference-doc 改字体 + YAML 加 `lang: zh-CN` |
| 配色丢失 | Pandoc 不读 SCSS；颜色在 reference-doc 里配 |
| 图片不显示 | 相对路径 + 远程 URL 带扩展名 |
| nbformat 报错 | `conda install jupyter nbformat` 或改纯语法高亮 |
| 同时输出两种 | YAML 写 `format: pptx: default, revealjs: default` |
| revealjs 打印 PDF | URL 加 `?print-pdf` 再打印 |

**详细 FAQ**：[references/ppt/quarto-faq.md](references/ppt/quarto-faq.md)

### 3.9 资产清单

**模板**（`assets/templates/`）：

| 文件 | 用途 |
|------|------|
| `basic-pptx.qmd` | 最小 PPTX 模板 |
| `basic-revealjs.qmd` | 最小 RevealJS 模板 |
| `lesson-pptx.qmd` | 课程用 PPTX 模板（封面+目录+章节+小结+思考题）|
| `brand-template.pptx` | PowerPoint 母版（可在 PowerPoint 里改色/字体）|
| `legacy-template.pptx` | 旧 python-pptx 时代的母版（仅历史参考）|

**示例**（`assets/examples/`）：

| 文件 | 用途 |
|------|------|
| `demo-pptx.qmd` | PPTX 完整示例 |
| `demo-revealjs.qmd` | RevealJS 完整示例 |
| `demo-with-template.qmd` | PPTX + reference-doc 示例 |

### 3.10 关键外部文档

- Quarto Presentations 概览：https://quarto.org/docs/presentations/
- PowerPoint 格式：https://quarto.org/docs/presentations/powerpoint.html
- RevealJS 格式：https://quarto.org/docs/presentations/revealjs/
- 主题定制：https://quarto.org/docs/presentations/revealjs/themes.html
- PPTX 选项参考：https://quarto.org/docs/reference/formats/presentations/pptx.html
- RevealJS 选项参考：https://quarto.org/docs/reference/formats/presentations/revealjs.html

---

## 4. 核心职责 2：脚本编写

输出 **.qmd**（Quarto Markdown）结构化脚本，描述每个画面的呈现方式。

详见 [references/script-writing-guide.md](references/script-writing-guide.md)

---

## 5. 核心职责 3：图片制作

| 类型 | 工具 | 输出 |
|------|------|------|
| 信息图 | 图像生成 | PNG/JPG |
| 插图 | 图像生成 | PNG/JPG |
| 海报 | 图像生成 + 排版 | PNG/PDF |

详见 [references/image-guide.md](references/image-guide.md) / [image-generation-guide.md](references/image-generation-guide.md)

---

## 6. 核心职责 4：图表设计

| 类型 | 工具 |
|------|------|
| 流程图 | Mermaid / Graphviz |
| 思维导图 | Markdown 嵌套列表 / Mermaid mindmap |
| 知识图谱 | Mermaid / Graphviz |
| 数据图 | matplotlib（Python 计算块）|

详见 [references/chart-guide.md](references/chart-guide.md)

---

## 7. 核心职责 5：UI 视觉

界面/图标/布局规范设计。详见 [references/ui-guide.md](references/ui-guide.md)

---

## 8. 核心职责 6：品牌视觉执行

配色规范、字体、品牌一致性。详见 [references/brand-guide.md](references/brand-guide.md) / [color-theory-guide.md](references/color-theory-guide.md)

---

## 9. 核心职责 7：文档排版

排版优化、视觉呈现。详见 [references/doc-guide.md](references/doc-guide.md) / [typography-guide.md](references/typography-guide.md)

---

## 10. 协作原则

1. **不原创教学内容**：仅呈现教员（instructor）提供的内容，不修改原意
2. **提交督导审核**：完成视觉设计后提交督导（auditor）质量终审
3. **遵循品牌规范**：在项目负责人定义的规范内执行
4. **不定义品牌配色**：品牌配色由项目负责人负责

---

## 11. 关键路径

```
~/.openclaw/workspace/presenter/
├── IDENTITY.md                            身份配置（核心职责、工具原则）
├── SOUL.md                                风格/信念
├── MEMORY.md                              工作记忆 + 程序性规则
├── TOOLS.md                               工具速查
└── .agents/skills/presenter/              ← 你正在读这份的技能
    ├── SKILL.md                           L2 指令层（<500 行）
    ├── _meta.json
    ├── README.md
    ├── assets/
    │   ├── templates/                     PPT 模板（4 个）
    │   │   ├── basic-pptx.qmd
    │   │   ├── basic-revealjs.qmd
    │   │   ├── lesson-pptx.qmd
    │   │   ├── brand-template.pptx
    │   │   └── legacy-template.pptx
    │   └── examples/                      PPT 示例（3 个）
    │       ├── demo-pptx.qmd
    │       ├── demo-revealjs.qmd
    │       └── demo-with-template.qmd
    ├── scripts/
    │   ├── render.sh                      Quarto 渲染小工具
    │   └── ppt/                           ⚠️ 旧 python-pptx（DEPRECATED）
    └── references/                        L3 资源层
        ├── index.md                       导航
        ├── guide.md                       技能使用指南
        ├── ppt/                           ← PPT 详细内容
        │   ├── quarto-syntax.md
        │   ├── quarto-theme.md
        │   ├── quarto-faq.md
        │   ├── quarto-vs-pptx.md
        │   └── ppt-workflow.md
        ├── ppt-guide.md                   ⚠️ 旧 PPT 制作指南（已弃用）
        ├── script-writing-guide.md
        ├── image-guide.md / image-generation-guide.md
        ├── chart-guide.md
        ├── ui-guide.md
        ├── brand-guide.md
        ├── color-theory-guide.md
        ├── typography-guide.md
        ├── doc-guide.md
        ├── visual-hierarchy-guide.md
        ├── layout-choice-guide.md
        ├── slide-design-guide.md
        ├── quality-standards.md
        └── workflows.md
```

---

## 12. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.9.0 | 2026-06-04 | **深度融合**：SKILL.md 精简到 <500 行（L2 指令层）；PPT 详细内容按主题拆到 `references/ppt/`；模板/示例入 `assets/`；按 skill-developer 的 L1/L2/L3 分层规范重构 |
| v1.8.0 | 2026-06-04 | 真融合：PPT 完整内容内联到主 SKILL.md（**被 v1.9.0 否决**，内联导致 612 行超限）|
| v1.7.0 | 2026-06-04 | 收编 quarto-ppt 为子技能（浅层搬迁，被 v1.8.0 否决）|
| v1.6.0 | 2026-06-04 | 固化工具原则：PPT 一律用 Quarto（.qmd）|
| v1.5.0 | 2026-05-23 | 初版技能集（七大职责索引）|
