# Originality Checklist（v5.21.0 新增）

> 来源：吸收 ARS Academic Paper **anti-leakage protocol** + Style Calibration 反抄袭思路  
> 用途：synthesize 输出后 / 投稿前**强制跑 originality 核验**，避免抄袭 / 自我抄袭 / 翻译抄袭 / LLM 痕迹  
> 工具：人工 + Turnitin / iThenticate（用户自己跑）+ 本 checklist 启发式

---

## 🎯 抄袭 5 大类型（必须分别核验）

| # | 类型 | 表现 | 检测 |
|---|------|------|------|
| 1 | **直接抄袭** | 逐字复制（> 4 词连续无引用）| Turnitin / iThenticate |
| 2 | **自我抄袭** | 复用自己已发表内容未注明 | Crossref / Text overlap |
| 3 | **翻译抄袭** | 把英文文献翻译成中文不引用 | 双语比对工具 |
| 4 | **观点未注明** | 用了别人的 idea / 理论 / 模型未引用 | 人工 + reference 对比 |
| 5 | **LLM 痕迹** | AI 写作的句式特征（"值得注意的是"）| AI detector + 人工 |

---

## 📋 30 项 Checklist（按类型分组）

### A. 直接抄袭（8 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 1 | 每段 > 4 词的连续文本都有引用？ | |
| 2 | 直接引用（带引号）有 Author (Year, p. xx)？ | |
| 3 | 没有"忘了改"的占位符（如 [TODO cite]）？ | |
| 4 | paraphrase 不是简单换词（要重组句式 + 加引用）| |
| 5 | 没有把图表 caption 当正文抄（要 paraphrasing）| |
| 6 | 表格 / 图里的数据来源有注明？ | |
| 7 | 没有 "Smith et al. found that..." 后直接抄结论 | |
| 8 | 二手引用有 "as cited in" 标识 | |

### B. 自我抄袭（6 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 9 | 已发表论文的段落未在新文中复用（如有，重写 + 引用）| |
| 10 | 已发表论文的图表未在新文中复用（除非明确许可）| |
| 11 | 已发表论文的 method 未原样搬（要写新 paper 的特定版本）| |
| 12 | 已发表综述未拆成多篇新综述（同主题）| |
| 13 | 学位论文章节未直接转为期刊论文 | |
| 14 | 自己会议论文未直接扩为期刊论文（要重写 30%+）| |

### C. 翻译抄袭（4 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 15 | 翻译的英文段落是否每段都有原文引用？ | |
| 16 | 中英对照翻译（如教科书翻译）是否获得许可？ | |
| 17 | 翻译后是否做了 paraphrasing 而非直译？ | |
| 18 | 是否有"翻译版权"声明（如有翻译授权）？ | |

### D. 观点/idea 抄袭（6 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 19 | 用的理论框架（Model A）有原始作者引用？ | |
| 20 | 用的概念定义（Concept B）有原始定义者引用？ | |
| 21 | 用的方法（Method C）有原始方法论文献？ | |
| 22 | 用的指标（Metric D）有原始开发者引用？ | |
| 23 | 复制的实验设计 / paradigm 有原作者引用？ | |
| 24 | 引用的某实验室 preprint 有致谢？ | |

### E. LLM / AI 痕迹（6 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 25 | 没有过度套话（"值得注意的是/不可否认/综上所述"）| |
| 26 | 没有过度对仗（"不仅...而且...，既...又..."）| |
| 27 | 没有 LLM 偏好的句式（"让我们来..." / "下面我们..."）| |
| 28 | 没有虚假精度（"100% / 完全 / 绝对"）| |
| 29 | 关键事实 / 数字 / 引文有原始出处（不是 LLM 编造）| |
| 30 | AI detector score < 30%（如 GPTZero / Originality.ai）| |

---

## 🔧 自动化辅助

### 反 LLM 痕迹检查（grep 启发式）

```bash
# 找 AI 写作常见套话
grep -nE "(值得注意的是|不可否认的是|综上所述|与此同时|让我们来)" manuscript.md
```

### 反可疑引用（未引用但提到术语）

```bash
# 找文中出现的专有名词（首字母大写），但 reference list 没对应的
# 粗略版：提取文中大写开头的术语
grep -oE '[A-Z][a-z]+([ -][A-Z][a-z]+)+' manuscript.md | sort -u > /tmp/terms.txt
# 看 reference list 是否覆盖
#（人工核）
```

### 反自我抄袭

```bash
# 拿自己已发表论文的 md / pdf 做 Crossref Similarity Check
# 或用 Turnitin 的 self-plagiarism detection
```

---

## 🛠️ 集成到 research-assistant

### 工作流

```
synthesize / write 输出
        ↓
Originality Checklist（本 SOP，30 项人工 + grep 启发式）
        ↓
如有疑虑 → 改稿
        ↓
用户自行跑 Turnitin / iThenticate（外部工具）
        ↓
通过 → 走 `references/manuscript-audit-checklist.md`
```

### 命令式集成（如果未来实现）

```bash
research-assistant originality-check --input manuscript.md
# 输出：30 项 checklist 的通过/未通过报告
```

---

## 📋 反 LLM 痕迹词表（高频）

| 类别 | 词例 |
|------|------|
| 套话 | 值得注意的是、不可否认、综上所述、与此同时、不仅如此、总的来说、由此可见、这样一来、毋庸置疑 |
| 句式 | 让我们来、下面我们、首先...其次...最后、不仅...而且...、既...又... |
| 断言 | 100%、完全、绝对、必然、毫无疑问、显然 |
| 模糊化 | 可能、或许、大概、也许、似乎（如果过度堆砌）|

**替换建议**：
- "值得注意的是" → "本研究聚焦" / "我们重点关注" / 直接删
- "不仅...而且..." → 直接两个分句
- "100%" → "几乎全部（98%）"/ 删
- "绝对" → "显著 / 强"

---

## ⚠️ 边界条件

| 不要做 | 原因 |
|--------|------|
| ❌ 不要把 paraphrasing 当成"换词" | paraphrasing = 重组句式 + 加引用 |
| ❌ 不要把 AI detector 当唯一标准 | 误报率高，要人工核 |
| ❌ 不要忽视自我抄袭 | 期刊会查！|
| ❌ 不要在 dissertation 中复用自己 conference paper | 必须重写 + 标注 |

---

## 📚 参考

- ARS Academic Paper anti-leakage protocol：https://github.com/Imbad0202/academic-research-skills
- Turnitin / iThenticate 文档
- COPE 自我抄袭指南：https://publicationethics.org/
- APA 7 自我抄袭（pp. 226-227）

---

*最后更新：2026-06-22 v5.21.0*  
*来源借鉴：ARS Academic Paper anti-leakage protocol*