#!/usr/bin/env python3
"""
lookup - 中央 References 搜索与索引工具

Usage:
    lookup search -i <index> <query>          搜索指南
    lookup index  -r <references> [-i <path>] 构建索引
    lookup list   -i <index>                  列出已索引文件
"""

import sys
import argparse
from pathlib import Path

# 确保 lookup 自身模块可导入
_sys_path = Path(__file__).resolve().parent.parent
if str(_sys_path) not in sys.path:
    sys.path.insert(0, str(_sys_path))


def cmd_search(args):
    from scripts.searcher import main as searcher_main
    sys.argv = ['searcher']
    if args.query:
        sys.argv.append(args.query)
    sys.argv.extend(['--index', args.index])
    if args.files_only:
        sys.argv.extend(['--files-only'])
    if args.list:
        sys.argv.extend(['--list'])
    if getattr(args, 'top', None):
        sys.argv.extend(['--top', str(args.top)])
    return searcher_main()


def cmd_index(args):
    from scripts.indexer import main as indexer_main
    sys.argv = ['indexer', '--references', args.references]
    if args.index:
        sys.argv.extend(['--index', args.index])
    return indexer_main()


def main():
    parser = argparse.ArgumentParser(
        description='lookup - 中央 References 搜索与索引工具',
        usage='lookup <command> [options]\n\n'
              'Commands:\n'
              '  search -i <index> <query>   搜索指南\n'
              '  index  -r <references> [-i]  构建索引\n'
              '  list   -i <index>            列出已索引文件\n\n'
              'Examples:\n'
              '  lookup search -i ./skill/index 工作流\n'
              '  lookup index  -r ./skill/references\n'
              '  lookup list   -i ~/.openclaw/skills/lark-base/index\n'
              '  lookup index  -r ./skill/references -i /tmp/my-index\n'
              '  lookup search -i /tmp/my-index/manifest.json 工作流\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # lookup search
    p_search = subparsers.add_parser('search', help='搜索指南')
    p_search.add_argument('query', nargs='?', help='搜索关键词')
    p_search.add_argument('-i', '--index', required=True,
                          help='索引目录路径（或 manifest.json 路径）')
    p_search.add_argument('--files-only', '-f', action='store_true',
                          help='只显示文件匹配')
    p_search.add_argument('--list', '-l', action='store_true',
                          help='列出所有已索引文件')
    p_search.add_argument('--top', '-k', type=int, default=5,
                          help='返回结果数（默认 5）')

    # lookup index
    p_index = subparsers.add_parser('index', help='构建索引')
    p_index.add_argument('-r', '--references', required=True,
                         help='references 目录路径')
    p_index.add_argument('-i', '--index',
                          help='输出索引目录路径（默认：<references>/../index）')

    # lookup list
    p_list = subparsers.add_parser('list', help='列出已索引文件')
    p_list.add_argument('-i', '--index', required=True,
                        help='索引目录路径（或 manifest.json 路径）')

    args = parser.parse_args()

    if args.command == 'search':
        return cmd_search(args)
    elif args.command == 'index':
        return cmd_index(args)
    elif args.command == 'list':
        args.query = None
        args.list = True
        args.files_only = False
        return cmd_search(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())