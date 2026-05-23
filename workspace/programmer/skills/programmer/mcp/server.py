#!/usr/bin/env python3
"""
programmer MCP server
暴露 programmer 技能的核心方法
"""

EXPOSED_TOOLS = [
    {
        "name": "programmer_oop_concepts",
        "description": "获取 OOP 核心概念指南",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "programmer_oop_principles",
        "description": "获取 OOP 原则详解（封装、继承、多态）",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "programmer_fullstack_guide",
        "description": "获取全栈开发指南",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "programmer_dev_workflow",
        "description": "获取开发流程指南",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "programmer_coding_standards",
        "description": "获取代码规范指南",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


def get_guide(guide_name: str) -> str:
    """读取指定指南内容"""
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    guide_path = os.path.join(base_dir, "references", f"{guide_name}.md")
    
    if os.path.exists(guide_path):
        with open(guide_path, "r") as f:
            return f.read()
    return f"指南 {guide_name} 不存在"


def oop_concepts() -> str:
    """OOP 核心概念"""
    return get_guide("oop-guide")


def oop_principles() -> str:
    """OOP 原则详解"""
    return get_guide("oop-principles")


def fullstack_guide() -> str:
    """全栈开发指南"""
    return get_guide("fullstack-guide")


def dev_workflow() -> str:
    """开发流程指南"""
    return get_guide("development-workflow")


def coding_standards() -> str:
    """代码规范指南"""
    return get_guide("coding-standards")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="programmer MCP server")
    parser.add_argument("--guide", choices=["oop-guide", "oop-principles", "fullstack-guide", "development-workflow", "coding-standards"])
    args = parser.parse_args()
    
    if args.guide:
        print(get_guide(args.guide))
    else:
        print("使用 --guide 参数指定要查看的指南")
        print("可用指南：oop-guide, oop-principles, fullstack-guide, development-workflow, coding-standards")
