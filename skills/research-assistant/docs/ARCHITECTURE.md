# research-assistant v7.0.0 架构

> **版本**：v7.0.0 · **不兼容旧代码** · **结构**：7 模块 × 多态 × 统一配置

---

## 〇、工具定位

**research-assistant 是 agent 的工具箱，不是成品生产器。**

### 核心原则

1. **返回材料，不返成品**
   - 工具产出字段、列表、报告、抽取的段落
   - **不**产出完整笔记 / 综述 narrative
   - **不**攥写论文中的连贯段落

2. **给 agent 用，不是给用户用**
   - CLI 调用者是 agent（programmer / steward / 其他 agent）
   - 输出格式优先结构化（JSON / dict）

3. **工具不做的事**
   - ❌ 攥写笔记 / 综述 narrative
   - ❌ 调 LLM 替 agent 写作
   - ❌ 做研究决策（选题 / 选文 / 选角度）
   - ❌ 评估文献质量

4. **工具做的事**（明确边界）
   - 检索 / 下载 / 上传：搬运数据到三联动
   - 提取 / 索引 / 分类：从 source 抽字段
   - 列表 / 统计 / 一致性检查：返结构化报告

**最终 narrative（笔记 / 综述）的攥写者 = agent**。

---

## 一、模块与类

### 1.1 7 个模块（每个模块一个文件夹）

| # | 模块 | 一句话职责 |
|---|------|----------|
| 1 | `upload/` | 本地 PDF → Zotero + WebDAV + wiki source |
| 2 | `download/` | Zotero → WebDAV → wiki raw（默认 `--source zotero`）；SciHub → wiki/raw/papers（`--source scihub`，v6.0.7+ 绕过付费墙）|
| 3 | `search/` | 4 数据库检索（ABC + kwargs 多态）+ 路由/fallback |
| 4 | `maintain/` | wiki ↔ Zotero ↔ WebDAV 三方一致性 |
| 5 | `manage/` | wiki source 列表 CRUD |
| 6 | `summarize/` | 单篇笔记生成（抽字段） |
| 7 | `synthesize/` | 综述素材抽取（抽段落） |

### 1.2 类清单（15 个）

| 模块 | 类（数量） |
|------|-----------|
| `upload/` | `Uploader` (1) |
| `download/` | `Downloader`(ABC) · `ZoteroJianguoyunDownloader` · `SciHubDownloader`（v6.0.7+）· `PaperMetadata` (4) |
| `search/` | `BaseSearcher`(ABC) · `SemanticScholarSearcher` · `GoogleScholarSearcher` · `CnkiSearcher` · `ArxivSearcher` · `SearchManager` · `Paper` (7) |
| `maintain/` | `DriftChecker` (1) |
| `manage/` | `WikiSourceManager` (1) |
| `summarize/` | `Summarizer` (1) |
| `synthesize/` | `Synthesizer` (1) |
| **合计** | **15**（2 ABC + 2 dataclass + 11 普通类） |

### 1.3 CLI 公共方法（16 个，全部单字）

每个方法都是完整功能入口（agent 调一次即可完成任务）：

| 模块 | 公共方法（数量） |
|------|-------------|
| `upload/` | `upload()` (1) |
| `download/` | `fetch()` (1) |
| `search/` | `pick()` + `search()` (2) |
| `maintain/` | `check()` / `missing()` / `report()` / `graph()` (4) |
| `manage/` | `list()` / `get()` / `filter()` / `merge()` / `stats()` / `search()` (6) |
| `summarize/` | `summarize()` (1) |
| `synthesize/` | `extract()` (1) |
| **合计** | **15** |

### 1.4 跨模块共享

- `scripts/utils.py`：3 个工具函数（`load_config` / `parse_frontmatter` / `extract_field`）+ 5 个 wiki 路径常量
- `scripts/main.py`：CLI 入口（~120 行）

---

## 二、目录结构

