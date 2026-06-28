"""summarize/ - 单篇笔记生成（基于规则分类 + 关键内容提取）

工具边界：返字段、返路径，不攥写 narrative。
"""

from scripts.summarize.summarizer import Summarizer

__all__ = ["Summarizer"]