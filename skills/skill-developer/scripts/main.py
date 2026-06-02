#!/usr/bin/env python3
"""skill-developer CLI 统一入口。

三段式：`skill-developer <模块名> <方法名> [参数]`

模块（对象类）：
  skill   技能对象操作（init / check / audit / extend）

后续可扩展：
  reference   reference 文件对象（add / list / lint）
  script      script 文件对象（add / list）
  version     版本对象（bump / check）
"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

_MODULES = {
    "skill": "技能对象操作",
}


def main() -> int:
    # 无参数 → 打印总帮助
    if len(sys.argv) < 2:
        print("skill-developer - 技能开发元工具")
        print("用法: skill-developer <模块名> <方法名> [参数]")
        print("模块（对象类）:")
        for name, desc in _MODULES.items():
            print(f"  {name:<12}  {desc}")
        print("\n查看帮助: skill-developer <模块名> --help")
        return 0

    module = sys.argv[1]

    if module in ("-h", "--help"):
        print("skill-developer - 技能开发元工具")
        print("用法: skill-developer <模块名> <方法名> [参数]")
        print("模块（对象类）:")
        for name, desc in _MODULES.items():
            print(f"  {name:<12}  {desc}")
        print("\n查看帮助: skill-developer <模块名> --help")
        return 0

    if module not in _MODULES:
        print(f"Error: 未知模块 '{module}'")
        print(f"可用模块: {', '.join(_MODULES.keys())}")
        return 1

    # 派发到模块
    if module == "skill":
        from scripts.skill.cli import run as skill_run
        del sys.argv[1]
        return skill_run()
    else:
        # 未来扩展点
        print(f"Error: 模块 '{module}' 已注册但尚未实现")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
