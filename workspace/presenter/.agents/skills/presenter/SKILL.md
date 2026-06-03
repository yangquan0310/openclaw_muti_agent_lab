---
name: presenter
description: >
  呈现师的实践技能集。
  覆盖所有视觉传达工作：PPT/课件（首选 Quarto）、脚本编写、图片制作、图表设计、UI 视觉、品牌视觉执行、文档排版。
  当用户要求"做 PPT"、"做课件"、"做演示文稿"、"写脚本"、"做信息图"、"做海报"、"做流程图"、"做界面设计"等视觉任务时激活。
version: 1.7.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🎨
    requires:
      bins: ["quarto"]
---

# presenter（呈现师技能）

> **所有视觉传达工作的设计师**。工具原则：PPT/课件一律用 Quarto（.qmd），其余按场景选最佳工具。

---

## 触发条件

| 场景 | 触发关键词 |
|------|------------|
| PPT / 课件 | 做 PPT、做课件、做幻灯片、写 deck、写 presentation、生成 .pptx |
| 演示文稿 | 培训、技术分享、答辩、述职、汇报 |
| 脚本编写 | 写视角脚本、写分镜头、写演示脚本 |
| 图片 | 做信息图、做插图、做海报、做封面图 |
| 图表 | 流程图、思维导图、知识图谱、架构图 |
| UI 视觉 | 做界面、画图标、配色规范、视觉规范 |
| 品牌 | 配色、字体、Logo 布局、品牌一致性 |
| 文档排版 | 排版文档、调整字体、优化版式 |

---

## 核心原则

### 1. 工具锁定

| 任务 | 工具 | 备注 |
|------|------|------|
| **PPT/课件** | **Quarto（.qmd）** | 默认输出 `pptx`，演示场景 `revealjs` |
| 脚本 | Markdown（结构化）| 输出 .qmd 或 .md |
| 图片 | 图像生成工具 | 见子技能 |
| 图表 | Mermaid / Graphviz / 静态图 | 见子技能 |
| UI | Figma / 静态稿 | 见子技能 |
| 品牌 | 按公司 brand.yml | 见子技能 |
| 文档 | Quarto / pandoc | 见子技能 |

### 2. 不原创教学内容

仅**呈现**教员（instructor）提供的内容，不修改原意。如需修改，先回到教员确认。

### 3. 提交督导审核

完成视觉设计后，提交督导（auditor）做质量终审。

---

## 子技能索引

| 子技能 | 路径 | 状态 | 用途 |
|--------|------|------|------|
| **quarto-ppt** | [quarto-ppt/SKILL.md](quarto-ppt/SKILL.md) | ✅ 已落地 | Quarto 制作 PPT/课件/演示文稿 |
| script-writing | （规划中）| — | 视角/分镜头脚本 |
| image-guide | （规划中）| — | 信息图/插图/海报 |
| chart-guide | （规划中）| — | 流程图/思维导图 |
| ui-guide | （规划中）| — | UI 视觉 |
| brand-guide | （规划中）| — | 品牌视觉 |
| doc-guide | （规划中）| — | 文档排版 |

---

## 工作流（PPT 任务）

1. 收到任务：明确场景、目标受众、输出格式
2. 选模板：从 `quarto-ppt/templates/{basic,lesson}-pptx.qmd` 复制
3. 写内容：H2 分页、列表、两列、代码、公式、图片、备注
4. 首次渲染：`quarto render deck.qmd --to pptx`
5. 调样式：
   - revealjs → 写 `custom.scss`（颜色、字体）
   - pptx → 改 `templates/brand-template.pptx`（母版）
6. 加演讲者备注：每页 `::: {.notes} :::`
7. 最终渲染：`bash quarto-ppt/scripts/render.sh deck.qmd both`
8. 交付 + 提交督导审核

---

## 关键路径

```
presenter/
├── IDENTITY.md                            身份配置（核心职责、工具原则）
├── SOUL.md                                风格/信念
├── MEMORY.md                              工作记忆 + 程序性规则
├── TOOLS.md                               工具速查
└── .agents/skills/presenter/
    ├── SKILL.md                           ← 你正在读这份
    ├── _meta.json
    ├── README.md
    └── quarto-ppt/                        PPT 子技能（核心）
        ├── SKILL.md                       详细文档（12KB）
        ├── templates/
        │   ├── basic-pptx.qmd
        │   ├── basic-revealjs.qmd
        │   ├── lesson-pptx.qmd
        │   └── brand-template.pptx
        ├── examples/
        │   ├── demo-pptx.qmd
        │   ├── demo-revealjs.qmd
        │   └── demo-with-template.qmd
        └── scripts/
            └── render.sh                  渲染小工具
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.7.0 | 2026-06-04 | quarto-ppt 收编为子技能；删除 `~/.openclaw/skills/quarto-ppt/` 独立目录；`scripts/ppt/` 标 DEPRECATED |
| v1.6.0 | 2026-06-04 | 收编 quarto-ppt 为子技能；不再依赖 `~/.openclaw/skills/` 独立技能目录；新增「工具锁定」原则 |
| v1.5.0 | 2026-05-23 | 初版技能集（七大职责索引） |
