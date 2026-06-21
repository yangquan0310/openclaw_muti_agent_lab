# APA 7 Citation Checklist（v5.21.0 新增）

> 来源：吸收通用 APA 7 规范 + Nature-skills citation 严格核验思路  
> 用途：synthesize 输出 / quarto 编译前 / 投稿前**强制跑这个 checklist**  
> 与 `hooks/quarto-cite-audit.md` 配合：审计自动化 + 本 checklist 人工核验

---

## 🎯 APA 7 引用核心规则（速查）

### In-text Citation（正文引用）

| 来源类型 | 首次引用 | 后续引用 |
|---------|---------|---------|
| 1 位作者 | Smith (2020) | Smith (2020) |
| 2 位作者 | Smith and Jones (2020) | Smith and Jones (2020) |
| 3+ 位作者 | Smith et al. (2020) | Smith et al. (2020) |
| 团体作者 | American Psychological Association (2020) | APA (2020) |
| 无作者 | Title (Year) | Title (Year) |
| 多文献 | (Smith, 2020; Jones, 2019) | - |
| 直接引用 | (Smith, 2020, p. 23) | - |

### 特殊位置

| 位置 | 格式 | 例 |
|------|------|-----|
| 句首 | Author (Year) | Smith (2020) argued... |
| 句中 | Author (Year) | ...as Smith (2020) noted... |
| 句末 | (Author, Year) | ...(Smith, 2020). |
| 括号内多文献 | 按字母排序 | (Jones, 2019; Smith, 2020) |

### Reference List（文末参考文献）

#### 期刊文章

```
Author, A. A., & Author, B. B. (Year). Title of article. 
*Journal Name*, *Volume*(Issue), Page–Page. https://doi.org/xxx
```

例：
```
Buzsáki, G. (2002). Theta oscillations in the hippocampus. 
*Neuron*, *33*(3), 325–340. https://doi.org/10.1016/S0896-6273(02)00586-X
```

#### 书

```
Author, A. A. (Year). *Title of work: Capital letter also for subtitle*. 
Publisher. https://doi.org/xxx
```

#### 书章

```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), 
*Title of book* (pp. xx–xx). Publisher.
```

#### 会议论文

```
Author, A. A. (Year, Month Days). *Title of paper*. Conference Name, 
Location. https://doi.org/xxx
```

#### 网页

```
Author, A. A. (Year, Month Day). *Title of page*. Site Name. 
https://URL
```

---

## 📋 50 项 Checklist（投稿前必跑）

### A. In-text 引用（15 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 1 | 所有引用都在 reference list 出现 | |
| 2 | 所有 reference list 条目都在正文被引用 | |
| 3 | 1 作者格式正确（Author, Year）| |
| 4 | 2 作者格式正确（Author and Author, Year）| |
| 5 | 3+ 作者首次用 et al.（Author et al., Year）| |
| 6 | 团体作者首次全称，后续缩写 | |
| 7 | 多文献按字母排序，逗号 + 分号分隔 | |
| 8 | 直接引用有页码（Author, Year, p. xx）| |
| 9 | 间接引用（Author, Year, as cited in Author, Year）| |
| 10 | 无作者用标题首词替代 | |
| 11 | 同作者同年用 a/b 区分（2020a, 2020b）| |
| 12 | 经典著作用 (Aristotle, trans. 1932) 格式 | |
| 13 | 通讯/私信用（personal communication, Month Day, Year）| |
| 14 | 引用无 "et al." 在 reference list（必须列全名）| |
| 15 | 没有 "in press" / "submitted" 漏标 | |

### B. Reference List（25 项）

#### 基本格式（10 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 16 | 作者名格式：姓, 名首字母. （全部大写首字母）| |
| 17 | & 符号在多位作者最后一位前（Smith, A. A., & Jones, B. B.）| |
| 18 | 21+ 作者：列前 19 + ... + 最后一位 | |
| 19 | 年份在括号中（2020.），无缩写月份 | |
| 20 | 标题首词大写 + 专有名词 + 冒号后首词 | |
| 21 | 期刊名斜体 + 标题大小写（Title Case）| |
| 22 | 卷号斜体，期号非斜体（括弧）| |
| 23 | 页码范围用 en dash（25–37），非 hyphen | |
| 24 | DOI 格式：https://doi.org/xxx | |
| 25 | 没有 "Retrieved from"（除非有时效内容）| |

