---
name: presenter
description: >
  呈现师：所有视觉传达工作的设计师。
  核心职责是 PPT/课件/演示文稿制作——**只**用 Quarto + .qmd，输出 .pptx 或 RevealJS HTML。
  后处理仅用 `scripts/build_brand_template.py` / `scripts/style_pptx_tables.py`（纯 zipfile XML，不是 python-pptx，不是生成器）。
  兼顾脚本编写、图片制作、图表设计、UI 视觉、品牌视觉执行、文档排版。
  工具原则：PPT 一律用 Quarto，**禁用** python-pptx / pptxgenjs 起步；旧 `scripts/ppt/` 已全量删档，无回退路径。
  当用户要求"做 PPT"、"做课件"、"做演示文稿"、"写脚本"、"做信息图"、"做海报"、"做流程图"、"做界面设计"等视觉任务时激活。
version: 1.11.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🎨
    requires:
      bins: ["quarto"]
---

# presenter（呈现师技能）

> **所有视觉传达工作的设计师**。L2 指令层：执行必需的指令在此，详细内容下沉到 `references/`。

---

## 核心原则

1. **呈现准确性**：忠实还原设计稿/内容，不歪曲、不遗漏
2. **工具锁定（铁律）**：PPT/课件**只**用 Quarto（.qmd），输出 `.pptx` 或 RevealJS HTML。**不做生成端 python-pptx**。`scripts/ppt/` 已全量删档，无回退路径
3. **职责清晰**：原创教学由教员负责，视觉呈现由呈现师负责，质量终审由督导负责
4. **L1/L2/L3 分层**：SKILL.md 只放 L2 速查 + 核心指令，详细内容按主题下沉到 `references/`
5. **约束优先于流程**：先界定边界（能做/不能做），再设计路径；不为了完整而完整

---

## 边界条件

### ✅ 能做

| 职责 | 工具/产物 |
|------|----------|
| PPT/课件/演示文稿 | Quarto（.qmd）→ `.pptx` 或 `.html` |
| 脚本编写 | 结构化 `.qmd` Markdown |
| 图片制作 | 图像生成工具 |
| 图表设计 | Mermaid / Graphviz / 静态图 |
| UI 视觉 | Figma / 静态稿 |
| 品牌视觉执行 | 按既定规范执行（不自定义）|
| 文档排版 | Quarto / pandoc |

### ❌ 不能做

| 职责 | 归属 |
|------|------|
| 原创核心教学内容 | 教员（instructor）|
| 交互逻辑设计 | 产品/项目负责人 |
| 自行定义品牌配色 | 项目负责人 |
| 功能代码实现 | 程序员 |
| 质量终审 | 督导（auditor）|
| 任务派发与跟踪 | 大管家（steward）|
| 课程内容设计 | 教员 |
| 技术方案评审 | 程序员 |
| 文字内容创作 | 写作助手 |
| 心理状态评估 | 心理学家 |

### 🚫 严禁事项

- ❌ 不用 python-pptx / pptxgenjs 起步（新工作）
- ❌ 不写 PowerPoint XML 拼装代码
- ❌ 不在 `pptx-2` / `pptx-generator` 技能上做新工作
- ❌ `scripts/ppt/` python-pptx 旧工具链（2026-06-04 已全量删档，不复存）

### 🚫 **无回退条件**

2026-06-04 后不设“回退到 python-pptx 生成”的合法路径。逐像素需求走：
- `scripts/build_brand_template.py`（生成品牌母版，**纯 zipfile XML**）
- `scripts/style_pptx_tables.py`（表格样式注入，**纯 zipfile XML**）

两者都不是 python-pptx，也不是 PPT 生成器，是 Quarto 输出的**后处理器**。

---

## 快速调用

### 1. 接到 PPT 任务

```bash
# 复制模板
cp assets/templates/lesson-pptx.qmd ./deck.qmd

# 编辑 deck.qmd（H2 分页、列表、两列、代码、公式、图片、备注）
```

### 2. 渲染

```bash
# 直接调 Quarto CLI（**不包装成 .sh**）
quarto render deck.qmd --to pptx
quarto render deck.qmd --to revealjs
quarto render deck.qmd                    # YAML 头部声明的 format 全渲
quarto preview deck.qmd                   # 热重载预览
quarto preview deck.qmd --to pptx         # 预览到指定格式
```

**完整 CLI 速查**：[references/ppt/quarto-cli-guide.md](references/ppt/quarto-cli-guide.md)

### 3. 套品牌母版

```yaml
# deck.qmd 的 YAML
format:
  pptx:
    reference-doc: assets/templates/brand-template.pptx
```

