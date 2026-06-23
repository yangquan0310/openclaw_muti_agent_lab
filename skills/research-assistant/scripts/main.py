#!/usr/bin/env python3
"""CLI 统一入口：整合研究助手所有子命令。"""

import argparse
import sys
from pathlib import Path

# Fix-01: 添加项目根目录到 path，解决 ModuleNotFoundError
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.search.Searcher import Searcher as OldSearcher
from scripts.search import search_by_keyword
from scripts.summarize.Summarizer import Summarizer
from scripts.manage.Manager import Manager
from scripts.synthesize.Synthesizer import Synthesizer
from scripts.download import ZoteroJianguoyunDownloader


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="research-assistant CLI")
    sub = parser.add_subparsers(dest="module", help="模块")

    # ── search（多态自动路由：中文→CNKI，英文→SemSch）─────────────
    search_parser = sub.add_parser("search", help="文献检索（自动路由）")
    # 两互斥模式
    mode = search_parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--queries", metavar="FILE",
                     help="检索条件 JSON 文件（高级用法）")
    mode.add_argument("--keyword", metavar="TEXT",
                     help="检索关键词（自动判断语言路由）")
    search_parser.add_argument("--kb-path", default="wiki/sources/cache.json",
                              help="知识库路径")
    search_parser.add_argument("--limit", type=int, default=20,
                              help="最大结果数（默认 20）")
    search_parser.add_argument("--year-min", type=int, help="最早发表年份")
    search_parser.add_argument("--year-max", type=int, help="最晚发表年份")
    search_parser.add_argument("--interval", type=float, default=3.0,
                              help="请求间隔（秒，默认 3.0）")
    search_parser.add_argument("--fields", help="请求字段（JSON 格式，仅 --queries 模式）")
    search_parser.add_argument("--no-deduplicate", action="store_true",
                              help="不去重（仅 --queries 模式）")
    search_parser.add_argument("--topic", default="general",
                                 help="wiki report 分类 topic（默认 general）")
    search_parser.add_argument("--dry-run", action="store_true",
                                 help="不写 wiki report（仅展示搜索结果）")
    search_parser.set_defaults(func=_run_search)

    # ── summarize ─────────────────────────────────────────────
    sum_parser = sub.add_parser("summarize", help="文献总结 (Summarizer)")
    sum_parser.add_argument("--source-id", required=True,
                            help="wiki source id (如 source.diehl-2026-captured-memories)")
    sum_parser.add_argument("--output", help="输出 Markdown 路径（可选）")
    sum_parser.add_argument("--pdf-path",
                            help="可选：本地 PDF 路径，工具用 pypdf/pypdfium2/tesseract 提取结构化数据（v6.0.2+）")
    sum_parser.add_argument("--ocr", action="store_true",
                            help="启用 tesseract OCR（默认关，只提文本）")
    sum_parser.set_defaults(func=_run_summarize)

    # ── manage ──────────────────────────────────────────────────
    manage_parser = sub.add_parser("manage", help="知识库管理 (Manager)")
    manage_sub = manage_parser.add_subparsers(dest="manage_cmd")

    merge_p = manage_sub.add_parser("merge", help="合并知识库")
    merge_p.add_argument("--inputs",
                         help="wiki source ids（逗号分隔，如 source.diehl-...,source.buzsaki...）")
    merge_p.add_argument("--output", help="输出路径（可选）")
    merge_p.set_defaults(func=_run_manage)

    filter_p = manage_sub.add_parser("filter", help="筛选知识库")
    filter_p.add_argument("--conditions", help="筛选条件 JSON 文件 (可选，内置 has_zotero_key/has_doi/pageType)")
    filter_p.add_argument("--has-zotero-key", type=lambda v: v.lower() == 'true', help="true/false")
    filter_p.add_argument("--has-doi", type=lambda v: v.lower() == 'true', help="true/false")
    filter_p.add_argument("--page-type", help="pageType 值")
    filter_p.set_defaults(func=_run_manage)

    list_p = manage_sub.add_parser("list", help="列出所有 wiki source")
    list_p.set_defaults(func=_run_manage)

    stats_p = manage_sub.add_parser("stats", help="查看 wiki 统计信息")
    stats_p.set_defaults(func=_run_manage)

    info_p = manage_sub.add_parser("info", help="查看 wiki source 详情（如指定 --source-id）或总统计（默认）")
    # v6.0.6+：manage info --source-id 返回单篇 source 详情（audit #2 修复，v6.0.3 文档广告但代码未实现）
    info_p.add_argument("--source-id",
                        help="wiki source id（如 source.diehl-2026-captured-memories）；不传则退化为 stats 总统计")
    info_p.set_defaults(func=_run_manage)

    # ── synthesize ───────────────────────────────────────────────
    synth_parser = sub.add_parser("synthesize", help="文献综述合成 (Synthesizer)")
    synth_sub = synth_parser.add_subparsers(dest="synth_cmd")

    extract_p = synth_sub.add_parser("extract", help="从 topic JSON 提取结构化笔记为 Markdown")
    extract_p.add_argument("--source-id", required=True,
                          help="wiki source id (如 source.diehl-2026-captured-memories)")
    extract_p.add_argument("--output", help="输出 Markdown 路径（可选）")
    extract_p.set_defaults(func=_run_synthesize)
    # v6.0.5: synthesize check/fix 已彻底从 argparse 删除（v6.0.4 文档修复不彻底）
    # APA 7 引用核验请走 references/apa7-standards.md（agent 手动跑）

    # ── download（多态：DOI/key → Zotero → 坚果云 → wiki）─────────
    download_parser = sub.add_parser(
        "download", help="PDF 下载（Zotero 库 → 坚果云 WebDAV → wiki raw）"
    )
    dl_mode = download_parser.add_mutually_exclusive_group(required=True)
    dl_mode.add_argument("--doi", metavar="DOI",
                         help="DOI（如 10.1177/0956797617694868）")
    dl_mode.add_argument("--zotero-key", metavar="KEY",
                         help="Zotero item key（8 字符，如 R8MVF42R）")
    download_parser.add_argument(
        "--wiki-raw-dir", default="/root/.openclaw/wiki/raw/papers",
        help="wiki raw 目录（默认 /root/.openclaw/wiki/raw/papers）"
    )
    download_parser.add_argument(
        "--tmp-dir", default="/tmp/zotero_dl",
        help="临时下载目录（默认 /tmp/zotero_dl）"
    )
    download_parser.set_defaults(func=_run_download)

    # ── upload（v6.0.3+ 本地 PDF 反向上传：download 的反向对偶）──
    upload_parser = sub.add_parser(
        "upload", help="本地 PDF 上传到 Zotero + WebDAV + wiki source（v6.0.3+）"
    )
    upload_parser.add_argument("--pdf-path", required=True,
                               help="本地 PDF 路径")
    upload_parser.add_argument("--slug", help="wiki source slug（必填或 --doi；agent 自決唯一标识）")
    upload_parser.add_argument("--doi", help="DOI（如有则建 Zotero 条目）")
    upload_parser.add_argument("--title", help="wiki source title（默认用 slug）")
    upload_parser.add_argument("--tags", help="Zotero tags（逗号分隔）")
    upload_parser.add_argument("--no-zotero", action="store_true", help="跳过 Zotero 建条目")
    upload_parser.add_argument("--no-webdav", action="store_true", help="跳过 WebDAV 推")
    upload_parser.add_argument("--no-wiki", action="store_true", help="跳过 wiki source 创建")
    upload_parser.set_defaults(func=_run_upload)

    # ── maintain（wiki-zotero-webdav 一致性维护，v5.20.0 新增 CLI 入口）──
    maintain_parser = sub.add_parser(
        "maintain", help="wiki-zotero-webdav 一致性维护（WikiZoteroManager）"
    )
    maintain_sub = maintain_parser.add_subparsers(dest="maintain_cmd", required=True)

    drift_p = maintain_sub.add_parser(
        "check-drift", help="检查 wiki source ↔ Zotero ↔ WebDAV 一致性"
    )
    drift_p.set_defaults(func=_run_maintain)

    missing_p = maintain_sub.add_parser(
        "list-missing", help="列出缺 zotero_item_key 的 sources"
    )
    missing_p.set_defaults(func=_run_maintain)

    report_p = maintain_sub.add_parser(
        "report", help="生成漂移报告 markdown 到 wiki/reports/"
    )
    report_p.add_argument(
        "--output", help="输出 markdown 路径（可选，默认 wiki/reports/wiki-zotero-drift-<date>.md）"
    )
    report_p.set_defaults(func=_run_maintain)

    graph_p = maintain_sub.add_parser(
        "drift-graph", help="三方联动 ASCII 状态图（v6.0.0 新增；默认 light 模式秒级完成，--full 跑完整三方）"
    )
    graph_p.add_argument(
        "--full", action="store_true",
        help="跑完整三方检查（耗时 1-5 分钟，依赖 source 数量）"
    )
    graph_p.set_defaults(func=_run_maintain)

    args = parser.parse_args(argv)
    if not args.module:
        parser.print_help()
        return 1
    return args.func(args)


