# Hook: concept / synthesis 页 ↔ Zotero 联动 SOP

> **触发场景**：在 wiki `concepts/` 或 `syntheses/` 创建或编辑页面，需要引用论文（Zotero item）时。
>
> **规则源**：`~/.openclaw/wiki/AGENTS.md` v4（联动字段 Schema 章节）
>
> **v5.15.0 状态**：规则已写入 AGENTS.md，**本 hook 是 skill 端的 SOP 实施步骤**。

---

## 判定：是否需要 zotero_refs？

| 页类型 | zotero_refs 必填？ |
|---|---|
| `sources/` | 不需要（用 `zotero_item_key` 单数字段） |
| `concepts/` | **可选**（仅当概念由论文支撑时填） |
| `syntheses/` | **必填**（写 synthesis 必然引用论文） |
| `reports/` | 可选（仅当报告引用论文时填） |

**判断标准**：
- ✅ 概念核心定义/机制/例证来自具体论文 → 必须填 `zotero_refs`
- ❌ 纯工具/技术/组织类概念（OpenClaw / Pandoc / rclone）→ 留空

---

## Step 1：找 Zotero itemKey

```bash
# 按 title 搜
python3 ~/.openclaw/skills/zotero/scripts/zotero.py search "<paper title>"

# 按 DOI 直接取
python3 ~/.openclaw/skills/zotero/scripts/zotero.py --json get <ITEMKEY> | jq '.title'

# 失败时（CrossRef 404）→ 见 hooks/manual-add-item.md
```

**记录**：`itemKey`（8 字符）+ 可选 `citekey`（Better BibTeX 生成）

---

## Step 2：补 wiki YAML 字段

### concepts/ 页（可选）

```yaml
---
pageType: concept
id: concept.phase-precession
title: 相位进动
zotero_refs:                        # 可选：仅当概念由论文支撑时填
  - key: OKEFE1993PHASE
    citekey: okeefe1993phase
    role: source                    # source | definition | example
  - key: BUZSAKI2002THETA
    role: supporting
---
```

### syntheses/ 页（必填）

```yaml
---
pageType: synthesis
id: synthesis.online-memory-llm-2026
title: LLM 在线记忆机制综述
zotero_refs:                        # 必填，至少 1 个
  - key: WSZJGS59                   # δ-mem
    citekey: dmem2026lei
    role: primary                   # primary | supporting | background
  - key: S2H6ZG5Q                   # Reflexion
    role: supporting
  - key: VNPN6FHT                   # 其它
    role: background
---
```

### reports/ 页（可选）

```yaml
---
pageType: report
id: report.cognitive-load-analysis-2026
title: 认知负荷 EEG 数据分析报告
local_path: /root/.../report.pdf
zotero_refs:                        # 可选
  - key: ERZMJJTP
    role: methodology
---
```

---

## Step 3：双向 tag（可选，但推荐）

如果 concept/synthesis 是从 Zotero item 抽象出来的，给 item 加反向 tag：

```bash
# 用 WikiZoteroManager.add_wiki_tag
python3 -c "
import sys; sys.path.insert(0, '/root/.openclaw/skills/research-assistant/scripts')
from maintain.WikiZoteroManager import WikiZoteroManager
mgr = WikiZoteroManager()
ok = mgr.add_wiki_tag('<ITEMKEY>', 'concept.phase-precession')
print('✅' if ok else '❌')
"
```

**tag 格式**：
- 概念反向到 source → `wiki:concept.<id>`（加在 source 所属 Zotero item 上）
- 综述反向到 source → `wiki:synthesis.<id>`（加在所有引用的 Zotero item 上）

⚠️ 注意：source 自己的反向 tag 仍是 `wiki:source.<id>`，不冲突。

---

## Step 4：验证双向

| 方向 | 验证方式 |
|---|---|
| wiki → Zotero | 点 wiki YAML 里的 `zotero://select/library/items/<KEY>` 链接 |
| Zotero → wiki | 在 Zotero 看 tag `wiki:concept.<id>` 或 `wiki:synthesis.<id>` 能否跳转 |

---

## 工具函数（WikiZoteroManager v5.15.0）

未来在 `WikiZoteroManager.py` 加方法：

```python
def find_concepts_by_zotero_key(self, item_key):
    """找所有引用某 Zotero item 的 wiki concept 页"""
    ...

def find_syntheses_by_zotero_key(self, item_key):
    """找所有引用某 Zotero item 的 wiki synthesis 页"""
    ...
```

当前 v5.15.0：**手动**——用 `grep` 扫所有 concept/synthesis 页的 `zotero_refs` 字段。

---

## 失败处理

| 失败 | 处理 |
|---|---|
| Zotero 找不到 paper | `hooks/manual-add-item.md` 4 路径 |
| 已知 wiki 引用了 paper 但 Zotero item 被删 | `hooks/check-drift.md` 漂移检测 |

---

## 一致性原则

- **concepts/ 和 syntheses/ 不重复论文元数据**——只引用 Zotero itemKey
- **Zotero 库是论文元数据唯一权威**——不在 wiki 重复 author/year/DOI 等
- **角色标注清晰**：每个 zotero_ref 都要标 `role`（primary / supporting / background / source / definition / example）
