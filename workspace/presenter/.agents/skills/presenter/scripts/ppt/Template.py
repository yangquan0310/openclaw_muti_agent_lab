#!/usr/bin/env python3
"""
Template.py — 母版装饰类

> 母版装饰的 5 个方法（一个方法一个功能）：
> - decorate: 一站式（add-header + add-accent + set-cover + set-fonts）
> - add_header: 加顶部色条
> - add_accent: 加左侧色条
> - set_cover: 改封面布局（全色底 + 装饰块）
> - set_fonts: 改 CJK / Latin 字体

> **不是 python-pptx**——纯 Python zipfile + XML 操作。
> 设计原则：每个方法只做一件事，不重叠（skill-developer 核心原则 4）。
"""

import re
from typing import Optional
from .PPT import PPTXFile


SLIDE_W_DEFAULT = 9144000
SLIDE_H_DEFAULT = 5143500
EMU_PER_INCH = 914400


class TemplateEditor:
    """母版装饰编辑器。复用同一个 PPTXFile 实例可链式调用。"""

    def __init__(self, ppt: PPTXFile):
        self.ppt = ppt
        if not ppt._loaded:
            ppt.load()

    def _next_id(self, master_xml: str, start: int = 100) -> int:
        """找 slide master 中未使用的 id 起点"""
        used = set(int(m) for m in re.findall(r'<p:cNvPr id="(\d+)"', master_xml))
        while start in used:
            start += 1
        return start

    # =========================================================
    # 主方法：一站式装饰（ch11 沿用的 teal+橙 风格）
    # =========================================================
    def decorate(
        self,
        output_path: str,
        header_color: str = "0096C7",
        accent_color: str = "F4A261",
        header_height: int = 274320,   # 0.30"
        accent_width: int = 73152,     # 0.08"
        header_label: str = "教育科学研究方法",
        latin_font: str = "Microsoft YaHei",
        chinese_font: str = "微软雅黑",
        set_cover: bool = True,
        set_fonts: bool = True,
        set_theme: bool = True,
    ) -> str:
        """一站式母版装饰（默认 ch11 风格：teal 顶栏 + 橙左条 + 封面布局 + YaHei 字体）"""
        # 链式：add_header → add_accent → set_cover → set_fonts → set_theme
        intermediate = output_path + ".intermediate.pptx"
        self.add_header(intermediate, header_color, header_height, header_label, latin_font, chinese_font)
        self.add_accent(intermediate, accent_color, accent_width, latin_font, chinese_font)
        if set_cover:
            intermediate2 = output_path + ".intermediate2.pptx"
            self.set_cover(intermediate2, header_color, accent_color)
            self._swap_file(intermediate2, intermediate)
        if set_fonts:
            self.set_fonts(output_path, latin_font, chinese_font)
        else:
            self._swap_file(intermediate, output_path)
        if set_theme:
            self.set_theme_colors(output_path, accent1=header_color, accent2=accent_color)
        # 清理中间文件
        import os
        for tmp in [intermediate, output_path + ".intermediate2.pptx"]:
            if os.path.exists(tmp):
                os.remove(tmp)
        return output_path

    # =========================================================
    # add_header：加顶部色条（slide master 装饰）
    # =========================================================
    def add_header(
        self,
        output_path: str,
        color: str = "0096C7",
        height: int = 274320,
        label: str = "教育科学研究方法",
        latin_font: str = "Microsoft YaHei",
        chinese_font: str = "微软雅黑",
    ) -> str:
        """在 slide master 加顶部色条"""
        slide_w, slide_h = self.ppt.slide_size()
        master_path = 'ppt/slideMasters/slideMaster1.xml'
        if not self.ppt.has(master_path):
            raise ValueError(f"母版文件不存在: {master_path}")

        master = self.ppt.read_text(master_path)
        new_id = self._next_id(master)
        header_bar = f'''<p:sp>
<p:nvSpPr>
<p:cNvPr id="{new_id}" name="HeaderBar"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm><a:off x="0" y="0"/><a:ext cx="{slide_w}" cy="{height}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
<a:ln><a:noFill/></a:ln>
</p:spPr>
<p:txBody>
<a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/>
<a:lstStyle/>
<a:p><a:pPr algn="r"/><a:r><a:rPr lang="zh-CN" sz="1000" b="0"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:latin typeface="{latin_font}"/><a:ea typeface="{chinese_font}"/></a:rPr><a:t>{label}</a:t></a:r></a:p>
</p:txBody>
</p:sp>
'''
        master = master.replace('<p:spTree>', '<p:spTree>' + header_bar, 1)
        self.ppt.write_text(master_path, master)
        return self.ppt.save(output_path)

    # =========================================================
    # add_accent：加左侧色条
    # =========================================================
    def add_accent(
        self,
        output_path: str,
        color: str = "F4A261",
        width: int = 73152,
        latin_font: str = "Microsoft YaHei",
        chinese_font: str = "微软雅黑",
    ) -> str:
        """在 slide master 加左侧色条（从顶部色条下方开始）"""
        slide_w, slide_h = self.ppt.slide_size()
        master_path = 'ppt/slideMasters/slideMaster1.xml'
        master = self.ppt.read_text(master_path)

        # 找现有 HeaderBar 的高度（如果存在），否则默认 274320）
        m = re.search(r'name="HeaderBar"[^<]*<[^>]+>.*?<a:ext cx="\d+" cy="(\d+)"', master, re.DOTALL)
        if m:
            header_h = int(m.group(1))
        else:
            header_h = 274320

        new_id = self._next_id(master)
        accent_strip = f'''<p:sp>
<p:nvSpPr>
<p:cNvPr id="{new_id}" name="AccentStrip"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm><a:off x="0" y="{header_h}"/><a:ext cx="{width}" cy="{slide_h - header_h}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
<a:ln><a:noFill/></a:ln>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p><a:endParaRPr lang="zh-CN"/></a:p>
</p:txBody>
</p:sp>
'''
        master = master.replace('<p:spTree>', '<p:spTree>' + accent_strip, 1)
        self.ppt.write_text(master_path, master)
        return self.ppt.save(output_path)

    # =========================================================
    # set_cover：改封面布局（Layout 1 = Title Slide）
    # =========================================================
    def set_cover(
        self,
        output_path: str,
        bg_color: str = "0096C7",
        accent_color: str = "F4A261",
    ) -> str:
        """设置封面布局：全色底 + 右侧装饰块（默认 Layout 1 = Title Slide）"""
        slide_w, slide_h = self.ppt.slide_size()
        cover_path = 'ppt/slideLayouts/slideLayout1.xml'
        if not self.ppt.has(cover_path):
            raise ValueError(f"封面 layout 不存在: {cover_path}")

        cover = self.ppt.read_text(cover_path)
        new_id1 = self._next_id(cover, 200)
        new_id2 = self._next_id(cover, new_id1 + 1)
        cover_decoration = f'''<p:sp>
<p:nvSpPr>
<p:cNvPr id="{new_id1}" name="CoverBackground"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm><a:off x="0" y="0"/><a:ext cx="{slide_w}" cy="{slide_h}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="{bg_color}"/></a:solidFill>
<a:ln><a:noFill/></a:ln>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p><a:endParaRPr lang="zh-CN"/></a:p>
</p:txBody>
</p:sp>
<p:sp>
<p:nvSpPr>
<p:cNvPr id="{new_id2}" name="CoverAccentBlock"/>
<p:cNvSpPr/>
<p:nvPr/>
</p:nvSpPr>
<p:spPr>
<a:xfrm><a:off x="{int(slide_w * 0.7)}" y="0"/><a:ext cx="{slide_w - int(slide_w * 0.7)}" cy="{slide_h}"/></a:xfrm>
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
<a:solidFill><a:srgbClr val="{accent_color}"/></a:solidFill>
<a:ln><a:noFill/></a:ln>
</p:spPr>
<p:txBody>
<a:bodyPr/>
<a:lstStyle/>
<a:p><a:endParaRPr lang="zh-CN"/></a:p>
</p:txBody>
</p:sp>
'''
        cover = cover.replace('<p:spTree>', '<p:spTree>' + cover_decoration, 1)
        self.ppt.write_text(cover_path, cover)
        return self.ppt.save(output_path)

    # =========================================================
    # set_fonts：改 CJK / Latin 字体（slide master + layouts + theme）
    # =========================================================
    def set_fonts(
        self,
        output_path: str,
        latin_font: str = "Microsoft YaHei",
        chinese_font: str = "微软雅黑",
    ) -> str:
        """改 theme 字体（master/layouts 也跟着用）"""
        # 1. 改 theme
        theme_path = 'ppt/theme/theme1.xml'
        if self.ppt.has(theme_path):
            theme = self.ppt.read_text(theme_path)
            theme = theme.replace('<a:latin typeface="Calibri"/>', f'<a:latin typeface="{latin_font}"/>')
            theme = theme.replace('typeface="Calibri"', f'typeface="{latin_font}"')
            theme = theme.replace('typeface="宋体"', f'typeface="{chinese_font}"')
            theme = theme.replace('typeface="+mj-lt"', f'typeface="{latin_font}"')
            theme = theme.replace('typeface="+mn-lt"', f'typeface="{latin_font}"')
            theme = theme.replace('typeface="+mj-ea"', f'typeface="{chinese_font}"')
            theme = theme.replace('typeface="+mn-ea"', f'typeface="{chinese_font}"')
            self.ppt.write_text(theme_path, theme)

        # 2. 改 slide master
        for master_path in self.ppt.list_files('ppt/slideMasters/slideMaster'):
            content = self.ppt.read_text(master_path)
            content = content.replace('typeface="+mj-lt"', f'typeface="{latin_font}"')
            content = content.replace('typeface="+mn-lt"', f'typeface="{latin_font}"')
            content = content.replace('typeface="+mj-ea"', f'typeface="{chinese_font}"')
            content = content.replace('typeface="+mn-ea"', f'typeface="{chinese_font}"')
            content = content.replace('typeface="Calibri"', f'typeface="{latin_font}"')
            self.ppt.write_text(master_path, content)

        # 3. 改所有 layouts
        for layout_path in self.ppt.list_files('ppt/slideLayouts/slideLayout'):
            content = self.ppt.read_text(layout_path)
            content = content.replace('typeface="+mj-lt"', f'typeface="{latin_font}"')
            content = content.replace('typeface="+mn-lt"', f'typeface="{latin_font}"')
            content = content.replace('typeface="+mj-ea"', f'typeface="{chinese_font}"')
            content = content.replace('typeface="+mn-ea"', f'typeface="{chinese_font}"')
            content = content.replace('typeface="Calibri"', f'typeface="{latin_font}"')
            self.ppt.write_text(layout_path, content)

        return self.ppt.save(output_path)

    # =========================================================
    # set_theme_colors：改 theme 颜色（accent1/2/...）
    # =========================================================
    def set_theme_colors(
        self,
        output_path: str,
        accent1: Optional[str] = None,
        accent2: Optional[str] = None,
        accent3: Optional[str] = None,
        accent4: Optional[str] = None,
        accent5: Optional[str] = None,
        accent6: Optional[str] = None,
    ) -> str:
        """改 theme 颜色（accent1 = teal 主色，accent2 = 橙副色，等等）"""
        theme_path = 'ppt/theme/theme1.xml'
        if not self.ppt.has(theme_path):
            raise ValueError(f"主题文件不存在: {theme_path}")
        theme = self.ppt.read_text(theme_path)

        # 替换 Office 默认色为新色
        default_to_new = {
            "4F81BD": accent1,
            "C0504D": accent2,
            "9BBB59": accent3,
            "8064A2": accent4,
            "4BACC6": accent5,
            "F79646": accent6,
            "1F497D": accent1,  # dk2 也用 accent1
        }
        for old, new in default_to_new.items():
            if new:
                theme = re.sub(rf'<a:srgbClr val="{old}"', f'<a:srgbClr val="{new}"', theme, flags=re.IGNORECASE)

        self.ppt.write_text(theme_path, theme)
        return self.ppt.save(output_path)

    # ---- helper ----
    def _swap_file(self, src: str, dst: str) -> None:
        """从 src 读新 PPTX 替换 self.ppt 内容到 dst"""
        self.ppt.path = dst
        self.ppt.load()