#### 不同来源类型（15 项）

| # | 类型 | 检查项 | ✓ |
|---|------|--------|---|
| 26 | 期刊 | 期刊全名（非缩写，除非 AMA 风格）| |
| 27 | 期刊 | DOI 必备（无 DOI 用 URL）| |
| 28 | 书 | 出版社位置不再需要（APA 7）| |
| 29 | 书 | 版次注明（2nd ed.）| |
| 30 | 书章 | 编辑者名字 + (Ed.) 或 (Eds.) | |
| 31 | 会议 | 会议名 + 地点 | |
| 32 | 学位论文 | [Doctoral dissertation, University] | |
| 33 | 预印本 | 标识 bioRxiv/arXiv + DOI | |
| 34 | 网页 | 作者 + 日期 + 标题 + 站点名 + URL | |
| 35 | 新闻 | 作者 + 年月日 + 标题 + 站点 | |
| 36 | 软件 | Author (Year). *Title* (Version) [Software]. URL | |
| 37 | 数据集 | Author (Year). *Title* [Data set]. Publisher. DOI | |
| 38 | 视频 | Author/Channel (Year, Month Day). *Title* [Video]. Platform. URL | |
| 39 | 推文 | Author (Year, Month Day). *Content* [Tweet]. Platform. URL | |
| 40 | 法律 | 按 Bluebook 格式（非 APA）| |

### C. 杂项（10 项）

| # | 检查项 | ✓ |
|---|--------|---|
| 41 | 标题层一致（一律 Title Case 或 Sentence case）| |
| 42 | 缩写首次给全称（LTP, long-term potentiation）| |
| 43 | 数字格式（< 100 用 word，> 100 用数字）| |
| 44 | 统计量格式：t(28) = 2.34, p = .013（小 p 加 0）| |
| 45 | 希腊字母用符号不用字母名（α 不是 alpha）| |
| 46 | et al. 后有逗号（Smith et al., 2020）| |
| 47 | 引号格式（美式双引号，英式单引号）| |
| 48 | 斜体用于：期刊名、书名、统计量符号、首次拉丁词 | |
| 49 | 表格图注符合期刊格式 | |
| 50 | 全文 reference list 按作者字母排序 | |

---

## 🔧 自动化辅助脚本

```python
# 简单 grep 辅助
import re

def check_apa7_intext(text: str) -> list:
    """返回可疑引用列表"""
    issues = []
    # 找 (Author, Year) 模式
    cites = re.findall(r'\(([^)]+,\s*\d{4}[a-z]?)\)', text)
    for c in cites:
        # 检查 Author 和 Year 间有空格
        if ',' not in c.split(';')[0]:
            issues.append(f'格式可疑: ({c})')
        # 检查多文献是否按字母排
        if ';' in c:
            authors = [a.strip().split(',')[0] for a in c.split(';')]
            if authors != sorted(authors):
                issues.append(f'未按字母排序: ({c})')
    return issues
```

---

## ⚠️ 边界条件

| 不要做 | 原因 |
|--------|------|
| ❌ 不要把 APA 7 套到非 APA 期刊 | 期刊有自家格式（如 Vancouver / AMA）|
| ❌ 不要把"et al." 用于 reference list | reference list 必须列全部作者 |
| ❌ 不要直接引用超过 40 字 | 改 paraphrasing |
| ❌ 不要混用 APA 6 和 7 规则 | 必须全用 7 |

---

## 📚 参考

- APA Publication Manual (7th ed.)
- Nature-skills nature-citation（严格 CNS 引用）：https://github.com/Yuan1z0825/nature-skills
- APA Style 官方：https://apastyle.apa.org/
- Purdue OWL APA：https://owl.purdue.edu/owl/research_and_citation/apa_style/

---

*最后更新：2026-06-22 v5.21.0*  
*来源借鉴：通用 APA 7 + Nature-skills citation*