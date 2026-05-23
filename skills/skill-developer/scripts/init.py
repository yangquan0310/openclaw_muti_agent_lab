#!/usr/bin/env python3
"""
初始化脚本 - 创建新技能目录结构（含 MCP 暴露）
自检清单在 skill-developer 自有 assets/ 中，不复制到新技能
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def init_skill(skill_path, skill_name, description, emoji="📦"):
    """初始化新技能"""
    skill_path = Path(skill_path)
    date = datetime.now().strftime("%Y-%m-%d")

    if skill_path.exists() and any(skill_path.iterdir()):
        print(f"⚠️ 目录已存在且非空: {skill_path}")
        response = input("继续覆盖？ (y/N): ")
        if response.lower() != "y":
            print("取消初始化")
            return 1

    skill_path.mkdir(parents=True, exist_ok=True)

    # 创建目录结构
    dirs = [
        "assets/templates",
        "scripts",
        "references",
        "mcp",
    ]
    for d in dirs:
        (skill_path / d).mkdir(parents=True, exist_ok=True)

    # _meta.json
    meta = {
        "name": skill_name,
        "version": "1.0.0",
        "description": description,
        "entry_point": "mcp/server.py",
        "triggers": [],
        "dependencies": [],
        "author": "Yang Quan"
    }
    (skill_path / "_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False)
    )

    # SKILL.md
    skill_md = f"""---
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

> 💡 自检脚本：`skill-developer/scripts/selfcheck.py`
> 💡 自检清单：`skill-developer/assets/templates/selfcheck-checklist.md`
> 💡 创建后使用 skill-developer 技能对照自检。

---

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.0.0 | {date} | 初始版本 |
"""
    (skill_path / "SKILL.md").write_text(skill_md)

    # README.md
    readme_md = f"""# {skill_name}

{description}

---

## 快速开始

完成开发后，使用 skill-developer 技能进行自检。

---

## MCP 暴露

scripts/ 下的方法通过 mcp/server.py 暴露为 MCP 工具。

---

## 目录结构

```
{skill_name}/
├── SKILL.md
├── README.md
├── _meta.json
├── assets/templates/
├── scripts/
├── mcp/
│   └── server.py
└── references/
```
"""
    (skill_path / "README.md").write_text(readme_md)

    # mcp/server.py
    mcp_server = f"""#!/usr/bin/env python3
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


class {skill_name.title().replace("-", "_")}Handler:
    \"\"\"处理 {skill_name} 请求\"\"\"

    def __init__(self):
        self.skill_dir = SKILL_DIR

    async def handle_do_something(self, args: dict) -> dict:
        \"\"\"执行某个操作\"\"\"
        return {{"success": True, "message": "操作完成"}}


app = Server("{skill_name}")
handler = {skill_name.title().replace("-", "_")}Handler()


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
""".format(skill_name)

    (skill_path / "mcp/server.py").write_text(mcp_server)

    # guide.md
    guide = f"""# {skill_name} 使用指南

> 详细使用说明文档

---

## 一、概述

{skill_name} 是一个用于{description}的技能。

---

## 二、触发条件

当用户提到相关关键词时触发。

---

## 三、MCP 工具

通过 mcp/server.py 暴露以下工具：

| 工具名 | 说明 |
|--------|------|
| {skill_name}_do_something | 执行某个操作 |

---

*最后更新：{date}*
"""
    (skill_path / "references/guide.md").write_text(guide)

    # index.md
    index_md = f"""# 索引

> {{skill_name}} 技能开发指南导航

---

## 快速导航

| 指南 | 说明 |
|------|------|
| [使用指南](guide.md) | 技能使用方法、触发条件、MCP 工具 |

---

## 按场景查找

**新建技能**
1. [初始化新技能](guide.md#初始化)
2. [编写 SKILL.md](guide.md#编写-skill-md)

**完成后**
3. [质量检查](guide.md#质量检查)

---

*点击标题跳转对应指南*
""".format(skill_name=skill_name)
    (skill_path / "references/index.md").write_text(index_md)

    print(f"\n✅ 技能初始化完成: {skill_path}")
    print(f"   - SKILL.md")
    print(f"   - README.md")
    print(f"   - _meta.json")
    print(f"   - scripts/")
    print(f"   - references/index.md   ← 书籍索引")
    print(f"   - references/guide.md   ← 使用指南")
    print(f"   - mcp/server.py         ← MCP 工具暴露")
    print(f"\n   自检：请使用 skill-developer 技能对照自检清单")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 scripts/init.py <skill-name> <description> [path] [emoji]")
        print("示例: python3 scripts/init.py my-skill \"这是一个测试技能\" ./my-skill 📦")
        sys.exit(1)

    name = sys.argv[1]
    desc = sys.argv[2]
    path = sys.argv[3] if len(sys.argv) > 3 else f"./{name}"
    emoji = sys.argv[4] if len(sys.argv) > 4 else "📦"

    sys.exit(init_skill(path, name, desc, emoji))
