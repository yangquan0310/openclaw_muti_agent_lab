#!/usr/bin/env python3
"""
References 索引构建器（中央版）
扫描 references 目录，构建索引到 index/ 目录。
"""

import json
import re
import argparse
from pathlib import Path
from typing import Any


def extract_keywords_from_content(content: str) -> list[str]:
    """从内容中提取关键词"""
    code_terms = re.findall(r'(class|def|import|from)\s+(\w+)', content)
    terms = [t[1] for t in code_terms]
    bold_terms = re.findall(r'\*\*(.+?)\*\*', content)
    terms.extend(bold_terms)
    return list(set(terms))


def extract_sections(content: str) -> list[dict[str, Any]]:
    """提取章节结构"""
    sections = []
    for line in content.split('\n'):
        m = re.match(r'^(#{1,4})\s+(.+)$', line)
        if m:
            sections.append({"heading": m.group(2), "level": len(m.group(1))})
    return sections


def extract_frontmatter_keywords(content: str) -> list[str]:
    """从标题、表格、代码中提取关键词"""
    keywords = []
    headings = re.findall(r'^#{1,4}\s+(.+)$', content, re.MULTILINE)
    for h in headings:
        parens = re.findall(r'[（(]([^）)]+)[）)]', h)
        keywords.extend(parens)
        cleaned = re.sub(r'^[一二三四五六七八九十、\d.\s]+', '', h)
        cleaned = re.sub(r'[（(][^）)]+[）)]', '', cleaned)
        if len(cleaned) >= 2:
            keywords.append(cleaned)

    table_terms = re.findall(r'\|\s*([^|\n]+?)\s*\|[^\n]*\|', content)
    for t in table_terms:
        t = t.strip()
        if len(t) >= 2 and not t.startswith('-') and '---' not in t:
            keywords.append(t)

    code_terms = re.findall(r'\b(class|def|function)\s+(\w+)', content)
    for _, name in code_terms:
        keywords.append(name)

    seen = set()
    result = []
    for kw in keywords:
        kw = kw.strip()
        if len(kw) >= 2 and kw not in seen and not re.match(r'^[-*\d\s]+$', kw):
            seen.add(kw)
            result.append(kw)
    return result[:30]


def process_markdown_file(md_path: Path) -> dict[str, Any]:
    """处理单个 markdown 文件"""
    content = md_path.read_text(encoding='utf-8')

    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem

    description = ""
    in_frontmatter = False
    paragraph_count = 0
    for line in content.split('\n'):
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if line.startswith('#'):
            continue
        if line.strip() == '':
            continue
        if line.startswith('|'):
            continue
        paragraph_count += 1
        if paragraph_count == 1:
            description = line.strip()
            if len(description) > 100:
                description = description[:100] + "..."
            break

    sections = extract_sections(content)
    keywords = extract_frontmatter_keywords(content)

    return {
        "file": md_path.name,
        "title": title,
        "description": description,
        "keywords": keywords,
        "sections": sections
    }


def scan_references(references_dir: Path) -> dict[str, Any]:
    """扫描 references 目录"""
    if not references_dir.exists():
        print(f"Error: {references_dir} does not exist")
        return {}

    manifest = {}
    for md_file in references_dir.glob("*.md"):
        if md_file.name == "index.md":
            continue
        try:
            data = process_markdown_file(md_file)
            manifest[md_file.stem] = data
            print(f"  ✓ {md_file.name}")
        except Exception as e:
            print(f"  ✗ {md_file.name}: {e}")
    return manifest


def build_chunks(references_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """构建内容块（按 ## 章节分割）"""
    chunks = []
    for md_file in references_dir.glob("*.md"):
        if md_file.name == "index.md":
            continue

        content = md_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        current_heading = ""
        current_level = 0
        current_content = []

        for line in lines:
            m = re.match(r'^(#{1,4})\s+(.+)$', line)
            if m:
                if current_content and current_heading:
                    chunk_text = '\n'.join(current_content).strip()
                    if chunk_text:
                        chunks.append({
                            "id": f"{md_file.stem}_{len(chunks):03d}",
                            "file": md_file.name,
                            "heading": current_heading,
                            "level": current_level,
                            "content_preview": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text,
                            "full_content": chunk_text
                        })
                current_heading = m.group(2)
                current_level = len(m.group(1))
                current_content = []
            else:
                current_content.append(line)

        if current_content and current_heading:
            chunk_text = '\n'.join(current_content).strip()
            if chunk_text:
                chunks.append({
                    "id": f"{md_file.stem}_{len(chunks):03d}",
                    "file": md_file.name,
                    "heading": current_heading,
                    "level": current_level,
                    "content_preview": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text,
                    "full_content": chunk_text
                })
    return chunks


def main():
    parser = argparse.ArgumentParser(description='构建 References 索引')
    parser.add_argument('--references', '-r', required=True,
                        help='references 目录路径')
    parser.add_argument('--index', '-i',
                        help='输出索引目录路径（默认：<references>/../index）')
    args = parser.parse_args()

    references_dir = Path(args.references).resolve()
    if not references_dir.exists():
        print(f"Error: references 目录不存在: {references_dir}")
        return 1

    index_dir = Path(args.index).resolve() if args.index else references_dir.parent / "index"
    index_dir.mkdir(parents=True, exist_ok=True)

    skill_name = references_dir.parent.name

    print(f"【{skill_name}】索引构建")
    print(f"  来源: {references_dir}")
    print(f"  输出: {index_dir}")

    manifest = scan_references(references_dir)
    chunks = build_chunks(references_dir, manifest)

    manifest_path = index_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    chunks_path = index_dir / "chunks.json"
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"\n  文件索引: {len(manifest)}")
    print(f"  内容块:   {len(chunks)}")
    print(f"  完成!")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())