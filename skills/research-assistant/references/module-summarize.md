# 文献总结（v5.16.0+ 走 wiki）

> **v5.16.0 重大重构**：删旧 `Summarizer.py`（走 knowledge/index.json），新 `Summarizer.py` 直接以 wiki 为存储（替代品 `WikiSummesizer.py` 已重命名）。
> **简化模式**：不调 LLM（避免费用/API key 风险），按规则做 type/importance 分类 + 关键内容提取。

---

## 一、Summarizer（v5.16.0+ wiki 版本，规则版）

### 文件位置

`scripts/summarize/Summarizer.py`（5157 bytes）

### 核心方法

| 方法 | 用途 | 输入 | 输出 |
|------|------|------|------|
| `summarize(source_id)` | 读 wiki source → 写 wiki synthesis | wiki source id | {success, output_path, paper_type, importance, zotero_key, notes_chars} |

### 分类规则（不调 LLM）

| 类型 | 触发词 |
|------|--------|
| **review** | "综述" / "review" / "元分析" / "meta-analysis" |
| **preprint** | "preprint" / "arxiv" |
| **report** | "report" / "报告" |
| **paper** | 默认 |

### 重要度规则

- **5⭐** "meta-analysis" / "元分析"
- **4⭐** "5 个研究" / "n=709" / "多研究" / "预注册"
- **3⭐** 默认

### CLI 用法

```bash
python3 main.py summarize --source-id source.diehl-2026-captured-memories
python3 main.py summarize --source-id source.buzsaki-2002-hippocampal-theta --output custom.md
```

### 输出格式

写到 `wiki/syntheses/<date>-summarize-<slug>.md`：
- YAML: pageType=synthesis, zotero_refs 填主 source
- 分类表（type/importance/zotero_key/zotero_doi）
- 关键内容（前 3000 chars）
- 提取时间

### 未来扩展

- v5.17.0+ 可加 `_summarize_with_llm()` 方法（调 OpenAI/deepseek）
- 改用 `self.llm_call(title, abstract)` 替代规则分类

### 不向后兼容

- 旧 `knowledge/index.json` 路径**已废弃**
- 旧 Summarizer 备份在 `_legacy_Summarizer_<TS>.py`
