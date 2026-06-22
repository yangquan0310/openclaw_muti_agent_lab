# 笔记合成（v5.16.0+ 走 wiki）

> **v5.16.0 重大重构**：删旧 `Synthesizer.py`（走 knowledge/topic/xxx.json + knowledge/note/），新 `Synthesizer.py` 直接从 wiki source 读，输出到 wiki syntheses/。
> **老板 00:08 指令**："不需要向后兼容，全部改为 wiki"。

---

## 一、Synthesizer（v5.16.0+ wiki 版本）

### 文件位置

`scripts/synthesize/Synthesizer.py`（4785 bytes）

### 核心方法

| 方法 | 用途 | 输入 | 输出 |
|------|------|------|------|
| `extract_notes(source_id)` | 从 wiki source 读 abstract → 输出 wiki synthesis | wiki source id | {success, output_path, zotero_key, summary_chars, key_content_chars} |

### 提取逻辑

1. 找 source 文件（按 id 字段或文件名匹配）
2. 解析 YAML frontmatter（zotero_item_key, zotero_doi, title）
3. 提取 markdown 段：「一句话总结」「关键内容」
4. 输出到 `wiki/syntheses/<date>-extract-<slug>.md`
5. 自动填 zotero_refs 字段（保持 wiki↔Zotero 一致性）

### CLI 用法

```bash
python3 main.py synthesize extract --source-id source.diehl-2026-captured-memories
python3 main.py synthesize extract --source-id source.okeefe-recce-1993-phase-precession --output custom.md
```

### 输出格式

写到 `wiki/syntheses/<date>-extract-<slug>.md`：
- YAML: pageType=synthesis, zotero_refs 填主 source
- 标题（来自 wiki source）
- 来源 `[[sources/<filename>]]`
- Zotero itemKey
- 一句话总结
- 关键内容（前 3000 chars）
- 提取时间

### 不向后兼容

- 旧 `knowledge/topic/xxx.json` 路径**已废弃**
- 旧 `check_references` / `fix_references` **未迁移**（v5.16.0 范围外）
- 旧 Synthesizer 备份在 `_legacy_Synthesizer_<TS>.py`

### 与 Summarizer 区别

| 维度 | Summarizer | Synthesizer |
|------|------------|-------------|
| 输入 | wiki source | wiki source |
| 输出 | 总结（type/importance） | 提取（结构化笔记） |
| 方式 | 规则分类 | 字段提取 |
| 文件名 | summarize-*.md | extract-*.md |
