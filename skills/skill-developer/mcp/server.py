#!/usr/bin/env python3
"""
Skill-developer MCP Server
将技能开发工具暴露为 MCP 工具
"""

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path("/root/.openclaw/workspace/skills/Skill-developer")

EXPOSED_TOOLS = [
    {
        "name": "skill_dev_create",
        "description": "创建新技能项目结构 - 初始化标准技能目录和文件",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["create_skill", "get_template"],
                    "description": "要执行的操作"
                },
                "skill_name": {
                    "type": "string",
                    "description": "技能名称（英文小写，横线分隔）"
                },
                "skill_description": {
                    "type": "string",
                    "description": "技能功能描述"
                },
                "triggers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "触发该技能的关键词或场景列表"
                },
                "with_mcp": {
                    "type": "boolean",
                    "description": "是否添加MCP支持"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "skill_dev_mcp",
        "description": "为现有技能添加MCP支持 - 创建mcp目录和server.py，注册到openclaw.json",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["add_mcp_support", "get_mcp_template", "register_to_openclaw"],
                    "description": "要执行的操作"
                },
                "skill_path": {
                    "type": "string",
                    "description": "技能路径（相对于workspace/skills）"
                },
                "tools": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"}
                        }
                    },
                    "description": "要暴露的工具列表"
                }
            },
            "required": ["action"]
        }
    },
    {
        "name": "skill_dev_extend",
        "description": "扩展现有技能 - 添加子模块或更新元数据",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["add_submodule", "update_meta", "add_workflow"],
                    "description": "要执行的操作"
                },
                "skill_path": {
                    "type": "string",
                    "description": "技能路径"
                },
                "submodule_name": {
                    "type": "string",
                    "description": "子模块名称（add_submodule时使用）"
                }
            },
            "required": ["action", "skill_path"]
        }
    }
]


