# module-maintain.md（v7.0.0）

> maintain 模块：wiki ↔ Zotero ↔ WebDAV 三方一致性检查

## 类清单

- `DriftChecker` — 单一类

## 类 / 方法职责

| 方法 | 作用 |
|------|------|
| `__init__(cfg)` | 读 config.zotero + jianguoyun + 兑底 ~/.openclaw/.env |
| `check() -> dict` | **主入口**：扫所有 wiki sources + 查 Zotero + WebDAV<br>返 `{ok, missing_key, zotero_not_found, webdav_missing, non_academic}` |
| `missing() -> list[dict]` | 缺 zotero_item_key 的 sources（学术型） |
| `report(drift, output_path) -> Path` | 写 wiki/reports/wiki-zotero-drift-<date>.md |
| `graph(mode) -> str` | ASCII 状态图（`"light"` / `"full"`） |

## CLI 用法

```bash
# 主检查
python3 scripts/main.py maintain check

# 列出缺 zotero_item_key 的 sources
python3 scripts/main.py maintain missing

# 生成漂移报告
python3 scripts/main.py maintain report

# ASCII 状态图
python3 scripts/main.py maintain graph              # light 模式（秒级）
python3 scripts/main.py maintain graph --full       # full 模式（跑完整三方）
```

## 返回结构

```python
{
    "ok": [...],                    # 三方同步正常
    "missing_key": [...],           # 学术型 source 缺 zotero_item_key
    "zotero_not_found": [...],      # Zotero 库无此 item
    "webdav_missing": [...],        # WebDAV 缺 PDF
    "non_academic": [...],          # 非文献型（豁免）
}
```

## 工具定位

maintain 返结构化报告（dict / markdown / ASCII 图），不返 narrative。**只检查不修复**——修复操作由 agent 根据报告执行。