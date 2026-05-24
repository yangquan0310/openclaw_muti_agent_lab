#!/usr/bin/env python3
"""skill-developer CLI：技能开发入口。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.skill.Skill import Skill


def main() -> int:
    skill = Skill()

    if len(sys.argv) < 3:
        print("用法:")
        print("  初始化: python scripts/main.py init <skill-name> <description> [path] [emoji]")
        print("  自检:   python scripts/main.py check <skill-path>")
        print("示例:")
        print("  python scripts/main.py init my-skill \"这是一个测试技能\" ./my-skill 📦")
        print("  python scripts/main.py check ./my-skill")
        return 1

    cmd = sys.argv[1]

    if cmd == "init":
        name = sys.argv[2]
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        path = sys.argv[4] if len(sys.argv) > 4 else f"./{name}"
        emoji = sys.argv[5] if len(sys.argv) > 5 else "📦"
        return skill.initialize(path, name, desc, emoji)

    elif cmd == "check":
        path = sys.argv[2] if len(sys.argv) > 2 else "."
        return skill.check(path)

    else:
        print(f"未知命令: {cmd}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
