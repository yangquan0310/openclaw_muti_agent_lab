# 研究工作流

> 科研文献综述的五阶段流程原则。

---

## 五阶段模型

```
理解 → 检索 → 阅读 → 撰写 → 检查
```

| 阶段 | 输入 | 输出 | 负责 |
|------|------|------|------|
| 理解 | 研究问题 | 明确的研究主题和范围 | 代理 |
| 检索 | 研究主题 + 关键词 | knowledge/index.json | Searcher |
| 阅读 | index.json | topic.json + 笔记.md | Manager + Summarizer |
| 撰写 | 笔记.md + 写作指南 | 综述.md | 代理 |
| 检查 | 综述.md + topic.json | 修正后的综述 + 更新的元数据 | Synthesizer + Maintainer |

---

## 核心原则

### 阶段顺序执行

不要跳跃阶段。每个阶段是下一阶段的输入基础。

### 输出驱动

没有明确输出 = 阶段未完成。必须产出可验证的成果物。

### Git 版本控制

每个阶段完成后 commit，便于追溯和回滚。

---

## 阶段准入判断

| 当前阶段 | 进入下一阶段的条件 |
|----------|------------------|
| 理解 | 明确研究主题和检索关键词 |
| 检索 | index.json 包含 ≥ 目标数量的 80% 文献 |
| 阅读 | 笔记.md 生成完毕 |
| 撰写 | 综述.md 完成初稿 |
| 检查 | APA 引用无错误，元数据已更新 |

---

## 数据流验证

```
queries.json → Searcher → index.json
                            ↓
                    Manager.filter → topic.json
                            ↓
                    Summarizer → notes/labels
                            ↓
                    Synthesizer → 笔记.md
                            ↓
                    补充检索 → Exa/Tavily → 笔记.md
                            ↓
                    代理撰写 → 综述.md
                            ↓
                    Synthesizer.check → APA 核查
                            ↓
                    Maintainer → 元数据更新
```

---

## 常见错误

| 错误 | 后果 |
|------|------|
| 跳阶段 | 返工 |
| 无输出就结束 | 阶段无效 |
| 不 commit | 无法追溯 |
| 检索不全就开始写 | 综述不完整 |
