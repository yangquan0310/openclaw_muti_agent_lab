#!/usr/bin/env python3
"""
Maintainer.py - 项目文件整理模块
负责自动化整理项目目录结构、归档中间文件、管理手稿文件和维护项目元数据
"""

import os
import sys
import json
import shutil
import re
from datetime import datetime
from pathlib import Path


class Maintainer:
    """项目文件整理主类"""

    def __init__(self, project_path):
        """
        初始化项目
        :param project_path: 项目文件夹路径
        """
        self.project_path = os.path.expanduser(project_path)
        self.project_name = os.path.basename(os.path.normpath(self.project_path))
        self.metadata_path = os.path.join(self.project_path, "元数据.json")
        
        # 加载现有元数据
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        """加载现有元数据"""
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  读取现有元数据失败: {e}")
        return {}

    def _save_metadata(self):
        """保存元数据到文件"""
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
        name = os.path.splitext(filename)[0].lower()
        
        # 备份文件
        if any(kw in name for kw in ['backup', '备份', 'old', '旧']):
            return "backup"
        
        # 中间文件
        if ext in ['.tmp', '.temp', '.log', '.bak']:
            return "intermediate"
        
        # 检索条件
        if ext == '.json' and '检索' in name:
            return "search_query"
        
        # 笔记文件
        if '笔记' in name and '提取' in name:
            return "extracted_note"
        
        # 综述文件
        if '综述' in name or 'review' in name:
            return "review"
        
        # 普通笔记
        if '笔记' in name:
            return "note"
        
        # 用户上传文档
        if ext in ['.docx', '.pdf', '.txt', '.doc', '.xlsx', '.pptx']:
            return "user_uploaded"
        
        # 代理撰写的md文件
        if ext == '.md':
            return "agent_written"
        
        return "other"

    def _extract_title(self, filename):
        """从文件名提取标题（去掉版本号、backup等后缀）"""
        name = os.path.splitext(filename)[0]
        # 去掉backup、备份、版本号等后缀
        title = re.sub(r'[_-]*(backup|备份|v\d+|version\d+|old|旧|final|终稿|draft|草稿)', '', name, flags=re.IGNORECASE).strip('_-')
        return title

    def _get_next_version(self, title):
        """获取下一个版本号"""
        draft_dir = os.path.join(self.project_path, "临时数据", "草稿", title)
        if not os.path.exists(draft_dir):
            return "v1"
        
        versions = []
        for f in os.listdir(draft_dir):
            match = re.search(rf"{re.escape(title)}_(v?\d+)", f)
            if match:
                v = int(match.group(1).replace('v', ''))
                versions.append(v)
        
        if versions:
            return f"v{max(versions) + 1}"
        return "v1"

    def archive_to_drafts(self, file_path, title=None, version=None, dry_run=False):
        """
        归档文件到临时数据/草稿/{标题}/目录
        公共方法，支持其他代理进行文档版本控制调用
        
        参数:
            file_path: 源文件路径（相对项目根目录或绝对路径）
            title: 指定标题（可选，默认从文件名提取）
            version: 指定版本号（可选，默认自动递增）
            dry_run: 是否仅预览
        
        返回:
            归档后的相对路径，失败返回None
        
        示例:
            maintainer = Maintainer("~/项目")
            # 自动提取标题和版本号
            maintainer.archive_to_drafts("论文.md")
            # 指定标题和版本
            maintainer.archive_to_drafts("论文.md", title="实验报告", version="v3")
        """
        # 解析源文件路径
        if os.path.isabs(file_path):
            src_path = file_path
        else:
            src_path = os.path.join(self.project_path, file_path)
        
        if not os.path.exists(src_path):
            print(f"❌ 源文件不存在: {file_path}")
            return None
        
        filename = os.path.basename(src_path)
        name, ext = os.path.splitext(filename)
        
        # 确定标题
        if title is None:
            title = self._extract_title(filename)
        
        # 确定版本号
        if version is None:
            version_match = re.search(r'[vV]?(\d+)', name)
            if version_match:
                version = f"v{version_match.group(1)}"
            else:
                version = self._get_next_version(title)
        
        # 构建目标路径: 临时数据/草稿/{标题}/{标题}_{version}.md
        draft_dir = os.path.join(self.project_path, "临时数据", "草稿", title)
        target_name = f"{title}_{version}{ext}"
        target_path = os.path.join(draft_dir, target_name)
        
        if dry_run:
            rel_path = os.path.relpath(target_path, self.project_path)
            print(f"  [预览] 归档: {filename} -> {rel_path}")
            return rel_path
        
        # 创建目录
        os.makedirs(draft_dir, exist_ok=True)
        
        # 移动文件
        try:
            shutil.move(src_path, target_path)
            rel_path = os.path.relpath(target_path, self.project_path)
            print(f"  ✅ 归档草稿: {filename} -> {rel_path}")
            return rel_path
        except Exception as e:
            print(f"  ❌ 归档失败: {e}")
            return None

    def ensure_directories(self):
        """确保标准目录存在"""
        dirs = {
            "文档": "文档/",
            "手稿": "手稿/",
            "知识库": "知识库/",
            "知识库/笔记": "知识库/笔记/",
            "知识库/综述": "知识库/综述/",
            "临时数据": "临时数据/",
            "临时数据/草稿": "临时数据/草稿/",
            "临时数据/检索条件": "临时数据/检索条件/",
            "临时数据/笔记": "临时数据/笔记/",
        }
        
        created = []
        for dir_name, dir_rel_path in dirs.items():
            dir_path = os.path.join(self.project_path, dir_rel_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                created.append(dir_name)
                print(f"  创建目录: {dir_name}")
        return created

    def _move_file(self, file_path, target_dir, new_name=None, overwrite=False):
        """
        移动文件到目标目录（私有方法，被organize调用）
        
        参数:
            file_path: 源文件路径（相对项目根目录或绝对路径）
            target_dir: 目标目录（相对项目根目录）
            new_name: 新文件名（可选）
            overwrite: 是否覆盖已存在文件
            
        返回:
            目标相对路径，失败返回None
        """
        # 解析源文件路径
        if os.path.isabs(file_path):
            src_path = file_path
        else:
            src_path = os.path.join(self.project_path, file_path)
        
        if not os.path.exists(src_path):
            print(f"❌ 源文件不存在: {file_path}")
            return None
        
        # 解析目标目录
        target_path = os.path.join(self.project_path, target_dir)
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
        
        # 确定目标文件名
        if new_name:
            filename = new_name
        else:
            filename = os.path.basename(src_path)
        
        dst_path = os.path.join(target_path, filename)
        
        # 如果目标已存在，添加序号
        if os.path.exists(dst_path) and not overwrite:
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dst_path):
                new_name = f"{name}_{counter}{ext}"
                dst_path = os.path.join(target_path, new_name)
                counter += 1
        
        try:
            shutil.move(src_path, dst_path)
            rel_dst = os.path.relpath(dst_path, self.project_path)
            return rel_dst
        except Exception as e:
            print(f"❌ 移动文件失败: {e}")
            return None

    def _move_to_documents(self, item, item_path, dry_run=False):
        """移动文件到文档目录"""
        if dry_run:
            return f"{item} -> 文档/"
        target = self._move_file(item_path, "文档")
        return target if target else None

    def _move_to_manuscripts(self, item, item_path, dry_run=False):
        """移动文件到手稿目录"""
        if dry_run:
            return f"{item} -> 手稿/"
        target = self._move_file(item_path, "手稿")
        return target if target else None

    def _move_to_notes(self, item, item_path, dry_run=False):
        """移动文件到知识库/笔记目录"""
        if dry_run:
            return f"{item} -> 知识库/笔记/"
        target = self._move_file(item_path, "知识库/笔记")
        return target if target else None

    def _move_to_reviews(self, item, item_path, dry_run=False):
        """移动文件到知识库/综述目录"""
        if dry_run:
            return f"{item} -> 知识库/综述/"
        target = self._move_file(item_path, "知识库/综述")
        return target if target else None

    def _move_to_search_queries(self, item, item_path, dry_run=False):
        """移动文件到临时数据/检索条件目录"""
        if dry_run:
            return f"{item} -> 临时数据/检索条件/"
        target = self._move_file(item_path, "临时数据/检索条件")
        return target if target else None

    def _move_to_extracted_notes(self, item, item_path, dry_run=False):
        """移动文件到临时数据/笔记目录"""
        if dry_run:
            return f"{item} -> 临时数据/笔记/"
        target = self._move_file(item_path, "临时数据/笔记")
        return target if target else None

    def _archive_to_drafts_internal(self, item, item_path, dry_run=False):
        """归档文件到临时数据/草稿目录"""
        if dry_run:
            target = self.archive_to_drafts(item_path, dry_run=True)
            return f"{item} -> {target}"
        target = self.archive_to_drafts(item_path)
        return target if target else None

    def _move_to_temp_data(self, item, item_path, dry_run=False):
        """移动文件到临时数据目录"""
        if dry_run:
            return f"{item} -> 临时数据/"
        target = self._move_file(item_path, "临时数据")
        return target if target else None

    def _move_directory_contents(self, src_dir, dst_dir, file_filter=None, dry_run=False):
        """
        移动目录内容到目标目录（私有方法，被organize调用）
        
        参数:
            src_dir: 源目录（相对项目根目录或绝对路径）
            dst_dir: 目标目录（相对项目根目录）
            file_filter: 文件过滤函数（可选）
            dry_run: 是否仅预览
            
        返回:
            移动的文件列表
        """
        results = []
        
        # 解析源目录
        if os.path.isabs(src_dir):
            src_path = src_dir
        else:
            src_path = os.path.join(self.project_path, src_dir)
        
        if not os.path.exists(src_path):
            return results
        
        # 解析目标目录
        dst_path = os.path.join(self.project_path, dst_dir)
        os.makedirs(dst_path, exist_ok=True)
        
        for item in os.listdir(src_path):
            item_path = os.path.join(src_path, item)
            if os.path.isfile(item_path):
                # 应用过滤
                if file_filter and not file_filter(item):
                    continue
                
                dst_item = os.path.join(dst_path, item)
                
                # 处理重名
                if os.path.exists(dst_item):
                    base, ext = os.path.splitext(item)
                    counter = 1
                    while os.path.exists(dst_item):
                        dst_item = os.path.join(dst_path, f"{base}_{counter}{ext}")
                        counter += 1
                
                if dry_run:
                    rel_src = os.path.relpath(item_path, self.project_path)
                    rel_dst = os.path.relpath(dst_item, self.project_path)
                    results.append(f"{rel_src} -> {rel_dst}")
                else:
                    try:
                        shutil.move(item_path, dst_item)
                        rel_dst = os.path.relpath(dst_item, self.project_path)
                        results.append(rel_dst)
                        print(f"  ✅ 移动: {os.path.basename(src_dir)}/{item} -> {dst_dir}/")
                    except Exception as e:
                        print(f"  ❌ 移动失败: {item} - {e}")
        
        # 删除空源目录
        if not dry_run and os.path.exists(src_path):
            try:
                remaining = os.listdir(src_path)
                if not remaining:
                    os.rmdir(src_path)
                    print(f"  ✅ 删除空目录: {src_dir}/")
            except Exception as e:
                print(f"  ⚠️  删除目录失败: {src_dir} - {e}")
        
        return results

    def _move_nonstandard_dirs(self, dry_run=False):
        """
        移动非标准目录文件到标准位置（私有方法，被organize调用）
        处理：知识库/检索报告/、知识库/文献综述/、审稿意见/、指南文档/、文献综述/
        """
        results = {
            "moved_to_manuscripts": [],
            "moved_to_reviews": [],
            "moved_to_documents": [],
        }
        
        # 1. 知识库/检索报告/ -> 手稿/
        search_report_dir = os.path.join(self.project_path, "知识库", "检索报告")
        if os.path.exists(search_report_dir):
            moved = self._move_directory_contents(
                search_report_dir, "手稿", 
                dry_run=dry_run
            )
            results["moved_to_manuscripts"].extend(moved)
            if not dry_run and os.path.exists(search_report_dir):
                try:
                    os.rmdir(search_report_dir)
                    print(f"  ✅ 删除空目录: 知识库/检索报告/")
                except:
                    pass
        
        # 2. 知识库/文献综述/ -> 知识库/综述/
        lit_review_dir = os.path.join(self.project_path, "知识库", "文献综述")
        if os.path.exists(lit_review_dir):
            moved = self._move_directory_contents(
                lit_review_dir, "知识库/综述",
                dry_run=dry_run
            )
            results["moved_to_reviews"].extend(moved)
            if not dry_run and os.path.exists(lit_review_dir):
                try:
                    os.rmdir(lit_review_dir)
                    print(f"  ✅ 删除空目录: 知识库/文献综述/")
                except:
                    pass
        
        # 3. 审稿意见/ -> 手稿/
        review_opinion_dir = os.path.join(self.project_path, "审稿意见")
        if os.path.exists(review_opinion_dir):
            moved = self._move_directory_contents(
                review_opinion_dir, "手稿",
                dry_run=dry_run
            )
            results["moved_to_manuscripts"].extend(moved)
            if not dry_run and os.path.exists(review_opinion_dir):
                try:
                    os.rmdir(review_opinion_dir)
                    print(f"  ✅ 删除空目录: 审稿意见/")
                except:
                    pass
        
        # 4. 指南文档/ -> 文档/
        guide_dir = os.path.join(self.project_path, "指南文档")
        if os.path.exists(guide_dir):
            moved = self._move_directory_contents(
                guide_dir, "文档",
                dry_run=dry_run
            )
            results["moved_to_documents"].extend(moved)
            if not dry_run and os.path.exists(guide_dir):
                try:
                    os.rmdir(guide_dir)
                    print(f"  ✅ 删除空目录: 指南文档/")
                except:
                    pass
        
        # 5. 文献综述/ -> 知识库/综述/
        lit_review_root = os.path.join(self.project_path, "文献综述")
        if os.path.exists(lit_review_root):
            moved = self._move_directory_contents(
                lit_review_root, "知识库/综述",
                dry_run=dry_run
            )
            results["moved_to_reviews"].extend(moved)
            if not dry_run and os.path.exists(lit_review_root):
                try:
                    os.rmdir(lit_review_root)
                    print(f"  ✅ 删除空目录: 文献综述/")
                except:
                    pass
        
        return results

    def _archive_old_versions(self, dry_run=False):
        """
        归档临时数据/草稿/中的旧版本文件（私有方法，被organize调用）
        处理：文件名含 v数字、backup、old、旧 等标记的文件
        """
        results = []
        drafts_dir = os.path.join(self.project_path, "临时数据", "草稿")
        
        if not os.path.exists(drafts_dir):
            return results
        
        for item in os.listdir(drafts_dir):
            item_path = os.path.join(drafts_dir, item)
            if os.path.isfile(item_path):
                # 检查是否是旧版本文件
                if re.search(r'[vV]\d+|backup|备份|old|旧', item):
                    if dry_run:
                        target = self.archive_to_drafts(item_path, dry_run=True)
                        if target:
                            results.append(f"{item} -> {target}")
                    else:
                        try:
                            target = self.archive_to_drafts(item_path)
                            if target:
                                results.append(target)
                        except Exception as e:
                            print(f"  ❌ 归档失败: {item} - {e}")
        
        return results

    def _move_md_from_documents(self, dry_run=False):
        """
        移动文档目录中的 .md 文件到手稿/（私有方法，被organize调用）
        """
        results = []
        doc_dir = os.path.join(self.project_path, "文档")
        
        if not os.path.exists(doc_dir):
            return results
        
        for item in os.listdir(doc_dir):
            if item.endswith('.md'):
                item_path = os.path.join(doc_dir, item)
                if dry_run:
                    results.append(f"{item} -> 手稿/")
                else:
                    target = self._move_file(item_path, "手稿")
                    if target:
                        results.append(target)
        
        return results

    def _unify_index_filename(self, dry_run=False):
        """
        统一知识库/笔记/中的索引文件名（私有方法，被organize调用）
        将 索引.json 重命名为 index.json
        """
        results = []
        notes_dir = os.path.join(self.project_path, "知识库", "笔记")
        
        if not os.path.exists(notes_dir):
            return results
        
        for item in os.listdir(notes_dir):
            if item == "索引.json":
                src = os.path.join(notes_dir, item)
                dst = os.path.join(notes_dir, "index.json")
                if not os.path.exists(dst):
                    if dry_run:
                        results.append(f"知识库/笔记/索引.json -> index.json")
                    else:
                        try:
                            shutil.move(src, dst)
                            results.append("index.json")
                            print(f"  ✅ 重命名: 知识库/笔记/索引.json -> index.json")
                        except Exception as e:
                            print(f"  ❌ 重命名失败: {e}")
        
        return results

    def _remove_nested_project_dir(self, dry_run=False):
        """
        删除嵌套的项目目录（私有方法，被organize调用）
        例如：AI降重提示工程/AI降重提示工程/
        """
        nested_dir = os.path.join(self.project_path, self.project_name)
        if not os.path.exists(nested_dir) or not os.path.isdir(nested_dir):
            return []
        
        results = []
        
        # 移动嵌套目录中的文件到根目录
        for item in os.listdir(nested_dir):
            src = os.path.join(nested_dir, item)
            dst = os.path.join(self.project_path, item)
            if os.path.exists(dst):
                print(f"    跳过（已存在）: {item}")
                continue
            if dry_run:
                results.append(f"{self.project_name}/{item} -> {item}")
            else:
                try:
                    shutil.move(src, dst)
                    results.append(item)
                    print(f"    移动: {item} -> 根目录")
                except Exception as e:
                    print(f"    移动失败: {item} - {e}")
        
        # 删除空嵌套目录
        if not dry_run and os.path.exists(nested_dir):
            try:
                shutil.rmtree(nested_dir)
                print(f"  ✅ 删除嵌套目录: {self.project_name}/")
            except Exception as e:
                print(f"  ❌ 删除嵌套目录失败: {e}")
        
        return results

    def _remove_old_metadata_backups(self, dry_run=False):
        """
        删除旧的元数据备份文件（私有方法，被organize调用）
        删除：临时数据/元数据_1.json、临时数据/元数据_2.json 等
        """
        results = []
        temp_dir = os.path.join(self.project_path, "临时数据")
        
        if not os.path.exists(temp_dir):
            return results
        
        for item in os.listdir(temp_dir):
            if item.startswith("元数据_") and item.endswith(".json"):
                item_path = os.path.join(temp_dir, item)
                if dry_run:
                    results.append(item)
                else:
                    try:
                        os.remove(item_path)
                        results.append(item)
                        print(f"  ✅ 删除旧元数据备份: {item}")
                    except Exception as e:
                        print(f"  ❌ 删除失败: {item} - {e}")
        
        return results

    def organize(self, dry_run=False):
        """
        自动整理项目文件
        包含：移动非标准目录、归档旧版本、统一文件名、删除嵌套目录等
        """
        results = {
            "moved_to_documents": [],
            "moved_to_manuscripts": [],
            "moved_to_notes": [],
            "moved_to_reviews": [],
            "archived_to_drafts": [],
            "moved_to_search_queries": [],
            "moved_to_extracted_notes": [],
            "deleted_nested_dirs": [],
            "deleted_old_backups": [],
            "renamed_index_files": [],
            "errors": [],
        }
        
        # 确保标准目录存在
        self.ensure_directories()
        
        # 1. 删除嵌套的项目目录
        print(f"\n  [1/6] 检查嵌套目录...")
        nested_results = self._remove_nested_project_dir(dry_run=dry_run)
        results["deleted_nested_dirs"].extend(nested_results)
        
        # 2. 删除旧的元数据备份
        print(f"\n  [2/6] 删除旧元数据备份...")
        backup_results = self._remove_old_metadata_backups(dry_run=dry_run)
        results["deleted_old_backups"].extend(backup_results)
        
        # 3. 移动非标准目录文件
        print(f"\n  [3/6] 移动非标准目录...")
        nonstandard_results = self._move_nonstandard_dirs(dry_run=dry_run)
        for key in nonstandard_results:
            if key in results:
                results[key].extend(nonstandard_results[key])
        
        # 4. 归档旧版本文件
        print(f"\n  [4/6] 归档旧版本...")
        archive_results = self._archive_old_versions(dry_run=dry_run)
        results["archived_to_drafts"].extend(archive_results)
        
        # 5. 移动文档目录中的 .md 文件
        print(f"\n  [5/6] 移动文档中的md文件...")
        md_results = self._move_md_from_documents(dry_run=dry_run)
        results["moved_to_manuscripts"].extend(md_results)
        
        # 6. 统一索引文件名
        print(f"\n  [6/6] 统一索引文件名...")
        index_results = self._unify_index_filename(dry_run=dry_run)
        results["renamed_index_files"].extend(index_results)
        
        # 7. 扫描项目根目录下的文件（标准整理）
        print(f"\n  [标准整理] 扫描根目录文件...")
        for item in os.listdir(self.project_path):
            item_path = os.path.join(self.project_path, item)
            
            # 跳过标准目录、隐藏文件和元数据
            if item.startswith('.') or item in ["文档", "手稿", "知识库", "临时数据", "元数据.json"]:
                continue
            
            if os.path.isfile(item_path):
                file_type = self._get_file_type(item)
                
                if file_type == "user_uploaded":
                    target = self._move_to_documents(item, item_path, dry_run)
                    if target:
                        results["moved_to_documents"].append(target)
                        
                elif file_type == "agent_written":
                    target = self._move_to_manuscripts(item, item_path, dry_run)
                    if target:
                        results["moved_to_manuscripts"].append(target)
                        
                elif file_type == "backup":
                    target = self._archive_to_drafts_internal(item, item_path, dry_run)
                    if target:
                        results["archived_to_drafts"].append(target)
                            
                elif file_type == "intermediate":
                    target = self._move_to_temp_data(item, item_path, dry_run)
                    if target:
                        results["archived_to_drafts"].append(target)
                        
                elif file_type == "search_query":
                    target = self._move_to_search_queries(item, item_path, dry_run)
                    if target:
                        results["moved_to_search_queries"].append(target)
                        
                elif file_type == "extracted_note":
                    target = self._move_to_extracted_notes(item, item_path, dry_run)
                    if target:
                        results["moved_to_extracted_notes"].append(target)
                        
                elif file_type == "review":
                    target = self._move_to_reviews(item, item_path, dry_run)
                    if target:
                        results["moved_to_reviews"].append(target)
                        
                elif file_type == "note":
                    target = self._move_to_notes(item, item_path, dry_run)
                    if target:
                        results["moved_to_notes"].append(target)
                        
                else:
                    target = self._move_to_temp_data(item, item_path, dry_run)
                    if target:
                        results["archived_to_drafts"].append(target)
        
        # 扫描知识库目录下的文件，分类到笔记/综述
        kb_dir = os.path.join(self.project_path, "知识库")
        if os.path.exists(kb_dir):
            for item in os.listdir(kb_dir):
                item_path = os.path.join(kb_dir, item)
                if os.path.isfile(item_path) and not item.startswith('.'):
                    if "综述" in item or "review" in item.lower():
                        target = self._move_to_reviews(item, item_path, dry_run)
                        if target:
                            results["moved_to_reviews"].append(target)
                    else:
                        target = self._move_to_notes(item, item_path, dry_run)
                        if target:
                            results["moved_to_notes"].append(target)
        
        # 扫描旧"草稿"目录，移动到 临时数据/草稿/
        old_draft_dir = os.path.join(self.project_path, "草稿")
        if os.path.exists(old_draft_dir):
            for root, dirs, files in os.walk(old_draft_dir):
                for item in files:
                    item_path = os.path.join(root, item)
                    rel_path = os.path.relpath(item_path, old_draft_dir)
                    if os.path.isfile(item_path) and not item.startswith('.'):
                        target = self._archive_to_drafts_internal(item, item_path, dry_run)
                        if target:
                            results["archived_to_drafts"].append(target)
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
                            target = self._move_to_manuscripts(item, item_path, dry_run)
                            if target:
                                results["moved_to_manuscripts"].append(target)
                        else:
                            target = self._move_to_documents(item, item_path, dry_run)
                            if target:
                                results["moved_to_documents"].append(target)
                # 处理完成后删除空终稿目录
                if os.path.exists(old_final_dir):
                    try:
                        shutil.rmtree(old_final_dir)
                        print(f"  删除空目录: 终稿/")
                    except Exception as e:
                        print(f"  ⚠️  删除终稿目录失败: {e}")
                break
        
        # 更新元数据
        if not dry_run:
            self.update_metadata()
        
        return results

    def move_file(self, file_path, target_dir, new_name=None, overwrite=False):
        """
        移动文件到目标目录
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
        
        # 确定目标文件名
        if new_name:
            filename = new_name
        else:
            filename = os.path.basename(src_path)
        
        dst_path = os.path.join(target_path, filename)
        
        # 如果目标已存在，添加序号
        if os.path.exists(dst_path) and not overwrite:
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

    def rename_folder(self, old_name, new_name, merge=False):
        """
        重命名项目内的文件夹
        """
        old_path = os.path.join(self.project_path, old_name)
        new_path = os.path.join(self.project_path, new_name)
        
        if not os.path.exists(old_path):
            print(f"❌ 原文件夹不存在: {old_name}")
            return False
        
        if os.path.exists(new_path):
            if merge:
                # 合并内容
                for item in os.listdir(old_path):
                    src = os.path.join(old_path, item)
                    dst = os.path.join(new_path, item)
                    if os.path.exists(dst):
                        # 如果目标已存在，添加序号
                        name, ext = os.path.splitext(item)
                        counter = 1
                        while os.path.exists(dst):
                            new_item = f"{name}_{counter}{ext}"
                            dst = os.path.join(new_path, new_item)
                            counter += 1
                    shutil.move(src, dst)
                try:
                    os.rmdir(old_path)
                    print(f"✅ 合并并删除: {old_name} -> {new_name}")
                    return True
                except Exception as e:
                    print(f"⚠️  合并后删除原目录失败: {e}")
                    return False
            else:
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
        """
        current_time = datetime.now().isoformat()
        created_date = self.metadata.get("created_date", datetime.now().strftime("%Y-%m-%d"))
        
        # 构建目录结构
        directories = {
            "文档": "文档/",
            "手稿": "手稿/",
            "知识库": "知识库/",
            "笔记": "知识库/笔记/",
            "综述": "知识库/综述/",
            "临时数据": "临时数据/",
            "草稿": "临时数据/草稿/",
            "检索条件": "临时数据/检索条件/",
            "临时笔记": "临时数据/笔记/",
        }
        
        # 扫描文档
        documents = []
        doc_dir = os.path.join(self.project_path, "文档")
        if os.path.exists(doc_dir):
            for filename in os.listdir(doc_dir):
                if not filename.startswith('.'):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in ['.docx', '.pdf', '.txt', '.doc', '.xlsx', '.pptx']:
                        documents.append({
                            "title": os.path.splitext(filename)[0],
                            "version": "v1",
                            "path": f"文档/{filename}",
                            "type": "user_uploaded"
                        })
        
        # 扫描手稿（markdown文件）
        markdown = {}
        manuscript_dir = os.path.join(self.project_path, "手稿")
        if os.path.exists(manuscript_dir):
            for filename in os.listdir(manuscript_dir):
                if filename.endswith('.md'):
                    markdown[filename] = {
                        "local_path": f"手稿/{filename}",
                        "cloud": []
                    }
        
        # 扫描笔记
        notes = {}
        notes_dir = os.path.join(self.project_path, "知识库", "笔记")
        if os.path.exists(notes_dir):
            for filename in os.listdir(notes_dir):
                if not filename.startswith('.'):
                    notes[filename] = {
                        "local_path": f"知识库/笔记/{filename}",
                        "created_at": created_date,
                        "description": ""
                    }
        
        # 扫描综述
        reviews = {}
        reviews_dir = os.path.join(self.project_path, "知识库", "综述")
        if os.path.exists(reviews_dir):
            for filename in os.listdir(reviews_dir):
                if not filename.startswith('.'):
                    reviews[filename] = {
                        "local_path": f"知识库/综述/{filename}"
                    }
        
        # 构建新元数据
        new_metadata = {
            "project_id": self.project_name,
            "title": kwargs.get("title", self.metadata.get("title", self.project_name)),
            "created_date": created_date,
            "status": kwargs.get("status", self.metadata.get("status", "active")),
            "version": kwargs.get("version", self.metadata.get("version", "v1")),
            "description": kwargs.get("description", self.metadata.get("description", f"{self.project_name}项目")),
            "directories": directories,
            "documents": documents,
            "markdown": markdown,
            "notes": notes,
            "reviews": reviews,
            "tags": kwargs.get("tags", self.metadata.get("tags", [])),
            "knowledge_base": {
                "index_file": "知识库/index.json",
                "description": f"{self.project_name}项目知识库索引",
                "created_at": created_date,
                "updated_at": current_time
            },
            "updated_at": current_time,
        }
        
        # 合并用户传入的其他字段
        for key, value in kwargs.items():
            if key not in new_metadata:
                new_metadata[key] = value
        
        self.metadata = new_metadata
        return self._save_metadata()

    def get_documents(self):
        """获取文档列表"""
        documents = []
        doc_dir = os.path.join(self.project_path, "文档")
        if os.path.exists(doc_dir):
            for filename in os.listdir(doc_dir):
                if not filename.startswith('.'):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in ['.docx', '.pdf', '.txt', '.doc', '.xlsx', '.pptx']:
                        documents.append({
                            "title": os.path.splitext(filename)[0],
                            "version": "v1",
                            "path": f"文档/{filename}",
                            "type": "user_uploaded"
                        })
        return documents

    def get_manuscripts(self):
        """获取手稿列表"""
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


