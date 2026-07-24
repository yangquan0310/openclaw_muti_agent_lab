#!/usr/bin/env python3
"""八字排盘 CLI.

用法：
    bazi 1996-03-10 14:30                          # 公历具体时间
    bazi 1996-03-10                                # 默认 12:00
    bazi 1996-03-10 14:30 --json                   # 输出 JSON
    bazi 1996-03-10 14:30 --liunian 2025           # 流年柱 + 与命局关系
    bazi 1996-03-10 14:30 --liumonth 2025-06       # 流月柱 + 与命局关系
    bazi 1996-03-10 14:30 --liushi 2025-06-15 14:30  # 流时柱 + 与命局关系
    bazi 1996-03-10 14:30 --liunian 2025 --json    # 流年 JSON
    bazi --self-test                               # 跑 test_cases.json 全部用例
    bazi --self-test 1996-03-10                    # 跑指定输入（按 input 字段匹配）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# 允许同目录下导入 bazi 模块
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bazi import (  # noqa: E402
    build_bazi_from_str,
    liunian, liumonth, liushi,
    liunian_text, liumonth_text, liushi_text,
)


HERE = Path(__file__).resolve().parent
TEST_CASES = HERE / "test_cases.json"


# ============================================================================
# 流年 / 流月 / 流时 子命令
# ============================================================================

def cmd_liunian(args, birth) -> int:
    """流年柱输出."""
    info = liunian(birth, args.liunian)
    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print(liunian_text(birth, args.liunian))
    return 0


def cmd_liumonth(args, birth) -> int:
    """流月柱输出."""
    y, m = args.liumonth.split("-")
    info = liumonth(birth, int(y), int(m))
    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print(liumonth_text(birth, int(y), int(m)))
    return 0


def cmd_liushi(args, birth) -> int:
    """流时柱输出."""
    target_dt = _parse_liushi_target(args.liushi)
    if target_dt is None:
        print(f"ERROR: 无法解析 --liushi 参数: {' '.join(args.liushi)}", file=sys.stderr)
        return 2
    info = liushi(birth, target_dt)
    if args.json:
        # target_dt 不能直接 JSON 化，转字符串
        out = dict(info)
        out["target_dt"] = info["target_dt"]
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(liushi_text(birth, target_dt))
    return 0


def _parse_liushi_target(args_value):
    """解析 --liushi YYYY-MM-DD [HH:MM]."""
    if isinstance(args_value, str):
        parts = args_value.split()
    elif isinstance(args_value, list):
        parts = list(args_value)
    else:
        return None
    if not parts:
        return None
    date_part = parts[0]
    time_part = parts[1] if len(parts) > 1 else "12:00"
    try:
        return datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
    except ValueError:
        return None


# ============================================================================
# 单张排盘 + 通用 dispatch
# ============================================================================

def cmd_chart(args, birth) -> int:
    """输出单张排盘（命主盘）."""
    if args.json:
        print(json.dumps(_bazi_to_dict(birth), ensure_ascii=False, indent=2))
    else:
        print(birth.pretty())
    return 0


# ============================================================================
# 自测
# ============================================================================

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
            print(f"ERROR: 用例 '{filter_input}' 未在 test_cases.json 中", file=sys.stderr)
            return 1

    fail = 0
    for c in cases:
        ok, diff = _check_case(c)
        mark = "✓" if ok else "✗"
        ctype = c.get("case_type", "chart")
        desc = c.get("description", "")
        if ctype != "chart":
            label = c.get("input", "") + " " + ctype
            print(f"{mark} {label:50s} {desc}")
        else:
            print(f"{mark} {c['input']:30s} {desc}")
        if not ok and diff:
            print(f"   diff: {diff}")
            fail += 1

    total = len(cases)
    passed = total - fail
    print()
    print(f"通过 {passed}/{total}")
    return 0 if fail == 0 else 1


def _check_case(case: dict) -> tuple[bool, str]:
    """比较实际输出与 expected 字段（dispatch by case_type）."""
    ctype = case.get("case_type", "chart")
    if ctype == "liunian":
        return _check_liunian_case(case)
    elif ctype == "liumonth":
        return _check_liumonth_case(case)
    elif ctype == "liushi":
        return _check_liushi_case(case)
    elif ctype == "combined":
        return _check_combined_case(case)
    else:
        return _check_chart_case(case)


def _check_chart_case(case: dict) -> tuple[bool, str]:
    """基础排盘用例."""
    inp = case["input"]
    date_part, _, time_part = inp.partition(" ")
    if not time_part:
        time_part = "12:00"
    bz = build_bazi_from_str(date_part, time_part)
    actual = _bazi_to_dict(bz)
    expected = case.get("expected", {})

    mismatches = []
    for pillar_name in ("year", "month", "day", "hour"):
        exp_p = expected.get(pillar_name, {})
        act_p = actual.get(pillar_name, {})
        for key in ("gan", "zhi", "gan_shishen", "zhi_shishen"):
            ev = exp_p.get(key)
            av = act_p.get(key)
            if ev is not None and ev != av:
                mismatches.append(
                    f"{pillar_name}.{key}: expected={ev!r} actual={av!r}"
                )
    if expected.get("day_master") and expected["day_master"] != actual["day_master"]:
        mismatches.append(
            f"day_master: expected={expected['day_master']!r} actual={actual['day_master']!r}"
        )

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_liunian_case(case: dict) -> tuple[bool, str]:
    """流年用例."""
    birth = _birth_from_case_input(case)
    actual = liunian(birth, case["year"])
    expected = case.get("expected", {})
    mismatches = []

    # target_year_pillar
    e_pillar = expected.get("target_year_pillar", {})
    a_pillar = actual.get("target_year_pillar", {})
    for key in ("gan", "zhi"):
        ev = e_pillar.get(key)
        av = a_pillar.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"target_year_pillar.{key}: exp={ev!r} act={av!r}")

    # vs_day_master
    e_dm = expected.get("vs_day_master", {})
    a_dm = actual.get("vs_day_master", {})
    for key in ("gan_shishen", "zhi_shishen"):
        ev = e_dm.get(key)
        av = a_dm.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"vs_day_master.{key}: exp={ev!r} act={av!r}")

    # vs_birth_year
    e_rel = expected.get("vs_birth_year", {})
    a_rel = actual.get("vs_birth_year", {})
    for key in ("gan_rels", "zhi_rels", "combined"):
        ev = e_rel.get(key)
        av = a_rel.get(key)
        if ev is not None:
            if isinstance(ev, list):
                for item in ev:
                    if item not in av:
                        mismatches.append(f"vs_birth_year.{key}: 期望列表含 {item!r} 实际={av}")
            else:
                if ev != av:
                    mismatches.append(f"vs_birth_year.{key}: exp={ev!r} act={av!r}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_liumonth_case(case: dict) -> tuple[bool, str]:
    """流月用例."""
    birth = _birth_from_case_input(case)
    actual = liumonth(birth, case["year"], case["month"])
    expected = case.get("expected", {})
    mismatches = []

    e_pillar = expected.get("target_month_pillar", {})
    a_pillar = actual.get("target_month_pillar", {})
    for key in ("gan", "zhi"):
        ev = e_pillar.get(key)
        av = a_pillar.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"target_month_pillar.{key}: exp={ev!r} act={av!r}")

    e_dm = expected.get("vs_day_master", {})
    a_dm = actual.get("vs_day_master", {})
    for key in ("gan_shishen", "zhi_shishen"):
        ev = e_dm.get(key)
        av = a_dm.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"vs_day_master.{key}: exp={ev!r} act={av!r}")

    e_rel = expected.get("vs_birth_month", {})
    a_rel = actual.get("vs_birth_month", {})
    for key in ("gan_rels", "zhi_rels", "combined"):
        ev = e_rel.get(key)
        av = a_rel.get(key)
        if ev is not None:
            if isinstance(ev, list):
                for item in ev:
                    if item not in av:
                        mismatches.append(f"vs_birth_month.{key}: 期望列表含 {item!r} 实际={av}")
            else:
                if ev != av:
                    mismatches.append(f"vs_birth_month.{key}: exp={ev!r} act={av!r}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_liushi_case(case: dict) -> tuple[bool, str]:
    """流时用例."""
    birth = _birth_from_case_input(case)
    target_dt = datetime.strptime(case["target_dt"], "%Y-%m-%d %H:%M")
    actual = liushi(birth, target_dt)
    expected = case.get("expected", {})
    mismatches = []

    e_pillar = expected.get("target_hour_pillar", {})
    a_pillar = actual.get("target_hour_pillar", {})
    for key in ("gan", "zhi"):
        ev = e_pillar.get(key)
        av = a_pillar.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"target_hour_pillar.{key}: exp={ev!r} act={av!r}")

    e_dm = expected.get("vs_day_master", {})
    a_dm = actual.get("vs_day_master", {})
    for key in ("gan_shishen", "zhi_shishen"):
        ev = e_dm.get(key)
        av = a_dm.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"vs_day_master.{key}: exp={ev!r} act={av!r}")

    e_rel = expected.get("vs_birth_hour", {})
    a_rel = actual.get("vs_birth_hour", {})
    for key in ("gan_rels", "zhi_rels", "combined"):
        ev = e_rel.get(key)
        av = a_rel.get(key)
        if ev is not None:
            if isinstance(ev, list):
                for item in ev:
                    if item not in av:
                        mismatches.append(f"vs_birth_hour.{key}: 期望列表含 {item!r} 实际={av}")
            else:
                if ev != av:
                    mismatches.append(f"vs_birth_hour.{key}: exp={ev!r} act={av!r}")

    # 可选检查：日柱是否随子时换日而变化
    if expected.get("target_day_pillar"):
        e_day = expected["target_day_pillar"]
        a_day = actual.get("target_day_pillar", {})
        for key in ("gan", "zhi"):
            ev = e_day.get(key)
            av = a_day.get(key)
            if ev is not None and ev != av:
                mismatches.append(f"target_day_pillar.{key}: exp={ev!r} act={av!r}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_combined_case(case: dict) -> tuple[bool, str]:
    """一次性含流年+流月+流时的组合用例."""
    birth = _birth_from_case_input(case)

    # 流年
    ok_ln, diff_ln = _check_liunian_case_inplace(birth, case)
    # 流月
    ok_lm, diff_lm = _check_liumonth_case_inplace(birth, case)
    # 流时
    ok_ls, diff_ls = _check_liushi_case_inplace(birth, case)

    diffs = []
    if not ok_ln: diffs.append(f"[流年] {diff_ln}")
    if not ok_lm: diffs.append(f"[流月] {diff_lm}")
    if not ok_ls: diffs.append(f"[流时] {diff_ls}")
    return (len(diffs) == 0), "; ".join(diffs)


def _check_liunian_case_inplace(birth, case: dict) -> tuple[bool, str]:
    expected = case.get("liunian_expected", {})
    if not expected:
        return True, ""
    actual = liunian(birth, case["year"])
    mismatches = []
    e_pillar = expected.get("target_year_pillar", {})
    a_pillar = actual.get("target_year_pillar", {})
    for key in ("gan", "zhi"):
        ev = e_pillar.get(key)
        av = a_pillar.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"target_year_pillar.{key}: exp={ev!r} act={av!r}")
    e_dm = expected.get("vs_day_master", {})
    a_dm = actual.get("vs_day_master", {})
    for key in ("gan_shishen", "zhi_shishen"):
        ev = e_dm.get(key)
        av = a_dm.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"vs_day_master.{key}: exp={ev!r} act={av!r}")
    e_rel = expected.get("vs_birth_year", {})
    a_rel = actual.get("vs_birth_year", {})
    for key in ("gan_rels", "zhi_rels", "combined"):
        ev = e_rel.get(key)
        av = a_rel.get(key)
        if ev is not None:
            if isinstance(ev, list):
                for item in ev:
                    if item not in av:
                        mismatches.append(f"vs_birth_year.{key}: 期望列表含 {item!r} 实际={av}")
            else:
                if ev != av:
                    mismatches.append(f"vs_birth_year.{key}: exp={ev!r} act={av!r}")
    return (len(mismatches) == 0), "; ".join(mismatches)


def _check_liumonth_case_inplace(birth, case: dict) -> tuple[bool, str]:
    expected = case.get("liumonth_expected", {})
    if not expected:
        return True, ""
    actual = liumonth(birth, case["year"], case["month"])
    mismatches = []
    e_pillar = expected.get("target_month_pillar", {})
    a_pillar = actual.get("target_month_pillar", {})
    for key in ("gan", "zhi"):
        ev = e_pillar.get(key)
        av = a_pillar.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"target_month_pillar.{key}: exp={ev!r} act={av!r}")
    e_dm = expected.get("vs_day_master", {})
    a_dm = actual.get("vs_day_master", {})
    for key in ("gan_shishen", "zhi_shishen"):
        ev = e_dm.get(key)
        av = a_dm.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"vs_day_master.{key}: exp={ev!r} act={av!r}")
    e_rel = expected.get("vs_birth_month", {})
    a_rel = actual.get("vs_birth_month", {})
    for key in ("gan_rels", "zhi_rels", "combined"):
        ev = e_rel.get(key)
        av = a_rel.get(key)
        if ev is not None:
            if isinstance(ev, list):
                for item in ev:
                    if item not in av:
                        mismatches.append(f"vs_birth_month.{key}: 期望列表含 {item!r} 实际={av}")
            else:
                if ev != av:
                    mismatches.append(f"vs_birth_month.{key}: exp={ev!r} act={av!r}")
    return (len(mismatches) == 0), "; ".join(mismatches)


def _check_liushi_case_inplace(birth, case: dict) -> tuple[bool, str]:
    expected = case.get("liushi_expected", {})
    if not expected:
        return True, ""
    target_dt = datetime.strptime(case["target_dt"], "%Y-%m-%d %H:%M")
    actual = liushi(birth, target_dt)
    mismatches = []
    e_pillar = expected.get("target_hour_pillar", {})
    a_pillar = actual.get("target_hour_pillar", {})
    for key in ("gan", "zhi"):
        ev = e_pillar.get(key)
        av = a_pillar.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"target_hour_pillar.{key}: exp={ev!r} act={av!r}")
    e_dm = expected.get("vs_day_master", {})
    a_dm = actual.get("vs_day_master", {})
    for key in ("gan_shishen", "zhi_shishen"):
        ev = e_dm.get(key)
        av = a_dm.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"vs_day_master.{key}: exp={ev!r} act={av!r}")
    e_rel = expected.get("vs_birth_hour", {})
    a_rel = actual.get("vs_birth_hour", {})
    for key in ("gan_rels", "zhi_rels", "combined"):
        ev = e_rel.get(key)
        av = a_rel.get(key)
        if ev is not None:
            if isinstance(ev, list):
                for item in ev:
                    if item not in av:
                        mismatches.append(f"vs_birth_hour.{key}: 期望列表含 {item!r} 实际={av}")
            else:
                if ev != av:
                    mismatches.append(f"vs_birth_hour.{key}: exp={ev!r} act={av!r}")
    return (len(mismatches) == 0), "; ".join(mismatches)


def _birth_from_case_input(case: dict) -> "Bazi":  # noqa: F821
    """从 case 的 input 字段恢复 birth Bazi."""
    inp = case.get("input", "")
    # input 格式: "YYYY-MM-DD HH:MM" 或 "YYYY-MM-DD"
    if " " in inp:
        date_part, time_part = inp.split(" ", 1)
    else:
        date_part, time_part = inp, "12:00"
    return build_bazi_from_str(date_part, time_part)


# ============================================================================
# 工具
# ============================================================================

def _bazi_to_dict(bz) -> dict:
    """Bazi → JSON-friendly dict."""
    out = {"day_master": bz.day_master, "solar": bz.solar.strftime("%Y-%m-%d %H:%M")}
    for name, p in zip(("year", "month", "day", "hour"), bz.four_pillars()):
        out[name] = {
            "gan": p.gan,
            "zhi": p.zhi,
            "gan_wuxing": p.gan_wuxing,
            "zhi_wuxing": p.zhi_wuxing,
            "gan_shishen": p.gan_shishen,
            "zhi_shishen": p.zhi_shishen,
            "canggan": p.canggan,
        }
    return out


def _validate_date(date_str: str) -> bool:
    """YYYY-MM-DD 校验."""
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_str))


# ============================================================================
# 主入口
# ============================================================================

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="bazi",
        description="八字排盘 / Four Pillars of Destiny（含流年/流月/流时扩展）",
    )
    # 主命令
    parser.add_argument("date", nargs="?", help="公历日期 YYYY-MM-DD")
    parser.add_argument("time", nargs="?", help="公历时间 HH:MM (默认 12:00)")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出排盘")
    parser.add_argument("--self-test", nargs="?", const="__ALL__", default=None,
                        help="跑 test_cases.json（可选指定 input 字段过滤）")

    # 流年 / 流月 / 流时 flag
    parser.add_argument("--liunian", type=int, metavar="YEAR",
                        help="推算 YEAR 年的流年柱（与命局关系）")
    parser.add_argument("--liumonth", type=str, metavar="YYYY-MM",
                        help="推算 YYYY-MM 月的流月柱（与命局关系）")
    parser.add_argument("--liushi", nargs="+", metavar="YYYY-MM-DD",
                        help="推算指定日期[时间]的流时柱（与命局关系）")

    args = parser.parse_args(argv)

    if args.self_test:
        return cmd_self_test(args)
    if not args.date:
        parser.print_help()
        return 1
    if not _validate_date(args.date):
        print(f"ERROR: 日期格式错误，期望 YYYY-MM-DD: {args.date}", file=sys.stderr)
        return 2
    time_str = args.time or "12:00"
    try:
        datetime.strptime(f"{args.date} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        print(f"ERROR: 时间格式错误，期望 HH:MM: {time_str}", file=sys.stderr)
        return 2

    # 构造命主盘
    birth = build_bazi_from_str(args.date, time_str)

    # 互斥/可组合：流年 + 流月 + 流时，按顺序输出
    rc = 0
    has_any = False

    if args.liunian is not None:
        has_any = True
        rc |= cmd_liunian(args, birth)
    if args.liumonth is not None:
        has_any = True
        rc |= cmd_liumonth(args, birth)
    if args.liushi is not None:
        has_any = True
        rc |= cmd_liushi(args, birth)

    if not has_any:
        return cmd_chart(args, birth)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
