---
name: presenter
description: >
  呈现师：所有视觉传达工作的设计师。
  核心职责是 PPT/课件/演示文稿制作（首选 Quarto + .qmd，输出 .pptx 或 RevealJS HTML）；
  兼顾脚本编写、图片制作、图表设计、UI 视觉、品牌视觉执行、文档排版。
  工具原则：PPT 一律用 Quarto，禁用 python-pptx / pptxgenjs 起步。
  当用户要求"做 PPT"、"做课件"、"做演示文稿"、"写脚本"、"做信息图"、"做海报"、"做流程图"、"做界面设计"等视觉任务时激活。
version: 1.10.0
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
2. **工具锁定**：PPT/课件一律用 Quarto（.qmd），输出 `.pptx` 或 RevealJS HTML
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

### 🔁 回退旧工具（必须满足其一）

- 维护既有 python-pptx 资产（不再改用 .qmd 重写）
- 客户/教员明确要求保留旧 .pptx 模板里某个宏 / 嵌入式 VBA
- 需要逐像素控制且 Quarto reference-doc 表达不了

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
# 一键渲染（封装脚本）
bash scripts/render.sh deck.qmd pptx
bash scripts/render.sh deck.qmd revealjs
bash scripts/render.sh deck.qmd both

# 或直接用 Quarto
quarto render deck.qmd --to pptx
quarto render deck.qmd --to revealjs
quarto preview deck.qmd                  # 热重载预览
```

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

### 5. 提交督导审核

完成视觉设计后，提交督导（auditor）做质量终审。

---

## 指南导航

### PPT 制作（核心职责）

| 指南 | 位置 | 内容 |
|------|------|------|
| 完整语法 | [references/ppt/quarto-syntax.md](references/ppt/quarto-syntax.md) | 分隔/列表/两列/代码/公式/图片/表格/备注/片段/背景/图表 |
| 主题与样式 | [references/ppt/quarto-theme.md](references/ppt/quarto-theme.md) | revealjs 主题、SCSS、reference-doc |
| 15 个 FAQ | [references/ppt/quarto-faq.md](references/ppt/quarto-faq.md) | 中文乱码/字体/图片/慢渲染等 |
| 与 python-pptx 对比 | [references/ppt/quarto-vs-pptx.md](references/ppt/quarto-vs-pptx.md) | 工具选型 |
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

| 类型 | 位置 |
|------|------|
| 模板 | [assets/templates/](assets/templates/) — `basic-pptx.qmd` / `basic-revealjs.qmd` / `lesson-pptx.qmd` / `brand-template.pptx` / `legacy-template.pptx` |
| 示例 | [assets/examples/](assets/examples/) — `demo-pptx.qmd` / `demo-revealjs.qmd` / `demo-with-template.qmd` |
| 渲染脚本 | [scripts/render.sh](scripts/render.sh) |
| ⚠️ 旧 python-pptx 工具 | [scripts/ppt/](scripts/ppt/) — **DEPRECATED**，仅维护旧资产时用 |

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
    ├── assets/                    L3 资产
    │   ├── templates/
    │   └── examples/
    ├── scripts/                   L3 工具
    │   ├── render.sh
    │   └── ppt/                   ⚠️ DEPRECATED
    └── references/                L3 资源
        ├── index.md
        ├── guide.md
        ├── ppt/                   PPT 详细文档
        │   ├── quarto-syntax.md
        │   ├── quarto-theme.md
        │   ├── quarto-faq.md
        │   ├── quarto-vs-pptx.md
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
