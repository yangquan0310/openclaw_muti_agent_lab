"""搜索引擎包"""

from pathlib import Path
from typing import Any

from .Searcher import ReferencesSearcher


def format_results(results: dict[str, Any]) -> str:
    """格式化输出"""
    output = []

    output.append(f"\n🔍 查询: {results['query']}")
    output.append("=" * 60)

    if not results['files']:
        output.append("\n❌ 没有找到相关内容")
        return '\n'.join(output)

    # 显示文件匹配
    output.append("\n📚 相关指南:")
    for i, file_data in enumerate(results['files'], 1):
        score_stars = "★" * int(file_data['score'] * 5) + "☆" * (5 - int(file_data['score'] * 5))
        output.append(f"\n{i}. {file_data['title']}")
        output.append(f"   文件: {file_data['file']}")
        output.append(f"   匹配度: {score_stars} ({file_data['score']:.2f})")
        output.append(f"   描述: {file_data['description']}")

    # 显示章节块
    if results['chunks']:
        output.append("\n\n📖 相关章节:")
        for chunk in results['chunks']:
            output.append(f"\n▶ {chunk['heading']}")
            output.append(f"  文件: {chunk['file']}")
            if 'content_preview' in chunk:
                preview = chunk['content_preview'][:150]
                if len(chunk['content_preview']) > 150:
                    preview += "..."
                output.append(f"  预览: {preview}")

    output.append("\n")
    return '\n'.join(output)


def main():
    """主入口"""
    import argparse

    parser = argparse.ArgumentParser(description='搜索 programmer 技术指南')
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--files-only', '-f', action='store_true', help='只显示文件匹配')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有已索引的文件')

    args = parser.parse_args()

    # 获取 skill 目录
    script_dir = Path(__file__).parent  # lookup/
    skill_dir = script_dir.parent.parent

    # 检查索引
    index_dir = script_dir / "index"
    if not (index_dir / "manifest.json").exists():
        print("❌ 索引不存在，请先运行索引构建器:")
        print(f"   python3 -m scripts.lookup.indexer")
        return

    searcher = ReferencesSearcher(skill_dir)

    # 列出文件
    if args.list:
        print("\n📚 已索引的指南:")
        print("=" * 60)
        for filename, data in searcher.manifest.items():
            print(f"\n• {data['title']}")
            print(f"  文件: {data['file']}")
            print(f"  关键词: {', '.join(data['keywords'][:5])}...")
        print()
        return

    # 搜索
    if not args.query:
        parser.print_help()
        return

    results = searcher.search(args.query, show_chunks=not args.files_only)
    print(format_results(results))


__all__ = [
    "ReferencesSearcher",
    "format_results",
    "main",
]


if __name__ == "__main__":
    main()
