# module-manage.md（v7.0.0）

> manage 模块：wiki source 列表 CRUD（只动 wiki，不调 Zotero / WebDAV）

## 类清单

- `WikiSourceManager` — 单一类

## 类 / 方法职责

| 方法 | 作用 |
|------|------|
| `__init__(cfg)` | 读 config.wiki.root |
| `list() -> list[dict]` | 列出所有 wiki source 摘要 |
| `get(source_id) -> dict` | 单篇详情（含完整 frontmatter） |
| `filter(conditions) -> list[dict]` | 按 `has_zotero_key` / `has_doi` / `pageType` 筛 |
| `merge(source_ids) -> list[dict]` | 按 zotero_item_key 去重 |
| `stats() -> dict` | 统计 total / with_zotero_key / by_pageType 等 |
| `search(keyword) -> list[dict]` | 按 title 模糊搜索 |

## CLI 用法

```bash
# 列表
python3 scripts/main.py manage list

# 统计
python3 scripts/main.py manage stats

# 单篇详情
python3 scripts/main.py manage get --source-id source.buzsaki-2002-hippocampal-theta

# 按条件筛
python3 scripts/main.py manage filter --has-zotero-key true
python3 scripts/main.py manage filter --has-doi true
python3 scripts/main.py manage filter --page-type source

# 合并重复
python3 scripts/main.py manage merge --inputs source.a,source.b

# 按 title 搜索
python3 scripts/main.py manage search --keyword "deep learning"
```

## 工具定位

manage 是 wiki 知识库的"ls / grep / cat / wc"——只动 wiki，不调 Zotero / WebDAV。

跟 maintain 的区别：
- **manage** = wiki 内部 CRUD
- **maintain** = 跨三方一致性检查