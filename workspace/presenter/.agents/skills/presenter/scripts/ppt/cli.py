#!/usr/bin/env python3
"""
scripts/ppt/cli.py - presenter ppt 模块的 CLI 调度

三段式调用：`presenter ppt <方法名> [参数]`
支持方法：
  template   母版装饰
    ├─ decorate         一站式装饰
    ├─ add-header       加顶部色条
    ├─ add-accent       加左侧色条
    ├─ set-cover        改封面布局
    ├─ set-fonts        改 CJK / Latin 字体
    └─ set-theme-colors 改主题色
  tables     表格样式
    └─ style            样式化所有表格
"""

import argparse
import sys
from pathlib import Path

# 让 import scripts.ppt.PPT 能找到
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.ppt.PPT import PPTXFile
from scripts.ppt.Template import TemplateEditor
from scripts.ppt.Tables import TableStyler


def build_parser() -> argparse.ArgumentParser:
    """构建 ppt 模块的 argparse"""
    parser = argparse.ArgumentParser(
        prog="presenter ppt",
        description="PPT 后处理（**不是 python-pptx**——纯 zipfile XML 操作）",
    )
    sub = parser.add_subparsers(dest="method", required=True, metavar="<方法>")

    # =========================================================
    # template 子命令
    # =========================================================
    template_p = sub.add_parser("template", help="母版装饰（decorate / add-header / add-accent / set-cover / set-fonts / set-theme-colors）")
    template_sub = template_p.add_subparsers(dest="sub_method", required=True, metavar="<子方法>")

    # template decorate
    p = template_sub.add_parser("decorate", help="一站式母版装饰（默认 teal+橙 风格）")
    p.add_argument("input", help="输入 .pptx 路径")
    p.add_argument("-o", "--output", required=True, help="输出 .pptx 路径")
    p.add_argument("--header-color", default="0096C7", help="顶栏颜色")
    p.add_argument("--accent-color", default="F4A261", help="左条 + 封面装饰块颜色")
    p.add_argument("--header-label", default="教育科学研究方法", help="顶栏文字")
    p.add_argument("--latin-font", default="Microsoft YaHei", help="拉丁字体")
    p.add_argument("--chinese-font", default="微软雅黑", help="中文字体")
    p.add_argument("--no-cover", action="store_true", help="不设置封面布局")
    p.add_argument("--no-fonts", action="store_true", help="不改字体")
    p.add_argument("--no-theme", action="store_true", help="不改主题色")

    # template add-header
    p = template_sub.add_parser("add-header", help="加顶部色条")
    p.add_argument("input", help="输入 .pptx 路径")
    p.add_argument("-o", "--output", required=True, help="输出 .pptx 路径")
    p.add_argument("--color", default="0096C7", help="顶栏颜色")
    p.add_argument("--height", type=int, default=274320, help="顶栏高度 EMU（默认 0.30\")")
    p.add_argument("--label", default="教育科学研究方法", help="顶栏文字")

    # template add-accent
    p = template_sub.add_parser("add-accent", help="加左侧色条")
    p.add_argument("input", help="输入 .pptx 路径")
    p.add_argument("-o", "--output", required=True, help="输出 .pptx 路径")
    p.add_argument("--color", default="F4A261", help="左条颜色")
    p.add_argument("--width", type=int, default=73152, help="左条宽度 EMU（默认 0.08\")")

    # template set-cover
    p = template_sub.add_parser("set-cover", help="改封面布局（全色底 + 装饰块）")
    p.add_argument("input", help="输入 .pptx 路径")
    p.add_argument("-o", "--output", required=True, help="输出 .pptx 路径")
    p.add_argument("--bg", default="0096C7", help="封面底色")
    p.add_argument("--accent", default="F4A261", help="封面装饰块颜色")

    # template set-fonts
    p = template_sub.add_parser("set-fonts", help="改 CJK / Latin 字体")
    p.add_argument("input", help="输入 .pptx 路径")
    p.add_argument("-o", "--output", required=True, help="输出 .pptx 路径")
    p.add_argument("--latin", default="Microsoft YaHei", help="拉丁字体")
    p.add_argument("--chinese", default="微软雅黑", help="中文字体")

    # template set-theme-colors
    p = template_sub.add_parser("set-theme-colors", help="改主题色（accent1-6）")
    p.add_argument("input", help="输入 .pptx 路径")
    p.add_argument("-o", "--output", required=True, help="输出 .pptx 路径")
    p.add_argument("--accent1", help="accent1 颜色（主色）")
    p.add_argument("--accent2", help="accent2 颜色（副色）")
    p.add_argument("--accent3", help="accent3 颜色")
    p.add_argument("--accent4", help="accent4 颜色")
    p.add_argument("--accent5", help="accent5 颜色")
    p.add_argument("--accent6", help="accent6 颜色")

    # =========================================================
    # tables 子命令
    # =========================================================
    tables_p = sub.add_parser("tables", help="表格样式（覆盖 Office 默认丑陋表样式）")
    tables_sub = tables_p.add_subparsers(dest="sub_method", required=True, metavar="<子方法>")

    # tables style
    p = tables_sub.add_parser("style", help="样式化所有表格")
    p.add_argument("input", help="输入 .pptx 路径")
    p.add_argument("-o", "--output", required=True, help="输出 .pptx 路径")
    p.add_argument("--header-color", default="0096C7", help="表头底色")
    p.add_argument("--alt-row-color", default="F8F9FA", help="隔行底色")
    p.add_argument("--data-row-color", default="FFFFFF", help="数据行底色")
    p.add_argument("--border-color", default="D0D0D0", help="边框色")
    p.add_argument("--header-text-color", default="FFFFFF", help="表头字色")
    p.add_argument("--data-text-color", default="1A1A1A", help="数据字色")
    p.add_argument("--latin-font", default="Microsoft YaHei", help="拉丁字体")
    p.add_argument("--chinese-font", default="微软雅黑", help="中文字体")
    p.add_argument("--font-size", type=int, default=1100, help="字号（1/100 pt）")

    # tables strip-media
    p = tables_sub.add_parser("strip-media", help="删除未被引用的媒体文件（图片 / 视频，瘦身 .pptx 80 percent）")
    p.add_argument("input", help="输入 .pptx 路径")
    p.add_argument("-o", "--output", required=True, help="输出 .pptx 路径")


    return parser