```
scripts/
├── utils.py                  # 工具函数（跨模块共享）
├── config.json                # 统一配置
├── main.py                    # CLI 入口（~120 行）
│
├── upload/                    # 模块 1
│   └── __init__.py           # 类：Uploader
├── download/                  # 模块 2
│   ├── __init__.py           # 导出
│   ├── base.py               # Downloader (ABC)
│   ├── zotero_jianguoyun.py  # ZoteroJianguoyunDownloader（--source zotero）
│   ├── scihub.py             # SciHubDownloader（v6.0.7+，--source scihub，零依赖）
│   └── paper.py              # PaperMetadata dataclass
├── search/                    # 模块 3（ABC + kwargs 多态）
│   ├── __init__.py           # 导出
│   ├── base.py               # BaseSearcher (ABC) + Paper dataclass
│   ├── semantic_scholar.py   # SemanticScholarSearcher
│   ├── google_scholar.py     # GoogleScholarSearcher
│   ├── cnki.py               # CnkiSearcher
│   ├── arxiv.py              # ArxivSearcher
│   └── manager.py            # SearchManager
├── maintain/                  # 模块 4
│   └── __init__.py           # 类：DriftChecker
├── manage/                    # 模块 5
│   └── __init__.py           # 类：WikiSourceManager
├── summarize/                 # 模块 6
│   └── __init__.py           # 类：Summarizer
└── synthesize/                # 模块 7
    └── __init__.py           # 类：Synthesizer
```

**目录规则**：每个模块独立成文件夹；类默认放 `__init__.py`；复杂模块（search/download）按职责拆多个文件。

---

## 三、每个模块的类 + 方法

### 模块 1：`upload/`

**类**：`Uploader`

| 方法 | 作用 |
|------|------|
| `__init__(config: dict)` | 从 config 读 rclone_config + jianguoyun.remote_root + upload.agent_id_env |
| `upload(pdf_path, slug, doi, title, tags, skip_zotero, skip_webdav, skip_wiki) -> dict` | **主入口**：add_to_zotero + push_webdav + create_wiki_source |
| `_add_to_zotero(doi, tags) -> dict` | subprocess 调 zotero.py add-doi |
| `_push_webdav(pdf_path) -> dict` | rclone copyto 推 PDF |
| `_create_wiki_source(slug, pdf_path, zotero_meta, title) -> dict` | 写 wiki/sources/<slug>.md |
| `_humanize_title_from_filename(pdf_path) -> str` | 从 PDF 文件名解析 title |

---

### 模块 2：`download/`

#### `Downloader` (ABC)

| 方法 | 作用 |
|------|------|
| `find(identifier) -> PaperMetadata` | **abstract** |
| `pull(meta, dest_dir) -> Path` | **abstract** |
| `save(pdf, meta, dest_dir) -> Path` | **abstract** |
| `fetch(identifier, dest_dir, archive_dir) -> Path` | 完整流水线（基类实现：find + pull + save） |

#### `ZoteroJianguoyunDownloader(Downloader)`（`--source zotero`，默认）

| 方法 | 作用 |
|------|------|
| `__init__(config: dict, archive_dir: Path)` | 读 config.zotero + jianguoyun |
| `find(identifier) -> PaperMetadata` | DOI 走 API；8 字符 key 走 get |
| `pull(meta, dest_dir) -> Path` | WebDAV .zip → 解压 PDF → 清理 |
| `save(pdf, meta, dest_dir) -> Path` | 按命名约定归档 |
| `_build_md5_index()` | PROPFIND + .prop 反查表 |
| `_webdav_get(url, dest)` | 带 retry 的 GET |
| `_zotero_api(path)` | 带 retry 的 API GET |

#### `SciHubDownloader(Downloader)`（`--source scihub`，v6.0.7+ 新增）

| 方法 | 作用 |
|------|------|
| `__init__(config: dict, archive_dir: Path)` | 无需凭据（不读 Zotero/WebDAV 配置） |
| `find(identifier) -> PaperMetadata` | 仅支持 DOI；遍历 6 个 SciHub 镜像拿页面 `citation_*` meta |
| `pull(meta, dest_dir) -> Path` | `resolve_pdf(doi)` 拿 PDF URL → 流式下载；4 种状态（FOUND / NOT_FOUND+OA_LINK / MIRROR_ERROR / INVALID_INPUT） |
| `save(pdf, meta, dest_dir) -> Path` | 按命名约定归档到 `wiki/raw/papers`（默认） |
| `DEFAULT_ARCHIVE_DIR` | `"/root/.openclaw/wiki/raw/papers"` |
| **零依赖** | 仅用 Python stdlib（urllib / http / hashlib / json / base64） |
| **镜像** | `sci-hub.st / .ru / .se / .ren / .box / .workflow`（`SCIHUB_MIRRORS` 环境变量可覆盖） |
| **验证码** | 内置 ALTCHA 解码器（v1.0.3 起）；镜像弹验证码时自动解 |

#### `PaperMetadata` (dataclass)

