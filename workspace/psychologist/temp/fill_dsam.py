
#!/usr/bin/env python3
"""
补全数字化存储与自传体记忆知识库元数据
"""

import sys
import os
import json
from datetime import datetime

# 添加knowledge-manager技能路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from AcademicSearchSummarizer import AcademicSearchSummarizer

KB_PATH = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"

def main():
    """主函数"""
    print("="*80)
    print("补全知识库元数据：数字化存储与自传体记忆")
    print("="*80)
    
    # 备份
    print("\n💾 备份知识库...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{KB_PATH}.metadata_backup_{timestamp}"
    import shutil
    shutil.copy2(KB_PATH, backup_path)
    print(f"  ✅ 已备份到: {backup_path}")
    
    # 初始化
    print("\n🔧 初始化 AcademicSearchSummarizer...")
    ass = AcademicSearchSummarizer()
    print("  ✅ 初始化成功！")
    
    # 读取并显示当前状态
    print("\n📊 当前状态:")
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    papers = kb["papers"]
    print(f"  文献总数: {len(papers)}")
    
    has_abstract = sum(1 for p in papers if p.get("abstract") and len(p["abstract"].strip()) > 0)
    has_doi = sum(1 for p in papers if p.get("doi") and len(p["doi"].strip()) > 0)
    has_volume = sum(1 for p in papers if p.get("volume") and len(p["volume"].strip()) > 0)
    has_issue = sum(1 for p in papers if p.get("issue") and len(p["issue"].strip()) > 0)
    has_pages = sum(1 for p in papers if p.get("pages") and len(p["pages"].strip()) > 0)
    
    print(f"  有摘要: {has_abstract}/{len(papers)} ({has_abstract/len(papers)*100:.1f}%)")
    print(f"  有DOI: {has_doi}/{len(papers)} ({has_doi/len(papers)*100:.1f}%)")
    print(f"  有卷号: {has_volume}/{len(papers)} ({has_volume/len(papers)*100:.1f}%)")
    print(f"  有期号: {has_issue}/{len(papers)} ({has_issue/len(papers)*100:.1f}%)")
    print(f"  有页码: {has_pages}/{len(papers)} ({has_pages/len(papers)*100:.1f}%)")
    
    # 补全元数据
    print("\n🚀 开始补全元数据...")
    try:
        count = ass.fill_metadata_from_kb(KB_PATH)
        print(f"\n✅ 成功补全 {count} 篇文献的元数据！")
    except Exception as e:
        print(f"\n❌ 补全失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 显示更新后状态
    print("\n📊 更新后状态:")
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    papers = kb["papers"]
    
    has_abstract = sum(1 for p in papers if p.get("abstract") and len(p["abstract"].strip()) > 0)
    has_doi = sum(1 for p in papers if p.get("doi") and len(p["doi"].strip()) > 0)
    has_volume = sum(1 for p in papers if p.get("volume") and len(p["volume"].strip()) > 0)
    has_issue = sum(1 for p in papers if p.get("issue") and len(p["issue"].strip()) > 0)
    has_pages = sum(1 for p in papers if p.get("pages") and len(p["pages"].strip()) > 0)
    
    print(f"  有摘要: {has_abstract}/{len(papers)} ({has_abstract/len(papers)*100:.1f}%)")
    print(f"  有DOI: {has_doi}/{len(papers)} ({has_doi/len(papers)*100:.1f}%)")
    print(f"  有卷号: {has_volume}/{len(papers)} ({has_volume/len(papers)*100:.1f}%)")
    print(f"  有期号: {has_issue}/{len(papers)} ({has_issue/len(papers)*100:.1f}%)")
    print(f"  有页码: {has_pages}/{len(papers)} ({has_pages/len(papers)*100:.1f}%)")
    
    print(f"\n{'='*80}")
    print("完成！")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
