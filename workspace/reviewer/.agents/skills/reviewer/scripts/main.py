#!/usr/bin/env python3
"""reviewer CLI 统一入口。"""

import sys
import os
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

# 单模块：直接导入并透传
from scripts.reviewer.ReviewChecklist import main as review_main


def main() -> int:
    return review_main()


if __name__ == "__main__":
    raise SystemExit(main())
