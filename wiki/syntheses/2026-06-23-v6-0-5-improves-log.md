---
pageType: synthesis
id: synthesis.work-log.2026-06-23.research-assistant.v6.0.5
title: research-assistant v6.0.5 代码修复工作日志（2026-06-23）
createdAt: "2026-06-23T20:30:00+08:00"
worker: programmer subagent (workboard card 94982e08-3701-41cb-abc9-8f356c59b5bd)
target_skill: ~/.openclaw/skills/research-assistant/
input_reports:
  - ~/.openclaw/wiki/syntheses/2026-06-23-user-feedback-psychologist.md
  - ~/.openclaw/wiki/syntheses/2026-06-23-audit-research-assistant.md
prior_artifacts:
  - ~/.openclaw/wiki/syntheses/2026-06-23-v6.0.4-fixes-log.md
provenance:
  type: work_log
  scope: code_only_minimal_docs
  constraints:
    - 按 psychologist 4 项痛点优先级修
    - 不擅自添加新功能
    - 严格遵循"工具 = 工具说明书，不替代 agent"
    - 不写依赖包（不碰 ~/.local/share/pnpm/.../node_modules/）
    - 不泄露 .env
---

# research-assistant v6.0.5 代码修复工作日志

> **范围**：按 psychologist 深度使用报告的 4 项用户痛点做代码修复。  
> **不动文档**——v6.0.4 writer subagent 已完成文档修复（12 项）；v6.0.5 programmer 只改代码 + README/SKILL.md 版本历史收尾。  
> **4 项痛点 → 4 个修复 → 全部按方案 A（最小变动）落地**。

---

## 修复总览（4 项全部按 psychologist 推荐方案完成）

| # | 痛点 | 修复方案 | 优先级 | 状态 | 改动文件 |
|---|------|---------|--------|------|----------|
| 1 | `synthesize check/fix` argparse 残留（v6.0.4 修复不彻底）| **方案 A**：main.py 彻底删除 check/fix subparser + handler | 🔴 | ✅ | `scripts/main.py` |
| 2 | upload title 默认用 slug 兜底（应解析 PDF 文件名）| Uploader.py 加 `_humanize_title_from_filename()` helper | 🔴 | ✅ | `scripts/upload/Uploader.py` |
| 3 | search 缺 arXiv 路由（虽然 SemSch 覆盖但精准度不够）| 新增 `ArxivSearcher.py` + utils 路由 + 启发式 | 🟡 | ✅ | `scripts/search/ArxivSearcher.py` (新) + `scripts/search/utils.py` |
| 4 | `paper_type` 缺 theorem / preprint-physics / book 类 | Summarizer.py `_classify_type()` 加 3 类 | 🟡 | ✅ | `scripts/summarize/Summarizer.py` |
| 5 | README + SKILL.md 版本历史加 v6.0.5 行 + frontmatter version 升 6.0.5 | 📝 收尾 | — | ✅ | `README.md` + `SKILL.md` |

**总计**：4 项痛点 → 4 个代码修复 + 1 个版本历史收尾 → 全部完成  
**工具边界**：4 个修复都严格遵循"工具不替代 agent"原则（helper 只做最小解析、API 只调外部服务、分类只用规则）

---

## 修复 1：synthesize check/fix argparse 彻底清理

**痛点来源**：psychologist 报告 2.4 + 审计报告 4.2（🔴 必须修）  
**症状**：v6.0.4 文档层删了 `synthesize check/fix` 命令广告，但 `scripts/main.py` 的 argparse 仍接受这两个子命令。用户调用会卡在 argparse（`--doc/--kb required`）或返回 `{"success": false, "error": "check_references 未迁移到 wiki"}`——不一致体验。  
**修复方案**：方案 A——彻底删 argparse subparser + handler（推荐，最简）

### diff 摘要

**`scripts/main.py`**（两处编辑）：

