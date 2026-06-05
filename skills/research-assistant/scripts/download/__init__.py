"""download module - 文献下载（多态流水线）

- Downloader: 抽象基类
- ZoteroJianguoyunDownloader: 老板专属（Zotero + 坚果云 WebDAV）
- PaperMetadata: 元数据 + 归档文件名生成

用法（Python API）：
    from scripts.download import ZoteroJianguoyunDownloader
    dl = ZoteroJianguoyunDownloader()  # 自动从 .env 读凭据
    path = dl.run("10.1177/0956797617694868")  # DOI 输入
    # 或 path = dl.run("R8MVF42R")  # Zotero item key

用法（CLI）：
    python3 main.py download --doi 10.1177/0956797617694868
    python3 main.py download --zotero-key R8MVF42R
"""

from .Downloader import Downloader
from .ZoteroJianguoyunDownloader import ZoteroJianguoyunDownloader
from .paper_metadata import PaperMetadata

__all__ = [
    "Downloader",
    "ZoteroJianguoyunDownloader",
    "PaperMetadata",
]
