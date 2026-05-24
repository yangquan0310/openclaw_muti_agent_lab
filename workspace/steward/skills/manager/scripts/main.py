#!/usr/bin/env python3
"""manager CLI 统一入口。"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.maintainer.Maintainer import main as maintainer_main


def main() -> int:
    # 无参数时打印总帮助
    if len(sys.argv) == 1:
        print("manager - 项目整理工具")
        print("用法: manager <子命令> [选项]")
        print("子命令:")
        print("  organize        整理项目文件（默认）")
        print("  sync-templates  同步模板文件")
        print("  check-updates  检查项目文档是否需要更新")
        print("  maintain       维护项目元数据和结构")
        print("  move           移动文件到标准目录")
        print("  meta           元数据管理")
        print("\n详细帮助: manager <子命令> --help")
        return 0

    return maintainer_main()


if __name__ == "__main__":
    raise SystemExit(main())