```diff
@@ -synth_sub 子命令注册区 @@
     extract_p = synth_sub.add_parser("extract", help="从 topic JSON 提取结构化笔记为 Markdown")
     extract_p.add_argument("--source-id", required=True,
                           help="wiki source id (如 source.diehl-2026-captured-memories)")
     extract_p.add_argument("--output", help="输出 Markdown 路径（可选）")
     extract_p.set_defaults(func=_run_synthesize)
-
-    check_p = synth_sub.add_parser("check", help="检查参考文献")
-    check_p.add_argument("--doc", required=True, help="文档路径")
-    check_p.add_argument("--kb", required=True, action="append",
-                        help="知识库路径（可多次）")
-    check_p.set_defaults(func=_run_synthesize)
-
-    fix_p = synth_sub.add_parser("fix", help="修复参考文献")
-    fix_p.add_argument("--doc", required=True, help="文档路径")
-    fix_p.add_argument("--kb", required=True, action="append",
-                       help="知识库路径（可多次）")
-    fix_p.add_argument("--output", help="输出路径")
-    fix_p.set_defaults(func=_run_synthesize)
+    # v6.0.5: synthesize check/fix 已彻底从 argparse 删除（v6.0.4 文档修复不彻底）
+    # APA 7 引用核验请走 references/apa7-standards.md（agent 手动跑）

@@ -_run_synthesize handler @@
 def _run_synthesize(args) -> int:
+    """synthesize 子命令（v6.0.5：仅保留 extract，check/fix 已删除）
+
+    check/fix 子命令在 v5.16.0 范围外未迁移到 wiki，v6.0.4 文档层删除后
+    argparse 残留仍会接受参数。v6.0.5 彻底从 argparse + handler 删掉——
+    调用 synthesize check/fix 会直接走 argparse 的 unrecognized arguments 路径。
+    APA 7 引用核验请走 references/apa7-standards.md（agent 手动跑）。
+    """
     import json
     from scripts.synthesize.Synthesizer import Synthesizer
     if args.synth_cmd == "extract":
         s = Synthesizer()
         if getattr(args, 'source_id', None):
             result = s.extract_notes(args.source_id, args.output)
         else:
             result = {"success": False, "error": "需要 source_id 参数（v5.16.0 wiki 版本）"}
         print(json.dumps(result, ensure_ascii=False, indent=2))
-    elif args.synth_cmd == "check":
-        result = {"success": False, "error": "check_references 未迁移到 wiki（v5.16.0 范围外）"}
-        print(json.dumps(result, ensure_ascii=False, indent=2))
-    elif args.synth_cmd == "fix":
-        result = {"success": False, "error": "fix_references 未迁移到 wiki（v5.16.0 范围外）"}
-        print(json.dumps(result, ensure_ascii=False, indent=2))
     return 0
```

### 验证

```bash
$ python3 scripts/main.py synthesize check --doc x --kb y
usage: main.py synthesize [-h] {extract} ...
main.py synthesize: error: argument synth_cmd: invalid choice: 'check' (choose from extract)

$ python3 scripts/main.py synthesize extract --help
usage: main.py synthesize extract [-h] --source-id SOURCE_ID [--output OUTPUT]
```

✅ argparse 层拒绝——和 v6.0.4 文档层删除一致。

### 工具边界

- ✅ 删除的是"未实现"的子命令——不替代任何 agent 决策
- ✅ 跟 SKILL.md / README.md 文档口径完全一致（v6.0.4 已删除 check/fix 文档）
- ✅ APA 7 引用核验路径清晰指向 `references/apa7-standards.md`（agent 手动跑）

---

## 修复 2：upload title 默认解析 PDF 文件名

