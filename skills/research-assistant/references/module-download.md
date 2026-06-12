# 文献下载模块使用指南

> **2026-06-12 实战沉淀**。`download` 模块从 Zotero 库 → 坚果云 WebDAV → wiki raw 自动下载并归档 PDF。
> **核心设计**：DOI / Zotero key → 找元数据 → 下载 PDF → 归档到 wiki raw。

---

## 三步流水线

```
research-assistant download --doi 10.1177/...        (或 --zotero-key R8MVF42R)
                          ↓
                1. find_paper: Zotero API 查元数据
                          ↓
                2. download_pdf: 坚果云 WebDAV GET PDF
                          ↓
                3. archive_to_wiki: 按 YYYY-MM-DD_作者_关键词_期刊.pdf 归档
```

---

## YAML 头示例（apaquarto-pdf）

apaquarto-pdf 跟下载**不相关**——apaquarto 是**排版**模块。下载是**CLI 命令**。

---

## CLI 完整命令

### 基本用法

```bash
# 按 DOI 下载
research-assistant download --doi 10.1177/0956797617694868

# 按 Zotero item key 下载
research-assistant download --zotero-key R8MVF42R

# 指定 wiki raw 目录
research-assistant download --doi 10.1177/0956797617694868 --wiki-raw-dir /path/to/wiki/raw/papers

# 指定临时下载目录
research-assistant download --doi 10.1177/0956797617694868 --tmp-dir /tmp/zotero_dl
```

### 参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--doi DOI` | 二选一 | — | DOI（如 `10.1177/0956797617694868`，以 `10.` 开头）|
| `--zotero-key KEY` | 二选一 | — | Zotero item key（8 字符 alnum，如 `R8MVF42R`）|
| `--wiki-raw-dir PATH` | ❌ | `/root/.openclaw/wiki/raw/papers` | wiki raw 论文归档目录 |
| `--tmp-dir PATH` | ❌ | `/tmp/zotero_dl` | 临时下载目录（解压 WebDAV .zip）|

### 互斥参数

`--doi` 和 `--zotero-key` **二选一**（mutually_exclusive_group）。

---

## 凭据（.env 文件）

下载模块需要以下凭据，存放在 `~/.openclaw/.env`：

```bash
# Zotero API
ZOTERO_USER_ID=12345678
ZOTERO_API_KEY=your_zotero_api_key_here

# 坚果云 WebDAV
JIANGUOYUN_USER=yangquan0310@qq.com
JIANGUOYUN_PASSWORD=your_jianguoyun_password

# wiki 归档目录
WIKI_RAW_PAPERS_DIR=/root/.openclaw/wiki/raw/papers
```

**缺少凭据会报错**，不会静默失败。

---

## 内部实现：三步流水线

### Step 1: find_paper(identifier)
- 输入：DOI 字符串 / Zotero item key
- 通过 Zotero API 查 item + attachment + MD5
- 返回 `PaperMetadata` 对象（含 zotero_attachment_key, md5, authors, year, title, journal）

### Step 2: download_pdf(meta, dest_dir)
- 通过坚果云 WebDAV GET `{attachment_key}.zip`（**注意**：8 字符 hash = Zotero attachment key，**不是** MD5 前 8 位）
- 解压 zip 提取 PDF
- 保存到 `dest_dir`

### Step 3: archive_to_wiki(pdf, meta)
- 文件名格式：`YYYY-MM-DD_作者_关键词_期刊.pdf`（如 `2024-03-15_WangAI_aging_psych.pdf`）
- 复制到 `wiki_raw_dir`
- 删除临时文件

### 完整流水线 run(identifier)

```python
from scripts.download import ZoteroJianguoyunDownloader

downloader = ZoteroJianguoyunDownloader()
meta = downloader.find_paper(identifier)  # Step 1
pdf = downloader.download_pdf(meta, tmp_dir)  # Step 2
archive_path = downloader.archive_to_wiki(pdf, meta)  # Step 3
print(f"Archived to: {archive_path}")
```

---

## 多态设计（基类 Downloader）

```python
class Downloader(ABC):
    @abstractmethod
    def find_paper(self, identifier: str) -> PaperMetadata: ...

    @abstractmethod
    def download_pdf(self, meta: PaperMetadata, dest_dir: Path) -> Path: ...

    @abstractmethod
    def archive_to_wiki(self, pdf: Path, meta: PaperMetadata) -> Path: ...

    def run(self, identifier: str) -> Path:
        """默认流水线：find → download → archive"""
        meta = self.find_paper(identifier)
        pdf = self.download_pdf(meta, Path(self.tmp_dir))
        return self.archive_to_wiki(pdf, meta)
```

**当前唯一实现**：`ZoteroJianguoyunDownloader`（老板专属 Zotero + 坚果云同步）。

**未来扩展**：可加 `SciHubDownloader`、`InstitutionalDownloader` 等子类。

---

## 关键发现（2026-06-05 Diehl 2026 实战沉淀）

- **8 字符 hash = Zotero attachment key**（**不是** MD5 前 8 位）
- 老板 Zotero 库 attachment 模式多为 `imported_url`，PDF 缓存到 Zotero Storage
- 反查路径：MD5 → 8 字符 hash（用 `.prop` 文件建索引）

---

## 实战要点

| 要点 | 说明 |
|------|------|
| **DOI 优先** | Zotero key 必须先入库（手动）才能用；DOI 任何时候都能下 |
| **凭据必填** | 缺任一 .env 必报错 |
| **wiki 归档命名** | `YYYY-MM-DD_作者_关键词_期刊.pdf`（时间倒序、便于查重）|
| **解压 zip** | WebDAV 返回 .zip 需解压出 PDF |
| **清理临时** | 临时目录 `/tmp/zotero_dl` 定期清理 |
| **错误重试** | 单次失败不重试，**手动** `--doi` 重跑 |

---

## 常见错误排错

| 错误 | 原因 | 修复 |
|------|------|------|
| `Zotero API 404` | DOI 不在 Zotero 库 | 手动用 Zotero connector 添加 |
| `WebDAV 404` | 坚果云 attachment 未同步 | 打开 Zotero 触发同步 |
| `MD5 mismatch` | 坚果云文件损坏 | 重新下载（手动）|
| `Permission denied` | wiki raw 目录权限 | `chmod 755` |
| `Identifier format invalid` | DOI 不以 10. 开头或 Zotero key 非 8 字符 | 检查输入 |

---

## 引用语法

不适用（下载是 CLI 操作，不生成引用）。

---

## 关键源码文件

- `scripts/download/Downloader.py` — 基类（多态接口）
- `scripts/download/ZoteroJianguoyunDownloader.py` — 老板专属实现
- `scripts/download/paper_metadata.py` — PaperMetadata 数据类
- `scripts/download/utils.py` — 工具函数
- `scripts/main.py` — CLI 入口（`--doi` / `--zotero-key` 参数）

---

## 关键参考文献

- 实战沉淀：2026-06-05 Diehl 2026 论文（Open Science Framework 数据）下载
- Zotero Web API v3：https://www.zotero.org/support/dev/web_api/v3/start
- 坚果云 WebDAV：https://www.jianguoyun.com/

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.0 | 2026-06-12 | 初版：基于现有 `scripts/download/` Python 实现 + 2026-06-05 Diehl 2026 实战沉淀。 |
