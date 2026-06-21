# Quarto Cite Audit Hook SOP（v5.21.0 新增）

> 来源：吸收 PaperSpine（WUBING2023/PaperSpine）LaTeX 安全审计思路，**适配 quarto + APA 7**  
> 用途：在 `quarto render <file>.md` **编译前**自动跑这个 hook，**防止** 编译失败 / 404 链接 / 重复 label / 引用 key 不存在  
> 触发时机：任何 `references/apaquarto-manuscript.md` 流程跑前必跑

---

## 🎯 解决的问题

研究助手 v5.17.0 时已修复一次 `references/index.md` 全部 404 链接的灾难（v5.17.0 evidence）。本 hook 把这类问题**自动化拦截**，避免重复发生。

### 5 类常见 quarto APA 编译错误

| 错误类型 | 表现 | 原因 |
|---------|------|------|
| **Missing cite key** | `[?] Citation not found` | .qmd 里 `@xxx` 但 references.bib 没这个 key |
| **Duplicate label** | `label multiply defined` | 两个 chunk 用同一个 `#label` |
| **Broken cross-ref** | `??` 引用显示问号 | `@sec-xxx` 章节标题改了但引用没改 |
| **Unescaped underscore** | LaTeX 报错 | `_` 在 markdown 里要转义成 `\_` |
| **Missing bibliography** | 引用全部变 [?] | YAML 头漏 `bibliography: references.bib` |

---

## 🔧 审计步骤（5 步全自动）

### Step 1：cite key 完整性

```bash
# 提取 .qmd 中所有 @citekey（排除 @fig- @tbl- @sec- 这类 cross-ref）
grep -oE '@[a-zA-Z0-9_-]+' <file>.qmd \
  | grep -v '^@fig-\|^@tbl-\|^@sec-\|^@eq-' \
  | sort -u > /tmp/cited_keys.txt

# 提取 references.bib 中所有 key
grep -oE '^@[a-zA-Z]+\{[a-zA-Z0-9_-]+' references.bib \
  | sed 's/^@[a-zA-Z]+{//' \
  | sort -u > /tmp/bib_keys.txt

# 差集 = 缺失
comm -23 /tmp/cited_keys.txt /tmp/bib_keys.txt
```

**如果有输出 → 报错 → 补 bib 或改 qmd**

### Step 2：duplicate label 检测

```bash
# 提取所有 {#label}
grep -oE '\{#[a-zA-Z0-9_-]+\}' <file>.qmd | sort | uniq -d
```

**如果有输出 → 报错 → 改 label**

### Step 3：cross-ref 一致性

```bash
# 列出所有 @sec-xxx 引用
grep -oE '@sec-[a-zA-Z0-9_-]+' <file>.qmd | sort -u > /tmp/sec_refs.txt

# 列出所有 ## 章节标题带 label
grep -oE '^# .*\{#sec-[a-zA-Z0-9_-]+\}' <file>.qmd | grep -oE 'sec-[a-zA-Z0-9_-]+' | sort -u > /tmp/sec_labels.txt

# 差集 = 引用了不存在的章节
comm -23 /tmp/sec_refs.txt /tmp/sec_labels.txt
```

**如果有输出 → 报错 → 改章节标题或引用**

### Step 4：下划线/特殊字符

```bash
# 找非代码块里的裸下划线（heuristic: 行内 code 反引号外）
grep -nE '[a-zA-Z0-9]_[a-zA-Z0-9]' <file>.qmd | grep -v '^[0-9]*:.*`.*_.*`' | head
```

**人工确认**（heuristic 不够准，需人核）

### Step 5：YAML 头完整性

```bash
head -10 <file>.qmd | grep -E '^bibliography:|^csl:|^reference-section-title:'
```

**如果 bibliography 缺失 → 报错**

---

## 🚀 集成脚本（可选）

`scripts/hooks/quarto_cite_audit.py`：

