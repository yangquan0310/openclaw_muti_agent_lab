#!/usr/bin/env python3
"""presenter CLI 统一入口。"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

from scripts.ppt.main import main as ppt_main


def main() -> int:
    return ppt_main()


if __name__ == "__main__":
    raise SystemExit(main())
