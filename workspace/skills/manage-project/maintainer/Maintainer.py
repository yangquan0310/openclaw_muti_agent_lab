#!/usr/bin/env python3
"""
manage-project.py - 项目文件自动化整理工具

基于面向对象设计，支持命令行和Python导入调用。
"""

import os
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path


class Maintainer:
    """项目文件整理类，用于管理单个项目的文件整理和元数据维护。"""

    # 标准目录结构由 _build_standard_dirs() 根据 config.json 动态构建

    def __init__(self, project_path: str):
        """
        初始化项目对象。

        Args:
            project_path: 项目文件夹路径
        """
        self.project_path = Path(project_path).resolve()
        self.metadata_path = self.project_path / "元数据.json"
        self.metadata = self._load_metadata()
        # 加载存储配置
        self.storage_config = self._load_storage_config()
        self.standard_dirs = self._build_standard_dirs()

    def _load_metadata(self) -> dict:
        """加载现有元数据，如果不存在则返回空字典。"""
        if self.metadata_path.exists():
            try:
                with open(self.metadata_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  读取现有元数据失败: {e}")
        return {}

    def _save_metadata(self) -> bool:
        """保存元数据到文件。"""
        try:
            with open(self.metadata_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            os.chmod(self.metadata_path, 0o644)
            return True
        except Exception as e:
            print(f"❌ 保存元数据失败: {e}")
            return False

    def _load_storage_config(self) -> dict:
        """从 config.json 加载 storage 配置"""
        config_path = Path(__file__).parent.parent / "config.json"
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("storage", {})
            except Exception as e:
                print(f"⚠️  读取 config.json 失败: {e}")
        return {}

    def _build_standard_dirs(self) -> dict:
        """根据 storage 配置构建标准目录映射"""
        storage = self.storage_config
        kb_dir = storage.get("knowledge_base_dir", "知识库").rstrip("/")
        temp_dir = "临时数据"
        return {
            "文档": "文档",
            "手稿": "手稿",
            "知识库": kb_dir,
            "笔记": storage.get("notes_dir", f"{kb_dir}/笔记").rstrip("/"),
            "综述": storage.get("reviews_dir", f"{kb_dir}/综述").rstrip("/"),
            "临时数据": temp_dir,
            "草稿": f"{temp_dir}/草稿",
            "检索条件": storage.get("search_queries_dir", f"{temp_dir}/检索条件").rstrip("/"),
            "临时笔记": storage.get("extracted_notes_dir", f"{temp_dir}/笔记").rstrip("/"),
        }

    def ensure_directories(self) -> None:
        """确保标准目录结构存在。"""
        for dir_name, dir_path in self.standard_dirs.items():
            full_path = self.project_path / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"  创建目录: {dir_path}")

    def move_file(self, file_path: str, target_dir: str, **kwargs) -> bool:
        """
        移动文件到目标目录。

        Args:
            file_path: 源文件路径（相对项目根目录或绝对路径）
            target_dir: 目标目录（相对项目根目录）
            **kwargs: 额外参数
                - new_name: 新文件名（可选）
                - overwrite: 是否覆盖已存在文件（默认False）

        Returns:
            bool: 是否成功
        """
        src = Path(file_path) if Path(file_path).is_absolute() else self.project_path / file_path
        if not src.exists():
            print(f"❌ 文件不存在: {src}")
            return False

        dst_dir = self.project_path / target_dir
        dst_dir.mkdir(parents=True, exist_ok=True)

        new_name = kwargs.get("new_name", src.name)
        dst = dst_dir / new_name

        if dst.exists() and not kwargs.get("overwrite", False):
            print(f"⚠️  目标文件已存在，跳过: {dst}")
            return False

        try:
            shutil.move(str(src), str(dst))
            print(f"✅ 移动: {src.name} -> {target_dir}/{new_name}")
            return True
        except Exception as e:
            print(f"❌ 移动失败: {e}")
            return False

    def rename_folder(self, old_name: str, new_name: str, **kwargs) -> bool:
        """
        重命名文件夹。

        Args:
            old_name: 原文件夹名（相对项目根目录）
            new_name: 新文件夹名
            **kwargs: 额外参数
                - merge: 如果目标存在，是否合并（默认False）

        Returns:
            bool: 是否成功
        """
        src = self.project_path / old_name
        dst = self.project_path / new_name

        if not src.exists():
            print(f"❌ 文件夹不存在: {src}")
            return False

        if dst.exists():
            if kwargs.get("merge", False):
                # 合并：将源目录内容移动到目标目录
                for item in src.iterdir():
                    target = dst / item.name
                    if target.exists():
                        print(f"⚠️  跳过已存在项: {item.name}")
                        continue
                    shutil.move(str(item), str(target))
                src.rmdir()
                print(f"✅ 合并并重命名: {old_name} -> {new_name}")
                return True
            else:
                print(f"⚠️  目标文件夹已存在: {dst}")
                return False

        try:
            src.rename(dst)
            print(f"✅ 重命名: {old_name} -> {new_name}")
            return True
        except Exception as e:
            print(f"❌ 重命名失败: {e}")
            return False

    def get_documents(self) -> list:
        """获取项目文档列表（用户上传的文档）。"""
        documents = []
        doc_dir = self.project_path / "文档"

        if doc_dir.exists():
            for file_path in doc_dir.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in (".md", ".docx", ".pdf", ".txt"):
                    documents.append({
                        "title": file_path.stem,
                        "version": "v1",
                        "path": f"文档/{file_path.name}",
                        "type": "user_uploaded"
                    })

        return documents

    def get_manuscripts(self) -> list:
        """获取手稿列表（代理撰写的md文档）。"""
        manuscripts = []
        manuscript_dir = self.project_path / "手稿"

        if manuscript_dir.exists():
            for file_path in manuscript_dir.iterdir():
                if file_path.is_file() and file_path.suffix.lower() == ".md":
                    manuscripts.append({
                        "title": file_path.stem,
                        "path": f"手稿/{file_path.name}",
                        "type": "agent_written"
                    })

        return manuscripts

    def update_metadata(self, **kwargs) -> bool:
        """
        更新项目元数据。

        Args:
            **kwargs: 额外参数
                - description: 项目描述
                - tags: 标签列表
                - status: 项目状态

        Returns:
            bool: 是否成功
        """
        self.ensure_directories()

        current_time = datetime.now().isoformat()
        created_date = self.metadata.get("created_date", datetime.now().strftime("%Y-%m-%d"))

        # 构建 directories 结构
        directories = {}
        for key, dir_path in self.standard_dirs.items():
            full_path = self.project_path / dir_path
            if full_path.exists():
                directories[key] = f"{dir_path}/"

        # 获取文档列表（仅扫描文档目录，不移动）
        documents = self.get_documents()

        # 去重
        seen = {}
        unique_docs = []
        for doc in documents:
            key = f"{doc.get('title', '')}|{doc.get('path', '')}"
            if key not in seen:
                seen[key] = True
                unique_docs.append(doc)

        # 更新元数据
        self.metadata.update({
            "project_id": self.project_path.name,
            "title": self.metadata.get("title", self.project_path.name),
            "created_date": created_date,
            "status": kwargs.get("status", self.metadata.get("status", "active")),
            "version": self.metadata.get("version", "v1"),
            "description": kwargs.get("description", self.metadata.get("description", f"{self.project_path.name}项目")),
            "directories": directories,
            "documents": unique_docs,
            "tags": kwargs.get("tags", self.metadata.get("tags", [])),
        })

        # 保留已有的 cloud_doc_mappings、notes、knowledge_base
        if "cloud_doc_mappings" not in self.metadata:
            self.metadata["cloud_doc_mappings"] = {}
        if "notes" not in self.metadata:
            self.metadata["notes"] = {}
        if "knowledge_base" not in self.metadata:
            self.metadata["knowledge_base"] = {}

        return self._save_metadata()

    def organize(self, **kwargs) -> bool:
        """
        自动整理项目文件。

        整理规则：
        1. 把中间文件归档到临时数据/
        2. 综述输出在知识库/综述/
        3. 笔记输出在知识库/笔记/
        4. 把用户上传移动到文档/
        5. 把撰写的最新md文档移动到手稿/
        6. 把备份版本移动到临时数据/草稿/

        Args:
            **kwargs: 额外参数
                - dry_run: 是否只预览不执行（默认False）

        Returns:
            bool: 是否成功
        """
        dry_run = kwargs.get("dry_run", False)
        if dry_run:
            print("🔍 预览模式（不实际执行）")

        print(f"\n📁 整理项目: {self.project_path.name}")
        print("-" * 40)

        # 确保目录存在
        if not dry_run:
            self.ensure_directories()

        # 扫描项目根目录的文件（排除文档目录）
        for item in self.project_path.iterdir():
            if item.is_file():
                self._organize_file(item, dry_run)
            elif item.is_dir() and item.name != "文档":
                # 可以处理非文档目录内的文件
                pass

        # 更新元数据
        if not dry_run:
            self.update_metadata()

        print("-" * 40)
        return True

    def _organize_file(self, file_path: Path, dry_run: bool = False) -> None:
        """根据规则整理单个文件。"""
        name = file_path.name.lower()
        suffix = file_path.suffix.lower()
        sd = self.standard_dirs

        # 判断文件类型并移动
        target_dir = None

        if suffix in (".docx", ".pdf", ".txt"):
            # 用户上传文档 - 不自动移动，仅用户命令可加入/移出
            target_dir = None
        elif suffix == ".md":
            if "backup" in name or "_backup" in name or "备份" in name:
                # 备份版本
                target_dir = sd["草稿"]
            elif "综述" in name or "review" in name or "summary" in name:
                # 综述
                target_dir = sd["综述"]
            elif "笔记" in name or "note" in name:
                # 笔记 - NoteExtractor提取的笔记放到临时笔记目录
                if "extract" in name or "提取" in name:
                    target_dir = sd["临时笔记"]
                else:
                    target_dir = sd["笔记"]
            else:
                # 默认作为手稿
                target_dir = sd["手稿"]
        elif suffix == ".json":
            # 检索条件文件
            target_dir = sd["检索条件"]
        elif suffix in (".tmp", ".temp", ".log", ".bak"):
            # 中间文件
            target_dir = sd["临时数据"]

        if target_dir:
            if dry_run:
                print(f"  [预览] {file_path.name} -> {target_dir}/")
            else:
                self.move_file(str(file_path), target_dir)

    def __repr__(self) -> str:
        return f"Maintainer('{self.project_path.name}')"


def main():
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="项目文件自动化整理工具")
    parser.add_argument("project_path", nargs="?", help="项目文件夹路径")
    parser.add_argument("--all", action="store_true", help="整理所有项目")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际执行")
    # 尝试从 config.json 读取默认项目根目录
    config_path = Path(__file__).parent.parent / "config.json"
    default_projects_dir = "/root/实验室仓库/项目文件"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                default_projects_dir = config.get("storage", {}).get("root_path", default_projects_dir)
        except:
            pass

    parser.add_argument("--projects-dir", default=default_projects_dir, help="项目根目录")

    args = parser.parse_args()

    if args.all:
        # 整理所有项目
        projects_dir = Path(args.projects_dir)
        if not projects_dir.exists():
            print(f"❌ 项目根目录不存在: {projects_dir}")
            return

        projects = [d for d in projects_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        projects.sort()

        print(f"找到 {len(projects)} 个项目\n")

        for project_path in projects:
            maintainer = Maintainer(str(project_path))
            maintainer.organize(dry_run=args.dry_run)

        print("\n✅ 所有项目整理完成")

    elif args.project_path:
        # 整理单个项目
        maintainer = Maintainer(args.project_path)
        maintainer.organize(dry_run=args.dry_run)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
