#!/usr/bin/env python3
"""
fortunetelling 统一 CLI 入口

Usage:
    fortunetelling bazi  year month day hour [--gender 男|女] [--lunar]
    fortunetelling lunar year month day  [--hour]
    fortunetelling fate  year month day hour [--gender] [--type dayun|timing]
                                              [--target YYYY-MM-DD-HH]
                                              [--start-year YYYY] [--end-year YYYY]
"""

import sys
import argparse
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.bazi  import main as bazi_main
from scripts.lunar import main as lunar_main
from scripts.fate  import main as fate_main


def main():
    if len(sys.argv) < 2:
        # 无子命令时打印整体帮助
        _parser = argparse.ArgumentParser(
            prog='fortunetelling',
            description='八字命理工具集'
        )
        _parser.print_help()
        print("\n子命令:")
        print("  bazi  八字排盘")
        print("  lunar 阴历转公历")
        print("  fate  运势分析")
        print("\n详细帮助: fortunetelling <子命令> --help")
        return 0

    subcmd = sys.argv[1]

    # 真正删除子命令参数，让子模块的 argparse 看到干净的 sys.argv
    del sys.argv[1]

    if subcmd == 'bazi':
        sys.argv[0] = 'fortunetelling bazi'
        return bazi_main()

    elif subcmd == 'lunar':
        sys.argv[0] = 'fortunetelling lunar'
        return lunar_main()

    elif subcmd == 'fate':
        sys.argv[0] = 'fortunetelling fate'
        return fate_main()

    else:
        print(f"Error: 未知子命令 '{subcmd}'")
        print("可用: bazi, lunar, fate")
        return 1


if __name__ == '__main__':
    sys.exit(main())
