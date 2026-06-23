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

---

## 二、多模态精读（v6.0.2+ 工具能力）

> **职责边界**：本节描述 **summarize 工具的能力**（能调哪些本地 PDF 解析器、返回什么数据）。**agent 拿到数据后怎么攥写笔记 / 综述**，由 agent 自己决定。

### 能力：本地 PDF 解析

`--pdf-path` 标志：agent 传本地 PDF 路径，工具内部用以下解析器提取数据：

| 解析器 | 数据 | 用途 |
|--------|------|------|
| `pypdf` | 全文 + 页级文本 | 文本提取（默认 0.00s 提一篇） |
| `pypdfium2` | 页面渲染（PNG）| 给 OCR / vision 用 |
| `tesseract`（系统）| 图片 OCR 文字 | 图表 / 公式的文字提取 |

### CLI 用法

```bash
# 仅处理 wiki source（不变）
python3 main.py summarize --source-id source.buzsaki-2002-hippocampal-theta

# 加 PDF 解析（agent 传本地路径）
python3 main.py summarize --source-id source.buzsaki-2002-hippocampal-theta --pdf-path /root/.openclaw/wiki/raw/papers/buzsaki-2002.pdf
```

### 工具返回数据（不攥写）

输出到 `wiki/syntheses/<date>-summarize-<slug>.md` 的结构：

```markdown
## PDF 提取数据（v6.0.2+ 工具能力）

### 元数据
- 页数: N
- 文件大小: KB
- 解析器: pypdf + pypdfium2 + tesseract

### 全文（pypdf 提取）
[每页文本结构化]

### 图片 OCR（pypdfium2 + tesseract）
- 第 X 页 图 Y：OCR 文字...
- 第 X 页 图 Y：OCR 文字...

---
**数据供 agent 使用**：本节为工具提取的原始数据，**攥写笔记 / 综述由 agent 完成**。
```

### 不做什么（明确边界）

- ❌ **不调 LLM**（保持"避费用/API key 风险"决策）
- ❌ **不攥写笔记 / 综述**——agent 的活
- ❌ **不调 OpenClaw `pdf` 工具**——OpenClaw 没装 native PDF vision 模型（A 方案不可行，见 v6.0.2 教训）

### agent 调用建议

- 拿到本工具的输出后，agent 用 LLM 整理成 narrative 笔记
- agent 自己决定怎么编排段落 / 加分析 / 加 context
