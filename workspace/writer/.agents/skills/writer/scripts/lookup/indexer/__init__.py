"""索引构建器包"""

from .Indexer import (
    extract_keywords_from_content,
    extract_sections,
    extract_frontmatter_keywords,
    process_markdown_file,
    scan_dir,
    scan_references,
    scan_references_recursive,
    scan_templates,
    build_chunks_from_dir,
    build_chunks_recursive,
    build_chunks,
    main,
)

__all__ = [
    "extract_keywords_from_content",
    "extract_sections",
    "extract_frontmatter_keywords",
    "process_markdown_file",
    "scan_dir",
    "scan_references",
    "scan_references_recursive",
    "scan_templates",
    "build_chunks_from_dir",
    "build_chunks_recursive",
    "build_chunks",
    "main",
]


if __name__ == "__main__":
    main()
