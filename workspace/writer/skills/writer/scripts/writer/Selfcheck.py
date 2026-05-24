#!/usr/bin/env python3
"""
writer技能自检脚本
用法: python3 selfcheck.py --file <path> [--level <sentence|paragraph|chapter>]
"""

import argparse
import re
import sys
from pathlib import Path

# 问题模式
PROBLEMS = {
    "evidence_tone": {
        "pattern": re.compile(r"这一表明|这一推断|确证|诱导了|表明工作自我|背后是|证明了|确认了"),
        "label": "🔴 证据层语气问题",
        "desc": "证据层使用了推断语气，应改为描述性陈述"
    },
    "filler_words": {
        "pattern": re.compile(r"此外|另外|同时|由此可见|总而言之"),
        "label": "🟡 填充词",
        "desc": "使用了口语填充词，建议删除或用具体逻辑词替代"
    },
    "citation_bare": {
        "pattern": re.compile(r"(?<![@[\w])\w+\d{4}"),
        "label": "🔴 疑似裸引用",
        "desc": "发现疑似未加括号的裸引用，需核实格式是否规范"
    },
    "filler_words_context": {
        "pattern": re.compile(r"造成|导致|产生|使得"),
        "label": "🟡 弱动词",
        "desc": "使用了模糊动词，建议用更精确的动词替代"
    }
}

def check_file(filepath: str, level: str = "all") -> list:
    """检查文件并返回问题列表"""
    path = Path(filepath)
    if not path.exists():
        return [{"error": f"文件不存在: {filepath}"}]
    
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    issues = []
    
    for lineno, line in enumerate(lines, 1):
        for check_type, check_info in PROBLEMS.items():
            if check_info["pattern"].search(line):
                issues.append({
                    "type": check_type,
                    "label": check_info["label"],
                    "desc": check_info["desc"],
                    "line": lineno,
                    "text": line.strip()[:80]
                })
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="writer技能自检脚本")
    parser.add_argument("--file", required=True, help="要检查的文件路径")
    parser.add_argument("--level", default="all", 
                        choices=["all", "sentence", "paragraph", "chapter"],
                        help="检查层级")
    args = parser.parse_args()
    
    issues = check_file(args.file, args.level)
    
    if not issues:
        print(f"✅ {args.file} — 检查通过，未发现问题")
        return 0
    
    print(f"⚠️  {args.file} — 发现 {len(issues)} 个问题:\n")
    
    current_label = None
    for issue in issues:
        if issue.get("error"):
            print(f"❌ {issue['error']}")
            continue
        if issue["label"] != current_label:
            print(f"\n{issue['label']}")
            print(f"   {issue['desc']}")
            current_label = issue["label"]
        print(f"   L{issue['line']}: {issue['text']}")
    
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
