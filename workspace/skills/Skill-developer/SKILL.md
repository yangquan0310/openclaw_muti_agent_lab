---
name: Skill-developer
description: >
  指导代理扮演“技能开发者”，按照面向对象的规范(类、对象、属性、方法、继承、封装)，创建新技能，实现技能的复用。
version: 2.0.0
---

# Skill-developer

代理将扮演“技能开发者”，遵循开发者开发原则，按照面向对象的规范(类、对象、属性、方法、继承、封装)，参考工作流，创建新技能，实现技能的复用。

## 文件说明
| 文件 | 功能 | 说明 |
|------|------|------|
| `SKILL.md` | 开发规范 | 写给代理的技能开发规范 |
| `README.md` | 技能说明 | 给人类看的开发说明 |

## 开发者开发原则
- 明确陈述假设——不确定就问，别猜
- 提供多种解读——有歧义时不要默默选一个 
- 该反驳就反驳——如果有更简单的方案，说出来
- 困惑就停——明确说哪里不清楚，请求澄清

---
## 工作流示例

### 工作流1：初始化项目结构
- 分析需求，按需求创建子模块
- 初始化项目
```
project-root/
│
├── SKILL.md                       # 根路由 / 项目总控 (相当于 main.py 的索引)
│
├── 子模块1/                        # 子模块
│   ├── SKILL.md                    # 子模块1初始化文件，集成了介绍、路由、工作流示例和使用指南等内容
│   ├── fetch_and_process.py       
│   └── daily_report.py
│
└── 子模块2/                         
│    ├── SKILL.md
│    └── ...
│
├── _mate.json                      # 技能元数据
│
└── README.md                       # 给人类看的开发说明

```
- 初始化项目元数据
```json
{
  "name": "",
  "description": "",
  "version": "",
  "author": "",
  "created_at": "2026-04-13",
  "triggers": [],
  "dependencies": {
    "bins": [],
    "python_packages": []
  },
  "environment_variables": []
}
```
### 工作流2：创建py脚本
- 结构化脚本最好使用python编写
- 需要同时支持命令行使用和.py文件调用
- pyhon代码必须使用面向对象框架
- 一个类除了必要实现的功能方法，其他方法都应该为私有方法。

```python

```

### 工作流3：攥写SKILL.md脚本
- SKILL.md应该至少包含“头部yaml”，技能概述、文件说明、工作流、使用指南和版本历史。
- SKILL.md示例
```markdown
---
name: <技能名称>
description: <描述>
version: 2.0.0
author: Yang Quan
dependencies:
tools:
---

# <技能名称>
<概述>

## 文件说明
文件说明表
| 文件 | 功能 | 说明 |
|------|------|------|
| | | |

## 工作流

### 子工作流

## 使用指南
对于python等结构化程序文件应该包含命令行使用指南、调用指南、参数详细解释
### 命令行使用指南bash


### python调用指南


### 参数详解
- 参数应该输入什么类型的值
- 参数值的范围

## 其他必要说明内容

---
版本历史
```
### 工作流4：扩展与维护项目
- 扩展与维护项目，可以重复工作流2和3，添加新的子模块
- 更新根目录的SKILL.md、_meta.json和README.md
### 工作流5：添加 MCP 支持（仅限公共技能，可选）

> ⚠️ **重要区分**：
> - **公共技能**（`workspace/skills/`）：可以添加 MCP 支持，供所有 Agent 调用
> - **个人私有技能**（`~/.openclaw/workspace/<agent>/skills/`）：**不需要**添加 MCP 支持

如果**公共技能**需要暴露为 MCP 服务器供其他 Agent 调用，按以下步骤添加 MCP 支持：

#### 5.1 创建 MCP 目录结构
```
workspace/skills/<技能名称>/
├── ...
├── mcp/
│   └── server.py              # MCP 服务器入口文件
└── ...
```

#### 5.2 编写 MCP 服务器 (mcp/server.py)
- 使用 Python MCP SDK 创建 stdio 服务器
- 定义工具列表（list_tools）
- 实现工具调用处理（call_tool）
- 每个工具对应技能的一个功能模块

```python
#!/usr/bin/env python3
"""
<技能名称> MCP Server
"""

import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SKILL_DIR = Path("/root/.openclaw/workspace/skills/<技能名称>")

EXPOSED_TOOLS = [
    {
        "name": "<工具名>",
        "description": "<工具描述>",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["<操作1>", "<操作2>"],
                    "description": "要执行的操作"
                }
            },
            "required": ["action"]
        }
    }
]


class <技能名>Handler:
    """处理技能请求"""
    
    def __init__(self):
        self.skill_dir = SKILL_DIR
    
    async def handle_<工具名>(self, args: dict) -> dict:
        """处理工具请求"""
        action = args.get("action")
        # 实现处理逻辑
        return {"success": True, "action": action}


app = Server("<技能名称>")
handler = <技能名>Handler()


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name=t["name"], description=t["description"], inputSchema=t["parameters"]) for t in EXPOSED_TOOLS]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    handlers = {
        "<工具名>": handler.handle_<工具名>,
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
```

#### 5.3 注册到 OpenClaw MCP

使用 `gateway config.patch` 将技能注册到 `openclaw.json` 的 `mcp.servers` 中：

```json
{
  "mcp": {
    "servers": {
      "<技能名称>": {
        "command": "python3",
        "args": ["/root/.openclaw/workspace/skills/<技能名称>/mcp/server.py"]
      }
    }
  }
}
```

#### 5.4 验证注册

注册完成后，运行以下命令验证：
```bash
openclaw mcp list
```

应看到新注册的技能服务器：
```
- <技能名称>
```

---
## 使用指南

### 核心功能
- 支持面向对象技能创建
- 自动生成标准文件结构，确保符合OpenClaw技能规范
- 统一SKILL.md和README.md内容，保持一致性
- 提供YAML元数据模板和文件结构模板

### 输入参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| 技能名称 | string | ✅ | 技能的唯一标识名称，英文小写，用横线分隔 |
| 技能功能描述 | string | ✅ | 详细说明技能的用途和能力 |
| 触发场景 | list | ✅ | 触发该技能的关键词或场景列表 |

### 输出结果
| 输出项 | 格式 | 说明 |
|--------|------|------|
| 核心技能文件 | code/Markdown | Python/Shell脚本或Markdown流程文档 |
| README.md | Markdown | 给人类阅读的技能说明文档 |
| SKILL.md | Markdown | 给AI解析的结构化技能规范文档 |

---
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2.0.0 | 2026-04-116 | 面向对象设计，包含完整的工作流程和模板 |
| 1.0.0 | 2026-04-13 | 初始版本，包含完整的技能创建流程和模板 |
| 0.9.0 | 2026-04-12 | 新增两种技能类型支持，完善文件结构规范 |
| 0.8.0 | 2026-04-10 | 添加YAML元数据模板和README/SKILL内容区分标准 |
