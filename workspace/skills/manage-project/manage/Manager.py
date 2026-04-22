#!/usr/bin/env python3
"""
Manager.py - 知识库管理工具

功能：
    - 合并多个知识库文件（去重）
    - 按条件筛选论文（年份、引用量、主题、类型等）
    - 支持链式调用和保存
"""

import os
import json
from datetime import datetime
from copy import deepcopy
from typing import List, Dict, Optional, Union, Any


class Manager:
    """知识库管理器 - 合并、筛选、整理"""

    def __init__(self, kb_path: Optional[str] = None):
        """
        初始化管理器（绑定知识库路径）
        Args:
            kb_path: 知识库文件路径。为 None 时表示空管理器，用于合并操作
        """
        self._kb_data = None
        self._current_papers = []
        self.kb_path = kb_path
        if kb_path:
            self.load(kb_path)

    # ==================== 加载与保存 ====================

    def load(self, kb_path: str) -> 'Manager':
        """加载知识库文件"""
        with open(kb_path, 'r', encoding='utf-8') as f:
            self._kb_data = json.load(f)
        self._current_papers = self._kb_data.get('papers', [])
        print(f"已加载知识库: {kb_path}, 共 {len(self._current_papers)} 篇论文")
        return self

    def save(self, output_path: Optional[str] = None, project_name: str = "") -> str:
        """
        保存当前知识库数据到文件
        Args:
            output_path: 输出文件路径（默认使用绑定的 kb_path）
            project_name: 项目名称（会更新到知识库中）
        """
        if self._kb_data is None:
            raise ValueError("没有可保存的知识库数据，请先加载或合并数据")
        
        # 确定保存路径
        save_path = output_path or self.kb_path
        if not save_path:
            raise ValueError("未指定输出路径，且未绑定 kb_path")
        
        # 更新统计和元数据
        self._kb_data['papers'] = self._current_papers
        self._kb_data['statistics'] = self._compute_statistics(self._current_papers)
        self._kb_data['updated_at'] = datetime.now().isoformat()
        if project_name:
            self._kb_data['project'] = project_name
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self._kb_data, f, ensure_ascii=False, indent=2)
        print(f"知识库已保存至: {save_path}")
        return save_path

    # ==================== 核心功能 ====================

    def merge(self, *kb_paths: str, deduplicate: bool = True) -> 'Manager':
        """
        合并一个或多个知识库文件（去重）
        Args:
            *kb_paths: 知识库文件路径（可传入多个）
            deduplicate: 是否全局去重（基于 paperId）
        Returns:
            self
        """
        all_papers = []
        # 若已存在当前知识库，先加入
        if self._current_papers:
            all_papers.extend(self._current_papers)

        for path in kb_paths:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                papers = data.get('papers', [])
                all_papers.extend(papers)
                print(f"合并 {path}: {len(papers)} 篇")

        if deduplicate:
            before = len(all_papers)
            all_papers = self._deduplicate(all_papers)
            print(f"去重: {before} -> {len(all_papers)} 篇")

        self._current_papers = all_papers
        # 重建知识库结构（保留原有元数据或创建新结构）
        if self._kb_data is None:
            self._kb_data = {
                "version": "1.0.0",
                "project": "合并知识库",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "statistics": {},
                "papers": self._current_papers
            }
        else:
            self._kb_data['papers'] = self._current_papers
        return self

    def filter(self, conditions: Dict[str, Any]) -> 'Manager':
        """
        按条件筛选当前知识库，生成新的知识库子集
        Args:
            conditions: 筛选条件字典，支持以下键：
                - year_min: 最小年份
                - year_max: 最大年份
                - citations_min: 最小引用量
                - citations_max: 最大引用量
                - topics: 主题列表（任意匹配）
                - types: 文献类型列表（如 ["📊实证", "📖综述"]）
                - importance: 重要性列表（如 ["🔴奠基", "🟡重要"]）
                - venue: 期刊/会议名称（模糊匹配）
                - limit: 返回前 N 篇（需与排序配合）
                - sort_by: 排序字段（如 "citationCount", "year"），默认不排序
                - sort_desc: 是否降序（默认 True）
        Returns:
            self (当前对象的 _current_papers 变为筛选后的列表)
        """
        if not self._current_papers:
            raise ValueError("当前没有论文数据，请先加载或合并知识库")

        result = deepcopy(self._current_papers)

        # 年份筛选
        if 'year_min' in conditions:
            year_min = conditions['year_min']
            result = [p for p in result if p.get('year', 0) >= year_min]
        if 'year_max' in conditions:
            year_max = conditions['year_max']
            result = [p for p in result if p.get('year', 0) <= year_max]

        # 引用量筛选
        if 'citations_min' in conditions:
            cit_min = conditions['citations_min']
            result = [p for p in result if p.get('citationCount', 0) >= cit_min]
        if 'citations_max' in conditions:
            cit_max = conditions['citations_max']
            result = [p for p in result if p.get('citationCount', 0) <= cit_max]

        # 主题筛选（任意匹配）
        if 'topics' in conditions:
            topics = conditions['topics']
            result = [p for p in result if any(t in p.get('topic', []) for t in topics)]

        # 文献类型筛选
        if 'types' in conditions:
            types = conditions['types']
            result = [p for p in result if p.get('labels', {}).get('type') in types]

        # 重要性筛选
        if 'importance' in conditions:
            imp_list = conditions['importance']
            result = [p for p in result if p.get('labels', {}).get('importance') in imp_list]

        # 期刊/会议名称模糊匹配
        if 'venue' in conditions:
            venue_keyword = conditions['venue'].lower()
            result = [p for p in result if venue_keyword in p.get('venue', '').lower()]

        # 排序
        if 'sort_by' in conditions:
            sort_key = conditions['sort_by']
            desc = conditions.get('sort_desc', True)
            result.sort(key=lambda x: x.get(sort_key, 0) or 0, reverse=desc)

        # 数量限制
        if 'limit' in conditions:
            limit = conditions['limit']
            result = result[:limit]

        self._current_papers = result
        # 同步到 _kb_data
        if self._kb_data:
            self._kb_data['papers'] = self._current_papers
        print(f"筛选后剩余 {len(result)} 篇论文")
        return self

    # ==================== 辅助方法 ====================

    def _deduplicate(self, papers: List[Dict]) -> List[Dict]:
        """基于 paperId 去重"""
        seen = set()
        unique = []
        for p in papers:
            pid = p.get('paperId')
            if pid and pid not in seen:
                seen.add(pid)
                unique.append(p)
            elif not pid:
                title = p.get('title')
                if title and title not in seen:
                    seen.add(title)
                    unique.append(p)
        return unique

    def _compute_statistics(self, papers: List[Dict]) -> Dict:
        total = len(papers)
        total_cites = sum(p.get('citationCount', 0) for p in papers)
        foundation = sum(1 for p in papers if p.get('labels', {}).get('importance') == '🔴奠基')
        important = sum(1 for p in papers if p.get('labels', {}).get('importance') == '🟡重要')
        general = total - foundation - important
        empirical = sum(1 for p in papers if p.get('labels', {}).get('type') == '📊实证')
        review = sum(1 for p in papers if p.get('labels', {}).get('type') == '📖综述')
        theory = sum(1 for p in papers if p.get('labels', {}).get('type') == '💡理论')
        return {
            "total_count": total,
            "total_citations": total_cites,
            "foundation_count": foundation,
            "important_count": important,
            "general_count": general,
            "empirical_count": empirical,
            "review_count": review,
            "theory_count": theory
        }

    # ==================== 获取结果 ====================

    def get_kb(self) -> Dict:
        """返回当前知识库字典（若没有 _kb_data 则基于 _current_papers 构建）"""
        if self._kb_data is None:
            return {
                "version": "1.0.0",
                "project": "临时知识库",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "statistics": self._compute_statistics(self._current_papers),
                "papers": self._current_papers
            }
        else:
            self._kb_data['papers'] = self._current_papers
            self._kb_data['statistics'] = self._compute_statistics(self._current_papers)
            return self._kb_data

    def get_papers(self) -> List[Dict]:
        """返回当前论文列表"""
        return self._current_papers


