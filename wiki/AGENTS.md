# Memory Wiki Agent Guide (全局共享)

- **本 wiki 为所有代理共享，任何代理均可读写。**
- Treat generated blocks as plugin-owned.
- Preserve human notes outside managed markers.
- Prefer source-backed claims over wiki-to-wiki citation loops.
- Prefer structured `claims` with evidence over burying key beliefs only in prose.
- Use `.openclaw-wiki/cache/agent-digest.json` and `claims.jsonl` for machine reads; markdown pages are the human view.

## 8 个核心角色的用途约定

> **6 个 wiki 目录 + 2 个外部存储**（Zotero 元数据 / WebDAV 附件）。每个角色有明确的边界，代理写入时必须匹配。

| 角色 | 存储位置 | 用途 | 处理深度 | 写入规则 |
|------|----------|------|----------|----------|
| **`raw/`** | wiki | 证据层，存放原始文件（PDF/OCR/笔记/资产） | **零处理**——只归档 | 文件原样存放，不做内容修改 |
| **`sources/`** | wiki | 存放**来源摘要**（每个 Zotero 条目对应一个 source summary） | **轻提炼**——一句话总结 + 关键内容 + 影响页面 + 待确认 | 详见 `sources/_template_source_summary.md` 模板 |
| **`syntheses/`** | wiki | 存放**总结**（综合分析、综述、论据链） | **重提炼**——多源综合 + 论证 + 结论 | 必须 source-backed（每个论断有 Zotero 条目引用） |
| **`concept/`** | wiki | 存放**概念**文件（抽象概念的定义与关系） | **抽象归纳**——从具体 source 抽出通用概念 | 概念是跨多篇 source 的归纳；如涉及论文则通过 `zotero_refs` 联动 |
| **`entities/`** | wiki | 存放**实体**（人物/机构/项目/工具等具象对象） | **抽象归纳**——把具象对象结构化 | 实体是具体的、可指向的对象 |
| **`reports/`** | wiki | 存放**客观报告**（lint/contradictions/open-questions 等） | **可重复生成**——机器或人工客观产出 | 内容必须是可验证的、不是主观论断 |
| **Zotero 库** | Zotero 本地库 + 坚果云同步 | 条目**元数据**（题录/tags/collections/relations） | **结构化管理**——Zotero 客户端 / Web API | 1 个学术条目 = 1 个 Zotero item |
| **WebDAV (坚果云)** | `nutstore:quanquanzi/zotero/storage/` | 条目**附件**（PDF / images / supplementary materials） | **零处理**——Zotero 自动同步 | Zotero 端配置附件链接/存储位置 |



## 9 个核心角色的依赖与流向（v4：工具类排除）

> v4 升级（2026-06-21）：**`sources/` 页分为两类**——"学术 source"必须满足一一对应铁律（zotero_item_key 必填），"技术 source"（工具/平台/系统笔记）**不**参与铁律，**不**强制 zotero_item_key。

| 类型 | 判定 | zotero_item_key |
|---|---|---|
| **学术 source** | paper / review / meta-analysis / preprint | ✅ 必填 |
| **技术 source** | tool / system / platform / language / config | ❌ 不需要 |

**判定方法**：看 wiki source 页面的 YAML `pageType` 与正文内容。

- 若 source 引用 DOI / arXiv / 期刊 / 学术会议 → 学术 → 必须有 zotero_item_key
- 若 source 是工具说明（conda、openclaw-system、programming-languages）→ 技术 → 跳过

**当前 P2 工具类 source**（7 个，不需维护）：conda / deepseek-cloud-local-hybrid / openclaw-env / openclaw-system / openclaw-workspace / programming-languages / repository

## 8 个角色的依赖与流向

```
原始资料 (raw/)
   ↓ 提炼
来源摘要 (sources/)   ← 每个 Zotero 条目 + raw source 必配
   ↓ 引用
总结 (syntheses/)
   ↓ 抽象
概念 (concept/)  +  实体 (entities/)

客观报告 (reports/)   ← 独立于上述链，但可引用任何层

外部存储（与 sources/ 双向联动）：
   ┌── Zotero 库（元数据）
   │     ↕ 双向链接（zotero_item_key ↔ tags: wiki:source.<id>）
   └── WebDAV 坚果云（附件）
```

