#!/usr/bin/env python3
"""
Synthesizer.py - 文献综述合成主类

作为 synthesize 模块的统一入口，协调 NoteExtractor 和 ReferenceChecker
完成综述撰写过程中的笔记提取与引用检查工作。
"""

import json
from typing import Dict, List, Optional, Any
from synthesize.NoteExtractor import NoteExtractor
from synthesize.ReferenceChecker import ReferenceChecker


class Synthesizer:
    """文献综述合成器 - 协调笔记提取与引用检查（初始化时绑定知识库路径）"""

    def __init__(self, *kb_paths: str):
        """
        初始化合成器（绑定一个或多个知识库路径）

        Args:
            *kb_paths: 知识库文件路径（可传入多个，用于引用检查）
        """
        self.kb_paths = list(kb_paths) if kb_paths else []
        self._extractor = NoteExtractor()
        self._checker = ReferenceChecker(*self.kb_paths) if self.kb_paths else None

    def extract(self, notes_path: str) -> Dict[str, Any]:
        """
        从知识库笔记文件中提取结构化信息

        Args:
            notes_path: 笔记 JSON 文件路径

        Returns:
            包含提取信息的字典（文献数量、统计、研究问题、方法、结果等）
        """
        return self._extractor.extract(notes_path)

    def check_references(self, doc_path: str) -> Dict[str, Any]:
        """
        检查文档中的参考文献引用是否正确

        Args:
            doc_path: 待检查的 Markdown 文档路径

        Returns:
            检查结果字典

        Raises:
            ValueError: 如果初始化时未绑定知识库路径
        """
        if not self._checker:
            raise ValueError("初始化时未绑定知识库路径，无法检查引用。请传入知识库路径：Synthesizer(kb_path)")
        return self._checker.check_references(doc_path)

    def fix_references(self, doc_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        修复文档中的引用格式（将 DSAM 引用替换为 APA 格式）

        注意：必须先调用 check_references() 构建引用映射，再调用此方法。

        Args:
            doc_path: 输入文档路径
            output_path: 输出文档路径（可选，默认覆盖原文件）

        Returns:
            修复结果字典

        Raises:
            ValueError: 如果初始化时未绑定知识库路径
        """
        if not self._checker:
            raise ValueError("初始化时未绑定知识库路径，无法修复引用。请传入知识库路径：Synthesizer(kb_path)")
        return self._checker.fix_references(doc_path, output_path)


# ==================== 命令行入口 ====================
if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Synthesizer - 文献综述合成工具")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # extract 命令
    extract_parser = subparsers.add_parser("extract", help="从知识库提取结构化信息")
    extract_parser.add_argument("--notes", required=True, help="知识库 JSON 文件路径")

    # check 命令
    check_parser = subparsers.add_parser("check", help="检查参考文献引用")
    check_parser.add_argument("--doc", required=True, help="待检查的 Markdown 文档路径")
    check_parser.add_argument("--kb", required=True, action="append", help="知识库文件路径（可多次使用）")

    # fix 命令
    fix_parser = subparsers.add_parser("fix", help="修复参考文献引用")
    fix_parser.add_argument("--doc", required=True, help="待修复的 Markdown 文档路径")
    fix_parser.add_argument("--kb", required=True, action="append", help="知识库文件路径（可多次使用）")
    fix_parser.add_argument("--output", help="修复后输出路径")

    args = parser.parse_args()

    if args.command == "extract":
        synthesizer = Synthesizer()
        result = synthesizer.extract(args.notes)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "check":
        synthesizer = Synthesizer(*args.kb)
        results = synthesizer.check_references(args.doc)
        print(f"检查完成!")
        print(f"DSAM引用总数: {results['stats']['dsam_total']}")
        print(f"缺失引用: {results['stats']['missing_count']}")
        if results["missing_references"]:
            print(f"缺失的引用: {results['missing_references']}")

    elif args.command == "fix":
        synthesizer = Synthesizer(*args.kb)
        synthesizer.check_references(args.doc)  # 先构建映射
        fix_result = synthesizer.fix_references(args.doc, args.output)
        if fix_result["success"]:
            print(f"修复完成! 输出: {fix_result['output_path']}")
        else:
            print(f"修复失败: {fix_result.get('error', '未知错误')}")
            sys.exit(1)

    else:
        parser.print_help()
