"""upload/ - 本地 PDF → Zotero + WebDAV + wiki source

download 模块的反向对偶：
- download: 远端 Zotero / WebDAV → 本地 wiki raw
- upload:   本地 PDF → 远端 Zotero / WebDAV + wiki source

工具边界：只搬运数据，不攥写笔记 / 综述。
"""

from scripts.upload.uploader import Uploader

__all__ = ["Uploader"]