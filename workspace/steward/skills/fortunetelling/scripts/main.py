#!/usr/bin/env python3
"""fortunetelling CLI 统一入口。"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.bazi  import main as bazi_main
from scripts.lunar import main as lunar_main
from scripts.fate  import main as fate_main


def main() -> int:
    # 全局 -h 在子命令之前处理
    if "-h" in sys.argv or "--help" in sys.argv:
        print("fortunetelling - 八字命理工具集")
        print("用法: fortunetelling <子命令> [选项]")
        print("子命令:")
        print("  bazi  八字排盘")
        print("  lunar 阴历转公历")
        print("  fate  运势分析")
        print("\n详细帮助: fortunetelling <子命令> --help")
        return 0

    if len(sys.argv) < 2:
        print("fortunetelling - 八字命理工具集")
        print("用法: fortunetelling <子命令> [选项]")
        print("子命令: bazi, lunar, fate")
        print("\n详细帮助: fortunetelling <子命令> --help")
        return 0

    subcmd = sys.argv[1]
    del sys.argv[1]

    if subcmd == "bazi":
        sys.argv[0] = "fortunetelling bazi"
        return bazi_main()
    elif subcmd == "lunar":
        sys.argv[0] = "fortunetelling lunar"
        return lunar_main()
    elif subcmd == "fate":
        sys.argv[0] = "fortunetelling fate"
        return fate_main()
    else:
        print(f"Error: 未知子命令 '{subcmd}'")
        print("可用: bazi, lunar, fate")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
