---
pageType: source
id: source.template-source-summary
createdAt: "2026-06-05T15:19:00+08:00"
updatedAt: "2026-06-05T15:21:00+08:00"
title: Source Summary 模板
sourceIds:
  - raw/README.md
aliases:
  - 资料源笔记模板
---

# Source Summary 模板

> **source summary 不是原文复述**——是一句话总结 + 关键内容 + 影响到的页面 + 待确认。

## 使用方法

1. 原始资料归档到 `raw/<category>/<file>`
2. 在 `sources/` 下创建本模板的副本，命名为对应文件（建议同名，扩展名 `.md`）
3. 填写以下 4 个字段
4. **必填** wikilink 回到 `raw/<category>/<file>`

## 字段说明

| 字段 | 含义 | 长度建议 |
|------|------|----------|
| **一句话总结** | 核心论断 | 1-2 句，30-80 字 |
| **关键内容** | 关键发现/方法/结论的精炼（3-7 条 bullet） | 每条 1 行 |
| **影响到的页面** | 本 source 会作为哪些 wiki 页面（syntheses/concepts/entities）的证据来源 | 0-N 个 wikilink |
| **待确认** | 引用前需要老板拍板的事项（事实疑点 / 引用位置 / 解读分歧） | 0-N 条 |

## 模板（复制后填写）

````markdown
---
pageType: source
id: source.<unique-id>
createdAt: "YYYY-MM-DDTHH:MM:SS+08:00"
updatedAt: "YYYY-MM-DDTHH:MM:SS+08:00"
title: <一句话总结>
sourceIds:
  - raw/<category>/<file>
aliases:
  - <关键词>
---

# <一句话总结>

> **来源**：`raw/<category>/<file>`
> **作者**：
> **年份**：
> **类型**：article | paper | book | note | asset
> **状态**：draft（待老板确认）| confirmed（已确认）

## 一句话总结

（1-2 句核心论断）

## 关键内容

- （关键发现 / 方法 / 结论 1）
- （关键发现 / 方法 / 结论 2）
- （关键发现 / 方法 / 结论 3）
- …

## 影响到的页面

- `synth:<对应综述页>`（如适用）
- `concept:<对应概念页>`（如适用）
- `entity:<对应实体页>`（如适用）

> 注：以上 wikilink 前缀为占位语法，复制后请改为实际 wikilink。

## 待确认

- [ ] （事实疑点 / 引用位置 / 解读分歧）
- [ ] …
````

## 撰写原则（老板定的核心规则）

| 原则 | 含义 |
|------|------|
| **❌ 不是原文复述** | 不要把摘要 / abstract 复制过来；要做主观提炼 |
| **✅ 是一句话总结** | 1-2 句最浓缩的论断（"我看完这篇最重要的 takeaway"）|
| **✅ 关键内容是有取舍的** | 3-7 条 bullet，不是穷举；老板说"重要的"才算 |
| **✅ 影响到的页面要有"反推"** | 读完这篇，我会去改 / 新建哪个 wiki 页？|
| **✅ 待确认要"暴露脆弱性"** | 不确定的事实、解读分歧、引用位置犹豫——都列出来 |

## 与 vault 其他层的关系

```
raw/<category>/<file>           ← 原始资料（零处理）
       ↑ 提炼
sources/<name>.md（本模板）    ← source summary（轻提炼）
       ↑ 引用
syntheses/<date>-<title>.md     ← 综述（重提炼）
       ↑ 抽象
concepts/<name>.md              ← 概念页
entities/<name>.md              ← 实体页
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v1.0 | 2026-06-05 | 初建模板（杨权 15:19 指令） |
| v1.1 | 2026-06-05 | 补 frontmatter（id/pageType/createdAt/updatedAt），wikilink 占位符改为代码块以通过 lint |

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
