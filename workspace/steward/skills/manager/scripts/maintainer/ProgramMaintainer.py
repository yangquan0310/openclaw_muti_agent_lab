#!/usr/bin/env python3
"""
ProgramMaintainer.py - 程序项目文件整理

OOP设计：子类只定义个性，通过继承自动获得共性
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/steward/skills/manager/scripts')
from maintainer.BaseMaintainer import BaseMaintainer

import os
import shutil
import re
from datetime import datetime


class ProgramMaintainer(BaseMaintainer):
    """程序项目文件整理类"""

    # ──────────────────────────────
    # 个性属性
    # ──────────────────────────────
    PROJECT_TYPE = 'program'

    EXTRA_DIRS = [
        'agents',
        'src',
        'test',
        '.agentsskills',
        'docs',
        'docs/roadmap',
        'docs/changelog',
        'docs/reference',
        'docs/reports',
        'docs/cases',
        'logs',
        'temp',
        'temp/draft',
    ]

    EXTRA_PROTECTED = {
        'package.json',
        'openclaw.plugin.json',
    }

    # ──────────────────────────────
    # 多态：模板个性化内容
    # ──────────────────────────────
    def _get_template_replacements(self):
        """获取模板占位符替换字典（扩展父类）"""
        base = super()._get_template_replacements()
        base['project_description'] = f'{self.project_name} 程序开发项目'
        return base

    def _get_template_custom_content(self, template_name):
        """
        获取各模板的个性化内容（多态实现）
        返回字典：{title, content}
        """
        if template_name == 'README.md':
            return {'title': '', 'content': self._get_readme_custom_content()}
        elif template_name == 'HANDBOOK.md':
            return {'title': '## 程序开发流程', 'content': self._get_skill_custom_content()}
        elif template_name == 'TODO.md':
            return {'title': '', 'content': self._get_todo_custom_content()}
        elif template_name == 'METADATA.json':
            return {'title': '', 'content': self._get_metadata_custom_content()}
        return {'title': '', 'content': ''}

    def _get_readme_custom_content(self):
        """README.md 个性内容"""
        return '''
## 开发流程

```
需求分析 → 设计 → 编码 → 测试 → 部署
```
'''

    def _get_skill_custom_content(self):
        """HANDBOOK.md 个性内容"""
        return '''
### Agent 角色

| 角色 | 职责 | 可操作目录 |
|------|------|-----------|
| 产品经理 | 需求分析、原型设计 | 全局 |
| 开发者 | 编码实现 | `src/`, `test/` |
| 审核 | 代码审查、合规检查 | 全局（只读） |

---

## 文件归档规范

| 产出类型 | 归档目录 |
|----------|----------|
| 源代码 | `src/` |
| 测试代码 | `test/` |
| 文档 | `docs/` |
| 日志 | `logs/` |
| 临时文件 | `temp/` |
'''
    def _get_todo_custom_content(self):
        """TODO.md 个性内容"""
        return '''
## 程序项目任务模板

| 任务ID | 模块 | 任务描述 | 负责人 | 状态 | 备注 |
|--------|------|----------|--------|------|------|
| — | — | — | — | pending | — |
'''
    def _get_metadata_custom_content(self):
        """METADATA.json 个性字段"""
        return '''
  "language": "",
  "framework": "",
  "modules": [],'''

    # ──────────────────────────────
    # 迁移逻辑（多态实现）
    # ──────────────────────────────
    CURRENT_SCHEMA_VERSION = "2.0"

    def _migrate_metadata(self, dry_run=False):
        """
        程序项目旧格式 → 新格式迁移
        旧格式常见字段: language, framework, modules[], package 等
        """
        print(f"    [迁移] 程序项目字段迁移")
        if dry_run:
            return "preview"

        backup_path = f"{self.metadata_path}.bak_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copy2(self.metadata_path, backup_path)
        print(f"    [备份] {os.path.basename(backup_path)}")

        old = self.metadata.copy()
        new = self._create_standard_metadata()

        # 程序项目特有迁移
        if "language" in old:
            new["language"] = old["language"]
        if "framework" in old:
            new["framework"] = old["framework"]
        if "modules" in old:
            new["modules"] = old["modules"]
        if "package" in old:
            new["package"] = old["package"]

        # 通用字段迁移
        for key in ["project_id", "title", "created_date", "updated_at",
                    "status", "version", "description", "documents"]:
            if key in old:
                new[key] = old[key]

        new["project_type"] = "program"
        self.metadata = new
        self._save_metadata()
        return "migrated"

    def _get_file_type(self, filename):
        """根据文件名判断文件类型（程序个性）"""
        ext = os.path.splitext(filename)[1].lower()
        name = os.path.splitext(filename)[0].lower()

        # 保护文件（包括 EXTRA_PROTECTED）
        if self._is_protected_file(filename):
            return "protected"
        if any(kw in name for kw in ['保留', 'keep', 'protected']):
            return "protected"

        # 中间文件
        if ext in ['.tmp', '.temp', '.log', '.bak'] or \
           any(kw in name for kw in ['backup', '备份', 'old', '旧']):
            return "intermediate"

        # 程序特有分类
        if ext in ['.js', '.ts', '.py', '.java', '.cpp', '.c', '.go', '.rs']:
            return "source"
        if ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.config']:
            return "config"
        if ext in ['.md', '.txt', '.rst']:
            return "document"
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico']:
            return "image"
        if ext in ['.zip', '.tar', '.gz', '.rar']:
            return "archive"
        if ext in ['.docx', '.pdf', '.txt', '.xlsx', '.pptx']:
            return "upload"

        return "other"

    def _get_custom_content(self):
        """返回程序项目个性的SKILL内容"""
        return '''
## 程序开发流程

```
需求分析 → 设计 → 编码 → 测试 → 部署
```

### Agent 角色

| 角色 | 职责 | 可操作目录 |
|------|------|-----------|
| 产品经理 | 需求分析、原型设计 | 全局 |
| 开发者 | 编码实现 | `src/`, `test/` |
| 审核 | 代码审查、合规检查 | 全局（只读） |

---

## 文件归档规范

| 产出类型 | 归档目录 | 说明 |
|----------|----------|------|
| 用户上传原始文档 | `uploads/` | .docx/.pdf/.txt 等 |
| 源代码 | `src/` | .py, .js 等 |
| 测试代码 | `test/` | 测试文件 |
| 文档 | `docs/` | README、API文档 |
| 配置文件 | 项目根目录 | package.json等 |
| 日志 | `logs/` | .log 文件 |
| 临时文件 | `temp/` | 中间产物 |
'''

    def _load_assets(self, dry_run=False):
        """加载模板到项目目录"""
        import inspect
        current_file = os.path.abspath(inspect.getfile(self.__class__))
        skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        assets_dir = os.path.join(skill_dir, "assets")
        template_dir = os.path.join(skill_dir, "assets", "project-level")

        if not os.path.exists(assets_dir):
            return []

        loaded = []
        today = datetime.now().strftime('%Y-%m-%d')

        base_replacements = {
            '{project_name}': self.project_name,
            '{project_path}': self.project_path,
            '{created_at}': today,
            '{project_type}': '程序项目',
        }

        custom_replacements = {
            '{project_description}': f'{self.project_name} 程序开发项目',
            '{custom_section_title}': '## 程序开发流程',
            '{custom_section_content}': self._get_custom_content(),
        }

        replacements = {**base_replacements, **custom_replacements}

        for template_name, target_name in [("README", "README.md"), ("HANDBOOK", "HANDBOOK.md")]:
            template_file = f"{template_name}.template"
            src = os.path.join(template_dir, template_file)
            dst = os.path.join(self.project_path, target_name)
            if os.path.exists(src) and not os.path.exists(dst):
                if not dry_run:
                    with open(src, 'r', encoding='utf-8') as f:
                        content = f.read()
                    for placeholder, value in replacements.items():
                        content = content.replace(placeholder, value)
                    with open(dst, 'w', encoding='utf-8') as f:
                        f.write(content)
                loaded.append(target_name)

        # 加载角色模板
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
                        loaded.append(f".agentsagents/{filename}")

        return loaded

    def init_post(self):
        """初始化后的特有逻辑"""
        self._load_assets()

    def _organize_files(self, dry_run=False):
        """整理程序项目文件"""
        results = {
            "moved": [],
            "deleted": [],
            "renamed": [],
        }

        print(f"\n  [加载模板]")
        loaded = self._load_assets(dry_run)
        for f in loaded:
            print(f"  ✅ 加载模板: {f}")

        print(f"\n  [扫描根目录]")
        ignore_rules = self._load_agentignore()

        for item in os.listdir(self.project_path):
            item_path = os.path.join(self.project_path, item)
            if item.startswith('.') or item in ['uploads', 'src', 'test', 'docs', 'logs', 'temp']:
                continue
            if self._is_ignored(item_path, ignore_rules):
                continue
            if os.path.isfile(item_path):
                file_type = self._get_file_type(item)
                if file_type == "protected":
                    continue
                target = self._move_to_standard(item, item_path, file_type, dry_run)
                if target:
                    results["moved"].append(target)

        return results

    def _move_to_standard(self, item, item_path, file_type, dry_run):
        """根据文件类型移动到标准目录"""
        target_map = {
            "source": "src",
            "config": "src",
            "document": "docs",
            "image": "docs",
            "archive": "temp",
            "upload": "uploads",
        }
        target_dir = target_map.get(file_type, "temp")
        if dry_run:
            print(f"  移动: {item} -> {target_dir}/")
            return f"{item} -> {target_dir}/"
        else:
            self._move_file(item_path, target_dir)
            print(f"  ✅ 移动: {item} -> {target_dir}/")
            return f"{item} -> {target_dir}/"

    def _load_agentignore(self):
        """加载 .agentignore 规则"""
        agentignore_path = os.path.join(self.project_path, '.agentignore')
        if not os.path.exists(agentignore_path):
            return []
        rules = []
        with open(agentignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    rules.append(line)
        return rules

    def _is_ignored(self, filepath, rules):
        """检查是否被 .agentignore 忽略"""
        import fnmatch
        rel_path = os.path.relpath(filepath, self.project_path)
        for rule in rules:
            if fnmatch.fnmatch(rel_path, rule) or fnmatch.fnmatch(os.path.basename(rel_path), rule):
                return True
        return False


def main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description="程序项目文件整理工具")
    parser.add_argument("command", nargs="?", default="organize", help="命令: init, organize")
    parser.add_argument("project_path", nargs="?", help="项目路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()
    if not args.project_path:
        print("用法: python3 ProgramMaintainer.py <init|organize> [项目路径] [--dry-run]")
        sys.exit(1)

    maintainer = ProgramMaintainer(args.project_path)
    if args.command == 'init':
        maintainer.init(dry_run=args.dry_run)
    elif args.command == 'organize':
        maintainer.organize(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
