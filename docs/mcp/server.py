#!/usr/bin/env python3
"""
agent_self_development MCP Server
将 Agent 自我发展技能暴露为 MCP 工具

技能模块：
- metacognition: 元认知模块（计划/监控/调节）
- working_memory: 工作记忆模块（任务追踪）
- assimilation_accommodation: 同化顺应模块（日记/更新）
"""

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path("/root/.openclaw/workspace/skills/agent_self_development")

EXPOSED_TOOLS = [
    {
        "name": "asd_root",
        "description": "Agent自我发展根路由 - 基于皮亚杰认知发展理论的自我进化系统，协调元认知/工作记忆/同化顺应三大模块",
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
        "name": "asd_metacognition",
        "description": "Agent自我发展 - 元认知模块：计划、监控、调节三阶段闭环",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_skill_doc", "planning", "monitoring", "regulation"],
                    "description": "要执行的操作"
                },
                "task_context": {
                    "type": "string",
                    "description": "当前任务的上下文描述"
                },
                "agent_identity": {
                    "type": "object",
                    "description": "当前Agent的身份定义"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "asd_working_memory",
        "description": "Agent自我发展 - 工作记忆模块：活跃任务和子代理状态管理（基于Baddeley工作记忆模型）",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_skill_doc", "track_subagent", "update_memory_table", "archive_completed"],
                    "description": "要执行的操作"
                },
                "subagent_key": {
                    "type": "string",
                    "description": "子代理标识"
                },
                "task_info": {
                    "type": "object",
                    "description": "任务信息"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "asd_assimilation",
        "description": "Agent自我发展 - 同化顺应模块：通过日记记录实现自我更新（基于皮亚杰认知发展理论）",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["get_skill_doc", "write_diary", "analyze_assimilation", "update_identity"],
                    "description": "要执行的操作"
                },
                "diary_date": {
                    "type": "string",
                    "description": "日记日期（YYYY-MM-DD格式）"
                },
                "update_type": {
                    "type": "string",
                    "enum": ["core_self", "identity", "style_beliefs", "skills"],
                    "description": "更新类型"
                }
            },
            "required": ["action"]
        }
    }
]


class AgentSelfDevelopmentHandler:
    """处理 Agent 自我发展技能请求"""
    
    def __init__(self):
        self.skill_dir = SKILL_DIR
    
    def _read_skill_doc(self, subpath: str = "") -> str:
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
    
    async def handle_asd_root(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "agent_self_development", "content": self._read_skill_doc()}
        
        elif action == "get_workflow":
            return {
                "success": True,
                "workflows": [
                    {
                        "name": "Agent完整任务生命周期",
                        "description": "六阶段闭环：初始化→决策→计划→执行监控→调节→完成归档",
                        "stages": ["初始化", "决策", "计划", "执行监控", "调节", "完成归档"]
                    },
                    {
                        "name": "每日自我更新",
                        "description": "基于皮亚杰认知发展理论的每日自我进化",
                        "stages": ["记录日记", "阅读核心自我", "同化顺应分析", "执行更新", "同步更新", "记录日志"]
                    }
                ]
            }
        
        elif action == "list_modules":
            return {
                "success": True,
                "modules": [
                    {
                        "name": "metacognition",
                        "description": "元认知模块：计划、监控、调节三阶段闭环",
                        "routes": ["planning", "monitoring", "regulation"]
                    },
                    {
                        "name": "working_memory",
                        "description": "工作记忆模块：活跃任务和子代理状态管理（Baddeley工作记忆模型）",
                        "routes": ["memory_table", "subagent_tracker"]
                    },
                    {
                        "name": "assimilation_accommodation",
                        "description": "同化顺应模块：通过日记记录实现自我更新（皮亚杰认知发展理论）",
                        "routes": ["diary", "assimilation", "accommodation"]
                    }
                ]
            }
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_asd_metacognition(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "agent_self_development/metacognition", "content": self._read_skill_doc("metacognition")}
        
        elif action == "planning":
            return {
                "success": True,
                "stage": "planning",
                "task_context": args.get("task_context", ""),
                "agent_identity": args.get("agent_identity", {}),
                "output": "task_plan",
                "next_stage": "monitoring"
            }
        
        elif action == "monitoring":
            return {"success": True, "stage": "monitoring", "output": "memory_update", "next_stage": "regulation (条件触发) 或 完成"}
        
        elif action == "regulation":
            return {"success": True, "stage": "regulation", "action": "返回 monitoring 阶段"}
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_asd_working_memory(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "agent_self_development/working_memory", "content": self._read_skill_doc("working_memory")}
        
        elif action == "track_subagent":
            return {
                "success": True,
                "action": "track_subagent",
                "subagent_key": args.get("subagent_key", ""),
                "task_info": args.get("task_info", {})
            }
        
        elif action in ["update_memory_table", "archive_completed"]:
            return {"success": True, "action": action, "message": f"{action}请求已记录"}
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_asd_assimilation(self, args: dict) -> dict:
        action = args.get("action")
        
        if action == "get_skill_doc":
            return {"success": True, "skill": "agent_self_development/assimilation_accommodation", "content": self._read_skill_doc("assimilation_accommodation")}
        
        elif action == "write_diary":
            return {
                "success": True,
                "action": "write_diary",
                "diary_date": args.get("diary_date", self._get_current_date()),
                "output": "diary_entry"
            }
        
        elif action == "analyze_assimilation":
            return {
                "success": True,
                "action": "analyze_assimilation",
                "theory": "皮亚杰认知发展理论",
                "concepts": ["同化(Assimilation)", "顺应(Accommodation)", "平衡(Equilibration)"]
            }
        
        elif action == "update_identity":
            update_type = args.get("update_type", "")
            target_files = {
                "core_self": "MEMORY.md",
                "identity": "IDENTITY.md",
                "style_beliefs": "SOUL.md",
                "skills": "skills/README.md"
            }
            return {
                "success": True,
                "action": "update_identity",
                "update_type": update_type,
                "target_file": target_files.get(update_type, "未知")
            }
        
        return {"success": False, "error": f"不支持的操作: {action}"}


app = Server("agent-self-development")
handler = AgentSelfDevelopmentHandler()


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name=t["name"], description=t["description"], inputSchema=t["parameters"]) for t in EXPOSED_TOOLS]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    handlers = {
        "asd_root": handler.handle_asd_root,
        "asd_metacognition": handler.handle_asd_metacognition,
        "asd_working_memory": handler.handle_asd_working_memory,
        "asd_assimilation": handler.handle_asd_assimilation,
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