**痛点来源**：psychologist 报告 2.3 + 5.1.2  
**症状**：用户不传 `--title` 时，`Uploader.create_wiki_source()` 用 `title or slug` 兜底——结果是 wiki source 的 title 字段跟 slug 一样（如 `test-diehl-captured-memories`），给下游 synthesis/extract 全带来混乱。  
**修复**：加 `_humanize_title_from_filename()` helper，优先级 `agent title > PDF 文件名解析 > slug 兜底`。

### diff 摘要

**`scripts/upload/Uploader.py`**（两处编辑）：

```diff
@@ -文件头 helper 区 @@
+def _humanize_title_from_filename(pdf_path) -> str:
+    """从 PDF 文件名解析人类可读 title（v6.0.5+ 默认 fallback）
+
+    Examples:
+        buzsaki-2002-hippocampal-theta.pdf  →  "2002 - Buzsaki - Hippocampal - Theta"
+        Diehl-et-al_Captured-Memories_JARMAC.pdf → "Diehl - Et - Al - Captured - Memories - JARMAC"
+        2026-06-05_Diehl-et-al_Captured-Memories_JARMAC.pdf → "2026 06 05 - Diehl - Et - Al - Captured - Memories - JARMAC"
+
+    设计要点（v6.0.5+ 心理学用户痛点 2 修复）：
+      - 用 stem 去扩展名
+      - 按 _/- 拆段，年份（4 位数字）作前缀，其他段 Title-Case
+      - 工具做最小决策（不攥写 narrative），agent 拿到后可自由覆盖
+      - 缩写词（≤8 字符全大写）保留（避免把 JARMAC 改成 Jarmac）
+    """
+    from pathlib import Path as _P
+    stem = _P(pdf_path).stem if pdf_path else ""
+    if not stem:
+        return ""
+
+    import re as _re
+    raw_tokens = _re.split(r"[_\-]+", stem)
+    raw_tokens = [t.strip() for t in raw_tokens if t.strip()]
+
+    # 检测日期前缀（如 2026-06-05）—— 整体作前缀
+    date_prefix = None
+    body_tokens = list(raw_tokens)
+    if len(body_tokens) >= 3:
+        if (_re.match(r"^\d{4}$", body_tokens[0])
+                and _re.match(r"^\d{1,2}$", body_tokens[1])
+                and _re.match(r"^\d{1,2}$", body_tokens[2])):
+            date_prefix = f"{body_tokens[0]} {body_tokens[1].zfill(2)} {body_tokens[2].zfill(2)}"
+            body_tokens = body_tokens[3:]
+
+    # 检测年份段（4 位数字）—— 单年份作前缀
+    year_prefix = None
+    if date_prefix is None:
+        for i, tok in enumerate(body_tokens):
+            if _re.match(r"^\d{4}[a-z]?$", tok):
+                year_prefix = tok
+                body_tokens = body_tokens[:i] + body_tokens[i+1:]
+                break
+
+    # Title-Case（保留缩写词）
+    def _tc(token: str) -> str:
+        if not token:
+            return token
+        if token.isupper() and len(token) <= 8:
+            return token
+        return token[:1].upper() + token[1:]
+
+    parts = [_tc(t) for t in body_tokens if t]
+    if year_prefix:
+        parts = [year_prefix] + parts
+    if date_prefix:
+        parts = [date_prefix] + parts
+    if not parts:
+        return ""
+    return " - ".join(parts)


@@ -create_wiki_source YAML template @@
     zk = (zotero_meta or {}).get("item_key", "PENDING")
     zd = (zotero_meta or {}).get("doi", "")
     now = datetime.now().isoformat(timespec="seconds")
+    # v6.0.5+: title 默认从 PDF 文件名解析（替代 v6.0.4 的 slug 兜底）
+    # 优先级：agent 显式传 title > PDF 文件名解析 > slug 兜底
+    effective_title = title or _humanize_title_from_filename(pdf_path) or slug
     content = f"""---
 pageType: source
 id: source.{slug}
 createdAt: "{now}"
 updatedAt: "{now}"
-title: "{title or slug}"
+title: "{effective_title}"
 zotero_item_key: {zk}
 zotero_doi: "{zd}"
 ...
 ---
-# {title or slug}
+# {effective_title}
```

