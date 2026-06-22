# 元数据维护（v5.14.0 重构）

> **v5.14.0 重大重构**：删 `MetadataManager` / `VersionController`（老板 19:39 指令）。
> - 旧项目级 `metadata.json` 维护 → 废弃（项目元数据应放 wiki frontmatter 或独立 config）
> - 旧 `temp/draft/{title}/` 版本快照 → 改用 git（wiki 已在 git 里）
> - Maintain 模块定位：**协调器**——只引导到 9 个 hooks/ SOP，不直接操作文件

---

## 一、维护对象（v5.14.0 唯一：wiki-zotero-webdav 三联动）

| 角色 | 存储位置 | 内容 | 维护工具 |
|---|---|---|---|
| **wiki** | `~/.openclaw/wiki/` | sources / syntheses / concepts / entities / reports | 文本编辑 + wiki_apply |
| **zotero** | Zotero 库 + 坚果云同步 | 文献条目 metadata（题录、tags、collections） | `zotero.py` (Web API v3) |
| **webdav** | `nutstore:quanquanzi/zotero/storage/` | PDF / images / supplementary | `rclone` |

**全部维护操作**走 `hooks/` 目录 9 个 SOP（见下），不直接动 Python 代码。

---

## 二、9 个 hooks 工作流

### `hooks/add-zotero-source.md`（核心）

> **触发**：wiki 新建 source ↔ Zotero item 双向建立

**5 步流程**：
1. 查 Zotero 库（按 title / DOI / author）
2. 验证 WebDAV PDF 是否存在（`rclone lsf nutstore:quanquanzi/zotero/`）
3. 补 wiki YAML（`zotero_item_key` / `zotero_attachment_key` / `zotero_pdf_path` / `zotero_doi`）
4. 加 Zotero 反向 tag（`wiki:source.<id>`）
5. 验证双向跳转（`zotero://select/library/items/<KEY>` ↔ `obsidian://open?vault=wiki&file=sources/<file>.md`）

### 失败处理 hooks

| 失败 | hook |
|---|---|
| add-doi 失败（CrossRef 404 / 翻译 503） | `manual-add-item.md` |
| add-doi 进错论文 | `cleanup-wrong-entry.md` |
| wiki source 找不到 Zotero item | `wiki-source-missing-in-zotero.md` |
| PATCH 428 (version header) | `zotero-patch-with-version.md` |
| arXiv title 解析 bug | `arxiv-title-parse.md` |

### 同步与漂移 hooks

| 任务 | hook |
|---|---|
| Zotero → wiki 增量同步 | `sync-zotero-new-items.md` |
| 检查 wiki-zotero-webdav 漂移 | `check-drift.md` |
| rclone / WebDAV 配置（首次接入） | `rclone-webdav-setup.md` |

---

## 三、维护操作（按使用频率排序）

### 1. 新建 source → 联动 Zotero

```bash
# Step 1: 查 Zotero
python3 ~/.openclaw/skills/zotero/scripts/zotero.py search "<title>"

# Step 2: 验证 WebDAV
rclone lsf nutstore:quanquanzi/zotero/ | grep <ATTACHMENT_KEY>

# Step 3-5: 见 add-zotero-source.md
```

### 2. 增量同步（Zotero → wiki）

```bash
python3 ~/.openclaw/skills/zotero/scripts/zotero.py items --limit 20 --sort dateAdded
# 然后逐个检查 + 维护（参考 sync-zotero-new-items.md）
```

### 3. 漂移检测

```bash
grep -h "^zotero_item_key:" ~/.openclaw/wiki/sources/*.md | awk '{print $2}' > /tmp/wiki_keys.txt
while read key; do
  python3 ~/.openclaw/skills/zotero/scripts/zotero.py get "$key" 2>&1 | head -2
done < /tmp/wiki_keys.txt
```

### 4. 手动添加条目（无 DOI / DOI 失败）

