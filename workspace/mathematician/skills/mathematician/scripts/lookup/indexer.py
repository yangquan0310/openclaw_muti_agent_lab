#!/usr/bin/env python3
"""
Mathematician References 索引构建器
扫描 references 目录，提取元数据，构建 manifest.json
"""

import json
import re
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
    lines = content.split('\n')
    
    for line in lines:
        m = re.match(r'^(#{1,4})\s+(.+)$', line)
        if m:
            sections.append({
                "heading": m.group(2),
                "level": len(m.group(1))
            })
    
    return sections


def extract_frontmatter_keywords(content: str) -> list[str]:
    """从标题、表格、代码中提取关键词"""
    keywords = []
    
    # 从标题中提取
    headings = re.findall(r'^#{1,4}\s+(.+)$', content, re.MULTILINE)
    for h in headings:
        parens = re.findall(r'[（(]([^）)]+)[）)]', h)
        keywords.extend(parens)
        cleaned = re.sub(r'^[一二三四五六七八九十、\d.\s]+', '', h)
        cleaned = re.sub(r'[（(][^）)]+[）)]', '', cleaned)
        if len(cleaned) >= 2:
            keywords.append(cleaned)
    
    # 从表格中提取术语
    table_terms = re.findall(r'\|\s*([^|\n]+?)\s*\|[^\n]*\|', content)
    for t in table_terms:
        t = t.strip()
        if len(t) >= 2 and not t.startswith('-') and '---' not in t:
            keywords.append(t)
    
    # 从代码模式中提取类名/函数名
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
    
    lines = content.split('\n')
    description = ""
    in_frontmatter = False
    paragraph_count = 0
    
    for line in lines:
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
            print(f"Indexed: {md_file.name}")
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")
    
    return manifest


def build_chunks(references_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """构建内容块（按 ## 章节分割）"""
    chunks = []
    
    for md_file in references_dir.glob("*.md"):
        if md_file.name == "index.md":
            continue
        
        content = md_file.read_text(encoding='utf-8')
        filename = md_file.stem
        
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
                            "id": f"{filename}_{len(chunks):03d}",
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
                    "id": f"{filename}_{len(chunks):03d}",
                    "file": md_file.name,
                    "heading": current_heading,
                    "level": current_level,
                    "content_preview": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text,
                    "full_content": chunk_text
                })
    
    return chunks


def main():
    """主入口"""
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent.parent
    references_dir = skill_dir / "references"
    output_dir = script_dir / "index"
    
    print(f"Scanning references: {references_dir}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    manifest = scan_references(references_dir)
    chunks = build_chunks(references_dir, manifest)
    
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Manifest saved: {manifest_path}")
    
    chunks_path = output_dir / "chunks.json"
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"Chunks saved: {chunks_path}")
    
    print(f"\nSummary:")
    print(f"  Files indexed: {len(manifest)}")
    print(f"  Chunks created: {len(chunks)}")


if __name__ == "__main__":
    main()
