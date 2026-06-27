# module-download.md（v7.0.0，含 v6.0.7 SciHub 整合）

> download 模块：PDF 下载
> - **默认**（`--source zotero`）：Zotero → WebDAV → wiki raw（论文必须先在 Zotero 库——避免乱下载到老板的坚果云）
> - **可选**（`--source scihub`）：SciHub → wiki/raw/papers（绕过付费墙，不动老板坚果云，仅落本地归档）

## 类清单

- `Downloader` (ABC) — 抽象基类
- `ZoteroJianguoyunDownloader` — 老板专属 Zotero + 坚果云实现（`--source zotero`）
- `SciHubDownloader` — SciHub 绕过付费墙实现（`--source scihub`），零外部依赖 + ALTCHA 验证码处理
- `PaperMetadata` (dataclass) — 元数据 + 归档文件名生成

## 类 / 方法职责

| 类 | 方法 | 作用 |
|----|------|------|
| `Downloader` (ABC) | `find(identifier) -> PaperMetadata` | abstract |
| `Downloader` (ABC) | `pull(meta, dest_dir) -> Path` | abstract |
| `Downloader` (ABC) | `save(pdf, meta, dest_dir) -> Path` | abstract |
| `Downloader` | `fetch(identifier, dest_dir, archive_dir) -> Path` | 主入口：find + pull + save（幂等） |

## CLI 用法

```bash
# 默认走 Zotero + 坚果云（论文必须先在 Zotero 库）
python3 scripts/main.py download --doi 10.1177/0956797617694868
python3 scripts/main.py download --zotero-key BNA4WATT

# 走 SciHub（绕过付费墙，仅落 wiki/raw/papers，不写 Zotero / 不动坚果云）
python3 scripts/main.py download --doi 10.1177/0956797617694868 --source scihub

# 自定义归档目录
python3 scripts/main.py download --doi 10.xxx --source scihub --archive-dir /data/papers
```

## 两个下载源的取舍

| 维度 | `--source zotero`（默认） | `--source scihub` |
|------|---------------------------|---------------------|
| 论文是否需先在 Zotero | ✅ 是（设计原则：避免乱下载到老板的坚果云） | ❌ 否 |
| 输出位置 | Zotero 库 + 坚果云 WebDAV + wiki raw（**三联动**） | 仅 wiki/raw/papers（不动 Zotero / WebDAV） |
| 元数据来源 | Zotero API（含 MD5 / 附件 key） | SciHub 页面 `citation_*` meta（轻量，缺 MD5） |
| 凭据要求 | `ZOTERO_*` + `JIANGUOYUN_PASSWORD` | 无 |
| 镜像健壮性 | WebDAV 自动重试（429/503 退避） | 6 镜像 fallback + ALTCHA 验证码自动解 + 状态语义（FOUND/NOT_FOUND/OA_LINK/MIRROR_ERROR）|
| 适用场景 | 已入 Zotero 库的论文 | Zotero 里没有、临时要读全文的论文 |

## v6.0.7 SciHub 整合说明

- **整合源**：原独立技能 `scihub-paper-downloader`（v1.0.3）已合并到本模块的 `SciHubDownloader`；原技能目录已删除
- **零依赖**：`SciHubDownloader` 仅用 Python stdlib（urllib / http / hashlib / json），无需 `requests`
- **状态语义**：4 种返回值——`FOUND`（拿到 PDF URL）/ `NOT_FOUND`（库无 + 可选 OA_LINK 提示）/ `MIRROR_ERROR`（所有镜像不可达）/ `INVALID_INPUT`（DOI 格式无效）
- **验证码**：内置 ALTCHA 解码器（v1.0.3 起），镜像被弹验证码时自动解

## 镜像配置（config.json 优先）

镜像列表 + 超时配置的优先级链（v6.0.7+ 老板 05:16 指令）：

```
config.json 的 scihub.mirrors / request_timeout / pdf_timeout / min_pdf_size
    ↓ 未设置时
SCIHUB_MIRRORS 环境变量（逗号分隔）
    ↓ 未设置时
DEFAULT_MIRRORS hardcoded 兑底（6 镜像）
```

**修改优先级**（v6.0.7 改：默认走 config.json，不依赖 env）：

```bash
# 1. 编辑 config.json（推荐）
vim ~/.openclaw/skills/research-assistant/scripts/config.json
#   "scihub": {
#     "mirrors": ["https://sci-hub.st", "https://sci-hub.se", ...],   # 顺序 = 优先级
#     "request_timeout": 20,
#     "pdf_timeout": 120,
#     "min_pdf_size": 1024
#   }

# 2. 临时覆盖（CI/调试）
SCIHUB_MIRRORS="https://custom1.example.com,https://custom2.example.org" \
  python3 scripts/main.py download --doi 10.xxx --source scihub
```

## 全失败反馈（structured feedback，v6.0.7+）

所有镜像都不可访问时，CLI 返结构化 JSON 而非纯字符串错误：

```json
{
  "success": false,
  "identifier": "10.1038/nature12373",
  "source": "scihub",
  "error": "SciHub 所有 6 个镜像都不可访问（DOI: 10.1038/nature12373）: ...",
  "error_type": "scihub_all_mirrors_failed",
  "mirrors_tried": ["https://sci-hub.st", "https://sci-hub.se", ...],
  "last_errors": [
    "https://sci-hub.st → HTTPError: HTTP Error 403: Forbidden",
    "https://sci-hub.se → URLError: <urlopen error [SSL: ...]>",
    ...
  ],
  "suggestion": "1) 加论文到 Zotero 库改走 --source zotero ... 2) 等待几分钟后重试 ... 3) 检查网络/代理 ... 4) 编辑 config.json 的 scihub.mirrors ..."
}
```

**异常类**：`scripts.download.scihub.SciHubAllMirrorsFailedError`（带 `mirrors_tried` / `last_errors` / `doi` 字段）。CLI `cmd_download` 用 `isinstance` 捕获后转结构化 JSON。

## 凭据

| 字段 | 来源 | 兑底 |
|------|------|------|
| `ZOTERO_USER_ID` | `config.json` 的 `zotero.user_id` | `~/.openclaw/.env` 的 `ZOTERO_USER_ID` |
| `ZOTERO_API_KEY` | `config.json` 的 `zotero.api_key` | `~/.openclaw/.env` 的 `ZOTERO_API_KEY` |
| `JIANGUOYUN_PASSWORD` | `config.json` 的 `jianguoyun.password` | `~/.openclaw/.env` 的 `JIANGUOYUN_PASSWORD` |

## 工具定位

download 返 PDF 路径（dict），不返 narrative。流水线 `find + pull + save` 由 `fetch()` 一次完成。