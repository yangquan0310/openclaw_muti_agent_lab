#!/usr/bin/env python3
"""scripts.ppt — presenter 技能的 PPT 后处理模块

> **不是 python-pptx**——纯 Python zipfile + XML 操作。
> 三段式 CLI: `presenter ppt <方法名> [参数]`
> 支持方法: template / tables

导出类:
- PPTXFile: zipfile 包装（PPT.py）
- TemplateEditor: 母版装饰（Template.py）
- TableStyler: 表格样式（Tables.py）
"""

from .PPT import PPTXFile
from .Template import TemplateEditor
from .Tables import TableStyler

__all__ = ["PPTXFile", "TemplateEditor", "TableStyler"]
