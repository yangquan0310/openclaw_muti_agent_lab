#!/usr/bin/env python3
"""
CourseMaintainer.py - 课程项目文件整理

OOP设计：子类只定义个性，通过继承自动获得共性
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/steward/skills/manager/scripts')
from maintainer.BaseMaintainer import BaseMaintainer

import os
import shutil
import re
from datetime import datetime


class CourseMaintainer(BaseMaintainer):
    """课程项目文件整理类"""

    # ──────────────────────────────
    # 个性属性
    # ──────────────────────────────
    PROJECT_TYPE = 'course'

    EXTRA_DIRS = [
        'syllabus',
        'chapters',
        'shared',
        'shared/templates',
        'shared/assets',
        'shared/rubrics',
        'archive',
        '.agentsevents',
        '.agentslocks',
        '.agentsskills',
        '.agentsdecisions',
        '.agentstasks',
    ]

    EXTRA_PROTECTED = set()

    # ──────────────────────────────
    # 多态：模板个性化内容
    # ──────────────────────────────
    def _get_template_replacements(self):
        """获取模板占位符替换字典（扩展父类）"""
        base = super()._get_template_replacements()
        base['project_description'] = f'{self.project_name} 课程备课项目'
        return base

    def _get_template_custom_content(self, template_name):
        """
        获取各模板的个性化内容（多态实现）
        返回字典：{title, content}
        """
        if template_name == 'README.md':
            return {'title': '', 'content': self._get_readme_custom_content()}
        elif template_name == 'HANDBOOK.md':
            return {'title': '## 备课流水线', 'content': self._get_skill_custom_content()}
        elif template_name == 'TODO.md':
            return {'title': '', 'content': self._get_todo_custom_content()}
        elif template_name == 'METADATA.json':
            return {'title': '', 'content': self._get_metadata_custom_content()}
        return {'title': '', 'content': ''}

    def _get_readme_custom_content(self):
        """README.md 个性内容"""
        return '''
## 备课流程

```
v1(需求分析) → v2(内容框架) → v3(学术前沿) → v4(课件脚本) → v5(审校) → v6(终稿) → v7(收工)
```
'''

    def _get_skill_custom_content(self):
        """HANDBOOK.md 个性内容"""
        return '''
### 反馈循环
- **v3→v2**：心理学家向教员提修改建议
- **v5→v4**：督导向呈现师提修改建议

---

## Agent 角色速查

| 角色 | 负责阶段 | 核心产出 | 可操作目录 |
|------|----------|----------|-------------|
| 教员 | v1, v2 | 需求分析、内容框架 | `chapters/*/manuscripts/` |
| 心理学家 | v3 | 学术前沿补充 | `chapters/*/knowledge/` |
| 呈现师 | v4, v6 | 课件脚本、编译pptx | `chapters/*/manuscripts/` |
| 督导 | v5 | 审校意见 | 全局（只读） |
| 大管家 | v7 | Git提交、收工 | 全局 |
'''

    def _get_todo_custom_content(self):
        """TODO.md 个性内容"""
        return '''
## 课程项目任务模板

| 任务ID | 章节 | 任务描述 | 负责人 | 状态 | 备注 |
|--------|------|----------|--------|------|------|
| — | ch01 | — | — | pending | — |
'''
    def _get_metadata_custom_content(self):
        """METADATA.json 个性字段"""
        return '''
  "course_code": "",
  "semester": "",
  "chapters": [],'''

    # ──────────────────────────────
    # 迁移逻辑（多态实现）
    # ──────────────────────────────
    CURRENT_SCHEMA_VERSION = "2.0"

    def _migrate_metadata(self, dry_run=False):
        """
        课程项目旧格式 → 新格式迁移
        旧格式常见字段: course_code, semester, chapters[], syllabus 等
        """
        print(f"    [迁移] 课程项目字段迁移")
        if dry_run:
            return "preview"

        backup_path = f"{self.metadata_path}.bak_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copy2(self.metadata_path, backup_path)
        print(f"    [备份] {os.path.basename(backup_path)}")

        old = self.metadata.copy()
        new = self._create_standard_metadata()

        # 课程项目特有迁移
        if "course_code" in old:
            new["course_code"] = old["course_code"]
        if "semester" in old:
            new["semester"] = old["semester"]
        if "chapters" in old:
            new["chapters"] = old["chapters"]
        if "syllabus" in old:
            new["syllabus"] = old["syllabus"]

        # 通用字段迁移
        for key in ["project_id", "title", "created_date", "updated_at",
                    "status", "version", "description", "documents"]:
            if key in old:
                new[key] = old[key]

        new["project_type"] = "course"
        self.metadata = new
        self._save_metadata()
        return "migrated"

    def _get_file_type(self, filename):
        """根据文件名判断文件类型（课程个性）"""
        ext = os.path.splitext(filename)[1].lower()
        name = os.path.splitext(filename)[0].lower()

        # 保护文件
        if any(kw in name for kw in ['保留', 'keep', 'protected']):
            return "protected"

        # 中间文件
        if ext in ['.tmp', '.temp', '.log', '.bak'] or \
           any(kw in name for kw in ['backup', '备份', 'old', '旧']):
            return "intermediate"

        # 课程特有分类
        if any(kw in name for kw in ['大纲', '课标', '进度', '考核', 'syllabus']):
            return "syllabus"
        if any(kw in name for kw in ['模板', 'template']):
            return "template"
        if any(kw in name for kw in ['评分', '量表', 'rubric']):
            return "rubric"
        if re.match(r'ch\d+', name):
            return "chapter"
        if ext in ['.pptx', '.ppt', '.key']:
            return "slides"
        if ext in ['.docx', '.pdf', '.txt', '.xlsx', '.csv']:
            return "upload"
        if ext == '.md':
            return "document"

        return "other"

    def _get_custom_content(self):
        """返回课程项目个性的SKILL内容"""
        return '''
## 备课流水线（v1-v7）

```
v1(需求分析)
   ↓
v2(内容框架) ←── v3(学术前沿补充) 的修改意见
   ↓
v4(课件脚本) ←── v5(审校意见) 的修改意见
   ↓
v6(终稿教案 + 课件编译)
   ↓
v7(Git提交 + 收工)
```

| 轮次 | 主导角色 | 产出 | 说明 |
|------|----------|------|------|
| v1 | 教员 | 需求分析.md | 教学目标、重难点、课时分配 |
| v2 | 教员 | 内容框架.md | 知识框架、知识点清单 |
| v3 | 心理学家 | 学术前沿补充.md | 前沿文献，研究进展 |
| v4 | 呈现师 | 课件脚本.md | 每页内容规划 |
| v5 | 督导 | 审校意见.md | P0/P1/P2问题清单 |
| v6 | 教员+呈现师 | 终稿教案.md + 课件.pptx | 教案整合+课件编译 |
| v7 | 大管家 | Git提交+收工 | — |

---

## 文件归档规范

| 产出类型 | 归档目录 | 说明 |
|----------|----------|------|
| 用户上传原始文档 | `uploads/` | .docx/.pdf/.txt 等 |
| 教学大纲 | `syllabus/` | 课程大纲、进度表、考核方案 |
| 章节备课内容 | `chapters/ch{编号}_{名称}/` | 每章独立工作区 |
| 章节教案 | `chapters/ch{编号}_{名称}/manuscripts/` | .md 格式 |
| 课件模板 | `shared/templates/` | 模板文件 |
| 共享素材 | `shared/assets/` | 图片、视频、字体 |
| 评分标准 | `shared/rubrics/` | 评分量表 |
| 终稿 | `docs/` | 最终版本 |

---

## Agent 角色速查

| 角色 | 负责阶段 | 核心产出 | 可操作目录 |
|------|----------|----------|-------------|
| 教员 | v1, v2 | 需求分析、内容框架 | `chapters/*/manuscripts/` |
| 心理学家 | v3 | 学术前沿补充 | `chapters/*/knowledge/` |
| 呈现师 | v4, v6 | 课件脚本、编译pptx | `chapters/*/manuscripts/` |
| 督导 | v5 | 审校意见 | 全局（只读） |
| 大管家 | v7 | Git提交、收工 | 全局 |
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
            '{project_type}': '课程项目',
        }

        custom_replacements = {
            '{project_description}': f'{self.project_name} 课程备课项目',
            '{custom_section_title}': '## 备课流水线（v1-v7）',
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
        """整理论居项目文件"""
        print(f"\n  [加载模板]")
        loaded = self._load_assets(dry_run)
        for f in loaded:
            print(f"  ✅ 加载模板: {f}")

        print(f"\n  [扫描根目录]")
        ignore_rules = self._load_agentignore()

        for item in os.listdir(self.project_path):
            item_path = os.path.join(self.project_path, item)
            if item.startswith('.') or item in ['uploads', 'syllabus', 'chapters', 'shared', 'archive']:
                continue
            if self._is_ignored(item_path, ignore_rules):
                continue
            if os.path.isfile(item_path):
                file_type = self._get_file_type(item)
                if file_type == "protected":
                    continue
                self._move_to_standard(item, item_path, file_type, dry_run)

    def _move_to_standard(self, item, item_path, file_type, dry_run):
        """根据文件类型移动到标准目录"""
        target_map = {
            "syllabus": "syllabus",
            "chapter": "chapters",
            "upload": "uploads",
            "template": "shared/templates",
            "rubric": "shared/rubrics",
            "slides": "shared/assets",
            "document": "uploads",
        }
        target_dir = target_map.get(file_type, "uploads")
        if dry_run:
            print(f"  移动: {item} -> {target_dir}/")
        else:
            self._move_file(item_path, target_dir)
            print(f"  ✅ 移动: {item} -> {target_dir}/")

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
    parser = argparse.ArgumentParser(description="课程项目文件整理工具")
    parser.add_argument("command", nargs="?", default="organize", help="命令: init, organize")
    parser.add_argument("project_path", nargs="?", help="项目路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()
    if not args.project_path:
        print("用法: python3 CourseMaintainer.py <init|organize> [项目路径] [--dry-run]")
        sys.exit(1)

    maintainer = CourseMaintainer(args.project_path)
    if args.command == 'init':
        maintainer.init(dry_run=args.dry_run)
    elif args.command == 'organize':
        maintainer.organize(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
