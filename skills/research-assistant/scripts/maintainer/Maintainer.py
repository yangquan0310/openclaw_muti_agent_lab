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


class MetadataManager:
    """元数据管理器 - 只操作metadata.json中的知识库相关字段"""

    def __init__(self, project_path):
        self.project_path = os.path.expanduser(project_path)
        self.metadata_path = os.path.join(self.project_path, "metadata.json")
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 读取元数据失败: {e}")
        return {}

    def save(self):
        try:
            self.metadata["updated_at"] = datetime.now().isoformat()
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            os.chmod(self.metadata_path, 0o644)
            return True
        except Exception as e:
            print(f"❌ 保存元数据失败: {e}")
            return False

    def to_dict(self):
        return self.metadata

    def get(self, key, default=None):
        return self.metadata.get(key, default)

    def set_title(self, title):
        self.metadata["title"] = title
        return self

    def set_description(self, description):
        self.metadata["description"] = description
        return self

    def set_status(self, status):
        self.metadata["status"] = status
        return self

    def set_version(self, version):
        self.metadata["version"] = version
        return self

    def set_tags(self, tags):
        self.metadata["tags"] = tags
        return self

    def add_tag(self, tag):
        if "tags" not in self.metadata:
            self.metadata["tags"] = []
        if tag not in self.metadata["tags"]:
            self.metadata["tags"].append(tag)
        return self

    def remove_tag(self, tag):
        if "tags" in self.metadata and tag in self.metadata["tags"]:
            self.metadata["tags"].remove(tag)
        return self

    def set_documents(self, docs):
        self.metadata["documents"] = docs
        return self

    def add_document(self, title, path, version="v1", doc_type="user_uploaded"):
        if "documents" not in self.metadata:
            self.metadata["documents"] = []
        self.metadata["documents"].append({
            "title": title,
            "version": version,
            "path": path,
            "type": doc_type
        })
        return self

    def remove_document(self, title, path=None):
        if "documents" in self.metadata:
            self.metadata["documents"] = [
                d for d in self.metadata["documents"]
                if not (d.get("title") == title and (path is None or d.get("path") == path))
            ]
        return self

    def add_directory(self, key, path):
        if "directories" not in self.metadata:
            self.metadata["directories"] = {}
        self.metadata["directories"][key] = path
        return self

    def remove_directory(self, key):
        if "directories" in self.metadata and key in self.metadata["directories"]:
            del self.metadata["directories"][key]
        return self

    def set_markdown(self, filename, local_path, cloud=None):
        if "markdown" not in self.metadata:
            self.metadata["markdown"] = {}
        self.metadata["markdown"][filename] = {
            "local_path": local_path,
            "cloud": cloud or []
        }
        return self

    def remove_markdown(self, filename):
        if "markdown" in self.metadata and filename in self.metadata["markdown"]:
            del self.metadata["markdown"][filename]
        return self

    def set_note(self, filename, local_path, created_at=None, description=""):
        if "notes" not in self.metadata:
            self.metadata["notes"] = {}
        self.metadata["notes"][filename] = {
            "local_path": local_path,
            "created_at": created_at or datetime.now().strftime("%Y-%m-%d"),
            "description": description
        }
        return self

    def remove_note(self, filename):
        if "notes" in self.metadata and filename in self.metadata["notes"]:
            del self.metadata["notes"][filename]
        return self

    def set_knowledge_base(self, index_file, description):
        self.metadata["knowledge_base"] = {
            "index_file": index_file,
            "description": description,
            "updated_at": datetime.now().isoformat()
        }
        return self

    def update_knowledge_base_timestamp(self):
        """自动更新知识库时间戳"""
        if "knowledge_base" not in self.metadata:
            self.metadata["knowledge_base"] = {}
        self.metadata["knowledge_base"]["updated_at"] = datetime.now().isoformat()
        return self

    def set_field(self, key, value):
        self.metadata[key] = value
        return self

    def update(self, **kwargs):
        self.metadata.update(kwargs)
        return self

    def delete_field(self, key):
        if key in self.metadata:
            del self.metadata[key]
        return self


