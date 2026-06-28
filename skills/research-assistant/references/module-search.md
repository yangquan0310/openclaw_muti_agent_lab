# module-search.md（v7.0.0）

> search 模块：4 个数据库的文献检索（ABC + kwargs 多态）

## 类清单

- `BaseSearcher` (ABC) — 抽象基类
- `SemanticScholarSearcher` — SemSch API
- `GoogleScholarSearcher` — Google Scholar（0 结果降级到 SemSch）
- `CnkiSearcher` — CNKI（依赖 browser snapshot 注入）
- `ArxivSearcher` — arXiv 预印本
- `SearchManager` — 编排器：选 source + 调 searcher 检索
- `Paper` (dataclass) — 标准化文献结构

## 类 / 方法职责

| 类 | 方法 | 作用 |
|----|------|------|
| `BaseSearcher` (ABC) | `search(**kwargs) -> list[Paper]` | abstract；统一签名，子类各自解析 kwargs |
| `SearchManager` | `pick(source, **kwargs) -> BaseSearcher` | 选 source（不调 API） |
| `SearchManager` | `search(**kwargs) -> dict` | 统一入口：自动路由 + fallback + 写 wiki report |

## CLI 用法

```bash
# 自动路由（中文→CNKI / 数/物→arXiv / 英文→SemSch）
python3 scripts/main.py search --keyword "深度学习" --limit 20

# 指定 source
python3 scripts/main.py search --keyword "deep learning" --source arxiv

# 多源并行
python3 scripts/main.py search --keyword "memory" --sources semantic_scholar,arxiv

# 不写 wiki report
python3 scripts/main.py search --keyword "deep learning" --dry-run
```

## kwargs 支持的文献字段

| 字段 | 说明 |
|------|------|
| `keyword` | 关键词（搜标题+摘要） |
| `title` | 标题 |
| `author` | 作者 |
| `year` / `year_min` / `year_max` | 年份 |
| `venue` | 期刊/会议 |
| `doi` | DOI 识别码 |
| `arxiv_id` | arXiv 编号 |
| `limit` | 最大结果数 |

## 工具定位

search 返 Paper 列表（dict 结构），不返 narrative。**真正的检索文献**是 searcher 子类的 `search(**kwargs)`，**SearchManager** 只管选 source。