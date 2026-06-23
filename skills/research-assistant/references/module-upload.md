# upload 模块（v6.0.3+）

> **download 模块的反向对偶**：
> - `download`：远端 Zotero / WebDAV → 本地 wiki raw（find_paper + download_pdf + archive_to_wiki）
> - `upload`：本地 PDF → 远端 Zotero / WebDAV + wiki source（add_to_zotero + push_to_webdav + create_wiki_source）

---

## 一、能力

| 步骤 | 方法 | 工具 | 输出 |
|------|------|------|------|
| **1. Zotero 建条目** | `add_to_zotero(doi, tags)` | `zotero.py add-doi` | Zotero item key |
| **2. WebDAV 推 PDF** | `push_to_webdav(pdf_path)` | `rclone copyto` | nutstore:quanquanzi/zotero/<filename> |
| **3. wiki source 创建** | `create_wiki_source(slug, pdf, ...)` | 直接写 YAML | `~/.openclaw/wiki/sources/<slug>.md` |

---

## 二、CLI 用法

```bash
# 完整流水线（建 Zotero 条目 + 推 WebDAV + 创建 wiki source）
python3 main.py upload \
  --pdf-path /data/local-pdfs/smith-2025-memory.pdf \
  --doi "10.1234/example.2025.001" \
  --tags "review,important"

# 显式 slug（agent 自決唯一标识；避免工具替 agent 决策）
python3 main.py upload \
  --pdf-path /data/local-pdfs/smith-2025-memory.pdf \
  --slug smith-2025-memory

# 仅创建 wiki source（跳过 Zotero 和 WebDAV）
python3 main.py upload \
  --pdf-path /data/local-pdfs/smith-2025-memory.pdf \
  --slug smith-2025-memory \
  --no-zotero --no-webdav

# 仅推 WebDAV + 建 Zotero（已有 wiki source）
python3 main.py upload \
  --pdf-path /data/local-pdfs/smith-2025-memory.pdf \
  --doi "10.1234/example.2025.001" \
  --slug smith-2025-memory \
  --no-wiki
```

### 必填参数

| 参数 | 必填性 | 说明 |
|------|--------|------|
| `--pdf-path` | **必填** | 本地 PDF 路径 |
| `--slug` | 与 `--doi` **二选一必填** | wiki source 唯一标识（agent 自決） |
| `--doi` | 与 `--slug` **二选一必填** | DOI（如有则建 Zotero 条目） |

### 可选参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--title` | 用 slug | wiki source title（agent 自決） |
| `--tags` | 无 | Zotero tags（逗号分隔） |
| `--no-zotero` | 关 | 跳过 Zotero 建条目 |
| `--no-webdav` | 关 | 跳过 WebDAV 推 |
| `--no-wiki` | 关 | 跳过 wiki source 创建 |

---

## 三、流水线详情

### Step 1: add_to_zotero(doi, tags)

```python
from scripts.upload.Uploader import Uploader
u = Uploader()
result = u.add_to_zotero("10.1234/example.2025.001", tags=["review"])
# 返回：{"success": bool, "item_key": "ABC12345", "stdout": "...", "stderr": "..."}
```

**注意**：当前只包装 `zotero.py add-doi`（已有）；**PDF attachment 上传 Zotero 暂未实现**——老板如需，单独做 v6.0.4 增量。

### Step 2: push_to_webdav(pdf_path)

```python
result = u.push_to_webdav(Path("/data/local-pdfs/smith-2025-memory.pdf"))
# 返回：{"success": bool, "remote_path": "nutstore:quanquanzi/zotero/smith-2025-memory.pdf", ...}
```

底层：`rclone copyto <pdf> nutstore:quanquanzi/zotero/<pdf-name>`。

### Step 3: create_wiki_source(slug, pdf, zotero_meta, title)

```python
result = u.create_wiki_source(
    slug="smith-2025-memory",
    pdf_path=Path("/data/local-pdfs/smith-2025-memory.pdf"),
    zotero_meta={"item_key": "ABC12345", "doi": "10.1234/..."},
    title="Smith 2025 - Memory Study",
)
# 返回：{"success": bool, "wiki_source_path": "...", "wiki_source_id": "source.smith-2025-memory"}
```

**输出最小可用 YAML**（agent 自己后续补 narrative）：
- `pageType: source`
- `id: source.<slug>`
- `zotero_item_key` / `zotero_doi`
- `provenance.type: local_upload`
- body 标注"PENDING — 等待 agent 攥写笔记" + agent 待办清单

---

## 四、明确边界（v6.0.3 教训沉淀）

| 工具提供 | 工具不做 |
|----------|----------|
| ✅ Zotero 建条目（基于 DOI）| ❌ 替 agent 决策 slug / title / tags |
| ✅ WebDAV 推 PDF（rclone）| ❌ PDF attachment 上传 Zotero（v6.0.4 TODO）|
| ✅ wiki source 最小 YAML（幂等检查）| ❌ 攥写笔记 / 综述（agent 的活）|
| ✅ 工具参数解析 + JSON 输出 | ❌ 调 LLM（保持"避费用"决策）|

### ⚠️ 已知约束

- **`--slug` 必填**：避免工具替 agent 决策命名（v6.0.3 教训）
- **slug 已存在**：返回 `success: false`，**不覆盖**——agent 自己决定如何处理（merge / 改名 / 跳过）
- **PDF attachment 上传 Zotero**：当前不支持（v6.0.4 TODO）——只建条目，不绑 PDF；要绑 PDF 需手工在 Zotero 客户端操作

---

## 五、典型工作流（agent 视角）

老板给本地 PDF + DOI，要求"上传到研究库"：

1. **agent 决定 slug**（基于 PDF 命名 / DOI 派生的合理 slug）
2. **agent 跑 upload**：
   ```bash
   python3 main.py upload \
     --pdf-path /data/local-pdfs/smith-2025-memory.pdf \
     --slug smith-2025-memory \
     --doi "10.1234/example.2025.001" \
     --tags "review"
   ```
3. **拿到 wiki source YAML**（最小可用，含 agent 待办清单）
4. **agent 用 summarize 提数据**：
   ```bash
   python3 main.py summarize \
     --source-id source.smith-2025-memory \
     --pdf-path /data/local-pdfs/smith-2025-memory.pdf
   ```
5. **agent 拿 summarize 数据 → 攥写 narrative → 改 wiki source body**

工具不攥写 narrative，agent 自決怎么整理笔记。

---

## 六、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v6.0.3 | 2026-06-23 | 初版：upload 模块上线（download 反向对偶）；CLI `upload --pdf-path/--slug/--doi`；严格遵循"工具不替代 agent"原则（slug 必填 agent 传） |