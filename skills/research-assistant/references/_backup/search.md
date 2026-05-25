# 文献检索模块 (Searcher)

Searcher 类负责从 Semantic Scholar 获取文献数据，支持多主题多轮检索，每轮可单独设置条件。

## 快速开始

### 我想...

| 需求 | 方法 |
|------|------|
| 检索新文献（英文） | [`search()`](#1-检索文献) |
| 检索新文献（中文） | [CNKI 浏览器自动化](#cnki-中文检索) |
| 更新已有知识库 | [`update()`](#2-更新知识库元数据) |

## 文件说明

| 文件 | 功能 |
|------|------|
| `Searcher.py` | 文献检索主类（英文，Semantic Scholar）|
| `CNKISearcher.py` | 知网检索主类（中文，浏览器自动化）|
| `检索报告模板.md` | 检索报告模板 |

---

## CNKI 中文检索（浏览器自动化方案）

> CNKI（中国知网）检索使用**浏览器自动化方案**：
> 通过 OpenClaw 内置浏览器访问 `search.cnki.com.cn`，抓取渲染后的页面 DOM，解析为标准化文献数据。
> 不依赖知网 API（KNS8S 接口有反爬限制，直接请求会返回 403）。

### 工作流

```
AI 代理 + browser 工具
    ↓  1. browser.navigate(url)
    ↓  2. browser.snapshot() → 渲染后的页面文本
CNKISearcher.parse_snapshot(snapshot_text)
    ↓  提取标题/作者/期刊/年份/关键词/被引数
BrowserCNKISearcher.normalize_batch()
    ↓  转为 index.json 标准格式
BrowserCNKISearcher.merge_to_kb()
    ↓  写入知识库文件
```

### 第一步：构造搜索 URL

```python
from search.CNKISearcher import BrowserCNKISearcher

searcher = BrowserCNKISearcher(kb_path="knowledge/index.json")
url = searcher.build_search_url(
    keyword="深度学习",   # 搜索关键词
    order=0,              # 0=相关度  1=发表时间  2=被引量
    page=1,               # 页码
    match="Contains",    # Contains=模糊  Exact=精确
)
# → https://search.cnki.com.cn/Search/Result?SearchWord=深度学习&Match=Contains&Order=0&Page=1
```

### 第二步：浏览器访问并抓取快照

在 OpenClaw 中使用 browser 工具：

```
# 1. 打开搜索结果页
browser.navigate(targetUrl="https://search.cnki.com.cn/Search/Result?SearchWord=深度学习&Match=Contains&Order=0&Page=1")

# 2. 等待页面加载完成后获取快照
browser.snapshot(refs="aria", compact=true, depth=3, maxChars=2000)

# 3. 将 snapshot 返回的原始文本保存为文件（或直接传给 Python）
```

### 第三步：解析快照并写入知识库

```python
from search.CNKISearcher import BrowserCNKISearcher

searcher = BrowserCNKISearcher(kb_path="knowledge/index.json")

# 读取浏览器快照文件
with open("snapshot_cnki.txt", "r", encoding="utf-8") as f:
    snapshot_text = f.read()

# 解析快照，提取文献列表
results = searcher.parse_snapshot(snapshot_text, topic="深度学习")
print(f"解析到 {len(results)} 条 CNKI 文献")

# 标准化并合并到知识库
papers = searcher.normalize_batch(results, topic="深度学习")
kb = searcher.merge_to_kb(papers)
stats = kb["statistics"]
print(f"知识库：共 {stats['total_count']} 篇（CNKI: {stats['cnki_count']} 篇）")
```

### 完整 CLI 管道

```bash
# 保存快照后，一行命令完成解析+写入
python3 -m scripts.search.CNKISearcher parse \
    --snapshot snapshot_cnki.txt \
    --topic "深度学习" \
    --kb-path knowledge/index.json \
    --output
```

### CNKI 快照字段说明

| accessibility tree 特征 | 对应字段 |
|------------------------|---------|
| 标题行含 `CNKI文献` | paper.title |
| 标题行 URL | paper.url |
| 标题后紧跟的姓名行 | paper.authors |
| `《期刊名》202X年` | paper.venue + paper.year |
| `被引（数字）` | paper.citationCount |
| `下载（数字）` | _cnki_download_count |
| `/` 分隔的短行 | paper._cnki_keywords |
| 长段落（>30字）紧跟标题 | paper.abstract |

### 注意事项

- **搜索入口**：`search.cnki.com.cn`（无需登录，结果较全）
- **翻页**：手动修改 URL 中的 `Page=N`，多页需多次抓取
- **排序**：`Order=0`（相关度）/ `Order=1`（发表时间）/ `Order=2`（被引量）
- **精确匹配**：`Match=Exact`，模糊：`Match=Contains`
- **防反爬**：两次搜索间建议间隔 3-5 秒
- **抓取限制**：知网对单 IP 请求频率有限制，批量抓取请控制节奏

### 知网 vs Semantic Scholar 对比

| 维度 | CNKI（知网） | Semantic Scholar |
|------|-------------|-----------------|
| 内容 | 中文期刊/学位论文/会议等 | 英文为主的全球学术文献 |
| 入口 | search.cnki.com.cn | api.semanticscholar.org |
| 抓取方式 | 浏览器 DOM 解析 | REST API（需 API Key） |
| 数据字段 | 标题/作者/期刊/年份/关键词/被引/下载 | 标题/作者/年份/摘要/DOI/引用量 |
| 适用场景 | 中文文献调研、文献综述 | 英文前沿研究调研 |

---

## 工作流示例

### 1. 检索文献

#### 第一步：确定检索条件
检索条件是一个字典。键是主题，list是检索内容，list的长度是检索次数。每次都应可以设置详细的检索条件，包括检索关键词、检索数量、年份范围、最小引用量、期刊/会议名称、研究领域、文献类型。详见检索规则小节。
```json
{
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30},
        {"query": "\"self-memory system\" Conway", "year": "2010-2025"},
        {"query": "autobiographical memory -childhood", "minCitationCount": 50}
    ],
    "数字记忆": [
        {"query": "digital memory | Google effect", "limit": 20},
        {"query": "photo taking memory", "year": "2020-2025", "minCitationCount": 20}
    ]
}
```

#### 第二步：执行检索
- 使用Searcher完成检索
```python
from search.Searcher import Searcher

# 初始化时绑定知识库路径
searcher = Searcher(kb_path="my_kb.json")
queries = {
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30},
        {"query": "\"self-memory system\" Conway", "year": "2010-2025"},
        {"query": "autobiographical memory -childhood", "minCitationCount": 50}
    ],
    "数字记忆": [
        {"query": "digital memory | Google effect", "limit": 20},
        {"query": "photo taking memory", "year": "2020-2025", "minCitationCount": 20}
    ]
}
# 方法调用时不再传知识库路径
kb = searcher.search(queries)
```
- 根据`/knowledge/retrieval_report/{标题}.md`给出检索报告
- 把检索报告保存在`knowledge/retrieval_report/{标题}.md`中
### 2. 更新知识库元数据
```python
from search.Searcher import Searcher

# 初始化时绑定知识库路径
searcher = Searcher(kb_path="my_kb.json")
# 方法调用时不再传知识库路径
kb = searcher.update()
```

---

## 方法详情

### `search(queries, fields=None, deduplicate=True, **global_params)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `queries` | Dict[str, List[Dict]] | 必填 | 多主题字典，格式 `{主题名: [条件字典列表]}` |
| `fields` | str | None | 返回字段，默认使用类属性 FIELDS |
| `deduplicate` | bool | True | 是否对结果去重（基于 paperId） |
| `**global_params` | - | - | 全局默认参数（会被条件字典中的同名字段覆盖） |

> **注意**：`kb_path` 在初始化 `Searcher(kb_path="...")` 时设置，不在 `search()` 方法中传入。

#### queries.list中的字典支持的字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `query` | str | **必填**，检索关键词 |
| `limit` | int | 本次检索数量（默认 20，最大 100） |
| `year` | str | 年份范围，如 `"2020-2023"` |
| `minCitationCount` | int | **客户端过滤**，最小引用量 |
| `venue` | str | 期刊/会议名称 |
| `fields_of_study` | str | 研究领域 |
| `publication_types` | str | 文献类型 |

### `update(fields=None)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `fields` | str | None | 请求字段，默认使用类属性 FIELDS |

> **注意**：`kb_path` 在初始化 `Searcher(kb_path="...")` 时设置，不在 `update()` 方法中传入。

---

## 检索规则

### query语法

| 语法 | 说明 | 示例 |
|------|------|------|
| **空格** | AND 关系（必须同时出现） | `autobiographical memory self` |
| `\|` | OR 关系（任一即可） | `autobiographical memory \| personal memory` |
| `\"\"` | 精确短语匹配 | `\"self-memory system\"` |
| `-` | NOT 关系（排除） | `autobiographical memory -childhood` |
| `()` | 优先级组合 | `(autobiographical \| personal) memory (self \| identity)` |

**使用示例**：
```json
{
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30},
        {"query": "\"self-memory system\" Conway", "year": "2010-2025"},
        {"query": "autobiographical memory -childhood", "minCitationCount": 50}
    ],
    "数字记忆": [
        {"query": "digital memory | Google effect", "limit": 20},
        {"query": "photo taking memory", "year": "2020-2025", "minCitationCount": 20}
    ]
}
```

### fields_of_study

| 研究领域 | 说明 |
|----------|------|
| `Computer Science` | 计算机科学 |
| `Medicine` | 医学 |
| `Chemistry` | 化学 |
| `Biology` | 生物学 |
| `Materials Science` | 材料科学 |
| `Physics` | 物理学 |
| `Geology` | 地质学 |
| `Psychology` | 心理学 |
| `Art` | 艺术 |
| `History` | 历史学 |
| `Geography` | 地理学 |
| `Sociology` | 社会学 |
| `Business` | 商学 |
| `Political Science` | 政治学 |
| `Economics` | 经济学 |
| `Philosophy` | 哲学 |
| `Mathematics` | 数学 |
| `Engineering` | 工程学 |
| `Environmental Science` | 环境科学 |
| `Agricultural and Food Sciences` | 农业与食品科学 |
| `Education` | 教育学 |
| `Law` | 法学 |
| `Linguistics` | 语言学 |

**使用示例**：
```json
{
    "自传体记忆": [
        {"query": "autobiographical memory", "fields_of_study": "Psychology", "limit": 30}
    ]
}
```

### publication_types

| 文献类型 | 说明 |
|----------|------|
| `Review` | 综述 |
| `JournalArticle` | 期刊论文 |
| `CaseReport` | 病例报告 |
| `ClinicalTrial` | 临床试验 |
| `Conference` | 会议论文 |
| `Dataset` | 数据集 |
| `Editorial` | 社论 |
| `LettersAndComments` | 信件与评论 |
| `MetaAnalysis` | 元分析 |
| `News` | 新闻 |
| `Study` | 研究报告 |
| `Book` | 书籍 |
| `BookSection` | 书籍章节 |

**使用示例**：
```json
{
    "自传体记忆": [
        {"query": "autobiographical memory", "publication_types": "Review,MetaAnalysis", "limit": 30}
    ]
}
```
---

## 命令行工具

### 检索文献
```bash
# 1. 创建检索条件 JSON 文件
cat > queries.json << 'EOF'
{
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30}
    ]
}
EOF

# 2. 执行检索（初始化时绑定知识库路径）
python3 Searcher.py search \
    --queries queries.json \
    --kb-path my_kb.json
```

### 更新知识库元数据
```bash
# 更新元数据（初始化时绑定知识库路径）
python3 Searcher.py update \
    --kb-path my_kb.json
```

### 命令参数
| 参数 | 说明 |
|------|------|
| `search` | 检索子命令 |
| `--queries` | 检索条件JSON文件（必填） |
| `--kb-path` | 知识库文件路径（默认: index.json） |
| `--fields` | 请求字段（可选） |
| `--no-deduplicate` | 不去重 |
| `update` | 更新元数据子命令 |
| `--kb-path` | 知识库文件路径（默认: index.json） |
| `--fields` | 请求字段（可选） |

---

## 配置说明

### config.json 配置

Searcher 会自动读取 `config.json` 中的 `semantic_scholar` 配置：

```json
{
  "semantic_scholar": {
    "api_key_env": "SEMANTIC_SCHOLAR_API_KEY",
    "request_interval": 0.5
  }
}
```

| 配置项 | 说明 |
|--------|------|
| `semantic_scholar.request_interval` | 两次 API 请求之间的间隔（秒） |

> **注意**：`kb_path` 由调用者传入，每个项目的知识库文件路径不同，不在 `config.json` 中配置。

### 环境变量
```bash
export SEMANTIC_SCHOLAR_API_KEY="your-semantic-scholar-api-key"
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.2.0 | 2026-04-22 | 统一风格：初始化时绑定知识库路径，方法调用时不再传知识库路径 |
| 2.1.0 | 2026-04-14 | 支持字典格式条件列表，每轮可单独设置条件 |
| 2.0.0 | 2026-04-14 | 重构为独立 Searcher 类 |
