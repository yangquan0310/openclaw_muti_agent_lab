#!/usr/bin/env python3
"""main.py - research-assistant CLI 入口（v7.0.0 精简版）

7 模块入口：upload / download / search / maintain / manage / summarize / synthesize
每个模块的公共方法都支持 CLI。
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.utils import config


# ─── CLI handlers ─────────────────────────────────

def cmd_upload(args, cfg):
    from scripts.upload import Uploader
    return Uploader(cfg).upload(
        pdf_path=args.pdf_path,
        doi=args.doi,
        slug=args.slug,
        title=args.title,
        tags=[t.strip() for t in (args.tags or "").split(",") if t.strip()] or None,
        skip_zotero=args.no_zotero,
        skip_webdav=args.no_webdav,
        skip_wiki=args.no_wiki,
    )


def cmd_download(args, cfg):
    from scripts.download import ZoteroJianguoyunDownloader, SciHubDownloader
    from scripts.download.scihub import SciHubAllMirrorsFailedError
    archive_dir = Path(args.archive_dir).expanduser() if args.archive_dir else None
    dest = Path(args.tmp_dir) if args.tmp_dir else None
    identifier = args.doi or args.zotero_key

    # 按 source 选择 downloader
    source = getattr(args, "source", None) or "zotero"
    if source == "scihub":
        dl = SciHubDownloader(cfg, archive_dir=archive_dir)
        if identifier and not identifier.startswith("10."):
            return {
                "success": False,
                "identifier": identifier,
                "source": source,
                "error": "SciHub 仅支持 DOI（以 '10.' 开头）",
            }
    else:
        dl = ZoteroJianguoyunDownloader(cfg, archive_dir=archive_dir)

    try:
        pdf_path = dl.fetch(identifier, dest_dir=dest, archive_dir=archive_dir)
    except SciHubAllMirrorsFailedError as e:
        # v6.0.7+ 老板 05:16 指令：全失败时给结构化反馈
        return {
            "success": False,
            "identifier": identifier,
            "source": source,
            "error": str(e),
            "error_type": "scihub_all_mirrors_failed",
            "mirrors_tried": e.mirrors_tried,
            "last_errors": e.last_errors,
            "suggestion": (
                "1) 加论文到 Zotero 库改走 --source zotero（老板默认源，保护坚果云）\n"
                "2) 等待几分钟后重试（sci-hub 镜像可能临时封 IP）\n"
                "3) 检查网络/代理是否可达 sci-hub\n"
                "4) 编辑 config.json 的 scihub.mirrors 列表调整优先级或加新镜像"
            ),
        }
    except Exception as e:
        return {"success": False, "identifier": identifier, "source": source, "error": str(e)}
    return {
        "success": True,
        "identifier": identifier,
        "source": source,
        "pdf_path": str(pdf_path),
        "size_bytes": pdf_path.stat().st_size if pdf_path.exists() else None,
    }


def cmd_search(args, cfg):
    from scripts.search import SearchManager
    mgr = SearchManager(cfg)
    kwargs = {
        "keyword": args.keyword,
        "limit": args.limit,
        "year_min": args.year_min,
        "year_max": args.year_max,
        "write_report": not args.dry_run,
        "topic": args.topic,
    }
    if args.source:
        kwargs["source"] = args.source
    elif args.sources:
        kwargs["sources"] = args.sources.split(",")
    return mgr.search(**kwargs)


def cmd_summarize(args, cfg):
    from scripts.summarize import Summarizer
    return Summarizer(cfg).summarize(
        source_id=args.source_id,
        pdf_path=args.pdf_path,
        ocr=args.ocr,
    )


def cmd_synthesize(args, cfg):
    from scripts.synthesize import Synthesizer
    return Synthesizer(cfg).extract(source_id=args.source_id)


def cmd_manage(args, cfg):
    from scripts.manage import WikiSourceManager
    m = WikiSourceManager(cfg)
    if args.manage_cmd == "list":
        return {"success": True, "count": len(m.list()), "sources": m.list()}
    if args.manage_cmd == "get":
        return m.get(args.source_id)
    if args.manage_cmd == "filter":
        conds = {}
        if args.has_zotero_key is not None:
            conds["has_zotero_key"] = args.has_zotero_key
        if args.has_doi is not None:
            conds["has_doi"] = args.has_doi
        if args.page_type:
            conds["pageType"] = args.page_type
        return {"success": True, "count": len(m.filter(conds)), "sources": m.filter(conds)}
    if args.manage_cmd == "merge":
        ids = args.inputs.split(",") if args.inputs else []
        return {"success": True, "merged_count": len(m.merge(ids)), "sources": m.merge(ids)}
    if args.manage_cmd == "stats":
        return {"success": True, "stats": m.stats()}
    if args.manage_cmd == "search":
        return {"success": True, "count": len(m.search(args.keyword)), "sources": m.search(args.keyword)}
    return {"success": False, "error": f"未知子命令: {args.manage_cmd}"}


def cmd_maintain(args, cfg):
    from scripts.maintain import DriftChecker
    checker = DriftChecker(cfg)
    if args.maintain_cmd == "check":
        return checker.check()
    if args.maintain_cmd == "missing":
        return {"success": True, "count": len(checker.missing()), "sources": checker.missing()}
    if args.maintain_cmd == "report":
        return {"success": True, "report_path": checker.report()}
    if args.maintain_cmd == "graph":
        return {"success": True, "graph": checker.graph("full" if args.full else "light")}
    return {"success": False, "error": f"未知子命令: {args.maintain_cmd}"}


# ─── argparse 分发 ─────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="research-assistant",
        description="research-assistant CLI（v7.0.0）",
    )
    sub = parser.add_subparsers(dest="module", required=True)

    # upload
    p = sub.add_parser("upload", help="本地 PDF → Zotero + WebDAV + wiki source")
    p.add_argument("--pdf-path", required=True)
    p.add_argument("--slug", help="必填或 --doi")
    p.add_argument("--doi")
    p.add_argument("--title")
    p.add_argument("--tags", help="逗号分隔")
    p.add_argument("--no-zotero", action="store_true")
    p.add_argument("--no-webdav", action="store_true")
    p.add_argument("--no-wiki", action="store_true")
    p.set_defaults(handler=cmd_upload)

    # download
    p = sub.add_parser("download", help="PDF 下载（Zotero / SciHub → wiki raw）")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--doi")
    g.add_argument("--zotero-key")
    p.add_argument(
        "--source", choices=["zotero", "scihub"], default="zotero",
        help="下载源：zotero（默认，需论文在 Zotero 库）/ scihub（绕过付费墙）",
    )
    p.add_argument("--archive-dir", help="归档目录（默认 ~/.openclaw/wiki/raw/papers）")
    p.add_argument("--tmp-dir", default="/tmp/zotero_dl")
    p.set_defaults(handler=cmd_download)

    # search
    p = sub.add_parser("search", help="文献检索")
    p.add_argument("--keyword", required=True)
    p.add_argument("--source", help="指定 source（cnki/semantic_scholar/google_scholar/arxiv）")
    p.add_argument("--sources", help="多源，逗号分隔")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--year-min", type=int)
    p.add_argument("--year-max", type=int)
    p.add_argument("--topic", default="general")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(handler=cmd_search)

    # summarize
    p = sub.add_parser("summarize", help="单篇笔记生成")
    p.add_argument("--source-id", required=True)
    p.add_argument("--pdf-path")
    p.add_argument("--ocr", action="store_true")
    p.set_defaults(handler=cmd_summarize)

    # synthesize
    p = sub.add_parser("synthesize", help="综述素材抽取")
    p.add_argument("--source-id", required=True)
    p.set_defaults(handler=cmd_synthesize)

    # manage
    p = sub.add_parser("manage", help="wiki source 列表管理")
    sp = p.add_subparsers(dest="manage_cmd", required=True)
    sp.add_parser("list")
    sp_get = sp.add_parser("get")
    sp_get.add_argument("--source-id", required=True)
    sp_filter = sp.add_parser("filter")
    sp_filter.add_argument("--has-zotero-key", type=lambda v: v.lower() == "true")
    sp_filter.add_argument("--has-doi", type=lambda v: v.lower() == "true")
    sp_filter.add_argument("--page-type")
    sp_merge = sp.add_parser("merge")
    sp_merge.add_argument("--inputs", help="逗号分隔的 source ids")
    sp.add_parser("stats")
    sp_search = sp.add_parser("search")
    sp_search.add_argument("--keyword", required=True)
    p.set_defaults(handler=cmd_manage)

    # maintain
    p = sub.add_parser("maintain", help="三方一致性检查")
    sp = p.add_subparsers(dest="maintain_cmd", required=True)
    sp.add_parser("check")
    sp.add_parser("missing")
    sp.add_parser("report")
    sp_graph = sp.add_parser("graph")
    sp_graph.add_argument("--full", action="store_true")
    p.set_defaults(handler=cmd_maintain)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    cfg = config("scripts/config.json")
    try:
        result = args.handler(args, cfg)
    except Exception as e:
        result = {"success": False, "error": str(e)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success", True) else 1


if __name__ == "__main__":
    sys.exit(main())