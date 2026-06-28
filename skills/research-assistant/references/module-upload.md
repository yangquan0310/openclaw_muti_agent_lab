# module-upload.md（v7.0.0）

> upload 模块：本地 PDF → Zotero + WebDAV + wiki source（download 的反向对偶）

## 类清单

- `Uploader` — 单一类

## 类 / 方法职责

| 方法 | 作用 |
|------|------|
| `__init__(cfg)` | 从 config 读 rclone + jianguoyun.remote_root + upload.agent_id_env |
| `upload(pdf_path, doi, slug, title, tags, skip_zotero, skip_webdav, skip_wiki) -> dict` | **主入口**：add_to_zotero + push_webdav + create_wiki_source |
| `_add_to_zotero(doi, tags) -> dict` | subprocess 调 zotero.py add-doi |
| `_push_webdav(pdf_path) -> dict` | rclone copyto 推 PDF |
| `_create_wiki_source(slug, pdf_path, zotero_meta, title) -> dict` | 写 wiki/sources/<slug>.md |
| `_humanize_title_from_filename(pdf_path) -> str` | 从 PDF 文件名解析 title |

## CLI 用法

```bash
# 完整流水线（默认跑全部三步）
python3 scripts/main.py upload --pdf-path /data/local-pdfs/smith-2025.pdf --slug smith-2025 --doi "10.1234/example.2025.001"

# 跳过某步
python3 scripts/main.py upload --pdf-path X.pdf --slug X --no-zotero
python3 scripts/main.py upload --pdf-path X.pdf --slug X --no-webdav
python3 scripts/main.py upload --pdf-path X.pdf --slug X --no-wiki

# 自定义 title / tags
python3 scripts/main.py upload --pdf-path X.pdf --slug X --title "Smith 2025" --tags "review,important"
```

## 工具边界

- ❌ 不攥写笔记 / 综述
- ❌ 不调 LLM
- 只搬运数据 + 写最小可用 wiki source YAML
- 笔记 narrative 由 agent 攥写（拿到 wiki source 后）