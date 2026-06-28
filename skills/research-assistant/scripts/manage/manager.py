"""manager.py - WikiSourceManager 类（wiki source 列表 CRUD）"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from scripts.utils import config, frontmatter, WIKI_SOURCES, WIKI_SYNTHESES, WIKI_CONCEPTS, WIKI_REPORTS


class WikiSourceManager:
    """wiki source 列表 CRUD：list / get / filter / merge / stats / search"""

    def __init__(self, cfg: dict | None = None):
        self.cfg = cfg or config()
        self.sources_dir = WIKI_SOURCES

    def _scan(self) -> list[dict]:
        """扫描 wiki sources/ 返回所有 source 摘要"""
        result = []
        if not self.sources_dir.exists():
            return result
        for f in sorted(self.sources_dir.glob("*.md")):
            if f.name.startswith("_") or f.name == "index.md":
                continue
            content = f.read_text(encoding="utf-8")
            meta, _ = frontmatter(content)
            if not meta.get("id"):
                continue
            result.append({
                "id": meta.get("id"),
                "file": f.name,
                "title": meta.get("title", ""),
                "zotero_item_key": meta.get("zotero_item_key") or None,
                "zotero_doi": meta.get("zotero_doi") or None,
                "pageType": meta.get("pageType", "source"),
            })
        return result

    def list(self) -> list[dict]:
        """列出所有 wiki source"""
        return self._scan()

    def get(self, source_id: str) -> dict:
        """单篇详情（含完整 frontmatter）"""
        sources = self._scan()
        match = next((s for s in sources if s["id"] == source_id), None)
        if not match:
            return {"success": False, "error": f"未找到 source: {source_id}"}
        fpath = self.sources_dir / match["file"]
        content = fpath.read_text(encoding="utf-8")
        meta, body = frontmatter(content)
        return {
            "success": True,
            "source": {
                **match,
                "frontmatter": meta,
                "body_preview": body[:500],
                "file_path": str(fpath),
            },
        }

    def filter(self, conditions: dict) -> list[dict]:
        """按条件筛选

        conditions 支持的 key:
        - has_zotero_key: bool
        - has_doi: bool
        - pageType: str
        """
        sources = self._scan()
        result = []
        for s in sources:
            ok = True
            if "has_zotero_key" in conditions:
                if bool(conditions["has_zotero_key"]) != bool(s.get("zotero_item_key")):
                    ok = False
            if "has_doi" in conditions:
                if bool(conditions["has_doi"]) != bool(s.get("zotero_doi")):
                    ok = False
            if "pageType" in conditions:
                if s.get("pageType") != conditions["pageType"]:
                    ok = False
            if ok:
                result.append(s)
        return result

    def merge(self, source_ids: list[str]) -> list[dict]:
        """按 zotero_item_key 去重合并"""
        sources = self._scan()
        by_id = {s["id"]: s for s in sources}
        by_zk: dict[str, dict] = {}
        result = []
        for sid in source_ids:
            s = by_id.get(sid)
            if not s:
                continue
            zk = s.get("zotero_item_key")
            if zk and zk in by_zk:
                continue
            if zk:
                by_zk[zk] = s
            result.append(s)
        return result

    def stats(self) -> dict:
        """统计 wiki 现状"""
        sources = self._scan()
        with_zk = sum(1 for s in sources if s.get("zotero_item_key"))
        with_doi = sum(1 for s in sources if s.get("zotero_doi"))
        page_types: dict[str, int] = {}
        for s in sources:
            pt = s.get("pageType", "unknown")
            page_types[pt] = page_types.get(pt, 0) + 1
        return {
            "total_sources": len(sources),
            "sources_with_zotero_key": with_zk,
            "sources_with_doi": with_doi,
            "sources_by_pageType": page_types,
            "total_syntheses": len(list(WIKI_SYNTHESES.glob("*.md"))) if WIKI_SYNTHESES.exists() else 0,
            "total_concepts": len(list(WIKI_CONCEPTS.glob("*.md"))) if WIKI_CONCEPTS.exists() else 0,
            "total_reports": len(list(WIKI_REPORTS.glob("*.md"))) if WIKI_REPORTS.exists() else 0,
            "computed_at": datetime.now().isoformat(timespec="seconds"),
        }

    def search(self, keyword: str) -> list[dict]:
        """按 title 模糊搜索"""
        sources = self._scan()
        kw = keyword.lower()
        return [s for s in sources if kw in s.get("title", "").lower()]