| 字段 | 类型 |
|------|------|
| `zotero_item_key` / `zotero_attachment_key` | `str \| None` |
| `doi` / `arxiv_id` / `semantic_scholar_id` | `str \| None` |
| `title` | `str` |
| `authors` | `list[str]`（仅姓氏） |
| `year` / `month` / `day` | `int \| None` |
| `venue` | `str \| None` |
| `md5` / `source_url` | `str \| None` |
| `link_mode` | `str` |
| `archive_filename()` | **方法**：生成 `YYYY-MM[-DD]_作者_关键词_期刊.pdf` |
| `to_dict()` | **方法** |

---

### 模块 3：`search/`（ABC 统一接口 + kwargs 参数多态）

**类用 ABC**（`BaseSearcher` 提供统一接口约束）。
**方法统一签名** `def search(self, **kwargs) -> list[Paper]`（子类从 kwargs 解析自己关心的参数）。

#### `BaseSearcher` (ABC)

| 属性 / 方法 | 说明 |
|------|------|
| `name: ClassVar[str]` | 子类标识（`"semantic_scholar"` / `"cnki"` / ...） |
| `__init__(config: dict)` | |
| `search(**kwargs) -> list[Paper]` | **abstract** —— **真正的检索文献**，参数从 kwargs 解析。支持的 kwargs：<br>· `title` 标题（精确/模糊）<br>· `author` 作者<br>· `year` / `year_min` / `year_max` 年份<br>· `venue` 期刊/会议<br>· `doi` DOI 识别码<br>· `arxiv_id` arXiv 预印本编号<br>· `keyword` 关键词（搜标题+摘要）<br>· `limit` 最大结果数 |
| `__repr__()` | 调试用 |

#### 4 个 Searcher 子类（统一 `def search(**kwargs)`）

| 类 | 关心的 kwargs | 备注 |
|----|---------|------|
| `SemanticScholarSearcher` | `keyword` / `limit` / `year_min` / `year_max` | 调 SemSch API |
| `GoogleScholarSearcher` | `keyword` / `limit` / `year_min` / `year_max` | 0 结果时降级到 SemSch |
| `CnkiSearcher` | `keyword` / `limit` / `match` / `page` | 需 agent 注入 browser snapshot |
| `ArxivSearcher` | `keyword` / `limit` / `category` / `year_min` / `year_max` | 调 arXiv API |

**示例**（CNKI）：
```python
class CnkiSearcher(BaseSearcher):
    name = "cnki"

    def search(self, **kwargs) -> list[Paper]:
        keyword = kwargs.get("keyword", "")
        limit = kwargs.get("limit", 20)
        match = kwargs.get("match", "Contains")  # CNKI 独享
        page = kwargs.get("page", 1)             # CNKI 独享
        ...
```

#### `SearchManager`

| 方法 | 作用 |
|------|------|
| `__init__(config: dict)` | 实例化 4 个 searcher 进 `self.sources` dict |
| `search(source: str, **kwargs) -> list[Paper]` | **多态入口**：`source` 路由 + ABC 统一 `search(**kwargs)` |
| `search(keyword, limit, topic, year_min, year_max, write_report) -> dict` | **主入口**：自动路由 + fallback + 写 wiki report |
| `multi(sources: list[str], keyword, limit, **kwargs) -> dict[str, list[Paper]]` | 多源并行 |
| `_route(keyword) -> tuple[BaseSearcher, BaseSearcher \| None]` | 中文→CNKI / 数/物→arXiv / 英文→SemSch |
| `_report(papers, keyword, topic) -> Path` | 写 wiki/reports/<date>-search-<topic>.md |
| `_chinese(text)` | 中文判断 |
| `_arxiv(keyword)` | 数/物关键词启发式 |

**多态机制**：`SearchManager` 内部用 `dict[str, Searcher]` 索引 searcher 实例，通过 `source` 参数路由调用。
**类用 ABC 统一接口**：`BaseSearcher.search(**kwargs)` 强制所有子类实现统一签名。
**方法参数用 kwargs 解析**：子类从 `**kwargs` 中提取自己关心的参数（CNKI 取 `match`/`page`，arXiv 取 `category`），不破坏接口统一。

#### `SearchManager`（主入口）

| 方法 | 作用 |
|------|------|
| `__init__(config: dict)` | 实例化 4 个 searcher 进 `self.sources` dict |
| `pick(source: str \| None = None, **kwargs) -> BaseSearcher` | **选 source**：<br>· `source="cnki"` → 返回 CnkiSearcher 实例<br>· 无 source → 自动路由返回 primary searcher |
| `_route(keyword) -> tuple[Searcher, Searcher \| None]` | 中文→CNKI / 数/物→arXiv / 英文→SemSch |
| `_report(papers, keyword, topic) -> Path` | 写 wiki/reports/<date>-search-<topic>.md |
| `_chinese(text)` | 中文判断 |
| `_arxiv(keyword)` | 数/物关键词启发式 |

