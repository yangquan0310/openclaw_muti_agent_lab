#!/usr/bin/env python3
"""
Maintainer.py - 项目文件整理模块
负责自动化整理项目目录结构、归档中间文件、管理manuscripts文件和维护项目元数据

OOP架构：
- BaseMaintainer: 通用基类，定义模板方法和多态钩子
- Maintainer: 项目主入口，根据 project_type 路由到正确的子类
- ThesisMaintainer / CourseMaintainer / ProgramMaintainer: 各项目类型的具体实现

所有CLI命令通过 Maintainer.from_path() 自动路由到对应子类，确保多态生效。
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/steward/skills/manager/scripts')
from maintainer.BaseMaintainer import BaseMaintainer

import os
import json
import shutil
import re
from datetime import datetime
from pathlib import Path


class Maintainer(BaseMaintainer):
    """项目文件整理主类（主入口，根据 project_type 路由到子类）"""

    # ──────────────────────────────
    # 工厂方法（多态分发）
    # ──────────────────────────────
    @classmethod
    def from_path(cls, project_path):
        """
        工厂方法：根据项目路径自动创建对应子类的实例
        内部委托给 BaseMaintainer.from_path() 实现
        """
        return BaseMaintainer.from_path(project_path)

    # ──────────────────────────────
    # 初始化（委托给父类）
    # ──────────────────────────────
    def __init__(self, project_path):
        """
        初始化项目。直接委托给 BaseMaintainer。
        注意：CLI 应使用 Maintainer.from_path() 获取正确子类的实例，
        以确保多态生效。
        """
        super().__init__(project_path)

    # ──────────────────────────────
    # 以下方法保留用于直接调用（向后兼容）
    # 推荐使用 Maintainer.from_path() 获取子类实例
    # ──────────────────────────────

    def _get_file_type(self, filename):
        """根据文件名判断文件类型"""
        ext = os.path.splitext(filename)[1].lower()
        name = os.path.splitext(filename)[0].lower()

        # 保护文件:根目录重要文件,不自动移动
        PROTECTED_FILES = ['readme', 'index', 'config', 'metadata', 'skill', 'todo', 'agentignore']
        PROTECTED_EXTS = ['.py', '.sh', '.yaml', '.yml', '.toml', '.ini']
        # 确保 index.json 在任何位置都是保护文件(尤其是 knowledge/ 根目录)
        if filename.lower() == 'index.json':
            return "protected"
        if any(filename.lower() == (p + ext).lower() for p in PROTECTED_FILES) or \
           any(filename.lower().startswith(p + '_') for p in PROTECTED_FILES) or \
           ext in PROTECTED_EXTS or \
           any(kw in name for kw in ['保留', 'keep', 'protected']):
            return "protected"

        # 中间文件（.tmp/.temp/.log/.bak 直接删除或由 git 管理）
        if ext in ['.tmp', '.temp', '.log', '.bak'] or \
           any(kw in name for kw in ['backup', '备份', 'old', '旧']):
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

        # 检索报告(.md文件含"检索报告",归入知识库)
        if ext == '.md' and '检索报告' in name:
            return "retrieval_report"

        # topic 子集(.json 文件,归入 knowledge/topic/)
        if ext == '.json' and filename != 'index.json':
            return "topic_subset"

        # 普通笔记
        if '笔记' in name:
            return "note"

        # 用户上传uploads
        if ext in ['.docx', '.pdf', '.txt', '.doc', '.xlsx', '.pptx']:
            return "user_uploaded"

        # 代理撰写的md文件
        if ext == '.md':
            return "agent_written"

        return "other"

    def _load_agentignore(self):
        """加载 .agentignore 文件,返回忽略规则列表"""
        agentignore_path = os.path.join(self.project_path, ".agentignore")
        if not os.path.exists(agentignore_path):
            return []

        rules = []
        try:
            with open(agentignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        rules.append(line)
        except Exception as e:
            print(f"⚠️  读取 .agentignore 失败: {e}")
        return rules

    def _is_ignored(self, name, ignore_rules):
        """检查文件名是否匹配 .agentignore 规则"""
        for rule in ignore_rules:
            # 简单通配符匹配
            if rule.endswith('/'):
                # 目录匹配
                if name == rule.rstrip('/'):
                    return True
            elif '*' in rule:
                # 通配符匹配
                import fnmatch
                if fnmatch.fnmatch(name, rule):
                    return True
            else:
                # 精确匹配
                if name == rule:
                    return True
        return False

    def _extract_title(self, filename):
        """从文件名提取标题(去掉版本号、backup等后缀)"""
        name = os.path.splitext(filename)[0]
        # 去掉backup、备份、版本号等后缀
        title = re.sub(r'[_-]*(backup|备份|v\d+|version\d+|old|旧|final|终稿|draft|草稿)', '', name, flags=re.IGNORECASE).strip('_-')
        return title

    def _load_assets(self, dry_run=False):
        """从技能 assets/ 加载模板文件到项目根目录(仅当文件不存在时)，并替换占位符"""
        import inspect
        current_file = os.path.abspath(inspect.getfile(self.__class__))
        skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        assets_dir = os.path.join(skill_dir, "assets")

        if not os.path.exists(assets_dir):
            return []

        loaded = []
        # 加载根目录契约文件
        for filename in ["README.md", "HANDBOOK.md", "TODO.md", "metadata.json"]:
            src = os.path.join(assets_dir, filename)
            dst = os.path.join(self.project_path, filename)
            if os.path.exists(src) and not os.path.exists(dst):
                if not dry_run:
                    with open(src, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # 替换占位符
                    from datetime import datetime
                    today = datetime.now().strftime('%Y-%m-%d')
                    content = content.replace('{项目名称}', self.project_name)
                    content = content.replace('{项目路径}', self.project_path)
                    content = content.replace('{创建日期}', today)
                    content = content.replace('{项目类型，如：博士论文/期刊论文/学位论文}', '论文项目')
                    content = content.replace('{一句话描述}', f'{self.project_name} 论文项目')
                    content = content.replace('{Agent名称}', '大管家')
                    with open(dst, 'w', encoding='utf-8') as f:
                        f.write(content)
                loaded.append(filename)

        # 加载角色模板到项目 .agentsagents/
        agents_src_dir = os.path.join(assets_dir, "agents")
        agents_dst_dir = os.path.join(self.project_path, ".agents", "agents")
        if os.path.exists(agents_src_dir):
            for filename in os.listdir(agents_src_dir):
                if filename.endswith(".md"):
                    src = os.path.join(agents_src_dir, filename)
                    dst = os.path.join(agents_dst_dir, filename)
                    if not os.path.exists(dst):
                        if not dry_run:
                            os.makedirs(agents_dst_dir, exist_ok=True)
                            shutil.copy2(src, dst)
                        loaded.append(f".agentsagents/{filename}")

        return loaded

    def ensure_directories(self, dry_run=False):
        """确保标准目录存在"""
        dirs = {
            "uploads": "uploads/",
            "uploads/markdown": "uploads/markdown/",
            "manuscripts": "manuscripts/",
            "knowledge": "knowledge/",
            "knowledge/note": "knowledge/note/",
            "knowledge/review": "knowledge/review/",
            "knowledge/search_query": "knowledge/search_query/",
            "knowledge/retrieval_report": "knowledge/retrieval_report/",
            "knowledge/topic": "knowledge/topic/",
            "temp": "temp/",
            "references": "references/",
            ".agent": ".agents",
            ".agentsevents": ".agents/events/",
            ".agentsagents": ".agents/agents/",
            ".agentsskills": ".agents/skills/",
            ".agentstasks": ".agents/tasks/",
        }

        created = []
        for dir_name, dir_rel_path in dirs.items():
            dir_path = os.path.join(self.project_path, dir_rel_path)
            if not os.path.exists(dir_path):
                if not dry_run:
                    os.makedirs(dir_path, exist_ok=True)
                created.append(dir_name)
        return created

    def _move_file(self, file_path, target_dir, new_name=None, overwrite=False):
        """
        移动文件到目标目录(私有方法,被organize调用)

        参数:
            file_path: 源文件路径(相对项目根目录或绝对路径)
            target_dir: 目标目录(相对项目根目录)
            new_name: 新文件名(可选)
            overwrite: 是否覆盖已存在文件

        返回:
            目标相对路径,失败返回None
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

        # 如果目标已存在,添加序号
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
        """移动文件到uploads目录"""
        if dry_run:
            return f"{item} -> uploads/"
        target = self._move_file(item_path, "uploads")
        return target if target else None

    def _move_to_manuscripts(self, item, item_path, dry_run=False):
        """移动文件到manuscripts目录"""
        if dry_run:
            return f"{item} -> manuscripts/"
        target = self._move_file(item_path, "manuscripts")
        return target if target else None

    def _move_to_notes(self, item, item_path, dry_run=False):
        """移动文件到knowledge/note目录"""
        if dry_run:
            return f"{item} -> knowledge/note/"
        target = self._move_file(item_path, "knowledge/note")
        return target if target else None

    def _move_to_reviews(self, item, item_path, dry_run=False):
        """移动文件到knowledge/review目录"""
        if dry_run:
            return f"{item} -> knowledge/review/"
        target = self._move_file(item_path, "knowledge/review")
        return target if target else None

    def _move_to_search_queries(self, item, item_path, dry_run=False):
        """移动文件到knowledge/search_query目录"""
        if dry_run:
            return f"{item} -> knowledge/search_query/"
        target = self._move_file(item_path, "knowledge/search_query")
        return target if target else None

    def _move_to_retrieval_report(self, item, item_path, dry_run=False):
        """移动检索报告文件到knowledge/retrieval_report目录"""
        if dry_run:
            return f"{item} -> knowledge/retrieval_report/"
        target = self._move_file(item_path, "knowledge/retrieval_report")
        return target if target else None

    def _move_to_topic_subset(self, item, item_path, dry_run=False):
        """移动topic子集文件到knowledge/topic目录"""
        if dry_run:
            return f"{item} -> knowledge/topic/"
        target = self._move_file(item_path, "knowledge/topic")
        return target if target else None

    def _move_to_extracted_notes(self, item, item_path, dry_run=False):
        """移动提取的笔记文件到knowledge/note目录"""
        if dry_run:
            return f"{item} -> knowledge/note/"
        target = self._move_file(item_path, "knowledge/note")
        return target if target else None

    def _move_to_temp_data(self, item, item_path, dry_run=False):
        """移动文件到temp目录"""
        if dry_run:
            return f"{item} -> temp/"
        target = self._move_file(item_path, "temp")
        return target if target else None

    def _move_directory_contents(self, src_dir, dst_dir, file_filter=None, dry_run=False):
        """
        移动目录内容到目标目录(私有方法,被organize调用)

        参数:
            src_dir: 源目录(相对项目根目录或绝对路径)
            dst_dir: 目标目录(相对项目根目录)
            file_filter: 文件过滤函数(可选)
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
        移动非标准目录文件到标准位置(私有方法,被organize调用)
        处理:knowledge/retrieval_report/、knowledge/review/、审稿意见/、指南uploads/、review/
        """
        results = {
            "moved_to_manuscripts": [],
            "moved_to_reviews": [],
            "moved_to_documents": [],
            "moved_to_knowledge": [],
        }

        # 1. knowledge/retrieval_reports/ -> knowledge/retrieval_report/(保留在知识库,不移动到手稿)
        search_report_dir = os.path.join(self.project_path, "knowledge", "retrieval_reports")
        if os.path.exists(search_report_dir):
            moved = self._move_directory_contents(
                search_report_dir, "knowledge/retrieval_report",
                dry_run=dry_run
            )
            results["moved_to_knowledge"].extend(moved)
            if not dry_run and os.path.exists(search_report_dir):
                try:
                    os.rmdir(search_report_dir)
                    print(f"  ✅ 删除空目录: knowledge/retrieval_reports/")
                except:
                    pass

        # 2. knowledge/review/ -> knowledge/review/
        lit_review_dir = os.path.join(self.project_path, "knowledge", "reviews")
        if os.path.exists(lit_review_dir):
            moved = self._move_directory_contents(
                lit_review_dir, "knowledge/review",
                dry_run=dry_run
            )
            results["moved_to_reviews"].extend(moved)
            if not dry_run and os.path.exists(lit_review_dir):
                try:
                    os.rmdir(lit_review_dir)
                    print(f"  ✅ 删除空目录: knowledge/review/")
                except:
                    pass

        # 3. 审稿意见/ -> manuscripts/
        review_opinion_dir = os.path.join(self.project_path, "审稿意见")
        if os.path.exists(review_opinion_dir):
            moved = self._move_directory_contents(
                review_opinion_dir, "manuscripts",
                dry_run=dry_run
            )
            results["moved_to_manuscripts"].extend(moved)
            if not dry_run and os.path.exists(review_opinion_dir):
                try:
                    os.rmdir(review_opinion_dir)
                    print(f"  ✅ 删除空目录: 审稿意见/")
                except:
                    pass

        # 4. 指南uploads/ -> uploads/
        guide_dir = os.path.join(self.project_path, "指南uploads")
        if os.path.exists(guide_dir):
            moved = self._move_directory_contents(
                guide_dir, "uploads",
                dry_run=dry_run
            )
            results["moved_to_documents"].extend(moved)
            if not dry_run and os.path.exists(guide_dir):
                try:
                    os.rmdir(guide_dir)
                    print(f"  ✅ 删除空目录: 指南uploads/")
                except:
                    pass

        # 5. review/ -> knowledge/review/
        lit_review_root = os.path.join(self.project_path, "reviews")
        if os.path.exists(lit_review_root):
            moved = self._move_directory_contents(
                lit_review_root, "knowledge/review",
                dry_run=dry_run
            )
            results["moved_to_reviews"].extend(moved)
            if not dry_run and os.path.exists(lit_review_root):
                try:
                    os.rmdir(lit_review_root)
                    print(f"  ✅ 删除空目录: review/")
                except:
                    pass

        return results

    def _move_md_from_documents(self, dry_run=False):
        """
        移动uploads目录中的 .md 文件到manuscripts/(私有方法,被organize调用)
        """
        results = []
        doc_dir = os.path.join(self.project_path, "uploads")

        if not os.path.exists(doc_dir):
            return results

        for item in os.listdir(doc_dir):
            if item.endswith('.md'):
                item_path = os.path.join(doc_dir, item)
                if dry_run:
                    results.append(f"{item} -> manuscripts/")
                else:
                    target = self._move_file(item_path, "manuscripts")
                    if target:
                        results.append(target)

        return results

    def _unify_index_filename(self, dry_run=False):
        """
        统一knowledge/note/中的索引文件名(私有方法,被organize调用)
        将 索引.json 重命名为 index.json
        """
        results = []
        notes_dir = os.path.join(self.project_path, "knowledge", "notes")

        if not os.path.exists(notes_dir):
            return results

        for item in os.listdir(notes_dir):
            if item == "索引.json":
                src = os.path.join(notes_dir, item)
                dst = os.path.join(notes_dir, "index.json")
                if not os.path.exists(dst):
                    if dry_run:
                        results.append(f"knowledge/note/索引.json -> index.json")
                    else:
                        try:
                            shutil.move(src, dst)
                            results.append("index.json")
                            print(f"  ✅ 重命名: knowledge/note/索引.json -> index.json")
                        except Exception as e:
                            print(f"  ❌ 重命名失败: {e}")

        return results

    def _remove_nested_project_dir(self, dry_run=False):
        """
        删除嵌套的项目目录(私有方法,被organize调用)
        例如:AI降重提示工程/AI降重提示工程/
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
                print(f"    跳过(已存在): {item}")
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
        删除旧的元数据备份文件(私有方法,被organize调用)
        删除:temp/元数据_1.json、temp/元数据_2.json 等
        """
        results = []
        temp_dir = os.path.join(self.project_path, "temp")

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

    def init(self, dry_run=False):
        """
        项目初始化（委托给父类模板方法，子类多态自动生效）
        """
        # 调用 BaseMaintainer 的模板方法 init()
        # 子类覆盖了 init_post() 和 _get_template_custom_content() 等多态钩子
        return super().init(dry_run=dry_run)

    def init_post(self):
        """特有初始化后置逻辑（子类覆盖）"""
        # BaseMaintainer.init() 末尾会调用此钩子
        pass

    def organize(self, dry_run=False):
        """
        自动整理项目文件（委托给父类模板方法，子类多态自动生效）
        """
        return super().organize(dry_run=dry_run)

    def update_metadata(self, **kwargs):
        """
        更新项目元数据
        """
        current_time = datetime.now().isoformat()
        created_date = self.metadata.get("created_date", datetime.now().strftime("%Y-%m-%d"))

        # 构建目录结构
        directories = {
            "uploads": "uploads/",
            "manuscripts": "manuscripts/",
            "knowledge": "knowledge/",
            "note": "knowledge/note/",
            "review": "knowledge/review/",
            "search_query": "knowledge/search_query/",
            "retrieval_report": "knowledge/retrieval_report/",
            "topic": "knowledge/topic/",
        }

        # 扫描uploads
        documents = []
        doc_dir = os.path.join(self.project_path, "uploads")
        if os.path.exists(doc_dir):
            for filename in os.listdir(doc_dir):
                if not filename.startswith('.'):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in ['.docx', '.pdf', '.txt', '.doc', '.xlsx', '.pptx']:
                        documents.append({
                            "title": os.path.splitext(filename)[0],
                            "version": "v1",
                            "path": f"uploads/{filename}",
                            "type": "user_uploaded"
                        })

        # 扫描manuscripts(markdown文件)
        markdown = {}
        manuscript_dir = os.path.join(self.project_path, "manuscripts")
        if os.path.exists(manuscript_dir):
            for filename in os.listdir(manuscript_dir):
                if filename.endswith('.md'):
                    # 保留现有的 cloud 数据
                    existing_cloud = []
                    if "markdown" in self.metadata and filename in self.metadata["markdown"]:
                        existing_entry = self.metadata["markdown"][filename]
                        if "cloud" in existing_entry:
                            existing_cloud = existing_entry["cloud"]

                    markdown[filename] = {
                        "local_path": f"manuscripts/{filename}",
                        "cloud": existing_cloud
                    }

        # 扫描笔记
        notes = {}
        notes_dir = os.path.join(self.project_path, "knowledge", "notes")
        if os.path.exists(notes_dir):
            for filename in os.listdir(notes_dir):
                if not filename.startswith('.'):
                    notes[filename] = {
                        "local_path": f"knowledge/note/{filename}",
                        "created_at": created_date,
                        "description": ""
                    }

        # 扫描综述
        reviews = {}
        reviews_dir = os.path.join(self.project_path, "knowledge", "reviews")
        if os.path.exists(reviews_dir):
            for filename in os.listdir(reviews_dir):
                if not filename.startswith('.'):
                    reviews[filename] = {
                        "local_path": f"knowledge/review/{filename}"
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
            "note": notes,
            "review": reviews,
            "tags": kwargs.get("tags", self.metadata.get("tags", [])),
            "knowledge_base": {
                "index_file": "knowledge/index.json",
                "description": f"{self.project_name}项目knowledge索引",
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

        # 如果目标已存在,添加序号
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
                        # 如果目标已存在,添加序号
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

    def get_documents(self):
        """获取uploads列表"""
        documents = []
        doc_dir = os.path.join(self.project_path, "uploads")
        if os.path.exists(doc_dir):
            for filename in os.listdir(doc_dir):
                if not filename.startswith('.'):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in ['.docx', '.pdf', '.txt', '.doc', '.xlsx', '.pptx']:
                        documents.append({
                            "title": os.path.splitext(filename)[0],
                            "version": "v1",
                            "path": f"uploads/{filename}",
                            "type": "user_uploaded"
                        })
        return documents

    def get_manuscripts(self):
        """获取manuscripts列表"""
        manuscripts = []
        manuscript_dir = os.path.join(self.project_path, "manuscripts")
        if os.path.exists(manuscript_dir):
            for filename in os.listdir(manuscript_dir):
                if filename.endswith('.md'):
                    manuscripts.append({
                        "title": os.path.splitext(filename)[0],
                        "version": "v1",
                        "path": f"manuscripts/{filename}",
                        "type": "agent_written"
                    })
        return manuscripts


class MetadataManager:
    """元数据管理器 - 不直接编辑文件,通过方法操作"""

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
                print(f"⚠️  读取元数据失败: {e}")
        return {}

    def save(self):
        try:
            self.metadata["updated_at"] = datetime.now().isoformat()
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
    parser.add_argument("--projects-dir", default="/root/data/disk/仓库", help="项目根目录（默认: /root/data/disk/仓库/）")

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 整理命令(默认)
    organize_parser = subparsers.add_parser("organize", help="整理项目文件(默认命令)")
    organize_parser.add_argument("project_path", nargs="?", help="项目路径")
    organize_parser.add_argument("--all", action="store_true", help="整理所有项目")
    organize_parser.add_argument("--dry-run", action="store_true", help="预览模式")
    organize_parser.add_argument("--projects-dir", default="/root/data/disk/仓库", help="项目根目录（默认: /root/data/disk/仓库/）")

    # 模板同步命令
    sync_parser = subparsers.add_parser("sync-templates", help="同步模板文件（保留 PRIVATE 区块）")
    sync_parser.add_argument("project_path", nargs="?", help="项目路径")
    sync_parser.add_argument("--all", action="store_true", help="同步所有项目")
    sync_parser.add_argument("--dry-run", action="store_true", help="预览模式")
    sync_parser.add_argument("--projects-dir", default="/root/data/disk/仓库", help="项目根目录（默认: /root/data/disk/仓库/）")

    # 检查更新命令
    check_parser = subparsers.add_parser("check-updates", help="检查项目文档是否需要更新")
    check_parser.add_argument("project_path", nargs="?", help="项目路径")
    check_parser.add_argument("--all", action="store_true", help="检查所有项目")
    check_parser.add_argument("--projects-dir", default="/root/data/disk/仓库", help="项目根目录（默认: /root/data/disk/仓库/）")

    # 维护命令
    maintain_parser = subparsers.add_parser("maintain", help="维护项目元数据和结构")
    maintain_parser.add_argument("project_path", nargs="?", help="项目路径")
    maintain_parser.add_argument("--all", action="store_true", help="维护所有项目")
    maintain_parser.add_argument("--dry-run", action="store_true", help="预览模式")
    maintain_parser.add_argument("--projects-dir", default="/root/data/disk/仓库", help="项目根目录（默认: /root/data/disk/仓库/）")

    # 移动命令
    move_parser = subparsers.add_parser("move", help="移动文件到标准目录")
    move_parser.add_argument("project_path", help="项目路径")
    move_parser.add_argument("file", help="要移动的文件路径(相对项目根目录)")
    move_parser.add_argument("target", help="目标目录(uploads/manuscripts/knowledge/note/knowledge/review)")
    move_parser.add_argument("--new-name", help="新文件名(可选)")
    move_parser.add_argument("--overwrite", action="store_true", help="覆盖已存在文件")

    # 元数据管理参数
    meta_parser = subparsers.add_parser("meta", help="元数据管理")
    meta_parser.add_argument("project_path", help="项目路径")
    meta_parser.add_argument("--title", help="设置项目标题")
    meta_parser.add_argument("--desc", "--description", help="设置项目描述")
    meta_parser.add_argument("--status", help="设置项目状态")
    meta_parser.add_argument("--version", help="设置版本号")
    meta_parser.add_argument("--tags", help="设置标签(逗号分隔)")
    meta_parser.add_argument("--add-tag", action="append", help="添加标签")
    meta_parser.add_argument("--rm-tag", action="append", help="移除标签")
    meta_parser.add_argument("--set", action="append", help="通用字段设置(KEY=VALUE)")
    meta_parser.add_argument("--show", action="store_true", help="显示当前元数据")
    meta_parser.add_argument("--save", action="store_true", help="显式保存")

    args = parser.parse_args()

    # 如果没有指定命令,默认使用 organize
    if not args.command:
        # 将参数转换为 organize 子命令的参数
        args.command = "organize"
        # 从全局参数获取 project_path
        if not hasattr(args, 'project_path'):
            args.project_path = None

    # 整理模式(默认) — 使用 from_path() 自动路由到正确子类
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
                    maintainer = Maintainer.from_path(project_path)
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
                        print(f"  ✅ 完成,共处理 {total} 个文件")
        else:
            if not args.project_path:
                print("❌ 请指定项目路径或使用 --all")
                sys.exit(1)

            maintainer = Maintainer.from_path(args.project_path)
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
                print(f"\n✅ 完成,共处理 {total} 个文件")
        return

    # 模板同步模式 — 使用 from_path() 自动路由到正确子类
    if args.command == "check-updates":
        from maintainer.BaseMaintainer import BaseMaintainer
        
        projects_dir = os.path.expanduser(args.projects_dir)
        
        if args.all:
            # 检查所有项目
            for name in sorted(os.listdir(projects_dir)):
                proj = os.path.join(projects_dir, name)
                if not os.path.isdir(proj) or name.startswith('.'):
                    continue
                print("\n=== " + name + " ===")
                try:
                    m = BaseMaintainer(proj)
                    updates = m.check_updates()
                    has_updates = False
                    for fname, current, expected, status in updates:
                        if status == 'outdated':
                            print("  📝 " + fname + ": " + current + " → " + expected + " (需要更新)")
                            has_updates = True
                        elif status == 'new':
                            print("  🆕 " + fname + ": " + expected + " (新文件)")
                            has_updates = True
                        else:
                            print("  ✅ " + fname + ": " + current + " (已是最新)")
                    if not updates:
                        print("  无模板文件")
                except Exception as e:
                    print("  ⚠️ 错误: " + str(e))
        elif args.project_path:
            project_path = os.path.expanduser(args.project_path)
            print("\n[检查更新] " + project_path)
            m = BaseMaintainer(project_path)
            updates = m.check_updates()
            has_updates = False
            for fname, current, expected, status in updates:
                if status == 'outdated':
                    print("  📝 " + fname + ": " + current + " → " + expected + " (需要更新)")
                    has_updates = True
                elif status == 'new':
                    print("  🆕 " + fname + ": " + expected + " (新文件)")
                    has_updates = True
                else:
                    print("  ✅ " + fname + ": " + current + " (已是最新)")
        else:
            print("错误: 请指定项目路径或使用 --all")
            sys.exit(1)

    if args.command == "sync-templates":
        if args.all:
            projects_dir = args.projects_dir
            if not os.path.exists(projects_dir):
                print(f"❌ 项目根目录不存在: {projects_dir}")
                sys.exit(1)

            for project_name in os.listdir(projects_dir):
                project_path = os.path.join(projects_dir, project_name)
                if os.path.isdir(project_path) and not project_name.startswith('.'):
                    print(f"\n📁 同步模板: {project_name}")
                    maintainer = Maintainer.from_path(project_path)
                    maintainer.sync_templates(dry_run=args.dry_run)
        else:
            if not args.project_path:
                print("❌ 请指定项目路径或使用 --all")
                sys.exit(1)

            maintainer = Maintainer.from_path(args.project_path)
            maintainer.sync_templates(dry_run=args.dry_run)
        return

    # 维护模式 — 使用 from_path() 自动路由到正确子类
    if args.command == "maintain":
        if args.all:
            projects_dir = args.projects_dir
            if not os.path.exists(projects_dir):
                print(f"❌ 项目根目录不存在: {projects_dir}")
                sys.exit(1)

            for project_name in os.listdir(projects_dir):
                project_path = os.path.join(projects_dir, project_name)
                if os.path.isdir(project_path) and not project_name.startswith('.'):
                    print(f"\n📁 维护项目: {project_name}")
                    maintainer = Maintainer.from_path(project_path)
                    results = maintainer.maintain(dry_run=args.dry_run)
        else:
            if not args.project_path:
                print("❌ 请指定项目路径或使用 --all")
                sys.exit(1)

            maintainer = Maintainer.from_path(args.project_path)
            results = maintainer.maintain(dry_run=args.dry_run)
        return

    # 移动模式 — 使用 Maintainer(project_path) 直接实例（不需要多态）
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
