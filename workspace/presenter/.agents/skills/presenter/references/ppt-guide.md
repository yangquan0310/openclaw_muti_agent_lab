# PPT 制作指南

> ⚠️ **已弃用**（2026-06-04）：本指南描述的 PPT 脚本 + python-pptx 流程已停止维护。
>
> **新工作请用** [Quarto PPT 技能](../quarto-ppt/SKILL.md)（.qmd → .pptx / revealjs）
>
> 本文档保留作历史参考。`scripts/ppt/` 目录已标记为 DEPRECATED。
>
> 详见 IDENTITY.md「工具原则」。

---

> 从 PPT 脚本设计 → Layout 选择 → PPTX 编译的完整流程（**旧版**）

---

## 一、核心概念

| 概念 | 说明 |
|------|------|
| **slide_master** | 画布（背景、主题色、字体、页脚） |
| **slide_layout** | 画布 + 预置占位符 |
| **slide** | 编译器在画布上自主绘制的具体画面 |

**编译器行为**：根据 `@structure` 自主设计 slide 的呈现方式，Layout 只是提供画布和可选的占位符位置参考。

---

## 二、脚本编写（结构化格式）

详见 [脚本编写指南](script-writing-guide.md)

### 快速格式

```markdown
## 第N页：页面标题

@layout: 1          # 可选：强制指定布局索引
@structure: list    # 可选：声明内容结构类型

**页面描述**：页面功能一句话说明

**核心内容**：
- 要点1
- 要点2
- 要点3

**图表设计**：    # 可选
- 排版建议

**互动设计**：    # 可选
- 课堂活动/提问设计

**备注**：         # 可选
- 教学备注、时间控制
```

### 内容结构类型（@structure）

| 结构类型 | 标记 | 适用场景 |
|----------|------|----------|
| **列表** | `@list` | 标题+多个条目（最常用） |
| **表格** | `@table` | 多行多列对比数据 |
| **时间轴** | `@timeline` | 按时间顺序的事件 |
| **流程图** | `@flowchart` | 线性步骤、程序 |
| **对比** | `@compare` | 左右双栏对比 |
| **卡片** | `@cards` | 并列特征、分类归纳 |
| **封面** | `@cover` | 课程封面 |
| **章节分隔** | `@section` | 节标题过渡页 |

---

## 三、Layout 选择

详见 [Layout 选择指南](layout-choice-guide.md)

### 快速选择表

| 内容类型 | 推荐 Layout | 索引 |
|----------|-------------|------|
| **封面** | 标题幻灯片 | 0 |
| **章节分隔/过渡** | 节标题 | 2 |
| **双栏对比** | 两栏内容 | 3 |
| **其他所有结构** | 标题和内容 | 1 |
| **思考题/讨论** | 仅标题 | 5 |

---

## 四、编译命令

```bash
# 列出模板所有 slide_layouts
python3 scripts/ppt/main.py list --template template

# 验证脚本（编译前检查）
python3 scripts/ppt/main.py validate \
  --input script.md --template template

# 编译（默认蓝色主题）
python3 scripts/ppt/main.py compile \
  --input script.md --output out.pptx --template template

# 编译（指定主题）
python3 scripts/ppt/main.py compile \
  --input script.md --output out.pptx --template template \
  --theme purple

# 解析脚本（调试）
python3 scripts/ppt/main.py parse --input script.md
```

### 配色主题

支持 5 种配色主题：`blue`（默认）、`green`、`purple`、`orange`、`gray`。

主题也可在脚本元数据中指定（优先级高于命令行）：
```markdown
---
title: 演示文稿
theme: purple
---
```

---

## 五、设计原理

详见 [Slide 设计指南](slide-design-guide.md)，或深入学习：

| 指南 | 说明 |
|------|------|
| [配色方法论](color-theory-guide.md) | 如何选择配色方案 |
| [排版方法论](typography-guide.md) | 如何选择字体、设计版式 |
| [视觉层级方法论](visual-hierarchy-guide.md) | 如何设计信息优先级 |

### 设计速查

| 设计要素 | 推荐做法 |
|----------|----------|
| **配色** | 一个主导色（60-70%）+ 1-2 支持色 + 1 强调色 |
| **字体** | 标题 36-44pt Bold，正文 14-16pt |
| **间距** | 边距 0.5"，内容块间距 0.3-0.5" |
| **对齐** | 正文左对齐，标题可居中 |

---

## 六、质量检查

详见 [质量检查清单](quality-standards.md)

---

*最后更新：2026-05-21*