- **`raw/` 是唯一的事实来源**——任何总结/概念/实体都必须可回溯到一个 raw 资料
- **`sources/` 是 raw + Zotero 的索引**——是双向入口（人工从 Zotero 进、从 raw 进）
- **`syntheses/` 是论证层**——综合多 source + 多 Zotero 条目形成论据链
- **`concept/` 与 `entities/` 是抽象层**——前者抽象概念，后者具体对象
- **`reports/` 是横切层**——可以基于任何层产出客观报告（lint/统计/问题清单）
- **Zotero + WebDAV** 是外部支撑——通过结构化字段（`zotero_item_key` / `tags: wiki:source.<id>`）与 `sources/` 双向联动

## 一一对应铁律（联动核心）

> **让文献和笔记一一对应**——避免 wiki/Zotero 数据漂移。

| 映射 | 是否强制 | 说明 |
|---|---|---|
| **1 Zotero 条目 → 1 source 页** | ✅ 强制 | 每个 Zotero item 必须在 wiki 有对应 source 页 |
| **1 Zotero 条目 → 1 raw 文件** | ✅ 推荐 | 每个 Zotero item 应有对应 raw 文件（PDF/OCR） |
| **1 Zotero 条目 → 0..N synthesis 页** | ✅ 自由 | 老板写笔记时按需引用 |
| **1 source 页 → 1 Zotero 条目** | ✅ 强制 | 不允许 1 个 source 页对应多个 Zotero item |
| **1 concept 页 → 0..N Zotero 条目** | ✅ 自由（按需） | 概念可能由 0..N 篇 paper 共同支撑；纯技术/工具类概念无需填 |

**违反铁律的处理**：先在 `reports/` 创建 `wiki-zotero-drift-<date>.md` 报告，再修复。

## 联动字段 Schema

### wiki 侧 YAML frontmatter

#### `sources/` 页（单一 Zotero 条目）

```yaml
---
pageType: source
id: source.<slug>
title: <标题>
zotero_item_key: <8字符itemKey>     # Zotero $itemKey（必填）
zotero_citekey: <citekey>            # 可选，需装 Better BibTeX
zotero_type: paper | review | meta-analysis  # 可选
raw_path: raw/<path>                 # 可选，对应原始文件
sourceIds:
  - external/<标识>
aliases: [...]
---
```

#### `syntheses/` 页（老板写的综述/分析）

```yaml
---
pageType: synthesis
id: synthesis.<slug>
title: <标题>
zotero_refs:                         # 数组（必填，至少 1 个）
  - key: <itemKey>
    citekey: <citekey>
    role: primary | supporting | background
  - key: <itemKey2>
    role: supporting
---
```

#### `concepts/` 页（抽象概念，**可选**引文）

```yaml
---
pageType: concept
id: concept.<slug>
title: <概念名>
zotero_refs:                         # 可选：仅当概念由论文支撑时填
  - key: <itemKey>
    citekey: <citekey>
    role: source | definition | example
  - key: <itemKey2>
    role: supporting
---
```

> **判定标准**：如果一个 concept 的核心定义/机制/例证来自具体论文，**必须**在 `zotero_refs` 中列出；纯工具/技术/组织类概念（如"OpenClaw"、"Pandoc"）不涉及论文，留空即可。

#### `reports/` 页（本地分析报告，可选引文）

```yaml
---
pageType: report
id: report.<slug>
title: <标题>
local_path: <path>                   # 本地文件路径
zotero_refs:                         # 可选，引用的 paper
  - key: <itemKey>
    role: methodology
---
```

### Zotero 侧 tags Schema（用结构化字段，不用 Extra）

| Tag 前缀 | 用途 | 示例 |
|---|---|---|
| `wiki:source.<id>` | 反向链到 wiki source 页 | `wiki:source.buzsaki-2002-hippocampal-theta` |
| `wiki:synthesis.<id>` | 反向链到 wiki synthesis 页 | `wiki:synthesis.online-memory-llm-2026` |
| `wiki:report.<id>` | 反向链到 wiki report 页 | `wiki:report.cognitive-load-analysis-2026` |
| `type:review` | 文献类型：综述 | — |
| `type:meta-analysis` | 元分析 | — |
| `type:case-study` | 个案研究 | — |
| `topic:<keyword>` | 主题分类（老板自定义） | `topic:cognitive-load` |

**为什么用 tags 不用 Extra 字段**：
- tags 是**结构化数组**，Zotero 自带索引/检索/过滤
- Extra 字段是文本字段，需要 regex 提取，跨设备同步弱
- tags 支持跨设备/跨平台一致同步（坚果云 WebDAV 同步 Zotero 数据）

## 跳转协议（双向 1-click）

