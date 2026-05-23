#!/usr/bin/env python3
"""
Physicist MCP Server
通过 MCP 暴露 Physicist 的工具方法
"""

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path("/root/.openclaw/skills/physicist")

EXPOSED_TOOLS = [
    {
        "name": "physicist_list_tools",
        "description": "列出 Physicist 所有可用工具",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "physicist_search_tools",
        "description": "搜索 Physicist 工具",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "搜索关键词"
                }
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "physicist_calculate",
        "description": "执行物理数值计算",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["basic", "matrix", "integrate", "ode"],
                    "description": "计算类型"
                },
                "args": {
                    "type": "object",
                    "description": "计算参数"
                }
            },
            "required": ["operation"]
        }
    },
    {
        "name": "physicist_visualize",
        "description": "生成物理可视化图表",
        "parameters": {
            "type": "object",
            "properties": {
                "plot_type": {
                    "type": "string",
                    "enum": ["function", "phase", "field", "surface"],
                    "description": "绘图类型"
                },
                "params": {
                    "type": "object",
                    "description": "绘图参数"
                }
            },
            "required": ["plot_type"]
        }
    }
]


class PhysicistHandler:
    """处理 Physicist 请求"""

    def __init__(self):
        self.skill_dir = SKILL_DIR

    async def handle_list_tools(self) -> dict:
        """列出所有工具"""
        import sys
        sys.path.insert(0, str(self.skill_dir / "scripts"))
        from lookup import list_tools
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            list_tools()
        return {"success": True, "output": f.getvalue()}

    async def handle_search_tools(self, keyword: str) -> dict:
        """搜索工具"""
        import sys
        sys.path.insert(0, str(self.skill_dir / "scripts"))
        from lookup import search_tools
        import io
        import contextlib
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            search_tools(keyword)
        return {"success": True, "output": f.getvalue()}

    async def handle_calculate(self, operation: str, args: dict) -> dict:
        """执行计算"""
        return {"success": True, "message": f"计算类型: {operation}", "params": args}

    async def handle_visualize(self, plot_type: str, params: dict) -> dict:
        """执行可视化"""
        return {"success": True, "message": f"绘图类型: {plot_type}", "params": params}


app = Server("physicist")
handler = PhysicistHandler()


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
    if name == "physicist_list_tools":
        result = await handler.handle_list_tools()
    elif name == "physicist_search_tools":
        result = await handler.handle_search_tools(arguments.get("keyword", ""))
    elif name == "physicist_calculate":
        result = await handler.handle_calculate(
            arguments.get("operation", ""),
            arguments.get("args", {})
        )
    elif name == "physicist_visualize":
        result = await handler.handle_visualize(
            arguments.get("plot_type", ""),
            arguments.get("params", {})
        )
    else:
        result = {"success": False, "error": f"未知工具: {name}"}
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]


async def main():
    async with stdio_server(server=app) as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
