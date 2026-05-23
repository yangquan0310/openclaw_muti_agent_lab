#!/usr/bin/env python3
"""CLI 统一入口：整合研究助手所有子命令。"""

import argparse
import sys
from pathlib import Path

# Fix-01: 添加项目根目录到 path，解决 ModuleNotFoundError
sys.path.insert(0, str(Path(__file__).parent.parent))

# 统一导出
from scripts import Searcher, Summarizer, Manager, Synthesizer


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="research-assistant CLI")
    sub = parser.add_subparsers(dest="module", help="模块")

    # search
    search_parser = sub.add_parser("search", help="文献检索 (Searcher)")
    search_parser.add_argument("--kb-path", default="index.json", help="知识库路径")
    search_parser.add_argument("--queries", required=True, help="检索条件 JSON 文件")
    search_parser.add_argument("--fields", help="请求字段")
    search_parser.add_argument("--no-deduplicate", action="store_true", help="不去重")
    search_parser.set_defaults(func=_run_search)

    # summarize
    sum_parser = sub.add_parser("summarize", help="文献总结 (Summarizer)")
    sum_parser.add_argument("--kb-path", default="index.json", help="知识库路径")
    sum_parser.add_argument("--progress-interval", type=int, default=10, help="进度间隔")
    sum_parser.set_defaults(func=_run_summarize)

    # manage
    manage_parser = sub.add_parser("manage", help="知识库管理 (Manager)")
    manage_sub = manage_parser.add_subparsers(dest="manage_cmd")
    merge_parser = manage_sub.add_parser("merge", help="合并知识库")
    merge_parser.add_argument("--inputs", required=True, help="输入文件（逗号分隔）")
    merge_parser.add_argument("--output", required=True, help="输出路径")
    merge_parser.set_defaults(func=_run_manage)
    filter_parser = manage_sub.add_parser("filter", help="筛选知识库")
    filter_parser.add_argument("--kb-path", default="index.json", help="知识库路径")
    filter_parser.add_argument("--output", help="输出路径")
    filter_parser.add_argument("--conditions", help="筛选条件 JSON 文件")
    filter_parser.set_defaults(func=_run_manage)
    info_parser = manage_sub.add_parser("info", help="查看知识库信息")
    info_parser.add_argument("--kb-path", default="index.json", help="知识库路径")
    info_parser.set_defaults(func=_run_manage)

    # synthesize
    synth_parser = sub.add_parser("synthesize", help="文献综述合成 (Synthesizer)")
    synth_sub = synth_parser.add_subparsers(dest="synth_cmd")
    extract_parser = synth_sub.add_parser("extract", help="提取笔记信息")
    extract_parser.add_argument("--notes", required=True, help="笔记 JSON 文件路径")
    extract_parser.set_defaults(func=_run_synthesize)
    check_parser = synth_sub.add_parser("check", help="检查参考文献")
    check_parser.add_argument("--doc", required=True, help="文档路径")
    check_parser.add_argument("--kb", required=True, action="append", help="知识库路径（可多次）")
    check_parser.set_defaults(func=_run_synthesize)
    fix_parser = synth_sub.add_parser("fix", help="修复参考文献")
    fix_parser.add_argument("--doc", required=True, help="文档路径")
    fix_parser.add_argument("--kb", required=True, action="append", help="知识库路径（可多次）")
    fix_parser.add_argument("--output", help="输出路径")
    fix_parser.set_defaults(func=_run_synthesize)

    args = parser.parse_args(argv)
    if not args.module:
        parser.print_help()
        return 1
    return args.func(args)


def _run_search(args) -> int:
    searcher = Searcher(kb_path=args.kb_path)
    import json
    with open(args.queries) as f:
        queries = json.load(f)
    kb = searcher.search(queries, fields=args.fields, deduplicate=not args.no_deduplicate)
    print(json.dumps({"success": True, "count": len(kb.get("papers", []))}, ensure_ascii=False))
    return 0


def _run_summarize(args) -> int:
    summarizer = Summarizer(kb_path=args.kb_path)
    kb = summarizer.summarize()
    print(json.dumps({"success": True, "count": len(kb.get("papers", []))}, ensure_ascii=False))
    return 0


def _run_manage(args) -> int:
    import json
    if args.manage_cmd == "merge":
        manager = Manager()
        inputs = args.inputs.split(",")
        manager.merge(*inputs).save(args.output)
        print(json.dumps({"success": True, "output": args.output}, ensure_ascii=False))
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
        print(json.dumps({"success": True, "info": kb.get("statistics", {})}, ensure_ascii=False))
    return 0


def _run_synthesize(args) -> int:
    import json
    if args.synth_cmd == "extract":
        synthesizer = Synthesizer()
        result = synthesizer.extract(args.notes)
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
