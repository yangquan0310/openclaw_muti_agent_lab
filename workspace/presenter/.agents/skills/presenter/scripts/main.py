#!/usr/bin/env python3
"""presenter 技能 CLI 统一入口。

三段式：`presenter <模块名> <方法名> [参数]`

模块（对象类）：
  ppt    PPT 后处理（**不是 python-pptx**——纯 zipfile XML 操作）
    ├─ template.decorate   一站式母版装饰
    ├─ template.add-header 加顶部色条
    ├─ template.add-accent 加左侧色条
    ├─ template.set-cover  改封面布局
    ├─ template.set-fonts  改 CJK / Latin 字体
    ├─ template.set-theme-colors 改主题色
    └─ tables.style        样式化所有表格
"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

_MODULES = {
    "ppt": "PPT 后处理（母版装饰 / 表格样式）",
}


def main() -> int:
    # 无参数 → 打印总帮助
    if len(sys.argv) < 2:
        print("presenter - 视觉传达设计师技能")
        print("用法: presenter <模块名> <方法名> [参数]")
        print("模块（对象类）:")
        for name, desc in _MODULES.items():
            print(f"  {name:<10}  {desc}")
        print("\n查看帮助: presenter <模块名> <方法名> --help")
        return 0

    module = sys.argv[1]

    if module in ("-h", "--help"):
        print("presenter - 视觉传达设计师技能")
        print("用法: presenter <模块名> <方法名> [参数]")
        print("模块（对象类）:")
        for name, desc in _MODULES.items():
            print(f"  {name:<10}  {desc}")
        print("\n查看帮助: presenter <模块名> <方法名> --help")
        return 0

    if module not in _MODULES:
        print(f"Error: 未知模块 '{module}'")
        print(f"可用模块: {', '.join(_MODULES.keys())}")
        return 1

    # 派发到模块
    if module == "ppt":
        from scripts.ppt.cli import run as ppt_run
        del sys.argv[1]
        return ppt_run()
    else:
        # 未来扩展点
        print(f"Error: 模块 '{module}' 已注册但尚未实现")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
