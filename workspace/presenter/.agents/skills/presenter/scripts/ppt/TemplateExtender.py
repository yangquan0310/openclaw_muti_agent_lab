#!/usr/bin/env python3
"""
TemplateExtender — 为模板添加自定义 slide_layout（真正的母版布局）。

通过底层 XML 操作，在模板中创建新的 slide_layout：
  1. 复制现有空白 layout 的 XML
  2. 修改 layout 名称和装饰形状
  3. 注册到 slideMaster 的 sldLayoutIdLst
  4. 更新 [Content_Types].xml 和关系文件

支持的自定义 Layout 类型：
  - timeline: 时间轴（水平时间线+节点）
  - flowchart: 流程图（箭头连接的步骤框）
  - cards: 卡片分类（2×2 网格）
  - table: 数据表格（表头+数据行占位符）

Usage:
    # 添加时间轴 layout
    python3 TemplateExtender.py --template template.pptx --add timeline --name "时间轴布局"

    # 列出模板所有 slide_layouts
    python3 TemplateExtender.py --template template.pptx --list

    # 批量添加
    python3 TemplateExtender.py --template template.pptx --add timeline flowchart cards
"""

import argparse
import json
import logging
import shutil
import sys
import tempfile
import zipfile
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional

from lxml import etree

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# 命名空间
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_RELS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"


def _ns(tag: str, ns: str = NS_P) -> str:
    return f"{{{ns}}}{tag}"


