#!/usr/bin/env python3
"""
PPT.py — PPTXFile 类（zipfile 包装）

> presenter 技能 ppt 后处理模块的基础类。
> **不是 python-pptx**——纯 Python zipfile + XML 操作。
> 提供打开 / 读取 / 写回 .pptx 的标准接口。
"""

import zipfile
import shutil
import re
from pathlib import Path
from typing import Optional


class PPTXFile:
    """代表一个 .pptx 文件，提供 zipfile 级别的读写接口。"""

    def __init__(self, path: str):
        self.path = Path(path)
        self._files: dict[str, bytes] = {}
        self._loaded = False

    def load(self) -> "PPTXFile":
        """加载 .pptx 到内存字典"""
        with zipfile.ZipFile(self.path, 'r') as z:
            self._files = {item.filename: z.read(item.filename) for item in z.infolist()}
        self._loaded = True
        return self

    def save(self, output_path: Optional[str] = None) -> str:
        """写回 .pptx（到新路径或覆盖原路径）"""
        if not self._loaded:
            raise RuntimeError("未调用 load()，先 load 再 save")
        out = Path(output_path) if output_path else self.path
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for fname, data in self._files.items():
                z.writestr(fname, data)
        return str(out)

    # ---- 文件访问 ----

    def list_files(self, prefix: str = "") -> list[str]:
        """列出所有文件（可按前缀过滤）"""
        return [f for f in self._files if f.startswith(prefix)]

    def read(self, name: str) -> bytes:
        """读一个文件的原始字节"""
        if name not in self._files:
            raise KeyError(f"文件不存在: {name}")
        return self._files[name]

    def read_text(self, name: str) -> str:
        """读一个 XML 文件为字符串"""
        return self.read(name).decode('utf-8')

    def write(self, name: str, data: bytes) -> None:
        """写 / 覆盖一个文件"""
        self._files[name] = data

    def write_text(self, name: str, content: str) -> None:
        self._files[name] = content.encode('utf-8')

    def has(self, name: str) -> bool:
        return name in self._files

    # ---- 演示元信息 ----

    def slide_size(self) -> tuple[int, int]:
        """从 presentation.xml 读 sldSz，返回 (cx, cy) EMU"""
        if not self.has('ppt/presentation.xml'):
            return (9144000, 5143500)  # default 16:9
        pres = self.read_text('ppt/presentation.xml')
        m = re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', pres)
        if m:
            return (int(m.group(1)), int(m.group(2)))
        return (9144000, 5143500)

    def slide_count(self) -> int:
        """slide 数（数 sldId 引用）"""
        if not self.has('ppt/presentation.xml'):
            return 0
        pres = self.read_text('ppt/presentation.xml')
        return len(re.findall(r'<p:sldId ', pres))

    def layout_count(self) -> int:
        """slideLayout 数"""
        return len(self.list_files('ppt/slideLayouts/slideLayout'))

    def master_count(self) -> int:
        """slideMaster 数"""
        return len(self.list_files('ppt/slideMasters/slideMaster'))

    def slides_with_tables(self) -> list[int]:
        """返回含表格的 slide 编号列表（1-based）"""
        result = []
        for i in range(1, self.slide_count() + 1):
            slide_path = f'ppt/slides/slide{i}.xml'
            if self.has(slide_path) and '<a:tbl>' in self.read_text(slide_path):
                result.append(i)
        return result

    # ---- 主题色 + 字体抽取 ----

    def theme_colors(self) -> dict[str, str]:
        """返回主题色方案（dk1/lt1/dk2/lt2/accent1-6/hlink/folHlink）"""
        if not self.has('ppt/theme/theme1.xml'):
            return {}
        theme = self.read_text('ppt/theme/theme1.xml')
        result = {}
        # Extract from <a:clrScheme>
        m = re.search(r'<a:clrScheme[^>]*>(.*?)</a:clrScheme>', theme, re.DOTALL)
        if not m:
            return {}
        scheme = m.group(1)
        for elem_match in re.finditer(r'<a:(dk1|lt1|dk2|lt2|accent[1-6]|hlink|folHlink)>(.*?)</a:\1>', scheme, re.DOTALL):
            name = elem_match.group(1)
            inner = elem_match.group(2)
            srgb = re.search(r'<a:srgbClr val="([0-9A-Fa-f]{6})"', inner)
            sysclr = re.search(r'<a:sysClr val="\w+" lastClr="([0-9A-Fa-f]{6})"', inner)
            if srgb:
                result[name] = '#' + srgb.group(1)
            elif sysclr:
                result[name] = '#' + sysclr.group(1)
        return result

    def theme_fonts(self) -> dict[str, str]:
        """返回主题字体（major-latin / minor-latin / ea）"""
        if not self.has('ppt/theme/theme1.xml'):
            return {}
        theme = self.read_text('ppt/theme/theme1.xml')
        result = {}
        m = re.search(r'<a:majorFont>.*?<a:latin typeface="([^"]+)"', theme, re.DOTALL)
        if m:
            result['major-latin'] = m.group(1)
        m = re.search(r'<a:minorFont>.*?<a:latin typeface="([^"]+)"', theme, re.DOTALL)
        if m:
            result['minor-latin'] = m.group(1)
        m = re.search(r'<a:font script="Hans" typeface="([^"]+)"', theme)
        if m:
            result['ea-Hans'] = m.group(1)
        return result

    # ---- 媒体清理 ----

    def strip_unused_media(self, output_path: str = None) -> dict:
        """删除未被任何 slide/master/layout 引用的媒体文件（图片、视频）。

        Pandoc/Quarto 渲 .pptx 时会把 reference-doc 里的所有媒体都搬进输出，
        即使那些媒体没在 slide 里用上。strip 后能大幅瘦身（典型 80%+）。

        返回:
            { "removed": int, "saved_bytes": int, "removed_files": [str, ...] }
        """
        import re
        # Find all media files
        media = self.list_files('ppt/media/')
        if not media:
            return {"removed": 0, "saved_bytes": 0, "removed_files": []}

        # Build rId -> media-filename mapping from all rels
        rel_to_media = {}
        for rels_path in self.list_files('_rels/') + self.list_files('ppt/slides/_rels/') +                         self.list_files('ppt/slideLayouts/_rels/') + self.list_files('ppt/slideMasters/_rels/'):
            if not rels_path.endswith('.rels'):
                continue
            content = self.read_text(rels_path)
            # Match <Relationship Id="rIdN" Type="...image" Target="../media/xxx"/>
            for m in re.finditer(r'Id="([^"]+)"[^>]*Target="\.\./(media/[^"]+)"', content):
                rel_to_media[m.group(1)] = m.group(2)
            for m in re.finditer(r'Target="\.\./(media/[^"]+)"[^>]*Id="([^"]+)"', content):
                rel_to_media[m.group(2)] = m.group(1)

        # Find referenced rIds in all slide/master/layout XMLs
        referenced_rids = set()
        for path in self.list_files('ppt/slides/') + self.list_files('ppt/slideLayouts/') + self.list_files('ppt/slideMasters/'):
            if not path.endswith('.xml'):
                continue
            content = self.read_text(path)
            for m in re.finditer(r'r:embed="([^"]+)"', content):
                referenced_rids.add(m.group(1))
            for m in re.finditer(r'r:link="([^"]+)"', content):
                referenced_rids.add(m.group(1))

        # Determine used media files
        used_media = set()
        for rid in referenced_rids:
            if rid in rel_to_media:
                used_media.add(rel_to_media[rid])

        # Remove unused media
        removed = []
        saved = 0
        for path in media:
            if path not in used_media:
                size = len(self._files[path])
                del self._files[path]
                removed.append(path)
                saved += size

        # Also clean up the rels entries
        for rels_path in self.list_files('ppt/slides/_rels/') + self.list_files('ppt/slideLayouts/_rels/') + self.list_files('ppt/slideMasters/_rels/'):
            if not rels_path.endswith('.rels'):
                continue
            content = self.read_text(rels_path)
            new_content = re.sub(r'<Relationship[^/]*Target="\.\./(media/[^"]+)"[^/]*/>', '', content)
            if new_content != content:
                self.write_text(rels_path, new_content)

        if output_path is None:
            output_path = str(self.path)
        self.save(output_path)
        return {"removed": len(removed), "saved_bytes": saved, "removed_files": removed}

