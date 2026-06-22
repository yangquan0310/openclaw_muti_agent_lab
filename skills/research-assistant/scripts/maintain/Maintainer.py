#!/usr/bin/env python3
"""
Maintainer.py - 元数据维护与版本控制模块
负责：更新项目元数据、对综述/研究现状进行版本快照
"""

import os
import json
import shutil
import re
from datetime import datetime


# MetadataManager 已删除（v5.14.0，迁到 wiki）


# VersionController 已删除（v5.14.0，迁到 wiki 用 git）


class Maintainer:
    """维护模块协调器（v5.14.0 重构：移除 metadata.json / 旧版本控制）"""

    def __init__(self, project_path):
        self.project_path = os.path.expanduser(project_path)

    # 所有具体维护操作请参考 hooks/ 目录：
    # - add-zotero-source.md
    # - sync-zotero-new-items.md
    # - check-drift.md
    # - manual-add-item.md
    # - cleanup-wrong-entry.md
    # - wiki-source-missing-in-zotero.md
    # - zotero-patch-with-version.md
    # - arxiv-title-parse.md
    # - rclone-webdav-setup.md (新增)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 Maintainer.py <命令>")
        print("")
        print("v5.14.0 起：CLI 已简化，详细操作见 hooks/ 目录")
        print("  python3 scripts/maintain/Maintainer.py help")
        sys.exit(1)
    print("v5.14.0: 请使用 hooks/ 目录的 SOP 脚本或 zotero.py + rclone + edit 工具")
