#!/usr/bin/env python3
"""physicist CLI 统一入口。"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.calculate import main as calculate_main
from scripts.visualize import main as visualize_main


def main() -> int:
    if "-h" in sys.argv or "--help" in sys.argv:
        print("physicist - 物理工具集")
        print("用法: physicist <子命令> [选项]")
        print("子命令:")
        print("  calculate  数值计算（基本运算/矩阵/积分/ODE）")
        print("  visualize  物理可视化（函数图/相轨迹/场分布/3D表面）")
        print("\n详细帮助: physicist <子命令> --help")
        return 0

    if len(sys.argv) < 2:
        print("physicist - 物理工具集")
        print("用法: physicist <子命令> [选项]")
        print("子命令:")
        print("  calculate  数值计算")
        print("  visualize  物理可视化")
        print("\n详细帮助: physicist <子命令> --help")
        return 0

    subcmd = sys.argv[1]
    del sys.argv[1]

    if subcmd == "calculate":
        sys.argv[0] = "physicist calculate"
        return calculate_main()
    elif subcmd == "visualize":
        sys.argv[0] = "physicist visualize"
        return visualize_main()
    else:
        print(f"Error: 未知子命令 '{subcmd}'")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
