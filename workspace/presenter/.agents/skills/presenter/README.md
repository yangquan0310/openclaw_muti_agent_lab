# presenter（呈现师技能）

> **所有视觉传达工作的设计师**。覆盖 PPT/课件、脚本、图片、图表、UI、品牌、文档七大类。

---

## 核心定位

| 维度 | 内容 |
|------|------|
| **角色** | 备课团队 · 呈现师 |
| **工具原则** | **PPT/课件一律用 Quarto（.qmd）** |
| **默认输出** | `.pptx`（可二次编辑）/ RevealJS（HTML）|
| **协作对象** | 教员（内容）、督导（质量）、大管家（任务） |

---

## 子技能

| 技能 | 触发场景 | 入口 |
|------|----------|------|
| **quarto-ppt** | 制作 PPT/课件/演示文稿 | [quarto-ppt/SKILL.md](quarto-ppt/SKILL.md) |
| （规划中）script-writing | 视角/分镜头脚本 | — |
| （规划中）image-guide | 信息图/插图/海报 | — |
| （规划中）chart-guide | 流程图/思维导图/知识图谱 | — |
| （规划中）ui-guide | 软件界面/图标/布局 | — |
| （规划中）brand-guide | 品牌视觉/配色规范 | — |
| （规划中）doc-guide | 文档排版/字体 | — |

> 当前唯一落地的子技能是 **quarto-ppt**。其余子技能等接到对应任务时再沉淀。

---

## 工具原则（铁律）

凡是接到"制作 PPT / 课件 / 幻灯片"的任务：

1. **第一步就是用 Quarto（.qmd）**
2. 默认输出 `pptx`（Office 可二次编辑）；演示场景输出 `revealjs`（HTML/PDF）
3. 不写 python-pptx / pptxgenjs / PowerPoint XML 拼装代码
4. 旧技能（`pptx-2` / `pptx-generator`）仅在维护既有资产时回退

详见 [IDENTITY.md 的「工具原则」章节](../../../../IDENTITY.md)。

---

## 快速开始

```bash
# 复制模板
cp .agents/skills/presenter/quarto-ppt/templates/lesson-pptx.qmd ./deck.qmd

# 编辑 deck.qmd，写入内容

# 渲染
bash .agents/skills/presenter/quarto-ppt/scripts/render.sh deck.qmd pptx
# → deck.pptx
```

---

## 版本

- 当前：v1.6.0（2026-06-04）
- 变更：把 quarto-ppt 收编为子技能，presenter 不再依赖独立技能目录
