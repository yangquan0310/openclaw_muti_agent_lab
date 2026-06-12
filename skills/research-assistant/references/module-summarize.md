# 文献总结

> 使用 Summarizer 从文献中提取结构化信息。

---

## 总结原则

### 提取而非改写

总结是从论文中提取关键信息，不是改写论文内容。

### 结构化输出

笔记应按固定结构组织，便于后续合成和撰写。

### 保留来源

每条笔记必须可追溯到原始文献，支持 APA 引用。

---

## Summarizer 输出格式

| 字段 | 说明 |
|------|------|
| title | 论文标题 |
| authors | 作者 |
| year | 发表年份 |
| venue | 期刊/会议 |
| key_findings | 核心发现（1-3条） |
| methodology | 研究方法 |
| limitations | 局限性 |
| contribution | 学术贡献 |

---

## 标签系统

### 用途

标签用于组织和筛选笔记。同一篇论文可有多个标签。

### 标签层级

| 层级 | 示例 |
|------|------|
| 主题 | 认知心理学, 人工智能 |
| 方法 | 实证研究, 综述, 元分析 |
| 观点 | 支持, 反对, 中立 |

---

## 常见错误

| 错误 | 后果 |
|------|------|
| 总结太冗长 | 后续难以使用 |
| 缺少来源信息 | 无法引用 |
| 标签混乱 | 筛选困难 |
| 观点缺失 | 综述缺乏判断 |

---

## JCR / SCI 分区更新（easyScholar API）

> 整合自原 `easyscholar-api.md`（v1.0）。summarize 模块的 `update_jcr()` 方法通过 easyScholar API 批量更新 `knowledge/index.json` 中所有论文的 JCR / SCI 分区。

### 快速开始

```bash
# 1. 设置环境变量
export EASYSCHOLAR_API_KEY=your-key-from-easyscholar.cc

# 2. 跑 CLI（dry-run 先看效果）
research-assistant summarize --kb-path knowledge/index.json --update-jcr --dry-run

# 3. 真跑（写入 index.json）
research-assistant summarize --kb-path knowledge/index.json --update-jcr
```

### API 端点

```
GET https://easyscholar.cc/open/getPublicationRank
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `secretKey` | ✓ | API 密钥（`EASYSCHOLAR_API_KEY`）|
| `publicationName` | ✓ | 期刊名称（URL 编码）|

### 返回字段

- **JCR 分区**：Q1 / Q2 / Q3 / Q4
- **SCI 升级版 2022 分区**：1 区 / 2 区 / 3 区 / 4 区

### 实战要点

- **API 限制**：每调用一次查一篇，论文多时**耗时**（`update_jcr()` 已加进度条）
- **期刊名匹配**：必须**精确**匹配 easyScholar 数据库，否则查不到
- **数据写入**：`update_jcr()` 把 JCR 分区写入 index.json 的 paper 字段
- **CI 用法**：`--update-jcr` 通常在初次建库后跑一次，后续论文增量更新

### 易主任务 vs 模块

- `module-summarize` 模块**自包含** update_jcr
- **不**需要单独的"easyscholar"模块
