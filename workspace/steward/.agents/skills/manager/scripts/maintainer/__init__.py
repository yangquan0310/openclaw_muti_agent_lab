#!/usr/bin/env python3
"""
manager - 大管家管理技能脚本模块
整合 thesis/course/program 三类项目管理功能

OOP设计：
- BaseMaintainer: 父类，封装共性
- ThesisMaintainer: 论文项目子类
- CourseMaintainer: 课程项目子类
- ProgramMaintainer: 程序项目子类
"""

from .BaseMaintainer import BaseMaintainer
from .ThesisMaintainer import ThesisMaintainer
from .CourseMaintainer import CourseMaintainer
from .ProgramMaintainer import ProgramMaintainer

# 向后兼容别名
Maintainer = BaseMaintainer

__all__ = [
    "BaseMaintainer",
    "ThesisMaintainer",
    "CourseMaintainer",
    "ProgramMaintainer",
    "Maintainer",
]
