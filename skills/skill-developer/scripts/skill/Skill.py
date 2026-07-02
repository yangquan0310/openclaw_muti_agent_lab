#!/usr/bin/env python3
"""
skill-developer 核心模块
提供技能初始化和自检能力
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Any


_MAIN_PY_TEMPLATE = r'''#!/usr/bin/env python3
"""
{skill_name} CLI 统一入口（✨ 本技能的**唯一入口**）。

三段式调用规范：
    python scripts/main.py <模块名> <方法名> [参数]

模块（对象类）：
  （请在下方 _MODULES 注册你的模块）

添加新模块的步骤：
  1. 在 scripts/<模块名>/ 下创建模块文件（实现类或函数）
  2. 在下方 _MODULES 字典中注册 "模块名": ("描述", "scripts.模块名.cli:run")
  3. 模块文件需提供 run() 函数作为 CLI 入口
"""

import sys
from pathlib import Path

_SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_ROOT))

# 模块注册表：模块名 → (描述, 派发器导入路径)
_MODULES: dict = {{
    # 示例："my_module": ("模块描述", "scripts.my_module.cli:run"),
}}


def _print_help() -> None:
    """打印顶层帮助"""
    print("{skill_name} - 技能 CLI")
    print("用法: python scripts/main.py <模块名> <方法名> [参数]")
    print()
    print("模块（对象类）:")
    for name, (desc, _) in _MODULES.items():
        print(f"  {{name:<12}}  {{desc}}")
    if not _MODULES:
        print("  （暂无已注册模块）")
    print()
    print("查看模块帮助: python scripts/main.py <模块名> --help")


def _dispatch(module: str) -> int:
    """派发到指定模块的 CLI 调度器"""
    if module not in _MODULES:
        print(f"Error: 未知模块 '{{module}}'")
        print(f"可用模块: {{', '.join(_MODULES.keys()) or '(暂无)'}}")
        return 1

    _, import_path = _MODULES[module]
    module_path, _, attr = import_path.partition(":")

    try:
        import importlib
        mod = importlib.import_module(module_path)
        run = getattr(mod, attr)
    except ImportError as e:
        print(f"Error: 模块 '{{module}}' 已注册但加载失败: {{e}}")
        return 1
    except AttributeError:
        print(f"Error: 模块 '{{module}}' 缺少入口函数 '{{attr}}'")
        return 1

    del sys.argv[1]
    return run()


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        _print_help()
        return 0
    return _dispatch(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())
'''

_TEMPLATES = {
    "SKILL.md": """---
name: {skill_name}
description: >
  {description}
version: 1.0.0
author: Yang Quan
metadata:
  openclaw:
    emoji: {emoji}
    requires:
      bins: []
---

# {skill_name}

> {description}

---

## 触发条件

当用户提到「」时触发。

---

## 模块导航

| 模块 | 位置 | 说明 |
|------|------|------|
| 指南 | [references/guide.md](references/guide.md) | 详细使用说明 |

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | {date} | 初始版本 |
""",

    "references/index.md": """# {skill_name}

> {description}

---

## 快速开始

