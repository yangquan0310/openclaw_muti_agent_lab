# Memory Wiki Agent Guide (全局共享)

- **本 wiki 为所有代理共享，任何代理均可读写。**
- Treat generated blocks as plugin-owned.
- Preserve human notes outside managed markers.
- Prefer source-backed claims over wiki-to-wiki citation loops.
- Prefer structured `claims` with evidence over burying key beliefs only in prose.
- Use `.openclaw-wiki/cache/agent-digest.json` and `claims.jsonl` for machine reads; markdown pages are the human view.

## 6 个核心目录的用途约定

> 每个目录有明确的角色定位，代理写入时必须匹配。

| 目录 | 用途 | 处理深度 | 写入规则 |
|------|------|----------|----------|
| **`raw/`** | 证据层，存放原始文件（PDF/OCR/笔记/资产） | **零处理**——只归档 | 文件原样存放，不做内容修改 |
| **`sources/`** | 存放**来源摘要**（每个 raw source 对应一个 source summary） | **轻提炼**——一句话总结 + 关键内容 + 影响页面 + 待确认 | 详见 `sources/_template_source_summary.md` 模板 |
| **`syntheses/`** | 存放**总结**（综合分析、综述、论据链） | **重提炼**——多源综合 + 论证 + 结论 | 必须 source-backed（每个论断有 raw 引用）|
| **`concept/`** | 存放**概念**文件（抽象概念的定义与关系） | **抽象归纳**——从具体 source 抽出通用概念 | 概念是跨多篇 source 的归纳 |
| **`entities/`** | 存放**实体**（人物/机构/项目/工具等具象对象） | **抽象归纳**——把具象对象结构化 | 实体是具体的、可指向的对象 |
| **`reports/`** | 存放**客观报告**（lint/contradictions/open-questions 等） | **可重复生成**——机器或人工客观产出 | 内容必须是可验证的、不是主观论断 |

## 6 个目录的依赖与流向

```
原始资料 (raw/)
   ↓ 提炼
来源摘要 (sources/)   ← 每个 raw source 必配一个
   ↓ 引用
总结 (syntheses/)
   ↓ 抽象
概念 (concept/)  +  实体 (entities/)

客观报告 (reports/)   ← 独立于上述链，但可引用任何层
```

- **`raw/` 是唯一的事实来源**——任何总结/概念/实体都必须可回溯到一个 raw 资料
- **`sources/` 是 raw 的索引**——是 raw 到 syntheses 的桥梁
- **`syntheses/` 是论证层**——综合多 source 形成论据链
- **`concept/` 与 `entities/` 是抽象层**——前者抽象概念，后者具体对象
- **`reports/` 是横切层**——可以基于任何层产出客观报告（lint/统计/问题清单）

## 写入规则

1. **6 个目录的边界不可混淆**——一段 PDF 摘录不能直接写进 syntheses/，必须先在 sources/ 做 source summary
2. **每个 raw source 必须对应一个 sources/ 笔记**——一对一定向引用
3. **concept/ 与 entities/ 不可混用**——"自传体记忆"是 concept，"Diehl Kristin" 是 entity
4. **reports/ 必须是客观的**——不写主观论断，只写可验证事实或自动生成结果
5. **syntheses/ 不可没有 source-backed**——每个论断必须指向至少一个 sources/ 笔记

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

