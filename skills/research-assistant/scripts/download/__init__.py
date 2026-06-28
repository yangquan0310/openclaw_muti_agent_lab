"""download/ - 文献下载（多态流水线）

- Downloader: 抽象基类（统一接口 find + pull + save）
- ZoteroJianguoyunDownloader: 老板专属（论文先在 Zotero 库才能下）
- SciHubDownloader: SciHub 替代方案（绕过付费墙，论文无需先入 Zotero）
- PaperMetadata: 元数据 + 归档文件名生成

多态扩展点：未来可加 ArxivDirectDownloader / OpenAccessDownloader 等
（继承 Downloader + 实现 find/pull/save 三个 abstract 方法）
"""

from scripts.download.base import Downloader
from scripts.download.paper import PaperMetadata
from scripts.download.zotero_jianguoyun import ZoteroJianguoyunDownloader
from scripts.download.scihub import SciHubDownloader

__all__ = [
    "Downloader",
    "PaperMetadata",
    "ZoteroJianguoyunDownloader",
    "SciHubDownloader",
]