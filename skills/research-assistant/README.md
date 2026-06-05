# research-assistant

科研论文知识库管理工具（研究助手）。聚焦文献检索、知识库总结、笔记导出、综述撰写和版本控制。

## 功能

- **文献检索**：从 Semantic Scholar 获取学术文献数据，追加到 index.json
- **文献总结**：使用 LLM 分析文献，自动添加分类标签和结构化笔记
- **知识库管理**：合并、筛选、保存知识库，导出 Markdown 笔记
- **文献综述合成**：基于笔记撰写文献综述和研究现状
- **元数据维护**：自动更新项目元数据，对综述/研究现状进行版本快照

## 目录结构

```
research-assistant/
├── scripts/
│   ├── search/              # 文献检索模块
│   │   ├── Searcher.py
│   │   └── __init__.py
│   ├── summarize/             # 文献总结模块
│   │   ├── Summarizer.py
│   │   └── __init__.py
│   ├── manage/                # 知识库管理模块
│   │   ├── Manager.py
│   │   └── __init__.py
│   ├── synthesize/           # 文献综述合成模块
│   │   ├── Synthesizer.py
│   │   └── __init__.py
│   ├── maintain/           # 元数据维护与版本控制模块
│   │   ├── Maintainer.py
│   │   └── __init__.py
│   ├── mcp/                   # MCP服务器
│   │   └── server.py
│   ├── main.py                # CLI统一入口
│   ├── config.json            # 统一配置
│   └── __init__.py
├── references/               # 参考文档
├── config.json               # 技能根目录配置
├── SKILL.md                  # 主技能说明
├── README.md                 # 给人类看的说明
└── _meta.json                # 技能元数据
```

## 数据流

```
index.json (核心数据源)
    ↑
search: 检索补充论文条目
    ↓
summarize: 总结补充 notes/labels
    ↓
manage: 筛选子集 → export_notes() → knowledge/note/笔记_主题.md
    ↓
synthesize: 基于笔记撰写 → knowledge/review/综述_主题.md
    ↓
maintain: 更新元数据 + 保存版本快照
```

## 快速开始

### 学术工作流

| 需求 | 命令 | 说明 |
|------|------|------|
| 检索文献 | `python3 scripts/main.py search --queries queries.json --kb-path index.json` | 追加论文到知识库 |
| 总结文献 | `python3 scripts/main.py summarize --kb-path index.json` | 补充 notes/labels |
| 管理知识库 | `python3 scripts/main.py manage filter --kb-path index.json` | 筛选并导出笔记 |
| 写文献综述 | `python3 scripts/main.py synthesize extract --notes notes.json` | 基于笔记生成综述 |
| 更新元数据 | `python3 scripts/maintain/Maintainer.py ~/项目 update-kb` | 自动更新时间戳 |
| 保存版本 | `python3 scripts/maintain/Maintainer.py ~/项目 save-version knowledge/review/综述.md` | 综述版本快照 |

### 完整学术工作流示例

```python
from scripts import Searcher, Summarizer, Manager, Synthesizer, Maintainer

# 1. 检索文献
searcher = Searcher(kb_path="knowledge/index.json")
queries = {
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30}
    ]
}
searcher.search(queries)

# 2. 总结文献
summarizer = Summarizer(kb_path="knowledge/index.json")
summarizer.summarize()

# 3. 管理知识库：筛选并导出笔记
manager = Manager("knowledge/index.json")
manager.filter({"citations_min": 50}).export_notes("自传体记忆")

# 4. 合成文献综述
synthesizer = Synthesizer("knowledge/index.json")
synthesizer.write_review("knowledge/note/笔记_自传体记忆.md", "knowledge/review/综述_自传体记忆.md")

# 5. 维护元数据 + 版本控制
maintainer = Maintainer("~/项目")
maintainer.update_kb_metadata()                          # 更新知识库时间戳
maintainer.save_review_version("knowledge/review/综述_自传体记忆.md", title="文献综述")  # 版本快照
```

## 安装依赖

```bash
pip install openai requests
```

## 环境变量配置

### Semantic Scholar API
```bash
export SEMANTIC_SCHOLAR_API_KEY="your-semantic-scholar-api-key"
```

### LLM API（Summarizer）
```bash
# 根据 config.json 中配置的 provider 设置对应环境变量
# 默认 provider 为 deepseek
export DEEPSEEK_API_KEY="your-deepseek-api-key"

# 或使用 Kimi
export KIMI_API_KEY="your-kimi-api-key"

# 或使用腾讯云 tokenhub
export TOKENHUB_API_KEY="your-tencent-api-key"
```

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `未设置 Semantic Scholar API key` | 环境变量未配置 | `export SEMANTIC_SCHOLAR_API_KEY=...` |
| `请设置环境变量：TOKENHUB_API_KEY` | Summarizer 的 LLM API key 未配置 | 检查 config.json 中 `llm.default_provider` 并设置对应环境变量 |
| `index.json 路径错误` | `kb_path` 路径错误 | 确认传入的是相对或绝对路径 |
| 检索结果为空 | 查询词过于具体或限制条件过多 | 尝试简化 query，增加 limit |
| API 请求超时 | 网络问题或 API 服务不稳定 | 检查网络，或调整 config.json 中的 timeout |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 5.0.0 | 2026-05-09 | 重构为研究助手，聚焦知识库管理，拆分项目整理为 lab-organizer |
| 4.0.0 | 2026-05-06 | 重构为 v3.1.0 混合结构 |
| 3.0.0 | 2026-04-22 | 重构为统一项目管理技能，整合五大模块 |
| 2.1.0 | 2026-04-15 | 面向对象重构知识库管理，拆分为四个独立子模块 |
| 2.0.0 | 2026-04-14 | 重构为三个独立类：Searcher、Summarizer、Manager |
| 1.0.0 | 2026-04-08 | 初始版本 |