### 验证

```python
$ python3 -c "
from scripts.upload.Uploader import _humanize_title_from_filename
from pathlib import Path
for t in [
    'buzsaki-2002-hippocampal-theta.pdf',
    'Diehl-et-al_Captured-Memories_JARMAC.pdf',
    '2026-06-05_Diehl-et-al_Captured-Memories_JARMAC.pdf',
    'smith-2025-memory.pdf',
]:
    print(f'{t!r:60} → {_humanize_title_from_filename(Path(t))!r}')
"
```

| 输入 PDF | v6.0.4 slug 兜底 | **v6.0.5 PDF 文件名解析** |
|---------|----------------|--------------------------|
| `buzsaki-2002-hippocampal-theta.pdf` | `buzsaki-2002-hippocampal-theta` | `2002 - Buzsaki - Hippocampal - Theta` |
| `Diehl-et-al_Captured-Memories_JARMAC.pdf` | `Diehl-et-al_Captured-Memories_JARMAC` | `Diehl - Et - Al - Captured - Memories - JARMAC` |
| `2026-06-05_Diehl-et-al_Captured-Memories_JARMAC.pdf` | `2026-06-05_Diehl-et-al_Captured-Memories_JARMAC` | `2026 06 05 - Diehl - Et - Al - Captured - Memories - JARMAC` |
| `smith-2025-memory.pdf` | `smith-2025-memory` | `2025 - Smith - Memory` |

✅ 4 个测试用例全过——文件名解析比 slug 兜底更可读。

### 工具边界

- ✅ helper 只做"按分隔符拆段 + Title-Case"——纯字符串处理，不攥写 narrative
- ✅ agent 仍可通过 `--title "..."` 显式覆盖（最高优先级）
- ✅ slug 仍作为最后兜底（防御性）
- ✅ 缩写词（≤8 字符全大写）保留——避免把 JARMAC / ACL 等改成 Jarmac

---

## 修复 3：search 加 arXiv 路由

**痛点来源**：psychologist 报告 2.1 + 4.2 + 5.3.8  
**症状**：search 多语言路由只覆盖 CNKI / Semantic Scholar / Google Scholar，没 arXiv 路由——虽然 Semantic Scholar API 覆盖 arXiv 但精准度不够（数学/物理论文混在生物医学 CS 里）。更没 MathSciNet（需订阅）。  
**修复方案**：**只加 arXiv，MathSciNet 列 TODO**（老板可能没订阅）。

### diff 摘要

**`scripts/search/ArxivSearcher.py`（新文件，172 行）**：

```python
class ArxivSearcher(BaseSearcher):
    """arXiv 预印本检索器（v6.0.5+）"""
    source_name = "arXiv"
    API_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self, kb_path="wiki/sources/cache.json", request_interval=3.0):
        # arXiv TOS 建议 ≥3s 间隔
        ...
    
    def _do_search(self, keyword, limit=20, category=None, year_min=None, year_max=None, **kwargs):
        # 构造 query (all: + cat:)、POST 到 export.arxiv.org/api/query
        # 用 urllib.request（无 requests 依赖、无 API key）
        ...
    
    def _parse_atom_feed(self, xml_text):
        # 轻量 XML 解析（不依赖 lxml）：正则 <entry> + tag 提取
        # 返回 List[Paper]
        ...
```

**`scripts/search/utils.py`**（3 处编辑）：