# ── 命令实现 ─────────────────────────────────────────────

def _run_search(args) -> int:
    """search 子命令（v5.19.0 起走 wiki report；v6.0.6+ 触发 fallback 时主动提示）

    v6.0.6 改动（audit #3 修复）：
      - 改走 scripts.search.search_by_keyword()（中文/英文/启发式主备路由 + fallback_used 标记）
      - CLI 输出包含 fallback_used / fallback_reason 字段（用户能感知 fallback 是否已触发）
      - wiki report 仍写（fallback 命中的论文也进 report）
    """
    import json
    from scripts.search import search_by_keyword
    from scripts.search.WikiSearchReport import WikiSearchReport

    topic = getattr(args, 'topic', None) or 'general'
    keyword = args.keyword or 'unknown'
    limit = getattr(args, 'limit', 20)
    year_min = getattr(args, 'year_min', None)
    year_max = getattr(args, 'year_max', None)
    write_report = not getattr(args, 'dry_run', False)

    # v6.0.6+：调 search_by_keyword() 获取 fallback_used 信息
    # （WikiSearchReport 默认走 SemSch 不会触发 fallback，这里走 search_by_keyword 拿到主备路由 + fallback 标记）
    search_results = search_by_keyword(
        keyword,
        limit=limit,
        year_min=year_min,
        year_max=year_max,
        include_fallback=True,
    )
    meta = search_results.pop("_meta", {}) or {}
    # 聚合所有来源的 papers
    all_papers = []
    for src, papers in search_results.items():
        for p in papers:
            d = p.to_dict() if hasattr(p, "to_dict") else (p if isinstance(p, dict) else {})
            d["source"] = src
            all_papers.append(d)

    # 写 wiki report（如需要）
    wiki_report_path = "N/A (dry-run)"
    if write_report and all_papers:
        try:
            ws = WikiSearchReport(topic=topic)
            queries = {'queries': [{'query': keyword, 'limit': limit}]}
            wr_result = ws.search(queries, write_report=True)
            wiki_report_path = wr_result.get('wiki_report_path', 'N/A')
        except Exception as e:
            wiki_report_path = f"failed: {e}"

    # v6.0.6+：CLI 输出包含 fallback_used 信息（audit #3）
    output = {
        'success': True,
        'papers_count': len(all_papers),
        'keyword': keyword,
        'primary_engine': meta.get('primary_engine', 'unknown'),
        'fallback_engine': meta.get('fallback_engine', 'unknown'),
        'fallback_used': meta.get('fallback_used'),  # None | 'CNKI' | 'Semantic Scholar' | 'Google Scholar' | 'arXiv'
        'fallback_reason': meta.get('fallback_reason'),  # None | str
        'fallback_count': meta.get('fallback_count', 0),
        'wiki_report_path': wiki_report_path,
        'wiki_topic': topic,
    }
    # 主动提示 fallback（用户视角可见）
    if output['fallback_used']:
        print(
            f"⚠️ fallback 已触发：{output['primary_engine']} 0 命中 → 切到 {output['fallback_used']}（{output['fallback_reason']}）",
            file=sys.stderr,
        )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0
