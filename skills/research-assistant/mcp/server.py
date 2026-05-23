#!/usr/bin/env python3
"""
research-assistant MCP Server
将研究助手技能暴露为 MCP 工具

技能模块：
- search: 检索模块 (Searcher)
- summarize: 总结模块 (Summarizer)
- manage: 管理模块 (Manager)
- synthesize: 综述模块 (Synthesizer)
- maintainer: 元数据维护与版本控制模块 (Maintainer)
"""

import asyncio
import json
import sys
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

EXPOSED_TOOLS = [
    {
        "name": "km_read_skill_doc",
        "description": "读取研究助手技能文档。支持读取根目录 SKILL.md 或子模块文档（search/summarize/manage/synthesize/maintainer）。",
        "parameters": {
            "type": "object",
            "properties": {
                "module": {
                    "type": "string",
                    "enum": ["", "search", "summarize", "manage", "synthesize", "maintainer"],
                    "description": "子模块名称，空字符串表示读取根目录 SKILL.md"
                }
            }
        }
    },
    {
        "name": "km_list_modules",
        "description": "列出研究助手的所有子模块及其功能说明",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "km_get_workflow",
        "description": "获取研究助手的标准工作流（检索→总结→管理→综述）",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]


class KnowledgeManagerHandler:
    """处理知识库管理技能请求"""
    
    def __init__(self):
        self.skill_dir = SKILL_DIR
    
    def _read_skill_doc(self, subpath: str = "") -> str:
        """读取技能文档"""
        if subpath:
            full_path = self.skill_dir / "references" / f"{subpath}.md"
        else:
            full_path = self.skill_dir / "SKILL.md"
        
        if full_path.exists():
            return full_path.read_text(encoding="utf-8")
        return f"技能文档不存在: {full_path}"
    
    def _get_current_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    async def handle_read_skill_doc(self, args: dict) -> dict:
        module = args.get("module", "")
        content = self._read_skill_doc(module)
        return {
            "success": True,
            "skill": f"research-assistant/{module}" if module else "research-assistant",
            "content": content
        }
    
    async def handle_list_modules(self, args: dict) -> dict:
        return {
            "success": True,
            "modules": [
                {"name": "search", "class": "Searcher", "description": "检索并获取论文列表"},
                {"name": "summarize", "class": "Summarizer", "description": "解析摘要并提取结构化笔记"},
                {"name": "manage", "class": "Manager", "description": "知识库合并、筛选、提取"},
                {"name": "synthesize", "class": "Synthesizer", "description": "将笔记组织成完整综述"},
                {"name": "maintainer", "class": "Maintainer", "description": "元数据维护与版本控制"}
            ]
        }
    
    async def handle_get_workflow(self, args: dict) -> dict:
        return {
            "success": True,
            "workflows": [
                {"name": "检索文献", "module": "search", "description": "检索并获取论文列表"},
                {"name": "总结文献", "module": "summarize", "description": "解析摘要并提取结构化笔记"},
                {"name": "管理知识库", "module": "manage", "description": "知识库合并、筛选、提取"},
                {"name": "撰写综述", "module": "synthesize", "description": "将笔记组织成完整综述"},
                {"name": "维护元数据", "module": "maintainer", "description": "元数据维护与版本控制"}
            ]
        }


app = Server("research-assistant")
handler = KnowledgeManagerHandler()


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name=t["name"], description=t["description"], inputSchema=t["parameters"]) for t in EXPOSED_TOOLS]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    handlers = {
        "km_read_skill_doc": handler.handle_read_skill_doc,
        "km_list_modules": handler.handle_list_modules,
        "km_get_workflow": handler.handle_get_workflow,
    }
    
    if name not in handlers:
        return [TextContent(type="text", text=json.dumps({"success": False, "error": f"未知工具: {name}"}, ensure_ascii=False))]
    
    try:
        result = await handlers[name](arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))]


async def main():
    async with stdio_server(server=app) as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
