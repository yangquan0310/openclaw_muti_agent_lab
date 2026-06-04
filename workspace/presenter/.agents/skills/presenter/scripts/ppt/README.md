# scripts/ppt/ — PPT 后处理模块

> **不是 python-pptx**——纯 Python zipfile + XML 操作。Quarto 输出的后处理器。

## 三段式 CLI

```
presenter <模块名> <方法名> [参数]
presenter ppt   <方法>      [参数]
```

### 模块：`ppt`

#### 方法组：`template`（母版装饰）

| 子方法 | 作用 | 关键参数 |
|--------|------|----------|
| `decorate` | 一站式（add-header + add-accent + set-cover + set-fonts + set-theme）| `--header-color 0096C7 --accent-color F4A261` |
| `add-header` | 加顶部色条 | `--color 0096C7 --height 274320 --label "..."` |
| `add-accent` | 加左侧色条 | `--color F4A261 --width 73152` |
| `set-cover` | 改封面布局（全色底 + 装饰块）| `--bg 0096C7 --accent F4A261` |
| `set-fonts` | 改 CJK / Latin 字体 | `--latin "Microsoft YaHei" --chinese "微软雅黑"` |
| `set-theme-colors` | 改主题色（accent1-6）| `--accent1 ... --accent2 ...` |

#### 方法组：`tables`（表格样式）

| 子方法 | 作用 | 关键参数 |
|--------|------|----------|
| `style` | 样式化所有表格（覆盖 Office 默认丑陋样式）| `--header-color 0096C7 --alt-row-color F8F9FA` |

## 典型工作流

### 1. 章节库标准（ch11 沿用的 teal+橙 风格）

```bash
# 生成端
quarto render ch14.pptx.qmd --to pptx

# 后处理：母版装饰 + 表格样式
presenter ppt template decorate ch14.pptx.pptx -o ch14_brand.pptx
presenter ppt tables style ch14_brand.pptx -o ch14_final.pptx
```

### 2. 章节库快速模式（默认参数）

```bash
quarto render ch14.pptx.qmd --to pptx
presenter ppt template decorate ch14.pptx.pptx -o ch14_brand.pptx
presenter ppt tables style ch14_brand.pptx -o ch14_final.pptx
```

### 3. 微调示例（不同色系）

```bash
# 深蓝+红 配色
presenter ppt template decorate ch14.pptx.pptx -o ch14.pptx \
  --header-color 1F4E79 --accent-color C00000

# 只加顶栏，不改其他
presenter ppt template add-header ch14.pptx.pptx -o ch14.pptx \
  --color 1F4E79

# 只改字体，不改其他
presenter ppt template set-fonts ch14.pptx.pptx -o ch14.pptx \
  --latin "Cascadia Code"
```

## Python API

```python
from scripts.ppt import PPTXFile, TemplateEditor, TableStyler

# 打开 .pptx
ppt = PPTXFile("input.pptx")
ppt.load()

# 看元信息
print(ppt.slide_count())         # 34
print(ppt.layout_count())        # 11
print(ppt.slides_with_tables())   # [5, 6, 10, 13, 18, 21, 24, 29, 31]
print(ppt.theme_colors())         # {'dk1': '#000000', 'accent1': '#0096C7', ...}
print(ppt.theme_fonts())          # {'major-latin': 'Microsoft YaHei', ...}

# 母版装饰
editor = TemplateEditor(ppt)
editor.decorate(
    "output.pptx",
    header_color="0096C7",
    accent_color="F4A261",
    latin_font="Microsoft YaHei",
    chinese_font="微软雅黑",
)

# 表格样式
ppt2 = PPTXFile("output.pptx")
ppt2.load()
styler = TableStyler(ppt2)
result = styler.style("final.pptx")
print(result)  # {'tables_styled': 9, 'slides': [5, 6, 10, 13, 18, 21, 24, 29, 31]}
```

## 设计原则

| 原则 | 实现 |
|------|------|
| 一个方法一个功能 | 5 个 template 子方法 + 1 个 tables 子方法，每个独立可调 |
| 不重叠 | decorate 是一站式，其余是单步微调 |
| 易链式 | 所有方法返回 output_path，支持 `\|` pipe + `&&` |
| 默认参数 | 大多数情况下只传 input + output 即可 |
| 透明 | 返回 dict / 打印 slide 列表，方便审计 |
| 不依赖 python-pptx | 纯 zipfile + XML，**不引第三方 pptx 库** |
| 不替代 Quarto | 这是后处理，生成端仍走 Quarto |

## 文件清单

```
scripts/ppt/
├── __init__.py        # 导出 PPTXFile, TemplateEditor, TableStyler
├── PPT.py             # PPTXFile 类（zipfile 包装 + 元信息查询）
├── Template.py        # TemplateEditor 类（5 个母版装饰方法）
├── Tables.py          # TableStyler 类（1 个表格样式方法）
├── cli.py             # 三段式 CLI 调度（presenter ppt ...）
└── README.md          # 本文件
```

## 之前 vs 现在

| 之前 | 现在 |
|------|------|
| `scripts/build_brand_template.py`（单文件）| `scripts/ppt/Template.py`（类） |
| `scripts/style_pptx_tables.py`（单文件）| `scripts/ppt/Tables.py`（类） |
| CLI 单一（只能做完整 decorate）| CLI 6 个子方法（细粒度微调） |
| Python 调用要读 CLI 参数 | 直接 `from scripts.ppt import TemplateEditor` |
| 无统一入口 | `presenter ppt ...` 三段式统一入口 |
