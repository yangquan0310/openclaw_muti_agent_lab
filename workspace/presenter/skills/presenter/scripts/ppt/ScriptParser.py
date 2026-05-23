#!/usr/bin/env python3
"""
课件脚本解析器 — 结构化丰富模式 v2.0

支持解析含结构化内容的丰富脚本，内容类型与 Layout 一一配对。

内容结构标记（@structure）：
  @list     — 列表（默认，标题+内容条目）
  @table    — 表格（多行多列数据）
  @timeline — 时间轴（按时间顺序排列的事件）
  @flowchart— 流程图（线性步骤、箭头连接）
  @compare  — 双栏对比（左右对比布局）
  @cards    — 卡片网格（并列特征、分类归纳）
  @cover    — 封面（课程名称、章节、教师信息）
  @section  — 章节分隔（大字+简洁装饰）

Layout 标记：
  **母版布局**：N  或  @layout: N

支持的元信息标记：
  **页面描述**：页面功能说明
  **核心内容**：页面文字内容（必需，支持 @structure 子标记）
  **图表设计**：图表、图形、排版建议
  **互动设计**：课堂互动、提问设计
  **备注**：教学备注、时间控制

Usage:
    python3 ScriptParser.py --input script.md
    python3 ScriptParser.py --input script.md --output script.json
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# 内容结构 → Layout 画布选择
# 核心原则：Layout 只是画布，Slide 内容由编译器自主绘制
# 默认使用"标题和内容"作为通用画布，特殊情况用有占位符位置的 layout
STRUCTURE_LAYOUT_MAP = {
    "cover":     0,  # 标题幻灯片（母版背景+页脚）
    "list":      1,  # 标题和内容（通用画布）
    "table":     1,  # 标题和内容（通用画布）
    "timeline":  1,  # 标题和内容（通用画布）
    "flowchart": 1,  # 标题和内容（通用画布）
    "compare":   3,  # 两栏内容（有左右占位符位置参考）
    "cards":     1,  # 标题和内容（通用画布）
    "section":   2,  # 节标题（有标题占位符位置参考）
    "toc":       1,  # 目录页（通用画布）
    "quote":     1,  # 引用页（通用画布）
    "stats":     1,  # 统计页（通用画布）
}


class ScriptParser:
    """解析结构化丰富模式课件脚本。"""

    # 支持的元信息标记（支持别名映射）
    META_TAGS = ["页面描述", "母版布局", "核心内容", "图表设计", "互动设计", "备注"]
    # 别名映射：非标准标记名 → 标准标记名
    TAG_ALIASES = {
        "核心文字内容": "核心内容",
        "图表互动设计说明": "图表设计",
        "图表互动设计": "图表设计",
    }

    def __init__(self) -> None:
        self.pages: List[Dict[str, Any]] = []
        self.metadata: Dict[str, str] = {}  # 文档级元数据

    def get_metadata(self) -> Dict[str, str]:
        """返回文档级元数据（从 front matter 解析）。"""
        return self.metadata

    # ========== 公有接口 ==========

    def parse(self, input_path: Path) -> List[Dict[str, Any]]:
        """解析脚本文件，返回页面列表。"""
        if not input_path.exists():
            raise FileNotFoundError(f"脚本文件不存在: {input_path}")

        text = input_path.read_text(encoding="utf-8")
        self.pages = self._parse_text(text)
        logger.info("解析完成: %d 页", len(self.pages))
        return self.pages

    def parse_string(self, text: str) -> List[Dict[str, Any]]:
        """从字符串直接解析。"""
        self.pages = self._parse_text(text)
        return self.pages

    # ========== 私有方法 ==========

    def _parse_text(self, text: str) -> List[Dict[str, Any]]:
        pages = []

        # 解析 YAML front matter 元数据
        text = self._parse_front_matter(text)

        # 按 ## 第N页 或 ### 第N页 分割（支持可选标题）
        # 使用 (?:^|\n) 匹配行首或换行后，支持文件第一行就是 ## 的情况
        parts = re.split(r"(?:^|\n)##+ 第\d+页.*?(?:\n|$)", text)
        headers = re.findall(r"(?:^|\n)##+ (第\d+页.*?)(?:\n|$)", text)

        # 第一个 parts[0] 是文件标题或前言，跳过
        for i, block in enumerate(parts[1:], start=1):
            header = headers[i - 1] if i - 1 < len(headers) else f"第{i}页"
            page = self._parse_page_block(header, block)
            if page:
                pages.append(page)

        return pages

    def _parse_front_matter(self, text: str) -> str:
        """解析 YAML front matter，提取文档级元数据。"""
        # 匹配 --- 包裹的 front matter
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if not fm_match:
            return text

        fm_content = fm_match.group(1)
        for line in fm_content.split("\n"):
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                self.metadata[key.strip()] = value.strip()

        logger.debug("解析 front matter: %s", self.metadata)
        # 返回去掉 front matter 后的正文
        return text[fm_match.end():]

    def _parse_page_block(self, header: str, block: str) -> Optional[Dict[str, Any]]:
        """解析单个页面块，提取所有元信息和结构化内容。"""
        lines = block.strip().split("\n")
        if not lines:
            return None

        # 初始化页面数据
        page = {
            "title": header,
            "layout": None,
            "structure": "list",  # 默认内容结构
            "lines": [],
            "description": "",
            "chart_design": "",
            "interaction": "",
            "notes": "",
        }

        # 第一步：扫描全局标记（@layout, @structure）
        remaining_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            # 检测 @layout: N
            layout_match = re.match(r"^@layout\s*[:：]\s*(\d+)$", stripped)
            if layout_match:
                page["layout"] = layout_match.group(1)
                continue
            # 检测 @structure: type
            structure_match = re.match(r"^@structure\s*[:：]\s*(\w+)$", stripped)
            if structure_match:
                page["structure"] = structure_match.group(1)
                continue
            remaining_lines.append(line)

        # 第二步：解析元信息标记
        current_tag = None
        content_buffer = []

        for line in remaining_lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped == "---":
                continue

            # 检测标记行：**标记**：内容
            tag_match = re.match(r"^\*\*(.+?)\*\*\s*[：:]\s*(.*)$", stripped)
            if tag_match:
                self._save_tag_content(page, current_tag, content_buffer)
                raw_tag = tag_match.group(1).strip()
                current_tag = self.TAG_ALIASES.get(raw_tag, raw_tag)
                initial_content = tag_match.group(2).strip()
                content_buffer = [initial_content] if initial_content else []
                continue

            # 检测 @structure 在核心内容内部
            if current_tag == "核心内容":
                struct_match = re.match(r"^@(\w+)\s*$", stripped)
                if struct_match:
                    struct_type = struct_match.group(1)
                    if struct_type in STRUCTURE_LAYOUT_MAP:
                        page["structure"] = struct_type
                        continue

            if current_tag:
                content_buffer.append(stripped)

        # 保存最后一个标记
        self._save_tag_content(page, current_tag, content_buffer)

        # 处理核心内容：去掉 markdown 列表前缀
        if page["lines"]:
            cleaned_lines = []
            for line in page["lines"]:
                line = re.sub(r"^[-*•]\s+", "", line)
                line = re.sub(r"^\d+\.\s+", "", line)
                cleaned_lines.append(line)
            page["lines"] = cleaned_lines

        # 自动推断 layout（如果未指定）
        if not page["layout"]:
            auto_layout = STRUCTURE_LAYOUT_MAP.get(page["structure"], 1)
            logger.debug("页面 '%s' 未指定 **母版布局**，根据 structure='%s' 自动推断为 %s",
                        header, page["structure"], auto_layout)
            page["layout"] = str(auto_layout)

        if not page["lines"]:
            logger.warning("页面 '%s' 无 **核心内容**", header)

        return page

    def _save_tag_content(self, page: Dict[str, Any], tag: Optional[str], content: List[str]) -> None:
        """将缓冲的内容保存到页面数据的对应字段。"""
        if not tag or not content:
            return

        text = "\n".join(content).strip()
        if not text:
            return

        if tag == "母版布局":
            m = re.search(r"(\d+)", text)
            page["layout"] = m.group(1) if m else text
        elif tag == "核心内容":
            page["lines"] = content
        elif tag == "页面描述":
            page["description"] = text
        elif tag == "图表设计":
            page["chart_design"] = text
        elif tag == "互动设计":
            page["interaction"] = text
        elif tag == "备注":
            page["notes"] = text


# ========== CLI 入口 ==========

def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="课件脚本解析器（结构化丰富模式 v2.0）")
    parser.add_argument("--input", required=True, type=Path, help="输入脚本文件路径(.md)")
    parser.add_argument("--output", type=Path, help="输出 JSON 文件路径(可选)")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    try:
        parser = ScriptParser()
        pages = parser.parse(args.input)
        result = {"success": True, "pages": pages, "count": len(pages)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.info("结果已保存到 %s", args.output)
        return 0
    except Exception as exc:
        logger.error("解析失败: %s", exc)
        import traceback
        traceback.print_exc()
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
