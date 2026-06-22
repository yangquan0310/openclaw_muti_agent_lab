# Hook: wiki source 在 Zotero 库找不到（v5.13.3 新增）

> **老板 wiki 的真实情况**：截至 2026-06-21，**6 个学术 source 在 Zotero 库搜不到**——历史笔记先入 wiki，Zotero 库还没建。

## 4 种处理路径

### 路径 A：手动 add-doi 入库（首选）

如果 wiki source 有 DOI：
```bash
python3 ~/.openclaw/skills/zotero/scripts/zotero.py add-doi "<DOI>"
```

### 路径 B：CrossRef 直查（绕过 Zotero 翻译服务器）

```bash
curl -s "https://api.crossref.org/works?query.bibliographic=<title>&rows=3" | \
  jq '.message.items[] | {title: .title[0], DOI}'
```

### 路径 C：arXiv add

```bash
# 见 manual-add-item.md 方案 C
```

### 路径 D：标红 + 跳过（暂时接受漂移）

如果论文**确实找不到**（罕见小众文献）：
```yaml
zotero_status: not_found  # v5.13.3 引入
# zotero_item_key: 留空
```

## 漂移跟踪

在 workboard 卡 / dashboard 维护一个表（v5.13.3 引入）。

## 决策原则

| 优先级 | 原则 |
|---|---|
| P0 | wiki source 被 syntheses/concepts 引用 → 必须入库（路径 A/B/C） |
| P1 | 历史笔记不活跃引用 → 标红跳过（路径 D） |
| P2 | 工具/技术笔记 → **不需要** zotero_item_key |
