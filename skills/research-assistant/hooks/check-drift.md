# Hook: wiki-zotero-webdav 数据漂移检测

> **触发**：定期（每月）或大批量同步后。

## 漂移类型

| 漂移 | 检测命令 | 严重度 |
|---|---|---|
| wiki source 引用 Zotero itemKey 但 Zotero 库无 | `zotero.py get <KEY>` | 🔴 P0 |
| Zotero item 有 `wiki:source.<id>` tag 但 wiki 无 source 页 | `ls wiki/sources/` | 🔴 P0 |
| wiki source 标 `zotero_pdf_path` 但 WebDAV 找不到 .zip | `rclone lsf nutstore:quanquanzi/zotero/` | 🟡 P1 |
| Zotero item 没 `wiki:source.<id>` tag 但 wiki 已引用 | 反查 | 🟡 P1 |

## 检测脚本

```bash
# 1. 列出所有 wiki source 引用的 itemKey
grep -h "^zotero_item_key:" ~/.openclaw/wiki/sources/*.md | awk '{print $2}' > /tmp/wiki_keys.txt

# 2. 逐个验证 Zotero
while read key; do
  result=$(python3 ~/.openclaw/skills/zotero/scripts/zotero.py get "$key" 2>&1 | head -2)
  echo "$key: $result"
done < /tmp/wiki_keys.txt

# 3. 验证 WebDAV PDF
for att in $(grep -h "^zotero_attachment_key:" ~/.openclaw/wiki/sources/*.md | awk '{print $2}'); do
  rclone lsf nutstore:quanquanzi/zotero/ | grep -q "^${att}\.zip$" \
    && echo "$att: ✅" || echo "$att: ❌"
done
```

## 输出

写入 `~/.openclaw/wiki/reports/wiki-zotero-drift-<YYYY-MM-DD>.md`：

```markdown
# 漂移报告 - <日期>

## 🔴 P0
- ...

## 🟡 P1
- ...
```
