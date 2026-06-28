"""base.py - Downloader 抽象基类

设计原则：
- 单一职责：找论文 → 下载 PDF → 归档三步独立
- 多态：每个 Downloader 子类可自由实现三个方法
- 默认流水线：run(identifier) = find + pull + save
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from scripts.download.paper import PaperMetadata


class Downloader(ABC):
    """文献下载器基类（抽象）"""

    @abstractmethod
    def find(self, identifier: str) -> PaperMetadata:
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
    def pull(self, meta: PaperMetadata, dest_dir: Path) -> Path:
        """下载 PDF 到 dest_dir

        Args:
            meta: 论文元数据（应含 md5 或 source_url）
            dest_dir: 临时下载目录

        Returns:
            最终 PDF 文件路径
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, pdf: Path, meta: PaperMetadata, dest_dir: Path) -> Path:
        """按命名约定归档到 dest_dir

        Args:
            pdf: 临时 PDF 路径
            meta: 论文元数据
            dest_dir: 归档目录

        Returns:
            归档后的最终路径
        """
        raise NotImplementedError

    def fetch(
        self,
        identifier: str,
        dest_dir: Path | None = None,
        archive_dir: Path | None = None,
    ) -> Path:
        """完整流水线：find + pull + save

        Idempotency：先预检目标文件是否已存在，存在则直接返回（避免重复下载节流 WebDAV）。

        Args:
            identifier: 标识符
            dest_dir: 临时下载目录（默认 /tmp/zotero_dl）
            archive_dir: 归档目录（覆盖构造时设置）

        Returns:
            归档后的最终路径
        """
        target_dir = Path(archive_dir) if archive_dir else getattr(self, "archive_dir", None)
        target_dir_path = Path(target_dir) if target_dir else None

        meta = self.find(identifier)

        if target_dir_path is not None:
            target_path = target_dir_path / meta.archive_filename()
            if target_path.exists():
                return target_path

        dest = dest_dir or Path("/tmp/zotero_dl")
        pdf = self.pull(meta, dest)
        if target_dir_path is None:
            return pdf
        return self.save(pdf, meta, target_dir_path)