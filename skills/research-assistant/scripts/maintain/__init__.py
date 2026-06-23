"""Maintainer 模块（v6.0.6+：精简到 WikiZoteroManager 单一入口）

v6.0.6 清理（按 v6.0.5 专项审计报告 #4）：
  - 删除 Maintainer.py（v5.14.0 旧协调器，无外部引用）
  - 实际维护能力全部由 WikiZoteroManager 类方法承担
  - 协调器角色已合并到 WikiZoteroManager（v5.21.2 起不再有 hooks/ SOP 中间层）
"""

from .WikiZoteroManager import WikiZoteroManager

__all__ = ["WikiZoteroManager"]