"""summarizer.py - Summarizer 类（单篇笔记生成）"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from scripts.utils import config, frontmatter, WIKI_SOURCES, WIKI_SYNTHESES


class Summarizer:
    """从 wiki source 读 → 分类 + 评级 + 提取关键内容 → 写 syntheses/"""

    def __init__(self, cfg: dict | None = None):
        self.cfg = cfg or config()
        self.sources_dir = WIKI_SOURCES
        self.syntheses_dir = WIKI_SYNTHESES
        self.syntheses_dir.mkdir(parents=True, exist_ok=True)

    def _find_source(self, source_id: str) -> Path | None:
        """按 frontmatter id 字段找 source 文件"""
        if not self.sources_dir.exists():
            return None
        for f in self.sources_dir.glob("*.md"):
            if f.name.startswith("_"):
                continue
            content = f.read_text(encoding="utf-8")
            if field := _first(content, "id"):
                if field == source_id:
                    return f
        return None

    def _classify(self, content: str) -> str:
        """规则分类（不调 LLM）"""
        c = content.lower()
        if any(k in c for k in ("theorem", "theorem.", "conjecture", "lemma ", "proof of",
                                 "proposition", "证明", "定理", "推论", "命题")):
            return "theorem"
        if any(k in c for k in ("book chapter", "edited volume", "handbook", "monograph",
                                 "章节", "专著", "手册")):
            return "book"
        if any(k in c for k in ("arxiv:", "cond-mat", "hep-th", "hep-ph", "gr-qc",
                                 "astro-ph", "nucl-th", "quant-ph", "physics.ins-det")):
            return "preprint-physics"
        if "arxiv" in c and any(p in c for p in ("quantum", "hamiltonian", "schroedinger",
                                                   "schrödinger", "relativity", "cosmology",
                                                   "entanglement", "fermion", "boson")):
            return "preprint-physics"
        if any(k in c for k in ("综述", "review", "元分析", "meta-analysis")):
            return "review"
        if "preprint" in c or "arxiv" in c:
            return "preprint"
        if "report" in c or "报告" in c:
            return "report"
        return "paper"

    def _rate(self, content: str) -> str:
        """规则评级"""
        c = content.lower()
        if "meta-analysis" in c or "元分析" in c:
            return "5⭐"
        if "预注册" in c or "preregistered" in c:
            return "4⭐"
        return "3⭐"

    def _extract_pdf(self, pdf_path: str, ocr: bool = False) -> dict:
        """用 pypdf + 可选 pypdfium2 + tesseract 提结构化数据"""
        p = Path(pdf_path)
        if not p.exists():
            return {"success": False, "error": f"PDF not found: {pdf_path}"}
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(p))
            page_texts = [page.extract_text() or "" for page in reader.pages]
            result = {
                "success": True,
                "page_count": len(page_texts),
                "file_size_kb": p.stat().st_size / 1024,
                "page_texts": page_texts,
                "image_ocr": [],
            }
            if ocr and page_texts:
                try:
                    import pypdfium2 as pdfium
                    import subprocess
                    import tempfile
                    pdf = pdfium.PdfDocument(str(p))
                    for page_idx in range(len(pdf)):
                        page = pdf[page_idx]
                        bitmap = page.render(scale=1.5)
                        img = bitmap.to_pil()
                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                            img.save(tmp.name)
                            proc = subprocess.run(
                                ["tesseract", tmp.name, "-", "-l", "eng"],
                                capture_output=True, text=True, timeout=30,
                            )
                            if proc.stdout.strip():
                                result["image_ocr"].append({
                                    "page": page_idx + 1,
                                    "text": proc.stdout.strip()[:2000],
                                })
                except Exception as e:
                    result["image_ocr_error"] = str(e)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def summarize(
        self,
        source_id: str,
        output_path: str | None = None,
        pdf_path: str | None = None,
        ocr: bool = False,
    ) -> dict:
        """主入口：读 source → 分类 + 评级 + 提取 → 写 syntheses/

        Args:
            source_id: wiki source id（如 source.buzsaki-2002-hippocampal-theta）
            output_path: 自定义输出路径（可选）
            pdf_path: 本地 PDF（可选，触发 PDF 提取）
            ocr: 是否启用 OCR

        Returns:
            {success, output_path, zotero_key, paper_type, importance, pdf_data?}
        """
        source_file = self._find_source(source_id)
        if not source_file:
            return {"success": False, "error": f"source not found: {source_id}"}

        content = source_file.read_text(encoding="utf-8")
        meta, body = frontmatter(content)

        zk = meta.get("zotero_item_key") or ""
        zd = meta.get("zotero_doi") or ""
        title = meta.get("title", "") or source_id

        paper_type = self._classify(body)
        importance = self._rate(body)

        # 提取 "## 关键内容" 段
        notes_match = re.search(r"## 关键内容\s*\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ""

        if not output_path:
            date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            slug = source_id.replace("source.", "").replace(".", "-")
            output_path = self.syntheses_dir / f"{date}-summarize-{slug}.md"
        else:
            output_path = Path(output_path)

        md = f"""---
