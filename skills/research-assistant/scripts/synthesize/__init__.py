"""synthesize/ - 综述素材抽取（从 body 抽 "一句话总结" + "关键内容"）

工具边界：返字段、返路径，不攥写 narrative。
"""

from scripts.synthesize.synthesizer import Synthesizer

__all__ = ["Synthesizer"]