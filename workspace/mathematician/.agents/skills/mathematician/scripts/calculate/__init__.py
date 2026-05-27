"""calculate package - 数值计算工具"""

from .Calculate import Calculate

__all__ = ["Calculate"]


def main():
    """CLI 入口，代理到 Calculate.main()"""
    return Calculate.main()
