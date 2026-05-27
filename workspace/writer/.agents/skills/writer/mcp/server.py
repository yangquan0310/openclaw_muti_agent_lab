#!/usr/bin/env python3
"""
writer MCP 入口
暴露写作相关工具供代理调用
"""

# 目前 writer 是纯方法论技能，
# 所有操作通过读取 references/ 中的指南执行，
# 不需要暴露额外的 MCP 工具。

EXPOSED_TOOLS = []

TOOL_DEFINITIONS = []
