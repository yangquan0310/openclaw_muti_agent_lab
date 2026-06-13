#!/usr/bin/env python3
"""
ThesisMaintainer.py - 论文项目文件整理

OOP设计：子类只定义个性，通过继承自动获得共性
- 个性属性：PROJECT_TYPE, EXTRA_DIRS, EXTRA_PROTECTED
- 个性方法：_get_file_type(), _get_custom_content(), _organize_files()
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/steward/skills/manager/scripts')
from maintainer.BaseMaintainer import BaseMaintainer

import os
import shutil
import re
from datetime import datetime


class ThesisMaintainer(BaseMaintainer):
    """论文项目文件整理类"""

    # ──────────────────────────────
    # 个性属性
    # ──────────────────────────────
    PROJECT_TYPE = 'thesis'

    TEAM_AGENTS = [
        'mathematician',
        'physicist',
        'psychologist',
        'writer',
        'reviewer',
        'steward',
    ]

    WORKFLOW_DESC = '''
## 论文工作流

```
开题报告 → 文献综述 → 研究设计 → 数据收集 → 论文撰写 → 审稿修改 → 定稿
```
'''

    AGENTS_TITLE = '## 论文工作流'

    EXTRA_DIRS = [
        'knowledge',
        'knowledge/note',
        'knowledge/review',
        'knowledge/search_query',
        'knowledge/retrieval_report',
        'knowledge/topic',
        'references',
        '.agentsevents',
        '.agentslocks',
        '.agentsskills',
        '.agentsdecisions',
        '.agentstasks',
    ]

    EXTRA_PROTECTED = {'index.json'}

    # ──────────────────────────────
    # 个性方法
    # ──────────────────────────────
    def _get_file_type(self, filename):
        """根据文件名判断文件类型（论文个性）"""
        ext = os.path.splitext(filename)[1].lower()
        name = os.path.splitext(filename)[0].lower()

        # 保护文件
        if filename.lower() == 'index.json':
            return "protected"
        if any(filename.lower() == (p + ext).lower() for p in ['readme', 'config', 'metadata', 'skill', 'todo', 'agentignore']):
            return "protected"
        if ext in ['.py', '.sh', '.yaml', '.yml', '.toml', '.ini']:
            return "protected"
        if any(kw in name for kw in ['保留', 'keep', 'protected']):
            return "protected"

        # 中间文件
        if ext in ['.tmp', '.temp', '.log', '.bak'] or \
           any(kw in name for kw in ['backup', '备份', 'old', '旧']):
            return "intermediate"

        # 论文特有文件分类
        if ext == '.json' and '检索' in name:
            return "search_query"
        if '笔记' in name and '提取' in name:
            return "extracted_note"
        if '综述' in name or 'review' in name:
            return "review"
        if ext == '.md' and '检索报告' in name:
            return "retrieval_report"
        if ext == '.json' and filename != 'index.json':
            return "topic_subset"
        if '笔记' in name:
            return "note"
        if ext in ['.docx', '.pdf', '.txt', '.doc', '.xlsx', '.pptx']:
            return "user_uploaded"
        if ext == '.md':
            return "agent_written"

        return "other"

    def _get_template_replacements(self):
        """获取模板占位符替换字典（扩展父类）"""
        base = super()._get_template_replacements()
        base['project_description'] = f'{self.project_name} 论文项目'
        return base

    def _get_skill_custom_content(self):
        """AGENTS.md 个性内容"""
        return '''
### 双分支策略

| 分支 | 用途 | 推送时机 |
|------|------|---------|
| `main` | 稳定版本，已完成的论文/章节 | **完成整体任务时** |
| `development` | 日常写作，章节修改中 | **完成阶段子任务时** |

### Commit Message 格式

```
ch{两位数字} v{轮次}: {简要说明}
```

---

## 文件归档规范

| 产出类型 | 归档目录 | 说明 |
|----------|----------|------|
| 用户上传原始文档 | `uploads/` | .docx/.pdf/.txt 等 |
| 手稿最新版 | `manuscripts/{标题}/` | .md 格式论文正文 |
| 知识库笔记 | `knowledge/note/` | 笔记、提取类文档 |
| 文献综述 | `knowledge/review/` | 综述、review 类文档 |
| 检索条件 | `knowledge/search_query/` | .json 格式检索条件 |
| 检索报告 | `knowledge/retrieval_report/` | 文献检索结果报告 |
| 主题/话题文件 | `knowledge/topic/` | 除 index.json 外的 .json 文件 |
| 终稿 | `docs/` | 最终版本 |
| 中间文件 | `temp/` | .tmp/.temp/.log、实验脚本 |

---

## Agent 角色速查

| 角色 | 核心职责 | 可操作目录 |
|------|----------|-------------|
| 大管家 | 整理目录，维护元数据、归档版本 | 全局 |
| 心理学家 | 文献检索、理论分析、实验设计 | `knowledge/*` |
| 写作助手 | 整合综述、撰写草稿、修改论文 | `manuscripts/` |
| 审稿助手 | 8维度审核、输出审稿意见 | `manuscripts/`（只读） |
| 数学家 | 数学建模、公式推导、统计分析 | `knowledge/*` |
| 物理学家 | 物理文献检索、理论推导、实验方案 | `knowledge/*` |
'''

    def _get_todo_custom_content(self):
        """TODO.md 个性内容"""
        return '''
## 论文项目任务模板

| 任务ID | 任务描述 | 负责人 | 状态 | 备注 |
|--------|----------|--------|------|------|
| — | — | — | pending | — |
'''

    def _get_metadata_custom_content(self):
        """METADATA.json 个性字段"""
        return '''
  "project_id": "{project_id}",
  "paper_type": "学术论文",
  "chapter_count": 0,
  "documents": []'''

    # ──────────────────────────────
    # 迁移逻辑（多态实现）
    # ──────────────────────────────
    CURRENT_SCHEMA_VERSION = "2.0"

    def _migrate_metadata(self, dry_run=False):
        """
        论文项目旧格式 → 新格式迁移
        旧格式常见字段: project_name, type, chapters[], paper_type 等
        """
        print(f"    [迁移] 论文项目字段迁移")
        if dry_run:
            return "preview"

        # 备份旧文件
        backup_path = f"{self.metadata_path}.bak_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copy2(self.metadata_path, backup_path)
        print(f"    [备份] {os.path.basename(backup_path)}")

        old = self.metadata.copy()
        new = self._create_standard_metadata()

        # 论文项目特有迁移
        # 旧字段: project_name -> project_id
        if "project_name" in old and "project_id" not in old:
            new["project_id"] = old["project_name"]
        # 旧字段: type -> paper_type
        if "type" in old:
            new["paper_type"] = old["type"]
        # 旧字段: chapters -> chapters
        if "chapters" in old:
            new["chapters"] = old["chapters"]
        # 旧字段: 文献检索信息
        if "search_queries" in old:
            new["search_queries"] = old["search_queries"]

        # 通用字段迁移
        for key in ["project_id", "title", "created_date", "updated_at",
                    "status", "version", "description", "documents",
                    "manuscripts", "notes", "directories"]:
            if key in old:
                new[key] = old[key]

        new["project_type"] = "thesis"
        self.metadata = new
        self._save_metadata()
        return "migrated"

    def _load_assets(self, dry_run=False):
        """加载角色模板到项目目录"""
        import inspect
        current_file = os.path.abspath(inspect.getfile(self.__class__))
        skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        assets_dir = os.path.join(skill_dir, "assets")

        if not os.path.exists(assets_dir):
            return []


        loaded = []

        # 加载角色模板到 .agents/agents/
        agents_src = os.path.join(assets_dir, "agents")
        agents_dst = os.path.join(self.project_path, ".agents", "agents")
        if os.path.exists(agents_src):
            for filename in os.listdir(agents_src):
                if filename.endswith(".md"):
                    src = os.path.join(agents_src, filename)
                    dst = os.path.join(agents_dst, filename)
                    if not os.path.exists(dst):
                        if not dry_run:
                            os.makedirs(agents_dst, exist_ok=True)
                            shutil.copy2(src, dst)
                        loaded.append(f".agents/agents/{filename}")

        return loaded

    def init_post(self):
        """初始化后的特有逻辑"""
        self._load_assets()

    def _organize_files(self, dry_run=False):
        """整理论文项目文件"""
        results = {
            "moved": [],
            "deleted": [],
            "renamed": [],
        }

        # 加载模板
        print(f"\n  [加载模板]")
        loaded = self._load_assets(dry_run)
        for f in loaded:
            print(f"  ✅ 加载模板: {f}")

        # 删除嵌套目录
        self._remove_nested_dir(dry_run)

        # 删除旧元数据备份
        self._remove_old_backups(dry_run)

        # 移动非标准目录
        self._move_nonstandard_dirs(dry_run)

        # 扫描根目录文件
        print(f"\n  [扫描根目录]")
        for item in os.listdir(self.project_path):
            item_path = os.path.join(self.project_path, item)
            if item.startswith('.') or item in ["uploads", "manuscripts", "knowledge", "temp", "metadata.json", ".agentignore"]:
                continue
            if os.path.isfile(item_path):
                file_type = self._get_file_type(item)
                if file_type == "protected":
                    continue
                target = self._move_file_to_standard(item, item_path, file_type, dry_run)
                if target:
                    results["moved"].append(target)

        # 扫描knowledge目录
        self._organize_knowledge_dir(dry_run)

        print(f"\n  [整理完成]")
        return results

    def _move_file_to_standard(self, item, item_path, file_type, dry_run):
        """根据文件类型移动到标准目录"""
        target_map = {
            "user_uploaded": "uploads",
            "agent_written": "manuscripts",
            "intermediate": "temp",
            "search_query": "knowledge/search_query",
            "extracted_note": "knowledge/note",
            "review": "knowledge/review",
            "retrieval_report": "knowledge/retrieval_report",
            "topic_subset": "knowledge/topic",
            "note": "knowledge/note",
        }
        target_dir = target_map.get(file_type, "temp")
        if dry_run:
            return f"{item} -> {target_dir}/"
        return self._move_file(item_path, target_dir)

    def _organize_knowledge_dir(self, dry_run):
        """整理knowledge目录"""
        kb_dir = os.path.join(self.project_path, "knowledge")
        if not os.path.exists(kb_dir):
            return

        for item in os.listdir(kb_dir):
            item_path = os.path.join(kb_dir, item)
            if os.path.isdir(item_path) or item.startswith('.'):
                continue
            if item.lower() in ['index.json', 'config.json', 'metadata.json']:
                continue
            file_type = self._get_file_type(item)
            self._move_file_to_standard(item, item_path, file_type, dry_run)

    def _remove_nested_dir(self, dry_run):
        """删除嵌套的项目目录"""
        nested = os.path.join(self.project_path, self.project_name)
        if not os.path.exists(nested) or not os.path.isdir(nested):
            return

        for item in os.listdir(nested):
            src = os.path.join(nested, item)
            dst = os.path.join(self.project_path, item)
            if os.path.exists(dst):
                print(f"  ⏭️  跳过(已存在): {item}")
                continue
            if dry_run:
                print(f"  移动: {self.project_name}/{item} -> {item}")
            else:
                shutil.move(src, dst)
                print(f"  ✅ 移动: {item} -> 根目录")

        if not dry_run:
            try:
                os.rmdir(nested)
                print(f"  ✅ 删除嵌套目录: {self.project_name}/")
            except Exception:
                pass

    def _remove_old_backups(self, dry_run):
        """删除旧元数据备份"""
        temp_dir = os.path.join(self.project_path, "temp")
        if not os.path.exists(temp_dir):
            return

        for item in os.listdir(temp_dir):
            if item.startswith("元数据_") and item.endswith(".json"):
                item_path = os.path.join(temp_dir, item)
                if dry_run:
                    print(f"  删除: {item}")
                else:
                    try:
                        os.remove(item_path)
                        print(f"  ✅ 删除旧备份: {item}")
                    except Exception:
                        pass

    def _move_nonstandard_dirs(self, dry_run):
        """移动非标准目录内容"""
        # knowledge/retrieval_reports/ -> knowledge/retrieval_report/
        self._merge_dir("knowledge/retrieval_reports", "knowledge/retrieval_report", dry_run)
        # knowledge/reviews/ -> knowledge/review/
        self._merge_dir("knowledge/reviews", "knowledge/review", dry_run)
        # 审稿意见/ -> manuscripts/
        self._merge_dir("审稿意见", "manuscripts", dry_run)
        # 终稿/ -> manuscripts/
        self._merge_dir("终稿", "manuscripts", dry_run)

    def _merge_dir(self, src, dst, dry_run):
        """合并目录内容"""
        src_path = os.path.join(self.project_path, src)
        if not os.path.exists(src_path):
            return

        dst_path = os.path.join(self.project_path, dst)
        os.makedirs(dst_path, exist_ok=True)

        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            if os.path.isfile(src_item) and not item.startswith('.'):
                dst_item = os.path.join(dst_path, item)
                if os.path.exists(dst_item):
                    name, ext = os.path.splitext(item)
                    counter = 1
                    while os.path.exists(dst_item):
                        dst_item = os.path.join(dst_path, f"{name}_{counter}{ext}")
                        counter += 1
                if dry_run:
                    print(f"  移动: {src}/{item} -> {dst}/")
                else:
                    shutil.move(src_item, dst_item)
                    print(f"  ✅ 移动: {item}")

        if not dry_run:
            try:
                os.rmdir(src_path)
                print(f"  ✅ 删除空目录: {src}/")
            except Exception:
                pass

    def _update_metadata(self):
        """更新项目元数据"""
        current_time = datetime.now().isoformat()
        created_date = self.metadata.get("created_date", datetime.now().strftime("%Y-%m-%d"))

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

        self.metadata = {
            "project_id": self.project_name,
            "title": self.metadata.get("title", self.project_name),
            "created_date": created_date,
            "status": self.metadata.get("status", "active"),
            "version": self.metadata.get("version", "v1"),
            "description": self.metadata.get("description", f"{self.project_name}项目"),
            "directories": directories,
            "documents": documents,
            "updated_at": current_time,
        }
        self._save_metadata()


def main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description="论文项目文件整理工具")
    parser.add_argument("command", nargs="?", default="organize", help="命令: init, organize")
    parser.add_argument("project_path", nargs="?", help="项目路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()

    if not args.project_path:
        print("用法: python3 ThesisMaintainer.py <init|organize> [项目路径] [--dry-run]")
        sys.exit(1)

    maintainer = ThesisMaintainer(args.project_path)

    if args.command == 'init':
        maintainer.init(dry_run=args.dry_run)
    elif args.command == 'organize':
        maintainer.organize(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