#### 4 个 Searcher 类（各自独立，不继承）

| 类 | 方法 | 备注 |
|----|---------|------|
| `SemanticScholarSearcher` | `search(keyword, year_min, year_max, limit) -> list[Paper]` | 调 SemSch API |
| `GoogleScholarSearcher` | `search(keyword, year_min, year_max, limit) -> list[Paper]` + `_parse_html(html)` | 0 结果时降级到 SemSch |
| `CnkiSearcher` | `search(keyword, limit, match, page) -> list[Paper]` + `parse_snapshot(keyword, snapshot_text)` | 需 agent 注入 browser snapshot |
| `ArxivSearcher` | `search(keyword, category, year_min, year_max, limit) -> list[Paper]` | 调 arXiv API |

#### `Paper` (dataclass)

| 字段 | 类型 |
|------|------|
| `title` | `str` |
| `authors` | `list[str]` |
| `year` | `int \| None` |
| `venue` | `str` |
| `doi` / `url` | `str` |
| `abstract` | `str` |
| `citation_count` | `int` |
| `external_ids` | `dict` |
| `source` | `str`（searcher.source_name） |
| `to_dict()` | **方法** |

---

### 模块 4：`maintain/`

**类**：`DriftChecker`

| 方法 | 作用 |
|------|------|
| `__init__(config: dict)` | 读 config.zotero + jianguoyun + wiki |
| `check() -> dict` | **主入口**：返回 `{ok, missing_key, zotero_not_found, webdav_missing, non_academic}` |
| `missing() -> list[dict]` | 缺 zotero_item_key 的 sources |
| `report(drift, output_path) -> Path` | 写 wiki/reports/wiki-zotero-drift-<date>.md |
| `graph(mode: "light"\|"full") -> str` | ASCII 状态图 |

---

### 模块 5：`manage/`

**类**：`WikiSourceManager`

| 方法 | 作用 |
|------|------|
| `__init__(config: dict)` | 读 config.wiki.root |
| `list() -> list[dict]` | 列出所有 source 摘要 |
| `get(source_id) -> dict` | 单篇详情（含完整 frontmatter） |
| `filter(conditions: dict) -> list[dict]` | 按 has_zotero_key / has_doi / pageType 筛 |
| `merge(source_ids: list[str]) -> list[dict]` | 按 zotero_item_key 去重 |
| `stats() -> dict` | 统计 total / with_zotero_key / by_pageType |
| `search(keyword: str) -> list[dict]` | 按 title 模糊搜索 |

---

### 模块 6：`summarize/`

**类**：`Summarizer`

| 方法 | 作用 |
|------|------|
| `__init__(config: dict)` | 读 config.wiki.root |
| `summarize(source_id, pdf_path, ocr) -> dict` | **主入口**：分类 + 评级 + 提取关键内容 → 写 wiki syntheses/<date>-summarize-<slug>.md |
| `_find_source(source_id) -> Path \| None` | 按 frontmatter id 字段匹配 |
| `_classify_type(content) -> str` | 规则分类（theorem > book > preprint-physics > review > preprint > paper） |
| `_calc_importance(content) -> str` | 规则评级（meta-analysis→5⭐） |
| `_extract_pdf(pdf_path, ocr) -> dict` | pypdf + pypdfium2 + tesseract |

---

### 模块 7：`synthesize/`

**类**：`Synthesizer`

| 方法 | 作用 |
|------|------|
| `__init__(config: dict)` | 读 config.wiki.root |
| `extract(source_id) -> dict` | **主入口**：从 body 抽"一句话总结" + "关键内容" → 写 wiki syntheses/<date>-extract-<slug>.md |
| `_find_source(source_id) -> Path \| None` | 同 Summarizer |

---

## 四、共享：`utils.py`

**不是类，是工具函数**。

| 函数 | 作用 |
|------|------|
| `load_config(path="scripts/config.json") -> dict` | 加载 config.json + 一次性解析 `${VAR}` 占位符 |
| `parse_frontmatter(content: str) -> tuple[dict, str]` | 解析 wiki 文件的 YAML 头 |
| `extract_field(content: str, field_name: str) -> str \| None` | 从 frontmatter 提取单字段 |

**路径常量**：
- `WIKI_ROOT = ~/.openclaw/wiki`
- `WIKI_SOURCES / WIKI_SYNTHESES / WIKI_CONCEPTS / WIKI_REPORTS / WIKI_RAW_PAPERS`
- `ensure_wiki_dirs()` —— 一次性 mkdir

