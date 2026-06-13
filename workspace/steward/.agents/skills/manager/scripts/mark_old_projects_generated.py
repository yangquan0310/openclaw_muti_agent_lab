#!/usr/bin/env python3
"""
为老项目 AGENTS.md 添加 GENERATED_START/END 标记（v1.6.0）

背景：
- 2026-06-13 老板拍板：HANDBOOK.md → AGENTS.md 改名（16 个老项目）
- 老板"同意"批量为老项目加 GENERATED 标记，让它们能"接收"模板后续更新
- 标记后，manager sync 会走"安全合并"路径（用模板替换 GENERATED 区间）

注意：
- 本脚本**只加标记**，不替换内容
- 实际升级需要老板显式跑 `manager sync <项目>` 才触发
- 加标记后，老项目 AGENTS.md 仍然保留原内容（被 GENERATED 区间包住）
- 但下次 sync 会用模板 5 节结构**替换** GENERATED 区间 = 老项目升级

用法：
  python3 mark_old_projects_generated.py [--projects-dir /data/disk/OneDrive/Applications/openclaw repository] [--dry-run]
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 标记常量（与 BaseMaintainer.py 一致）
GENERATED_START = "<!-- GENERATED_START -->"
GENERATED_END = "<!-- GENERATED_END -->"
PROTECTED_FILES_MSG = "<!-- ⚠️ 保护：本段已加 GENERATED 标记，sync 时由 manager 技能模板替换 -->\n"


def add_generated_markers(filepath, dry_run=False):
    """
    为单个项目的 AGENTS.md 加 GENERATED_START/END 标记（包住现有内容）

    策略：
    - 已有标记 → 跳过
    - 无标记 → 在头部加 GENERATED_START，尾部加 GENERATED_END
    - 保留所有原内容（标记之间的"项目定制"内容）
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 已标记 → 跳过
    if GENERATED_START in content and GENERATED_END in content:
        return 'already_marked', '已有 GENERATED 标记，跳过'

    # 检查是否只有部分标记（异常情况）
    if GENERATED_START in content or GENERATED_END in content:
        return 'partial_markers', '⚠️ 检测到部分标记（GENERATED_START/END 不完整），请手动检查'

    # 无标记 → 加 GENERATED_START/END 包住现有内容
    # 头部加注释 + GENERATED_START
    header = f"{PROTECTED_FILES_MSG}{GENERATED_START}\n"
    # 尾部加 GENERATED_END
    footer = f"\n{GENERATED_END}"

    new_content = header + content + footer

    if dry_run:
        return 'dry_run', f'[预览] 将加标记 ({len(content)} → {len(new_content)} 字节)'

    # 写文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return 'marked', f'已加标记 ({len(content)} → {len(new_content)} 字节)'


def process_projects(projects_dir, dry_run=False):
    """
    遍历项目目录，为所有含 AGENTS.md 的项目加 GENERATED 标记
    """
    if not os.path.exists(projects_dir):
        print(f"❌ 项目根目录不存在: {projects_dir}")
        sys.exit(1)

    print(f"{'[预览] ' if dry_run else ''}扫描项目根: {projects_dir}\n")

    results = {
        'marked': 0,
        'already_marked': 0,
        'partial_markers': 0,
        'dry_run': 0,
        'skipped': 0,
    }

    for project_name in sorted(os.listdir(projects_dir)):
        project_path = os.path.join(projects_dir, project_name)
        # 跳过非目录和隐藏目录
        if not os.path.isdir(project_path) or project_name.startswith('.'):
            continue

        agents_path = os.path.join(project_path, 'AGENTS.md')
        if not os.path.exists(agents_path):
            # 没有 AGENTS.md 的项目（如 docs/、openclaw-bot-review/）跳过
            results['skipped'] += 1
            continue

        status, msg = add_generated_markers(agents_path, dry_run=dry_run)
        results[status] = results.get(status, 0) + 1

        icon = {
            'marked': '✅',
            'already_marked': '⏭️',
            'partial_markers': '⚠️',
            'dry_run': '🔍',
        }.get(status, '❓')
        print(f"  {icon} {project_name}: {msg}")

    # 汇总
    print(f"\n{'[预览] ' if dry_run else ''}汇总:")
    for k, v in results.items():
        print(f"  {k}: {v}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="为老项目 AGENTS.md 加 GENERATED 标记（v1.6.0）"
    )
    parser.add_argument(
        '--projects-dir',
        default='/data/disk/OneDrive/Applications/openclaw repository',
        help='项目根目录（默认: /data/disk/OneDrive/Applications/openclaw repository）'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式，不实际写文件'
    )
    args = parser.parse_args()

    print(f"=== 为老项目 AGENTS.md 加 GENERATED 标记 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"模式: {'DRY-RUN（仅预览）' if args.dry_run else '实际写入'}")
    print()

    process_projects(args.projects_dir, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
