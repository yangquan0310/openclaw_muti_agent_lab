# reviewer 审稿技能

> 统一的学术文稿审稿技能，适用于期刊论文、学位论文、开源论文、课程论文、项目申请书等各类学术写作。

---

## 快速开始

当用户要求审稿时，直接调用本技能：

```
用户：帮我审阅这篇论文
→ 加载 reviewer 技能
→ 根据论文类型选择对应指南
→ 按八大维度审查
→ 输出带优先级的审稿意见
```

---

## 支持的论文类型

| 类型 | 说明 | 触发关键词 |
|------|------|-----------|
| 学位论文 | 硕士/博士论文、学年论文 | "学位论文"、"毕业论文" |
| 期刊论文 | SCI/SSCI/CSSCI等 | "期刊论文"、"投稿"、"审稿" |
| 开源论文 | arXiv/预印本 | "arXiv"、"预印本" |
| 课程论文 | 学期论文、课程报告 | "课程论文"、"学期报告" |
| 项目申请书 | 国自然/省部级课题 | "申请书"、"课题申报" |

---

## 目录结构

```
reviewer/
├── SKILL.md                    # 技能入口
├── README.md                   # 本文件
├── _meta.json                  # 元数据
├── scripts/
│   └── review_checklist.py    # 审稿清单脚本
├── references/
│   ├── index.md               # 索引
│   ├── guide.md               # 使用指南
│   ├── thesis-review-guide.md # 学位论文审稿
│   ├── journal-review-guide.md # 期刊论文审稿
│   ├── opensource-review-guide.md
│   ├── course-paper-review-guide.md
│   └── proposal-review-guide.md
└── assets/
    └── templates/             # 模板文件
```

---

## 核心原则

1. **建设性优先**：每条意见附带改进建议
2. **尊重原创**：只改错误不改风格
3. **提升质量**：帮助论文达到更高标准
4. **协作导向**：扮演质量改进伙伴

---

## 与 thesis-reviewer 的关系

- `reviewer` 是统一的审稿入口
- `thesis-reviewer` 暂时保留，作为过渡
- 未来所有审稿需求统一由 `reviewer` 处理

---

*最后更新：2026-05-20*
