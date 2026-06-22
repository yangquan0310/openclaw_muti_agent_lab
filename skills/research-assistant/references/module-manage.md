# 知识库管理（v5.16.0+ 全部走 wiki）

> **v5.16.0 重大重构**：删旧 `Manager.py`（走 knowledge/index.json 旧路径），新 `Manager.py` 直接以 wiki 为存储（替代品 `WikiManager.py` 已重命名为默认名）。
> **老板 00:08 指令**："不需要向后兼容，全部改为 wiki"。

---

## 一、Manager（v5.16.0+ wiki 版本）

### 文件位置

`scripts/manage/Manager.py`（6162 bytes）

### 4 个核心方法

| 方法 | 用途 | 输入 | 输出 |
|------|------|------|------|
| `list_sources()` | 列出所有 wiki source | - | list[dict]（id, file, title, zotero_item_key, zotero_doi, pageType） |
| `merge(*source_ids)` | 按 zotero_item_key 去重合并 | source id 列表 | list[dict]（已去重） |
| `filter(conditions)` | 按 YAML 字段筛选 source | dict（has_zotero_key/has_doi/pageType） | list[dict] |
| `statistics()` | 统计 wiki 现状 | - | dict（total_sources, total_concepts, total_syntheses, total_reports） |

### CLI 用法

```bash
python3 main.py manage list                    # 列出所有 wiki source
python3 main.py manage stats                   # wiki 统计（14 sources / 47 syntheses / 54 concepts）
python3 main.py manage filter --has-zotero-key true   # 筛已对齐 Zotero 的
python3 main.py manage filter --has-zotero-key false  # 筛缺字段的
python3 main.py manage filter --page-type source       # 筛 pageType
python3 main.py manage merge --inputs source.diehl-...,source.buzsaki-...  # 按 zk 去重合并
```

### 不向后兼容

- 旧 `knowledge/index.json` 路径**已废弃**
- 旧 Manager 备份在 `_legacy_Manager_<TS>.py`
- 任何依赖旧 CLI (`--kb-path`, `--inputs` 等) 的脚本需更新

### demo（v5.16.0 上线）

```
Total: 14 sources / 47 syntheses / 54 concepts / 13 reports
7 学术 source 已对齐 Zotero
7 工具类 source 按 v4 规则跳过
```

### 与 wiki/AGENTS.md 配合

- 一一对应铁律：1 Zotero item = 1 source 页
- 工具类 source（conda/openclaw-system 等）不需 zotero_item_key
