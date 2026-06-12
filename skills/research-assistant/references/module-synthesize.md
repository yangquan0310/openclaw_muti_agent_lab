# 笔记合成

> 使用 Synthesizer 将结构化笔记合成为连贯的笔记文档。

---

## 合成原则

### 主题聚合

按主题聚合相关论文的笔记，而非按论文罗列。

### 观点对比

不同论文的观点应对比分析，而非孤立描述。

### 批判性分析

不仅描述，要分析、比较、评价已有研究。

---

## Synthesizer 操作

### extract_notes

将 topic.json 中的笔记导出为 Markdown 格式。

### check_references

验证笔记中的 APA 引用是否正确。

### identify_gaps

识别已有研究中的空白（Research Gap）。

---

## 输出结构

```markdown
## 主题一：[主题名称]

### 核心观点
- 观点1 [citation]
- 观点2 [citation]

### 比较分析
| 研究 | 方法 | 结论 | 局限 |
|------|------|------|------|

### 研究空白
- gap1
- gap2
```

---

## 补充检索

`extract_notes` 输出**初步笔记**后，**人工**用 jina-ai/Exa/Tavily 补检索（OpenClaw 系统级工具），将补检索结果**手动**整合回写笔记.md。

补检索时机：
- 补检索**不在** Synthesizer 代码内
- 是**完整工作流**中的**人工/代理**环节
- 补检索工具：jina-ai skill（`~/.openclaw/skills/jina-ai/`，需 `JINA_API_KEY`） + Exa/Tavily（OpenClaw MCP 工具，需 `EXA_API_KEY` / `TAVILY_API_KEY`）

---

## 常见错误

| 错误 | 后果 |
|------|------|
| 按论文罗列 | 缺乏分析深度 |
| 不对比观点 | 综述表面化 |
| 不识别 gap | 研究动机不明确 |
| 引用错误 | 学术规范问题 |