class VersionController:
    """版本控制器 - 对综述/研究现状进行版本快照"""

    def __init__(self, project_path):
        self.project_path = os.path.expanduser(project_path)
        self.drafts_dir = os.path.join(self.project_path, "temp", "draft")
        os.makedirs(self.drafts_dir, exist_ok=True)

    def _get_next_version(self, title):
        """获取下一个版本号"""
        version_dir = os.path.join(self.drafts_dir, title)
        if not os.path.exists(version_dir):
            return "v1"

        versions = []
        for f in os.listdir(version_dir):
            match = re.search(rf"{re.escape(title)}_(v?\d+)", f)
            if match:
                v = int(match.group(1).replace('v', ''))
                versions.append(v)

        if versions:
            return f"v{max(versions) + 1}"
        return "v1"

    def save_version(self, doc_path, title=None, version=None, dry_run=False):
        """
        保存综述/研究现状的版本快照
        旧版本归档到 temp/draft/{标题}/，knowledge/review/ 保留最新版本

        参数:
            doc_path: 源文件路径（相对项目根目录或绝对路径）
            title: 文档标题（默认从文件名提取）
            version: 版本号（默认自动递增）
            dry_run: 是否仅预览

        返回:
            快照后的相对路径，失败返回 None
        """
        # 解析源文件路径
        if os.path.isabs(doc_path):
            src_path = doc_path
        else:
            src_path = os.path.join(self.project_path, doc_path)

        if not os.path.exists(src_path):
            print(f"❌ 源文件不存在: {doc_path}")
            return None

        filename = os.path.basename(src_path)
        name, ext = os.path.splitext(filename)

        # 确定标题
        if title is None:
            title = re.sub(r'[_-]*(v\d+|version\d+|final|终稿|draft|草稿)', '', name, flags=re.IGNORECASE).strip('_-')

        # 确定版本号
        if version is None:
            version_match = re.search(r'[_-][vV](\d+)$', name)
            if version_match:
                version = f"v{version_match.group(1)}"
            else:
                version = self._get_next_version(title)

        # 构建目标路径: temp/draft/{标题}/{标题}_{version}.md
        version_dir = os.path.join(self.drafts_dir, title)
        target_name = f"{title}_{version}{ext}"
        target_path = os.path.join(version_dir, target_name)

        if dry_run:
            rel_path = os.path.relpath(target_path, self.project_path)
            print(f"  [预览] 版本快照: {filename} -> {rel_path}")
            return rel_path

        # 创建目录
        os.makedirs(version_dir, exist_ok=True)

        # 复制文件（保留原文档，创建快照副本）
        try:
            shutil.copy2(src_path, target_path)
            rel_path = os.path.relpath(target_path, self.project_path)
            print(f"  ✅ 版本快照: {filename} -> {rel_path}")
            return rel_path
        except Exception as e:
            print(f"  ❌ 快照失败: {e}")
            return None

    def list_versions(self, title):
        """列出指定文档的所有版本"""
        version_dir = os.path.join(self.drafts_dir, title)
        if not os.path.exists(version_dir):
            return []

        versions = []
        for f in sorted(os.listdir(version_dir)):
            match = re.search(rf"{re.escape(title)}_(v?\d+)", f)
            if match:
                versions.append({
                    "version": match.group(1),
                    "filename": f,
                    "path": os.path.join("temp/draft", title, f),
                    "updated_at": datetime.fromtimestamp(os.path.getmtime(os.path.join(version_dir, f))).isoformat()
                })
        return sorted(versions, key=lambda x: x["version"])

    def get_version(self, title, version):
        """获取指定版本的内容"""
        version_path = os.path.join(self.drafts_dir, title, f"{title}_{version}.md")
        if not os.path.exists(version_path):
            return None

        try:
            with open(version_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ 读取版本失败: {e}")
            return None


class Maintainer:
    """维护模块 - 元数据维护与版本控制协调器"""

    def __init__(self, project_path):
        self.project_path = os.path.expanduser(project_path)
        self.metadata_manager = MetadataManager(project_path)
        self.version_controller = VersionController(project_path)

    def update_kb_metadata(self):
        """
        更新知识库元数据时间戳
        由 search/summarize/manage/synthesize 模块在操作完成后调用
        """
        self.metadata_manager.update_knowledge_base_timestamp().save()
        print("  ✅ 已更新知识库元数据时间戳")
        return True

    def update_notes_metadata(self, note_filename, local_path, description=""):
        """
        更新笔记元数据
        由 manage.export_notes() 在导出笔记后调用
        """
        self.metadata_manager.set_note(note_filename, local_path, description=description).save()
        print(f"  ✅ 已更新笔记元数据: {note_filename}")
        return True

    def save_review_version(self, doc_path, title=None, version=None, dry_run=False):
        """
        保存综述/研究现状版本快照
        公共方法，供 synthesize 模块调用
        """
        return self.version_controller.save_version(doc_path, title, version, dry_run)

    def list_review_versions(self, title):
        """列出综述/研究现状的所有版本"""
        return self.version_controller.list_versions(title)

    def get_review_version(self, title, version):
        """获取指定版本的内容"""
        return self.version_controller.get_version(title, version)

    def get_metadata_manager(self):
        """获取元数据管理器实例"""
        return self.metadata_manager


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 scripts/maintainer/Maintainer.py <项目路径> [命令] [参数...]")
        print("")
        print("命令:")
        print("  update-kb              更新知识库时间戳")
        print("  update-notes <文件> <路径> [描述]  更新笔记元数据")
        print("  save-version <文件> [标题] [版本]  保存版本快照")
        print("  list-versions <标题>  列出所有版本")
        print("  get-version <标题> <版本>  获取版本内容")
        sys.exit(1)

    project_path = sys.argv[1]
    maintainer = Maintainer(project_path)

    if len(sys.argv) < 3:
        # 默认更新知识库时间戳
        maintainer.update_kb_metadata()
        sys.exit(0)

    command = sys.argv[2]

    if command == "update-kb":
        maintainer.update_kb_metadata()

    elif command == "update-notes":
        if len(sys.argv) < 5:
            print("用法: update-notes <文件名> <路径> [描述]")
            sys.exit(1)
        maintainer.update_notes_metadata(sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "")

    elif command == "save-version":
        if len(sys.argv) < 4:
            print("用法: save-version <文件路径> [标题] [版本]")
            sys.exit(1)
        title = sys.argv[4] if len(sys.argv) > 4 else None
        version = sys.argv[5] if len(sys.argv) > 5 else None
        result = maintainer.save_review_version(sys.argv[3], title=title, version=version)
        if result:
            print(f"✅ 版本快照: {result}")
        else:
            print("❌ 快照失败")

    elif command == "list-versions":
        if len(sys.argv) < 4:
            print("用法: list-versions <标题>")
            sys.exit(1)
        versions = maintainer.list_review_versions(sys.argv[3])
        print(json.dumps(versions, ensure_ascii=False, indent=2))

    elif command == "get-version":
        if len(sys.argv) < 5:
            print("用法: get-version <标题> <版本>")
            sys.exit(1)
        content = maintainer.get_review_version(sys.argv[3], sys.argv[4])
        if content:
            print(content)
        else:
            print("❌ 版本不存在")

    else:
        print(f"未知命令: {command}")
        sys.exit(1)