| 方向 | 协议 | 例子 |
|---|---|---|
| wiki → Zotero | `zotero://select/library/items/<itemKey>` | `zotero://select/library/items/ERZMJJTP` |
| Zotero → wiki | `obsidian://open?vault=wiki&file=sources/<file>.md` | `obsidian://open?vault=wiki&file=sources/buzsaki-2002-hippocampal-theta.md` |

- **Obsidian 端**：在 source 页 markdown 中用 `obsidian://` 链接，渲染时自动可点击
- **Zotero 端**：tags 中的 `wiki:source.<id>` 配合 Zotero Better Notes / Markdown Here 等插件可生成跳转链接

## 写入规则

1. **6 个目录的边界不可混淆**——一段 PDF 摘录不能直接写进 syntheses/，必须先在 sources/ 做 source summary
2. **每个 Zotero 条目必须在 wiki 有对应 source 页**（一一对应铁律，强制）
3. **每个 raw source 必须对应一个 sources/ 笔记**——一对一定向引用
4. **concept/ 与 entities/ 不可混用**——"自传体记忆"是 concept，"Diehl Kristin" 是 entity
5. **reports/ 必须是客观的**——不写主观论断，只写可验证事实或自动生成结果
6. **syntheses/ 不可没有 source-backed**——每个论断必须指向至少一个 sources/ 笔记（同时也是 Zotero 条目）
7. **Zotero 端用 tags 字段做反向链，不用 Extra 字段**（结构化优势）
8. **联动字段必填规则**：
   - `sources/` 页：**必填** `zotero_item_key`（单一 item）
   - `syntheses/` 页：**必填** `zotero_refs`（数组，至少 1 个）
   - `concepts/` 页：**可选** `zotero_refs`（仅当涉及论文时填）
   - `reports/` 页：**可选** `zotero_refs`（仅当引用论文时填）

## 文件命名约定

> 命名约定保证 wiki 页面可被自然排序、按时间检索、与 plugin 自动索引兼容。

### `syntheses/` 目录

**格式**：`YYYY-MM-DD-HH-MM-SS-<标题>.md`

| 字段 | 说明 |
|------|------|
| `YYYY-MM-DD-HH-MM-SS` | 17 字符紧凑时间戳（ISO 8601 无分隔符），精确到秒 |
| `-` | 分隔符（时间与标题之间用单连字符） |
| `<标题>` | 中文/英文/混合均可，建议用关键词而非完整句子（例：`照片视角-记忆视角漂移-Diehl-2026`，不用"关于照片视角对记忆漂移影响的研究"） |
| `.md` | Markdown 扩展名 |

**示例**：
- `2026-05-17-18-40-33-如何设计agent-memory.md`
- `2026-05-31-12-22-00-认知过程的对称性破缺机制-理论框架.md`
- `2026-06-05-XX-XX-XX-照片视角-记忆视角漂移-Diehl-2026.md`（待创建）

**为什么用时间戳不用日期？**
- 同一日可能产出多篇总结（如多 Agent 协作），时间戳保证全局唯一
- 紧凑格式（17 字符）可按字典序自动按时间排序
- plugin 自动索引 `index.md` 中的"Generated"节可直接使用

### 其他目录的命名（参考）

| 目录 | 命名格式 | 示例 |
|------|----------|------|
| `raw/papers/` | `YYYY-MM-DD_<作者>_关键词_期刊.pdf` | `2026-06-05_Diehl-et-al_Captured-Memories_JARMAC.pdf` |
| `raw/articles/` | `YYYY-MM-DD_<作者/机构>_关键词.<ext>` | `2026-06-05_Wired_数字记忆重塑.md` |
| `sources/` | 模板 `_template_source_summary.md` + 自由命名 | `2026-06-05_Diehl-et-al_Captured-Memories.md` |
| `concepts/` `entities/` `reports/` | 自由命名（小写中划线连接） | `agent-personal-config-architecture.md` `wangyaxin.md` `lint.md` |

### Zotero 条目命名

- **Title**：保留期刊原文标题（**不要翻译**），便于检索
- **Short Title**：可填便于识别的中文短标题
- **Call Number**：建议填 `wiki:source.<id>`，便于本地/坚果云检索时识别归属

### WebDAV (坚果云) 命名

- 由 Zotero 自动管理，**禁止**手动修改 `nutstore:quanquanzi/zotero/storage/` 内的文件
- 文件名 = Zotero item key + 原始扩展名（如 `VNPN6FHT.pdf`）
- 同步路径：`rclone sync nutstore:quanquanzi/zotero/storage /root/Zotero/storage`