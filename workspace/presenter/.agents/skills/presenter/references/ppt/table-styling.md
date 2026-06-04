# pptx 表格样式工作流（v1）

> 来源：ch14 v9 实战（2026-06-04）—— Quarto 直接渲的 pptx 表格丑，原因是 Office 默认 table style（`{5C22544A-...}`），不是模板本身的问题。
> 此参考记录"两段式渲染"流程，已固化进 `scripts/`。

## 核心问题

Quarto 的 `pptx` 输出对表格样式的控制力极弱：

- **不能用 YAML 控制**：`format.pptx` 没有 `table-style` 这类选项
- **不能用 reference-doc 覆盖**：换母版也只能换 slide master 装饰，表格 cell 走 Office 默认 style
- **不能用 SCSS**：SCSS 只对 revealjs 生效，pptx 完全看不到

**唯一可靠路径**：渲染后用 Python 注入 `<a:tcPr>` 到每个 cell。

## 工具链

```
~/.openclaw/workspace/presenter/.agents/skills/presenter/scripts/
├── build_brand_template.py    # 从任意 .pptx 模板生成品牌母版（teal+橙 装饰 + 字体）
├── style_pptx_tables.py       # 后处理：给所有表格 cell 注入 tcPr（覆盖默认 style）
└── render-with-tables.sh      # 一步式：Quarto 渲 + 表格样式注入
```

对应模板：

```
~/.openclaw/workspace/presenter/.agents/skills/presenter/assets/templates/
├── brand-template.pptx                  # 原始空白 Office 母版（ch11 沿用）
└── brand-template-teal-orange.pptx     # 品牌化母版（teal #0096C7 + 橙 #F4A261 + YaHei 字体）
```

## 两段式流程

### Step 1: 渲染 pptx

```bash
quarto render chXX.pptx.qmd --to pptx
```

`.qmd` 头部必须指 reference-doc：
```yaml
format:
  pptx:
    reference-doc: /root/.openclaw/workspace/presenter/.agents/skills/presenter/assets/templates/brand-template-teal-orange.pptx
    incremental: false
    slide-level: 2
```

### Step 2: 表格样式注入

```bash
python3 ~/.openclaw/workspace/presenter/.agents/skills/presenter/scripts/style_pptx_tables.py \
  chXX.pptx \
  -o chXX_styled.pptx
```

默认输出（章节库品牌色）：
- 表头：`#0096C7` 底 + `#FFFFFF` 白字加粗 + 居中
- 隔行：`#F8F9FA` 浅灰（zebra 斑马纹）
- 数据行：`#FFFFFF` 白
- 边框：`#D0D0D0` 浅灰细线（6350 EMU ≈ 0.5pt）
- 单元格内边距：左右 91440 EMU（0.1"）/ 上下 45720 EMU（0.05"）
- 字体：Microsoft YaHei / 微软雅黑 11pt

### 一键版

```bash
bash ~/.openclaw/workspace/presenter/.agents/skills/presenter/scripts/render-with-tables.sh \
  chXX.pptx.qmd 14
```

## 自定义品牌色

```bash
python3 style_pptx_tables.py input.pptx -o output.pptx \
  --header-color 1F4E79 \
  --alt-row-color F2F2F2 \
  --border-color BFBFBF
```

或批量改母版：

```bash
python3 build_brand_template.py source.pptx -o new.pptx \
  --header-color 1F4E79 \
  --accent-color C00000 \
  --header-label "我的课程名"
```

## 工作量与陷阱

| 坑 | 解决 |
|----|----|
| 表格用 Office 默认 style，灰底粗黑边 | 注入 tcPr 覆盖 |
| 自闭 `<a:tcPr />` 标签 | 单独 regex 处理（`r'<a:tcPr\s*/>'`） |
| 母版装饰只在 master 层，slide 不带 | 用 build_brand_template.py 改 slide master + cover layout |
| theme 改了 colors 但 slide 不变 | Pandoc 不应用 theme 颜色到 slide 内容，必须 master 层装饰 |

## 历史

- **2026-06-04 ch14 v9** — 老板反馈"表格好丑"，首次落地两段式流程
- 之前 ch06-ch13 全部踩过这个坑，但当时手工一份份改，未来应统一走工具链

## 相关

- 母版选择与配色：见 `../brand-guide.md` / `../color-theory-guide.md`
- 模板与 SCSS 关系：见 `quarto-theme.md`（revealjs 路线）
- v6 → v7 → v8 → v9 演进细节：见 MEMORY.md "PPT 渲染" 段