class SkillDeveloperHandler:
    """处理技能开发请求"""
    
    def __init__(self):
        self.skill_dir = SKILL_DIR
        self.workspace_skills = Path("/root/.openclaw/workspace/skills")
    
    def _get_current_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    async def handle_skill_dev_create(self, args: dict) -> dict:
        """处理创建技能请求"""
        action = args.get("action")
        
        if action == "get_template":
            return {
                "success": True,
                "templates": {
                    "skill_md": "---\nname: <技能名称>\ndescription: <描述>\nversion: 1.0.0\n---\n\n# <技能名称>\n\n<概述>\n\n## 文件说明\n| 文件 | 功能 | 说明 |\n|------|------|------|\n| SKILL.md | 技能规范 | 给AI的技能开发规范 |\n| README.md | 人类说明 | 给人类阅读的技能说明 |\n| _meta.json | 元数据 | 技能元数据配置 |\n\n## 工作流\n\n### 工作流1\n\n## 使用指南\n\n---\n版本历史\n| 版本 | 日期 | 更新内容 |\n|------|------|----------|\n| 1.0.0 | <日期> | 初始版本 |",
                    "readme_md": "# <技能名称>\n\n<描述>\n\n## 安装\n\n## 使用\n\n## 配置",
                    "meta_json": {
                        "name": "<技能名称>",
                        "description": "<描述>",
                        "version": "1.0.0",
                        "created_at": "<日期>",
                        "triggers": [],
                        "dependencies": {"bins": [], "python_packages": []},
                        "environment_variables": []
                    }
                }
            }
        
        elif action == "create_skill":
            skill_name = args.get("skill_name", "")
            skill_description = args.get("skill_description", "")
            triggers = args.get("triggers", [])
            with_mcp = args.get("with_mcp", False)
            
            if not skill_name:
                return {"success": False, "error": "skill_name 不能为空"}
            
            # 构建技能路径
            skill_path = self.workspace_skills / skill_name
            
            # 创建目录结构
            directories = [skill_path]
            if with_mcp:
                directories.append(skill_path / "mcp")
            
            for d in directories:
                d.mkdir(parents=True, exist_ok=True)
            
            created_files = []
            
            # 创建 SKILL.md
            skill_md = f"""---
name: {skill_name}
description: {skill_description}
version: 1.0.0
---

# {skill_name}

{skill_description}

## 触发场景
{chr(10).join(f"- {t}" for t in triggers) if triggers else "- 待补充"}

## 文件说明
| 文件 | 功能 | 说明 |
|------|------|------|
| SKILL.md | 技能规范 | 给AI的技能开发规范 |
| README.md | 人类说明 | 给人类阅读的技能说明 |
| _meta.json | 元数据 | 技能元数据配置 |

## 工作流

### 工作流1

## 使用指南

---
版本历史
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | {self._get_current_date()} | 初始版本 |
"""
            (skill_path / "SKILL.md").write_text(skill_md, encoding="utf-8")
            created_files.append("SKILL.md")
            
            # 创建 README.md
            readme_md = f"""# {skill_name}

{skill_description}

## 安装

## 使用

## 配置
"""
            (skill_path / "README.md").write_text(readme_md, encoding="utf-8")
            created_files.append("README.md")
            
            # 创建 _meta.json
            meta = {
                "name": skill_name,
                "description": skill_description,
                "version": "1.0.0",
                "created_at": self._get_current_date(),
                "triggers": triggers,
                "dependencies": {"bins": [], "python_packages": []},
                "environment_variables": []
            }
            (skill_path / "_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
            created_files.append("_meta.json")
            
            result = {
                "success": True,
                "action": "create_skill",
                "skill_name": skill_name,
                "skill_path": str(skill_path),
                "created_files": created_files,
                "with_mcp": with_mcp
            }
            
            if with_mcp:
                result["note"] = "已创建mcp目录，请使用 skill_dev_mcp 工具添加MCP服务器代码"
            
            return result
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_skill_dev_mcp(self, args: dict) -> dict:
        """处理添加MCP支持请求"""
        action = args.get("action")
        
        if action == "get_mcp_template":
            return {
                "success": True,
                "template": {
                    "server_py": "#!/usr/bin/env python3\n\"\"\"\n<技能名称> MCP Server\n\"\"\"\n\nimport asyncio\nimport json\nfrom pathlib import Path\nfrom mcp.server import Server\nfrom mcp.server.stdio import stdio_server\nfrom mcp.types import Tool, TextContent\n\nSKILL_DIR = Path(\"/root/.openclaw/workspace/skills/<技能名称>\")\n\nEXPOSED_TOOLS = [\n    {\n        \"name\": \"<工具名>\",\n        \"description\": \"<工具描述>\",\n        \"parameters\": {\n            \"type\": \"object\",\n            \"properties\": {\n                \"action\": {\n                    \"type\": \"string\",\n                    \"enum\": [\"<操作1>\", \"<操作2>\"],\n                    \"description\": \"要执行的操作\"\n                }\n            },\n            \"required\": [\"action\"]\n        }\n    }\n]\n\nclass <技能名>Handler:\n    async def handle_<工具名>(self, args: dict) -> dict:\n        return {\"success\": True}\n\napp = Server(\"<技能名称>\")\nhandler = <技能名>Handler()\n\n@app.list_tools()\nasync def list_tools() -> list[Tool]:\n    return [Tool(name=t[\"name\"], description=t[\"description\"], inputSchema=t[\"parameters\"]) for t in EXPOSED_TOOLS]\n\n@app.call_tool()\nasync def call_tool(name: str, arguments: dict) -> list[TextContent]:\n    # 实现调用逻辑\n    pass\n\nasync def main():\n    async with stdio_server(server=app) as (read_stream, write_stream):\n        await app.run(read_stream, write_stream, app.create_initialization_options())\n\nif __name__ == \"__main__\":\n        asyncio.run(main())",
                    "openclaw_config": {
                        "mcp": {
                            "servers": {
                                "<技能名称>": {
                                    "command": "python3",
                                    "args": ["/root/.openclaw/workspace/skills/<技能名称>/mcp/server.py"]
                                }
                            }
                        }
                    }
                }
            }
        
        elif action == "add_mcp_support":
            skill_path = args.get("skill_path", "")
            tools = args.get("tools", [])
            
            if not skill_path:
                return {"success": False, "error": "skill_path 不能为空"}
            
            full_path = self.workspace_skills / skill_path
            mcp_dir = full_path / "mcp"
            mcp_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建 server.py
            server_py = f"""#!/usr/bin/env python3
\"\"\"
{skill_path} MCP Server
\"\"\"

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path("/root/.openclaw/workspace/skills/{skill_path}")

EXPOSED_TOOLS = {json.dumps([{"name": t.get("name", ""), "description": t.get("description", ""), "parameters": {"type": "object", "properties": {}, "required": []}} for t in tools], indent=4, ensure_ascii=False)}


class {skill_path.replace("-", "_").title()}Handler:
    \"\"\"处理技能请求\"\"\"
    
    def __init__(self):
        self.skill_dir = SKILL_DIR


app = Server("{skill_path}")
handler = {skill_path.replace("-", "_").title()}Handler()


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name=t["name"], description=t["description"], inputSchema=t["parameters"]) for t in EXPOSED_TOOLS]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps({{"success": True, "tool": name}}, ensure_ascii=False))]


async def main():
    async with stdio_server(server=app) as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
"""
            (mcp_dir / "server.py").write_text(server_py, encoding="utf-8")
            
            return {
                "success": True,
                "action": "add_mcp_support",
                "skill_path": str(full_path),
                "mcp_dir": str(mcp_dir),
                "created_file": "mcp/server.py",
                "next_step": "使用 register_to_openclaw 操作注册到 openclaw.json"
            }
        
        elif action == "register_to_openclaw":
            skill_path = args.get("skill_path", "")
            
            if not skill_path:
                return {"success": False, "error": "skill_path 不能为空"}
            
            config_patch = {
                "mcp": {
                    "servers": {
                        skill_path: {
                            "command": "python3",
                            "args": [f"/root/.openclaw/workspace/skills/{skill_path}/mcp/server.py"]
                        }
                    }
                }
            }
            
            return {
                "success": True,
                "action": "register_to_openclaw",
                "skill_name": skill_path,
                "config_patch": config_patch,
                "instruction": "使用 gateway config.patch 将上述配置应用到 openclaw.json",
                "verify_command": "openclaw mcp list"
            }
        
        return {"success": False, "error": f"不支持的操作: {action}"}
    
    async def handle_skill_dev_extend(self, args: dict) -> dict:
        """处理扩展现有技能请求"""
        action = args.get("action")
        skill_path = args.get("skill_path", "")
        
        if not skill_path:
            return {"success": False, "error": "skill_path 不能为空"}
        
        full_path = self.workspace_skills / skill_path
        
        if action == "add_submodule":
            submodule_name = args.get("submodule_name", "")
            if not submodule_name:
                return {"success": False, "error": "submodule_name 不能为空"}
            
            submodule_dir = full_path / submodule_name
            submodule_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建子模块 SKILL.md
            submodule_md = f"""---
name: {submodule_name}
description: {skill_path} 的子模块 - {submodule_name}
version: 1.0.0
---

# {submodule_name}

{skill_path} 技能的子模块。

## 文件说明
| 文件 | 功能 | 说明 |
|------|------|------|
| SKILL.md | 子模块规范 | 子模块开发规范 |

## 工作流

### 工作流1

---
版本历史
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | {self._get_current_date()} | 初始版本 |
"""
            (submodule_dir / "SKILL.md").write_text(submodule_md, encoding="utf-8")
            
            return {
                "success": True,
                "action": "add_submodule",
                "skill_path": str(full_path),
                "submodule": submodule_name,
                "submodule_path": str(submodule_dir),
                "created_file": f"{submodule_name}/SKILL.md"
            }
        
        elif action == "update_meta":
            return {
                "success": True,
                "action": "update_meta",
                "skill_path": str(full_path),
                "note": "请手动编辑 _meta.json 文件更新元数据"
            }
        
        elif action == "add_workflow":
            return {
                "success": True,
                "action": "add_workflow",
                "skill_path": str(full_path),
                "note": "请在 SKILL.md 中添加新的工作流章节"
            }
        
        return {"success": False, "error": f"不支持的操作: {action}"}


app = Server("skill-developer")
handler = SkillDeveloperHandler()


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name=t["name"], description=t["description"], inputSchema=t["parameters"]) for t in EXPOSED_TOOLS]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    handlers = {
        "skill_dev_create": handler.handle_skill_dev_create,
        "skill_dev_mcp": handler.handle_skill_dev_mcp,
        "skill_dev_extend": handler.handle_skill_dev_extend,
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
