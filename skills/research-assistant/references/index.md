# research-assistant 参考手册

> 科研文献综述全流程助手

---

## 书籍目录

| 章节 | 对应的问题 |
|------|------------|
| [ch01_how-to-execute-research-workflow.md](ch01_how-to-execute-research-workflow.md) | 如何执行研究工作流？ |
| [ch02_how-to-search-academic-papers.md](ch02_how-to-search-academic-papers.md) | 如何检索学术文献？ |
| [ch03_how-to-manage-knowledge-base.md](ch03_how-to-manage-knowledge-base.md) | 如何管理知识库？ |
| [ch04_how-to-summarize-papers.md](ch04_how-to-summarize-papers.md) | 如何总结文献？ |
| [ch05_how-to-synthesize-notes.md](ch05_how-to-synthesize-notes.md) | 如何合成笔记？ |
| [ch06_how-to-write-literature-review.md](ch06_how-to-write-literature-review.md) | 如何撰写文献综述？ |
| [ch07_how-to-write-research-status.md](ch07_how-to-write-research-status.md) | 如何撰写研究现状？ |
| [ch08_how-to-maintain-metadata.md](ch08_how-to-maintain-metadata.md) | 如何维护元数据？ |

---

## 按阶段查找

### 研究流程

| 阶段 | 问题 | 章节 |
|------|------|------|
| 理解 | 如何执行研究工作流？ | ch01 |
| 检索 | 如何检索学术文献？ | ch02 |
| 整理 | 如何管理知识库？ | ch03 |
| 分析 | 如何总结文献？ | ch04 |
| 综合 | 如何合成笔记？ | ch05 |
| 撰写 | 如何撰写文献综述？ | ch06 |
| 撰写 | 如何撰写研究现状？ | ch07 |
| 检查 | 如何维护元数据？ | ch08 |

---

## 章节结构

每章统一包含四个层次：

| 层次 | 回答的问题 |
|------|------------|
| **问题** | 为什么要知道这个？ |
| **方法论** | 怎么思考这个问题？ |
| **工作流** | 具体怎么执行？ |
| **执行标准** | 做到什么程度算合格？ |

---

## 快速命令

```bash
# 检索文献
research-assistant search --queries queries.json --kb-path knowledge/index.json

# 总结文献
research-assistant summarize --kb-path knowledge/index.json

# 管理知识库
research-assistant manage info --kb-path knowledge/index.json
research-assistant manage merge --inputs a.json,b.json --output merged.json
```
