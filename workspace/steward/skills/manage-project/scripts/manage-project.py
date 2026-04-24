#!/usr/bin/env python3
"""
manage-project.py - 项目管理核心类
面向对象封装，支持命令行和Python导入调用
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# 默认项目根目录
DEFAULT_PROJECTS_DIR = "/root/实验室仓库/项目文件"

# 标准目录结构
STANDARD_DIRS = {
    "文档": "文档/",
    "手稿": "手稿/",
    "知识库": "知识库/",
    "知识库/笔记": "知识库/笔记/",
    "知识库/综述": "知识库/综述/",
    "临时数据": "临时数据/",
    "临时数据/草稿": "临时数据/草稿/",
}

# 文件类型映射
FILE_TYPE_PATTERNS = {
    "user_uploaded": [".docx", ".pdf", ".txt", ".doc", ".xlsx", ".pptx"],
    "agent_written": [".md"],
    "backup": [".bak", ".old", ".backup"],
    "intermediate": [".tmp", ".draft", ".intermediate"],
}


class Project:
    """项目管理类，封装所有项目操作"""

    def __init__(self, project_path, projects_dir=None):
        """
        初始化项目
        :param project_path: 项目路径（可以是绝对路径或相对于projects_dir的路径）
        :param projects_dir: 项目根目录，默认 DEFAULT_PROJECTS_DIR
        """
        self.projects_dir = projects_dir or DEFAULT_PROJECTS_DIR
        
        # 解析项目路径
        if os.path.isabs(project_path):
            self.project_path = project_path
        else:
            self.project_path = os.path.join(self.projects_dir, project_path)
        
        self.project_name = os.path.basename(os.path.normpath(self.project_path))
        self.metadata_path = os.path.join(self.project_path, "元数据.json")
        
        # 加载现有元数据
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        """加载现有元数据"""
        # 优先从根目录加载
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  读取现有元数据失败: {e}")
        # 兼容旧位置：临时数据/元数据.json
        old_metadata_path = os.path.join(self.project_path, "临时数据", "元数据.json")
        if os.path.exists(old_metadata_path):
            try:
                with open(old_metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  读取旧位置元数据失败: {e}")
        return {}

    def _save_metadata(self):
        """保存元数据到文件（始终保存到根目录）"""
        try:
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            os.chmod(self.metadata_path, 0o644)
            return True
        except Exception as e:
            print(f"❌ 保存元数据失败: {e}")
            return False

    def _get_file_type(self, filename):
        """根据文件名判断文件类型"""
        ext = os.path.splitext(filename)[1].lower()
        for file_type, extensions in FILE_TYPE_PATTERNS.items():
            if ext in extensions:
                return file_type
        return "other"

    def _deduplicate_documents(self, documents):
        """去重：基于 title + path 去重，保留第一个"""
        seen = {}
        unique_docs = []
        for doc in documents:
            key = f"{doc.get('title', '')}|{doc.get('path', '')}"
            if key not in seen:
                seen[key] = True
                unique_docs.append(doc)
        return unique_docs

    def ensure_directories(self, **kwargs):
        """
        确保标准目录存在
        :return: 创建的目录列表
        """
        created = []
        for dir_name, dir_rel_path in STANDARD_DIRS.items():
            dir_path = os.path.join(self.project_path, dir_rel_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                created.append(dir_name)
                print(f"  创建目录: {dir_name}")
        return created

    def get_directories(self, **kwargs):
        """
        获取项目当前目录结构
        :return: 目录字典 {dir_name: relative_path}
        """
        dirs = {}
        for dir_name, dir_rel_path in STANDARD_DIRS.items():
            dir_path = os.path.join(self.project_path, dir_rel_path)
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                dirs[dir_name] = dir_rel_path
        return dirs

    def get_documents(self, **kwargs):
        """
        获取用户上传文档列表（仅文档目录中的文件）
        :return: 文档列表
        """
        documents = []
        doc_dir = os.path.join(self.project_path, "文档")
        if os.path.exists(doc_dir):
            for filename in os.listdir(doc_dir):
                if not filename.startswith('.'):
                    file_type = self._get_file_type(filename)
                    if file_type == "user_uploaded":
                        documents.append({
                            "title": os.path.splitext(filename)[0],
                            "version": "v1",
                            "path": f"文档/{filename}",
                            "type": "user_uploaded"
                        })
        return self._deduplicate_documents(documents)

    def get_manuscripts(self, **kwargs):
        """
        获取手稿列表（手稿目录中的 .md 文件）
        :return: 手稿列表
        """
        manuscripts = []
        manuscript_dir = os.path.join(self.project_path, "手稿")
        if os.path.exists(manuscript_dir):
            for filename in os.listdir(manuscript_dir):
                if filename.endswith('.md'):
                    manuscripts.append({
                        "title": os.path.splitext(filename)[0],
                        "version": "v1",
                        "path": f"手稿/{filename}",
                        "type": "agent_written"
                    })
        return manuscripts

    def get_notes(self, **kwargs):
        """
        获取笔记列表（知识库/笔记目录中的文件）
        :return: 笔记列表
        """
        notes = []
        notes_dir = os.path.join(self.project_path, "知识库/笔记")
        if os.path.exists(notes_dir):
            for filename in os.listdir(notes_dir):
                if not filename.startswith('.'):
                    notes.append({
                        "title": os.path.splitext(filename)[0],
                        "path": f"知识库/笔记/{filename}",
                        "type": "note"
                    })
        return notes

    def get_reviews(self, **kwargs):
        """
        获取综述列表（知识库/综述目录中的文件）
        :return: 综述列表
        """
        reviews = []
        reviews_dir = os.path.join(self.project_path, "知识库/综述")
        if os.path.exists(reviews_dir):
            for filename in os.listdir(reviews_dir):
                if not filename.startswith('.'):
                    reviews.append({
                        "title": os.path.splitext(filename)[0],
                        "path": f"知识库/综述/{filename}",
                        "type": "review"
                    })
        return reviews

    def move_file(self, file_path, target_dir, **kwargs):
        """
        移动文件到目标目录
        :param file_path: 源文件路径（相对项目根目录或绝对路径）
        :param target_dir: 目标目录（相对项目根目录）
        :return: 是否成功
        """
        # 解析源文件路径
        if os.path.isabs(file_path):
            src_path = file_path
        else:
            src_path = os.path.join(self.project_path, file_path)
        
        if not os.path.exists(src_path):
            print(f"❌ 源文件不存在: {file_path}")
            return False
        
        # 解析目标目录
        target_path = os.path.join(self.project_path, target_dir)
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
        
        # 移动文件
        filename = os.path.basename(src_path)
        dst_path = os.path.join(target_path, filename)
        
        # 如果目标已存在，添加序号
        if os.path.exists(dst_path):
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dst_path):
                new_name = f"{name}_{counter}{ext}"
                dst_path = os.path.join(target_path, new_name)
                counter += 1
        
        try:
            shutil.move(src_path, dst_path)
            rel_dst = os.path.relpath(dst_path, self.project_path)
            print(f"✅ 移动文件: {file_path} -> {rel_dst}")
            return True
        except Exception as e:
            print(f"❌ 移动文件失败: {e}")
            return False

    def rename_folder(self, old_name, new_name, **kwargs):
        """
        重命名项目内的文件夹
        :param old_name: 原文件夹名（相对项目根目录）
        :param new_name: 新文件夹名（相对项目根目录）
        :return: 是否成功
        """
        old_path = os.path.join(self.project_path, old_name)
        new_path = os.path.join(self.project_path, new_name)
        
        if not os.path.exists(old_path):
            print(f"❌ 原文件夹不存在: {old_name}")
            return False
        
        if os.path.exists(new_path):
            print(f"❌ 目标文件夹已存在: {new_name}")
            return False
        
        try:
            os.rename(old_path, new_path)
            print(f"✅ 重命名文件夹: {old_name} -> {new_name}")
            return True
        except Exception as e:
            print(f"❌ 重命名失败: {e}")
            return False

    def update_metadata(self, **kwargs):
        """
        更新项目元数据
        支持传入任意字段更新
        :return: 是否成功
        """
        current_time = datetime.now().isoformat()
        created_date = self.metadata.get("created_date", datetime.now().strftime("%Y-%m-%d"))
        
        # 基础元数据
        new_metadata = {
            "project_id": self.project_name,
            "title": kwargs.get("title", self.metadata.get("title", self.project_name)),
            "created_date": created_date,
            "status": kwargs.get("status", self.metadata.get("status", "active")),
            "version": kwargs.get("version", self.metadata.get("version", "v1")),
            "description": kwargs.get("description", self.metadata.get("description", f"{self.project_name}项目")),
            "directories": self.get_directories(),
            "documents": self.get_documents(),
            "manuscripts": self.get_manuscripts(),
            "notes": self.get_notes(),
            "reviews": self.get_reviews(),
            "tags": kwargs.get("tags", self.metadata.get("tags", [])),
            "cloud_doc_mappings": kwargs.get("cloud_doc_mappings", self.metadata.get("cloud_doc_mappings", {})),
            "knowledge_base": kwargs.get("knowledge_base", self.metadata.get("knowledge_base", {})),
            "updated_at": current_time,
        }
        
        # 合并用户传入的其他字段
        for key, value in kwargs.items():
            if key not in new_metadata:
                new_metadata[key] = value
        
        self.metadata = new_metadata
        return self._save_metadata()

    def organize(self, **kwargs):
        """
        自动整理项目文件
        工作流：
        1. 把中间文件归档到 临时数据/ 下
        2. 综述输出在 知识库/综述/
        3. 笔记输出在 知识库/笔记/
        4. 把用户上传移动到 文档/
        5. 把撰写的最新md文档移动到 手稿/
        6. 把备份版本移动到 临时数据/草稿/
        :return: 整理结果统计
        """
        results = {
            "moved_to_temp": [],
            "moved_to_documents": [],
            "moved_to_manuscripts": [],
            "moved_to_notes": [],
            "moved_to_reviews": [],
            "moved_to_drafts": [],
            "errors": [],
        }
        
        # 确保标准目录存在
        self.ensure_directories()
        
        # 扫描项目根目录下的文件（不包括标准目录和元数据）
        for item in os.listdir(self.project_path):
            item_path = os.path.join(self.project_path, item)
            
            # 跳过标准目录、隐藏文件和元数据
            if item.startswith('.') or item in ["文档", "手稿", "知识库", "临时数据", "元数据.json"]:
                continue
            
            if os.path.isfile(item_path):
                file_type = self._get_file_type(item)
                
                # 判断文件归属
                if file_type == "user_uploaded":
                    # 用户上传文档 -> 文档/
                    if self.move_file(item, "文档/"):
                        results["moved_to_documents"].append(item)
                elif file_type == "agent_written":
                    # 代理撰写的md文件 -> 手稿/
                    if self.move_file(item, "手稿/"):
                        results["moved_to_manuscripts"].append(item)
                elif file_type in ["backup", "intermediate"]:
                    # 备份/中间文件 -> 临时数据/
                    if self.move_file(item, "临时数据/"):
                        results["moved_to_temp"].append(item)
                else:
                    # 其他文件也移到临时数据/
                    if self.move_file(item, "临时数据/"):
                        results["moved_to_temp"].append(item)
        
        # 扫描知识库目录下的文件，分类到笔记/综述
        kb_dir = os.path.join(self.project_path, "知识库")
        if os.path.exists(kb_dir):
            for item in os.listdir(kb_dir):
                item_path = os.path.join(kb_dir, item)
                if os.path.isfile(item_path) and not item.startswith('.'):
                    # 简单规则：包含"综述"或"review"的文件名 -> 综述/
                    if "综述" in item or "review" in item.lower():
                        if self.move_file(f"知识库/{item}", "知识库/综述/"):
                            results["moved_to_reviews"].append(item)
                    else:
                        # 其他 -> 笔记/
                        if self.move_file(f"知识库/{item}", "知识库/笔记/"):
                            results["moved_to_notes"].append(item)
        
        # 扫描旧"草稿"目录，移动到 临时数据/草稿/
        old_draft_dir = os.path.join(self.project_path, "草稿")
        if os.path.exists(old_draft_dir):
            for root, dirs, files in os.walk(old_draft_dir):
                for item in files:
                    item_path = os.path.join(root, item)
                    rel_path = os.path.relpath(item_path, old_draft_dir)
                    if os.path.isfile(item_path) and not item.startswith('.'):
                        if self.move_file(os.path.join("草稿", rel_path), "临时数据/草稿/"):
                            results["moved_to_drafts"].append(rel_path)
                # 处理完成后删除空草稿目录
                if os.path.exists(old_draft_dir):
                    try:
                        shutil.rmtree(old_draft_dir)
                        print(f"  删除空目录: 草稿/")
                    except Exception as e:
                        print(f"  ⚠️  删除草稿目录失败: {e}")
                break
        
        # 扫描旧"终稿"目录，移动md到手稿，其他到文档
        old_final_dir = os.path.join(self.project_path, "终稿")
        if os.path.exists(old_final_dir):
            for root, dirs, files in os.walk(old_final_dir):
                for item in files:
                    item_path = os.path.join(root, item)
                    rel_path = os.path.relpath(item_path, old_final_dir)
                    if os.path.isfile(item_path) and not item.startswith('.'):
                        if item.endswith('.md'):
                            if self.move_file(os.path.join("终稿", rel_path), "手稿/"):
                                results["moved_to_manuscripts"].append(rel_path)
                        else:
                            if self.move_file(os.path.join("终稿", rel_path), "文档/"):
                                results["moved_to_documents"].append(rel_path)
                # 处理子目录中的文件
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    for sub_item in os.listdir(dir_path):
                        sub_item_path = os.path.join(dir_path, sub_item)
                        sub_rel_path = os.path.relpath(sub_item_path, old_final_dir)
                        if os.path.isfile(sub_item_path) and not sub_item.startswith('.'):
                            if sub_item.endswith('.md'):
                                if self.move_file(os.path.join("终稿", sub_rel_path), "手稿/"):
                                    results["moved_to_manuscripts"].append(sub_rel_path)
                            else:
                                if self.move_file(os.path.join("终稿", sub_rel_path), "文档/"):
                                    results["moved_to_documents"].append(sub_rel_path)
                # 处理完成后删除空终稿目录
                if os.path.exists(old_final_dir):
                    try:
                        shutil.rmtree(old_final_dir)
                        print(f"  删除空目录: 终稿/")
                    except Exception as e:
                        print(f"  ⚠️  删除终稿目录失败: {e}")
                break
        
        # 更新元数据（始终保存到根目录）
        self.update_metadata()
        
        # 打印整理报告
        print("\n📊 整理报告:")
        print(f"  移动到文档: {len(results['moved_to_documents'])} 个")
        print(f"  移动到手稿: {len(results['moved_to_manuscripts'])} 个")
        print(f"  移动到笔记: {len(results['moved_to_notes'])} 个")
        print(f"  移动到综述: {len(results['moved_to_reviews'])} 个")
        print(f"  移动到临时数据: {len(results['moved_to_temp'])} 个")
        print(f"  移动到草稿备份: {len(results['moved_to_drafts'])} 个")
        if results["errors"]:
            print(f"  错误: {len(results['errors'])} 个")
        
        return results

    def scan_all(self, **kwargs):
        """
        全面扫描项目，更新所有元数据
        :return: 是否成功
        """
        self.ensure_directories()
        return self.update_metadata()


def list_projects(projects_dir=None, **kwargs):
    """
    列出所有项目
    :param projects_dir: 项目根目录
    :return: 项目列表
    """
    projects_dir = projects_dir or DEFAULT_PROJECTS_DIR
    projects = []
    
    if not os.path.exists(projects_dir):
        return projects
    
    for item in os.listdir(projects_dir):
        item_path = os.path.join(projects_dir, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            metadata_path = os.path.join(item_path, "元数据.json")
            project_info = {
                "name": item,
                "path": item_path,
                "has_metadata": os.path.exists(metadata_path),
            }
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        project_info["status"] = metadata.get("status", "unknown")
                        project_info["version"] = metadata.get("version", "v1")
                except:
                    pass
            projects.append(project_info)
    
    return sorted(projects, key=lambda x: x["name"])


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="项目管理工具")
    parser.add_argument("project", nargs="?", help="项目名称或路径")
    parser.add_argument("--projects-dir", default=DEFAULT_PROJECTS_DIR, help="项目根目录")
    parser.add_argument("--action", default="scan", 
                       choices=["scan", "organize", "move", "rename", "update", "list", "ensure-dirs"],
                       help="执行的操作")
    parser.add_argument("--file", help="源文件路径（用于move）")
    parser.add_argument("--target", help="目标目录（用于move）")
    parser.add_argument("--old-name", help="原名称（用于rename）")
    parser.add_argument("--new-name", help="新名称（用于rename）")
    parser.add_argument("--title", help="项目标题")
    parser.add_argument("--description", help="项目描述")
    parser.add_argument("--status", help="项目状态")
    parser.add_argument("--version", help="项目版本")
    
    args = parser.parse_args()
    
    # list 操作不需要指定项目
    if args.action == "list":
        projects = list_projects(args.projects_dir)
        print(f"找到 {len(projects)} 个项目:\n")
        for p in projects:
            status_icon = "✅" if p["has_metadata"] else "❌"
            print(f"  {status_icon} {p['name']} (状态: {p.get('status', 'unknown')}, 版本: {p.get('version', 'v1')})")
        return
    
    if not args.project:
        print("❌ 请指定项目名称")
        parser.print_help()
        return
    
    # 初始化项目
    project = Project(args.project, args.projects_dir)
    
    if not os.path.exists(project.project_path):
        print(f"❌ 项目不存在: {args.project}")
        return
    
    # 执行操作
    if args.action == "scan":
        project.scan_all()
        print(f"✅ 项目扫描完成: {args.project}")
    
    elif args.action == "organize":
        project.organize()
        print(f"✅ 项目整理完成: {args.project}")
    
    elif args.action == "ensure-dirs":
        created = project.ensure_directories()
        print(f"✅ 目录检查完成，创建 {len(created)} 个目录")
    
    elif args.action == "move":
        if not args.file or not args.target:
            print("❌ move 操作需要 --file 和 --target 参数")
            return
        project.move_file(args.file, args.target)
    
    elif args.action == "rename":
        if not args.old_name or not args.new_name:
            print("❌ rename 操作需要 --old-name 和 --new-name 参数")
            return
        project.rename_folder(args.old_name, args.new_name)
    
    elif args.action == "update":
        kwargs = {}
        if args.title:
            kwargs["title"] = args.title
        if args.description:
            kwargs["description"] = args.description
        if args.status:
            kwargs["status"] = args.status
        if args.version:
            kwargs["version"] = args.version
        project.update_metadata(**kwargs)
        print(f"✅ 元数据更新完成: {args.project}")


if __name__ == "__main__":
    main()
