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
| MCP 入口 | [mcp/server.py](mcp/server.py) | 工具暴露 |

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

    "mcp/server.py": """#!/usr/bin/env python3
\"\"\"
{skill_name} MCP Server
通过 MCP 暴露 {skill_name} 的工具方法
\"\"\"

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path("/root/.openclaw/skills/{skill_name}")

EXPOSED_TOOLS = [
    {{
        "name": "{skill_name}_do_something",
        "description": "执行 {skill_name} 的某个操作",
        "parameters": {{
            "type": "object",
            "properties": {{
                "action": {{
                    "type": "string",
                    "enum": ["do_something"],
                    "description": "要执行的操作"
                }}
            }},
            "required": ["action"]
        }}
    }}
]


class {handler_name}Handler:
    \"\"\"处理 {skill_name} 请求\"\"\"

    def __init__(self):
        self.skill_dir = SKILL_DIR

    async def handle_do_something(self, args: dict) -> dict:
        \"\"\"执行某个操作\"\"\"
        return {{"success": True, "message": "操作完成"}}


app = Server("{skill_name}")
handler = {handler_name}Handler()


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name=t["name"],
            description=t["description"],
            inputSchema=t["parameters"]
        )
        for t in EXPOSED_TOOLS
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    action = arguments.get("action")
    if action == "do_something":
        result = await handler.handle_do_something(arguments)
    else:
        result = {{"success": False, "error": f"未知操作: {{action}}"}}
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]


async def main():
    async with stdio_server(server=app) as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
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
        for d in ["assets/templates", "scripts", "references", "mcp"]:
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
            ("mcp/server.py", "mcp/server.py"),
        ]:
            content = _TEMPLATES[key].format(**vars_)
            (skill_path / rel_path).write_text(content, encoding="utf-8")

        print(f"\n✅ 技能初始化完成: {skill_path}")
        print(f"   - SKILL.md")
        print(f"   - scripts/  - references/  - mcp/server.py")
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




def main() -> int:
    skill = Skill()

    if len(sys.argv) < 3:
        print("用法:")
        print("  初始化: skill-developer init <skill-name> <description> [path] [emoji]")
        print("  自检:   skill-developer check <skill-path>")
        print("示例:")
        print("  skill-developer init my-skill \"这是一个测试技能\" ./my-skill 📦")
        print("  skill-developer check ./my-skill")
        return 1

    cmd = sys.argv[1]

    if cmd == "init":
        name = sys.argv[2]
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        path = sys.argv[4] if len(sys.argv) > 4 else f"./{name}"
        emoji = sys.argv[5] if len(sys.argv) > 5 else "📦"
        return skill.initialize(path, name, desc, emoji)

    if cmd == "check":
        path = sys.argv[2] if len(sys.argv) > 2 else "."
        return skill.check(path)

    print(f"未知命令: {cmd}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
