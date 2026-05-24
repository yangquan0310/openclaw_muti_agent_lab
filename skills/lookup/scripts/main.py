#!/usr/bin/env python3
"""
lookup - 中央 References 搜索与索引工具

Usage:
    lookup search [--skill <name>] <query>        搜索指南
    lookup index --skill <name>                   构建索引
    lookup list [--skill <name>]                  列出已索引文件
    lookup --help                                 显示本帮助
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
    # 重构 sys.argv 传给 searcher
    sys.argv = ['searcher']
    if args.query:
        sys.argv.append(args.query)
    if args.skill:
        sys.argv.extend(['--skill', args.skill])
    if args.files_only:
        sys.argv.extend(['--files-only'])
    if args.list:
        sys.argv.extend(['--list'])
    if args.top:
        sys.argv.extend(['--top', str(args.top)])
    return searcher_main()


def cmd_index(args):
    from scripts.indexer import main as indexer_main
    sys.argv = ['indexer', '--skill', args.skill]
    return indexer_main()


def main():
    parser = argparse.ArgumentParser(
        description='lookup - 中央 References 搜索与索引工具',
        usage='lookup <command> [--skill <name>] [options]\n\n'
              'Commands:\n'
              '  search [--skill <name>] <query>   搜索指南\n'
              '  index --skill <name>              构建索引\n'
              '  list [--skill <name>]             列出已索引文件\n\n'
              'Examples:\n'
              '  lookup search --skill programmer 设计模式\n'
              '  lookup index --skill mathematician\n'
              '  lookup list --skill programmer\n'
              '  lookup list                         # 默认 programmer',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # lookup search
    p_search = subparsers.add_parser('search', help='搜索指南')
    p_search.add_argument('query', nargs='?', help='搜索关键词')
    p_search.add_argument('--skill', default='programmer',
                          help='技能名（默认 programmer）')
    p_search.add_argument('--files-only', '-f', action='store_true',
                          help='只显示文件匹配')
    p_search.add_argument('--list', '-l', action='store_true',
                          help='列出所有已索引文件')
    p_search.add_argument('--top', '-k', type=int, default=5,
                          help='返回结果数（默认 5）')

    # lookup index
    p_index = subparsers.add_parser('index', help='构建索引')
    p_index.add_argument('--skill', required=True,
                         help='技能名（如 programmer, mathematician）')

    # lookup list
    p_list = subparsers.add_parser('list', help='列出已索引文件')
    p_list.add_argument('--skill', default='programmer',
                        help='技能名（默认 programmer）')

    args = parser.parse_args()

    if args.command == 'search':
        return cmd_search(args)
    elif args.command == 'index':
        return cmd_index(args)
    elif args.command == 'list':
        # list 复用 searcher 的 --list 功能
        args.query = None
        args.list = True
        return cmd_search(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