pageType: synthesis
id: synthesis.summarize.{source_id.replace('source.', '')}
title: Summarize — {title}
createdAt: "{datetime.now().isoformat(timespec='seconds')}"
zotero_refs:
  - key: {zk or 'PENDING'}
    role: primary
---

# {title} — 文献总结

> 来源：[[sources/{source_file.name}]]
> 总结时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 简化模式（规则分类 + 关键内容提取）

## 分类

| 字段 | 值 |
|---|---|
| 类型 | **{paper_type}** |
| 重要度 | **{importance}** |
| Zotero itemKey | `{zk or '未填'}` |
| Zotero DOI | `{zd or '未填'}` |

## 关键内容

{notes[:3000] or '（无）'}
"""

        pdf_section = ""
        if pdf_path:
            pdf_data = self._extract_pdf(pdf_path, ocr=ocr)
            if pdf_data.get("success"):
                page_count = pdf_data["page_count"]
                file_size = pdf_data["file_size_kb"]
                page_texts = pdf_data["page_texts"]
                full_text = "\n\n".join(
                    f"### 第 {i+1} 页\n```\n{t[:1000]}\n```" for i, t in enumerate(page_texts[:5])
                )
                image_ocr = pdf_data.get("image_ocr", [])
                ocr_text = "\n".join(
                    f"- 第 {o['page']} 页：{o['text'][:500]}" for o in image_ocr
                ) if image_ocr else "_未跑 OCR（加 --ocr 启动）_"
                pdf_section = f"""

## PDF 提取数据

> 本节为工具提取的原始数据，**攥写笔记 / 综述由 agent 完成**（本工具不攥写 narrative）。

### 元数据

| 字段 | 值 |
|------|-----|
| PDF 路径 | `{pdf_path}` |
| 页数 | {page_count} |
| 文件大小 | {file_size:.1f} KB |
| 解析器 | pypdf + pypdfium2 + tesseract |

### 全文（pypdf 提取）

{full_text}

### 图片 OCR（pypdfium2 + tesseract）

{ocr_text}
"""
            else:
                pdf_section = f"\n\n## PDF 提取数据\n\n❌ PDF 解析失败：{pdf_data.get('error')}\n"

        md += pdf_section
        md += f"\n## 提取时间\n\n{datetime.now().isoformat(timespec='seconds')}\n"
        output_path.write_text(md, encoding="utf-8")

        return {
            "success": True,
            "output_path": str(output_path),
            "zotero_key": zk,
            "paper_type": paper_type,
            "importance": importance,
            "notes_chars": len(notes),
            "pdf_data": pdf_data if pdf_path else None,
        }


def _first(content: str, key: str) -> str | None:
    """便捷函数：从 frontmatter 提取单字段"""
    meta, _ = frontmatter(content)
    return meta.get(key)
