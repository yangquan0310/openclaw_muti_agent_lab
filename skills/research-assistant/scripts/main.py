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
    search_parser.add_argument("--kb-path", default="knowledge/index.json",
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
    search_parser.set_defaults(func=_run_search)

    # ── summarize ─────────────────────────────────────────────
    sum_parser = sub.add_parser("summarize", help="文献总结 (Summarizer)")
    sum_parser.add_argument("--kb-path", default="knowledge/index.json",
                            help="知识库路径")
    sum_parser.add_argument("--progress-interval", type=int, default=10,
                            help="进度间隔（秒，默认 10）")
    sum_parser.set_defaults(func=_run_summarize)

    # ── manage ──────────────────────────────────────────────────
    manage_parser = sub.add_parser("manage", help="知识库管理 (Manager)")
    manage_sub = manage_parser.add_subparsers(dest="manage_cmd")

    merge_p = manage_sub.add_parser("merge", help="合并知识库")
    merge_p.add_argument("--inputs", required=True,
                         help="输入文件（逗号分隔）")
    merge_p.add_argument("--output", required=True, help="输出路径")
    merge_p.set_defaults(func=_run_manage)

    filter_p = manage_sub.add_parser("filter", help="筛选知识库")
    filter_p.add_argument("--kb-path", default="knowledge/index.json",
                          help="知识库路径")
    filter_p.add_argument("--output", help="输出路径")
    filter_p.add_argument("--conditions", help="筛选条件 JSON 文件")
    filter_p.set_defaults(func=_run_manage)

    info_p = manage_sub.add_parser("info", help="查看知识库信息")
    info_p.add_argument("--kb-path", default="knowledge/index.json",
                        help="知识库路径")
    info_p.set_defaults(func=_run_manage)

    # ── synthesize ───────────────────────────────────────────────
    synth_parser = sub.add_parser("synthesize", help="文献综述合成 (Synthesizer)")
    synth_sub = synth_parser.add_subparsers(dest="synth_cmd")

    extract_p = synth_sub.add_parser("extract", help="从 topic JSON 提取结构化笔记为 Markdown")
    extract_p.add_argument("--topic", required=True,
                          help="topic JSON 文件路径（如 knowledge/topic/xxx.json）")
    extract_p.add_argument("--output", help="输出 Markdown 路径（默认 knowledge/note/笔记_{主题}.md）")
    extract_p.set_defaults(func=_run_synthesize)

    check_p = synth_sub.add_parser("check", help="检查参考文献")
    check_p.add_argument("--doc", required=True, help="文档路径")
    check_p.add_argument("--kb", required=True, action="append",
                        help="知识库路径（可多次）")
    check_p.set_defaults(func=_run_synthesize)

    fix_p = synth_sub.add_parser("fix", help="修复参考文献")
    fix_p.add_argument("--doc", required=True, help="文档路径")
    fix_p.add_argument("--kb", required=True, action="append",
                       help="知识库路径（可多次）")
    fix_p.add_argument("--output", help="输出路径")
    fix_p.set_defaults(func=_run_synthesize)

    args = parser.parse_args(argv)
    if not args.module:
        parser.print_help()
        return 1
    return args.func(args)


# ── 命令实现 ─────────────────────────────────────────────

def _run_search(args) -> int:
    import json
    if args.queries:
        # 模式 1：JSON 条件文件（兼容原有 Searcher）
        searcher = OldSearcher(kb_path=args.kb_path)
        with open(args.queries) as f:
            queries = json.load(f)
        kb = searcher.search(
            queries,
            fields=args.fields,
            deduplicate=not args.no_deduplicate,
        )
        stats = kb.get("statistics", {})
        print(json.dumps({
            "success": True,
            "mode": "queries",
            "count": stats.get("total_count", 0),
        }, ensure_ascii=False))

    else:
        # 模式 2：关键词（语言自动路由）
        results = search_by_keyword(
            keyword=args.keyword,
            kb_path=args.kb_path,
            limit=args.limit,
            year_min=args.year_min,
            year_max=args.year_max,
        )
        total = sum(len(papers) for papers in results.values())
        sources = list(results.keys())
        print(json.dumps({
            "success": True,
            "mode": "keyword",
            "keyword": args.keyword,
            "total": total,
            "sources": sources,
        }, ensure_ascii=False))

    return 0


def _run_summarize(args) -> int:
    summarizer = Summarizer(kb_path=args.kb_path)
    kb = summarizer.summarize()
    print(json.dumps({
        "success": True,
        "count": len(kb.get("papers", [])),
    }, ensure_ascii=False))
    return 0


def _run_manage(args) -> int:
    import json
    if args.manage_cmd == "merge":
        manager = Manager()
        manager.merge(*args.inputs.split(",")).save(args.output)
        print(json.dumps({"success": True, "output": args.output},
                         ensure_ascii=False))
    elif args.manage_cmd == "filter":
        manager = Manager(args.kb_path)
        conditions = {}
        if args.conditions:
            with open(args.conditions) as f:
                conditions = json.load(f)
        manager.filter(conditions).save(args.output)
        print(json.dumps({"success": True}, ensure_ascii=False))
    elif args.manage_cmd == "info":
        manager = Manager(args.kb_path)
        kb = manager.get_kb()
        print(json.dumps({"success": True, "info": kb.get("statistics", {})},
                         ensure_ascii=False))
    return 0


def _run_synthesize(args) -> int:
    import json
    if args.synth_cmd == "extract":
        synthesizer = Synthesizer()
        result = synthesizer.extract_notes(args.topic, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.synth_cmd == "check":
        synthesizer = Synthesizer(*args.kb)
        result = synthesizer.check_references(args.doc)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.synth_cmd == "fix":
        synthesizer = Synthesizer(*args.kb)
        synthesizer.check_references(args.doc)
        result = synthesizer.fix_references(args.doc, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
