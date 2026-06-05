---
type: raw
status: scaffold
created: 2026-06-05
owner: 杨权
---

# raw — 原始资料归档

> 本目录存放**未经提炼的原始资料**，是 wiki 的"证据层（evidence layer）"。
> **每个 raw source 必须对应一个 source summary**（见 [[sources/_template_source_summary]]）。

## 子目录结构

```
raw/
├── articles/   短篇文章（博客、新闻、评论、专栏等）
├── papers/     学术论文（PDF + 补充材料）
├── books/      书籍（章节 / 整本扫描 / 摘录）
├── notes/      原始笔记（手写扫描、便签、研究日志等）
└── assets/     配套资产（图片、数据集、代码、附件等）
```

## 命名约定（建议）

| 类型 | 格式 | 示例 |
|------|------|------|
| 论文 | `YYYY-MM-DD_作者_关键词_期刊.pdf` | `2026-06-05_Diehl-et-al_Captured-Memories_JARMAC.pdf` |
| 文章 | `YYYY-MM-DD_作者/机构_关键词.md` 或 `.pdf` | `2026-06-05_某人_自传体记忆观察.md` |
| 书籍 | `YYYY-MM-DD_作者_书名.pdf` | `2026-06-05_Tulving_记忆.epsitem.pdf` |
| 笔记 | `YYYY-MM-DD_主题.md` 或 `.jpg` | `2026-06-05_团辅方案设计手稿.md` |
| 资产 | `YYYY-MM-DD_说明.扩展名` | `2026-06-05_研究数据_v1.csv` |

> **注**：命名仅建议，老板的特定场景可自由。

## raw source → source summary 的工作流

```
1. 原始资料落入 raw/<category>/
2. 在 sources/ 下创建同名 .md 笔记
3. 笔记结构见 [[sources/_template_source_summary]]
   (一句话总结 / 关键内容 / 影响到的页面 / 待确认)
4. 笔记通过 [[wikilink]] 反向引用 raw/ 文件
```

## 与其他目录的边界

| 目录 | 内容 | 处理深度 |
|------|------|----------|
| **`raw/`**（本目录） | 原始资料归档 | **零处理**——只归档 |
| `_attachments/` | Obsidian 附件缓存 | 渲染时引用 |
| `sources/` | **source summary**（提炼过的资料源笔记） | **轻提炼**（一句话 + 关键 + 链接） |
| `syntheses/` | 综述 / 综合分析笔记 | **重提炼**（论据链 + 结论） |
| `concepts/` / `entities/` | 概念 / 实体页 | 抽象归纳 |

> 依据：vault 架构原则 "Raw sources remain the evidence layer; Wiki pages are the human-readable synthesis layer."

## 待定项（请老板拍板）

| # | 决策 | 候选 | 我的默认建议 | 状态 |
|---|------|------|------------|------|
| ~~1~~ | ~~子目录分类~~ | ~~raw/pdf/、raw/ocr/...~~ | ~~(A)~~ | ✅ **已定**（5 个语义子目录）|
| 2 | **文件命名** | (A) `YYYY-MM-DD_作者_关键词.ext`<br>(B) DOI 为主键<br>(C) 自由命名 | (A) | 待老板确认 |
| 3 | **是否在 Zotero 建同步** | (A) 是（Zotero 作元数据源，raw/ 作文件归档）<br>(B) 否（双轨独立） | (A) | 待老板确认 |
| 4 | **与 `temp/` 目录的关系** | (A) raw/ 长期归档，temp/ 短期 → 到时迁移<br>(B) raw/ 替代 temp/ 角色<br>(C) 保持现状 | (A) | ✅ **已验证**（15:42 迁移 Hutmacher & Schramm 2026） |
| 5 | **首份归档资料** | Diehl et al. (2026). *Captured memories*. JARMAC 15(1), 98–107. → `raw/papers/2026-06-05_Diehl-et-al_Captured-Memories_JARMAC.pdf` | ✅ **已归档**（15:25） |

## 索引（自动维护）

<!-- openclaw:wiki:raw:index:start -->
<!-- openclaw:wiki:raw:index:end -->

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| v0.1 | 2026-06-05 | 脚手架初建（杨权 15:13 指令） |
| v0.2 | 2026-06-05 | 重命名 `Raw/` → `raw/`（杨权 15:16 指令） |
| v0.3 | 2026-06-05 | 5 个语义子目录 + source summary 工作流（杨权 15:19 指令）|
| v0.4 | 2026-06-05 | 首份归档：Diehl et al. 2026 PDF 移入 `raw/papers/`（杨权 15:24 指令）|
| v0.5 | 2026-06-05 | 迁移 Hutmacher & Schramm 2026 PDF（temp/ → raw/papers/），验证 temp/raw 分工（杨权 15:42 trigger D.1）|
