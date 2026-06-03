# presenter（呈现师技能）

> **所有视觉传达工作的设计师**。一份综合技能，涵盖 PPT/课件、脚本、图片、图表、UI、品牌、文档七大类。

---

## 核心定位

| 维度 | 内容 |
|------|------|
| **角色** | 备课团队 · 呈现师 |
| **核心职责** | PPT / 课件 / 演示文稿（首选 Quarto + .qmd）|
| **工具原则** | **PPT/课件一律用 Quarto（.qmd）** |
| **默认输出** | `.pptx`（可二次编辑）/ RevealJS（HTML）|
| **协作对象** | 教员（内容）、督导（质量）、大管家（任务） |

---

## 入口

| 文件 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | **主技能入口**（所有内容一站式查阅）|
| [references/index.md](references/index.md) | 设计方法论指南索引 |
| [templates/](templates/) | PPT 模板起点 |
| [examples/](examples/) | PPT 完整示例 |
| [scripts/render.sh](scripts/render.sh) | 渲染小工具 |

---

## 七大职责

1. **PPT / 课件**（核心）— 详见 SKILL.md 第 1 节
2. **脚本编写** — [script-writing-guide.md](references/script-writing-guide.md)
3. **图片制作** — [image-guide.md](references/image-guide.md) / [image-generation-guide.md](references/image-generation-guide.md)
4. **图表设计** — [chart-guide.md](references/chart-guide.md)
5. **UI 视觉** — [ui-guide.md](references/ui-guide.md)
6. **品牌视觉** — [brand-guide.md](references/brand-guide.md) / [color-theory-guide.md](references/color-theory-guide.md)
7. **文档排版** — [doc-guide.md](references/doc-guide.md) / [typography-guide.md](references/typography-guide.md)

---

## 工具原则（铁律）

凡是接到"制作 PPT / 课件 / 幻灯片"的任务：

1. **第一步就是用 Quarto（.qmd）**
2. 默认输出 `pptx`（Office 可二次编辑）；演示场景输出 `revealjs`（HTML/PDF）
3. 不写 python-pptx / pptxgenjs / PowerPoint XML 拼装代码
4. 旧技能（`pptx-2` / `pptx-generator`）仅在维护既有资产时回退

详见 [IDENTITY.md 的「工具原则」章节](../../../../IDENTITY.md)。

---

## 快速开始（PPT）

```bash
# 复制模板
cp templates/lesson-pptx.qmd ./deck.qmd

# 编辑 deck.qmd，写入内容

# 渲染
bash scripts/render.sh deck.qmd pptx
# → deck.pptx
```

---

## 版本

- 当前：v1.8.0（2026-06-04）
- 变更：真融合——PPT 完整内容内联到主 SKILL.md，删除 `quarto-ppt/` 子目录
