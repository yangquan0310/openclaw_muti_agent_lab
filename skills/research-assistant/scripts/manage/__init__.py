"""manage/ - wiki source 列表管理（CRUD）

只动 wiki 这一侧，不调 Zotero / WebDAV。
"""

from scripts.manage.manager import WikiSourceManager

__all__ = ["WikiSourceManager"]