---

## 五、main.py 设计（直接 import，不用反射）

```python
# 简化版（~120 行，vs v6.x 380 行）
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.utils import load_config


# === 7 个 cmd_xxx 函数，每个 ~10 行 ===
def cmd_upload(args, config): ...
def cmd_download(args, config): ...
def cmd_search(args, config): ...
def cmd_maintain(args, config): ...
def cmd_manage(args, config): ...
def cmd_summarize(args, config): ...
def cmd_synthesize(args, config): ...


# === argparse 分发 ===
def build_parser() -> argparse.ArgumentParser: ...


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = load_config("scripts/config.json")
    try:
        result = args.handler(args, config)
    except Exception as e:
        result = {"success": False, "error": str(e)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success", True) else 1


if __name__ == "__main__":
    sys.exit(main())
```

**关键点**：
- ✅ 直接 `import` 各模块的类
- ✅ 不动态注册、不反射
- ✅ 每个 cmd_xxx 函数显式对应一个模块
- ✅ 统一调 `args.handler(args, config)`，result 统一 JSON 输出

---

## 六、config.json 精简

**删**：`easy_scholar` / `storage` / `llm` 段（工具不调 LLM）
**新增**：`wiki.root` 段
**统一**：`xxx_env` 占位符字段

```json
{
  "semantic_scholar": { "api_key_env": "${SEMANTIC_SCHOLAR_API_KEY}", "request_interval": 0.5, "default_limit": 20 },
  "arxiv": { "request_interval": 3.0, "default_limit": 20 },
  "google_scholar": { "request_interval": 3.0, "hl": "zh-CN" },
  "cnki": { "request_interval": 3.0 },
  "zotero": { "user_id_env": "${ZOTERO_USER_ID}", "api_key_env": "${ZOTERO_API_KEY}" },
  "jianguoyun": { "url_env": "${JIANGUOYUN_URL}", "user_env": "${JIANGUOYUN_USER}", "password_env": "${JIANGUOYUN_PASSWORD}", "remote_root": "nutstore:quanquanzi/zotero" },
  "wiki": { "root": "~/.openclaw/wiki" },
  "upload": { "rclone_config": "~/.config/rclone/rclone.conf", "agent_id_env": "${OPENCLAW_AGENT_ID}" }
}
```

**8 段**：4 个 searcher 段 + 2 个三联动凭据段 + 1 个 wiki 段 + 1 个 upload 段。

---

## 七、删除清单（v6.x → v7.0.0）

| 删除 | 原因 |
|------|------|
| `Searcher.py`（shim） | 90% 重复 `SemSchSearcher` |
| `ZoteroSearcher.py`（内嵌 Searcher） | search→add-to-zotero 由 agent 显式串联 |
| `WikiSearchReport.py`（内嵌 Searcher） | `SearchManager.search` 接管 |
| `ZoteroAdder.py` | 合并到 `Uploader._add_to_zotero` |
| `BaseSearcher.KBAdapter` 抽象 | v7.0.0 全部走 wiki |
| `IndexJsonKBAdapter` / `WikiReportKBAdapter` | 不再需要 |
| `BaseSearcher.merge_to_kb` / `_load_kb` 等 | wiki 是单一后端 |
| `Synthesizer.check_references` / `fix_references` | 超出 v7.0.0 范围 |
| `cache/index.json` 旧知识库后端 | 不再使用 |
| 380 行 main.py + 6 个 `_run_xxx` | 简化到 ~120 行 |

**保留**：`BaseSearcher` (ABC) + `Downloader` (ABC)。search 方法统一签名为 `def search(**kwargs)`，子类各自解析 kwargs。

---

## 八、版本演进

| 版本 | 改动 |
|------|------|
| **v7.0.0** | 删 4 个 shim + 删 KBAdapter 抽象 + 统一 frontmatter 解析（utils.py）+ 统一 config 加载 + 简化 main.py（380→120 行）+ class 重命名（`Manager`→`WikiSourceManager`, `WikiZoteroManager`→`DriftChecker`） |

**不兼容点**：
- ✗ 旧类名 `Searcher` / `ZoteroSearcher` / `WikiSearchReport` / `ZoteroAdder` / `WikiZoteroManager` / `KBAdapter` 全删
- ✗ 旧 `cache/index.json` 不再使用
- ✗ config.json 段简化（删 `easy_scholar` / `storage` / `llm`）

---

**当前状态**：架构文档重写完成（精简版），等老板拍板后开始写代码。