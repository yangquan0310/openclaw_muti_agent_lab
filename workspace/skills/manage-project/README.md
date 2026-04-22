# manage-project

项目文件自动化整理与学术事务管理工具。

## 功能

- **文献检索**：从 Semantic Scholar 获取学术文献数据
- **文献总结**：使用 LLM 分析文献，自动添加分类标签和结构化笔记
- **知识库管理**：合并、筛选、保存知识库，支持链式调用
- **文献综述合成**：基于知识库生成文献综述和研究现状
- **项目文件整理**：自动化整理项目目录结构、归档中间文件、管理手稿和元数据

## 目录结构

```
manage-project/
├── search/                   # 文献检索模块
│   ├── Searcher.py          # 文献检索类
│   ├── SKILL.md             # 检索模块说明
│   └── 检索报告模板.md      # 检索报告模板
├── summarize/                # 文献总结模块
│   ├── Summarizer.py        # 文献总结类
│   └── SKILL.md             # 总结模块说明
├── manage/                   # 知识库管理模块
│   ├── Manager.py           # 知识库管理类
│   └── SKILL.md             # 管理模块说明
├── synthesize/               # 文献综述合成模块
│   ├── Synthesizer.py       # 综述合成主类
│   ├── NoteExtractor.py     # 笔记信息提取类
│   ├── ReferenceChecker.py  # 参考文献检查与修复类
│   ├── SKILL.md             # 综述合成模块说明
│   ├── 文献综述模板.md      # 文献综述模板
│   └── 研究现状模板.md      # 研究现状模板
├── maintainer/               # 项目文件整理模块
│   └── Maintainer.py        # 核心Python脚本
├── mcp/                      # MCP服务器
│   └── server.py            # MCP服务暴露
├── references/               # 参考文档
│   ├── 数据结构.md          # 元数据结构说明
│   └── 知识库管理.md        # 知识库管理技能适配指南
├── config.json               # 统一配置文件
├── SKILL.md                  # 主技能说明（AI 入口）
├── README.md                 # 给人类看的说明（本文件）
└── _meta.json                # 技能元数据
```

## 快速开始

### 学术工作流

| 需求 | 跳转 |
|------|------|
| 检索文献 | [search/SKILL.md](./search/SKILL.md) |
| 总结文献 | [summarize/SKILL.md](./summarize/SKILL.md) |
| 管理知识库 | [manage/SKILL.md](./manage/SKILL.md) |
| 写文献综述 | [synthesize/SKILL.md](./synthesize/SKILL.md) |

### 完整学术工作流示例

```python
# 1. 检索文献
from search.Searcher import Searcher
searcher = Searcher(kb_path="my_kb.json")
queries = {
    "自传体记忆": [
        {"query": "autobiographical memory | personal memory", "limit": 30}
    ]
}
searcher.search(queries)

# 2. 总结文献
from summarize.Summarizer import Summarizer
summarizer = Summarizer(kb_path="my_kb.json")
summarizer.summarize()

# 3. 管理知识库
from manage.Manager import Manager
manager = Manager("my_kb.json")
manager.filter({"citations_min": 50}).save()

# 4. 合成文献综述
from synthesize.Synthesizer import Synthesizer
synthesizer = Synthesizer("my_kb.json")
synthesizer.check_references("综述文档.md")
```

### 项目文件整理

```bash
# 整理单个项目
python3 maintainer/Maintainer.py /path/to/project

# 整理所有项目
python3 maintainer/Maintainer.py --all
```

### Python导入

```python
from maintainer.Maintainer import Maintainer

# 初始化项目
maintainer = Maintainer("/path/to/project")

# 移动文件
maintainer.move_file("文件.txt", target_dir="临时数据")

# 重命名文件夹
maintainer.rename_folder("旧名", "新名")

# 更新元数据
maintainer.update_metadata()
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
# 默认 provider 为 Kimi
export KIMI_API_KEY="your-kimi-api-key"

# 或使用腾讯云 tokenhub
export TOKENHUB_API_KEY="your-tencent-api-key"
```

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `未设置 Semantic Scholar API key` | 环境变量未配置 | `export SEMANTIC_SCHOLAR_API_KEY=...` |
| `请设置环境变量：TOKENHUB_API_KEY` | Summarizer 的 LLM API key 未配置 | 检查 config.json 中 `llm.default_provider` 并设置对应环境变量 |
| `知识库文件不存在` | `kb_path` 路径错误 | 确认传入的是相对或绝对路径 |
| 检索结果为空 | 查询词过于具体或限制条件过多 | 尝试简化 query，增加 limit |
| API 请求超时 | 网络问题或 API 服务不稳定 | 检查网络，或调整 config.json 中的 timeout |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 3.0.0 | 2026-04-22 | 重构为统一项目管理技能，整合五大模块 |
| 2.1.0 | 2026-04-15 | 面向对象重构知识库管理，拆分为四个独立子模块 |
| 2.0.0 | 2026-04-14 | 重构为三个独立类：Searcher、Summarizer、Manager |
| 1.6.0 | 2026-04-08 | filter_by_criteria 功能升级 |
| 1.3.0 | 2026-04-13 | 重构为 AcademicSearchSummarizer |
| 1.0.0 | 2026-04-08 | 初始版本 |
