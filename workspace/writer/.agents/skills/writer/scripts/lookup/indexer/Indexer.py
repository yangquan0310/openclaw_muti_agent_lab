#!/usr/bin/env python3
"""
Skill 索引构建器
扫描 references + assets/templates 目录，提取元数据，构建 manifest.json
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


def scan_dir(dir_path: Path, category: str, skip_index: bool = True) -> dict[str, Any]:
    """扫描指定目录（单层）"""
    if not dir_path.exists():
        print(f"Info: {dir_path} does not exist, skipping")
        return {}
    
    manifest = {}
    
    for md_file in dir_path.glob("*.md"):
        if skip_index and md_file.name == "index.md":
            continue
        
        try:
            data = process_markdown_file(md_file)
            key = f"{category}/{md_file.stem}"
            data['category'] = category
            manifest[key] = data
            print(f"Indexed [{category}]: {md_file.name}")
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")
    
    return manifest


def scan_references_recursive(references_dir: Path) -> dict[str, Any]:
    """递归扫描 references 目录及其子目录"""
    manifest = {}
    
    if not references_dir.exists():
        print(f"Info: {references_dir} does not exist, skipping")
        return manifest
    
    # 获取所有子目录
    subdirs = [d for d in references_dir.iterdir() if d.is_dir()]
    
    # 扫描根目录（guide.md, index.md）
    for md_file in references_dir.glob("*.md"):
        try:
            data = process_markdown_file(md_file)
            key = f"references/{md_file.stem}"
            data['category'] = 'references'
            manifest[key] = data
            print(f"Indexed [references]: {md_file.name}")
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")
    
    # 扫描子目录
    for subdir in subdirs:
        category = f"references/{subdir.name}"
        for md_file in subdir.glob("*.md"):
            try:
                data = process_markdown_file(md_file)
                key = f"references/{subdir.name}/{md_file.stem}"
                data['category'] = category
                manifest[key] = data
                print(f"Indexed [{category}]: {md_file.name}")
            except Exception as e:
                print(f"Error processing {md_file.name}: {e}")
    
    return manifest


def scan_references(references_dir: Path) -> dict[str, Any]:
    """扫描 references 目录（兼容模式）"""
    # 检查是否有子目录
    has_subdirs = any(d.is_dir() for d in references_dir.iterdir())
    if has_subdirs:
        return scan_references_recursive(references_dir)
    return scan_dir(references_dir, "references")


def scan_templates(templates_dir: Path) -> dict[str, Any]:
    """扫描 templates 目录"""
    return scan_dir(templates_dir, "templates", skip_index=False)


def build_chunks_from_dir(dir_path: Path, category: str) -> list[dict[str, Any]]:
    """从指定目录构建 chunks"""
    chunks = []
    
    for md_file in dir_path.glob("*.md"):
        if category == "references" and md_file.name == "index.md":
            continue
        
        content = md_file.read_text(encoding='utf-8')
        filename = f"{category}/{md_file.stem}"
        
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


def build_chunks_recursive(references_dir: Path) -> list[dict[str, Any]]:
    """递归构建 references 的 chunks"""
    chunks = []
    
    # 根目录 chunks
    chunks.extend(build_chunks_from_dir(references_dir, "references"))
    
    # 子目录 chunks
    for subdir in references_dir.iterdir():
        if subdir.is_dir():
            category = f"references/{subdir.name}"
            chunks.extend(build_chunks_from_dir(subdir, category))
    
    return chunks


def build_chunks(references_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """构建 references 的 chunks"""
    # 检查是否有子目录
    has_subdirs = any(d.is_dir() for d in references_dir.iterdir())
    if has_subdirs:
        return build_chunks_recursive(references_dir)
    return build_chunks_from_dir(references_dir, "references")


def main():
    """主入口"""
    # 获取 skill 根目录
    script_dir = Path(__file__).parent.parent
    skill_dir = script_dir.parent.parent
    references_dir = skill_dir / "references"
    templates_dir = skill_dir / "assets" / "templates"
    output_dir = script_dir / "index"
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 扫描 references
    manifest = scan_references(references_dir)
    
    # 扫描 templates
    templates_manifest = scan_templates(templates_dir)
    manifest.update(templates_manifest)
    
    # 构建 chunks
    chunks = build_chunks(references_dir, manifest)
    chunks.extend(build_chunks_from_dir(templates_dir, "templates"))
    
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
