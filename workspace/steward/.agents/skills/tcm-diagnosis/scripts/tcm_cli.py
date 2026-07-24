#!/usr/bin/env python3
"""tcm_cli.py — 中医辨证 CLI（v1.0.0）

用法：
    tcm diagnose --symptoms "头痛3天，怕冷，无汗，舌苔白，脉浮紧"
    tcm diagnose --symptoms "..." --json          # JSON 输出
    tcm diagnose --symptoms "..." --top-n 5
    tcm --self-test                              # 跑 test_cases.json
    tcm --self-test 风寒感冒                     # 跑指定用例（按 title 匹配）
    tcm list                                     # 列出全部证型
    tcm list-formulas                            # 列出全部方剂
    tcm version                                  # 版本
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# 同目录导入
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tcm_diagnose import TCMDiagnose, run_self_test, ZHENG_TABLE, FORMULA_TABLE  # noqa: E402

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
TEST_CASES = HERE / "test_cases.json"


# ============================================================================
# 命令实现
# ============================================================================

def cmd_diagnose(args) -> int:
    """输出单次辨证结果."""
    diag = TCMDiagnose(skill_root=SKILL_ROOT)
    out = diag.diagnose(args.symptoms, top_n=args.top_n)

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    # 人类可读
    print("=" * 70)
    print(f"中医辨证技能 v1.0.0 · 输入症状：{args.symptoms}")
    print("=" * 70)
    bagang = out["bagang"]
    print(f"\n【八纲】  表里={bagang['表里']}  寒热={bagang['寒热']}  虚实={bagang['虚实']}  阴阳={bagang['阴阳']}")

    print(f"\n【候选证型】（共 {len(out['zheng_candidates'])} 条）")
    for i, z in enumerate(out["zheng_candidates"], 1):
        print(f"  {i}. {z['id']}  {z['name']}  "
              f"[{z['category']}]  score={z['score']}  "
              f"舌：{z['tongue']}  脉：{z['pulse']}")
        print(f"     教材来源：{z['source']}")

    if out["formulas"]:
        print(f"\n【对应方剂】")
        for i, f in enumerate(out["formulas"], 1):
            herbs_str = "、".join(f["herbs"]) if f["herbs"] else "—"
            print(f"  {i}. {f['name']}（{f['formula_id']}）  [{f['category']}]")
            print(f"     主治：{f['indications']}")
            print(f"     组成药物：{herbs_str}  ⚠️ 不含剂量")
            print(f"     出处：{f['source']}")

    print("\n" + "─" * 70)
    print("⚠️  免责声明")
    print("─" * 70)
    print(out["disclaimer"]["text"].split("\n")[1] if "\n" in out["disclaimer"]["text"] else out["disclaimer"]["text"])
    print("─" * 70)
    print(f"\n（完整 disclaim 见 references/tcm-disclaimer.md）")
    return 0


def cmd_self_test(args) -> int:
    """跑自测用例."""
    if not TEST_CASES.exists():
        print(f"ERROR: 测试用例文件不存在: {TEST_CASES}", file=sys.stderr)
        return 2
    summary = run_self_test(SKILL_ROOT)
    target = getattr(args, "target", None)  # 可选：指定 title 过滤

    if target:
        # 过滤指定用例
        filtered = [r for r in summary["results"]
                    if target in r["case_title"] or target in r["case_id"]]
        if not filtered:
            print(f"ERROR: 未找到匹配 '{target}' 的用例", file=sys.stderr)
            return 2
        print(f"--- 自测子集（{len(filtered)}/{summary['total']}）---")
        results_to_show = filtered
    else:
        results_to_show = summary["results"]

    # 表格
    print()
    print(f"{'用例':28s} | {'期望':22s} | {'实际':22s} | {'得分':5s} | {'主方':18s}")
    print("-" * 110)
    pass_count = 0
    for r in results_to_show:
        ok = "✅" if r["passed"] else "❌"
        print(f"{r['case_title']:28s} | {r['expected']:22s} | "
              f"{r['got'] or '-':22s} | {ok}      | {r['formula'] or '-':18s}")
        if r["passed"]:
            pass_count += 1

    total_shown = len(results_to_show)
    print("-" * 110)
    print(f"通过 {pass_count}/{total_shown}")

    if target:
        # 仍返回整体分数
        return 0 if pass_count == total_shown else 1
    return 0 if summary["passed"] == summary["total"] else 1


def cmd_list(args) -> int:
    """列出全部证型."""
    cats = sorted(set(z.get("category", "?") for z in ZHENG_TABLE))
    print("=== 中医证型表（共 {} 条）===\n".format(len(ZHENG_TABLE)))
    for cat in cats:
        items = [z for z in ZHENG_TABLE if z.get("category") == cat]
        print(f"▸ {cat}（{len(items)} 条）")
        for z in items:
            print(f"   {z['id']:<22s}  {z['name']}")
        print()
    print(f"\n总计：{len(ZHENG_TABLE)} 条证型")
    return 0


def cmd_list_formulas(args) -> int:
    """列出全部方剂."""
    print(f"=== 中医经典方剂表（共 {len(FORMULA_TABLE)} 首）===\n")
    cats = sorted(set(f.get("category", "?") for f in FORMULA_TABLE.values()))
    for cat in cats:
        items = [(k, f) for k, f in FORMULA_TABLE.items() if f.get("category") == cat]
        print(f"▸ {cat}（{len(items)} 首）")
        for k, f in items:
            herbs = "、".join(f["herbs"])
            print(f"   {k}  {f['name']:<18s}  组成：{herbs}")
        print()
    print(f"\n总计：{len(FORMULA_TABLE)} 首方剂（**均不含剂量**）")
    return 0


def cmd_version(args) -> int:
    """显示版本."""
    print("tcm-diagnosis  v1.0.0")
    print(f"skill root: {SKILL_ROOT}")
    print(f"zheng entries: {len(ZHENG_TABLE)}")
    print(f"formula entries: {len(FORMULA_TABLE)}")
    return 0


# ============================================================================
# argparse 主入口
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tcm",
        description="中医辨证技能 v1 —— 文本症状 → 八纲 → 证型 → 方剂（**仅学习参考，非医疗建议**）",
    )
    sub = p.add_subparsers(dest="cmd")

    # diagnose
    pd = sub.add_parser("diagnose", help="辨证推理：文本症状 → 八纲/证型/方剂")
    pd.add_argument("--symptoms", "-s", required=True,
                    help='症状描述，例如 "头痛3天，怕冷，无汗，鼻塞流清涕，脉浮紧"')
    pd.add_argument("--json", action="store_true", help="输出 JSON")
    pd.add_argument("--top-n", type=int, default=3,
                    help="返回候选证型条数（默认 3）")
    pd.set_defaults(func=cmd_diagnose)

    # self-test
    pst = sub.add_parser("self-test", aliases=["test"], help="跑内置测试用例")
    pst.add_argument("target", nargs="?", default=None,
                     help="可选：按 title 过滤指定用例")
    pst.set_defaults(func=cmd_self_test)

    # list
    pl = sub.add_parser("list", help="列出证型")
    pl.set_defaults(func=cmd_list)

    # list-formulas
    plf = sub.add_parser("list-formulas", help="列出方剂")
    plf.set_defaults(func=cmd_list_formulas)

    # version
    pv = sub.add_parser("version", help="版本与统计")
    pv.set_defaults(func=cmd_version)

    return p


def main(argv=None) -> int:
    parser = build_parser()
    # 简化的入口：接受 `tcm subcmd ...`、`tcm --symptoms ...`、以及不带 subcmd 的 `--symptoms`
    if argv is None:
        argv = sys.argv[1:]

    # 优化：若首参不是任何已知 subcommand（含 --symptoms），自动前置 diagnose
    if not argv:
        parser.print_help()
        return 0

    if argv[0] in ("list", "list-formulas", "diagnose", "self-test", "test", "version"):
        pass  # OK
    elif "--symptoms" in argv or "-s" in argv:
        argv = ["diagnose"] + argv
    else:
        parser.print_help()
        return 2

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 2
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
