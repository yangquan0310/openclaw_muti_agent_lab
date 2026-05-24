#!/usr/bin/env python3
"""
lookup - 中央 References 搜索与索引工具

Usage:
    lookup search [--skill <name>] [--path <path>] <query>  搜索指南
    lookup index --skill <name> | --path <path>            构建索引
    lookup list [--skill <name>] [--path <path>]          列出已索引文件

    lookup --help                                   显示本帮助
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
    if getattr(args, 'skill', None):
        sys.argv.extend(['--skill', args.skill])
    elif getattr(args, 'path', None):
        sys.argv.extend(['--path', args.path])
    if getattr(args, 'files_only', False):
        sys.argv.extend(['--files-only'])
    if getattr(args, 'list', False):
        sys.argv.extend(['--list'])
    if getattr(args, 'top', None):
        sys.argv.extend(['--top', str(args.top)])
    return searcher_main()


def cmd_index(args):
    from scripts.indexer import main as indexer_main
    sys.argv = ['indexer']
    if args.skill:
        sys.argv.extend(['--skill', args.skill])
    elif args.path:
        sys.argv.extend(['--path', args.path])
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
    p_search.add_argument('--skill',
                          help='技能名（默认 programmer）')
    p_search.add_argument('--path',
                          help='技能根目录路径（与 --skill 二选一）')
    p_search.add_argument('--files-only', '-f', action='store_true',
                          help='只显示文件匹配')
    p_search.add_argument('--list', '-l', action='store_true',
                          help='列出所有已索引文件')
    p_search.add_argument('--top', '-k', type=int, default=5,
                          help='返回结果数（默认 5）')

    # lookup index
    p_index = subparsers.add_parser('index', help='构建索引')
    p_index.add_argument('--skill',
                         help='技能名（如 programmer, mathematician）')
    p_index.add_argument('--path',
                         help='技能根目录路径（与 --skill 二选一）')

    # lookup list
    p_list = subparsers.add_parser('list', help='列出已索引文件')
    p_list.add_argument('--skill',
                        help='技能名（默认 programmer）')
    p_list.add_argument('--path',
                        help='技能根目录路径（与 --skill 二选一）')

    args = parser.parse_args()

    if args.command == 'search':
        return cmd_search(args)
    elif args.command == 'index':
        return cmd_index(args)
    elif args.command == 'list':
        # list 复用 searcher 的 --list 功能
        args.query = None
        args.list = True
        # 确保 list 命令也有 files_only 属性
        args.files_only = False
        return cmd_search(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