# ==================== 命令行入口 ====================
if __name__ == "__main__":
    import argparse
    import os
    import json
    
    parser = argparse.ArgumentParser(
        description="Manager - 知识库管理工具"
    )
    subparsers = parser.add_subparsers(title="命令", dest="command")
    
    # merge 命令
    merge_parser = subparsers.add_parser("merge", help="合并多个知识库")
    merge_parser.add_argument("kb_paths", nargs="+", help="知识库文件路径列表")
    merge_parser.add_argument("--output", required=True, help="输出文件路径")
    merge_parser.add_argument("--project", default="合并项目", help="项目名称 (默认: 合并项目)")
    merge_parser.add_argument("--no-deduplicate", action="store_true", help="不去重")
    
    # filter 命令
    filter_parser = subparsers.add_parser("filter", help="筛选知识库")
    filter_parser.add_argument("--kb-path", required=True, help="输入知识库文件路径")
    filter_parser.add_argument("--output", required=True, help="输出文件路径")
    filter_parser.add_argument("--conditions", help="筛选条件JSON文件路径")
    filter_parser.add_argument("--year-min", type=int, help="最小年份")
    filter_parser.add_argument("--year-max", type=int, help="最大年份")
    filter_parser.add_argument("--citations-min", type=int, help="最小引用量")
    filter_parser.add_argument("--citations-max", type=int, help="最大引用量")
    filter_parser.add_argument("--types", help="文献类型（逗号分隔，如：📊实证,📖综述）")
    filter_parser.add_argument("--importance", help="重要性（逗号分隔，如：🔴奠基,🟡重要）")
    filter_parser.add_argument("--venue", help="期刊/会议名称（模糊匹配）")
    filter_parser.add_argument("--sort-by", help="排序字段（如：citationCount, year）")
    filter_parser.add_argument("--sort-asc", action="store_true", help="升序排序（默认降序）")
    filter_parser.add_argument("--limit", type=int, help="返回前N篇")
    
    # info 命令
    info_parser = subparsers.add_parser("info", help="显示知识库信息")
    info_parser.add_argument("--kb-path", default="index.json", help="知识库文件路径 (默认: index.json)")
    
    args = parser.parse_args()
    
    if args.command == "merge":
        # 检查输入文件
        for kb_path in args.kb_paths:
            if not os.path.exists(kb_path):
                print(f"错误: 知识库文件不存在: {kb_path}")
                import sys
                sys.exit(1)
        
        print(f"正在合并 {len(args.kb_paths)} 个知识库...")
        manager = Manager()  # 空管理器用于合并
        manager.merge(*args.kb_paths, deduplicate=not args.no_deduplicate)
        # 合并操作必须指定输出路径（空管理器无绑定路径）
        manager.save(args.output, args.project)
        print(f"完成! 输出: {args.output}")
    
    elif args.command == "filter":
        # 检查输入文件
        if not os.path.exists(args.kb_path):
            print(f"错误: 知识库文件不存在: {args.kb_path}")
            import sys
            sys.exit(1)
        
        # 构建筛选条件
        conditions = {}
        if args.conditions:
            if not os.path.exists(args.conditions):
                print(f"错误: 筛选条件文件不存在: {args.conditions}")
                import sys
                sys.exit(1)
            with open(args.conditions, 'r', encoding='utf-8') as f:
                conditions = json.load(f)
        
        # 命令行参数覆盖
        if args.year_min is not None:
            conditions["year_min"] = args.year_min
        if args.year_max is not None:
            conditions["year_max"] = args.year_max
        if args.citations_min is not None:
            conditions["citations_min"] = args.citations_min
        if args.citations_max is not None:
            conditions["citations_max"] = args.citations_max
        if args.types:
            conditions["types"] = args.types.split(",")
        if args.importance:
            conditions["importance"] = args.importance.split(",")
        if args.venue:
            conditions["venue"] = args.venue
        if args.sort_by:
            conditions["sort_by"] = args.sort_by
        if args.sort_asc:
            conditions["sort_desc"] = False
        if args.limit is not None:
            conditions["limit"] = args.limit
        
        print(f"正在筛选知识库...")
        manager = Manager(args.kb_path)
        # 使用绑定的路径保存（无参save）
        save_path = args.output or args.kb_path
        manager.filter(conditions).save(save_path)
        print(f"完成! 输出: {save_path}")
    
    elif args.command == "info":
        if not os.path.exists(args.kb_path):
            print(f"错误: 知识库文件不存在: {args.kb_path}")
            import sys
            sys.exit(1)
        
        manager = Manager(args.kb_path)
        kb = manager.get_kb()
        print("="*60)
        print("知识库信息")
        print("="*60)
        print(f"版本: {kb.get('version', 'N/A')}")
        print(f"项目: {kb.get('project', 'N/A')}")
        print(f"创建时间: {kb.get('created_at', 'N/A')}")
        print(f"更新时间: {kb.get('updated_at', 'N/A')}")
        print("-"*60)
        stats = kb.get('statistics', {})
        print(f"论文总数: {stats.get('total_count', 0)}")
        print(f"总引用量: {stats.get('total_citations', 0)}")
        print(f"奠基文献: {stats.get('foundation_count', 0)}")
        print(f"重要文献: {stats.get('important_count', 0)}")
        print(f"一般文献: {stats.get('general_count', 0)}")
        print(f"实证文献: {stats.get('empirical_count', 0)}")
        print(f"综述文献: {stats.get('review_count', 0)}")
        print(f"理论文献: {stats.get('theory_count', 0)}")
        print("="*60)
    
    else:
        parser.print_help()