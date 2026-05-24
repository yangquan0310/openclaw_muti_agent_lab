"""visualize package - 数据可视化工具"""

from .Visualize import Visualize

__all__ = ["Visualize"]


def main():
    """CLI 入口，代理到 Visualize.main()"""
    return Visualize.main()