```python
#!/usr/bin/env python3
"""quarto 编译前 cite 审计 hook"""
import re, sys, subprocess
from pathlib import Path

def audit(qmd_path: str) -> bool:
    qmd = Path(qmd_path)
    bib = qmd.parent / 'references.bib'
    if not bib.exists():
        print(f'❌ {bib} 不存在')
        return False
    
    content = qmd.read_text(encoding='utf-8')
    
    # Step 1: cite key
    cited = set(re.findall(r'@([a-zA-Z][a-zA-Z0-9_-]*)', content))
    bib_keys = set(re.findall(r'^@\w+\{([^,]+),', bib.read_text(encoding='utf-8'), re.M))
    missing = cited - bib_keys - {m for m in cited if m.startswith(('fig-','tbl-','sec-','eq-'))}
    if missing:
        print(f'❌ Missing cite keys: {sorted(missing)}')
        return False
    print(f'✅ Cite keys OK ({len(cited)} cited, {len(bib_keys)} in bib)')
    
    # Step 2: duplicate label
    labels = re.findall(r'\{#([a-zA-Z0-9_-]+)\}', content)
    dup = [l for l in set(labels) if labels.count(l) > 1]
    if dup:
        print(f'❌ Duplicate labels: {dup}')
        return False
    print(f'✅ Labels OK ({len(labels)} unique)')
    
    # Step 3: cross-ref (simplified)
    sec_refs = set(re.findall(r'@sec-([a-zA-Z0-9_-]+)', content))
    sec_labels = set(re.findall(r'^# .*\{#sec-([a-zA-Z0-9_-]+)\}', content, re.M))
    missing_sec = sec_refs - sec_labels
    if missing_sec:
        print(f'❌ Missing section labels: {sorted(missing_sec)}')
        return False
    print(f'✅ Cross-refs OK')
    
    # Step 5: YAML
    if 'bibliography:' not in content[:500]:
        print('❌ YAML 头缺 bibliography')
        return False
    print(f'✅ YAML 头 OK')
    
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: quarto-cite-audit.py <file>.qmd')
        sys.exit(1)
    sys.exit(0 if audit(sys.argv[1]) else 1)
```

**调用方式**：
```bash
python3 scripts/hooks/quarto_cite_audit.py manuscript.qmd \
  && quarto render manuscript.qmd
```

---

## 📋 SOP（人工跑法）

如果没装脚本，按 5 步手动跑：

```bash
# 1. cite key
grep -oE '@[a-zA-Z0-9_-]+' manuscript.qmd | grep -v '^@fig-\|^@tbl-\|^@sec-' | sort -u > /tmp/cited.txt
grep -oE '^@[a-zA-Z]+\{[a-zA-Z0-9_-]+' references.bib | sed 's/^@[a-zA-Z]+{//' | sort -u > /tmp/bib.txt
diff /tmp/cited.txt /tmp/bib.txt  # missing in bib = 左侧有，右侧无

# 2. duplicate label
grep -oE '\{#[a-zA-Z0-9_-]+\}' manuscript.qmd | sort | uniq -d

# 3. cross-ref
grep -oE '@sec-[a-zA-Z0-9_-]+' manuscript.qmd | sort -u

# 4. 下划线（人工核）
grep -nE '[a-zA-Z0-9]_[a-zA-Z0-9]' manuscript.qmd | head

# 5. YAML 头
head -10 manuscript.qmd
```

---

## ⚠️ 边界条件

| 不要做 | 原因 |
|--------|------|
| ❌ 不要跳过审计直接 render | 90% 编译失败来自这 5 类问题 |
| ❌ 不要在 missing cite key 时用 `--citeproc=false` | 那样只是不显示，不是修复 |
| ❌ 不要修改 references.bib 中的 key 来匹配 qmd | 应该反过来，把 qmd 改成与 bib 一致 |
| ❌ 不要在 commit 前不跑 | 应该 commit 前必跑（pre-commit hook） |

---

## 📚 参考

- PaperSpine paper-spine-latex 思路
- 来源仓库：https://github.com/WUBING2023/PaperSpine
- Quarto 官方文档：https://quarto.org/docs/authoring/citations.html
- APA 7 引用核验：见 `references/apa7-citation-checklist.md`（同 v5.21.0 新增）

---

*最后更新：2026-06-22 v5.21.0*  
*来源借鉴：PaperSpine paper-spine-latex（WUBING2023/PaperSpine）*