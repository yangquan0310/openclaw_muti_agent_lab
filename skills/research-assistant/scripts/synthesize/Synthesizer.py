#!/usr/bin/env python3
"""
Synthesizer.py - 文献综述合成主类

职责：
- 从 topic JSON 提取结构化 Markdown 笔记
- 检查综述中的参考文献引用格式（APA 7th）
- 修复 DSAM 引用为 APA 格式
- 不直接撰写综述（这是代理的工作）
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class Synthesizer:
    """文献综述合成器（初始化时绑定知识库路径）"""

    def __init__(self, *kb_paths: str):
        self.kb_paths = list(kb_paths) if kb_paths else []
        self._kb_cache: List[Dict[str, Any]] = []

    def _load_kbs(self) -> List[Dict[str, Any]]:
        """加载所有绑定的知识库。"""
        if self._kb_cache:
            return self._kb_cache
        papers: List[Dict[str, Any]] = []
        for p in self.kb_paths:
            path = Path(p)
            if not path.exists():
                continue
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                papers.extend(data.get("papers", []))
        self._kb_cache = papers
        return papers

    # ==================== 笔记提取 ====================

    def extract_notes(self, topic_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        从 topic JSON 中提取结构化笔记，输出为 Markdown。
        
        输出格式:
            ## 1. 标题
            **作者**: 作者名, et al.  
            **年份**: 2019  
            **期刊**: 期刊名  
            **引用**: 304  
            **标签**: 📖综述 🟡重要文献
            
            ### 研究问题
            ...
            
            ### 研究方法
            ...
            
            ### 研究结果
            ...
            
            ### 研究结论
            ...

        Args:
            topic_path: topic JSON 文件路径 (如 knowledge/topic/治疗期待.json)
            output_path: 输出 Markdown 文件路径（可选，默认 knowledge/note/笔记_{主题}.md）

        Returns:
            {"success": True, "output_path": ..., "count": ...}
        """
        path = Path(topic_path)
        if not path.exists():
            return {"success": False, "error": f"文件不存在: {topic_path}"}

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        papers = data.get("papers", [])
        if len(papers) < 1:
            return {"success": False, "error": "topic 中无文献", "count": 0}

        theme = data.get("topic", data.get("project", "文献笔记"))
        
        # 默认输出路径
        if not output_path:
            output_path = f"knowledge/note/笔记_{theme}.md"
        
        lines: List[str] = []
        lines.append(f"# {theme} — 文献笔记")
        lines.append("")
        lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"> 总文献: {len(papers)} 篇")
        lines.append("")
        lines.append("---")
        lines.append("")

        for i, p in enumerate(papers, 1):
            title = p.get("title", "未知标题")
            authors = p.get("authors", [])
            if len(authors) == 1:
                author_str = str(authors[0])
            elif len(authors) > 1:
                author_str = f"{authors[0]}, et al."
            else:
                author_str = "未知作者"
            year = p.get("year", "N/A")
            venue = p.get("venue", "N/A")
            citation = p.get("citationCount", 0)
            labels = p.get("labels", {})
            importance = labels.get("importance", "")
            ptype = labels.get("type", "")
            notes = p.get("notes", {})

            # 标题行
            lines.append(f"## {i}. {title}")
            lines.append("")
            
            # 元信息行
            lines.append(f"**作者**: {author_str}")
            lines.append(f"**年份**: {year}")
            if venue and venue != "N/A":
                lines.append(f"**期刊**: {venue}")
            if citation:
                lines.append(f"**引用**: {citation}")
            tag_str = ' '.join(filter(None, [ptype, importance])).strip()
            if tag_str:
                lines.append(f"**标签**: {tag_str}")
            lines.append("")
            
            # notes 结构化字段（使用 ### 三级标题）
            if isinstance(notes, dict):
                if '研究问题' in notes:
                    lines.append("### 研究问题")
                    lines.append(notes['研究问题'])
                    lines.append("")
                if '研究方法' in notes:
                    lines.append("### 研究方法")
                    lines.append(notes['研究方法'])
                    lines.append("")
                if '研究结果' in notes:
                    lines.append("### 研究结果")
                    lines.append(notes['研究结果'])
                    lines.append("")
                if '研究结论' in notes:
                    lines.append("### 研究结论")
                    lines.append(notes['研究结论'])
                    lines.append("")
                if '研究展望' in notes:
                    lines.append("### 研究展望")
                    lines.append(notes['研究展望'])
                    lines.append("")
                if '理论观点' in notes:
                    lines.append("### 理论观点")
                    lines.append(notes['理论观点'])
                    lines.append("")
                if '说明' in notes:
                    lines.append("### 说明")
                    lines.append(notes['说明'])
                    lines.append("")
            else:
                lines.append("### 笔记")
                lines.append(str(notes))
                lines.append("")
            
            lines.append("---")
            lines.append("")

        md_content = "\n".join(lines)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        return {"success": True, "output_path": str(out), "count": len(papers)}

    # ==================== 引用检查 ====================

    def check_references(self, doc_path: str) -> Dict[str, Any]:
        """
        检查文档中的文献引用是否按照 APA 7th 格式。

        Args:
            doc_path: 待检查的 Markdown 文档路径

        Returns:
            检查结果字典
        """
        doc_path_obj = Path(doc_path)
        if not doc_path_obj.exists():
            return {"success": False, "error": f"文档不存在: {doc_path}"}

        with open(doc_path_obj, "r", encoding="utf-8") as f:
            content = f.read()

        # APA 7th 格式匹配
        apa_parenthetical = re.findall(r"\([A-Z][a-zA-Z\-]+(?:,\s+\d{4}[a-z]?|\s+\&\s+[A-Z][a-zA-Z\-]+,\s+\d{4}[a-z]?)\)", content)
        apa_narrative = re.findall(r"[A-Z][a-zA-Z\-]+\s+\(\d{4}[a-z]?\)", content)

        # 非 APA 格式的可疑引用
        non_apa = re.findall(r"DSAM_\d+\b|\[\d+\]|\([12]\d{3}\)(?!\w)", content)

        return {
            "success": True,
            "apa_parenthetical": len(apa_parenthetical),
            "apa_narrative": len(apa_narrative),
            "non_apa_suspect": len(non_apa),
            "non_apa_examples": list(set(non_apa))[:10],
            "check_passed": len(non_apa) == 0,
        }

    def fix_references(self, doc_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        将文档中的 DSAM 引用替换为 APA 7th 格式。

        Args:
            doc_path: 输入文档路径
            output_path: 输出文档路径（可选，默认覆盖原文件）

        Returns:
            修复结果字典
        """
        if not self.kb_paths:
            raise ValueError("初始化时未绑定知识库路径，无法修复引用。请传入知识库路径：Synthesizer(kb_path)")

        doc_path_obj = Path(doc_path)
        if not doc_path_obj.exists():
            return {"success": False, "error": f"文档不存在: {doc_path}"}

        with open(doc_path_obj, "r", encoding="utf-8") as f:
            content = f.read()

        papers = self._load_kbs()
        seq_map: Dict[str, Dict[str, Any]] = {}
        for i, p in enumerate(papers):
            key = f"DSAM_{i:04d}"
            seq_map[key] = p
            pid = p.get("paperId", "")
            if pid:
                seq_map[pid] = p

        def _replace_ref(match: re.Match) -> str:
            ref = match.group(0)
            paper = seq_map.get(ref)
            if not paper:
                return match.group(0)
            authors = paper.get("authors", [])
            year = paper.get("year", "")
            if authors and year:
                if len(authors) == 1:
                    return f"({authors[0]}, {year})"
                elif len(authors) == 2:
                    return f"({authors[0]} & {authors[1]}, {year})"
                else:
                    return f"({authors[0]} et al., {year})"
            return match.group(0)

        fixed_content = re.sub(r"DSAM_\d+", _replace_ref, content)

        out = Path(output_path) if output_path else doc_path_obj
        with open(out, "w", encoding="utf-8") as f:
            f.write(fixed_content)

        return {"success": True, "output_path": str(out)}


# ==================== 命令行入口 ====================
if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Synthesizer - 文献综述合成工具")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # extract 命令：从 topic JSON 提取结构化笔记
    extract_parser = subparsers.add_parser("extract", help="从 topic JSON 提取结构化笔记为 Markdown")
    extract_parser.add_argument("--topic", required=True, help="topic JSON 文件路径 (如 knowledge/topic/xxx.json)")
    extract_parser.add_argument("--output", help="输出 Markdown 文件路径 (默认 knowledge/note/笔记_{主题}.md)")

    # check 命令：检查引用格式
    check_parser = subparsers.add_parser("check", help="检查引用是否符合 APA 7th 格式")
    check_parser.add_argument("--doc", required=True, help="待检查的 Markdown 文档路径")

    # fix 命令：修复 DSAM 引用
    fix_parser = subparsers.add_parser("fix", help="将 DSAM 引用修复为 APA 7th 格式")
    fix_parser.add_argument("--doc", required=True, help="待修复的 Markdown 文档路径")
    fix_parser.add_argument("--kb", required=True, action="append", help="知识库文件路径（可多次使用）")
    fix_parser.add_argument("--output", help="修复后输出路径")

    args = parser.parse_args()

    if args.command == "extract":
        synthesizer = Synthesizer()
        result = synthesizer.extract_notes(args.topic, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "check":
        synthesizer = Synthesizer()
        results = synthesizer.check_references(args.doc)
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif args.command == "fix":
        synthesizer = Synthesizer(*args.kb)
        result = synthesizer.fix_references(args.doc, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        parser.print_help()