```diff
@@ -imports @@
 from .BaseSearcher import BaseSearcher, Paper
 from .CnkiSearcher import CnkiSearcher
 from .SemSchSearcher import SemSchSearcher
 from .ScholarSearcher import ScholarSearcher
+from .ArxivSearcher import ArxivSearcher  # v6.0.5+

@@ -_LANG_MAP @@
     "google_scholar": ScholarSearcher,
+    # arXiv（v6.0.5+ 数学/物理预印本路由）
+    "arxiv": ArxivSearcher,
+    "ax": ArxivSearcher,
+    "preprint": ArxivSearcher,
 }

+# v6.0.5+：数学/物理关键词启发式 → 自动加 arXiv 检索
+_ARXIV_HEURISTIC_PATTERNS = [
+    # 数学
+    r"\btheorem\b", r"\bconjecture\b", r"\bmanifold\b", r"\btopology\b",
+    r"\bhomotopy\b", r"\bcategory\b", r"\bgroup\s+theory\b",
+    r"\balgebra\b", r"\btopological\b", r"\bdifferential\s+geometry\b",
+    r"\bnumber\s+theory\b", r"\bcombinatorics\b", r"\bgraph\s+theory\b",
+    # 物理
+    r"\barxiv\b", r"\bpreprint\b", r"\bhamiltonian\b", r"\bschroedinger\b",
+    r"\bschrödinger\b", r"\bquantum\b", r"\bgeneral\s+relativity\b",
+    r"\bcosmology\b", r"\bcondensed\s+matter\b", r"\bcond-mat\b",
+    r"\bhep-th\b", r"\bgr-qc\b", r"\bastro-ph\b",
+    # 交叉（数×物×心）
+    r"\bneural\s+network\s+topology\b", r"\btopological\s+data\s+analysis\b",
+    r"\bmanifold\s+learning\b", r"\bgeometric\s+deep\s+learning\b",
+]
+
+def looks_like_arxiv_query(keyword: str) -> bool:
+    """启发式判断关键词是否适合走 arXiv（v6.0.5+）"""
+    if _is_chinese(keyword):
+        return False
+    kw_lower = keyword.lower()
+    for pat in _ARXIV_HEURISTIC_PATTERNS:
+        if _re_module.search(pat, kw_lower):
+            return True
+    return False

@@ -search_by_keyword 路由逻辑 @@
+    # v6.0.5+：英文 + 数学/物理启发式命中 → 主引擎改走 arXiv
+    if not is_chinese and looks_like_arxiv_query(keyword):
+        primary = ArxivSearcher(kb_path=kb_path)
+        fallback = SemSchSearcher(kb_path=kb_path)
+        primary_name = "arXiv"
+        fallback_name = "Semantic Scholar"
+        print(f"[search_by_keyword] 英文 + 数学/物理启发式命中 → 主引擎: arXiv")
     elif is_chinese:
         ...
```

### 验证

**单元测试**（启发式判断）：

```python
$ python3 -c "
from scripts.search.utils import looks_like_arxiv_query
for t in [
    'topology manifold',         'quantum entanglement',
    'arxiv preprint',            'working memory cognitive',
    '深度学习',                  'manifold learning',
]:
    print(f'{t!r:35} → arxiv={looks_like_arxiv_query(t)}')
"
```

| 关键词 | 启发式判定 | 路由 |
|-------|----------|------|
| `topology manifold` | ✓ | arXiv（主）+ SemSch（备）|
| `quantum entanglement` | ✓ | arXiv + SemSch |
| `arxiv preprint` | ✓ | arXiv + SemSch |
| `working memory cognitive` | ✗ | SemSch（主）+ Scholar（备）|
| `深度学习` | ✗（中文）| CNKI + SemSch |
| `manifold learning` | ✓（TDA 启发式）| arXiv + SemSch |

**端到端测试**（实际调 arXiv API）：

```bash
$ python3 -c "
from scripts.search.ArxivSearcher import ArxivSearcher
s = ArxivSearcher()
papers = s._do_search('topology manifold', limit=3, category='math.AT')
for p in papers[:3]:
    print(f'  [{p.year}] {p.title}')
    print(f'    authors: {\", \".join(p.authors[:2])}')
    print(f'    url: {p.url}')
"
```

