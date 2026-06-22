# Hook: 手动添加 Zotero item（无 DOI / DOI 失败时）

> **触发**：`add-doi` 失败（CrossRef 404 / 翻译服务器 503 / DOI 错误导致 add 进错论文）。

## 方案 A：ISBN / PMID

```bash
python3 ~/.openclaw/skills/zotero/scripts/zotero.py add-isbn "<ISBN>"
python3 ~/.openclaw/skills/zotero/scripts/zotero.py add-pmid "<PMID>"
```

## 方案 B：CrossRef 直查

```bash
curl -s "https://api.crossref.org/works?query.bibliographic=<title>&rows=3" | \
  jq '.message.items[] | {title: .title[0], DOI, author: .author[0].family}'
```

## 方案 C：arXiv

```bash
# 找 arXiv ID 后从 arXiv API 拉元数据
curl -s "http://export.arxiv.org/api/query?id_list=<ARXIV_ID>" | \
  grep -E "<title>|<author>|<id>"
# 然后用 Zotero web API 创建 item（见 zotero-patch-with-version.md）
```

## 方案 D：Zotero GUI 手动添加

打开 Zotero 桌面端 → New Item → 选类型 → 填题录 → 同步。

## v5.13.2 SOP

1. 先 A（ISBN/PMID）
2. 次 B（CrossRef 直查）
3. 再次 C（arXiv）
4. 最后 D（GUI）
5. 绝不 add 错误 DOI 后不删——污染库
