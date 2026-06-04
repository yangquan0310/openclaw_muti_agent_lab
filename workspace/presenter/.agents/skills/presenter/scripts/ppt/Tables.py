#!/usr/bin/env python3
"""
Tables.py — 表格样式类

> 表格样式方法：
> - style: 样式化所有表格（覆盖 Office 默认丑陋表样式）
> - style_xml: 样式化单个 slide 的 XML 字符串

> **不是 python-pptx**——纯 Python zipfile + XML 操作。
> 设计原则：每个方法只做一件事。
"""

import re
from typing import Optional
from .PPT import PPTXFile


MARGIN_LR = 91440   # 0.1" 单元格左右内边距
MARGIN_TB = 45720   # 0.05" 单元格上下内边距


class TableStyler:
    """表格样式编辑器。复用同一个 PPTXFile 实例。"""

    def __init__(self, ppt: PPTXFile):
        self.ppt = ppt
        if not ppt._loaded:
            ppt.load()

    # =========================================================
    # 主方法：样式化 .pptx 中所有表格
    # =========================================================
    def style(
        self,
        output_path: str,
        header_color: str = "0096C7",
        alt_row_color: str = "F8F9FA",
        data_row_color: str = "FFFFFF",
        border_color: str = "D0D0D0",
        header_text_color: str = "FFFFFF",
        data_text_color: str = "1A1A1A",
        latin_font: str = "Microsoft YaHei",
        chinese_font: str = "微软雅黑",
        font_size: int = 1100,   # 1/100 pt，1100 = 11pt
    ) -> dict:
        """样式化所有表格，覆盖 Office 默认 `{5C22544A-...}` 灰底粗黑边。

        返回:
            { "tables_styled": int, "slides": [int, ...] }
        """
        styled_slides = []
        for i in self.ppt.slides_with_tables():
            slide_path = f'ppt/slides/slide{i}.xml'
            content = self.ppt.read_text(slide_path)
            new_content = self.style_xml(content, header_color, alt_row_color, data_row_color, border_color, header_text_color, data_text_color, latin_font, chinese_font, font_size)
            if new_content != content:
                self.ppt.write_text(slide_path, new_content)
                styled_slides.append(i)
        self.ppt.save(output_path)
        return {"tables_styled": len(styled_slides), "slides": styled_slides}

    # =========================================================
    # style_xml：样式化单个 slide XML 字符串（utility，导出供外部用）
    # =========================================================
    def style_xml(
        self,
        content: str,
        header_color: str = "0096C7",
        alt_row_color: str = "F8F9FA",
        data_row_color: str = "FFFFFF",
        border_color: str = "D0D0D0",
        header_text_color: str = "FFFFFF",
        data_text_color: str = "1A1A1A",
        latin_font: str = "Microsoft YaHei",
        chinese_font: str = "微软雅黑",
        font_size: int = 1100,
    ) -> str:
        """对单段 slide XML 字符串做表格样式注入"""
        def process_table(match):
            table = match.group(0)
            rows = re.findall(r'<a:tr[^>]*>.*?</a:tr>', table, re.DOTALL)
            if not rows:
                return table

            styled_rows = []
            for idx, row in enumerate(rows):
                is_header = (idx == 0)
                is_alt = (idx % 2 == 0) and idx > 0

                if is_header:
                    row_fill = header_color
                    text_color = header_text_color
                    bold = True
                elif is_alt:
                    row_fill = alt_row_color
                    text_color = data_text_color
                    bold = False
                else:
                    row_fill = data_row_color
                    text_color = data_text_color
                    bold = False

                def style_cell(cell_match):
                    cell = cell_match.group(0)
                    cell_props = f'''<a:tcPr marL="{MARGIN_LR}" marR="{MARGIN_LR}" marT="{MARGIN_TB}" marB="{MARGIN_TB}">
<a:lnL w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill><a:prstDash val="solid"/></a:lnL>
<a:lnR w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill><a:prstDash val="solid"/></a:lnR>
<a:lnT w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill><a:prstDash val="solid"/></a:lnT>
<a:lnB w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill><a:prstDash val="solid"/></a:lnB>
<a:solidFill><a:srgbClr val="{row_fill}"/></a:solidFill>
</a:tcPr>'''

                    # Handle self-closing <a:tcPr /> AND paired <a:tcPr>...</a:tcPr>
                    if re.search(r'<a:tcPr\s*/>', cell):
                        cell = re.sub(r'<a:tcPr\s*/>', cell_props, cell, count=1)
                    elif '<a:tcPr' in cell:
                        cell = re.sub(r'<a:tcPr.*?</a:tcPr>', cell_props, cell, count=1, flags=re.DOTALL)
                    else:
                        cell = cell.replace('</a:tc>', cell_props + '</a:tc>')

                    # Style text runs
                    def style_run(run_match):
                        run = run_match.group(0)
                        bold_attr = ' b="1"' if bold else ''
                        new_rpr = f'<a:rPr lang="zh-CN" altLang="en-US"{bold_attr} sz="{font_size}"><a:solidFill><a:srgbClr val="{text_color}"/></a:solidFill><a:latin typeface="{latin_font}"/><a:ea typeface="{chinese_font}"/><a:cs typeface="{latin_font}"/></a:rPr>'
                        if '<a:rPr' in run:
                            run = re.sub(r'<a:rPr[^>]*(?:/>|>.*?</a:rPr>)', new_rpr, run, count=1, flags=re.DOTALL)
                        else:
                            run = re.sub(r'<a:r>', '<a:r>' + new_rpr, run, count=1)
                        return run

                    cell = re.sub(r'<a:r>.*?</a:r>', style_run, cell, flags=re.DOTALL)
                    return cell

                row = re.sub(r'<a:tc>.*?</a:tc>', style_cell, row, flags=re.DOTALL)
                styled_rows.append(row)

            # Reassemble table
            new_table = table
            for orig_row, styled_row in zip(rows, styled_rows):
                new_table = new_table.replace(orig_row, styled_row, 1)

            # Add table-level cell margin
            new_table = re.sub(
                r'<a:tblPr([^>]*)>',
                r'<a:tblPr\1><a:tblCellMar><a:top w="45720" type="dxa"/><a:left w="91440" type="dxa"/><a:bottom w="45720" type="dxa"/><a:right w="91440" type="dxa"/></a:tblCellMar>',
                new_table, count=1
            )
            # Remove table style reference so our explicit colors win
            new_table = re.sub(r'<a:tableStyleId>\{[^}]+\}</a:tableStyleId>', '', new_table)
            return new_table

        return re.sub(r'<a:tbl>.*?</a:tbl>', process_table, content, flags=re.DOTALL)
