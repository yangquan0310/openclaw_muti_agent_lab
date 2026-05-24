#!/usr/bin/env python3
"""skill-developer CLI：技能开发入口。"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.init import init_skill


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="skill-developer CLI")
    sub = parser.add_subparsers(dest="command", help="子命令")

    # init：初始化新技能
    init_parser = sub.add_parser("init", help="初始化新技能目录结构")
    init_parser.add_argument("skill-name", help="技能名称（kebab-case）")
    init_parser.add_argument("description", help="技能描述")
    init_parser.add_argument("path", nargs="?", help="安装路径（默认 ./技能名）")
    init_parser.add_argument("emoji", nargs="?", default="📦", help="表情符号（默认 📦）")
    init_parser.set_defaults(func=_run_init)

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 1
    return args.func(args)


def _run_init(args) -> int:
    skill_path = args.path or f"./{args.skill_name}"
    return init_skill(
        skill_path=skill_path,
        skill_name=args.skill_name,
        description=args.description,
        emoji=args.emoji,
    )


if __name__ == "__main__":
    sys.exit(main())
