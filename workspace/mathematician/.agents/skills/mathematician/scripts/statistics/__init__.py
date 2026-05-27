"""statistics package - 统计分析工具"""

from .Statistics import Statistics

__all__ = ["Statistics"]


def main():
    """CLI 入口，代理到 Statistics.main()"""
    return Statistics.main()
