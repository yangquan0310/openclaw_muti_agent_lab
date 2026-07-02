#!/usr/bin/env python3
"""
skill-developer CLI 统一入口（✨ 本技能的**唯一入口**）。

三段式调用规范：
    python scripts/main.py <模块名> <方法名> [参数]

模块（对象类）：
  skill   技能对象操作（init / check / audit / extend）

添加新模块的步骤：
  1. 在 scripts/<模块名>/ 下创建模块文件（实现类或函数）
  2. 在下方 _MODULES 字典中注册："<模块名>": ("<描述>", "<导入路径>")
  3. （可选）在 _METHODS 字典中声明该模块支持的方法列表，便于自动生成帮助

添加新方法只需在对应模块文件中实现，由模块自身的 CLI 调度器负责解析参数。
main.py 只负责：解析 <模块> → 派发到模块 CLI → 不关心具体方法。
"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

# 模块注册表：模块名 → (描述, 派发器导入路径)
# 派发器必须提供 run() 函数，参数从 sys.argv[2:] 开始
_MODULES: dict[str, tuple[str, str]] = {
    "skill": ("技能对象操作", "scripts.skill.cli:run"),
}


def _print_help() -> None:
    """打印顶层帮助"""
    print("skill-developer - 技能开发元工具")
    print("用法: python scripts/main.py <模块名> <方法名> [参数]")
    print()
    print("模块（对象类）:")
    for name, (desc, _) in _MODULES.items():
        print(f"  {name:<12}  {desc}")
    print()
    print("查看模块帮助: python scripts/main.py <模块名> --help")
    print()
    print("提示: scripts/main.py 是本技能的唯一入口，")
    print("      任何模块/方法的调用都必须经过本文件。")


def _dispatch(module: str) -> int:
    """派发到指定模块的 CLI 调度器"""
    if module not in _MODULES:
        print(f"Error: 未知模块 '{module}'")
        print(f"可用模块: {', '.join(_MODULES.keys())}")
        return 1

    _, import_path = _MODULES[module]
    module_path, _, attr = import_path.partition(":")

    try:
        # 动态导入模块文件
        import importlib
        mod = importlib.import_module(module_path)
        run = getattr(mod, attr)
    except ImportError as e:
        print(f"Error: 模块 '{module}' 已注册但加载失败: {e}")
        print(f"  请检查 {module_path} 是否存在")
        return 1
    except AttributeError:
        print(f"Error: 模块 '{module}' 缺少入口函数 '{attr}'")
        return 1

    # 把 <模块> 从 argv 中剔除，让模块 CLI 看到干净的 [方法, 参数...]
    del sys.argv[1]
    return run()


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        _print_help()
        return 0

    return _dispatch(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())