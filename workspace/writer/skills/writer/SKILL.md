---
name: writer
description: >
  writer的实践技能。
  当需要进行写作、撰写、起草、编辑、修改、润色论文、文章、报告、文档、方案、说明等写作任务时激活。
  通用写作技能，覆盖一切写作任务。
version: 2.0.0
author: Yang Quan
metadata:
  openclaw:
    emoji: ✍️
    requires: []
---

# writer（通用写作技能）

> **通用写作技能**：不绑定任何领域，适用于一切写作任务。
> **核心结构**：指南下沉至 references/，模板存放于 assets/templates/，快速检索用 lookup search --skill writer

---

## 触发条件

| 场景 | 触发关键词 |
|------|------------|
| 写作任务 | 写、写作、撰写、起草、编辑、修改、润色 |
| 论文文章 | 论文、文章、报告、文档、方案、说明 |
| 学术写作 | 摘要、综述、大纲、致谢 |
| 翻译写作 | 中译英、英译中、翻译 |

---

## 核心原则

1. **证据优先**：所有主张必须有文献支持，禁止捏造数据
2. **结构驱动**：先搭框架再填内容，结构 > 内容
3. **精准表达**：学术写作要求精确、简洁、客观
4. **检索验证**：遇到陌生主题必须检索，不许凭空编造

---

## 边界条件（禁止事项）

| 边界 | 说明 |
|------|------|
| 禁止捏造 | 禁止捏造文献作者、年份、期刊、数据 |
| 禁止臆测 | 禁止"应该是"、"大概如此"等模糊表述 |
| 禁止删除原意 | 修改时不得大幅删改用户原有段落结构和核心论点 |
| 禁止破坏结构 | 禁止删除主题句或破坏论证链完整性 |
| 禁止自我决策 | 执行修改前必须先汇报修改内容并获得确认 |

---

## 核心理念

> **证据 > 推测 > 观点**，**结构 > 内容**，**精准 > 冗余**

| 层级 | 核心 |
|------|------|
| **证据层** | 可验证的实证结果，必有引用 |
| **推测层** | 对证据的解释，归因到研究者 |
| **观点层** | 本研究对证据的解读，弱语气 |

---

## 五阶段工作流

```
阶段1: 理解任务 → 阶段2: 规划 → 阶段3: 起草 → 阶段4: 修改 → 阶段5: 校对
```

每个阶段有明确的输入、输出和必读指南。

---

### 阶段1: 理解任务

**输入**: 写作任务描述
**输出**: 任务分解（主题 / 限制 / 指令词 / 边界）

**必读指南**: `references/workflows/writing-process-workflow.md` 第1节

---

### 阶段2: 规划

**输入**: 任务分解
**输出**: 论证结构（核心论点 + 子论点 + 证据 + 潜在反驳）

**必读指南**: 
- `references/workflows/writing-process-workflow.md` 第2节
- `references/guides/writing-principles-guide.md`

---

### 阶段3: 起草

**输入**: 论证结构
**输出**: 初稿

**必读指南**:
- `references/standards/sentence-standards.md` — 每句主语明确、动词精确
- `references/standards/paragraph-standards.md` — 主题句统领、论证链清晰
- `references/standards/chapter-standards.md` — 引言-主体-结论闭环
- `references/guides/academic-style-guide.md` — 清晰/简洁/客观/中立

---

### 阶段4: 修改

**输入**: 初稿
**输出**: 修改清单 → 逐章执行 → 终稿

**必读指南**:
- `references/workflows/modification-workflow.md` — 修改方法论（建立论证地图→修改清单→汇报确认→执行→核查）
- `references/guides/evidence-layers-guide.md` — 证据-推测-解读三层区分
- `references/standards/style-standards.md` — 术语管理、禁用词表
- `references/standards/citation-standards.md` — 引用格式规范
- `references/guides/editing-proofreading-guide.md` — 句子/段落/语言润色检查

**修改优先级**:
| 优先级 | 类型 |
|--------|------|
| P0 | 术语清洗 |
| P1 | 引用修复 |
| P2 | 图表编号 |
| P3 | 逻辑深度 · 段落结构 |
| P4 | 终极核查 |

---

### 阶段5: 校对

**输入**: 终稿
**输出**: 提交稿

**必读指南**:
- `references/guides/editing-proofreading-guide.md` 第9节 — 格式/引用/数字校对
- `references/standards/citation-standards.md` — 确保每条引用有对应参考文献
- `references/guides/ai-writing-guide.md` — 消除AI写作模式

---

## 场景化快速调用

