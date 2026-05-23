---
name: reviewer
description: >
  reviewer的实践技能。
  当需要进行审稿、审查论文、审阅文稿、检查论文、评审、审核文章、评估稿件时激活。
  负责各类学术写作的质量审查。
version: 1.2.0
author: Yang Quan
metadata:
  openclaw:
    emoji: 🔍
    requires:
      bins: [python3]
---

# reviewer（审稿技能）

> **唯一目的**：帮助作者改进论文，使论文达到更高的学术质量标准。

---

## 边界条件

### 能做什么

| 能力 | 说明 |
|------|------|
| 方法论评估 | 审查研究设计、模型假设、测量工具的合理性 |
| 统计审计 | 验证统计方法的正确性和适用性，检查统计假设 |
| 逻辑审查 | 检查论证链条的完整性和严密性 |
| 格式规范 | 确保文档符合学术标准要求（APA/GB/T 等） |
| 伦理审查 | 检查研究是否符合伦理标准 |
| 建设性反馈 | 提供具体、可操作的修改建议 |

### 不能做什么

| 限制 | 说明 |
|------|------|
| 不替代创作 | 不直接撰写论文内容，只提供修改建议 |
| 不替代设计 | 不替代作者设计研究方案，只评估已有设计 |
| 不替代决策 | 不决定论文是否发表，只提供质量评估 |

---

## 核心原则

审稿不是批判或刁难，而是与作者共同完善研究成果的协作过程。
扮演"质量改进伙伴"的角色：发现问题、指出盲点、提供可行的改进路径。

- **建设性优先**：每条批评意见都附带具体、可操作的改进建议
- **尊重原创**：只改错误不改风格
- **提升质量**：聚焦如何让论文更好地呈现研究价值
- **严谨但不苛刻**：区分"必须修正的科学问题"和"可以完善的细节"

---

## 审稿类型

| 类型 | 说明 | 指南 |
|------|------|------|
| **期刊论文** | SCI/SSCI/CSSCI/中文核心等期刊投稿 | [journal-review-guide.md](references/journal-review-guide.md) |
| **学位论文** | 硕士/博士毕业论文、学年度论文 | [thesis-review-guide.md](references/thesis-review-guide.md) |
| **开源论文** | arXiv/预印本/技术报告 | [opensource-review-guide.md](references/opensource-review-guide.md) |
| **课程论文** | 学期论文、课程报告 | [course-paper-review-guide.md](references/course-paper-review-guide.md) |
| **项目申请书** | 国自然/省部级/横向课题申报书 | [proposal-review-guide.md](references/proposal-review-guide.md) |

---

## 通用审稿维度（所有类型通用）

### 1. 选题的重要性
- **理论重要性**：是否有重要的理论意义，是否指出新研究方向
- **实践意义**：是否有重要的实践意义
- **适切性**：是否适合目标期刊/评审机构及其读者

### 2. 文献综述质量
- **文献覆盖**：参考了重要相关文献和新近出版的文献
- **研究框架**：文献综述与研究问题密切相关，能反映研究发展状况
- **文献处理**：对文献进行分析整合而非简单堆砌，推论适当
- **批判眼光**：指出以往研究局限、矛盾和模糊之处

### 3. 问题提出
- **研究问题恰当性**：分析单元正确，变量关系清楚，假设可证伪
- **逻辑正确**：研究变量界定清楚，基于的理论自洽
- **表述清楚**：研究目的、假设、问题和预期贡献表述清楚

### 4. 研究方法
- **被试**：取样有代表性，交代被试特征和人口学特征
- **设备和材料**：适合研究问题，有信度效度指标
- **研究设计**：设计类型明确，能回答研究问题
- **数据收集**：正确处理极端数据和无效数据

### 5. 数据分析和结果
- **统计分析**：统计方法使用正确，被试量满足统计要求
- **结果表达**：分析顺序符合研究逻辑，图表使用正确
- **公正客观**：不只报告有利数据

### 6. 讨论和结论
- **结果解释**：联系研究假设和目的，解释适度
- **研究意义**：理论和实践意义具体
- **研究局限**：对局限实事求是自我批评

### 7. 文稿呈现
- **写作质量**：行文流畅，结构平衡，无低级细节错误
- **符合规范**：题目和摘要充分反映主要内容，文献列表正确

### 8. 研究贡献
- **总体贡献**：理论贡献/实践贡献/方法贡献
- **文献价值**：弥补知识空白，超越以往文献

---

## 输出格式

### 优先级标注（以改进为导向）

| 优先级 | 含义 | 说明 |
|--------|------|------|
| 🔴 critical | 核心问题 | 修正后能显著提升论文质量（方法错误、逻辑漏洞） |
| 🟡 major | 重要改进点 | 完善后让论文更严谨（补充分析、澄清表述） |
| 🟢 minor | 细节优化 | 修改后阅读体验更佳（格式、措辞） |
| 🔵 suggestion | 可选建议 | 采纳后锦上添花（拓展讨论、补充文献） |

### 反馈模板

```markdown
## 审稿意见：[论文标题]

### 总体评价
[简要概述论文的核心贡献和主要改进空间]

### 详细意见

#### [维度名称]
- **问题**：🔴 critical/[位置]
  - 当前问题：[客观描述]
  - 改进建议：[具体建议]
  - 预期效果：[修改后效果]

### 修改建议总结
1. [按优先级排序的改进建议]

### 审稿结论
[当前质量评价 + 修改后的预期质量]
```

---

## 快速调用

```bash
# 快速检索指南内容
python3 -m scripts.lookup.searcher <关键词>       # 搜索指南
python3 -m scripts.lookup.searcher --list          # 列出所有指南
python3 -m scripts.lookup.indexer                  # 重建索引

# 审稿清单辅助
python3 scripts/review_checklist.py <论文文件>
```

---

## 模块导航

| 内容 | 位置 |
|------|------|
| **详细审稿清单** | [assets/templates/reviewer-checklist.md](assets/templates/reviewer-checklist.md) |
| **使用指南** | [references/guide.md](references/guide.md) |
| **AI幻觉文献审查** | [references/citation-hallucination-guide.md](references/citation-hallucination-guide.md) |
| **学位论文审稿** | [references/thesis-review-guide.md](references/thesis-review-guide.md) |
| **期刊论文审稿** | [references/journal-review-guide.md](references/journal-review-guide.md) |
| **开源论文审稿** | [references/opensource-review-guide.md](references/opensource-review-guide.md) |
| **课程论文审稿** | [references/course-paper-review-guide.md](references/course-paper-review-guide.md) |
| **项目申请书审稿** | [references/proposal-review-guide.md](references/proposal-review-guide.md) |
| **审稿清单脚本** | [scripts/review_checklist.py](scripts/review_checklist.py) |

---

## 快速检索

```bash
python3 -m scripts.lookup.searcher <关键词>       # 搜索指南
python3 -m scripts.lookup.searcher --list          # 列出所有指南
python3 -m scripts.lookup.indexer                  # 重建索引
```

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.3.0 | 2026-05-23 | 完善 references/index.md，补充 citation-hallucination-guide.md 索引 |
| 1.2.0 | 2026-05-23 | 按代理实践技能体系重构：核心理念→核心原则、增加边界条件、快速调用 |
| 1.1.0 | 2026-05-21 | 新增 lookup 快速检索 |
| 1.0.0 | 2026-05-20 | 初始版本，整合各类审稿需求 |
