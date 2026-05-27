#!/usr/bin/env python3
"""manager CLI 统一入口。

用法: manager maintainer <子命令> [选项]

模块:
  maintainer  项目整理（organize/sync-templates/check-updates/maintain/move/meta）
"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))


def main() -> int:
    # 无参数 → 打印总帮助
    if len(sys.argv) < 2:
        print("manager - 项目整理工具")
        print("用法: manager maintainer <子命令> [选项]")
        print("模块:")
        print("  maintainer  项目整理")
        print("\n查看帮助: manager maintainer --help")
        return 0

    # manager maintainer <subcmd>
    if sys.argv[1] == "maintainer":
        from scripts.maintainer.Maintainer import main as mnt_main
        del sys.argv[1]  # 去掉 maintainer，让 Maintainer.py 看到干净的子命令
        return mnt_main()
    else:
        # -h/--help 或未知模块
        if sys.argv[1] in ("-h", "--help"):
            print("manager - 项目整理工具")
            print("用法: manager maintainer <子命令> [选项]")
            print("模块:")
            print("  maintainer  项目整理")
            print("\n查看帮助: manager maintainer --help")
            return 0
        print(f"Error: 未知模块 '{sys.argv[1]}'")
        print("可用模块: maintainer")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
