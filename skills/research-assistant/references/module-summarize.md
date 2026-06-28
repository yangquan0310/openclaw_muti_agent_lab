# module-summarize.md（v7.0.0）

> summarize 模块：单篇笔记生成（基于规则分类 + 关键内容提取）

## 类清单

- `Summarizer` — 单一类

## 类 / 方法职责

| 方法 | 作用 |
|------|------|
| `__init__(cfg)` | 读 config.wiki.root |
| `summarize(source_id, pdf_path, ocr) -> dict` | **主入口**：分类 + 评级 + 提取关键内容 → 写 wiki syntheses/<date>-summarize-<slug>.md |
| `_classify(content) -> str` | 规则分类（theorem > book > preprint-physics > review > preprint > paper） |
| `_rate(content) -> str` | 规则评级（meta-analysis→5⭐） |
| `_extract_pdf(pdf_path, ocr) -> dict` | pypdf + 可选 pypdfium2 + tesseract |

## CLI 用法

```bash
# 基本笔记生成
python3 scripts/main.py summarize --source-id source.buzsaki-2002-hippocampal-theta

# 含 PDF 提取（pypdf 提文本）
python3 scripts/main.py summarize --source-id source.xxx --pdf-path /tmp/paper.pdf

# 启用 OCR（pypdfium2 + tesseract）
python3 scripts/main.py summarize --source-id source.xxx --pdf-path /tmp/paper.pdf --ocr
```

## 返回结构

```python
{
    "success": True,
    "output_path": "/root/.openclaw/wiki/syntheses/2026-06-28-...-summarize-xxx.md",
    "zotero_key": "BNA4WATT",
    "paper_type": "review",         # 规则分类结果
    "importance": "3⭐",
    "notes_chars": 259,
    "pdf_data": null,               # 或 PDF 提取数据
}
```

## 工具定位

summarize 返字段 + 路径，不攥写 narrative。**工具只做数据搬运**——笔记 narrative 由 agent 攥写。