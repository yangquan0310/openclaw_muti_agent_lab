"""Downloader.py - 文献下载器基类（多态接口）

设计原则：
- 单一职责：找论文 → 下载 PDF → 归档到 wiki 三步独立
- 多态：每个 Downloader 子类可自由实现三个方法
- 默认流水线：run(identifier) = find → download → archive
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from .paper_metadata import PaperMetadata


class Downloader(ABC):
    """文献下载器基类（抽象）"""

    @abstractmethod
    def find_paper(self, identifier: str) -> PaperMetadata:
        """根据 identifier (DOI / Zotero item key / arxiv id) 找到论文元数据

        Args:
            identifier: 标识符（DOI 以 '10.' 开头；Zotero item key 为 8 字符 alnum）

        Returns:
            PaperMetadata（含 zotero_attachment_key, md5 等下载所需的字段）

        Raises:
            ValueError: identifier 格式无法识别
            RuntimeError: 找不到对应论文
        """
        raise NotImplementedError

    @abstractmethod
    def download_pdf(self, meta: PaperMetadata, dest_dir: Path) -> Path:
        """下载 PDF 到 dest_dir

        Args:
            meta: 论文元数据（应含 md5 或 source_url）
            dest_dir: 临时下载目录

        Returns:
            最终 PDF 文件路径
        """
        raise NotImplementedError

    @abstractmethod
    def archive_to_wiki(
        self, pdf: Path, meta: PaperMetadata, wiki_raw_dir: Path
    ) -> Path:
        """按命名约定归档到 wiki raw 目录

        Args:
            pdf: 临时 PDF 路径
            meta: 论文元数据
            wiki_raw_dir: wiki raw 目录（默认 raw/papers/）

        Returns:
            归档后的最终路径
        """
        raise NotImplementedError

    def run(
        self,
        identifier: str,
        dest_dir: Optional[Path] = None,
        wiki_raw_dir: Optional[Path] = None,
    ) -> Path:
        """完整流水线：find_paper → download_pdf → archive_to_wiki

        Idempotency：先预检目标文件是否已存在，存在则直接返回（避免重复下载节流 WebDAV）。

        Args:
            identifier: 标识符
            dest_dir: 临时下载目录（默认 /tmp/zotero_dl）
            wiki_raw_dir: wiki raw 目录（覆盖构造时设置）

        Returns:
            归档后的最终路径
        """
        target_dir = Path(wiki_raw_dir) if wiki_raw_dir else getattr(
            self, "wiki_raw_dir", None
        )
        target_dir_path = Path(target_dir) if target_dir else None

        # 先拿元数据（轻量）
        meta = self.find_paper(identifier)

        # Idempotency 预检：目标文件已存在则直接返回
        if target_dir_path is not None:
            target_path = target_dir_path / meta.archive_filename()
            if target_path.exists():
                return target_path

        # 实际下载 + 归档
        dest = dest_dir or Path("/tmp/zotero_dl")
        pdf = self.download_pdf(meta, dest)
        if target_dir_path is None:
            return pdf
        return self.archive_to_wiki(pdf, meta, target_dir_path)
