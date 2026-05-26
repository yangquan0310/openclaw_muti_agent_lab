# 知识库管理

> knowledge/index.json 是核心数据源。

---

## 数据结构

```
knowledge/
├── index.json           ← 核心数据源
├── topic/              ← 主题子集
│   └── {topic}.json
├── note/                ← 结构化笔记
│   └── 笔记_{topic}.md
└── review/              ← 综述文档
    ├── 综述_{topic}.md
    └── 研究现状.md
```

---

## index.json 原则

### 是核心驱动

所有知识产出以 index.json 为核心。它是检索结果、阅读笔记、撰写素材的统一来源。

### 版本控制

使用 Git 管理 index.json。每次更新后 commit。

### 不直接编辑

index.json 由 Searcher/Manager 自动维护，不手动编辑。

---

## Manager 操作原则

### topic 筛选

使用 Manager.filter() 从 index.json 中筛选特定 topic，生成 topic.json。

### 数据合并

使用 Manager.merge() 合并多个 index.json，支持多轮检索整合。

---

## 常见错误

| 错误 | 后果 |
|------|------|
| 手动编辑 index.json | 被 Searcher 覆盖 |
| 不 commit | 更新丢失无法追溯 |
| 多份 index.json | 数据不一致 |
| 不备份 | 意外丢失 |