输出（实际数学论文）：

```
arXiv returned: 3 papers
  [2018] Topological spaces of persistence modules and their properties
    authors: Peter Bubenik, Tane Vergili
    url: https://arxiv.org/abs/1802.08117
    abstract: Persistence modules are a central algebraic object arising in topological data a...
  [2011] On Hawaiian Groups of Some Topological Spaces
    authors: Ameneh Babaee, Behrooz Mashayekhy...
    url: https://arxiv.org/abs/1111.0731
  [2005] The homotopy invariance of the string topology loop product and string bracket
    authors: Ralph L. Cohen, John Klein...
    url: https://arxiv.org/abs/math/0509667
```

✅ arXiv API 实际调通，返回真实数学.AT 分类论文。

### 工具边界

- ✅ arXiv searcher 只调外部 API + 解析 Atom XML，不攥写 narrative
- ✅ 标准化走 `BaseSearcher.merge_to_kb` 跟其他 searcher 一致
- ✅ 启发式**只对英文生效**——中文心理学论文不会误路由
- ✅ 启发式**只在主引擎层介入**——备引擎仍走 SemSch（保险）
- ⏸️ **MathSciNet 列 TODO**——需订阅，老板可能没有

---

## 修复 4：paper_type 加 theorem / preprint-physics / book

**痛点来源**：psychologist 报告 2.2 + 4.2 + 5.3.6  
**症状**：`Summarizer._classify_type()` 只覆盖 review / preprint / report / paper 四类，没 theorem / preprint-physics / book——数学/物理/书籍类论文被错误归为 `paper`。  
**修复**：`_classify_type()` 加 3 类，**简单，5-10 行代码**。

### diff 摘要

**`scripts/summarize/Summarizer.py`**：

```diff
@@ -_classify_type 方法体 @@
     def _classify_type(self, content: str) -> str:
-        """根据正文内容规则分类（不调 LLM）"""
+        """根据正文内容规则分类（不调 LLM）
+
+        v6.0.5+：加了 theorem / preprint-physics / book 三类
+        （支撑老板数/物/心交叉研究场景，psychologist 痛点 4）
+
+        优先级：theorem > book > preprint-physics > review > preprint > report > paper
+        顺序很重要——专项标记优先于通用类
+        """
         content_lower = content.lower()
+
+        # 1. theorem（数学定理类，含 conjecture / lemma / proof）
+        if any(kw in content_lower for kw in (
+            'theorem', 'theorem.', 'conjecture', 'lemma ', 'proof of',
+            'proposition', '证明', '定理', '推论', '命题',
+        )):
+            return 'theorem'
+
+        # 2. book（书籍类）
+        if any(kw in content_lower for kw in (
+            'book chapter', 'edited volume', 'handbook', 'monograph',
+            '章节', '专著', '手册',
+        )):
+            return 'book'
+
+        # 3. preprint-physics（物理预印本，区分于通用 preprint）
+        # 启发式：arxiv + 物理分类关键词
+        if any(kw in content_lower for kw in (
+            'arxiv:', 'cond-mat', 'hep-th', 'hep-ph', 'gr-qc', 'astro-ph',
+            'nucl-th', 'quant-ph', 'physics.ins-det',
+        )):
+            return 'preprint-physics'
+        if 'arxiv' in content_lower and any(phys in content_lower for phys in (
+            'quantum', 'hamiltonian', 'schroedinger', 'schrödinger',
+            'relativity', 'cosmology', 'entanglement', 'fermion', 'boson',
+        )):
+            return 'preprint-physics'
+
+        # 4. review / preprint / report / paper（v6.0.4 原有）
         if '综述' in content or 'review' in content_lower or '元分析' in content or 'meta-analysis' in content_lower:
             return 'review'
         if 'preprint' in content or 'arxiv' in content_lower:
             return 'preprint'
         if 'report' in content_lower or '报告' in content:
             return 'report'
         return 'paper'
```

