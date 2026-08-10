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
    zhengge, shiju, shensha, yongshen, dayun, reverse_lookup,
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
# v1.8.0 模块子命令
# ============================================================================

def cmd_zhengge(args, birth) -> int:
    """v1.8.0 正格判定."""
    result = zhengge(birth)
    if args.json:
        out = {
            "chart": _bazi_to_dict(birth),
            "analysis": {"zhengge": result},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print(f"【正格分析】{birth.solar.strftime('%Y-%m-%d %H:%M')}")
        print("=" * 50)
        print(f"格局：{result.get('ge_type') or '未成格（走势局）'}")
        print(f"来源：{result.get('ge_source','')}")
        print(f"用神方向：{result.get('yongshen_direction','')}（{result.get('yongshen_wuxing','')}）")
        print(f"相神：{result.get('xiangshen','')}")
        print(f"忌神：{result.get('jishen','')}")
        print(f"仇神：{result.get('choushen','')}")
        if result.get("po_ge"):
            print(f"破格：{result['po_ge']}")
        if result.get("jiu_ying"):
            print(f"救应：{result['jiu_ying']}")
    return 0


def cmd_shiju(args, birth) -> int:
    """v1.8.0 势局分析."""
    result = shiju(birth)
    if args.json:
        out = {
            "chart": _bazi_to_dict(birth),
            "analysis": {"shiju": result},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print(f"【势局分析】{birth.solar.strftime('%Y-%m-%d %H:%M')}")
        print("=" * 50)
        print(f"旺衰：{result.get('wangshuai','')}（{result.get('wangshuai_score',0)}/4）")
        print(f"  得令：{result.get('de_ling')}")
        print(f"  得地：{result.get('de_di')}")
        print(f"  得生：{result.get('de_sheng')}")
        print(f"  得助：{result.get('de_zhu')}")
        print(f"调候用神：{result.get('tiaohou','')}")
        print(f"流通分析：{result.get('liutong','')}")
        print(f"精化用神：{result.get('yongshen_jinhua','')}")
        if result.get("zhuan_ge"):
            print(f"特殊格局：{result['zhuan_ge']}")
    return 0


def cmd_shensha(args, birth) -> int:
    """v1.8.0 神煞清单."""
    result = shensha(birth)
    if args.json:
        out = {
            "chart": _bazi_to_dict(birth),
            "analysis": {"shensha": result, "count": len(result)},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print(f"【神煞清单】{birth.solar.strftime('%Y-%m-%d %H:%M')}（命中 {len(result)} 个）")
        print("=" * 50)
        for s in result:
            print(f"\n■ {s['name']}（{s['zhiwei']}）")
            print(f"  🟢 阳面：{s['yang']}")
            print(f"  🔴 阴面：{s['yin']}")
            print(f"  激活：{s['activation']}")
            print(f"  制化：{s['control']}")
    return 0


def cmd_yongshen(args, birth) -> int:
    """v1.8.0 用神融合."""
    result = yongshen(birth)
    if args.json:
        out = {
            "chart": _bazi_to_dict(birth),
            "analysis": {"yongshen": result},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print(f"【用神融合】{birth.solar.strftime('%Y-%m-%d %H:%M')}")
        print("=" * 50)
        print(f"最终用神：{result.get('final','')}")
        print(f"总结：{result.get('final_desc','')}")
        print(f"正格方向：{result.get('zhengge_direction','')}")
        print(f"势局精化：{result.get('shiju_jinhua','')}")
        print(f"调候：{result.get('tiaohou','')}")
        print(f"相神：{result.get('xiangshen','')}")
        print(f"忌神：{result.get('jishen','')}")
        print(f"仇神：{result.get('choushen','')}")
        print(f"\n融合来源：{result.get('fusion_source','')}")
    return 0


def cmd_dayun(args, birth) -> int:
    """v1.8.0 大运推算."""
    gender = getattr(args, "gender", "男") or "男"
    result = dayun(birth, gender=gender)
    if args.json:
        out = {
            "chart": _bazi_to_dict(birth),
            "gender": gender,
            "analysis": {"dayun": result},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print(f"【大运】{birth.solar.strftime('%Y-%m-%d %H:%M')}（{gender}命）")
        print("=" * 50)
        print(f"顺/逆排：{result.get('shunni','')}")
        print(f"起运岁数：{result.get('qi_yun_age','')} 岁")
        print(f"所对节：{result.get('qi_yun_jie','')}")
        print(f"计算说明：{result.get('qi_yun_note','')}")
        print(f"\n10 步大运：")
        for s in result.get("steps", []):
            print(
                f"  [{s['index']:2d}] {s['gan']}{s['zhi']} "
                f"({s['gan_shishen']}/{s['zhi_shishen']}) "
                f"岁数 {s['start_age']}-{s['end_age']}"
            )
    return 0


def cmd_reverse(args) -> int:
    """v1.8.0 八字反查."""
    year_gz = getattr(args, "year", None)
    month_gz = getattr(args, "month", None)
    day_gz = getattr(args, "day", None)
    hour_gz = getattr(args, "hour", None)

    if not all([year_gz, month_gz, day_gz, hour_gz]):
        print("ERROR: --reverse 需要 --year/--month/--day/--hour 四个参数", file=sys.stderr)
        return 2

    result = reverse_lookup(year_gz, month_gz, day_gz, hour_gz)
    if args.json:
        out = {
            "input": {"year": year_gz, "month": month_gz, "day": day_gz, "hour": hour_gz},
            "candidates": result,
            "count": len(result),
            "notes": "cnlunar 节气精度限制，反查为候选范围而非唯一日期（±1 天）",
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("=" * 50)
        print(f"【八字反查】{year_gz} {month_gz} {day_gz} {hour_gz}")
        print("=" * 50)
        print(f"候选数：{len(result)}")
        for c in result:
            if "error" in c:
                print(f"\nERROR: {c['error']}")
                continue
            print(
                f"\n#{c['candidate_rank']}  {c['solar']} "
                f"（{c['lunar']} · {c['shengxiao']}年）"
            )
            print(f"     四柱：年{c['year_pillar']} 月{c['month_pillar']} 日{c['day_pillar']} 时{c['hour_pillar']}")
            print(f"     节气匹配：{c.get('jieqi_match','')}")
            print(f"     cnlunar 精度：{c.get('cnlunar_precision','')}")
    return 0


def cmd_daliuren(args, birth) -> int:
    """v2.0.0 大六壬排盘（天地盘/四课/三传/九宗门）."""
    from bazi_daliuren import daliuren_text
    print(daliuren_text(birth.solar))
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
    elif ctype == "zhengge":
        return _check_zhengge_case(case)
    elif ctype == "shiju":
        return _check_shiju_case(case)
    elif ctype == "shensha":
        return _check_shensha_case(case)
    elif ctype == "yongshen":
        return _check_yongshen_case(case)
    elif ctype == "dayun":
        return _check_dayun_case(case)
    elif ctype == "reverse":
        return _check_reverse_case(case)
    elif ctype == "daliuren":
        return _check_daliuren_case(case)
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


# ============================================================================
# v1.8.0 用例检查函数
# ============================================================================

def _check_zhengge_case(case: dict) -> tuple[bool, str]:
    """v1.8.0 正格用例."""
    birth = _birth_from_case_input(case)
    actual = zhengge(birth)
    expected = case.get("expected", {})
    mismatches = []

    # 严格相等字段
    for key in ("ge_type", "yongshen_wuxing", "xiangshen", "jishen", "choushen", "tou_gan"):
        ev = expected.get(key)
        av = actual.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"{key}: exp={ev!r} act={av!r}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_shiju_case(case: dict) -> tuple[bool, str]:
    """v1.8.0 势局用例."""
    birth = _birth_from_case_input(case)
    actual = shiju(birth)
    expected = case.get("expected", {})
    mismatches = []

    # 严格相等字段
    for key in ("wangshuai_score", "de_ling", "de_di", "de_sheng", "de_zhu", "tiaohou"):
        ev = expected.get(key)
        av = actual.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"{key}: exp={ev!r} act={av!r}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_shensha_case(case: dict) -> tuple[bool, str]:
    """v1.8.0 神煞用例."""
    birth = _birth_from_case_input(case)
    actual = shensha(birth)
    expected = case.get("expected", {})
    mismatches = []

    # must_contain: 至少包含指定名称
    must_contain = expected.get("must_contain", [])
    actual_names = [s["name"] for s in actual]
    for name in must_contain:
        if name not in actual_names:
            mismatches.append(f"must_contain: {name!r} 未在 {actual_names} 中")

    # min_count: 至少多少个
    min_count = expected.get("min_count")
    if min_count is not None and len(actual) < min_count:
        mismatches.append(f"min_count: 实际 {len(actual)} < 期望 {min_count}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_yongshen_case(case: dict) -> tuple[bool, str]:
    """v1.8.0 用神融合用例."""
    birth = _birth_from_case_input(case)
    actual = yongshen(birth)
    expected = case.get("expected", {})
    mismatches = []

    # 严格相等字段
    for key in ("final", "tiaohou", "wangshuai_score"):
        ev = expected.get(key)
        av = actual.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"{key}: exp={ev!r} act={av!r}")

    # final_wuxing_contains: final 字符串中必须包含的五行
    final_wx = expected.get("final_wuxing_contains", [])
    actual_final = actual.get("final", "")
    for wx in final_wx:
        if wx not in actual_final:
            mismatches.append(f"final_wuxing_contains: {wx!r} 未在 final={actual_final!r} 中")

    # zg_direction_contains: 正格方向中必须包含
    zg_dir = actual.get("zhengge_direction", "")
    zg_contains = expected.get("zhengge_direction_contains")
    if zg_contains and zg_contains not in zg_dir:
        mismatches.append(f"zhengge_direction_contains: {zg_contains!r} 未在 {zg_dir!r} 中")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_dayun_case(case: dict) -> tuple[bool, str]:
    """v1.8.0 大运用例."""
    birth = _birth_from_case_input(case)
    gender = case.get("gender", "男")
    actual = dayun(birth, gender=gender)
    expected = case.get("expected", {})
    mismatches = []

    # 严格相等字段
    for key in ("shunni",):
        ev = expected.get(key)
        av = actual.get(key)
        if ev is not None and ev != av:
            mismatches.append(f"{key}: exp={ev!r} act={av!r}")

    # qi_yun_age_min / qi_yun_age_max: 起运岁数范围
    qi_min = expected.get("qi_yun_age_min")
    qi_max = expected.get("qi_yun_age_max")
    qi_act = actual.get("qi_yun_age", 0)
    if qi_min is not None and qi_act < qi_min:
        mismatches.append(f"qi_yun_age: 实际 {qi_act} < 期望最小 {qi_min}")
    if qi_max is not None and qi_act > qi_max:
        mismatches.append(f"qi_yun_age: 实际 {qi_act} > 期望最大 {qi_max}")

    # steps_count
    steps_count_exp = expected.get("steps_count")
    steps_count_act = len(actual.get("steps", []))
    if steps_count_exp is not None and steps_count_exp != steps_count_act:
        mismatches.append(f"steps_count: exp={steps_count_exp} act={steps_count_act}")

    # first_step_gan / first_step_zhi
    first_step = actual.get("steps", [{}])[0] if actual.get("steps") else {}
    for key in ("first_step_gan", "first_step_zhi"):
        ev = expected.get(key)
        av = first_step.get(key.replace("first_step_", ""))
        if ev is not None and ev != av:
            mismatches.append(f"{key}: exp={ev!r} act={av!r}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_reverse_case(case: dict) -> tuple[bool, str]:
    """v1.8.0 八字反查用例."""
    year_gz = case.get("year", "")
    month_gz = case.get("month", "")
    day_gz = case.get("day", "")
    hour_gz = case.get("hour", "")
    year_range = tuple(case.get("year_range", (1900, 2100)))

    actual = reverse_lookup(year_gz, month_gz, day_gz, hour_gz, year_range=year_range)
    expected = case.get("expected", {})
    mismatches = []

    # must_contain_solar: 必须包含的公历日期
    must_solar = expected.get("must_contain_solar")
    if must_solar:
        actual_solars = [c.get("solar", "") for c in actual]
        if must_solar not in actual_solars:
            mismatches.append(f"must_contain_solar: {must_solar!r} 未在 {actual_solars} 中")

    # min_candidates: 最少候选数
    min_c = expected.get("min_candidates")
    if min_c is not None and len(actual) < min_c:
        mismatches.append(f"min_candidates: 实际 {len(actual)} < 期望最小 {min_c}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


def _check_daliuren_case(case: dict) -> tuple[bool, str]:
    """v2.0.0 大六壬用例."""
    from datetime import datetime as _dt
    from bazi_daliuren import judge_daliuren
    inp = case.get("input", "")
    date_part, _, time_part = inp.partition(" ")
    if not time_part:
        time_part = "12:00"
    solar = _dt.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
    actual = judge_daliuren(solar)
    d = actual.to_dict()
    expected = case.get("expected", {})
    mismatches = []

    # yue_jiang
    if "yue_jiang" in expected and d["yue_jiang"] != expected["yue_jiang"]:
        mismatches.append(f"yue_jiang: exp={expected['yue_jiang']!r} act={d['yue_jiang']!r}")
    # hour_zhi
    if "hour_zhi" in expected and d["hour_zhi"] != expected["hour_zhi"]:
        mismatches.append(f"hour_zhi: exp={expected['hour_zhi']!r} act={d['hour_zhi']!r}")
    # month_zhi
    if "month_zhi" in expected and d["month_zhi"] != expected["month_zhi"]:
        mismatches.append(f"month_zhi: exp={expected['month_zhi']!r} act={d['month_zhi']!r}")
    # ke_1_down
    if "ke_1_down" in expected:
        ke1_down = d["si_ke"]["ke_1"][1]
        if ke1_down != expected["ke_1_down"]:
            mismatches.append(f"ke_1_down: exp={expected['ke_1_down']!r} act={ke1_down!r}")
    # chu_chuan
    if "chu_chuan" in expected and d["san_chuan"]["chu_chuan"] != expected["chu_chuan"]:
        mismatches.append(f"chu_chuan: exp={expected['chu_chuan']!r} act={d['san_chuan']['chu_chuan']!r}")
    # zongmen
    if "zongmen" in expected and d["san_chuan"]["zongmen"] != expected["zongmen"]:
        mismatches.append(f"zongmen: exp={expected['zongmen']!r} act={d['san_chuan']['zongmen']!r}")

    if mismatches:
        return False, "; ".join(mismatches)
    return True, ""


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
    out = {
        "day_master": bz.day_master,
        "solar": bz.solar.strftime("%Y-%m-%d %H:%M"),
        "shengxiao": bz.shengxiao,  # 修复：JSON 漏输出生肖字段
    }
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

    # v1.8.0 新增模块 flag
    parser.add_argument("--zhengge", action="store_true",
                        help="v1.8.0 正格判定（月令定格 + 透干 + 用神方向）")
    parser.add_argument("--shiju", action="store_true",
                        help="v1.8.0 势局分析（旺衰四维度 + 调候 + 流通）")
    parser.add_argument("--shensha", action="store_true",
                        help="v1.8.0 神煞清单（28 神煞 × 4 柱 = 一体两面）")
    parser.add_argument("--yongshen", action="store_true",
                        help="v1.8.0 用神融合（正格方向 ∩ 势局精化，神煞不进入）")
    parser.add_argument("--dayun", action="store_true",
                        help="v1.8.0 大运推算（顺/逆排 + 起运岁数 + 10 步）")
    parser.add_argument("--gender", type=str, choices=["男", "女"], default="男",
                        help="性别（与 --dayun 配合使用，默认男）")

    # v1.8.0 八字反查 flag
    parser.add_argument("--reverse", action="store_true",
                        help="v1.8.0 八字反查（4 柱 → 候选公历日期）")
    parser.add_argument("--year", type=str, metavar="干支",
                        help="反查年柱（甲子）")
    parser.add_argument("--month", type=str, metavar="干支",
                        help="反查月柱（甲子）")
    parser.add_argument("--day", type=str, metavar="干支",
                        help="反查日柱（甲子）")
    parser.add_argument("--hour", type=str, metavar="干支",
                        help="反查时柱（甲子）")

    # v2.0.0 大六壬 flag
    parser.add_argument("--daliuren", action="store_true",
                        help="v2.0.0 大六壬排盘（天地盘/四课/三传/九宗门）")

    args = parser.parse_args(argv)

    if args.self_test:
        return cmd_self_test(args)

    # 反查是独立命令（不需要 date 参数）
    if args.reverse:
        return cmd_reverse(args)

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

    # 互斥/可组合：流年 + 流月 + 流时 + v1.8.0 模块，按顺序输出
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
    if args.zhengge:
        has_any = True
        rc |= cmd_zhengge(args, birth)
    if args.shiju:
        has_any = True
        rc |= cmd_shiju(args, birth)
    if args.shensha:
        has_any = True
        rc |= cmd_shensha(args, birth)
    if args.yongshen:
        has_any = True
        rc |= cmd_yongshen(args, birth)
    if args.dayun:
        has_any = True
        rc |= cmd_dayun(args, birth)
    if getattr(args, "daliuren", False):
        has_any = True
        rc |= cmd_daliuren(args, birth)

    if not has_any:
        return cmd_chart(args, birth)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
