# Hook: wiki source ↔ Zotero 双向建立

> **触发**：在 wiki `sources/` 新建/编辑 source 页，或老板说"加 paper 到 wiki"。

## 5 步流程

1. **查 Zotero 库**
   ```bash
   python3 ~/.openclaw/skills/zotero/scripts/zotero.py search "<title>"
   python3 ~/.openclaw/skills/zotero/scripts/zotero.py --json get <ITEMKEY>
   ```

2. **验证 WebDAV PDF 是否存在**
   ```bash
   rclone lsf nutstore:quanquanzi/zotero/ | grep <ATTACHMENT_KEY>
   # 输出应包含 <KEY>.zip + <KEY>.prop
   # ⚠️ 如果是 imported_url（linked），PDF 不在 WebDAV，跳过 zotero_pdf_path
   ```

3. **补 wiki YAML 字段**
   ```yaml
   zotero_item_key: <ITEMKEY>                  # 必填
   zotero_attachment_key: <ATTACHMENT_KEY>     # 可选
   zotero_pdf_path: nutstore:quanquanzi/zotero/<KEY>.zip  # 可选
   zotero_doi: <DOI>                            # 可选
   ```

4. **加 Zotero 反向 tag**
   ```bash
   python3 ~/.openclaw/skills/zotero/scripts/zotero.py update <ITEMKEY> \
     --add-tags "wiki:source.<wiki-source-id>"
   ```

5. **验证双向跳转**
   - wiki → Zotero: `zotero://select/library/items/<ITEMKEY>`
   - Zotero → wiki: `obsidian://open?vault=wiki&file=sources/<file>.md`

## 失败处理

| 失败 | 处理 | 详见 hook |
|---|---|---|
| Zotero 找不到 | `add-doi` / `add-isbn` / `add-pmid` | `manual-add-item.md` |
| CrossRef 404 | 查正确 DOI 或 arXiv ID | `manual-add-item.md` |
| add-doi 进错论文 | 移到回收站 + 修 DOI | `cleanup-wrong-entry.md` |
| PATCH 428 | 带 `If-Match: <version>` | `zotero-patch-with-version.md` |
| arXiv title 解析 | 用 `<entry>` 内的 title | `arxiv-title-parse.md` |
| wiki source 无 Zotero item | 4 路径处理 | `wiki-source-missing-in-zotero.md` |
