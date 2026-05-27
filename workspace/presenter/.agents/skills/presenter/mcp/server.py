#!/usr/bin/env python3
"""
presenter MCP Server
通过 MCP 暴露 presenter 技能的工具方法
"""

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path("/root/.openclaw/skills/presenter")

EXPOSED_TOOLS = [
    {
        "name": "presenter_compile_ppt",
        "description": "编译 PPT 脚本为 PPTX 文件",
        "parameters": {
            "type": "object",
            "properties": {
                "script_path": {
                    "type": "string",
                    "description": "PPT 脚本路径 (.md)"
                },
                "output_path": {
                    "type": "string",
                    "description": "输出 PPTX 路径"
                },
                "template": {
                    "type": "string",
                    "description": "模板名称 (默认: template)"
                }
            },
            "required": ["script_path", "output_path"]
        }
    },
    {
        "name": "presenter_list_layouts",
        "description": "列出模板中所有可用的 slide_layout",
        "parameters": {
            "type": "object",
            "properties": {
                "template": {
                    "type": "string",
                    "description": "模板名称 (默认: template)"
                }
            }
        }
    },
    {
        "name": "presenter_parse_script",
        "description": "解析 PPT 脚本，输出结构化 JSON",
        "parameters": {
            "type": "object",
            "properties": {
                "script_path": {
                    "type": "string",
                    "description": "PPT 脚本路径 (.md)"
                }
            },
            "required": ["script_path"]
        }
    }
]


class PresenterHandler:
    """处理 presenter 请求"""

    def __init__(self):
        self.skill_dir = SKILL_DIR

    async def handle_compile_ppt(self, args: dict) -> dict:
        """编译 PPT 脚本为 PPTX"""
        import subprocess
        script_path = args["script_path"]
        output_path = args["output_path"]
        template = args.get("template", "template")

        cmd = [
            "python3",
            str(self.skill_dir / "scripts/ppt/main.py"),
            "compile",
            "--input", script_path,
            "--output", output_path,
            "--template", template
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output": output_path
        }

    async def handle_list_layouts(self, args: dict) -> dict:
        """列出所有布局"""
        import subprocess
        template = args.get("template", "template")

        cmd = [
            "python3",
            str(self.skill_dir / "scripts/ppt/main.py"),
            "list",
            "--template", template
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    async def handle_parse_script(self, args: dict) -> dict:
        """解析 PPT 脚本"""
        import subprocess
        script_path = args["script_path"]

        cmd = [
            "python3",
            str(self.skill_dir / "scripts/ppt/main.py"),
            "parse",
            "--input", script_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }


app = Server("presenter")
handler = PresenterHandler()


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
    if name == "presenter_compile_ppt":
        result = await handler.handle_compile_ppt(arguments)
    elif name == "presenter_list_layouts":
        result = await handler.handle_list_layouts(arguments)
    elif name == "presenter_parse_script":
        result = await handler.handle_parse_script(arguments)
    else:
        result = {"success": False, "error": f"未知工具: {name}"}
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]


async def main():
    async with stdio_server(server=app) as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
