#!/usr/bin/env python3
"""
Physicist References 索引构建器
扫描 references 目录，提取元数据，构建 manifest.json
"""

import json
import re
from pathlib import Path
from typing import Any


def extract_keywords_from_content(content: str) -> list[str]:
    """从内容中提取关键词"""
    # 提取代码中的关键术语
    code_terms = re.findall(r'(class|def|import|from)\s+(\w+)', content)
    terms = [t[1] for t in code_terms]
    
    # 提取加粗/高亮的术语
    bold_terms = re.findall(r'\*\*(.+?)\*\*', content)
    terms.extend(bold_terms)
    
    # 去重
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
    
    # 1. 从标题中提取（## 标题中的核心词）
    headings = re.findall(r'^#{1,4}\s+(.+)$', content, re.MULTILINE)
    for h in headings:
        # 提取括号中的英文
        parens = re.findall(r'[（(]([^）)]+)[）)]', h)
        keywords.extend(parens)
        # 提取核心词（去掉序号和符号）
        cleaned = re.sub(r'^[一二三四五六七八九十、\d.\s]+', '', h)
        cleaned = re.sub(r'[（(][^）)]+[）)]', '', cleaned)
        if len(cleaned) >= 2:
            keywords.append(cleaned)
    
    # 2. 从表格中提取术语（第一列）
    table_terms = re.findall(r'\|\s*([^|\n]+?)\s*\|[^\n]*\|', content)
    for t in table_terms:
        t = t.strip()
        if len(t) >= 2 and not t.startswith('-') and '---' not in t:
            keywords.append(t)
    
    # 3. 从代码模式中提取类名/函数名
    code_terms = re.findall(r'\b(class|def|function)\s+(\w+)', content)
    for _, name in code_terms:
        keywords.append(name)
    
    # 去重并过滤
    seen = set()
    result = []
    for kw in keywords:
        kw = kw.strip()
        # 过滤太短的、无意义的
        if len(kw) >= 2 and kw not in seen and not re.match(r'^[-*\d\s]+$', kw):
            seen.add(kw)
            result.append(kw)
    
    return result[:30]  # 限制数量


def process_markdown_file(md_path: Path) -> dict[str, Any]:
    """处理单个 markdown 文件"""
    content = md_path.read_text(encoding='utf-8')
    
    # 提取标题（第一个 # 标题）
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem
    
    # 提取描述（第二个段落）
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
    
    # 提取章节
    sections = extract_sections(content)
    
    # 提取关键词
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
                # 保存之前的块
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
        
        # 保存最后一个块
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
    # 获取 skill 根目录
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent.parent
    references_dir = skill_dir / "references"
    output_dir = script_dir / "index"
    
    print(f"Scanning references: {references_dir}")
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 扫描 references
    manifest = scan_references(references_dir)
    
    # 构建 chunks
    chunks = build_chunks(references_dir, manifest)
    
    # 保存 manifest
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Manifest saved: {manifest_path}")
    
    # 保存 chunks
    chunks_path = output_dir / "chunks.json"
    with open(chunks_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"Chunks saved: {chunks_path}")
    
    print(f"\nSummary:")
    print(f"  Files indexed: {len(manifest)}")
    print(f"  Chunks created: {len(chunks)}")


if __name__ == "__main__":
    main()
