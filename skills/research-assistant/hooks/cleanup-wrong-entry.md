# Hook: 清理错误 add-doi 入库的 item

> **触发**：`add-doi` 后发现 Zotero item 标题和论文不符。

## 检测

```bash
python3 ~/.openclaw/skills/zotero/scripts/zotero.py get <ITEMKEY> | head -8
# 对比 wiki source 的 title，标题不一致 = 错误
```

## 清理

```bash
# 移到回收站（默认可恢复）
python3 ~/.openclaw/skills/zotero/scripts/zotero.py delete <WRONG_ITEMKEY> --yes

# 永久删除
python3 ~/.openclaw/skills/zotero/scripts/zotero.py delete <WRONG_ITEMKEY> --permanent --yes
```

## 验证

```bash
python3 ~/.openclaw/skills/zotero/scripts/zotero.py get <WRONG_ITEMKEY> 2>&1
# 应返回 404 / not found
```

## 实际案例（v5.13.2 触发）

`add-doi 10.1016/j.tics.2014.01.008` → 实际 add 进 "The compulsive habit of cars"（错的，DOI 月份错）
→ `delete J3XZ6XMX --yes` 移到回收站
→ 改用正确 DOI `10.1016/j.tics.2014.04.012` 重新 add
