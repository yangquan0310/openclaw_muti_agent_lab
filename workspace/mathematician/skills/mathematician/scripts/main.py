#!/usr/bin/env python3
"""mathematician CLI 统一入口。"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.calculate import main as calculate_main
from scripts.statistics import main as statistics_main
from scripts.visualize import main as visualize_main


def main() -> int:
    # 全局 -h 在子命令之前处理
    if "-h" in sys.argv or "--help" in sys.argv:
        print("mathematician - 数学工具集")
        print("用法: mathematician <子命令> [选项]")
        print("子命令:")
        print("  calculate   数值计算（基本运算/矩阵/积分/ODE/求根/插值）")
        print("  statistics  统计分析（描述统计/假设检验/回归/时间序列）")
        print("  visualize   数据可视化（统计图表/函数绘图/分布图）")
        print("\n详细帮助: mathematician <子命令> --help")
        return 0

    if len(sys.argv) < 2:
        print("mathematician - 数学工具集")
        print("用法: mathematician <子命令> [选项]")
        print("子命令:")
        print("  calculate   数值计算")
        print("  statistics  统计分析")
        print("  visualize   数据可视化")
        print("\n详细帮助: mathematician <子命令> --help")
        return 0

    subcmd = sys.argv[1]
    del sys.argv[1]

    if subcmd == "calculate":
        sys.argv[0] = "mathematician calculate"
        return calculate_main()
    elif subcmd == "statistics":
        sys.argv[0] = "mathematician statistics"
        return statistics_main()
    elif subcmd == "visualize":
        sys.argv[0] = "mathematician visualize"
        return visualize_main()
    else:
        print(f"Error: 未知子命令 '{subcmd}'")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
