#!/usr/bin/env python3
"""
BaseMaintainer.py - 通用项目管理基础类

OOP设计：
- 封装：共性功能在父类
- 继承：子类自动获得共性
- 多态：子类通过覆盖属性和方法钩子实现个性

子类通过覆盖以下属性/方法实现扩展：
- PROJECT_TYPE: 项目类型（必须定义）
- EXTRA_DIRS: 追加的标准目录列表
- EXTRA_PROTECTED: 追加的保护文件集合
- INIT_TEMPLATES: 初始化时加载的模板列表
- EXTRA_TEMPLATE_DIRS: 追加的模板搜索路径
- init_post(): 初始化后的特有逻辑
- _get_file_type(): 判断文件类型（默认返回"other"）
- _get_custom_content(): 获取个性的SKILL内容
"""

import os
import sys
import json
import shutil
import re
import fnmatch
from datetime import datetime
from pathlib import Path


class BaseMaintainer:
    """通用项目管理基础类"""

    # ──────────────────────────────
    # GENERATED / PRIVATE 标记区块（模板安全更新机制）
    # ──────────────────────────────
    # 共性内容区（模板更新时整体替换）
    GENERATED_START = "<!-- GENERATED_START -->"
    GENERATED_END = "<!-- GENERATED_END -->"
    # 私有内容区（模板更新时保留）
    PRIVATE_START = "<!-- PRIVATE_START -->"
    PRIVATE_END = "<!-- PRIVATE_END -->"

    # 需要同步的模板文件列表（子类可追加）
    SYNC_TEMPLATES = ['README.md', 'AGENTS.md', 'TODO.md']

    # ──────────────────────────────
    # 工厂方法（多态入口）
    # ──────────────────────────────
    @classmethod
    def from_path(cls, project_path):
        """
        工厂方法：根据项目路径自动创建对应子类的实例
        读取 metadata.json 的 project_type，路由到正确的子类
        """
        import os
        project_path = os.path.expanduser(project_path)
        metadata_path = os.path.join(project_path, "metadata.json")
        project_type = None

        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        project_type = data.get("project_type")
            except Exception:
                pass

        # 动态导入子类（避免循环导入）
        if project_type:
            from .ThesisMaintainer import ThesisMaintainer
            from .ProgramMaintainer import ProgramMaintainer
            subclass_map = {
                "thesis": ThesisMaintainer,
                "program": ProgramMaintainer,
            }
            if project_type in subclass_map:
                subclass_cls = subclass_map[project_type]
                if subclass_cls and subclass_cls is not cls:
                    return subclass_cls(project_path)

        # 无 metadata 或未知类型：返回当前类实例
        return cls(project_path)

    # ──────────────────────────────
    # 共性属性（所有项目通用）
    # ──────────────────────────────
    BASE_DIRS = [
        'uploads',
        'uploads/markdown',
        'manuscripts',
        'temp',
        '.agents',
        '.agentsagents',
    ]

    BASE_PROTECTED = {
        'README.md', 'AGENTS.md', 'TODO.md', 'metadata.json',
        '.agentignore', '.gitignore'
    }

    # ──────────────────────────────
    # 抽象属性（子类必须定义）
    # ──────────────────────────────
    PROJECT_TYPE = None  # 子类必须定义，如 'thesis', 'course', 'program'
    EXTRA_DIRS = []     # 子类追加的标准目录
    EXTRA_PROTECTED = set()  # 子类追加的保护文件

    # 初始化时加载的模板列表（子类可追加）
    INIT_TEMPLATES = ['README.md', 'AGENTS.md', 'TODO.md', 'METADATA.json']
    EXTRA_TEMPLATE_DIRS = []

    # ──────────────────────────────
    # 属性合并（计算属性）
    # ──────────────────────────────
    @property
    def STANDARD_DIRS(self):
        """合并后的标准目录列表"""
        return self.BASE_DIRS + self.EXTRA_DIRS

    @property
    def PROTECTED_FILES(self):
        """合并后的保护文件集合"""
        return self.BASE_PROTECTED | self.EXTRA_PROTECTED

    # ──────────────────────────────
    # 初始化
    # ──────────────────────────────
    def __init__(self, project_path):
        """
        初始化项目
        :param project_path: 项目文件夹路径。支持：
          - 绝对路径: /home/user/仓库/项目名
          - 相对路径(含/): 仓库/项目名
          - 仅项目名: 项目名 → 自动解析为 ~/.openclaw/repository/项目名
        """
        raw_path = project_path.strip()
        if '/' not in raw_path and '\\' not in raw_path:
            raw_path = os.path.join(os.path.expanduser('~/.openclaw/repository'), raw_path)
        self.project_path = os.path.expanduser(raw_path)
        self.project_name = os.path.basename(os.path.normpath(self.project_path))
        self.metadata_path = os.path.join(self.project_path, "metadata.json")
        self.metadata = self._load_metadata()

    # ──────────────────────────────
    # 元数据管理（封装的共性）
    # ──────────────────────────────
    def _load_metadata(self):
        """加载现有元数据"""
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except Exception:
                pass
        return {}

    def _save_metadata(self):
        """保存元数据到文件"""
        try:
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            os.chmod(self.metadata_path, 0o644)
            return True
        except Exception as e:
            print(f"[错误] 保存元数据失败: {e}")
            return False

    # ──────────────────────────────
    # 保护文件判断（封装的共性）
    # ──────────────────────────────
    def _is_protected(self, filename):
        """判断文件是否受保护"""
        return filename in self.PROTECTED_FILES

    def _is_ignored(self, filepath):
        """检查文件是否被 .agentignore 忽略"""
        agentignore_path = os.path.join(self.project_path, '.agentignore')
        if not os.path.exists(agentignore_path):
            return False
        try:
            with open(agentignore_path, 'r', encoding='utf-8') as f:
                patterns = [line.strip() for line in f
                            if line.strip() and not line.startswith('#')]
            rel_path = os.path.relpath(filepath, self.project_path)
            for pattern in patterns:
                pattern_re = pattern.replace('.', r'\.'
                    ).replace('*', '.*').replace('?', '.')
                if (re.search(pattern_re, rel_path) or
                        re.search(pattern_re, os.path.basename(rel_path))):
                    return True
            return False
        except Exception:
            return False

    # ──────────────────────────────
    # 目录管理（封装的共性）
    # ──────────────────────────────
    def _create_directories(self):
        """创建标准目录，返回创建的目录列表"""
        created = []
        for dir_name in self.STANDARD_DIRS:
            dir_path = os.path.join(self.project_path, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                created.append(dir_name)
        return created

    # ──────────────────────────────
    # Git 初始化（封装的共性）
    # ──────────────────────────────
    def _init_git_repo(self):
        """初始化 Git 仓库并首次提交"""
        git_dir = os.path.join(self.project_path, '.git')
        if os.path.exists(git_dir):
            print("[信息] Git 仓库已存在，跳过初始化")
            return True
        try:
            import subprocess
            subprocess.run(['git', 'init'], cwd=self.project_path,
                           capture_output=True, check=True)
            gitignore = os.path.join(self.project_path, '.gitignore')
            if not os.path.exists(gitignore):
                with open(gitignore, 'w', encoding='utf-8') as f:
                    f.write("*.tmp\n*.temp\n*.log\n*.bak\n")
                print("[信息] 创建 .gitignore")
            subprocess.run(['git', 'add', '.'], cwd=self.project_path,
                           capture_output=True, check=True)
            subprocess.run(['git', 'commit', '-m', 'init: 项目初始化'],
                           cwd=self.project_path, capture_output=True, check=True)
            print("[信息] Git 仓库初始化完成")
            return True
        except Exception as e:
            print(f"[警告] Git 初始化失败: {e}")
            return False

    # ──────────────────────────────
    # 模板加载（封装的共性 + 子类覆盖）
    # ──────────────────────────────
    def _get_template_search_paths(self):
        """模板搜索路径：EXTRA → 子技能 → 父技能"""
        for extra_dir in self.EXTRA_TEMPLATE_DIRS:
            if os.path.exists(extra_dir):
                yield extra_dir
        child_dir = self._infer_child_template_dir()
        if child_dir and os.path.exists(child_dir):
            yield child_dir
        parent_dir = self._get_parent_template_dir()
        if parent_dir and os.path.exists(parent_dir):
            yield parent_dir

    def _infer_child_template_dir(self):
        """推断子技能模板目录"""
        module_file = sys.modules[self.__class__.__module__].__file__
        skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(module_file))))
        child_dir = os.path.join(skill_dir, 'assets', 'templates')
        parent_dir = self._get_parent_template_dir()
        if child_dir == parent_dir:
            return None
        return child_dir

    def _get_parent_template_dir(self):
        """父技能模板目录（统一模板在 project-level/）"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base_dir, 'assets', 'project-level')

    def _load_template_content(self, template_name):
        """加载模板内容"""
        for search_dir in self._get_template_search_paths():
            # 尝试 .template 后缀
            template_file = f"{template_name}.template"
            template_path = os.path.join(search_dir, template_file)
            if os.path.exists(template_path):
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception:
                    pass
            # 尝试直接 .template.json 后缀（用于 JSON 模板）
            template_file = f"{template_name}.template.json"
            template_path = os.path.join(search_dir, template_file)
            if os.path.exists(template_path):
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception:
                    pass
        return None

    # 子类可覆盖的标签映射
    TEMPLATE_LABELS = {
        'thesis': '论文项目',
        'course': '课程项目',
        'program': '程序项目',
    }

    # 子类可覆盖的角色列表（决定 README 分工表格显示哪些 Agent）
    TEAM_AGENTS = []
    WORKFLOW_DESC = ''  # 子类覆盖：README 的工作流描述
    AGENTS_TITLE = ''  # 子类覆盖：AGENTS 的标题

    def _generate_team_division_table(self):
        """从 assets/agents/ 目录解析角色文件，生成团队分工表格"""
        skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        agents_dir = os.path.join(skill_dir, 'assets', 'agents')

        lines = ['## 团队分工\n', '| 角色 | 核心职责 | 适用项目 |', '|------|----------|---------|']
        for agent in self.TEAM_AGENTS:
            agent_path = os.path.join(agents_dir, f'{agent}.md')
            if os.path.exists(agent_path):
                with open(agent_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 解析角色名（第一行 # xxx（xxx））
                name_cn = ''
                first_line = content.split('\n')[0].strip()
                if first_line.startswith('#'):
                    parts = first_line.lstrip('#').strip().split('（')
                    if len(parts) == 2:
                        name_cn = parts[0].strip()

                # 解析角色定位（从 blockquote）
                role_desc = ''
                for line in content.split('\n')[:10]:
                    if line.startswith('>') and '角色定位' in line:
                        role_desc = line.split('角色定位：')[-1].strip().rstrip('>')
                        break

                # 解析适用项目
                applicable = ''
                for line in content.split('\n')[:10]:
                    if line.startswith('>') and '适用项目' in line:
                        applicable = line.split('适用项目：')[-1].strip().rstrip('>')
                        break

                role_name = name_cn or agent
                lines.append(f'| {role_name} | {role_desc} | {applicable} |')

        return '\n'.join(lines)

    def _get_template_replacements(self):
        """获取模板占位符替换字典"""
        project_type_label = self.TEMPLATE_LABELS.get(
            self.PROJECT_TYPE, self.PROJECT_TYPE or 'general'
        )
        return {
            'project_name': self.project_name,
            'project_path': self.project_path,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'project_type': project_type_label,
        }

    def _write_template(self, template_name, target_name=None,
                        replacements=None, force=False):
        """加载模板并写入项目目录"""
        target_name = target_name or template_name
        target_path = os.path.join(self.project_path, target_name)
        if os.path.exists(target_path) and not force:
            return False
        content = self._load_template_content(template_name)
        if content is None:
            return False
        repl = self._get_template_replacements()
        if replacements:
            repl.update(replacements)
        for key, value in repl.items():
            content = content.replace(f'{{{key}}}', str(value))
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    def _init_templates(self, dry_run=False):
        """加载所有初始化模板（多态：子类可覆盖各文件内容）"""
        if dry_run:
            print(f"\n  [预览] 将加载以下模板:")
            for template in self.INIT_TEMPLATES:
                print(f"    - {template}")
            return True
        print(f"\n  [加载模板]")
        for template in self.INIT_TEMPLATES:
            if self._write_template_with_custom_content(template):
                print(f"  [创建] {template}")
        return True

    def _write_template_with_custom_content(self, template_name):
        """
        写入模板（多态实现）
        根据模板类型调用子类方法获取个性化内容
        _load_template_content会在末尾加.template，所以传入时要去除
        """
        target_name = template_name
        target_path = os.path.join(self.project_path, target_name)
        if os.path.exists(target_path):
            return False

        # 加载共性模板（.json -> .template.json, .md -> .template）
        if template_name.endswith('.json'):
            template_base = template_name.replace('.json', '')
        else:
            template_base = template_name.replace('.md', '')
        content = self._load_template_content(template_base)
        if content is None:
            return False

        # 获取个性化内容并注入
        custom_content = self._get_template_custom_content(template_name)
        content = self._inject_custom_content(content, custom_content)

        # 替换基础占位符
        repl = self._get_template_replacements()
        for key, value in repl.items():
            content = content.replace(f'{{{key}}}', str(value))

        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    def _get_template_custom_content(self, template_name):
        """
        获取各模板的个性化内容（模板方法，调用子类实现）
        返回字典：{title, content}
        """
        if template_name == 'README.md':
            return {'title': '', 'content': self._get_readme_custom_content()}
        elif template_name == 'AGENTS.md':
            return {'title': self.AGENTS_TITLE, 'content': self._get_skill_custom_content()}
        elif template_name == 'TODO.md':
            return {'title': '', 'content': self._get_todo_custom_content()}
        elif template_name == 'METADATA.json':
            return {'title': '', 'content': self._get_metadata_custom_content()}
        return {'title': '', 'content': ''}

    def _get_readme_custom_content(self):
        """README 个性内容：工作流描述 + 团队分工表格"""
        team_table = self._generate_team_division_table()
        return (self.WORKFLOW_DESC + '\n' + team_table).strip()

    # 子类覆盖的个性内容方法（基类提供空实现）
    def _get_skill_custom_content(self):
        """AGENTS 个性内容（子类覆盖）"""
        return ''

    def _get_todo_custom_content(self):
        """TODO 个性内容（子类覆盖）"""
        return ''

    def _get_metadata_custom_content(self):
        """METADATA 个性字段（子类覆盖）"""
        return ''


    def _inject_custom_content(self, content, custom):
        """注入个性化内容到模板（支持两种格式）"""
        # 格式1：SKILL.template 使用 {custom_section_title} 和 {custom_section_content}
        if '{custom_section_title}' in content:
            title = custom.get('title', '') if isinstance(custom, dict) else ''
            content = content.replace('{custom_section_title}', title)
        if '{custom_section_content}' in content:
            body = custom.get('content', '') if isinstance(custom, dict) else custom
            content = content.replace('{custom_section_content}', body)
        # 格式2：README/TODO/METADATA 使用 {custom_section}
        if '{custom_section}' in content:
            body = custom.get('content', '') if isinstance(custom, dict) else str(custom)
            content = content.replace('{custom_section}', body)
        return content

    # ──────────────────────────────
    # 元数据初始化（封装的共性）
    # ──────────────────────────────
    def _init_metadata(self):
        """初始化 METADATA.json（由模板生成，不再单独创建）"""
        # METADATA.json 由 _init_templates() 通过模板生成
        return True

    # ──────────────────────────────
    # 初始化入口（模板方法）
    # ──────────────────────────────
    def init(self, dry_run=False):
        """通用项目初始化流程"""
        prefix = "[预览] " if dry_run else ""
        print(f"{prefix}初始化项目: {self.project_name}")
        print(f"{prefix}路径: {self.project_path}")

        if not os.path.exists(self.project_path):
            if not dry_run:
                os.makedirs(self.project_path, exist_ok=True)
            print(f"  [创建] 项目目录: {self.project_path}")

        created = self._create_directories()
        if created:
            print(f"  [创建] 目录: {', '.join(created)}")
        else:
            print(f"  [信息] 所有标准目录已存在")

        self._init_templates(dry_run)

        if not dry_run:
            self._init_metadata()
            self._init_git_repo()
            self.init_post()

        print(f"\n{prefix}初始化完成！")
        return True

    def init_post(self):
        """初始化后的子类特有逻辑（子类覆盖）"""
        pass

    # ──────────────────────────────
    # 文件整理入口（模板方法）
    # ──────────────────────────────
    def organize(self, dry_run=False):
        """通用整理流程（模板方法）"""
        prefix = "[预览] " if dry_run else ""
        print(f"{prefix}整理项目: {self.project_name}")

        self._create_directories()
        results = self._organize_files(dry_run)

        if not dry_run:
            self._update_metadata()
        print(f"\n{prefix}整理完成")
        return results if results is not None else {"moved": [], "deleted": [], "renamed": []}

    def _organize_files(self, dry_run=False):
        """整理文件（子类覆盖的钩子）"""
        pass

    def _update_metadata(self):
        """更新元数据（子类可覆盖）"""
        self.metadata["last_organized"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_metadata()

    # ──────────────────────────────
    # 通用工具方法
    # ──────────────────────────────
    def _move_file(self, file_path, target_dir, new_name=None, overwrite=False):
        """移动文件到目标目录"""
        if os.path.isabs(file_path):
            src_path = file_path
        else:
            src_path = os.path.join(self.project_path, file_path)

        if not os.path.exists(src_path):
            return None

        target_path = os.path.join(self.project_path, target_dir)
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)

        filename = new_name or os.path.basename(src_path)
        dst_path = os.path.join(target_path, filename)

        if os.path.exists(dst_path) and not overwrite:
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dst_path):
                dst_path = os.path.join(target_path, f"{name}_{counter}{ext}")
                counter += 1

        try:
            shutil.move(src_path, dst_path)
            return os.path.relpath(dst_path, self.project_path)
        except Exception:
            return None

    def _get_file_type(self, filename):
        """
        判断文件类型（子类覆盖的钩子）
        默认返回 "other"，子类可覆盖实现个性化分类
        """
        return "other"

    def _is_protected_file(self, filename):
        """判断是否为保护文件（考虑 EXTRA_PROTECTED）"""
        if filename in self.BASE_PROTECTED:
            return True
        if filename in self.EXTRA_PROTECTED:
            return True
        return False

    # ──────────────────────────────
    # 维护流程（模板方法）
    # ──────────────────────────────
    CURRENT_SCHEMA_VERSION = "2.0"

    def maintain(self, dry_run=False):
        """
        项目维护流程（模板方法）：
        1. 检测 metadata 状态（missing/outdated/current）
        2. 迁移/初始化 metadata
        3. 检查并修复目录结构
        4. 扫描文件并修复 metadata 记录
        5. 验证保护文件
        6. 记录维护日志

        :param dry_run: True 则只报告不修改
        :return: bool
        """
        prefix = "[预览] " if dry_run else ""
        print(f"\n{prefix}维护项目: {self.project_name}")
        print(f"  路径: {self.project_path}")

        results = {
            "schema_status": None,
            "metadata_action": None,
            "directories_created": [],
            "directories_missing": [],
            "files_scanned": 0,
            "metadata_patched": 0,
            "protected_missing": [],
            "log_written": False,
        }

        # 1. 检测 schema 版本
        schema_status = self._detect_schema_version()
        results["schema_status"] = schema_status
        print(f"\n  [1/5] 检测元数据状态: {schema_status}")

        # 2. 迁移/初始化
        if schema_status == "missing":
            print(f"  [2/5] 初始化元数据...")
            results["metadata_action"] = self._init_metadata_from_scratch(dry_run)
        elif schema_status == "outdated":
            print(f"  [2/5] 迁移元数据到 v{self.CURRENT_SCHEMA_VERSION}...")
            results["metadata_action"] = self._migrate_metadata(dry_run)
        else:
            print(f"  [2/5] 验证元数据 (已是 v{self.CURRENT_SCHEMA_VERSION})")
            results["metadata_action"] = "skipped"

        # 3. 目录检查
        print(f"  [3/5] 检查目录结构...")
        dir_result = self._check_and_repair_directories(dry_run)
        results["directories_created"] = dir_result["created"]
        results["directories_missing"] = dir_result["missing"]

        # 4. 扫描文件 & 修复 metadata
        print(f"  [4/5] 扫描文件并修复元数据...")
        scan_result = self._scan_and_patch_metadata(dry_run)
        results["files_scanned"] = scan_result["scanned"]
        results["metadata_patched"] = scan_result["patched"]

        # 5. 验证保护文件
        print(f"  [5/5] 验证保护文件...")
        results["protected_missing"] = self._verify_protected_files(dry_run)

        # 6. 写维护日志
        if not dry_run:
            results["log_written"] = self._write_maintain_log(results)

        # 汇总输出
        print(f"\n  ── 维护摘要 ──")
        print(f"  元数据状态: {schema_status}")
        if results["directories_created"]:
            print(f"  新建目录: {', '.join(results['directories_created'])}")
        if results["metadata_patched"] > 0:
            print(f"  元数据修复: {results['metadata_patched']} 项")
        if results["protected_missing"]:
            print(f"  缺失保护文件: {', '.join(results['protected_missing'])}")
        print(f"  扫描文件: {results['files_scanned']} 个")

        print(f"\n{prefix}维护完成")
        return results

    def _detect_schema_version(self):
        """
        检测 metadata schema 版本
        :return: 'missing' | 'outdated' | 'current'
        """
        if not os.path.exists(self.metadata_path):
            return "missing"
        if not self.metadata:
            return "missing"
        if "schema_version" not in self.metadata:
            return "outdated"
        if self.metadata.get("schema_version") == self.CURRENT_SCHEMA_VERSION:
            return "current"
        return "outdated"

    def _init_metadata_from_scratch(self, dry_run=False):
        """
        无 metadata 时初始化标准格式
        """
        print(f"    [新建] metadata.json (v{self.CURRENT_SCHEMA_VERSION})")
        if dry_run:
            return "preview"
        self.metadata = self._create_standard_metadata()
        self._save_metadata()
        return "created"

    def _create_standard_metadata(self):
        """创建标准格式的 metadata（子类可覆盖扩展字段）"""
        return {
            "schema_version": self.CURRENT_SCHEMA_VERSION,
            "project_id": self.project_name,
            "project_type": self.PROJECT_TYPE or "unknown",
            "title": self.project_name,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "updated_at": datetime.now().isoformat(),
            "status": "active",
            "version": "1.0.0",
            "description": f"{self.project_name} 项目",
            "directories": {d: f"{d}/" for d in self.STANDARD_DIRS},
            "documents": [],
            "maintain_history": [],
        }

    def _migrate_metadata(self, dry_run=False):
        """
        迁移旧格式 metadata 到当前标准格式
        子类覆盖此方法实现个性迁移逻辑
        """
        print(f"    [迁移] 执行通用字段迁移")
        if dry_run:
            return "preview"

        # 备份旧文件
        backup_path = f"{self.metadata_path}.bak_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copy2(self.metadata_path, backup_path)
        print(f"    [备份] {os.path.basename(backup_path)}")

        # 基础迁移：保留已有字段，补全缺失字段
        old = self.metadata.copy()
        new = self._create_standard_metadata()

        # 迁移旧字段
        for key in ["project_id", "title", "created_date", "updated_at",
                    "status", "version", "description", "documents"]:
            if key in old:
                new[key] = old[key]

        self.metadata = new
        self._save_metadata()
        return "migrated"

    def _check_and_repair_directories(self, dry_run=False):
        """
        检查并修复目录结构：缺失则创建
        :return: {created: [...], missing: [...]}
        """
        result = {"created": [], "missing": []}
        for dir_name in self.STANDARD_DIRS:
            dir_path = os.path.join(self.project_path, dir_name)
            if not os.path.exists(dir_path):
                result["missing"].append(dir_name)
                if not dry_run:
                    os.makedirs(dir_path, exist_ok=True)
                    result["created"].append(dir_name)
                    print(f"    [创建] {dir_name}/")
        return result

    def _scan_and_patch_metadata(self, dry_run=False):
        """
        扫描实际文件并修复 metadata 记录
        子类可覆盖 _scan_directory() 实现自定义文件扫描
        :return: {scanned: int, patched: int}
        """
        result = {"scanned": 0, "patched": 0}

        # 扫描 uploads/
        uploads_dir = os.path.join(self.project_path, "uploads")
        if os.path.exists(uploads_dir):
            for fname in os.listdir(uploads_dir):
                fpath = os.path.join(uploads_dir, fname)
                if os.path.isfile(fpath) and not fname.startswith('.'):
                    result["scanned"] += 1
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in ['.docx', '.pdf', '.txt', '.doc', '.xlsx', '.pptx']:
                        path_key = f"uploads/{fname}"
                        if not self._metadata_has_document(path_key):
                            self._metadata_add_document(fname, path_key)
                            result["patched"] += 1
                            if not dry_run:
                                print(f"    [补录] {fname} -> uploads/")

        # 扫描 manuscripts/
        manuscripts_dir = os.path.join(self.project_path, "manuscripts")
        if os.path.exists(manuscripts_dir):
            for fname in os.listdir(manuscripts_dir):
                fpath = os.path.join(manuscripts_dir, fname)
                if os.path.isfile(fpath) and fname.endswith('.md'):
                    result["scanned"] += 1
                    path_key = f"manuscripts/{fname}"
                    if not self._metadata_has_manuscript(path_key):
                        self._metadata_add_manuscript(fname, path_key)
                        result["patched"] += 1
                        if not dry_run:
                            print(f"    [补录] {fname} -> manuscripts/")

        # 扫描知识库子目录（notes, reviews）
        kb_dir = os.path.join(self.project_path, "knowledge")
        if os.path.exists(kb_dir):
            for subdir in ["notes", "reviews"]:
                subdir_path = os.path.join(kb_dir, subdir)
                if os.path.exists(subdir_path):
                    key = "notes" if subdir == "notes" else "reviews"
                    for fname in os.listdir(subdir_path):
                        fpath = os.path.join(subdir_path, fname)
                        if os.path.isfile(fpath) and not fname.startswith('.'):
                            result["scanned"] += 1
                            path_key = f"knowledge/{key}/{fname}"
                            if not self._metadata_has_note(path_key):
                                self._metadata_add_note(fname, path_key)
                                result["patched"] += 1
                                if not dry_run:
                                    print(f"    [补录] {fname} -> knowledge/{key}/")

        if not dry_run and result["patched"] > 0:
            self._save_metadata()

        return result

    def _metadata_has_document(self, path):
        docs = self.metadata.get("documents", [])
        return any(d.get("path") == path for d in docs)

    def _metadata_add_document(self, title, path):
        if "documents" not in self.metadata:
            self.metadata["documents"] = []
        self.metadata["documents"].append({
            "title": os.path.splitext(title)[0],
            "version": "v1",
            "path": path,
            "type": "user_uploaded",
        })

    def _metadata_has_manuscript(self, path):
        mds = self.metadata.get("manuscripts", {})
        return path in mds

    def _metadata_add_manuscript(self, title, path):
        if "manuscripts" not in self.metadata:
            self.metadata["manuscripts"] = {}
        self.metadata["manuscripts"][title] = {
            "local_path": path,
            "cloud": [],
        }

    def _metadata_has_note(self, path):
        notes = self.metadata.get("notes", {})
        return any(n.get("local_path") == path for n in notes.values())

    def _metadata_add_note(self, title, path):
        if "notes" not in self.metadata:
            self.metadata["notes"] = {}
        self.metadata["notes"][title] = {
            "local_path": path,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "description": "",
        }

    def _verify_protected_files(self, dry_run=False):
        """
        验证保护文件是否存在
        :return: 缺失文件列表
        """
        missing = []
        for fname in self.PROTECTED_FILES:
            fpath = os.path.join(self.project_path, fname)
            if not os.path.exists(fpath):
                missing.append(fname)
                print(f"    [缺失] {fname}")
        return missing

    def _write_maintain_log(self, results):
        """
        写入维护日志到 .agentsevents/
        """
        events_dir = os.path.join(self.project_path, ".agentsevents")
        if not os.path.exists(events_dir):
            os.makedirs(events_dir, exist_ok=True)

        log_file = os.path.join(events_dir, f"maintain_{datetime.now().strftime('%Y%m%d')}.log")
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "schema_status": results["schema_status"],
            "metadata_action": results["metadata_action"],
            "directories_created": results["directories_created"],
            "files_scanned": results["files_scanned"],
            "metadata_patched": results["metadata_patched"],
            "protected_missing": results["protected_missing"],
        }

        # 追加到日志文件
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            # 更新 metadata 中的维护历史
            if "maintain_history" not in self.metadata:
                self.metadata["maintain_history"] = []
            self.metadata["maintain_history"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "action": results["metadata_action"],
                "scanned": results["files_scanned"],
                "patched": results["metadata_patched"],
            })
            self._save_metadata()
            return True
        except Exception as e:
            print(f"    [警告] 写维护日志失败: {e}")
            return False

    # ──────────────────────────────
    # 模板安全更新（GENERATED / PRIVATE 标记区块）
    # ──────────────────────────────
    def _extract_private_blocks(self, content):
        """
        提取所有 PRIVATE 区块内容，替换为占位符
        支持嵌套 PRIVATE 区块（从内到外逐层提取）
        :return: [(placeholder, original_text), ...]
        """
        blocks = []
        placeholder_prefix = "__PRIVATE_BLOCK_"
        counter = [0]

        def extract_one_layer(text):
            """提取一层的 PRIVATE 区块，返回 (处理后文本, 提取的块列表)"""
            extracted = []
            pattern = re.compile(
                re.escape(self.PRIVATE_START) + r"(.*?)" + re.escape(self.PRIVATE_END),
                re.DOTALL
            )

            def replacer(match):
                inner = match.group(1)
                placeholder = f"{placeholder_prefix}{counter[0]}"
                counter[0] += 1
                extracted.append((placeholder, inner))
                return placeholder

            result = pattern.sub(replacer, text)
            return result, extracted

        # 从内到外逐层提取
        current = content
        while self.PRIVATE_START in current:
            current, layer_blocks = extract_one_layer(current)
            blocks.extend(layer_blocks)
            # 如果没有提取到任何块但仍有标记，说明格式损坏，停止
            if not layer_blocks:
                break

        return blocks

    def _verify_template_sections(self, filepath):
        """
        检查文件的标记区块完整性
        :return: ('ok' | 'missing_start' | 'missing_end' | 'no_markers', warnings[])
        """
        if not os.path.exists(filepath):
            return 'missing_file', []

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        has_gen_start = self.GENERATED_START in content
        has_gen_end = self.GENERATED_END in content
        has_priv_start = self.PRIVATE_START in content
        has_priv_end = self.PRIVATE_END in content

        warnings = []

        if not has_gen_start and not has_gen_end and not has_priv_start and not has_priv_end:
            return 'no_markers', ['文件中没有任何 GENERATED 或 PRIVATE 标记，将执行全量替换']

        if has_gen_start != has_gen_end:
            warnings.append(f"GENERATED 标记不完整：{'缺少 ' + self.GENERATED_START if not has_gen_start else '缺少 ' + self.GENERATED_END}")
            return 'incomplete', warnings

        if has_priv_start != has_priv_end:
            warnings.append(f"PRIVATE 标记不完整：{'缺少 ' + self.PRIVATE_START if not has_priv_start else '缺少 ' + self.PRIVATE_END}")
            return 'incomplete', warnings

        return 'ok', warnings

    def update_template(self, template_name, dry_run=False):
        """
        安全更新单个模板文件，保留 PRIVATE 区块内容

        策略：
        1. 文件不存在 → 直接从模板创建
        2. 文件存在但无标记 → 全量替换（旧项目兼容）
        3. 文件存在且有 GENERATED 标记 → 保留 PRIVATE，替换 GENERATED
        4. PRIVATE 区块全部还原到原位置

        :param template_name: 模板文件名（如 'README.md'）
        :param dry_run: True 则只预览不写入
        :return: ('skipped' | 'created' | 'updated' | 'full_replaced', description)
        """
        target_path = os.path.join(self.project_path, template_name)

        # 1. 文件不存在，直接从模板创建
        if not os.path.exists(target_path):
            content = self._load_template_content(
                template_name.replace('.md', '').replace('.json', '')
            )
            if content is None:
                return 'skipped', f"模板 {template_name} 不存在"

            # 应用占位符替换
            repl = self._get_template_replacements()
            for key, value in repl.items():
                content = content.replace(f'{{{key}}}', str(value))

            if dry_run:
                return 'created', f"[预览] 将创建 {template_name}"
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return 'created', f"已创建 {template_name}"

        # 2. 文件存在，检查标记完整性
        status, warnings = self._verify_template_sections(target_path)

        if status == 'no_markers' or status == 'missing_file':
            # 无标记 → 默认 SKIP 保护项目定制内容（v1.6.0 行为变更）
            #   老项目 AGENTS.md（从 HANDBOOK.md 改名）无 GENERATED 标记，
            #   误判"全量替换"会丢失项目特定章节。默认 skip，需要时加 --force
            if not getattr(self, 'force_overwrite', False):
                return 'skipped', f"[保护] {template_name} 无 GENERATED 标记(疑似项目定制)——已 skip,加 --force 强制覆盖"

            # --force 显式 opt-in,才执行全量替换(旧行为,谨慎使用)
            new_content = self._load_template_content(
                template_name.replace('.md', '').replace('.json', '')
            )
            if new_content is None:
                return 'skipped', f"模板 {template_name} 不存在"

            # 应用占位符替换
            repl = self._get_template_replacements()
            for key, value in repl.items():
                new_content = new_content.replace(f'{{{key}}}', str(value))

            if dry_run:
                return 'full_replaced', f"[预览/--force] 将全量替换 {template_name}（无标记区块）"
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return 'full_replaced', f"[--force] 全量替换 {template_name}（无标记区块,项目定制内容已覆盖）"

        # 3. 有 GENERATED 标记 → 安全合并
        with open(target_path, 'r', encoding='utf-8') as f:
            existing = f.read()

        # 提取 PRIVATE 区块
        private_blocks = self._extract_private_blocks(existing)

        # 加载新模板
        new_content = self._load_template_content(
            template_name.replace('.md', '').replace('.json', '')
        )
        if new_content is None:
            return 'skipped', f"模板 {template_name} 不存在"

        # 应用占位符替换
        repl = self._get_template_replacements()
        for key, value in repl.items():
            new_content = new_content.replace(f'{{{key}}}', str(value))

        # 如果新模板没有 GENERATED 标记，追加 PRIVATE 区块到末尾
        if self.GENERATED_START not in new_content:
            priv_sections = "\n\n".join(
                f"{self.PRIVATE_START}\n{content}\n{self.PRIVATE_END}"
                for _, content in private_blocks
            )
            new_content = new_content.rstrip() + "\n\n" + priv_sections
        else:
            # 用 PRIVATE 占位符替换原有内容中非 GENERATED 的部分
            result_parts = []
            gen_start = self.GENERATED_START
            gen_end = self.GENERATED_END

            # 拆分：GENERATED 区域 vs 外部区域
            # 外部区域保留 PRIVATE 标记（如果有的话）
            pattern = re.compile(
                re.escape(gen_start) + r".*?" + re.escape(gen_end),
                re.DOTALL
            )

            def replacer_gen(match):
                return f"{gen_start}\n{new_content}\n{gen_end}"

            # 先生成保留 PRIVATE 标记的新内容
            new_with_priv_markers = new_content
            priv_sections = "\n\n".join(
                f"{self.PRIVATE_START}\n{content}\n{self.PRIVATE_END}"
                for _, content in private_blocks
            )

            if priv_sections:
                new_with_priv_markers = new_with_priv_markers.rstrip() + "\n\n" + priv_sections

            if dry_run:
                changed = len(private_blocks)
                return 'updated', f"[预览] 将更新 {template_name}（保留 {changed} 个 PRIVATE 区块）"
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(new_with_priv_markers)
            changed = len(private_blocks)
            return 'updated', f"已更新 {template_name}（保留 {changed} 个 PRIVATE 区块）"


    def check_updates(self):
        """
        检查项目文档是否需要更新（对比模板版本号）
        
        :return: [(filename, current_version, expected_version, status), ...]
        """
        import json
        import os
        from packaging import version as pkg_version
        
        # 读取模板版本表
        skill_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        version_file = os.path.join(skill_dir, 'assets', 'template-versions.json')
        
        if not os.path.exists(version_file):
            return []
        
        with open(version_file, 'r', encoding='utf-8') as f:
            tv_data = json.load(f)
        
        expected_versions = tv_data.get('templates', {})
        results = []
        
        for template_name in self.SYNC_TEMPLATES:
            target_path = os.path.join(self.project_path, template_name)
            expected = expected_versions.get(template_name, {}).get('version', '0.0.0')
            
            if not os.path.exists(target_path):
                results.append((template_name, 'N/A', expected, 'new'))
                continue
            
            # 从文件中提取版本号
            current = '0.0.0'
            try:
                with open(target_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 匹配 version: X.X.X 或 "version": "X.X.X"
                for pattern in [r'^version:\s*(\d+\.\d+\.\d+)', 
                               r'"version":\s*"(\d+\.\d+\.\d+)"']:
                    m = re.search(pattern, content, re.MULTILINE)
                    if m:
                        current = m.group(1)
                        break
            except Exception:
                pass
            
            # 比较版本
            try:
                if pkg_version.parse(current) < pkg_version.parse(expected):
                    status = 'outdated'
                else:
                    status = 'ok'
            except Exception:
                status = 'unknown'
            
            results.append((template_name, current, expected, status))
        
        return results

    def sync_templates(self, dry_run=False):
        """
        同步所有模板文件，保留 PRIVATE 区块内容

        :param dry_run: True 则只预览不写入
        :return: [(filename, status, description), ...]
        """
        print(f"\n  [同步模板]")
        results = []

        # 合并基类 + 子类的模板列表
        templates = list(self.SYNC_TEMPLATES)
        for t in getattr(self, 'EXTRA_SYNC_TEMPLATES', []):
            if t not in templates:
                templates.append(t)

        for template_name in templates:
            status, desc = self.update_template(template_name, dry_run=dry_run)
            results.append((template_name, status, desc))
            icon = {
                'created': '🆕',
                'updated': '🔄',
                'full_replaced': '🔃',
                'skipped': '⏭️',
            }.get(status, '❓')
            print(f"  {icon} {desc}")

        if dry_run:
            changed = [r for r in results if r[1] not in ('skipped',)]
            print(f"\n  [预览] 共 {len(changed)} 个文件将被更新")
        else:
            changed = [r for r in results if r[1] not in ('skipped',)]
            print(f"\n  ✅ 已更新 {len(changed)} 个文件")

        return results

    def _get_sync_templates(self):
        """
        获取需要同步的模板文件列表（子类可覆盖）
        """
        return self.SYNC_TEMPLATES


def main():
    """命令行入口（BaseMaintainer 自身，支持 sync-templates）"""
    import argparse
    parser = argparse.ArgumentParser(description="BaseMaintainer 模板同步工具")
    parser.add_argument("command", nargs="?", default="sync-templates",
                        help="命令: sync-templates（默认）")
    parser.add_argument("project_path", nargs="?", help="项目路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()

    command = args.command
    if not args.project_path:
        print("用法: python3 BaseMaintainer.py sync-templates <项目路径> [--dry-run]")
        sys.exit(1)

    dry_run = args.dry_run
    maintainer = BaseMaintainer(args.project_path)

    if command == 'sync-templates':
        maintainer.sync_templates(dry_run=dry_run)
    elif command == 'init':
        maintainer.init(dry_run=dry_run)
    elif command == 'organize':
        maintainer.organize(dry_run=dry_run)
    elif command == 'maintain':
        maintainer.maintain(dry_run=dry_run)
    else:
        print(f"未知命令: {command}")
        print("可用命令: sync-templates, init, organize, maintain")
        sys.exit(1)


if __name__ == '__main__':
    main()
