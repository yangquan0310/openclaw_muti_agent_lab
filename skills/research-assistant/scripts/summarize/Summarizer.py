#!/usr/bin/env python3
"""
WikiSummesizer.py - summarize 模块接入 wiki 后端（v5.16.0）
- 输入：wiki source 替代 index.json
- 输出：wiki syntheses/<date>-summarize-<id>.md
- 简化：不做 LLM 调用（避免费用/API key 风险），按规则做 type 分类 + notes 提取
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any


class Summarizer:
    """从 wiki source 读，summarize 输出到 wiki syntheses/"""

    def __init__(self, wiki_path: str = '~/.openclaw/wiki'):
        self.wiki_path = Path(wiki_path).expanduser()
        self.sources_dir = self.wiki_path / 'sources'
        self.syntheses_dir = self.wiki_path / 'syntheses'
        self.syntheses_dir.mkdir(parents=True, exist_ok=True)

    def _find_source(self, source_id: str) -> Optional[Path]:
        for candidate in self.sources_dir.glob(f"*{source_id}*"):
            if candidate.suffix == '.md' and not candidate.name.startswith('_'):
                return candidate
        for f in self.sources_dir.glob('*.md'):
            if f.name.startswith('_'):
                continue
            content = f.read_text(encoding='utf-8')
            m = re.search(r'^id:\s*(\S+)', content, re.MULTILINE)
            if m and m.group(1) == source_id:
                return f
        return None

    def _classify_type(self, content: str) -> str:
        """根据正文内容规则分类（不调 LLM）

        v6.0.5+：加了 theorem / preprint-physics / book 三类
        （支撑老板数/物/心交叉研究场景，psychologist 痛点 4）

        优先级：theorem > book > preprint-physics > review > preprint > report > paper
        顺序很重要——专项标记优先于通用类
        """
        content_lower = content.lower()

        # 1. theorem（数学定理类，含 conjecture / lemma / proof）
        if any(kw in content_lower for kw in (
            'theorem', 'theorem.', 'conjecture', 'lemma ', 'proof of',
            'proposition', '证明', '定理', '推论', '命题',
        )):
            return 'theorem'

        # 2. book（书籍类）
        if any(kw in content_lower for kw in (
            'book chapter', 'edited volume', 'handbook', 'monograph',
            '章节', '专著', '手册',
        )):
            return 'book'

        # 3. preprint-physics（物理预印本，区分于通用 preprint）
        # 启发式：arxiv + 物理分类关键词
        if any(kw in content_lower for kw in (
            'arxiv:', 'cond-mat', 'hep-th', 'hep-ph', 'gr-qc', 'astro-ph',
            'nucl-th', 'quant-ph', 'physics.ins-det',
        )):
            return 'preprint-physics'
        if 'arxiv' in content_lower and any(phys in content_lower for phys in (
            'quantum', 'hamiltonian', 'schroedinger', 'schrödinger',
            'relativity', 'cosmology', 'entanglement', 'fermion', 'boson',
        )):
            return 'preprint-physics'

        # 4. review / preprint / report / paper（v6.0.4 原有）
        if '综述' in content or 'review' in content_lower or '元分析' in content or 'meta-analysis' in content_lower:
            return 'review'
        if 'preprint' in content or 'arxiv' in content_lower:
            return 'preprint'
        if 'report' in content_lower or '报告' in content:
            return 'report'
        return 'paper'

    def _calc_importance(self, content: str) -> str:
        """根据内容估算重要度（5⭐/4⭐/3⭐/2⭐）"""
        if 'meta-analysis' in content.lower() or '元分析' in content:
            return '5⭐'
        if '5 个研究' in content or 'n=709' in content or '多研究' in content:
            return '4⭐'
        if '预注册' in content or 'preregistered' in content.lower():
            return '4⭐'
        return '3⭐'

    def read_pdf(self, pdf_path: str, do_ocr: bool = False) -> Dict[str, Any]:
        """读取本地 PDF 提取结构化数据（v6.0.2+ 工具能力）

        使用工具（已装在 conda base / 系统）：
        - pypdf：文本提取（秒级）
        - pypdfium2：渲染页面为 PNG（可选，给 OCR 用）
        - tesseract：OCR 图片（系统命令，可选）

        参数：
          pdf_path: 本地 PDF 文件路径
          do_ocr: 是否对每页渲染后 OCR（默认 False，只提文本）

        返回：
          {
            'success': bool,
            'page_count': int,
            'file_size_kb': float,
            'page_texts': [str, ...],     # 每页文本（pypdf）
            'image_ocr': [...],           # OCR 结果（仅 do_ocr=True）
            'error': str                  # 仅 success=False
          }
        """
        from pathlib import Path
        try:
            pdf_p = Path(pdf_path)
            if not pdf_p.exists():
                return {'success': False, 'error': f'PDF not found: {pdf_path}'}
            from pypdf import PdfReader
            reader = PdfReader(str(pdf_p))
            page_texts = [p.extract_text() or '' for p in reader.pages]
            result = {
                'success': True,
                'page_count': len(page_texts),
                'file_size_kb': pdf_p.stat().st_size / 1024,
                'page_texts': page_texts,
                'image_ocr': [],
            }
            if do_ocr and page_texts:
                try:
                    import pypdfium2 as pdfium
                    import subprocess, tempfile
                    pdf = pdfium.PdfDocument(str(pdf_p))
                    for page_idx in range(len(pdf)):
                        page = pdf[page_idx]
                        bitmap = page.render(scale=1.5)
                        img = bitmap.to_pil()
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                            img.save(tmp.name)
                            ocr_proc = subprocess.run(
                                ['tesseract', tmp.name, '-', '-l', 'eng'],
                                capture_output=True, text=True, timeout=30
                            )
                            if ocr_proc.stdout.strip():
                                result['image_ocr'].append({
                                    'page': page_idx + 1,
                                    'text': ocr_proc.stdout.strip()[:2000]
                                })
                except Exception as e:
                    result['image_ocr_error'] = str(e)
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def summarize(self, source_id: str, output_path: Optional[str] = None,
                  pdf_path: Optional[str] = None, do_ocr: bool = False) -> Dict[str, Any]:
        """从单个 wiki source 读，做 summarize（简化版），输出到 wiki syntheses/"""
        source_file = self._find_source(source_id)
        if not source_file:
            return {"success": False, "error": f"source not found: {source_id}"}

        content = source_file.read_text(encoding='utf-8')

        # 解析 YAML
        yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        yaml_text = yaml_match.group(1) if yaml_match else ''
        body = content[yaml_match.end():] if yaml_match else content

        # 提取字段
        zk_match = re.search(r'^zotero_item_key:\s*(\S+)', yaml_text, re.MULTILINE)
        zotero_key = zk_match.group(1) if zk_match else None
        doi_match = re.search(r'^zotero_doi:\s*(\S+)', yaml_text, re.MULTILINE)
        zotero_doi = doi_match.group(1) if doi_match else None
        title_match = re.search(r'^title:\s*"?([^"\n]+)"?', yaml_text, re.MULTILINE)
        wiki_title = title_match.group(1) if title_match else ''

        # 分类 + 重要度
        paper_type = self._classify_type(body)
        importance = self._calc_importance(body)

        # 提取 notes 段
        notes_match = re.search(r'## 关键内容\s*\n(.*?)(?=\n## |\Z)', body, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ''

        # 输出路径
        if not output_path:
            date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            slug = source_id.replace('source.', '').replace('.', '-')
            output_path = self.syntheses_dir / f"{date}-summarize-{slug}.md"
        else:
            output_path = Path(output_path)

        summary_md = f"""---
