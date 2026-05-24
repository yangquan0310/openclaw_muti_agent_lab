#!/usr/bin/env python3
"""writer CLI 统一入口。"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

# 单模块：直接导入并透传
from scripts.writer.Selfcheck import main as selfcheck_main


def main() -> int:
    return selfcheck_main()


if __name__ == "__main__":
    raise SystemExit(main())
