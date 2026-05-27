# reviewer 技能索引

> 本技能是审稿助手的核心技能，统一处理各类学术文稿的审稿需求。

---

## 指南总览

| 指南 | 适用范围 | 优先级 |
|------|----------|--------|
| [guide.md](guide.md) | 通用审稿流程和方法论 | 必读 |
| [citation-hallucination-guide.md](citation-hallucination-guide.md) | AI幻觉文献识别与审查 | 高 |
| [thesis-review-guide.md](thesis-review-guide.md) | 学位论文（硕博论文、学年论文） | 高 |
| [journal-review-guide.md](journal-review-guide.md) | 期刊论文（SCI/SSCI/CSSCI/中文核心） | 高 |
| [opensource-review-guide.md](opensource-review-guide.md) | 开源论文（arXiv/预印本/技术报告） | 中 |
| [course-paper-review-guide.md](course-paper-review-guide.md) | 课程论文（学期论文、课程报告） | 中 |
| [proposal-review-guide.md](proposal-review-guide.md) | 项目申请书（国自然/省部级课题） | 中 |

---

## 快速选择指南

```
审稿任务
├── 通用方法 → guide.md
├── AI幻觉文献审查 → citation-hallucination-guide.md
├── 学位论文（硕士/博士论文）→ thesis-review-guide.md
├── 期刊论文（投稿审稿）→ journal-review-guide.md
├── 开源/预印本论文 → opensource-review-guide.md
├── 课程论文（学期报告）→ course-paper-review-guide.md
└── 项目申请书 → proposal-review-guide.md
```

---

## 核心原则

1. **建设性优先**：每条意见附带改进建议
2. **尊重原创**：只改错误不改风格
3. **严谨但不苛刻**：区分科学问题和细节完善
4. **协作导向**：扮演质量改进伙伴角色

---

## 配套资源

- **审稿清单脚本**：`scripts/review_checklist.py` — 结构化检查辅助
- **输出模板**：见 SKILL.md 输出格式章节
- **优先级标注**：🔴 critical → 🟡 major → 🟢 minor → 🔵 suggestion