```bash
# 4 种路径见 manual-add-item.md
python3 ~/.openclaw/skills/zotero/scripts/zotero.py add-isbn "<ISBN>"
python3 ~/.openclaw/skills/zotero/scripts/zotero.py add-pmid "<PMID>"
# arXiv → 用 Zotero web API（见 arxiv-title-parse.md + zotero-patch-with-version.md）
```

### 5. rclone / WebDAV 配置（首次接入）

见 `hooks/rclone-webdav-setup.md`

---

## 四、删除记录（v5.14.0）

| 删除项 | 原因 | 替代方案 |
|---|---|---|
| `MetadataManager` 类 | 老板 19:39 指令"用不到了、全部转移到 wiki" | wiki frontmatter YAML 自描述元数据 |
| `VersionController` 类 | 同上 | git 管理 wiki 版本（wiki 已在 git 里） |
| 项目级 `metadata.json` 维护 | 同上 | wiki 是统一存储 |
| `temp/draft/{title}/` 版本快照 | 同上 | git history |
| 旧 CLI 命令（update-kb / save-version / list-versions 等） | 同上 | hooks/ 目录 SOP |

---

## 五、数据一致性原则（v5.14.0 简化）

| 数据类型 | 单一来源 |
|---|---|
| 文献元数据（题录、作者、年份） | **Zotero 库**（绝对权威） |
| PDF / 附件 | **WebDAV**（Zotero 自动同步） |
| 笔记 / 摘要 / 概念 | **wiki**（人可读视图） |

一一对应铁律见 `wiki/AGENTS.md`：
- 1 Zotero item → 1 wiki source 页 ✅ 强制
- 1 wiki source 页 → 1 Zotero item ✅ 强制
- 1 Zotero item → 0..N wiki synthesis/concept 页 ✅ 自由

---

## 六、参考

- **wiki AGENTS.md v4**：`~/.openclaw/wiki/AGENTS.md`（**三联动规则的源头**）
- **zotero skill**：`~/.openclaw/skills/zotero/SKILL.md`（Web API v3 工具）
- **download skill**（本 skill 内）：`module-download.md`（PDF 下载到坚果云）
- **dashboard.md**：`~/.openclaw/skills/research-assistant/dashboard.md`（实时状态）
- **hooks/**：`~/.openclaw/skills/research-assistant/hooks/`（9 个 SOP）


---

## 二、WikiZoteroManager Python 类（v5.15.0 新增）

### 文件位置

`scripts/maintain/WikiZoteroManager.py`（9434 bytes）

### 5 个核心方法

| 方法 | 用途 | 输入 | 输出 |
|------|------|------|------|
| `list_wiki_sources()` | 列出所有 wiki source + 解析 YAML | - | list[dict]（含 zotero_item_key, zotero_doi, pageType） |
| `verify_zotero_item(item_key)` | 验证 Zotero item 存在 + 拿元数据 | itemKey | dict（title, version, tags） |
| `check_webdav_pdf(att_key)` | 检查 WebDAV PDF 可达 | attachment key | bool + found_files |
| `check_drift()` | 漂移检测（4 类型） | - | dict{ok, missing_key, zotero_not_found, webdav_missing} |
| `generate_drift_report()` | 写 `wiki/reports/wiki-zotero-drift-<date>.md` | - | report path |

### CLI 用法

```bash
python3 WikiZoteroManager.py list-sources         # 列出所有 wiki source
python3 WikiZoteroManager.py check-drift          # 跑漂移检测
python3 WikiZoteroManager.py generate-report      # 写 reports/
python3 WikiZoteroManager.py verify <KEY>         # 验证 Zotero item
python3 WikiZoteroManager.py add-tag <KEY> <WIKI_ID>  # 加 wiki:source.<id> tag
```

### 首跑结果（v5.15.0 上线）

- 🟢 7 OK / 🔴 7 缺（全工具类按 AGENTS.md v4 规则不需要）/ 0 漂移
- 14 个 wiki source 中 7 个学术已对齐 Zotero，7 个工具类按 v4 规则跳过

### 与 main.py CLI 集成

通过 `main.py maintain <子命令>` 调度（详见 module-maintain.md 后续章节）。
