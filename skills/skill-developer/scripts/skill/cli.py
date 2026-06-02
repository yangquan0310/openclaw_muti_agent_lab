#!/usr/bin/env python3
"""
scripts/skill/cli.py - skill-developer skill 模块的 CLI 调度

三段式调用：`skill-developer skill <方法> <参数>`
支持方法：init / check / audit / extend
"""

import argparse
import sys
from pathlib import Path

# 让 import scripts.skill.Skill 能找到
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.skill.Skill import Skill


def build_parser() -> argparse.ArgumentParser:
    """构建 skill 模块的 argparse"""
    parser = argparse.ArgumentParser(
        prog="skill-developer skill",
        description="技能对象操作（init / check / audit / extend）",
    )
    sub = parser.add_subparsers(dest="method", required=True, metavar="<方法>")

    # init - 创建新技能
    p = sub.add_parser("init", help="创建新技能（init 已有参数：name desc [path] [emoji]）")
    p.add_argument("name", help="技能名（小写连字符）")
    p.add_argument("description", help="技能描述")
    p.add_argument("path", nargs="?", default=None, help="目标路径（默认 ./<name>）")
    p.add_argument("emoji", nargs="?", default="📦", help="emoji 图标（默认 📦）")

    # check - 自检
    p = sub.add_parser("check", help="自检（结构 + 命名）")
    p.add_argument("path", help="技能路径")

    # audit - 严格审计
    p = sub.add_parser("audit", help="严格审计（结构 + 命名 + CLI 入口 + symlink + 版本）")
    p.add_argument("path", help="技能路径")

    # extend - 扩展
    p = sub.add_parser("extend", help="扩展现有技能")
    p.add_argument("path", help="技能路径")
    p.add_argument("--reference", metavar="FILE", help="添加 reference 文件（如 foo.md）")
    p.add_argument("--script", metavar="FILE", help="添加 script 文件（如 foo.py）")

    return parser


def run() -> int:
    """skill 模块 CLI 入口"""
    parser = build_parser()
    args = parser.parse_args()
    skill = Skill()

    if args.method == "init":
        path = args.path or f"./{args.name}"
        return skill.initialize(path, args.name, args.description, args.emoji)
    elif args.method == "check":
        return skill.check(args.path)
    elif args.method == "audit":
        return skill.audit(args.path)
    elif args.method == "extend":
        return skill.extend(
            args.path,
            reference=args.reference,
            script=args.script,
        )

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(run())