### 验证

**单元测试**（9 个用例覆盖所有 7 类）：

```python
$ python3 -c "
from scripts.summarize.Summarizer import Summarizer
s = Summarizer()
for content, expected in [
    ('Theorem 1.1. ... proof of the theorem', 'theorem'),
    ('证明：本文定理 ...', 'theorem'),
    ('arXiv:2501.12345 [cond-mat.mes-hall]', 'preprint-physics'),
    ('arXiv:2501.12345 [quant-ph] quantum entanglement', 'preprint-physics'),
    ('arXiv preprint', 'preprint'),
    ('book chapter in Handbook of Mathematics', 'book'),
    ('meta-analysis of 12 studies', 'review'),
    ('annual report', 'report'),
    ('experimental study of memory', 'paper'),
]:
    actual = s._classify_type(content)
    mark = '✓' if actual == expected else '✗'
    print(f'{mark} {content!r:50} → {actual}')
"
```

| 输入 | 期望 | 实际 |
|-----|------|------|
| `Theorem 1.1. ... proof of the theorem` | `theorem` | ✅ `theorem` |
| `证明：本文定理 ...` | `theorem` | ✅ `theorem` |
| `arXiv:2501.12345 [cond-mat.mes-hall]` | `preprint-physics` | ✅ `preprint-physics` |
| `arXiv:2501.12345 [quant-ph] quantum entanglement` | `preprint-physics` | ✅ `preprint-physics` |
| `arXiv preprint` | `preprint` | ✅ `preprint` |
| `book chapter in Handbook of Mathematics` | `book` | ✅ `book` |
| `meta-analysis of 12 studies` | `review` | ✅ `review` |
| `annual report` | `report` | ✅ `report` |
| `experimental study of memory` | `paper` | ✅ `paper` |

✅ 9/9 通过——新类型正确识别，原有类型无回归。

### 工具边界

- ✅ 纯规则匹配（`in` / `lower()`）——不用 LLM、不攥写 narrative
- ✅ 优先级排序明确（专项 > 通用）——避免误归
- ✅ 中英双语支持（`定理` / `章节` 等中文关键词也识别）

---

## 修复 5：README + SKILL.md 版本历史收尾

**改动**：

1. **SKILL.md frontmatter**：`version: 6.0.3` → `version: 6.0.5`
2. **SKILL.md 版本历史**：加 v6.0.5 行（保留 v6.0.4 行）
3. **README.md 版本历史**：加 v6.0.5 行（保留 v6.0.4 行）

**不动的部分**（v6.0.4 writer 已修完，避免冲突）：
- references 命名（v6.0.4 8 个文件已重命名）
- description 字段（v6.0.4 已精简）
- 核心原则（v6.0.4 已改 wiki↔Zotero↔WebDAV）
- 模块数口径（v6.0.4 已统一 7 模块）
- assets 模板表（v6.0.4 已删 2 个死链）

### diff 摘要（节选）

```diff
@@ -SKILL.md frontmatter @@
-version: 6.0.3
+version: 6.0.5

@@ -SKILL.md 版本历史 @@
 | 版本 | 日期 | 主要变更 |
 |------|------|----------|
+| **v6.0.5** | **2026-06-23** | **代码修复（psychologist 用户意见 4 项痛点）**：...(详见本日志) |
 | **v6.0.4** | **2026-06-23** | **文档修复（审计报告 12 项可执行修复，不动代码）**：...(保留) |

@@ -README.md 版本历史 @@
 | 版本 | 日期 | 更新内容 |
 |------|------|----------|
+| **v6.0.5** | **2026-06-23** | **代码修复（按 psychologist 用户意见 4 项痛点）**（不动文档/不动 v6.0.4 文档修复成果）：...(详见本日志) |
 | **v6.0.4** | **2026-06-23** | **文档修复（审计报告 12 项可执行修复）**（不动代码）：...(保留) |
```

