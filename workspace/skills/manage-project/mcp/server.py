#!/usr/bin/env python3
"""
manage-project MCP Server
将项目管理技能暴露为 MCP 工具

技能模块：
- search: 检索模块 (Searcher)
- summarize: 总结模块 (Summarizer)
- manage: 管理模块 (Manager)
- synthesize: 综述模块 (Synthesizer)
- maintainer: 项目整理模块 (Maintainer)
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
        "name": "km_root",
        "description": "项目管理根路由 - 协调Searcher/Summarizer/Manager/Synthesizer/Maintainer五个子技能",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_skill_doc", "get_workflow", "list_modules"],
                    "description": "要执行的操作"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "km_search",
        "description": "知识库管理 - 检索模块(Searcher)：检索并获取论文列表或加载已有知识库并更新",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_skill_doc", "search_papers", "load_kb", "update_kb"],
                    "description": "要执行的操作"
                },
                "queries": {
                    "type": "object",
                    "description": "检索查询字典，格式：{主题: [{query: 查询词, limit: 数量}]}"
                },
                "kb_path": {
                    "type": "string",
                    "description": "知识库文件路径"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "km_summarize",
        "description": "知识库管理 - 总结模块(Summarizer)：解析摘要并提取结构化笔记",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_skill_doc", "summarize_kb", "extract_notes"],
                    "description": "要执行的操作"
                },
                "kb_path": {
                    "type": "string",
                    "description": "知识库文件路径"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "km_manage",
        "description": "知识库管理 - 管理模块(Manager)：知识库合并、筛选、提取",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_skill_doc", "filter_kb", "merge_kb", "export_notes"],
                    "description": "要执行的操作"
                },
                "kb_path": {
                    "type": "string",
                    "description": "知识库文件路径"
                },
                "filter_criteria": {
                    "type": "object",
                    "description": "筛选条件，如 {citations_min: 50, year_after: 2020}"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "km_synthesize",
        "description": "知识库管理 - 综述模块(Synthesizer)：将笔记组织成完整综述，检查参考文献",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_skill_doc", "write_review", "check_references"],
                    "description": "要执行的操作"
                },
                "notes_path": {
                    "type": "string",
                    "description": "笔记文件路径"
                },
                "output_path": {
                    "type": "string",
                    "description": "综述输出路径"
                }
            },
            "required": ["action"]
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
            full_path = self.skill_dir / subpath / "SKILL.md"
        else:
            full_path = self.skill_dir / "SKILL.md"
        
        if full_path.exists():
            return full_path.read_text(encoding="utf-8")
        return f"技能文档不存在: {full_path}"
    
    def _get_current_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    async def handle_km_root(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "manage-project", "content": self._read_skill_doc()}
        
        elif action == "get_workflow":
            return {
                "success": True,
                "workflows": [
                    {"name": "检索文献", "module": "search", "description": "检索并获取论文列表"},
                    {"name": "总结文献", "module": "summarize", "description": "解析摘要并提取结构化笔记"},
                    {"name": "管理知识库", "module": "manage", "description": "知识库合并、筛选、提取"},
                    {"name": "撰写综述", "module": "synthesize", "description": "将笔记组织成完整综述"},
                    {"name": "整理项目", "module": "maintainer", "description": "自动化整理项目目录结构"}
                ]
            }
        
        elif action == "list_modules":
            return {
                "success": True,
                "modules": [
                    {"name": "search", "class": "Searcher", "description": "检索并获取论文列表"},
                    {"name": "summarize", "class": "Summarizer", "description": "解析摘要并提取结构化笔记"},
                    {"name": "manage", "class": "Manager", "description": "知识库合并、筛选、提取"},
                    {"name": "synthesize", "class": "Synthesizer", "description": "将笔记组织成完整综述"},
                    {"name": "maintainer", "class": "Maintainer", "description": "自动化整理项目目录结构"}
                ]
            }
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_km_search(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "manage-project/search", "content": self._read_skill_doc("search")}
        
        elif action == "search_papers":
            queries = args.get("queries", {})
            kb_path = args.get("kb_path", f"kb_{self._get_current_date()}.json")
            return {
                "success": True,
                "action": "search_papers",
                "queries": queries,
                "kb_path": kb_path,
                "message": "检索请求已记录",
                "python_example": f"from search.Searcher import Searcher\nsearcher = Searcher()\nqueries = {json.dumps(queries, ensure_ascii=False)}\nsearcher.search(queries, kb_path='{kb_path}')"
            }
        
        elif action in ["load_kb", "update_kb"]:
            kb_path = args.get("kb_path", "")
            return {"success": True, "action": action, "kb_path": kb_path, "message": f"{action}请求已记录"}
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_km_summarize(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "manage-project/summarize", "content": self._read_skill_doc("summarize")}
        
        elif action in ["summarize_kb", "extract_notes"]:
            kb_path = args.get("kb_path", "")
            return {
                "success": True,
                "action": action,
                "kb_path": kb_path,
                "message": f"{action}请求已记录",
                "python_example": f"from summarize.Summarizer import Summarizer\nsummarizer = Summarizer()\nsummarizer.summarize(kb_path='{kb_path}')"
            }
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_km_manage(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "manage-project/manage", "content": self._read_skill_doc("manage")}
        
        elif action == "filter_kb":
            kb_path = args.get("kb_path", "")
            criteria = args.get("filter_criteria", {})
            return {
                "success": True,
                "action": "filter_kb",
                "kb_path": kb_path,
                "criteria": criteria,
                "python_example": f"from manage.Manager import Manager\nmanager = Manager('{kb_path}')\nmanager.filter({json.dumps(criteria, ensure_ascii=False)}).save('filtered_kb.json')"
            }
        
        elif action in ["merge_kb", "export_notes"]:
            return {"success": True, "action": action, "message": f"{action}请求已记录"}
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_km_synthesize(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "manage-project/synthesize", "content": self._read_skill_doc("synthesize")}
        
        elif action == "write_review":
            notes_path = args.get("notes_path", "")
            output_path = args.get("output_path", f"review_{self._get_current_date()}.md")
            return {"success": True, "action": "write_review", "notes_path": notes_path, "output_path": output_path}
        
        elif action == "check_references":
            return {"success": True, "action": "check_references", "message": "检查参考文献请求已记录"}
        
        return {"success": False, "error": f"不支持的操作: {action}"}


app = Server("manage-project")
handler = KnowledgeManagerHandler()


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name=t["name"], description=t["description"], inputSchema=t["parameters"]) for t in EXPOSED_TOOLS]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    handlers = {
        "km_root": handler.handle_km_root,
        "km_search": handler.handle_km_search,
        "km_summarize": handler.handle_km_summarize,
        "km_manage": handler.handle_km_manage,
        "km_synthesize": handler.handle_km_synthesize,
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
