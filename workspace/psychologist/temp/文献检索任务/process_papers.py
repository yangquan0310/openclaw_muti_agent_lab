#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
课堂拍照行为文献检索数据处理脚本

由于Semantic Scholar MCP服务暂时不可用，此脚本用于处理手动提供的文献数据。
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

# 文献分级标准
FOUNDATION_THRESHOLD = 500  # 🔴奠基
IMPORTANT_THRESHOLD = 50    # 🟡重要

def classify_importance(citation_count):
    """根据引用量分级"""
    if citation_count >= FOUNDATION_THRESHOLD:
        return "🔴奠基"
    elif citation_count >= IMPORTANT_THRESHOLD:
        return "🟡重要"
    else:
        return "🔵一般"

def classify_type(title, abstract):
    """根据标题和摘要分类文献类型"""
    title_lower = title.lower()
    abstract_lower = abstract.lower() if abstract else ""
    
    # 综述
    if any(kw in title_lower for kw in ['review', 'meta-analysis', 'systematic review']):
        return "📖综述"
    
    # 理论
    if any(kw in title_lower for kw in ['theoretical', 'theory', 'perspective', 'viewpoint']):
        return "💡理论"
    
    # 实证
    if any(kw in abstract_lower for kw in ['participant', 'subject', 'sample', 'method', 'result', 'experiment']):
        return "📊实证"
    
    return "📋待分类"

def process_papers(papers):
    """处理文献列表，添加标签"""
    processed = []
    for paper in papers:
        citation_count = paper.get('citation_count', 0)
        labels = {
            "importance": classify_importance(citation_count),
            "type": classify_type(paper.get('title', ''), paper.get('abstract', '')),
            "jcr_quartile": "待筛选"
        }
        paper['labels'] = labels
        processed.append(paper)
    return processed

def generate_statistics(papers):
    """生成统计信息"""
    stats = {
        "total_count": len(papers),
        "foundation_count": 0,
        "important_count": 0,
        "general_count": 0,
        "empirical_count": 0,
        "review_count": 0,
        "theory_count": 0
    }
    
    for paper in papers:
        labels = paper.get('labels', {})
        importance = labels.get('importance', '')
        doc_type = labels.get('type', '')
        
        if '🔴' in importance:
            stats["foundation_count"] += 1
        elif '🟡' in importance:
            stats["important_count"] += 1
        else:
            stats["general_count"] += 1
        
        if '📊' in doc_type:
            stats["empirical_count"] += 1
        elif '📖' in doc_type:
            stats["review_count"] += 1
        elif '💡' in doc_type:
            stats["theory_count"] += 1
    
    return stats

def generate_report(papers, stats, query):
    """生成检索报告"""
    report = f"""# 文献检索报告：{query}

> 检索时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 检索工具：手动整理（Semantic Scholar服务暂时不可用）

---

## 1. 检索概况

| 项目 | 内容 |
|------|------|
| 检索主题 | {query} |
| 检索词 | photo-taking, classroom, learning, cognitive load |
| 文献总数 | {stats['total_count']}篇 |
| 数据来源 | 手动整理 |

---

## 2. 文献统计

### 2.1 重要性分布

| 级别 | 数量 | 占比 |
|------|------|------|
| 🔴奠基（>500） | {stats['foundation_count']} | {stats['foundation_count']/stats['total_count']*100:.1f}% |
| 🟡重要（50-500） | {stats['important_count']} | {stats['important_count']/stats['total_count']*100:.1f}% |
| 🔵一般（<50） | {stats['general_count']} | {stats['general_count']/stats['total_count']*100:.1f}% |

### 2.2 文献类型分布

| 类型 | 数量 | 占比 |
|------|------|------|
| 📊实证研究 | {stats['empirical_count']} | {stats['empirical_count']/stats['total_count']*100:.1f}% |
| 📖综述 | {stats['review_count']} | {stats['review_count']/stats['total_count']*100:.1f}% |
| 💡理论 | {stats['theory_count']} | {stats['theory_count']/stats['total_count']*100:.1f}% |

---

## 3. 文献列表

"""
    
    # 按引用量排序
    sorted_papers = sorted(papers, key=lambda x: x.get('citation_count', 0), reverse=True)
    
    for i, paper in enumerate(sorted_papers[:30], 1):
        labels = paper.get('labels', {})
        report += f"""
### {i}. {paper.get('title', '')}

- **作者**：{', '.join(paper.get('authors', [])[:3])}{' et al.' if len(paper.get('authors', [])) > 3 else ''}
- **年份**：{paper.get('year', 'N/A')}
- **期刊**：{paper.get('venue', 'N/A')}
- **引用量**：{paper.get('citation_count', 0)}
- **标签**：{labels.get('importance', '')} {labels.get('type', '')}
- **DOI**：{paper.get('doi', 'N/A')}

**摘要**：
{paper.get('abstract', '无摘要')[:300]}...

---
"""
    
    return report

def main():
    if len(sys.argv) < 3:
        print("用法: python3 process_papers.py <输入JSON文件> <输出报告路径>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 加载文献数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    papers = data.get('papers', [])
    query = data.get('query', '课堂拍照行为对学习效果的影响')
    
    print(f"加载文献: {len(papers)}篇")
    
    # 处理文献
    processed_papers = process_papers(papers)
    
    # 生成统计
    stats = generate_statistics(processed_papers)
    
    # 生成报告
    report = generate_report(processed_papers, stats, query)
    
    # 保存报告
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 保存处理后的数据
    output_data = {
        "version": "1.0.0",
        "project": query,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "statistics": stats,
        "papers": processed_papers
    }
    
    data_file = output_file.replace('.md', '_data.json')
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 报告已保存: {output_file}")
    print(f"✅ 数据已保存: {data_file}")
    print(f"\n统计结果:")
    print(f"  总文献: {stats['total_count']}篇")
    print(f"  奠基文献: {stats['foundation_count']}篇")
    print(f"  重要文献: {stats['important_count']}篇")
    print(f"  一般文献: {stats['general_count']}篇")

if __name__ == "__main__":
    main()
