#!/usr/bin/env python3
"""manager CLI 统一入口。

用法: manager <模块> <子命令> [选项]

模块:
  maintainer  项目整理（organize/sync-templates/check-updates/maintain/move/meta）
  workboard   Workboard 任务发布/管理（list/read/create/claim/heartboard/release/...）
"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

_MODULES = {
    "maintainer": "项目整理",
    "workboard": "Workboard 任务发布/管理",
}


def main() -> int:
    # 无参数 → 打印总帮助
    if len(sys.argv) < 2:
        print("manager - 多模块管理工具")
        print("用法: manager <模块> <子命令> [选项]")
        print("模块:")
        for name, desc in _MODULES.items():
            print(f"  {name:<12}  {desc}")
        print("\n查看帮助: manager <模块> --help")
        return 0

    module = sys.argv[1]

    if module in ("-h", "--help"):
        print("manager - 多模块管理工具")
        print("用法: manager <模块> <子命令> [选项]")
        print("模块:")
        for name, desc in _MODULES.items():
            print(f"  {name:<12}  {desc}")
        print("\n查看帮助: manager <模块> --help")
        return 0

    if module == "maintainer":
        from scripts.maintainer.Maintainer import main as mnt_main
        del sys.argv[1]
        return mnt_main()
    elif module == "workboard":
        from scripts.workboard.cli import main as wb_main
        del sys.argv[1]
        return wb_main()
    else:
        print(f"Error: 未知模块 '{module}'")
        print("可用模块:", ", ".join(_MODULES.keys()))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
