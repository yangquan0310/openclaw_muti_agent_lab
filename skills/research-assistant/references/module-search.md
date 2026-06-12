# 文献检索

> 学术文献检索的原则与策略。

---

## 语言路由原则

```
关键词语言
    ↓
中文关键词 → CNKI（主）+ SemSch（备）
英文关键词 → SemSch（主）+ Scholar/GS（备）
```

---

## 检索引擎选择

| 引擎 | 适用语言 | 数据量 | API |
|------|----------|--------|-----|
| **Semantic Scholar** | 英文为主 | 全球学术文献 | REST API（`SEMANTIC_SCHOLAR_API_KEY` 环境变量）|
| **CNKI（知网）** | 中文 | 中文期刊/学位论文 | 浏览器自动化 |
| **Google Scholar** | 通用 | 全球 | 受 rate limit 限制 |

---

## 检索条件设计原则

### 明确目标

每次检索有明确目标。不是越多越好，而是覆盖目标主题。

### 多轮递进

| 轮次 | 策略 |
|------|------|
| 第一轮 | 宽泛检索，了解全貌 |
| 第二轮 | 精炼关键词，排除噪声 |
| 第三轮 | 补充特定主题/方法 |

### 过滤条件

| 条件 | 说明 |
|------|------|
| 年份范围 | 近 5-10 年为主 |
| 引用量 | 高引用优先 |
| 文献类型 | 同行评审优先 |

---

## query 语法

| 语法 | 说明 | 示例 |
|------|------|------|
| 空格 | AND 关系 | `autobiographical memory self` |
| `\|` | OR 关系 | `autobiographical \| personal` |
| `\"\"` | 精确短语 | `\"self-memory system\"` |
| `-` | NOT 排除 | `autobiographical -childhood` |
| `()` | 优先级 | `(autobiographical \| personal) memory` |

---

## 补检索原则（系统级工具）

`sdk-search` 模块只覆盖学术数据库（Semantic Scholar / CNKI / Google Scholar）。

补检索用 OpenClaw 系统级工具：
- **jina-ai** skill（`~/.openclaw/skills/jina-ai/`，需 `JINA_API_KEY`）— 主要补检索工具
- **Exa / Tavily**（OpenClaw MCP 工具，需 `EXA_API_KEY` / `TAVILY_API_KEY`）— 政策/行业/新闻来源

补检索时机：
- search 阶段**不**用（search 是**学术数据库**检索）
- **Synthesizer 阶段后**用——发现笔记空白时，人工用 jina-ai/Exa/Tavily 补检索，**手动**整合结果回写笔记.md

补检索可补充：
- 政策文件
- 行业报告
- 新闻报道
- 非学术来源

---

## 常见错误

| 错误 | 后果 |
|------|------|
| 检索词太窄 | 漏掉重要文献 |
| 检索词太宽 | 结果太多，无法处理 |
| 不设置过滤 | 低质量文献过多 |
| 只用一个引擎 | 覆盖不全 |
| 不补检索 | 缺少政策/行业视角 |
