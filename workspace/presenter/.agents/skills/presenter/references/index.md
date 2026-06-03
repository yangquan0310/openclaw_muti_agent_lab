# 索引

> presenter 技能设计方法论指南导航。PPT 制作内容已内联在 [主 SKILL.md](../SKILL.md) 第 1 节。

---

## 快速导航

### 技能总览
| 入口 | 说明 |
|------|------|
| [主技能入口](../SKILL.md) | 呈现师综合技能（v1.8.0，**含 PPT 完整内容**）|
| [使用指南](guide.md) | 技能使用概述、触发条件 |

### PPT 制作
**直接看 [主 SKILL.md 第 1 节](../SKILL.md#核心职责-1ppt--课件默认-quarto)**——所有 PPT 内容已内联。

> 配套资产：
> - [templates/](../templates/) — basic-pptx / basic-revealjs / lesson-pptx / brand-template.pptx
> - [examples/](../examples/) — demo-pptx / demo-revealjs / demo-with-template
> - [scripts/render.sh](../scripts/render.sh) — 渲染小工具
>
> ⚠️ [旧 PPT 制作指南](ppt-guide.md)（python-pptx 流程）已弃用，仅作历史参考。

### 脚本编写
| 指南 | 说明 |
|------|------|
| [脚本编写指南](script-writing-guide.md) | 视角/分镜头脚本；当前输出 **.qmd** |

### 设计方法论（工具无关）
| 指南 | 说明 |
|------|------|
| [Layout 选择指南](layout-choice-guide.md) | 4 种路径查找合适的 Layout（适用于 PPT 与文档）|
| [Slide 设计指南](slide-design-guide.md) | 颜色、逻辑、重点、层级设计规范 |
| [配色方法论](color-theory-guide.md) | 如何为可视化选择合适的配色方案 |
| [排版方法论](typography-guide.md) | 如何选择字体和设计版式 |
| [视觉层级方法论](visual-hierarchy-guide.md) | 如何设计信息的优先级和呈现顺序 |
| [图片生成方法论](image-generation-guide.md) | 如何使用 AI 图片生成模型创建可视化素材 |
| [品牌视觉指南](brand-guide.md) | 品牌一致性执行 |
| [UI 视觉指南](ui-guide.md) | 界面/图标/布局规范 |
| [文档排版指南](doc-guide.md) | 文档排版与视觉呈现 |

### 其他可视化
| 指南 | 说明 |
|------|------|
| [图片制作指南](image-guide.md) | 信息图、插图、海报设计 |
| [图表设计指南](chart-guide.md) | 流程图、思维导图、知识图谱 |

### 质量保障
| 指南 | 说明 |
|------|------|
| [质量检查清单](quality-standards.md) | 交付物质量检查 |

---

## 按场景查找

**制作 PPT（默认 Quarto）**
1. 看 [主 SKILL.md 第 1 节](../SKILL.md#核心职责-1ppt--课件默认-quarto)
2. 复制 `templates/lesson-pptx.qmd` 起步
3. 调样式参考 [Slide 设计指南](slide-design-guide.md)
4. 验收参考 [质量检查清单](quality-standards.md)

**编写脚本**
1. [脚本编写指南](script-writing-guide.md)（输出 .qmd）

**提升设计水平**
1. [配色方法论](color-theory-guide.md)
2. [排版方法论](typography-guide.md)
3. [视觉层级方法论](visual-hierarchy-guide.md)

**制作图片/图表**
1. [图片制作指南](image-guide.md) / [图片生成方法论](image-generation-guide.md)
2. [图表设计指南](chart-guide.md)
3. [质量检查清单](quality-standards.md)

---

## 设计理念

> **约束 > 流程**，**目的 > 形式**，**进化 > 固化**

- **约束**：每种可视化类型都有明确的边界
- **目的**：解决问题，而非万能工具
- **进化**：随使用迭代优化

---

## 核心原则速查

| 原则 | 说明 |
|------|------|
| **一图胜千言** | 好的可视化胜过千言万言 |
| **留白是设计** | 信息密度与呼吸感同样重要 |
| **一致性建立信任** | 统一的视觉语言让内容更专业 |
| **呈现服务于理解** | 所有设计都为了让知识更易懂 |
| **工具服务于内容** | 锁定 Quarto 作为 PPT 默认工具，让创作回归思考本身 |

---

*点击标题跳转对应指南*

---

> 最近更新：2026-06-04 — PPT 入口改指主 SKILL.md 第 1 节（不再单独成子技能）
