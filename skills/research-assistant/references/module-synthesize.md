# module-synthesize.md（v7.0.0）

> synthesize 模块：综述素材抽取（从 body 抽"一句话总结" + "关键内容"）

## 类清单

- `Synthesizer` — 单一类

## 类 / 方法职责

| 方法 | 作用 |
|------|------|
| `__init__(cfg)` | 读 config.wiki.root |
| `extract(source_id) -> dict` | **主入口**：从 source body 抽两段 → 写 wiki syntheses/<date>-extract-<slug>.md |

## CLI 用法

```bash
python3 scripts/main.py synthesize --source-id source.buzsaki-2002-hippocampal-theta
```

## 返回结构

```python
{
    "success": True,
    "output_path": "/root/.openclaw/wiki/syntheses/2026-06-28-...-extract-xxx.md",
    "zotero_key": "BNA4WATT",
    "zotero_doi": "10.1016/...",
    "summary_chars": 75,
    "key_content_chars": 259,
}
```

## 跟 summarize 的区别

| 维度 | summarize | synthesize |
|------|-----------|------------|
| 目的 | 单篇笔记生成 | 综述素材抽取 |
| 分类 | 规则分类（theorem/paper/...） | 不分类 |
| 评级 | 评级（⭐） | 不评级 |
| 输出命名 | `*-summarize-*.md` | `*-extract-*.md` |
| 场景 | 拿到一篇论文生成笔记 | 为综述准备素材 |

## 工具定位

synthesize 返字段 + 路径，不攥写 narrative。**工具只抽两段**——综述由 agent 用这些素材攥写。