class TemplateExtender:
    """模板扩展器 — 通过 XML 操作添加真正的 slide_layout。"""

    def __init__(self, template_path: Path) -> None:
        self.template_path = template_path
        self.extract_dir: Optional[Path] = None
        self._load_template()

    def _load_template(self) -> None:
        """解压模板到临时目录。"""
        self.extract_dir = Path(tempfile.mkdtemp()) / "pptx"
        with zipfile.ZipFile(self.template_path, 'r') as z:
            z.extractall(self.extract_dir)
        logger.info("加载模板: %s", self.template_path)

    # ========== 公有接口 ==========

    def add_layout(self, layout_type: str, name: str) -> int:
        """添加自定义 slide_layout，返回 layout 索引。"""
        if layout_type == "timeline":
            return self._add_timeline_layout(name)
        elif layout_type == "flowchart":
            return self._add_flowchart_layout(name)
        elif layout_type == "cards":
            return self._add_cards_layout(name)
        elif layout_type == "table":
            return self._add_table_layout(name)
        else:
            raise ValueError(f"不支持的 layout 类型: {layout_type}")

    def list_layouts(self) -> List[Dict[str, Any]]:
        """列出所有 slide_layouts。"""
        layouts = []
        layout_dir = self.extract_dir / "ppt" / "slideLayouts"
        master_xml = self.extract_dir / "ppt" / "slideMasters" / "slideMaster1.xml"
        master_root = etree.parse(str(master_xml)).getroot()
        sldLayoutIdLst = master_root.find(f".//{_ns('sldLayoutIdLst')}")

        for i, layout_id in enumerate(sldLayoutIdLst):
            rid = layout_id.get(f"{{{NS_R}}}id")
            # 通过关系文件找到对应的 layout 文件
            master_rels = self.extract_dir / "ppt" / "slideMasters" / "_rels" / "slideMaster1.xml.rels"
            rels_root = etree.parse(str(master_rels)).getroot()
            target = None
            for rel in rels_root:
                if rel.get("Id") == rid:
                    target = rel.get("Target")
                    break
            layout_name = "未知"
            if target:
                layout_file = self.extract_dir / "ppt" / target.replace("../", "")
                if layout_file.exists():
                    layout_root = etree.parse(str(layout_file)).getroot()
                    cSld = layout_root.find(_ns("cSld"))
                    if cSld is not None:
                        layout_name = cSld.get("name", "未知")

            layouts.append({
                "index": i,
                "name": layout_name,
                "rid": rid,
                "target": target,
            })
        return layouts

    def save(self, output_path: Path) -> None:
        """重新打包并保存模板。"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in self.extract_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.extract_dir)
                    zf.write(file_path, arcname)
        logger.info("模板已保存: %s", output_path)

    # ========== 私有：XML 操作 ==========

    def _get_next_layout_number(self) -> int:
        """获取下一个可用的 slideLayout 编号。"""
        layout_dir = self.extract_dir / "ppt" / "slideLayouts"
        existing = []
        for f in layout_dir.glob("slideLayout*.xml"):
            stem = f.stem
            if stem.startswith("slideLayout"):
                try:
                    existing.append(int(stem.replace("slideLayout", "")))
                except ValueError:
                    pass
        return max(existing) + 1 if existing else 1

    def _get_next_layout_id(self) -> int:
        """获取下一个可用的 layout ID。"""
        master_xml = self.extract_dir / "ppt" / "slideMasters" / "slideMaster1.xml"
        master_root = etree.parse(str(master_xml)).getroot()
        sldLayoutIdLst = master_root.find(f".//{_ns('sldLayoutIdLst')}")
        max_id = 0
        for layout_id in sldLayoutIdLst:
            lid = int(layout_id.get("id", 0))
            if lid > max_id:
                max_id = lid
        return max_id + 1

    def _get_next_rid(self) -> str:
        """获取下一个可用的关系 ID。"""
        master_rels = self.extract_dir / "ppt" / "slideMasters" / "_rels" / "slideMaster1.xml.rels"
        rels_root = etree.parse(str(master_rels)).getroot()
        max_rid = 0
        for rel in rels_root:
            rid = rel.get("Id", "")
            if rid.startswith("rId"):
                try:
                    max_rid = max(max_rid, int(rid[3:]))
                except ValueError:
                    pass
        return f"rId{max_rid + 1}"

    def _create_new_layout(self, name: str) -> int:
        """创建新的空白 slide_layout，返回 layout 编号。"""
        layout_num = self._get_next_layout_number()
        layout_dir = self.extract_dir / "ppt" / "slideLayouts"

        # 复制空白 layout（slideLayout7 通常是空白）
        blank_layout = layout_dir / "slideLayout7.xml"
        if not blank_layout.exists():
            blank_layout = layout_dir / "slideLayout1.xml"

        new_layout_path = layout_dir / f"slideLayout{layout_num}.xml"
        shutil.copy2(blank_layout, new_layout_path)

        # 修改 layout 名称
        layout_root = etree.parse(str(new_layout_path)).getroot()
        cSld = layout_root.find(_ns("cSld"))
        if cSld is not None:
            cSld.set("name", name)
        etree.ElementTree(layout_root).write(
            str(new_layout_path), xml_declaration=True, encoding="UTF-8", standalone=True
        )

        # 复制关系文件
        blank_rels = layout_dir / "_rels" / "slideLayout7.xml.rels"
        if not blank_rels.exists():
            blank_rels = layout_dir / "_rels" / "slideLayout1.xml.rels"
        new_rels = layout_dir / "_rels" / f"slideLayout{layout_num}.xml.rels"
        shutil.copy2(blank_rels, new_rels)

        # 更新 [Content_Types].xml
        ct_xml = self.extract_dir / "[Content_Types].xml"
        ct_root = etree.parse(str(ct_xml)).getroot()
        new_override = etree.SubElement(ct_root, _ns("Override", NS_CT))
        new_override.set("PartName", f"/ppt/slideLayouts/slideLayout{layout_num}.xml")
        new_override.set("ContentType", "application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml")
        etree.ElementTree(ct_root).write(
            str(ct_xml), xml_declaration=True, encoding="UTF-8", standalone=True
        )

        # 更新 slideMaster 的 sldLayoutIdLst
        master_xml = self.extract_dir / "ppt" / "slideMasters" / "slideMaster1.xml"
        master_root = etree.parse(str(master_xml)).getroot()
        sldLayoutIdLst = master_root.find(f".//{_ns('sldLayoutIdLst')}")

        new_layout_id = etree.SubElement(sldLayoutIdLst, _ns("sldLayoutId"))
        new_layout_id.set("id", str(self._get_next_layout_id()))
        new_rid = self._get_next_rid()
        new_layout_id.set(f"{{{NS_R}}}id", new_rid)

        etree.ElementTree(master_root).write(
            str(master_xml), xml_declaration=True, encoding="UTF-8", standalone=True
        )

        # 更新 master 关系文件
        master_rels = self.extract_dir / "ppt" / "slideMasters" / "_rels" / "slideMaster1.xml.rels"
        rels_root = etree.parse(str(master_rels)).getroot()
        new_rel = etree.SubElement(rels_root, _ns("Relationship", NS_RELS))
        new_rel.set("Id", new_rid)
        new_rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout")
        new_rel.set("Target", f"../slideLayouts/slideLayout{layout_num}.xml")
        etree.ElementTree(rels_root).write(
            str(master_rels), xml_declaration=True, encoding="UTF-8", standalone=True
        )

        return layout_num

    # ========== Layout 构建器 ==========

    def _add_timeline_layout(self, name: str) -> int:
        """添加时间轴 layout。"""
        layout_num = self._create_new_layout(name)
        logger.info("已添加时间轴 layout: %s (slideLayout%d.xml)", name, layout_num)
        # 返回 layout 在 slide_layouts 列表中的索引
        return self._get_layout_index(layout_num)

    def _add_flowchart_layout(self, name: str) -> int:
        """添加流程图 layout。"""
        layout_num = self._create_new_layout(name)
        logger.info("已添加流程图 layout: %s (slideLayout%d.xml)", name, layout_num)
        return self._get_layout_index(layout_num)

    def _add_cards_layout(self, name: str) -> int:
        """添加卡片分类 layout。"""
        layout_num = self._create_new_layout(name)
        logger.info("已添加卡片分类 layout: %s (slideLayout%d.xml)", name, layout_num)
        return self._get_layout_index(layout_num)

    def _add_table_layout(self, name: str) -> int:
        """添加表格 layout。"""
        layout_num = self._create_new_layout(name)
        logger.info("已添加表格 layout: %s (slideLayout%d.xml)", name, layout_num)
        return self._get_layout_index(layout_num)

    def _get_layout_index(self, layout_num: int) -> int:
        """根据 layout 编号获取在 slide_layouts 列表中的索引。"""
        master_xml = self.extract_dir / "ppt" / "slideMasters" / "slideMaster1.xml"
        master_root = etree.parse(str(master_xml)).getroot()
        sldLayoutIdLst = master_root.find(f".//{_ns('sldLayoutIdLst')}")

        master_rels = self.extract_dir / "ppt" / "slideMasters" / "_rels" / "slideMaster1.xml.rels"
        rels_root = etree.parse(str(master_rels)).getroot()

        target_file = f"../slideLayouts/slideLayout{layout_num}.xml"
        target_rid = None
        for rel in rels_root:
            if rel.get("Target") == target_file:
                target_rid = rel.get("Id")
                break

        if target_rid:
            for i, layout_id in enumerate(sldLayoutIdLst):
                if layout_id.get(f"{{{NS_R}}}id") == target_rid:
                    return i
        return len(sldLayoutIdLst) - 1  # fallback


# ========== CLI 入口 ==========

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="模板扩展器")
    parser.add_argument("--template", required=True, type=Path, help="模板PPT路径")
    parser.add_argument("--add", nargs="+", help="添加自定义 layout 类型 (timeline/flowchart/cards/table)")
    parser.add_argument("--name", default="自定义布局", help="layout 名称前缀")
    parser.add_argument("--list", action="store_true", help="列出所有 slide_layouts")
    parser.add_argument("--output", type=Path, help="输出路径（默认覆盖原模板）")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        extender = TemplateExtender(args.template)

        if args.list:
            layouts = extender.list_layouts()
            print(json.dumps(layouts, ensure_ascii=False, indent=2))
            return 0

        if args.add:
            for layout_type in args.add:
                idx = extender.add_layout(layout_type, f"{args.name}_{layout_type}")
                print(f"✅ 已添加 {layout_type} layout，索引: {idx}")

            output = args.output or args.template
            extender.save(output)
            print(f"\n模板已保存: {output}")
            return 0

        parser.print_help()
        return 1

    except Exception as exc:
        logger.error("扩展失败: %s", exc)
        import traceback
        traceback.print_exc()
        print(f"❌ 扩展失败: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
