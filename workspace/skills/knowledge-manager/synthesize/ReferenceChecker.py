#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引用检查修复类 - 面向对象重构
版本: v3.0.0
"""

import re
import json
from typing import Dict, List, Tuple, Optional


class ReferenceChecker:
    """
    参考文献检查与修复类
    
    核心方法: check_references(doc_path, **kwargs)
    """
    
    def __init__(self):
        self.citation_map = {}
        self.citation_text_map = {}
        self.dsam_pattern = re.compile(r'DSAM_\d+')
        self.content = ""
        self.knowledge_bases = {}
    
    def check_references(self, doc_path: str, **kwargs) -> Dict:
        """
        核心方法：检查参考文献（使用**kwargs支持多个知识库文件）
        
        参数:
            doc_path: 待检查的Markdown文档路径
            **kwargs: 知识库文件路径（如 kb1="path1", kb2="path2"）
            
        返回:
            检查结果字典
        """
        results = {
            "success": False,
            "doc_path": doc_path,
            "knowledge_bases": kwargs,
            "issues": [],
            "stats": {},
            "recommendations": []
        }
        
        try:
            # 步骤1: 加载文件
            self._load_documents(doc_path, **kwargs)
            
            # 步骤2: 构建引用映射
            self._build_citation_maps()
            
            # 步骤3: 检查引用
            dsam_refs = self._find_dsam_references()
            apa_refs = self._find_apa_references()
            
            # 步骤4: 验证引用
            missing_refs = self._validate_references(dsam_refs)
            
            # 步骤5: 统计结果
            stats = self._collect_stats(dsam_refs, apa_refs, missing_refs)
            
            # 步骤6: 生成建议
            recommendations = self._generate_recommendations(missing_refs, apa_refs)
            
            results["success"] = True
            results["stats"] = stats
            results["missing_references"] = missing_refs
            results["recommendations"] = recommendations
            
        except Exception as e:
            results["issues"].append(f"检查过程出错: {str(e)}")
        
        return results
    
    # ========== 私有辅助方法 ==========
    
    def _load_documents(self, doc_path: str, **kwargs):
        """加载文档和多个知识库文件"""
        # 加载Markdown文档
        with open(doc_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        # 加载所有知识库文件
        self.knowledge_bases = {}
        for kb_name, kb_path in kwargs.items():
            if kb_path:
                with open(kb_path, 'r', encoding='utf-8') as f:
                    self.knowledge_bases[kb_name] = json.load(f)
    
    def _build_citation_maps(self):
        """从多个知识库构建引用映射"""
        all_notes = {}
        
        # 合并所有知识库文件
        for kb_name, kb_data in self.knowledge_bases.items():
            all_notes.update(kb_data.get('notes', {}))
        
        for note_id, note_data in all_notes.items():
            if note_id.startswith('DSAM_'):
                paper = note_data.get('paper', {})
                authors = paper.get('authors', '')
                year = paper.get('year', '')
                
                if authors and year:
                    self.citation_map[note_id] = self._format_apa_citation(authors, year)
                    self.citation_text_map[note_id] = self._format_apa_citation_text(authors, year)
    
    def _find_dsam_references(self) -> List[str]:
        """查找文档中所有DSAM格式引用"""
        return self.dsam_pattern.findall(self.content)
    
    def _find_apa_references(self) -> List[str]:
        """查找文档中所有APA格式引用"""
        apa_pattern = re.compile(r'\([A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)?(?:\s+et\s+al\.)?,\s*\d{4}[a-z]?\)')
        return apa_pattern.findall(self.content)
    
    def _validate_references(self, dsam_refs: List[str]) -> List[str]:
        """验证引用是否存在于知识库中"""
        unique_refs = set(dsam_refs)
        return [ref for ref in unique_refs if ref not in self.citation_map]
    
    def _collect_stats(self, dsam_refs: List[str], apa_refs: List[str], missing_refs: List[str]) -> Dict:
        """收集统计信息"""
        return {
            "dsam_total": len(dsam_refs),
            "dsam_unique": len(set(dsam_refs)),
            "apa_total": len(apa_refs),
            "missing_count": len(missing_refs),
            "knowledge_base_count": len(self.knowledge_bases),
            "has_content": len(self.content) > 0,
            "content_length": len(self.content)
        }
    
    def _generate_recommendations(self, missing_refs: List[str], apa_refs: List[str]) -> List[str]:
        """生成修复建议"""
        recommendations = []
        
        if missing_refs:
            recommendations.append(f"需要补充 {len(missing_refs)} 个缺失的文献笔记")
        
        if apa_refs:
            recommendations.append(f"文档中已包含 {len(apa_refs)} 个APA格式引用")
        
        if self.citation_map:
            recommendations.append(f"可以替换 {len(self.citation_map)} 个DSAM引用为APA格式")
        
        if len(self.knowledge_bases) > 1:
            recommendations.append(f"已加载 {len(self.knowledge_bases)} 个知识库文件")
        
        return recommendations
    
    def _parse_authors(self, author_str: str) -> List[str]:
        """解析作者字符串，返回姓氏列表"""
        author_str = author_str.replace(' and ', ', ').replace(' & ', ', ')
        authors = [a.strip() for a in author_str.split(',') if a.strip()]
        
        surnames = []
        for author in authors:
            parts = author.split()
            if parts:
                surnames.append(parts[-1])
        
        return surnames
    
    def _format_apa_citation(self, authors: str, year: str) -> str:
        """格式化APA引用 (作者, 年份)"""
        surnames = self._parse_authors(authors)
        
        if len(surnames) == 1:
            return f"({surnames[0]}, {year})"
        elif len(surnames) == 2:
            return f"({surnames[0]} & {surnames[1]}, {year})"
        else:
            return f"({surnames[0]} et al., {year})"
    
    def _format_apa_citation_text(self, authors: str, year: str) -> str:
        """格式化APA引用（文本格式：作者等（年份））"""
        surnames = self._parse_authors(authors)
        
        if len(surnames) == 1:
            return f"{surnames[0]}（{year}）"
        elif len(surnames) == 2:
            return f"{surnames[0]}和{surnames[1]}（{year}）"
        else:
            return f"{surnames[0]}等（{year}）"
    
    # ========== 可选的修复方法 ==========
    
    def fix_references(self, doc_path: str, output_path: Optional[str] = None) -> Dict:
        """
        修复文档中的引用格式
        
        参数:
            doc_path: 输入文档路径
            output_path: 输出文档路径（可选，默认覆盖原文件）
            
        返回:
            修复结果字典
        """
        if not self.citation_map:
            return {"success": False, "error": "请先调用 check_references 构建引用映射"}
        
        content = self.content
        
        # 替换模式1: "DSAM_XXXX研究" -> "作者等（年份）的研究"
        for dsam_id, citation_text in self.citation_text_map.items():
            content = re.sub(rf'{dsam_id}研究', f'{citation_text}的研究', content)
        
        # 替换模式2: "（DSAM_XXXX）" -> "（作者, 年份）"
        for dsam_id, citation in self.citation_map.items():
            content = re.sub(rf'（{dsam_id}）', citation.replace('(', '（').replace(')', '）'), content)
            content = re.sub(rf'\({dsam_id}\)', citation, content)
        
        # 替换模式3: 单独出现的 "DSAM_XXXX"
        for dsam_id, citation_text in self.citation_text_map.items():
            content = re.sub(rf'(?<![A-Za-z0-9_]){dsam_id}(?![A-Za-z0-9_])', citation_text, content)
        
        # 保存结果
        save_path = output_path or doc_path
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 统计替换情况
        replaced = sum(1 for dsam_id in self.citation_map if dsam_id not in content)
        
        return {
            "success": True,
            "output_path": save_path,
            "total_references": len(self.citation_map),
            "replaced_count": replaced
        }


def main():
    """命令行入口（支持**kwargs风格的多个知识库参数）"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="ReferenceChecker - 参考文献检查与修复工具"
    )
    parser.add_argument("--doc", required=True, help="待检查的Markdown文档路径")
    parser.add_argument("--kb", required=True, help="知识库文件路径（可使用多个--kb参数）", action="append")
    parser.add_argument("--fix", action="store_true", help="修复引用（将DSAM引用替换为APA格式）")
    parser.add_argument("--output", help="修复后输出路径（仅在--fix时使用）")
    
    args = parser.parse_args()
    
    checker = ReferenceChecker()
    
    # 将 --kb 参数转换为 kwargs（kb1, kb2, kb3...）
    kb_kwargs = {}
    for i, kb_path in enumerate(args.kb, 1):
        kb_kwargs[f'kb{i}'] = kb_path
    
    # 检查引用
    print("正在检查参考文献...")
    print(f"已加载 {len(kb_kwargs)} 个知识库文件")
    results = checker.check_references(args.doc, **kb_kwargs)
    
    if not results["success"]:
        print(f"检查失败: {results.get('error', '未知错误')}")
        sys.exit(1)
    
    # 显示检查结果
    print(f"\n检查完成!")
    print(f"知识库文件数: {results['stats']['knowledge_base_count']}")
    print(f"DSAM引用总数: {results['stats']['dsam_total']}")
    print(f"唯一DSAM引用: {results['stats']['dsam_unique']}")
    print(f"缺失引用: {results['stats']['missing_count']}")
    
    if results["missing_references"]:
        print(f"\n缺失的引用: {results['missing_references']}")
    
    if results["recommendations"]:
        print(f"\n建议:")
        for rec in results["recommendations"]:
            print(f"  - {rec}")
    
    # 如果指定修复，则执行修复
    if args.fix:
        print(f"\n正在修复引用...")
        fix_result = checker.fix_references(args.doc, args.output)
        if fix_result["success"]:
            print(f"修复完成!")
            print(f"输出文件: {fix_result['output_path']}")
            print(f"总引用数: {fix_result['total_references']}")
            print(f"已替换: {fix_result['replaced_count']}")
        else:
            print(f"修复失败: {fix_result.get('error', '未知错误')}")
            sys.exit(1)


if __name__ == '__main__':
    main()
