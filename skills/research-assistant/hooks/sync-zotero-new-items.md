# Hook: 从 Zotero 拉新条目到 wiki（增量同步）

> **触发**：老板在 Zotero 端手动加了 paper，或 fetch-pdfs 自动入了 item。

## 步骤

```bash
# 1. 列出最近添加的 Zotero items
python3 ~/.openclaw/skills/zotero/scripts/zotero.py items --limit 20 --sort dateAdded

# 2. 逐个 item 检查 wiki 是否已有 source 页
#   - 有 → 检查 4 个 zotero_* 字段是否齐全，按 add-zotero-source.md 补字段
#   - 没有 → 按 sources/_template_source_summary.md 模板新建
```

## 自动 vs 手动

| 模式 | 适用 | 状态 |
|---|---|---|
| 自动批量（WikiZoteroManager Python 类） | 100+ items 入库时 | v5.15.0 计划 |
| 手动逐个 | < 10 items 入库时 | 当前推荐 |

**当前策略**：手动逐个，老板目检。