pageType: synthesis
id: synthesis.summarize.{source_id.replace('source.', '')}
title: Summarize — {wiki_title or source_id}
createdAt: "{datetime.now().isoformat(timespec='seconds')}"
zotero_refs:
  - key: {zotero_key or 'PENDING'}
    role: primary
---

# {wiki_title or source_id} — 文献总结

> 来源：[[sources/{source_file.name}]]
> 总结时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 简化模式（不调 LLM，规则分类 + 关键内容提取）

## 分类

| 字段 | 值 |
|---|---|
| 类型 | **{paper_type}** |
| 重要度 | **{importance}** |
| Zotero itemKey | `{zotero_key or '未填'}` |
| Zotero DOI | `{zotero_doi or '未填'}` |

## 关键内容

{notes[:3000] or '（无）'}
"""
        # v6.0.2+：PDF 提取数据（如指定 --pdf-path）
        pdf_section = ''
        if pdf_path:
            pdf_data = self.read_pdf(pdf_path, do_ocr=do_ocr)
            if pdf_data.get('success'):
                page_count = pdf_data['page_count']
                file_size = pdf_data['file_size_kb']
                page_texts = pdf_data['page_texts']
                # 只嵌每页前 1000 字符 + 全文总长度
                full_text_preview = '\n\n'.join([
                    f'### 第 {i+1} 页\n```\n{t[:1000]}\n```' for i, t in enumerate(page_texts[:5])
                ])
                image_ocr = pdf_data.get('image_ocr', [])
                ocr_text = '\n'.join([
                    f'- 第 {o["page"]} 页：{o["text"][:500]}' for o in image_ocr
                ]) if image_ocr else '_未跑 OCR（加 --ocr 启动）_'
                pdf_section = f'''

## PDF 提取数据（v6.0.2+ 工具能力）

> 本节为工具提取的原始数据，**攥写笔记 / 综述由 agent 完成**（本工具不攥写 narrative）。

### 元数据

| 字段 | 值 |
|------|-----|
| PDF 路径 | `{pdf_path}` |
| 页数 | {page_count} |
| 文件大小 | {file_size:.1f} KB |
| 解析器 | pypdf + pypdfium2 + tesseract |

### 全文（pypdf 提取）

{full_text_preview}

### 图片 OCR（pypdfium2 + tesseract）

{ocr_text}
'''
            else:
                pdf_section = f'\n\n## PDF 提取数据（v6.0.2+）\n\n❌ PDF 解析失败：{pdf_data.get("error")}\n'

        summary_md += pdf_section
        summary_md += f"\n## 提取时间\n\n{datetime.now().isoformat(timespec='seconds')}\n"
        output_path.write_text(summary_md, encoding='utf-8')

        return {
            "success": True,
            "output_path": str(output_path),
            "zotero_key": zotero_key,
            "paper_type": paper_type,
            "importance": importance,
            "notes_chars": len(notes),
            "pdf_data": pdf_data if pdf_path else None,
        }


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('用法: python3 WikiSummesizer.py summarize <wiki-source-id>')
        sys.exit(1)
    s = WikiSummesizer()
    if sys.argv[1] == 'summarize':
        result = s.summarize(sys.argv[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print('未知命令')
