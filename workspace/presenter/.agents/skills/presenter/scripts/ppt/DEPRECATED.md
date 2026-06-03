# ⚠️ DEPRECATED — python-pptx 编译工具链

> **状态**：已弃用。自 2026-06-04 起，呈现师 PPT 工作一律用 Quarto（.qmd）。
>
> **新工具位置**：[`../../quarto-ppt/`](../../quarto-ppt/)
>
> 详见 IDENTITY.md「工具原则」章节。

---

## 为什么弃用

| 旧方式 | 新方式 |
|--------|--------|
| `SlideScript.md` + `PptxCompiler.py` | `.qmd` + `quarto render` |
| `slide_master` / `slide_layout` / `slide` 三层抽象 | Pandoc reference-doc 直接复用 PPT 母版 |
| Python 拼装 XML | Markdown 写内容，Pandoc 编译 |
| 脚本化但难调试 | 标准 Markdown，Git diff 友好 |

---

## 文件清单（保留作历史参考，不再维护）

```
scripts/ppt/
├── main.py                  # 入口（弃用）
├── PptxCompiler.py          # python-pptx 编译器（弃用）
├── ScriptParser.py          # 旧脚本格式解析器（弃用）
├── LayoutImporter.py        # Layout 导入工具（弃用）
├── TemplateBuilder.py       # 母版生成（弃用）
├── TemplateExtractor.py     # 母版提取（弃用）
├── TemplateExtender.py      # 母版扩展（弃用）
└── __init__.py
```

---

## 旧工作流（已废弃）

```bash
# 旧：用结构化脚本 + python-pptx 编译
python scripts/ppt/main.py scripts/xxx.md -o output/xxx.pptx
```

## 新工作流

```bash
# 新：用 Quarto 渲染
quarto render deck.qmd --to pptx
# 或
bash quarto-ppt/scripts/render.sh deck.qmd pptx
```

---

## 何时仍可能用到旧代码

- **维护既有资产**：已经用旧流程生成的 .pptx 需要小修 → 改用 python-pptx 直接编辑
- **逐像素控制**：Quarto 表达不了 → 回退 python-pptx

但**新工作一律不再用本目录**。