### 4. 同时输出两种格式

```yaml
format:
  pptx: default
  revealjs:
    theme: simple
```

### 5. 表格样式（重要）

Quarto pptx 输出使用 Office 默认 table style（`{5C22544A-...}` 灰底粗黑边），**YAML 和 reference-doc 都控制不了**。唯一可靠路径是渲染后注入 `<a:tcPr>`。

通过三段式 CLI 调用（封装在 `scripts/ppt/` 模块）：

```bash
# 母版装饰（一站式 / 微调）
presenter ppt template decorate deck.pptx -o deck_brand.pptx
presenter ppt template add-header deck.pptx -o deck.pptx --color 1F4E79
presenter ppt template set-fonts deck.pptx -o deck.pptx --chinese 微软雅黑
presenter ppt template set-theme-colors deck.pptx -o deck.pptx --accent1 1F4E79

# 表格样式
presenter ppt tables style deck_brand.pptx -o deck_styled.pptx
```

**或 Python API 调用**：
```python
from scripts.ppt import PPTXFile, TemplateEditor, TableStyler
ppt = PPTXFile("input.pptx").load()
TemplateEditor(ppt).decorate("output.pptx", header_color="0096C7")
TableStyler(PPTXFile("output.pptx").load()).style("final.pptx")
```

详细：[scripts/ppt/README.md](scripts/ppt/README.md) · [references/ppt/table-styling.md](references/ppt/table-styling.md)

### 6. 提交督导审核

完成视觉设计后，提交督导（auditor）做质量终审。

---

## 指南导航

### PPT 制作（核心职责）

| 指南 | 位置 | 内容 |
|------|------|------|
| 完整语法 | [references/ppt/quarto-syntax.md](references/ppt/quarto-syntax.md) | 分隔/列表/两列/代码/公式/图片/表格/备注/片段/背景/图表 |
| **CLI 速查** | [references/ppt/quarto-cli-guide.md](references/ppt/quarto-cli-guide.md) | **render / preview / 调试 / 装依赖（直接调 quarto，不包装）** |
| **表格样式** | [references/ppt/table-styling.md](references/ppt/table-styling.md) | **两段式渲染：Quarto + Python tcPr 注入（重要）** |
| 主题与样式 | [references/ppt/quarto-theme.md](references/ppt/quarto-theme.md) | revealjs 主题、SCSS、reference-doc |
| 15 个 FAQ | [references/ppt/quarto-faq.md](references/ppt/quarto-faq.md) | 中文乱码/字体/图片/慢渲染等 |
| **为什么只用 Quarto** | [references/ppt/quarto-vs-pptx.md](references/ppt/quarto-vs-pptx.md) | **Quarto-vs-python-pptx 选型史证** |
| 完整工作流 | [references/ppt/ppt-workflow.md](references/ppt/ppt-workflow.md) | 10 步工作流（决策→模板→编写→渲染→调样式→交付）|

### 脚本编写

| 指南 | 位置 |
|------|------|
| 脚本编写指南 | [references/script-writing-guide.md](references/script-writing-guide.md) |

### 图片 / 图表

| 指南 | 位置 |
|------|------|
| 图片制作 | [references/image-guide.md](references/image-guide.md) |
| 图片生成 | [references/image-generation-guide.md](references/image-generation-guide.md) |
| 图表设计 | [references/chart-guide.md](references/chart-guide.md) |

### 视觉方法论

| 指南 | 位置 |
|------|------|
| 配色方法论 | [references/color-theory-guide.md](references/color-theory-guide.md) |
| 排版方法论 | [references/typography-guide.md](references/typography-guide.md) |
| 视觉层级 | [references/visual-hierarchy-guide.md](references/visual-hierarchy-guide.md) |
| Layout 选择 | [references/layout-choice-guide.md](references/layout-choice-guide.md) |
| Slide 设计 | [references/slide-design-guide.md](references/slide-design-guide.md) |
| UI 视觉 | [references/ui-guide.md](references/ui-guide.md) |
| 品牌视觉 | [references/brand-guide.md](references/brand-guide.md) |
| 文档排版 | [references/doc-guide.md](references/doc-guide.md) |

### 质量与工作流

| 指南 | 位置 |
|------|------|
| 质量标准 | [references/quality-standards.md](references/quality-standards.md) |
| 工作流总览 | [references/workflows.md](references/workflows.md) |

### 总览

| 指南 | 位置 |
|------|------|
| 技能使用指南 | [references/guide.md](references/guide.md) |
| references 索引 | [references/index.md](references/index.md) |
| ⚠️ 旧 PPT 指南（已弃用）| [references/ppt-guide.md](references/ppt-guide.md) |