class MetadataManager:
    """元数据管理器 - 不直接编辑文件，通过方法操作"""
    
    def __init__(self, project_path):
        self.project_path = os.path.expanduser(project_path)
        self.metadata_path = os.path.join(self.project_path, "元数据.json")
        self.metadata = self._load_metadata()
    
    def _load_metadata(self):
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  读取元数据失败: {e}")
        return {}
    
    def save(self):
        try:
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            os.chmod(self.metadata_path, 0o644)
            print("✅ 元数据已保存")
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


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="项目文件整理工具")
    parser.add_argument("--all", action="store_true", help="整理所有项目")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    parser.add_argument("--projects-dir", default="/root/实验室仓库/项目文件", help="项目根目录")
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 整理命令（默认）
    organize_parser = subparsers.add_parser("organize", help="整理项目文件（默认命令）")
    organize_parser.add_argument("project_path", nargs="?", help="项目路径")
    organize_parser.add_argument("--all", action="store_true", help="整理所有项目")
    organize_parser.add_argument("--dry-run", action="store_true", help="预览模式")
    organize_parser.add_argument("--projects-dir", default="/root/实验室仓库/项目文件", help="项目根目录")
    
    # 归档命令
    archive_parser = subparsers.add_parser("archive", help="归档文件到草稿目录")
    archive_parser.add_argument("project_path", help="项目路径")
    archive_parser.add_argument("file", help="要归档的文件路径（相对项目根目录或绝对路径）")
    archive_parser.add_argument("--title", help="指定标题（默认从文件名提取）")
    archive_parser.add_argument("--version", help="指定版本号（默认自动递增）")
    archive_parser.add_argument("--dry-run", action="store_true", help="预览模式")
    
    # 移动命令
    move_parser = subparsers.add_parser("move", help="移动文件到标准目录")
    move_parser.add_argument("project_path", help="项目路径")
    move_parser.add_argument("file", help="要移动的文件路径（相对项目根目录）")
    move_parser.add_argument("target", help="目标目录（文档/手稿/知识库/笔记/知识库/综述/临时数据/临时数据/草稿/临时数据/检索条件/临时数据/笔记）")
    move_parser.add_argument("--new-name", help="新文件名（可选）")
    move_parser.add_argument("--overwrite", action="store_true", help="覆盖已存在文件")
    
    # 元数据管理参数
    meta_parser = subparsers.add_parser("meta", help="元数据管理")
    meta_parser.add_argument("project_path", help="项目路径")
    meta_parser.add_argument("--title", help="设置项目标题")
    meta_parser.add_argument("--desc", "--description", help="设置项目描述")
    meta_parser.add_argument("--status", help="设置项目状态")
    meta_parser.add_argument("--version", help="设置版本号")
    meta_parser.add_argument("--tags", help="设置标签（逗号分隔）")
    meta_parser.add_argument("--add-tag", action="append", help="添加标签")
    meta_parser.add_argument("--rm-tag", action="append", help="移除标签")
    meta_parser.add_argument("--set", action="append", help="通用字段设置（KEY=VALUE）")
    meta_parser.add_argument("--show", action="store_true", help="显示当前元数据")
    meta_parser.add_argument("--save", action="store_true", help="显式保存")

    args = parser.parse_args()
    
    # 如果没有指定命令，默认使用 organize
    if not args.command:
        # 将参数转换为 organize 子命令的参数
        args.command = "organize"
        # 从全局参数获取 project_path
        if not hasattr(args, 'project_path'):
            args.project_path = None
    
    # 整理模式（默认）
    if args.command == "organize":
        if args.all:
            projects_dir = args.projects_dir
            if not os.path.exists(projects_dir):
                print(f"❌ 项目根目录不存在: {projects_dir}")
                sys.exit(1)
            
            for project_name in os.listdir(projects_dir):
                project_path = os.path.join(projects_dir, project_name)
                if os.path.isdir(project_path) and not project_name.startswith('.'):
                    print(f"\n📁 整理项目: {project_name}")
                    maintainer = Maintainer(project_path)
                    results = maintainer.organize(dry_run=args.dry_run)
                    
                    if args.dry_run:
                        print("  [预览模式]")
                        for key, items in results.items():
                            if items:
                                print(f"  {key}: {len(items)} 项")
                                for item in items[:5]:
                                    print(f"    - {item}")
                                if len(items) > 5:
                                    print(f"    ... 等 {len(items)} 项")
                    else:
                        total = sum(len(items) for items in results.values() if isinstance(items, list))
                        print(f"  ✅ 完成，共处理 {total} 个文件")
        else:
            if not args.project_path:
                print("❌ 请指定项目路径或使用 --all")
                sys.exit(1)
            
            maintainer = Maintainer(args.project_path)
            results = maintainer.organize(dry_run=args.dry_run)
            
            if args.dry_run:
                print("\n[预览模式]")
                for key, items in results.items():
                    if items:
                        print(f"{key}: {len(items)} 项")
                        for item in items[:10]:
                            print(f"  - {item}")
                        if len(items) > 10:
                            print(f"  ... 等 {len(items)} 项")
            else:
                total = sum(len(items) for items in results.values() if isinstance(items, list))
                print(f"\n✅ 完成，共处理 {total} 个文件")
        return

    # 归档模式
    if args.command == "archive":
        maintainer = Maintainer(args.project_path)
        result = maintainer.archive_to_drafts(
            args.file,
            title=args.title,
            version=args.version,
            dry_run=args.dry_run
        )
        if result:
            print(f"✅ 归档成功: {result}")
        else:
            print("❌ 归档失败")
        return
    
    # 移动模式
    if args.command == "move":
        maintainer = Maintainer(args.project_path)
        result = maintainer.move_file(
            args.file,
            args.target,
            new_name=args.new_name,
            overwrite=args.overwrite
        )
        if result:
            print(f"✅ 移动成功")
        else:
            print("❌ 移动失败")
        return
    
    # 元数据管理模式
    if args.command == "meta":
        mm = MetadataManager(args.project_path)
        
        if args.title:
            mm.set_title(args.title)
        if args.desc:
            mm.set_description(args.desc)
        if args.status:
            mm.set_status(args.status)
        if args.version:
            mm.set_version(args.version)
        if args.tags:
            mm.set_tags(args.tags.split(","))
        if args.add_tag:
            for tag in args.add_tag:
                mm.add_tag(tag)
        if args.rm_tag:
            for tag in args.rm_tag:
                mm.remove_tag(tag)
        if args.set:
            for setting in args.set:
                if "=" in setting:
                    key, value = setting.split("=", 1)
                    mm.set_field(key.strip(), value.strip())
        
        if args.show:
            print(json.dumps(mm.to_dict(), ensure_ascii=False, indent=2))
        
        if args.save or not args.show:
            mm.save()
        
        return


if __name__ == "__main__":
    main()
