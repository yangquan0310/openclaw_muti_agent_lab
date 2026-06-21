# Data Availability Statement 模板（v5.21.0 新增）

> 来源：吸收 Nature-skills（Yuan1z0825/nature-skills）nature-data + FAIR 原则  
> 用途：投稿前自动生成符合 Nature / Cell / Science 标准的 Data Availability Statement  
> 触发：synthesize 输出最终稿 → 走"生成 DAS"步骤

---

## 🎯 为什么需要？

Nature 系列期刊强制要求 **Data Availability Statement (DAS)**：
- 数据是否公开
- 公开在哪（DOI / accession ID）
- 是否有访问限制

研究助手 v5.20.0 之前**没有自动生成 DAS**，用户投稿前要手写。

---

## 📋 模板（按数据状态 4 选 1）

### 模板 A：完全公开

```markdown
## Data Availability

All data generated or analysed during this study are included in this article 
and its supplementary files. The raw datasets generated and analysed during 
the current study are also available in the [REPOSITORY NAME] repository, 
[DOI/PERMALINK].

**Source data**：[列出每个 figure/table 的源数据文件]
**Code availability**：All analysis code is available at [REPOSITORY + DOI]。
```

### 模板 B：部分公开（敏感数据）

```markdown
## Data Availability

The datasets generated and analysed during the current study are available 
from the corresponding author on reasonable request. The de-identified 
participant data that underlie the results in this article will be shared 
with researchers who provide a methodologically sound proposal.

**Restrictions**：Participant privacy / GDPR / IRB restrictions  
**Access procedure**：Apply via [email/link] + data access agreement  
**Time frame**：Response within 30 days; data shared within 90 days
```

### 模板 C：第三方数据

```markdown
## Data Availability

This study used third-party data from [DATASET NAME], obtained under license 
from [PROVIDER]. Due to the licensing agreement, we cannot publicly share 
these data. Researchers interested in accessing the data should contact 
[PROVIDER CONTACT] directly.

**Citation requirements**：[原文引用格式]
**Access link**：[如果有公开申请门户]
```

### 模板 D：无可用数据（理论/方法学论文）

```markdown
## Data Availability

No new data were generated or analysed in support of this research. All 
results derive from previously published studies, which are cited in the 
reference list.

**Theory/Method paper only**：[说明这是理论/方法学贡献]
```

---

## 🔧 集成到 research-assistant

### 自动生成 DAS 的 4 步

1. **扫描 manuscript**
   ```bash
   grep -E "^(figure|fig\.|table|tab\.)" manuscript.md | head
   grep -E "\.csv|\.tsv|\.json|\.xlsx" manuscript.md
   ```

2. **识别数据状态**
   - 是否提到 "data available at"?
   - 是否提到 IRB / 伦理限制?
   - 是否纯理论/方法?

3. **匹配模板（A/B/C/D）**

4. **写入 manuscript 末尾**
   - 位置：`## Data Availability` 在 Acknowledgments 之前
   - Word count：50-200 字（Nature 偏好 100-150）

---

## 📋 DAS 核验 Checklist

| 检查项 | 是/否 |
|--------|-------|
| 提供了 DOI 或 accession ID？ | |
| 说明了访问限制（如有）？ | |
| 提供了 contact email 或申请链接？ | |
| 提到了伦理 / GDPR / IRB（如适用）？ | |
| 引用格式符合目标期刊？ | |
| 长度 50-200 字？ | |
| 与 supplementary files 一致？ | |
| Code availability 单独列？ | |

---

## 🛠️ 反例 vs 正例

| 反例 ❌ | 正例 ✅ | 改了什么 |
|--------|--------|---------|
| 数据可向作者索取。 | 数据可向通讯作者索取（email@example.com）。30 天内回复合理申请，签署数据访问协议后 90 天内共享。 | 加 contact + 时间承诺 |
| 数据都公开了。 | 所有数据可在 Zenodo 公开访问（DOI: 10.5281/zenodo.XXXXXXX）。 | 加具体 DOI |
| 用了 public dataset。 | 本研究使用了 [DATASET NAME] 数据（[PROVIDER] 提供）。因许可协议，无法公开共享。研究人员可通过 [申请链接] 申请访问。 | 加限制说明 + 申请路径 |

---

## 🛠️ 命令式集成（如果未来实现）

```bash
# 未来加个命令（不在 v5.21.0 范围）：
research-assistant das --input manuscript.md \
                       --output manuscript-with-das.md \
                       --template B \
                       --contact "yangquan@xxx.edu"
```

---

## ⚠️ 边界条件

| 不要做 | 原因 |
|--------|------|
| ❌ 不要替用户决定数据是否可公开 | 用户/伦理委员会决定 |
| ❌ 不要编造 DOI / accession ID | 必须用户确认 |
| ❌ 不要忽略第三方数据许可 | 违反许可 = 法律风险 |
| ❌ 不要把 supplementary 当 primary data | 必须区分 |

---

## 📚 参考

- Nature-skills nature-data：https://github.com/Yuan1z0825/nature-skills
- Nature Data Availability Statement 指南：https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards
- FAIR 原则：https://www.go-fair.org/fair-principles/
- DataCite DOI 注册：https://datacite.org

---

*最后更新：2026-06-22 v5.21.0*  
*来源借鉴：Nature-skills nature-data*