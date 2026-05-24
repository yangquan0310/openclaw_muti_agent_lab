#!/usr/bin/env python3
"""
lookup - 中央 References 搜索与索引工具

Usage:
    lookup search -i <manifest.json> <query>                     搜索指南
    lookup index  -r <references> [-m <manifest>] [-c <chunks>] 构建索引
    lookup list   -i <manifest.json>                             列出已索引文件
"""

import sys
import argparse
from pathlib import Path

_sys_path = Path(__file__).resolve().parent.parent
if str(_sys_path) not in sys.path:
    sys.path.insert(0, str(_sys_path))


def cmd_search(args):
    from scripts.searcher.Searcher import main as searcher_main
    sys.argv = ['searcher']
    if args.query:
        sys.argv.append(args.query)
    sys.argv.extend(['--index', args.index])
    if getattr(args, 'files_only', False):
        sys.argv.extend(['--files-only'])
    if getattr(args, 'list', False):
        sys.argv.extend(['--list'])
    if getattr(args, 'top', None):
        sys.argv.extend(['--top', str(args.top)])
    return searcher_main()


def cmd_index(args):
    from scripts.indexer.Indexer import main as indexer_main
    sys.argv = ['indexer', '-r', args.references]
    if args.manifest:
        sys.argv.extend(['-m', args.manifest])
    if args.chunks:
        sys.argv.extend(['-c', args.chunks])
    return indexer_main()


def main():
    parser = argparse.ArgumentParser(
        prog='lookup',
        description='lookup - 中央 References 搜索与索引工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # lookup search
    p_search = subparsers.add_parser('search', help='搜索指南')
    p_search.add_argument('query', nargs='?', help='搜索关键词')
    p_search.add_argument('-i', '--index', required=True,
                          help='manifest.json 文件路径')
    p_search.add_argument('-f', '--files-only', action='store_true',
                          help='只显示文件匹配')
    p_search.add_argument('-l', '--list', action='store_true',
                          help='列出所有已索引文件')
    p_search.add_argument('-k', '--top', type=int, default=5,
                          help='返回结果数（默认 5）')

    # lookup index
    p_index = subparsers.add_parser('index', help='构建索引')
    p_index.add_argument('-r', '--references', required=True,
                         help='references 目录路径')
    p_index.add_argument('-m', '--manifest',
                         help='manifest.json 输出路径（默认：<references>/../index/manifest.json）')
    p_index.add_argument('-c', '--chunks',
                         help='chunks.json 输出路径（默认：与 manifest 同目录）')

    # lookup list
    p_list = subparsers.add_parser('list', help='列出已索引文件')
    p_list.add_argument('-i', '--index', required=True,
                        help='manifest.json 文件路径')

    args = parser.parse_args()

    if args.command == 'search':
        return cmd_search(args)
    elif args.command == 'index':
        return cmd_index(args)
    elif args.command == 'list':
        from scripts.searcher.Searcher import main as searcher_main
        sys.argv = ['searcher', '--list', '--index', args.index]
        return searcher_main()
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
