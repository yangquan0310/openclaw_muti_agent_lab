#!/usr/bin/env python3
"""
自检脚本 - 检查技能目录结构和命名规范
"""

import sys
import json
import re
from pathlib import Path


def check_structure(skill_path):
    """检查技能目录结构"""
    skill_path = Path(skill_path)
    results = {"pass": [], "fail": [], "warnings": []}

    required_files = ["SKILL.md", "README.md", "_meta.json"]
    for f in required_files:
        if (skill_path / f).exists():
            results["pass"].append(f"✅ 必选文件存在: {f}")
        else:
            results["fail"].append(f"❌ 必选文件缺失: {f}")

    for d in ["scripts", "references", "assets"]:
        if (skill_path / d).exists():
            results["pass"].append(f"✅ 目录存在: {d}/")
        else:
            results["warnings"].append(f"⚠️ 目录缺失: {d}/")

    return results


def check_naming(skill_path):
    """检查命名规范"""
    skill_path = Path(skill_path)
    results = {"pass": [], "fail": [], "warnings": []}

    for f in skill_path.rglob("*.py"):
        content = f.read_text()
        for match in re.finditer(r"class (\w+)", content):
            cls_name = match.group(1)
            if cls_name.islower() or "_" in cls_name:
                results["fail"].append(f"❌ 类名不符合规范: {cls_name} (in {f.relative_to(skill_path)})")
            else:
                results["pass"].append(f"✅ 类名规范: {cls_name}")

    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        lines = skill_md.read_text().split("\n")
        if len(lines) > 200:
            results["warnings"].append(f"⚠️ SKILL.md 超过200行（当前{len(lines)}行），建议精简")
        else:
            results["pass"].append(f"✅ SKILL.md 行数合理（{len(lines)}行）")

    return results


def check_meta(skill_path):
    """检查 _meta.json 格式"""
    skill_path = Path(skill_path)
    results = {"pass": [], "fail": [], "warnings": []}

    meta_file = skill_path / "_meta.json"
    if not meta_file.exists():
        results["fail"].append("❌ _meta.json 不存在")
        return results

    try:
        meta = json.loads(meta_file.read_text())
        required_keys = ["name", "version", "description", "entry_point"]
        for key in required_keys:
            if key in meta:
                results["pass"].append(f"✅ meta字段: {key}")
            else:
                results["fail"].append(f"❌ meta缺少必要字段: {key}")
    except json.JSONDecodeError as e:
        results["fail"].append(f"❌ _meta.json 格式错误: {e}")

    return results


def selfcheck(skill_path):
    """执行完整自检"""
    print(f"\n🔍 开始自检: {skill_path}\n")
    print("=" * 50)

    all_results = {}
    all_results["结构检查"] = check_structure(skill_path)
    all_results["命名检查"] = check_naming(skill_path)
    all_results["元数据检查"] = check_meta(skill_path)

    total_pass = sum(len(r["pass"]) for r in all_results.values())
    total_fail = sum(len(r["fail"]) for r in all_results.values())
    total_warn = sum(len(r["warnings"]) for r in all_results.values())

    for check_name, results in all_results.items():
        print(f"\n【{check_name}】")
        for msg in results["pass"]:
            print(f"  {msg}")
        for msg in results["fail"]:
            print(f"  {msg}")
        for msg in results["warnings"]:
            print(f"  {msg}")

    print("\n" + "=" * 50)
    print(f"📊 自检结果: ✅ {total_pass} | ❌ {total_fail} | ⚠️ {total_warn}")

    if total_fail > 0:
        print("\n🔴 自检未通过，请修复以上 ❌ 问题")
        return 1
    elif total_warn > 0:
        print("\n🟡 自检通过但有警告，建议检查 ⚠️ 项")
        return 0
    else:
        print("\n🟢 自检完全通过")
        return 0


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(selfcheck(path))