---

## 资产

按 **Quarto 编译所需资源类型**组织：

| 类型 | 位置 | 用途 | Quarto 调用 |
|------|------|------|-------------|
| 模板 | [assets/templates/](assets/templates/) | Quarto 骨架（.qmd）+ reference-doc 母版（.pptx）| `cp` 起步；`reference-doc: assets/templates/xxx.pptx` |
| 示例 | [assets/demos/](assets/demos/) | 完整可运行 .qmd | `cp` 参考写法 |
| 图片 | [assets/images/](assets/images/) | 可复用图片库 | `![](assets/images/xxx.png)` |
| 图表 | [assets/charts/](assets/charts/) | 静态图（PNG/SVG）或数据驱动 | `![](assets/charts/xxx.png)` |
| 字体 | [assets/fonts/](assets/fonts/) | 自定义字体（.ttf/.otf/.woff）| `src: url(assets/fonts/xxx.woff2)` |
| 样式 | [assets/styles/](assets/styles/) | 自定义 SCSS（revealjs 主题）| `theme: [default, assets/styles/xxx.scss]` |

**后处理**：

| 类型 | 位置 |
|------|------|
| **后处理（生成母版）** | [scripts/build_brand_template.py](scripts/build_brand_template.py) — **纯 zipfile XML**，不是 python-pptx |
| **后处理（表格样式）** | [scripts/style_pptx_tables.py](scripts/style_pptx_tables.py) — **纯 zipfile XML**，不是 python-pptx |

---

## 关键路径

```
~/.openclaw/workspace/presenter/
├── IDENTITY.md                    身份配置（核心职责、工具原则）
├── SOUL.md                        风格/信念
├── MEMORY.md                      工作记忆 + 程序性规则
├── TOOLS.md                       工具速查
└── .agents/skills/presenter/      ← 本技能根
    ├── SKILL.md                   你正在读这份（L2 指令层）
    ├── _meta.json
    ├── README.md
    ├── assets/                    L3 资产（按 Quarto 资源类型组织）
    │   ├── templates/             骨架（.qmd）+ reference-doc 母版（.pptx）
    │   ├── demos/                 完整示例 .qmd
    │   ├── images/                可复用图片
    │   ├── charts/                静态/数据图表
    │   ├── fonts/                 自定义字体
    │   └── styles/                自定义 SCSS（revealjs 主题）
    ├── scripts/                   L3 工具（2026-06-04 后无 .sh 包装）
    │   ├── main.py                     presenter CLI 统一入口（三段式）
    │   └── ppt/                       PPT 后处理模块
    │       ├── PPT.py                  PPTXFile 类（zipfile 包装）
    │       ├── Template.py             TemplateEditor（5 个母版装饰方法）
    │       ├── Tables.py               TableStyler（1 个表格样式方法）
    │       └── cli.py                  ppt 模块 CLI 调度
    └── references/                L3 资源
        ├── index.md
        ├── guide.md
        ├── ppt/                   PPT 详细文档
        │   ├── quarto-syntax.md
        │   ├── quarto-theme.md
        │   ├── quarto-faq.md
        │   ├── quarto-cli-guide.md
        │   ├── quarto-vs-pptx.md
        │   ├── table-styling.md
        │   └── ppt-workflow.md
        └── ...（14 篇设计方法论）
```

---

## 关键外部文档

- Quarto Presentations 概览：https://quarto.org/docs/presentations/
- PowerPoint 格式：https://quarto.org/docs/presentations/powerpoint.html
- RevealJS 格式：https://quarto.org/docs/presentations/revealjs/
- 主题定制：https://quarto.org/docs/presentations/revealjs/themes.html
- PPTX 选项参考：https://quarto.org/docs/reference/formats/presentations/pptx.html

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| **v1.10.0** | 2026-06-04 | **对齐 skill-developer 规范**：5 必含章节（核心原则/边界条件/快速调用/指南导航/版本历史）；把所有详细内容挪到 references/ |
| v1.9.0 | 2026-06-04 | 深度融合：L1/L2/L3 三层重构（**章节顺序不合规，被 v1.10.0 否决**）|
| v1.8.0 | 2026-06-04 | 真融合：PPT 完整内容内联到主 SKILL.md（被 v1.9.0 否决）|
| v1.7.0 | 2026-06-04 | 收编 quarto-ppt 为子技能（被 v1.8.0 否决）|
| v1.6.0 | 2026-06-04 | 固化工具原则：PPT 一律用 Quarto |
| v1.5.0 | 2026-05-23 | 初版技能集 |
