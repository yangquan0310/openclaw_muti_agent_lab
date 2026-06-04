# presenter（呈现师技能）

> **所有视觉传达工作的设计师**。L2 指令层控制在 500 行内，详细内容下沉到 `references/`。

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
| [SKILL.md](SKILL.md) | **主技能入口**（L2 指令层，389 行）|
| [references/index.md](references/index.md) | L3 资源导航 |
| [assets/templates/](assets/templates/) | PPT 模板起点 |
| [assets/demos/](assets/demos/) | PPT 完整示例 |
| [scripts/render.sh](scripts/render.sh) | 渲染小工具 |

---

## 七大职责

1. **PPT / 课件**（核心）— SKILL.md 第 3 节 + [references/ppt/](references/ppt/)
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
cp assets/templates/lesson-pptx.qmd ./deck.qmd

# 编辑 deck.qmd，写入内容

# 渲染
bash scripts/render.sh deck.qmd pptx
# → deck.pptx
```

---

## 分层结构

按 skill-developer 的 L1/L2/L3 三层规范组织：

| 层 | 位置 | 内容 | 加载时机 |
|----|------|------|----------|
| **L1 元数据** | SKILL.md YAML | name + description | 启动时（注入 System Prompt）|
| **L2 指令** | SKILL.md 正文 | 速查表 + 核心指令 | 触发判断后 |
| **L3 资源** | references/ + assets/ + scripts/ | 详细内容、模板、脚本 | 按需读取 |

---

## 版本

- 当前：v1.9.0（2026-06-04）
- 变更：深度融合——按 L1/L2/L3 三层规范重构；SKILL.md 精简到 389 行；PPT 详细内容拆到 `references/ppt/`
