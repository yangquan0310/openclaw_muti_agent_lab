
#!/usr/bin/env python3
"""
补全知识库元数据脚本
使用AcademicSearchSummarizer的fill_metadata_from_kb方法
"""

import sys
import os

# 添加knowledge-manager技能路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from AcademicSearchSummarizer import AcademicSearchSummarizer

# 知识库路径
KB_PATHS = {
    "学生论文修改": "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json",
    "数字化存储与自传体记忆": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json",
    "跨期选择的年龄差异": "/root/实验室仓库/项目文件/跨期选择的年龄差异/知识库/index.json"
}

def main():
    """主函数"""
    print("="*80)
    print("知识库元数据补全工具")
    print("="*80)
    
    # 初始化
    print("\n🔧 初始化 AcademicSearchSummarizer...")
    ass = AcademicSearchSummarizer()
    print("  ✅ 初始化成功！")
    
    # 按顺序处理三个知识库
    kb_order = [
        "数字化存储与自传体记忆",  # 优先：已有100%摘要
        "学生论文修改",
        "跨期选择的年龄差异"
    ]
    
    for kb_name in kb_order:
        kb_path = KB_PATHS[kb_name]
        
        print(f"\n{'='*80}")
        print(f"处理知识库: {kb_name}")
        print(f"路径: {kb_path}")
        print(f"{'='*80}")
        
        if not os.path.exists(kb_path):
            print(f"❌ 文件不存在！跳过")
            continue
        
        try:
            count = ass.fill_metadata_from_kb(kb_path)
            print(f"\n✅ 成功补全 {count} 篇文献的元数据！")
            
            # 再次核查
            print(f"\n📊 更新后统计:")
            import json
            with open(kb_path, 'r', encoding='utf-8') as f:
                kb = json.load(f)
            
            papers = kb["papers"]
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
            
        except Exception as e:
            print(f"\n❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("所有知识库处理完成！")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
