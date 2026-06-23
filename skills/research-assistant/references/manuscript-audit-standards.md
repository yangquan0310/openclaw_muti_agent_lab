# Manuscript Audit Checklist（v5.21.0 新增）

> 来源：吸收 PaperSpine（WUBING2023/PaperSpine）paper-spine-audit + 综合 ARS / Nature-skills 思路  
> 用途：**投稿前 / 终稿前**的**最终审计**，覆盖完整性 / rationale 深度 / 引用库 / 翻译覆盖 / artifact 健康  
> 触发：synthesize 输出完成 + originality check 通过后

---

## 🎯 5 大审计维度

| # | 维度 | 检查什么 | 来源 |
|---|------|---------|------|
| 1 | **完整性** | 章节齐 + 数据齐 + 图表齐 | PaperSpine audit |
| 2 | **rationale 深度** | 论证链是否严密 + overclaim | PaperSpine audit |
| 3 | **引用库质量** | 数量 + 时效 + 平衡 + DOI | PaperSpine citation |
| 4 | **翻译覆盖** | 中英对照 + 术语统一 | PaperSpine translate |
| 5 | **artifact 健康** | 文件齐全 + 命名规范 + 可复现 | PaperSpine audit |

---

## 📋 60 项 Checklist

### A. 完整性（15 项）

#### 章节结构（5 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 1 | Abstract / 摘要 ≤ 250 字 | |
| 2 | Introduction 含 3 段：背景 / 缺口 / 目的 | |
| 3 | Methods 含 PICO / 数据源 / 分析方法 | |
| 4 | Results 按 sub-question 顺序呈现 | |
| 5 | Discussion 含 主要发现 / 与既有理论对话 / 局限 / 未来 | |

#### 数据 + 图表（5 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 6 | 每个 claim 有数据支撑（图/表/统计）| |
| 7 | 图表都有 caption + 编号 | |
| 8 | 图表在正文被引用（"Figure 1 shows..."）| |
| 9 | 数据可复现（数据/代码已上传 Zenodo/GitHub）| |
| 10 | Data Availability Statement 在文末 | |

#### 必备小节（5 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 11 | Acknowledgments（含基金 + 协助者）| |
| 12 | Author Contributions（CRediT taxonomy）| |
| 13 | Conflict of Interest | |
| 14 | Ethics / IRB（如涉及人体/动物）| |
| 15 | Funding | |

### B. Rationale 深度（12 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 16 | 每段有明确 purpose（hook / evidence / synthesis / bridge）| |
| 17 | 没有 "相关≠因果" 的 overclaim | |
| 18 | 没有 "显著≠重要" 的混淆 | |
| 19 | effect size + CI 都有（不只是 p-value）| |
| 20 | 异质性有解释（不是只报 I²）| |
| 21 | 局限性诚实讨论（不止"样本小"）| |
| 22 | future direction 具体（不是"未来可研究"）| |
| 23 | 与既有理论显式对话（不只是描述）| |
| 24 | 反驳性证据有讨论（不只是选择性引用）| |
| 25 | alternative explanation 有考虑 | |
| 26 | 没有遗漏关键反对意见 | |
| 27 | abstract 数字与正文一致 | |

### C. 引用库质量（15 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 28 | 引用数量合理（综述 ≥ 50，原研 ≥ 25）| |
| 29 | 引用近 3-5 年 ≥ 30% | |
| 30 | 引用经典文献（领域开山 / 高被引）| |
| 31 | 没有"全部是英文"或"全部是中文" | |
| 32 | 关键观点有 ≥ 2 个独立来源支撑 | |
| 33 | 引用平衡（不只支持自己观点的）| |
| 34 | 引用 DOI 100%（无 DOI 用 URL）| |
| 35 | 引用格式 APA 7 / 期刊要求（参见 apa7-standards.md）| |
| 36 | in-text 与 reference list 一一对应 | |
| 37 | 没有 "et al." 在 reference list | |
| 38 | 自引 < 10%（除非领域惯例）| |
| 39 | 引用预印本明确标 "preprint" | |
| 40 | 数据集 / 软件引用按 APA 7 格式 | |
| 41 | 自我引用 cross-reference 到自己已发表论文（如有）| |
| 42 | 引用非英语文献有英文翻译标题 | |

