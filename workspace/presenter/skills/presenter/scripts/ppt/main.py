#!/usr/bin/env python3
"""
CLI 统一入口：课件脚本 → PPTX 编译。

工作流：
  1. 编写脚本：人工根据 content-layout-matching.md 参考指南选择 @layout
  2. 扩展模板（如需）：使用 extend 添加自定义 layout 原型
  3. 编译：将脚本编译为 PPTX

Usage:
    # 列出模板所有 layouts
    python3 main.py list --template template

    # 扩展模板，添加自定义 layout
    python3 main.py extend --template template --add timeline flowchart

    # 编译脚本
    python3 main.py compile --input script.md --output out.pptx --template template
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

if __name__ == "__main__" and __package__ is None:
    import os
    # 脚本在 scripts/ppt/ 下，模块也在 scripts/ppt/ 下
    # 往上一级是 scripts/，再往上一级是技能根目录
    skill_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, skill_root)
    # 由于脚本在 scripts/ppt/ 下，导入时需要加上 ppt 前缀
    from scripts.ppt.ScriptParser import ScriptParser
    from scripts.ppt.PptxCompiler import PptxCompiler
    from scripts.ppt.TemplateExtender import TemplateExtender
    from scripts.ppt.LayoutImporter import LayoutImporter
else:
    from .ScriptParser import ScriptParser
    from .PptxCompiler import PptxCompiler
    from .TemplateExtender import TemplateExtender
    from .LayoutImporter import LayoutImporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def _resolve_template(name: str) -> Path:
    """从 assets/ 目录解析模板路径。"""
    base = Path(__file__).parent.parent.parent / "assets" / "templates"
    p = Path(name)
    if p.exists():
        return p
    for ext in ["", ".pptx"]:
        candidate = base / f"{name}{ext}"
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"模板未找到: {name} (在 {base} 中查找)")


def cmd_parse(args: argparse.Namespace) -> int:
    """解析脚本为 JSON。"""
    parser = ScriptParser()
    pages = parser.parse(args.input)
    result = {"success": True, "pages": pages, "count": len(pages)}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("解析结果已保存: %s", args.output)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """列出模板所有 slide_layouts。"""
    template_path = _resolve_template(args.template)
    compiler = PptxCompiler(template_path)
    info = compiler.list_layouts()
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


def cmd_extend(args: argparse.Namespace) -> int:
    """扩展模板，添加自定义 slide_layout。"""
    template_path = _resolve_template(args.template)
    extender = TemplateExtender(template_path)

    for layout_type in args.add:
        idx = extender.add_layout(layout_type, f"自定义_{layout_type}")
        print(f"✅ 已添加 {layout_type} slide_layout，索引: {idx}")

    output = args.output or template_path
    extender.save(output)
    print(f"\n模板已保存: {output}")
    return 0


def cmd_import_layout(args: argparse.Namespace) -> int:
    """从源PPT导入slides为新的slide_layout。"""
    source_path = Path(args.source)
    if not source_path.exists():
        # 尝试在assets目录查找
        base = Path(__file__).parent.parent / "assets"
        for ext in ["", ".pptx"]:
            candidate = base / f"{args.source}{ext}"
            if candidate.exists():
                source_path = candidate
                break

    if not source_path.exists():
        print(f"错误: 源PPT未找到: {args.source}")
        return 1

    target_path = _resolve_template(args.template)
    importer = LayoutImporter(source_path, target_path)

    if args.analyze:
        candidates = importer.analyze_source()
        print(json.dumps(candidates[:10], ensure_ascii=False, indent=2))
        return 0

    if args.auto:
        candidates = importer.analyze_source()
        slide_indices = [c["index"] for c in candidates[:args.top]]
        print(f"自动选择 {len(slide_indices)} 个slides: {slide_indices}")
    elif args.slides:
        slide_indices = [int(x.strip()) for x in args.slides.split(",")]
    else:
        print("错误: 请指定 --slides 或 --auto")
        return 1

    result = importer.import_slides(slide_indices)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """验证脚本合法性。"""
    parser = ScriptParser()
    try:
        pages = parser.parse(args.input)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "errors": [f"解析失败: {e}"],
            "pages": 0,
        }, ensure_ascii=False, indent=2))
        return 1

    # 获取模板 layouts
    template_path = _resolve_template(args.template)
    compiler = PptxCompiler(template_path)
    layouts_info = compiler.list_layouts()
    max_layout_idx = len(layouts_info["layouts"]) - 1

    errors = []
    warnings = []

    for i, page in enumerate(pages):
        page_num = i + 1
        layout_idx = int(page.get("layout", 0))
        structure = page.get("structure", "list")
        lines = page.get("lines", [])

        # 检查 layout 越界
        if layout_idx > max_layout_idx:
            errors.append(f"第{page_num}页: layout 索引 {layout_idx} 越界（最大 {max_layout_idx}）")

        # 检查 structure 有效性
        valid_structures = ["cover", "list", "table", "timeline", "flowchart", "compare", "cards", "section", "toc", "quote", "stats"]
        if structure not in valid_structures:
            errors.append(f"第{page_num}页: 无效的 @structure '{structure}'（有效值: {', '.join(valid_structures)}）")

        # 检查核心内容
        if not lines or len(lines) == 0:
            errors.append(f"第{page_num}页: 缺少核心内容")
        elif len(lines) > 10:
            warnings.append(f"第{page_num}页: 内容较多（{len(lines)}条），建议拆分为多页")

        # 检查内容溢出风险
        total_chars = sum(len(l) for l in lines)
        if total_chars > 500:
            warnings.append(f"第{page_num}页: 内容较长（{total_chars}字符），可能溢出")

    result = {
        "success": len(errors) == 0,
        "pages": len(pages),
        "errors": errors,
        "warnings": warnings,
        "max_layout_idx": max_layout_idx,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if errors:
        print("\n❌ 验证失败，共 {} 个错误".format(len(errors)))
        return 1
    elif warnings:
        print("\n⚠️ 验证通过，但有 {} 个警告".format(len(warnings)))
        return 0
    else:
        print("\n✅ 验证通过")
        return 0


def cmd_compile(args: argparse.Namespace) -> int:
    """编译脚本为 PPTX。"""
    parser = ScriptParser()
    pages = parser.parse(args.input)
    logger.info("脚本解析完成: %d 页", len(pages))

    # 优先使用命令行指定的 theme，否则使用脚本元数据中的 theme
    metadata = parser.get_metadata()
    cmd_theme = getattr(args, "theme", None)
    if cmd_theme:
        theme = cmd_theme  # 命令行显式指定
    elif metadata.get("theme"):
        theme = metadata["theme"]
        logger.info("使用脚本元数据中的 theme: %s", theme)
    else:
        theme = "blue"

    template_path = _resolve_template(args.template)
    logger.info("使用模板: %s", template_path)

    compiler = PptxCompiler(template_path, theme=theme)
    for page in pages:
        compiler.compile_page(
            int(page["layout"]),
            page["lines"],
            structure=page.get("structure", "list"),
            chart_design=page.get("chart_design", "")
        )

    compiler.save(args.output)
    print(json.dumps({
        "success": True,
        "output": str(args.output),
        "pages": len(pages),
        "template": str(template_path),
        "theme": theme,
    }, ensure_ascii=False, indent=2))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="PowerPoint-presenter CLI")
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # parse 子命令
    p_parse = sub.add_parser("parse", help="解析 .md 脚本为 JSON")
    p_parse.add_argument("--input", required=True, type=Path, help="输入脚本 .md 文件")
    p_parse.add_argument("--output", type=Path, help="输出 JSON 文件路径")
    p_parse.set_defaults(func=cmd_parse)

    # list 子命令
    p_list = sub.add_parser("list", help="列出模板所有 layouts 和原型 slides")
    p_list.add_argument("--template", required=True, help="模板名称或路径")
    p_list.set_defaults(func=cmd_list)

    # extend 子命令
    p_extend = sub.add_parser("extend", help="扩展模板，添加自定义 layout")
    p_extend.add_argument("--template", required=True, help="模板名称或路径")
    p_extend.add_argument("--add", nargs="+", required=True, help="添加的 layout 类型 (timeline/flowchart/cards/table)")
    p_extend.add_argument("--output", type=Path, help="输出路径（默认覆盖原模板）")
    p_extend.set_defaults(func=cmd_extend)

    # import-layout 子命令
    p_import = sub.add_parser("import-layout", help="从源PPT导入slides为新的slide_layout")
    p_import.add_argument("--source", required=True, help="源PPT路径（或assets/下的文件名）")
    p_import.add_argument("--template", required=True, help="目标模板名称或路径")
    p_import.add_argument("--slides", type=str, help="要导入的slide索引（逗号分隔）")
    p_import.add_argument("--auto", action="store_true", help="自动导入最有代表性的slides")
    p_import.add_argument("--top", type=int, default=5, help="自动导入时选择前N个")
    p_import.add_argument("--analyze", action="store_true", help="仅分析源模板，列出有代表性的slides")
    p_import.set_defaults(func=cmd_import_layout)

    # validate 子命令
    p_validate = sub.add_parser("validate", help="验证脚本合法性（编译前检查）")
    p_validate.add_argument("--input", required=True, type=Path, help="输入脚本 .md 文件")
    p_validate.add_argument("--template", required=True, help="模板名称或路径")
    p_validate.set_defaults(func=cmd_validate)

    # compile 子命令
    p_compile = sub.add_parser("compile", help="编译 .md 脚本为 .pptx")
    p_compile.add_argument("--input", required=True, type=Path, help="输入脚本 .md 文件")
    p_compile.add_argument("--output", required=True, type=Path, help="输出 .pptx 文件路径")
    p_compile.add_argument("--template", required=True, help="模板名称或路径")
    p_compile.add_argument("--theme", choices=["blue", "green", "purple", "orange", "gray"],
                           help="配色主题（可选，默认 blue）")
    p_compile.set_defaults(func=cmd_compile)

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