开发新技能时，使用 [skill-developer](~/.openclaw/skills/skill-developer/SKILL.md) 技能。
""",
}


class Skill:
    """技能初始化与自检核心类"""

    def __init__(self, skill_dir: Path = None):
        self.skill_dir = skill_dir or Path("/root/.openclaw/skills")
        self._date = datetime.now().strftime("%Y-%m-%d")

    # ── 核心方法 ─────────────────────────────────────

    def initialize(
        self,
        skill_path: str | Path,
        skill_name: str,
        description: str,
        emoji: str = "📦",
    ) -> int:
        """初始化新技能目录结构"""
        skill_path = Path(skill_path)

        if skill_path.exists() and any(skill_path.iterdir()):
            print(f"⚠️  目录已存在且非空: {skill_path}")
            response = input("继续覆盖？ (y/N): ")
            if response.lower() != "y":
                print("取消初始化")
                return 1

        # 目录结构
        for d in ["assets/templates", "scripts", "references"]:
            (skill_path / d).mkdir(parents=True, exist_ok=True)

        # 模板文件
        vars_ = {
            "skill_name": skill_name,
            "handler_name": "".join(p.title() for p in skill_name.replace("-", "_").split("_")),
            "description": description,
            "emoji": emoji,
            "date": self._date,
        }
        for rel_path, key in [
            ("SKILL.md", "SKILL.md"),
            ("references/index.md", "references/index.md"),
        ]:
            content = _TEMPLATES[key].format(**vars_)
            (skill_path / rel_path).write_text(content, encoding="utf-8")

        # 生成 scripts/main.py（唯一入口）
        main_py = skill_path / "scripts" / "main.py"
        main_py.write_text(_MAIN_PY_TEMPLATE.format(**vars_), encoding="utf-8")
        main_py.chmod(0o755)

        print(f"\n✅ 技能初始化完成: {skill_path}")
        print(f"   - SKILL.md")
        print(f"   - scripts/  - references/")
        print(f"   - assets/templates/")
        print(f"\n   自检：skill-developer check {skill_path}")
        return 0

    def check(self, skill_path: str | Path) -> int:
        """执行自检并打印结果"""
        skill_path = Path(skill_path)
        print(f"\n🔍 开始自检: {skill_path}\n" + "=" * 50)

        pass_, fail, warn = [], [], []
        self._check_structure(skill_path, pass_, fail, warn)
        self._check_naming(skill_path, pass_, fail, warn)

        for label, items in [("✅ 通过", pass_), ("❌ 失败", fail), ("⚠️  警告", warn)]:
            if items:
                print(f"\n【{label}】")
                for m in items:
                    print(f"  {m}")

        total_pass, total_fail, total_warn = len(pass_), len(fail), len(warn)
        print("\n" + "=" * 50)
        print(f"📊 自检结果: ✅ {total_pass} | ❌ {total_fail} | ⚠️ {total_warn}")

        if total_fail > 0:
            print("\n🔴 自检未通过，请修复以上 ❌ 问题")
            return 1
        elif total_warn > 0:
            print("\n🟡 自检通过但有警告")
            return 0
        print("\n🟢 自检完全通过")
        return 0

    def audit(self, skill_path: str | Path) -> int:
        """严格审计：结构 + 命名 + CLI 入口 + 全局 symlink + 版本号"""
        skill_path = Path(skill_path)
        print(f"\n📋 开始审计: {skill_path}\n" + "=" * 50)

        pass_, fail, warn = [], [], []
        self._check_structure(skill_path, pass_, fail, warn)
        self._check_naming(skill_path, pass_, fail, warn)
        self._check_cli_entry(skill_path, pass_, fail, warn)
        self._check_global_symlink(skill_path, pass_, fail, warn)
        self._check_version(skill_path, pass_, fail, warn)

        for label, items in [("✅ 通过", pass_), ("❌ 失败", fail), ("⚠️  警告", warn)]:
            if items:
                print(f"\n【{label}】")
                for m in items:
                    print(f"  {m}")

        total_pass, total_fail, total_warn = len(pass_), len(fail), len(warn)
        print("\n" + "=" * 50)
        print(f"📊 审计结果: ✅ {total_pass} | ❌ {total_fail} | ⚠️ {total_warn}")

        if total_fail > 0:
            return 1
        return 0

    def extend(
        self,
        skill_path: str | Path,
        reference: str | None = None,
        script: str | None = None,
    ) -> int:
        """扩展现有技能（添加 reference 或 script）"""
        skill_path = Path(skill_path)
        if not skill_path.exists():
            print(f"❌ 技能目录不存在: {skill_path}")
            return 1

        if reference:
            ref_path = skill_path / "references" / reference
            ref_path.parent.mkdir(parents=True, exist_ok=True)
            ref_path.write_text(
                f"# {reference.removesuffix('.md')}\n\n待补充内容。\n",
                encoding="utf-8",
            )
            print(f"✅ 添加 reference: {ref_path}")

        if script:
            scr_path = skill_path / "scripts" / script
            scr_path.parent.mkdir(parents=True, exist_ok=True)
            scr_path.write_text(
                f"#!/usr/bin/env python3\n# {script} - 待补充\n",
                encoding="utf-8",
            )
            scr_path.chmod(0o755)
            print(f"✅ 添加 script: {scr_path}")

        if not (reference or script):
            print("⚠️  extend 需要 --reference 或 --script 参数")
            return 1

        print(f"\n💡 下一步：编辑 {skill_path} 下的新文件")
        return 0

    # ── 自检子方法 ───────────────────────────────────

    def _check_structure(self, p: Path, pass_: list, fail: list, warn: list) -> None:
        (pass_ if (p / "SKILL.md").exists() else fail).append(
            f"必选文件{'存在' if (p / "SKILL.md").exists() else '缺失'}: SKILL.md"
        )
        for d in ["scripts", "references", "assets"]:
            (pass_ if (p / d).exists() else warn).append(f"目录{'存在' if (p / d).exists() else '缺失'}: {d}/")

    def _check_naming(self, p: Path, pass_: list, fail: list, warn: list) -> None:
        for f in p.rglob("*.py"):
            for m in re.finditer(r"class (\w+)", f.read_text()):
                ok = not (m.group(1).islower() or "_" in m.group(1))
                (pass_ if ok else fail).append(f"类名{'规范' if ok else '不规范'}: {m.group(1)} ({f.relative_to(p)})")
        md = p / "SKILL.md"
        if md.exists():
            lines = md.read_text().split("\n")
            ok = len(lines) <= 200
            (pass_ if ok else warn).append(f"SKILL.md {'合理' if ok else '过长'}: {len(lines)}行")

    def _check_cli_entry(self, p: Path, pass_: list, fail: list, warn: list) -> None:
        """检查 scripts/main.py 是否存在且支持三段式 CLI（软提示）"""
        main = p / "scripts" / "main.py"

        if not main.exists():
            warn.append(
                "CLI 入口缺失: scripts/main.py"
                "（所有技能必须提供 python scripts/main.py <模块> <方法> <参数> 三段式入口）"
            )
            return

        pass_.append("CLI 入口存在: scripts/main.py")

        # 检查是否支持三段式（通过关键字识别）
        try:
            content = main.read_text(encoding="utf-8")
        except Exception:
            warn.append("CLI 入口无法读取: scripts/main.py")
            return

        indicators = ["_MODULES", "_dispatch", "sys.argv[1]"]
        missing = [ind for ind in indicators if ind not in content]

        if missing:
            warn.append(
                f"CLI 入口可能不支持三段式: 缺少标识 {missing}，"
                f"建议参考 skill-developer 的 scripts/main.py 重写"
            )
        else:
            pass_.append("CLI 入口支持三段式调度: scripts/main.py")

    def _check_global_symlink(self, p: Path, pass_: list, fail: list, warn: list) -> None:
        """检查 /usr/local/bin/ 下是否有 symlink"""
        # 从 SKILL.md 提取技能名
        skill_md = p / "SKILL.md"
        if not skill_md.exists():
            return
        import re as _re
        m = _re.search(r"^name:\s*(\S+)", skill_md.read_text(), _re.MULTILINE)
        if not m:
            return
        name = m.group(1)
        link = Path(f"/usr/local/bin/{name}")
        if link.exists() or link.is_symlink():
            pass_.append(f"全局 symlink 已配置: {link}")
        else:
            warn.append(f"全局 symlink 缺失: {link} (运行: ln -s {p/'scripts/main.py'} {link})")

    def _check_version(self, p: Path, pass_: list, fail: list, warn: list) -> None:
        """检查 SKILL.md 的 version 字段"""
        skill_md = p / "SKILL.md"
        if not skill_md.exists():
            return
        import re as _re
        m = _re.search(r"^version:\s*(\S+)", skill_md.read_text(), _re.MULTILINE)
        if not m:
            fail.append("SKILL.md 缺少 version 字段")
            return
        ver = m.group(1)
        # 简单 semver 检查
        if _re.match(r"^\d+\.\d+\.\d+", ver):
            pass_.append(f"version 合规: {ver}")
        else:
            fail.append(f"version 不符合 semver: {ver}")