### D. 翻译覆盖（8 项）

> 仅当产出有双语（中英对照 / 翻译）需求时跑

| # | 检查项 | ✓ |
|---|--------|---|
| 43 | 关键术语首次出现给中英对照 | |
| 44 | 缩写首次给全称 + 缩写 | |
| 45 | 翻译标题 / 摘要专业 | |
| 46 | 没有机翻痕迹（如 "进行了一个研究" → "conducted a study"）| |
| 47 | 翻译论文段不是直译（paraphrased）| |
| 48 | 翻译后引用格式与原文一致 | |
| 49 | 中英数字 / 标点规范统一 | |
| 50 | 翻译流程文档化（见 PaperSpine translate）| |

### E. Artifact 健康（10 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 51 | 主文档（.md / .docx / .tex）齐全 | |
| 52 | 引用文件（references.bib）齐全 | |
| 53 | 图表文件（PNG/PDF/SVG）齐全 | |
| 54 | 数据文件（CSV/JSON）齐全 + 命名规范 | |
| 55 | 代码（如有）有 README + 依赖说明 | |
| 56 | 命名规范（snake_case 或 kebab-case，无中文）| |
| 57 | 文件大小合理（< 50MB 单元）| |
| 58 | Git history 整洁（commit 信息规范）| |
| 59 | 没有遗留 TODO / FIXME / XXX | |
| 60 | 终稿前跑过 `quarto render` 验证编译 | |

---

## 🔧 自动化辅助

### Quarto 编译前引用核验（v5.21.2 已删除 hooks/，按本文 60 项手动核验）

`scripts/hooks/quarto_cite_audit.py` 已随 hooks/ 整目录删除（v5.21.2 老板 14:29 明确不需要）。APA 7 引用核验直接走本清单 + `apa7-standards.md` 50 项交叉核验，Quarto 编译前手工跑 `quarto render manuscript.qmd` 看 warning/error。

### 最终审计报告输出

```bash
# 未来加个命令：
research-assistant audit --input manuscript.md \
                          --checklist references/manuscript-audit-standards.md \
                          --output audit-report.md
```

---

## 🛠️ 集成到 research-assistant

### 工作流（终稿前最后一步）

```
synthesize 输出
        ↓

        ↓
references/originality-standards.md（30 项原创性）
        ↓
references/apa7-standards.md（50 项 APA）
        ↓
references/manuscript-audit-standards.md（60 项最终审计）← 本文
        ↓
所有 P0 = 0，P1 ≥ 80% 已修 → 投稿
```

### Score 汇总

| 阶段 | 通过线 |
|------|--------|

| Originality | 30/30 全过 |
| APA 7 | P0 = 0 + P1 ≥ 90% |
| Manuscript Audit | P0 = 0 + P1 ≥ 80% + P2 ≥ 60% |

**P0 = 必改** / **P1 = 应改** / **P2 = 建议改**

---

## ⚠️ 边界条件

| 不要做 | 原因 |
|--------|------|
| ❌ 不要跳过 P0 直接投 | P0 是期刊硬性要求 |
| ❌ 不要把 checklist 当成 LLM 单次提问 | 必须**结构化**每项独立核验 |
| ❌ 不要把审计输出当终稿 | 审计是诊断，不是修改 |

---

## 📚 参考

- PaperSpine paper-spine-audit：https://github.com/WUBING2023/PaperSpine
- ARS Academic Pipeline integrity verification
- Nature-skills 多 skill 整合
- COPE / ICMJE 投稿前 checklist

---

*最后更新：2026-06-22 v5.21.0*  
*来源借鉴：PaperSpine paper-spine-audit + ARS + Nature-skills*