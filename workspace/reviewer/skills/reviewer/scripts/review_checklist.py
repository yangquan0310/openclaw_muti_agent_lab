#!/usr/bin/env python3
"""
审稿清单脚本 - reviewer 技能配套工具
用于结构化审稿检查，辅助生成审稿意见

使用方法：
    python3 scripts/review_checklist.py --type thesis paper.pdf
    python3 scripts/review_checklist.py --type journal paper.pdf
"""

import argparse
import sys
from pathlib import Path

# 审稿维度定义
REVIEW_DIMENSIONS = {
    "importance": {
        "name": "选题的重要性",
        "items": [
            "理论重要性：是否有重要理论意义",
            "实践意义：是否有重要实践价值",
            "适切性：是否适合目标读者群",
        ],
    },
    "literature": {
        "name": "文献综述质量",
        "items": [
            "文献覆盖：是否覆盖重要相关文献",
            "研究框架：文献与问题是否密切相关",
            "批判眼光：是否指出研究局限",
            "文献处理：是否分析整合而非堆砌",
        ],
    },
    "research_question": {
        "name": "问题提出",
        "items": [
            "研究问题恰当性：分析单元是否正确",
            "逻辑正确：变量界定是否清楚",
            "表述清楚：目的、假设是否明确",
        ],
    },
    "methodology": {
        "name": "研究方法",
        "items": [
            "被试：取样是否有代表性",
            "设备和材料：是否有信度效度",
            "研究设计：是否能回答研究问题",
            "数据收集：是否正确处理异常数据",
        ],
    },
    "analysis": {
        "name": "数据分析",
        "items": [
            "统计分析：方法是否正确",
            "结果表达：顺序是否合理",
            "公正客观：是否只报告有利数据",
        ],
    },
    "discussion": {
        "name": "讨论和结论",
        "items": [
            "结果解释：是否联系假设和目的",
            "研究意义：意义是否具体",
            "研究局限：是否实事求是",
        ],
    },
    "writing": {
        "name": "文稿呈现",
        "items": [
            "写作质量：是否流畅清晰",
            "符合规范：格式是否正确",
        ],
    },
    "contribution": {
        "name": "研究贡献",
        "items": [
            "理论/实践/方法贡献是否明确",
            "文献价值：是否超越以往研究",
        ],
    },
}

# 学位论文专项
THESIS_ADDITIONAL = {
    "depth": {
        "name": "研究深度与工作量",
        "items": [
            "是否展示完整研究过程",
            "数据量/实验量是否足够",
            "分析深度是否充足",
        ],
    },
    "innovation": {
        "name": "创新性",
        "items": [
            "创新点表述是否清晰",
            "创新程度是否达到要求",
            "与现有工作差异是否明确",
        ],
    },
    "ethics": {
        "name": "研究伦理",
        "items": [
            "人类被试保护声明",
            "数据伦理说明",
            "学术诚信规范",
        ],
    },
}


def generate_checklist(paper_type: str, include_additional: bool = False) -> str:
    """生成审稿清单"""
    output = []
    output.append(f"# 审稿清单 - {paper_type}\n")
    output.append("使用方法：逐项检查，在 [ ] 中标记 ✅/❌\n")

    for key, dim in REVIEW_DIMENSIONS.items():
        output.append(f"\n## {dim['name']}\n")
        for item in dim["items"]:
            output.append(f"- [ ] {item}")

    if include_additional and paper_type == "thesis":
        output.append("\n## 学位论文专项\n")
        for key, dim in THESIS_ADDITIONAL.items():
            output.append(f"\n### {dim['name']}\n")
            for item in dim["items"]:
                output.append(f"- [ ] {item}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="审稿清单生成工具")
    parser.add_argument("--type", "-t", choices=["thesis", "journal", "opensource", "course", "proposal"],
                        default="journal", help="论文类型")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("paper", nargs="?", help="论文文件路径（可选）")

    args = parser.parse_args()

    include_additional = args.type == "thesis"
    checklist = generate_checklist(args.type, include_additional)

    if args.output:
        Path(args.output).write_text(checklist)
        print(f"审稿清单已保存到: {args.output}")
    else:
        print(checklist)


if __name__ == "__main__":
    main()