def run() -> int:
    """ppt 模块 CLI 入口"""
    parser = build_parser()
    args = parser.parse_args()
    ppt = PPTXFile(args.input)
    editor = TemplateEditor(ppt)

    if args.method == "template":
        if args.sub_method == "decorate":
            editor.decorate(
                args.output,
                header_color=args.header_color,
                accent_color=args.accent_color,
                header_label=args.header_label,
                latin_font=args.latin_font,
                chinese_font=args.chinese_font,
                set_cover=not args.no_cover,
                set_fonts=not args.no_fonts,
                set_theme=not args.no_theme,
            )
            print(f"✓ 一站式装饰完成: {args.output}")
        elif args.sub_method == "add-header":
            editor.add_header(args.output, color=args.color, height=args.height, label=args.label)
            print(f"✓ 顶栏添加完成: {args.output}")
        elif args.sub_method == "add-accent":
            editor.add_accent(args.output, color=args.color, width=args.width)
            print(f"✓ 左条添加完成: {args.output}")
        elif args.sub_method == "set-cover":
            editor.set_cover(args.output, bg_color=args.bg, accent_color=args.accent)
            print(f"✓ 封面布局设置完成: {args.output}")
        elif args.sub_method == "set-fonts":
            editor.set_fonts(args.output, latin_font=args.latin, chinese_font=args.chinese)
            print(f"✓ 字体设置完成: {args.output}")
        elif args.sub_method == "set-theme-colors":
            editor.set_theme_colors(
                args.output,
                accent1=args.accent1,
                accent2=args.accent2,
                accent3=args.accent3,
                accent4=args.accent4,
                accent5=args.accent5,
                accent6=args.accent6,
            )
            print(f"✓ 主题色设置完成: {args.output}")
        else:
            parser.parse_args(["template", "--help"])
            return 1
    elif args.method == "tables":
        if args.sub_method == "style":
            styler = TableStyler(ppt)
            result = styler.style(
                args.output,
                header_color=args.header_color,
                alt_row_color=args.alt_row_color,
                data_row_color=args.data_row_color,
                border_color=args.border_color,
                header_text_color=args.header_text_color,
                data_text_color=args.data_text_color,
                latin_font=args.latin_font,
                chinese_font=args.chinese_font,
                font_size=args.font_size,
            )
            print(f"✓ 样式化 {result['tables_styled']} 张表格（slide {result['slides']}）")
        elif args.sub_method == "strip-media":
            result = ppt.strip_unused_media(args.output)
            print(f"✓ 删除 {result['removed']} 个未引用媒体，节省 {result['saved_bytes'] / 1024:.1f} KB")
            for f in result['removed_files']:
                print(f"    - {f}")
        else:
            parser.parse_args(["tables", "--help"])
            return 1
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