def _run_summarize(args) -> int:
    import json
    from scripts.summarize.Summarizer import Summarizer as WikiSummesizer
    summarizer = WikiSummesizer()
    pdf_path = getattr(args, 'pdf_path', None)
    do_ocr = getattr(args, 'ocr', False)
    if getattr(args, 'source_id', None):
        result = summarizer.summarize(args.source_id, args.output, pdf_path=pdf_path, do_ocr=do_ocr)
    else:
        result = {"success": False, "error": "需要 --source-id 参数（v5.16.0 wiki 版本）"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _run_manage(args) -> int:
    import json
    from scripts.manage.Manager import Manager
    m = Manager()
    if args.manage_cmd == "list":
        sources = m.list_sources()
        print(json.dumps({"success": True, "count": len(sources), "sources": sources}, ensure_ascii=False, indent=2))
    elif args.manage_cmd == "merge":
        ids = args.inputs.split(",") if hasattr(args, 'inputs') and args.inputs else []
        result = m.merge(*ids)
        print(json.dumps({"success": True, "merged_count": len(result), "merged": [s['id'] for s in result]}, ensure_ascii=False, indent=2))
    elif args.manage_cmd == "filter":
        conditions = {}
        if hasattr(args, 'has_zotero_key') and args.has_zotero_key is not None:
            conditions['has_zotero_key'] = args.has_zotero_key
        if hasattr(args, 'has_doi') and args.has_doi is not None:
            conditions['has_doi'] = args.has_doi
        if hasattr(args, 'page_type') and args.page_type:
            conditions['pageType'] = args.page_type
        if hasattr(args, 'conditions') and args.conditions:
            with open(args.conditions) as f:
                conditions.update(json.load(f))
        result = m.filter(conditions)
        print(json.dumps({"success": True, "count": len(result), "sources": result}, ensure_ascii=False, indent=2))
    elif args.manage_cmd in ("info", "stats"):
        # v6.0.6+：manage info --source-id 返回单篇 source 详情；不传则退化为 stats（audit #2）
        source_id = getattr(args, "source_id", None)
        if args.manage_cmd == "info" and source_id:
            # 单篇 source 详情（走 list_sources + 匹配 + 读 frontmatter）
            try:
                sources = m.list_sources()
                match = next((s for s in sources if s.get("id") == source_id or s.get("name") == source_id), None)
                if not match:
                    print(json.dumps({"success": False, "error": f"未找到 source: {source_id}"}, ensure_ascii=False, indent=2))
                    return 1
                # 读完整 frontmatter（不只是 list_sources 的摘要）
                from pathlib import Path
                fpath = Path(match.get("file", ""))
                wiki_root = Path("~/.openclaw/wiki").expanduser()
                full_path = (wiki_root / fpath) if not fpath.is_absolute() else fpath
                if not full_path.exists():
                    full_path = Path("/root/.openclaw/wiki") / fpath
                detail = dict(match)
                if full_path.exists():
                    content = full_path.read_text(encoding="utf-8")
                    import re as _re
                    yaml_match = _re.match(r'^---\s*\n(.*?)\n---', content, _re.DOTALL)
                    if yaml_match:
                        # 保留完整 frontmatter（agent 可看全字段）
                        detail["frontmatter_raw"] = yaml_match.group(1).strip()
                    detail["file_path"] = str(full_path)
                print(json.dumps({"success": True, "source": detail}, ensure_ascii=False, indent=2))
            except Exception as e:
                print(json.dumps({"success": False, "error": f"查询失败: {e}"}, ensure_ascii=False, indent=2))
                return 1
        else:
            stats = m.statistics()
            print(json.dumps({"success": True, "stats": stats}, ensure_ascii=False, indent=2))
    return 0


def _run_synthesize(args) -> int:
    """synthesize 子命令（v6.0.5：仅保留 extract，check/fix 已删除）

    check/fix 子命令在 v5.16.0 范围外未迁移到 wiki，v6.0.4 文档层删除后
    argparse 残留仍会接受参数。v6.0.5 彻底从 argparse + handler 删掉——
    调用 synthesize check/fix 会直接走 argparse 的 unrecognized arguments 路径。
    APA 7 引用核验请走 references/apa7-standards.md（agent 手动跑）。
    """
    import json
    from scripts.synthesize.Synthesizer import Synthesizer
    if args.synth_cmd == "extract":
        s = Synthesizer()
        if getattr(args, 'source_id', None):
            result = s.extract_notes(args.source_id, args.output)
        else:
            result = {"success": False, "error": "需要 source_id 参数（v5.16.0 wiki 版本）"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _run_download(args) -> int:
    """download 子命令：Zotero → 坚果云 → wiki 流水线"""
    import json
    identifier = args.doi or args.zotero_key
    try:
        dl = ZoteroJianguoyunDownloader(wiki_raw_dir=args.wiki_raw_dir)
        pdf_path = dl.run(identifier, dest_dir=Path(args.tmp_dir))
        meta = dl.find_paper(identifier)  # 重新拿元数据用于输出
        result = {
            "success": True,
            "identifier": identifier,
            "pdf_path": str(pdf_path),
            "size_bytes": pdf_path.stat().st_size,
            "title": meta.title,
            "authors": meta.authors,
            "year": meta.year,
            "zotero_item_key": meta.zotero_item_key,
            "zotero_attachment_key": meta.zotero_attachment_key,
            "archive_filename": meta.archive_filename(),
        }
    except Exception as e:
        result = {
            "success": False,
            "identifier": identifier,
            "error": str(e),
        }
        print(json.dumps(result, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _run_upload(args) -> int:
    """upload 子命令（v6.0.3+）：本地 PDF 反向上传（download 的反向对偶）"""
    import json
    from scripts.upload.Uploader import Uploader
    if not args.doi and not args.slug:
        print(json.dumps({"success": False, "error": "需要 --doi 或 --slug 其中之一（agent 自決唯一标识）"}, ensure_ascii=False, indent=2))
        return 1
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    u = Uploader()
    result = u.run(
        pdf_path=args.pdf_path,
        doi=args.doi,
        slug=args.slug,
        title=args.title,
        tags=tags or None,
        no_zotero=args.no_zotero,
        no_webdav=args.no_webdav,
        no_wiki=args.no_wiki,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


def _run_maintain(args) -> int:
    """maintain 子命令（v5.20.0 新增）：WikiZoteroManager 一致性检查入口"""
    import json
    from scripts.maintain.WikiZoteroManager import WikiZoteroManager

    m = WikiZoteroManager()

    if args.maintain_cmd == "check-drift":
        result = m.check_drift()
        output = {
            "success": True,
            "ok_count": len(result.get("ok", [])),
            "missing_key_count": len(result.get("missing_key", [])),
            "zotero_not_found_count": len(result.get("zotero_not_found", [])),
            "webdav_missing_count": len(result.get("webdav_missing", [])),
            "non_academic_count": len(result.get("non_academic", [])),
            "ok_sources": [s["name"] for s in result.get("ok", [])],
            "missing_key_sources": [s["name"] for s in result.get("missing_key", [])],
            "zotero_not_found": result.get("zotero_not_found", []),
            "webdav_missing": result.get("webdav_missing", []),
            "non_academic_sources": [s["name"] for s in result.get("non_academic", [])],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.maintain_cmd == "list-missing":
        missing = m.find_missing_zotero_keys()
        output = {
            "success": True,
            "count": len(missing),
            "sources": [
                {"name": s.get("name"), "file": s.get("file")}
                for s in missing
            ],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.maintain_cmd == "report":
        drift = m.check_drift()
        report_path = m.generate_drift_report(drift)
        output = {
            "success": True,
            "report_path": str(report_path) if report_path else None,
            "ok_count": len(drift.get("ok", [])),
            "missing_key_count": len(drift.get("missing_key", [])),
            "zotero_not_found_count": len(drift.get("zotero_not_found", [])),
            "webdav_missing_count": len(drift.get("webdav_missing", [])),
            "non_academic_count": len(drift.get("non_academic", [])),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.maintain_cmd == "drift-graph":
        mode = "full" if getattr(args, "full", False) else "light"
        print(m.generate_drift_graph(mode=mode))

    return 0


if __name__ == "__main__":
    sys.exit(main())
