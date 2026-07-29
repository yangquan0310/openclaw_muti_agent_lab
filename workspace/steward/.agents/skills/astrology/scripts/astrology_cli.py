#!/usr/bin/env python3
"""西方占星排盘 CLI.

用法：
    astrology 1990-05-15 14:30                          # 基础排盘（默认北京）
    astrology 1990-05-15 14:30 --location "纽约"          # 指定地点
    astrology 1990-05-15 14:30 --json                   # JSON 输出
    astrology 1990-05-15 14:30 --focus love career      # 聚焦 2 个领域
    astrology 1990-05-15 14:30 --focus all              # 全部 10 领域
    astrology 1990-05-15 14:30 --compatibility 1992-08-22   # 合盘
    astrology --self-test                               # 跑 test_cases.json 全部用例
    astrology --self-test 1990-05-15                    # 跑指定 input

⚠️ 本 CLI 仅供学术研究与文化记录使用。
   - 不构成医学/心理学/投资/婚恋建议
   - 占星术无科学因果证据
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# 允许同目录下导入 astrology 模块
sys.path.insert(0, str(Path(__file__).resolve().parent))
from astrology import (  # noqa: E402
    build_chart_from_str,
    compatibility,
    DOMAIN_LABEL,
    Chart,
)


HERE = Path(__file__).resolve().parent
TEST_CASES = HERE.parent / "test_cases.json"


# ============================================================================
# 子命令
# ============================================================================

def cmd_chart(args, chart: Chart) -> int:
    """基础排盘输出."""
    if args.focus:
        domains = _parse_focus(args.focus)
        print(chart.pretty())
        print("=" * 60)
        for d in domains:
            print(chart.profile_text(d))
            print("-" * 60)
    else:
        print(chart.pretty())
    return 0


def cmd_chart_json(args, chart: Chart) -> int:
    """JSON 输出."""
    out = chart.to_dict()
    if args.focus:
        domains = _parse_focus(args.focus)
        # 只保留指定领域
        if "profile" in out and out["profile"]:
            out["profile"] = {d: out["profile"][d] for d in domains
                              if d in out["profile"]}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def cmd_compatibility(args, chart_a: Chart) -> int:
    """合盘."""
    date_b = args.compatibility
    time_b = args.compatibility_time or "12:00"
    loc_b = args.location or "北京"
    chart_b = build_chart_from_str(date_b, time_b, location=loc_b)
    chart_b.profile = chart_b.profile or None

    result = compatibility(chart_a, chart_b)

    print(f"合盘对象：{date_b} {time_b} @ {loc_b}")
    print(f"综合匹配分（仅文化参考）：{result['score']}/100")
    print(f"软相位：{result['soft_count']}  硬相位：{result['hard_count']}  合相：{result['conjunction_count']}")
    print()

    print("主要相位（A 行星 vs B 行星）：")
    for asp in result["aspects"]:
        print(f"  A.{asp['a_planet']} {asp['symbol']} B.{asp['b_planet']}"
              f"（容许度±{asp['orb']}°，{asp['kind']}）")
    print()

    print("同星座行星：")
    for ov in result["overlap_signs"][:8]:
        print(f"  A.{ov['planet']} & B.{ov['b_planet']} → {ov['sign']}")
    print()

    print("A 行星落入 B 宫位：")
    for ov in result["overlap_houses"]:
        print(f"  A.{ov['a_planet']} → B {ov['b_house']} 宫")
    print()

    print("⚠️ 本合盘仅作文化/学术层面的描述，不替代关系评估。")
    return 0


def cmd_compatibility_json(args, chart_a: Chart) -> int:
    """合盘 JSON."""
    date_b = args.compatibility
    time_b = args.compatibility_time or "12:00"
    loc_b = args.location or "北京"
    chart_b = build_chart_from_str(date_b, time_b, location=loc_b)

    result = compatibility(chart_a, chart_b)
    out = {
        "a_solar": chart_a.solar.strftime("%Y-%m-%d %H:%M"),
        "a_location": chart_a.location,
        "b_solar": chart_b.solar.strftime("%Y-%m-%d %H:%M"),
        "b_location": chart_b.location,
        "score": result["score"],
        "soft_count": result["soft_count"],
        "hard_count": result["hard_count"],
        "conjunction_count": result["conjunction_count"],
        "aspects": result["aspects"],
        "overlap_signs": result["overlap_signs"],
        "overlap_houses": result["overlap_houses"],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def cmd_self_test(args) -> int:
    """跑 test_cases.json 全部用例."""
    if not TEST_CASES.exists():
        print(f"ERROR: 测试用例文件不存在: {TEST_CASES}", file=sys.stderr)
        return 2
    with TEST_CASES.open(encoding="utf-8") as f:
        cases = json.load(f)
    filter_input = getattr(args, "self_test", None)
    if filter_input and filter_input != "__ALL__":
        cases = [c for c in cases if c.get("input") == filter_input]
        if not cases:
            print(f"ERROR: 用例 '{filter_input}' 未在 test_cases.json 中",
                  file=sys.stderr)
            return 1

    fail = 0
    for c in cases:
        ok, diff = _check_case(c)
        mark = "✓" if ok else "✗"
        ctype = c.get("case_type", "chart")
        desc = c.get("description", "")
        if ctype != "chart":
            label = c.get("input", "") + " " + ctype
            print(f"{mark} {label[:50]:50s} {desc}")
        else:
            inp = c.get("input", "")
            print(f"{mark} {inp[:30]:30s} {desc}")
        if not ok and diff:
            print(f"   diff: {diff}")
            fail += 1

    total = len(cases)
    passed = total - fail
    print()
    print(f"通过 {passed}/{total}")
    return 0 if fail == 0 else 1


# ============================================================================
# 自测用例断言
# ============================================================================

def _check_case(case: dict) -> tuple[bool, str]:
    ctype = case.get("case_type", "chart")
    if ctype == "chart":
        return _check_chart_case(case)
    elif ctype == "focus":
        return _check_focus_case(case)
    elif ctype == "compatibility":
        return _check_compatibility_case(case)
    return _check_chart_case(case)


def _check_chart_case(case: dict) -> tuple[bool, str]:
    """基础排盘用例：校验 sun/moon/rising/sign/degree/house 等核心字段."""
    inp = case["input"]
    date_part, _, time_part = inp.partition(" ")
    if not time_part:
        time_part = "12:00"
    loc = case.get("location", "北京")
    chart = build_chart_from_str(date_part, time_part, location=loc)
    actual = chart.to_dict()
    expected = case.get("expected", {})
    mismatches = []

    # Sun / Moon
    for body in ("sun", "moon"):
        exp = expected.get(body, {})
        act = actual.get(body, {})
        for key in ("sign", "house"):
            ev = exp.get(key)
            av = act.get(key)
            if ev is not None and ev != av:
                mismatches.append(f"{body}.{key}: exp={ev!r} act={av!r}")
        # degree 容许度 ±2°
        ev = exp.get("degree")
        av = act.get("degree")
        if ev is not None and av is not None:
            if abs(ev - av) > case.get("degree_tolerance", 2.0):
                mismatches.append(
                    f"{body}.degree: exp={ev!r} act={av!r} "
                    f"(tol={case.get('degree_tolerance', 2.0)})"
                )

    # Rising
    if "rising_sign" in expected:
        if expected["rising_sign"] != actual["rising_sign"]:
            mismatches.append(
                f"rising_sign: exp={expected['rising_sign']!r} "
                f"act={actual['rising_sign']!r}"
            )

    # 行星
    for planet_name, exp_p in expected.get("planets", {}).items():
        act_p = actual["planets"].get(planet_name, {})
        for key in ("sign", "house"):
            ev = exp_p.get(key)
            av = act_p.get(key)
            if ev is not None and ev != av:
                mismatches.append(
                    f"planets.{planet_name}.{key}: exp={ev!r} act={av!r}"
                )
        ev = exp_p.get("degree")
        av = act_p.get("degree")
        if ev is not None and av is not None:
            if abs(ev - av) > case.get("degree_tolerance", 2.0):
                mismatches.append(
                    f"planets.{planet_name}.degree: exp={ev!r} act={av!r}"
                )

    # Profile（领域强度）
    for domain, exp_d in expected.get("profile", {}).items():
        act_d = actual.get("profile", {}).get(domain, {})
        for key in ("intensity",):
            ev = exp_d.get(key)
            av = act_d.get(key)
            if ev is not None and av is not None:
                if abs(ev - av) > case.get("intensity_tolerance", 1.5):
                    mismatches.append(
                        f"profile.{domain}.{key}: exp={ev!r} act={av!r}"
                    )

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_focus_case(case: dict) -> tuple[bool, str]:
    """聚焦用例：单领域文本输出检查关键词出现."""
    inp = case["input"]
    date_part, _, time_part = inp.partition(" ")
    if not time_part:
        time_part = "12:00"
    loc = case.get("location", "北京")
    chart = build_chart_from_str(date_part, time_part, location=loc)
    domain = case["domain"]
    text = chart.profile_text(domain)
    expected_kw = case.get("expected_keywords", [])
    missing = [kw for kw in expected_kw if kw not in text]
    if missing:
        return False, f"缺少关键词: {missing}"
    return True, ""


def _check_compatibility_case(case: dict) -> tuple[bool, str]:
    """合盘用例."""
    inp_a = case["input"]
    date_a, _, time_a = inp_a.partition(" ")
    if not time_a:
        time_a = "12:00"
    loc_a = case.get("location", "北京")
    chart_a = build_chart_from_str(date_a, time_a, location=loc_a)

    inp_b = case["input_b"]
    date_b, _, time_b = inp_b.partition(" ")
    if not time_b:
        time_b = "12:00"
    loc_b = case.get("location_b", "北京")
    chart_b = build_chart_from_str(date_b, time_b, location=loc_b)

    result = compatibility(chart_a, chart_b)
    expected = case.get("expected", {})
    mismatches = []

    if "score_min" in expected and result["score"] < expected["score_min"]:
        mismatches.append(
            f"score: {result['score']} < min {expected['score_min']}"
        )
    if "score_max" in expected and result["score"] > expected["score_max"]:
        mismatches.append(
            f"score: {result['score']} > max {expected['score_max']}"
        )
    if "aspect_count_min" in expected and len(result["aspects"]) < expected["aspect_count_min"]:
        mismatches.append(
            f"aspects: {len(result['aspects'])} < min {expected['aspect_count_min']}"
        )

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


# ============================================================================
# 工具
# ============================================================================

def _parse_focus(arg) -> list[str]:
    """解析 --focus 参数：all / love / [love, career, wealth, ...] """
    if isinstance(arg, list):
        tokens = []
        for a in arg:
            if a == "all":
                return list(DOMAIN_LABEL.keys())
            tokens.extend(re.split(r"[,，\s]+", a.strip()))
    else:
        if arg.strip() == "all":
            return list(DOMAIN_LABEL.keys())
        tokens = re.split(r"[,，\s]+", arg.strip())
    valid = [t for t in tokens if t in DOMAIN_LABEL]
    return valid or list(DOMAIN_LABEL.keys())


def _validate_date(date_str: str) -> bool:
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_str))


# ============================================================================
# 主入口
# ============================================================================

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="astrology",
        description=(
            "西方占星排盘 / Western Astrology Natal Chart\n"
            "⚠️ 本工具仅供学术研究与文化记录使用，"
            "不构成医学/心理学/投资/婚恋建议。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("date", nargs="?", help="公历日期 YYYY-MM-DD")
    parser.add_argument("time", nargs="?", help="公历时间 HH:MM (默认 12:00)")
    parser.add_argument("--location", type=str, default="北京",
                        help="出生地（城市名或 'lat,lon,tz'）")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    parser.add_argument("--focus", type=str, nargs="+", default=None,
                        help="聚焦特定领域（love career wealth ... 或 all）")
    parser.add_argument("--compatibility", type=str, default=None,
                        metavar="YYYY-MM-DD",
                        help="合盘：另一人出生日期")
    parser.add_argument("--compatibility-time", type=str, default=None,
                        metavar="HH:MM",
                        help="合盘对象的出生时间（默认 12:00）")
    parser.add_argument("--compatibility-location", type=str, default=None,
                        help="合盘对象的出生地（默认同 --location）")
    parser.add_argument("--self-test", nargs="?", const="__ALL__", default=None,
                        help="跑 test_cases.json（可选指定 input 字段过滤）")

    args = parser.parse_args(argv)

    if args.self_test:
        return cmd_self_test(args)

    if not args.date:
        parser.print_help()
        return 1
    if not _validate_date(args.date):
        print(f"ERROR: 日期格式错误，期望 YYYY-MM-DD: {args.date}",
              file=sys.stderr)
        return 2
    time_str = args.time or "12:00"
    try:
        datetime.strptime(f"{args.date} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        print(f"ERROR: 时间格式错误，期望 HH:MM: {time_str}", file=sys.stderr)
        return 2

    # 构造命主盘
    try:
        chart = build_chart_from_str(args.date, time_str, location=args.location)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 3

    # 合盘
    if args.compatibility:
        if args.compatibility_location:
            # 用临时换 location
            saved_loc = args.location
            args.location = args.compatibility_location
            try:
                if args.json:
                    return cmd_compatibility_json(args, chart)
                return cmd_compatibility(args, chart)
            finally:
                args.location = saved_loc
        if args.json:
            return cmd_compatibility_json(args, chart)
        return cmd_compatibility(args, chart)

    # 单张排盘
    if args.json:
        return cmd_chart_json(args, chart)
    return cmd_chart(args, chart)


if __name__ == "__main__":
    raise SystemExit(main())