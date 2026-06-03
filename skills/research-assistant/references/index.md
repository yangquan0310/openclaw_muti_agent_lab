# research-assistant 参考手册

> 科研文献综述全流程助手参考指南。

---

## 章节导航

| 章节 | 文件 | 内容 |
|------|------|------|
| 研究工作流 | [research-workflow.md](research-workflow.md) | 五阶段流程原则 |
| 文献检索 | [paper-search.md](paper-search.md) | 检索策略与引擎选择 |
| 知识库管理 | [knowledge-management.md](knowledge-management.md) | index.json 管理原则 |
| 文献总结 | [paper-summary.md](paper-summary.md) | Summarizer 使用原则 |
| 笔记合成 | [note-synthesis.md](note-synthesis.md) | Synthesizer 使用原则 |
| 文献综述撰写 | [literature-review.md](literature-review.md) | 综述撰写原则 |
| 研究现状撰写 | [research-status.md](research-status.md) | 现状报告撰写原则 |
| 元数据维护 | [metadata-maintenance.md](metadata-maintenance.md) | Maintainer 使用原则 |
| 🆕 排版原则（Quarto 四范式）| [typesetting.md](typesetting.md) | ①书 / ②基础 / ③一般 / **④apaquarto 严格 APA 7** |
| 🆕 APA 7 manuscript 详细配置 | [apaquarto-manuscript.md](apaquarto-manuscript.md) | 范式 ④ 环境/扩展/YAML/排错指南 |
| 排版标准 | [formatting-standards.md](formatting-standards.md) | 写作内容规范 + 范式决策 |

---

## 按场景查找

### 执行阶段

| 场景 | 章节 |
|------|------|
| 不知道工作流程 | [research-workflow.md](research-workflow.md) |
| 不知道如何检索 | [paper-search.md](paper-search.md) |
| 不知道如何管理知识库 | [knowledge-management.md](knowledge-management.md) |

### 撰写阶段

| 场景 | 章节 |
|------|------|
| 不知道如何总结文献 | [paper-summary.md](paper-summary.md) |
| 不知道如何合成笔记 | [note-synthesis.md](note-synthesis.md) |
| 不知道如何写文献综述 | [literature-review.md](literature-review.md) |
| 不知道如何写研究现状 | [research-status.md](research-status.md) |

### 排版阶段

| 场景 | 章节 |
|------|------|
| 不知道选哪个范式 | [typesetting.md](typesetting.md) → 四范式对比表 |
| 投稿论文/严格 APA 7 | [apaquarto-manuscript.md](apaquarto-manuscript.md) → 范式 ④ 完整配置 |
| 写作内容规范 | [formatting-standards.md](formatting-standards.md) |
| 范式 ④ 5 步关键修复踩坑 | [apaquarto-manuscript.md](apaquarto-manuscript.md) → 第 6 节 |

### 维护阶段

| 场景 | 章节 |
|------|------|
| 不知道如何维护元数据 | [metadata-maintenance.md](metadata-maintenance.md) |

---

## 快速命令

```bash
# 检索文献
research-assistant search --keyword "关键词" --limit 20

# 总结文献
research-assistant summarize --kb-path knowledge/index.json

# 管理知识库
research-assistant manage info --kb-path knowledge/index.json
research-assistant manage merge --inputs a.json,b.json --output merged.json
```
