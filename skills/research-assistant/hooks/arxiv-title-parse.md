# Hook: 解析 arXiv Atom API 返回值

> **触发**：用 `http://export.arxiv.org/api/query?id_list=<ARXIV_ID>` 拉论文元数据。
> **v5.13.4 触发**：Al-Kari (arXiv 2605.28864) 入库时 title 抓到 query string。

## arXiv Atom XML 结构

```xml
<feed>
  <title>arXiv Query: ...</title>          ← 顶层 title 是 query 描述（不要）
  <entry>
    <title>Correct Paper Title</title>    ← 论文 title 在 entry 内
    <author><name>X</name></author>
    <published>2026-05-22</published>
    <summary>Abstract</summary>
  </entry>
</feed>
```

## 正确 Python 解析

```python
import re
import urllib.request

with urllib.request.urlopen('http://export.arxiv.org/api/query?id_list=<ID>', timeout=15) as resp:
    xml = resp.read().decode('utf-8')

# 抓 entry 块（不是 feed 顶层）
entry_match = re.search(r'<entry>(.*?)</entry>', xml, re.DOTALL)
entry = entry_match.group(1) if entry_match else ''

title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL).group(1).strip()
authors = re.findall(r'<author>\s*<name>(.*?)</name>', entry)
published = re.search(r'<published>(.*?)</published>', entry).group(1)[:10]
abstract = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL).group(1).strip()
```

## 错误示例（v5.13.3 的 bug）

```python
# ❌ 错：抓了 feed 顶层 title
title = re.search(r'<title>(.*?)</title>', xml, re.DOTALL).group(1).strip()
# → "arXiv Query: search_query=&id_list=..."
```