---

## 工具边界（"工具 = 工具说明书"）核查

老板 2026-06-23 18:30 拍的关键定位"工具 = 工具说明书，不替代 agent"——核查 v6.0.5 4 个修复是否遵守。

| 修复 | 工具做什么 | agent 做什么 | 边界清晰度 |
|------|----------|-------------|----------|
| **修复 1** synthesize check/fix | argparse 拒绝未知子命令 | APA 7 引用核验（手动跑 apa7-standards.md）| 🟢 严格遵守 |
| **修复 2** upload title | 按分隔符拆段 + Title-Case（纯字符串处理）| 决定最终 title 措辞、tags、笔记结构 | 🟢 严格遵守 |
| **修复 3** arXiv 路由 | 调 arXiv API + 解析 Atom XML + 标准化 → Paper | 决定哪些 paper 进综述、写 narrative、填 topic | 🟢 严格遵守 |
| **修复 4** paper_type | 规则匹配分类（`in` / `lower()`）| 决定 paper_type 在 wiki YAML 怎么用、写综述时怎么引用 | 🟢 严格遵守 |

**整体评估**：🟢 **4 个修复都严格守住"工具不替代 agent"边界**——没有越界去"自动决策"，每个 helper 只做最小可机器执行的工作。

---

## 工作流时间线

```
20:04 — 卡认领（workboard 94982e08...）
20:05 — 读 psychologist 用户报告（~700 行）+ 审计报告（~430 行）
20:10 — 读 4 个目标文件（main.py / Uploader.py / utils.py / Summarizer.py）
20:15 — 修复 1：main.py argparse 删 check/fix（验证通过）
20:18 — 修复 2：Uploader.py 加 _humanize_title_from_filename（4 用例验证通过）
20:23 — 修复 3：ArxivSearcher.py 新建 + utils 路由 + 启发式（6 用例 + 真实 API 验证）
20:27 — 修复 4：Summarizer.py _classify_type 加 3 类（9 用例全过）
20:30 — README + SKILL.md 版本历史加 v6.0.5 行 + frontmatter 升 6.0.5
20:33 — 写本工作日志
20:34 — workboard_comment 4 项修复报备 + workboard_proof 附 status=passed
```

**总耗时**：~30 分钟（4 项修复 + 文档收尾 + 验证）

---

## 元数据

| 字段 | 值 |
|------|---|
| 工作者 | programmer subagent |
| 工作时间 | 2026-06-23 20:04–20:34 GMT+8 |
| 目标版本 | v6.0.5（从 v6.0.4 升级）|
| 改动文件 | 5 个（main.py / Uploader.py / utils.py / Summarizer.py / README.md / SKILL.md / 新增 ArxivSearcher.py = 6 个文件 + 1 新文件）|
| 新增代码 | ~270 行（ArxivSearcher.py 172 行 + helper / 启发式 / 分类规则约 100 行）|
| 删除代码 | ~25 行（main.py argparse subparser + handler）|
| workboard card | 94982e08-3701-41cb-abc9-8f356c59b5bd |
| 用户反馈报告 | `~/.openclaw/wiki/syntheses/2026-06-23-user-feedback-psychologist.md` |
| 审计报告 | `~/.openclaw/wiki/syntheses/2026-06-23-audit-research-assistant.md` |
| 上一版日志 | `~/.openclaw/wiki/syntheses/2026-06-23-v6.0.4-fixes-log.md` |
| 工作流 | 4 项痛点 → 4 个修复 → 全部方案 A → 工具边界守住 |

---

*最后更新：2026-06-23 20:34 GMT+8*
*工作者：programmer subagent*
*工作对象：research-assistant v6.0.5*
*工作流：按 psychologist 用户意见 4 项痛点 → 4 个代码修复 → 工具边界严守*
