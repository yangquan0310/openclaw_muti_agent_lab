#!/usr/bin/env python3
"""
Mathematician MCP Server
通过 MCP 暴露数学工具
"""

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path(__file__).parent.parent

EXPOSED_TOOLS = [
    {
        "name": "math_lookup",
        "description": "列出或搜索数学工具",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["list", "search", "info"],
                    "description": "操作类型"
                },
                "keyword": {
                    "type": "string",
                    "description": "搜索关键词（用于search/info）"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "math_calculate",
        "description": "执行数值计算",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["basic", "matrix", "integrate", "ode", "root", "interp"],
                    "description": "运算类型"
                },
                "args": {
                    "type": "string",
                    "description": "运算参数（JSON格式）"
                }
            },
            "required": ["operation", "args"]
        }
    },
    {
        "name": "math_statistics",
        "description": "执行统计分析",
        "parameters": {
            "type": "object",
            "properties": {
                "analysis": {
                    "type": "string",
                    "enum": ["describe", "ttest", "chi2", "corr", "regress", "anova", "normality"],
                    "description": "分析类型"
                },
                "args": {
                    "type": "string",
                    "description": "分析参数（JSON格式）"
                }
            },
            "required": ["analysis", "args"]
        }
    }
]


class MathHandler:
    """处理数学请求"""

    def __init__(self):
        self.skill_dir = SKILL_DIR

    async def handle_lookup(self, action: str, keyword: str = None) -> dict:
        """处理工具查找请求"""
        import sys
        sys.path.insert(0, str(self.skill_dir / "scripts"))
        from lookup import list_tools, search_tools, show_info
        import io
        import contextlib

        if action == "list":
            # 捕获输出
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                list_tools()
            return {"success": True, "output": f.getvalue()}
        elif action == "search" and keyword:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                search_tools(keyword)
            return {"success": True, "output": f.getvalue()}
        elif action == "info" and keyword:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                show_info(keyword)
            return {"success": True, "output": f.getvalue()}
        else:
            return {"success": False, "error": "无效的操作"}

    async def handle_calculate(self, operation: str, args: str) -> dict:
        """处理计算请求"""
        import subprocess
        import sys

        try:
            args_dict = json.loads(args)
            cmd = [sys.executable, str(self.skill_dir / "scripts" / "calculate.py"), operation]
            
            for key, value in args_dict.items():
                cmd.extend([f"--{key}", str(value)])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {"success": True, "result": json.loads(result.stdout)}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def handle_statistics(self, analysis: str, args: str) -> dict:
        """处理统计请求"""
        import subprocess
        import sys

        try:
            args_dict = json.loads(args)
            cmd = [sys.executable, str(self.skill_dir / "scripts" / "statistics.py"), analysis]
            
            for key, value in args_dict.items():
                cmd.extend([f"--{key}", str(value)])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {"success": True, "result": json.loads(result.stdout)}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}


app = Server("mathematician")
handler = MathHandler()


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
    if name == "math_lookup":
        result = await handler.handle_lookup(
            arguments.get("action"),
            arguments.get("keyword")
        )
    elif name == "math_calculate":
        result = await handler.handle_calculate(
            arguments.get("operation"),
            arguments.get("args")
        )
    elif name == "math_statistics":
        result = await handler.handle_statistics(
            arguments.get("analysis"),
            arguments.get("args")
        )
    else:
        result = {"success": False, "error": f"未知工具: {name}"}
    
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


async def main():
    async with stdio_server(server=app) as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
