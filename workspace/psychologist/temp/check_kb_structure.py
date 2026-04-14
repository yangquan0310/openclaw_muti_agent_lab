
#!/usr/bin/env python3
"""
知识库结构核查脚本
检查三个知识库是否符合知识库结构.md的规范
"""

import json
import os
from pathlib import Path

# 预期字段顺序（按知识库结构.md）
EXPECTED_FIELD_ORDER = [
    "id",
    "paperId",
    "authors",
    "year",
    "title",
    "venue",
    "volume",
    "issue",
    "pages",
    "doi",
    "url",
    "abstract",
    "topic",
    "citationCount",
    "labels",
    "notes"
]

# 知识库路径
KB_PATHS = {
    "学生论文修改": "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json",
    "数字化存储与自传体记忆": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json",
    "跨期选择的年龄差异": "/root/实验室仓库/项目文件/跨期选择的年龄差异/知识库/index.json"
}

def check_kb_structure(kb_path, kb_name):
    """核查单个知识库结构"""
    print(f"\n{'='*80}")
    print(f"知识库: {kb_name}")
    print(f"路径: {kb_path}")
    print(f"{'='*80}")
    
    if not os.path.exists(kb_path):
        print(f"❌ 文件不存在！")
        return False
    
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb = json.load(f)
    except Exception as e:
        print(f"❌ JSON解析失败: {e}")
        return False
    
    # 检查顶层字段
    print(f"\n📋 顶层字段检查:")
    expected_top_fields = ["version", "project", "created_at", "updated_at", "statistics", "papers"]
    for field in expected_top_fields:
        if field in kb:
            print(f"  ✅ {field}")
        else:
            print(f"  ❌ {field} - 缺失")
    
    # 检查statistics字段
    print(f"\n📊 statistics字段检查:")
    expected_stats_fields = ["total_count", "foundation_count", "important_count", "general_count", 
                            "empirical_count", "review_count", "theory_count"]
    if "statistics" in kb:
        for field in expected_stats_fields:
            if field in kb["statistics"]:
                print(f"  ✅ {field}: {kb['statistics'][field]}")
            else:
                print(f"  ❌ {field} - 缺失")
    else:
        print(f"  ❌ statistics字段缺失")
    
    # 检查papers字段
    print(f"\n📚 papers字段检查:")
    if "papers" not in kb:
        print(f"  ❌ papers字段缺失")
        return False
    
    papers = kb["papers"]
    if not isinstance(papers, list):
        print(f"  ❌ papers不是list类型！是: {type(papers)}")
        return False
    
    print(f"  ✅ papers是list类型，共{len(papers)}篇文献")
    
    if len(papers) == 0:
        print(f"  ⚠️  没有文献")
        return True
    
    # 检查第一篇文献的字段顺序
    first_paper = papers[0]
    print(f"\n🔍 第一篇文献字段顺序检查:")
    actual_fields = list(first_paper.keys())
    
    print(f"  预期字段顺序: {EXPECTED_FIELD_ORDER}")
    print(f"  实际字段顺序: {actual_fields}")
    
    # 检查字段顺序是否匹配
    order_ok = True
    for i, (expected, actual) in enumerate(zip(EXPECTED_FIELD_ORDER, actual_fields)):
        if expected != actual:
            print(f"  ❌ 位置{i}: 预期'{expected}', 实际'{actual}'")
            order_ok = False
    
    if order_ok:
        print(f"  ✅ 字段顺序正确")
    
    # 统计摘要完整性
    print(f"\n📝 摘要完整性统计:")
    has_abstract = 0
    has_doi = 0
    has_volume = 0
    has_issue = 0
    has_pages = 0
    
    for paper in papers:
        if paper.get("abstract") and len(paper["abstract"].strip()) > 0:
            has_abstract += 1
        if paper.get("doi") and len(paper["doi"].strip()) > 0:
            has_doi += 1
        if paper.get("volume") and len(paper["volume"].strip()) > 0:
            has_volume += 1
        if paper.get("issue") and len(paper["issue"].strip()) > 0:
            has_issue += 1
        if paper.get("pages") and len(paper["pages"].strip()) > 0:
            has_pages += 1
    
    total = len(papers)
    print(f"  有摘要: {has_abstract}/{total} ({has_abstract/total*100:.1f}%)")
    print(f"  有DOI: {has_doi}/{total} ({has_doi/total*100:.1f}%)")
    print(f"  有卷号: {has_volume}/{total} ({has_volume/total*100:.1f}%)")
    print(f"  有期号: {has_issue}/{total} ({has_issue/total*100:.1f}%)")
    print(f"  有页码: {has_pages}/{total} ({has_pages/total*100:.1f}%)")
    
    return True

def main():
    """主函数"""
    print("="*80)
    print("知识库结构核查工具")
    print("="*80)
    
    for kb_name, kb_path in KB_PATHS.items():
        check_kb_structure(kb_path, kb_name)
    
    print(f"\n{'='*80}")
    print("核查完成")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
