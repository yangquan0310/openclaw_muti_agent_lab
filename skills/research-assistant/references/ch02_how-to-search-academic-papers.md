# 如何检索学术文献

> 从 Semantic Scholar 和 CNKI 获取文献数据，支持多主题多轮检索。

---

## 问题

### 为什么要专门讲检索？

文献检索是研究的第一步。检索不全，后面都是白费。常见问题：
- 检索词不准确，漏掉重要文献
- 检索引擎选择错误，中文文献用英文引擎
- 检索结果重复或遗漏

### Searcher 支持哪些引擎？

| 引擎 | 适用语言 | 数据量 | API |
|------|----------|--------|-----|
| **Semantic Scholar** | 英文为主 | 全球学术文献 | REST API（需 Key） |
| **CNKI（知网）** | 中文 | 中文期刊/学位论文 | 浏览器自动化 |

### 什么时候需要检索？

| 场景 | 是否需要 |
|------|----------|
| 新开研究课题 | ✅ 必须 |
| 更新知识库 | ✅ 必须 |
| 仅管理已有文献 | ❌ 使用 manage |

---

## 方法论

### 语言路由原则

```
关键词语言
    ↓
中文关键词 → CNKI（主）+ SemSch（备）
英文关键词 → SemSch（主）+ Scholar（备）
```

### 检索条件设计原则

1. **每次检索有明确目标**：不是越多越好
2. **多轮递进**：先宽后窄，逐步精炼
3. **设置过滤条件**：年份、引用量、文献类型

### 判断：单次检索还是多轮检索？

| 情况 | 方式 |
|------|------|
| 单一主题，简单条件 | 单次检索 |
| 多主题，每个主题条件不同 | 多轮检索（queries dict） |
| 需要逐步精炼 | 多轮递进检索 |

---

## 工作流

### 步骤 1：设计检索条件

**格式**：
```json
{
    "主题名": [
        {"query": "检索关键词", "limit": 30},
        {"query": "精确短语匹配", "year": "2020-2025"},
        {"query": "排除词 -excluded", "minCitationCount": 50}
    ]
}
```

**query 语法**：
| 语法 | 说明 | 示例 |
|------|------|------|
| 空格 | AND 关系 | `autobiographical memory self` |
| `\|` | OR 关系 | `autobiographical \| personal` |
| `\"\"` | 精确短语 | `\"self-memory system\"` |
| `-` | NOT 排除 | `autobiographical -childhood` |
| `()` | 优先级 | `(autobiographical \| personal) memory` |

### 步骤 2：执行检索

**英文检索（Semantic Scholar）**：
```bash
research-assistant search \
    --queries queries.json \
    --kb-path knowledge/index.json
```

**中文检索（CNKI）**：
1. 使用 browser 工具访问 search.cnki.com.cn
2. 抓取页面快照
3. 使用 CNKISearcher 解析

### 步骤 3：验证结果

**检查项**：
| 检查项 | 标准 |
|--------|------|
| 论文数量 | ≥ 目标数量的 80% |
| 时间范围 | 覆盖近 5-10 年 |
| 引用格式 | 所有论文有完整 APA 信息 |

---

## 执行标准

### 检索报告

每次检索后应生成检索报告，保存在 `knowledge/retrieval_report/{标题}.md`

### 检索质量标准

| 标准 | 要求 |
|------|------|
| 查全率 | 核心文献不遗漏 |
| 查准率 | 不相关结果 < 20% |
| 去重 | 基于 paperId 去重 |
| 更新 | 使用 `update()` 刷新元数据 |

### 配置要求

| 配置项 | 要求 |
|--------|------|
| `semantic_scholar.api_key_env` | SEMANTIC_SCHOLAR_API_KEY 环境变量 |
| `semantic_scholar.request_interval` | ≥ 0.5 秒（防限流）|