| 场景 | 必读指南 | 禁止行为 |
|------|----------|----------|
| 撰写学术论文 | `guides/academic-style-guide.md` + `standards/citation-standards.md` | 捏造文献数据 |
| 修改润色文章 | `workflows/modification-workflow.md` + `guides/editing-proofreading-guide.md` | 大幅删改原意 |
| 检查写作质量 | `guides/evidence-layers-guide.md` + `standards/sentence-standards.md` | 只看表面错误 |
| 消除AI痕迹 | `guides/ai-writing-guide.md` | 直接删除整段 |
| 中英文论文差异 | `guides/chinese-english-writing-guide.md` | 混用中英文格式 |
| 跨语言翻译写作 | `guides/chinese-english-writing-guide.md` + `standards/citation-standards.md` | 直译不调整结构 |

---

## 检索使用规范（强制）

遇到以下场景**必须**使用检索工具，不许凭空编造：

| 场景 | 工具 | 示例 |
|------|------|------|
| 引用文献数据 | `exa_search` | "Author 2020 memory recall statistics" |
| 核实事实性陈述 | `tavily_search` | "cognitive offloading effects on memory" |
| 补充背景知识 | `exa_search` | "distributed cognition theory Hutchins 1995" |
| 验证学术术语 | `tavily_search` | "autobiographical memory definition" |
| 补充文献 | `exa_search` | "photo-taking impairment effect meta-analysis" |

**禁止**：
- ❌ 捏造文献作者、年份、期刊
- ❌ 凭空想象实验数据
- ❌ 未经证实的主观推测
- ❌ "应该是"、"大概如此"等模糊表述

---

## scripts 使用

```bash
# 自检脚本：检查证据语气/填充词/禁用隐喻/人称观点
python3 scripts/selfcheck.py --file <path> --level <sentence|paragraph|chapter>

# 快速检索
lookup search --skill writer <关键词>       # 搜索指南
lookup list --skill writer          # 列出所有指南
lookup index --skill writer                  # 重建索引
```

---

## references 完整索引

### references/（使用指南）

| 文件 | 内容 |
|------|------|
| `guide.md` | 使用指南 |
| `index.md` | 书籍式索引 |

### references/workflows/（工作流）

| 文件 | 内容 |
|------|------|
| `writing-process-workflow.md` | 五阶段写作流程（理解→规划→起草→修改→校对） |
| `modification-workflow.md` | 修改方法论（论证地图→修改清单→执行→核查） |

### references/standards/（规范标准）

| 文件 | 内容 |
|------|------|
| `sentence-standards.md` | 句子规范（主语/动词/定义/"我们"边界） |
| `paragraph-standards.md` | 段落规范（主题句/论证链/过渡/字数） |
| `chapter-standards.md` | 篇章规范（闭环/子论点编排/过渡句） |
| `style-standards.md` | 术语管理/禁用词表/"我们"使用规则 |
| `citation-standards.md` | 引用类型/APA格式/常见错误 |

### references/guides/（方法论指南）

| 文件 | 内容 |
|------|------|
| `writing-principles-guide.md` | 写作原则（立论/证据/结构） |
| `academic-style-guide.md` | 学术写作风格（清晰/简洁/客观/中立） |
| `evidence-layers-guide.md` | 证据-推测-解读三层区分 |
| `editing-proofreading-guide.md` | 修改层次/句子润色/校对清单 |
| `ai-writing-guide.md` | AI写作模式检测与消除 |
| `chinese-english-writing-guide.md` | 中英文论文差异与翻译写作规范 |

---

## 模板导航

| 模板 | 位置 | 说明 |
|------|------|------|
| 学术论文模板 | `assets/templates/academic-paper.md` | 论文标准结构模板 |
| 章节模板 | `assets/templates/chapter.md` | 各章节写作模板 |
| 摘要模板 | `assets/templates/abstract.md` | 摘要标准格式 |

> 注意：模板目录正在建设中，部分模板待补充。

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 2.1.0 | 2026-05-23 | references目录重组：分为standards/workflows/guides三个子目录，SKILL.md路径同步更新 |
| 2.0.0 | 2026-05-23 | 按代理技能体系重构：新增模板导航章节、修复核心原则重复、明确目录结构 |
| 1.4.0 | 2026-05-20 | 同步skill-developer模板：新增触发条件表格、核心原则、边界条件 |
| 1.3.0 | 2026-05-20 | 彻底重构SKILL.md：新增五阶段工作流、场景化快速调用、完整references索引 |
| 1.2.0 | 2026-05-20 | 完善模块导航（15个references全收录），新增检索规范 |
| 1.1.0 | 2026-05-20 | 新增检索指引 + AI写作去痕 + 中英文差异指南 |
| 1.0.0 | 2026-05-20 | 初始版本，整合 thesis-writer 为通用写作技能 |

---

*维护者：杨权*
