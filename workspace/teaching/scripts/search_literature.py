#!/usr/bin/env python3
"""
小学教育文献检索脚本
使用 Semantic Scholar API 检索真实文献
"""

import json
import os
import sys
import requests
from typing import List, Dict, Any

# API 配置
CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/skills/semantic-scholar-mcp/semantic_scholar_config.json")

def get_api_key() -> str:
    """从配置文件读取 API Key"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            return config.get('api_key', '')
    except:
        return os.environ.get('SEMANTIC_SCHOLAR_API_KEY', '')

def search_papers(query: str, limit: int = 10, fields: str = "title,authors,abstract,venue,year,citationCount,url,externalIds") -> List[Dict[str, Any]]:
    """搜索论文"""
    api_key = get_api_key()
    headers = {"x-api-key": api_key} if api_key else {}
    
    params = {
        "query": query,
        "limit": limit,
        "fields": fields
    }
    
    try:
        response = requests.get(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            params=params,
            headers=headers,
            timeout=30.0
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"搜索论文时出错: {e}", file=sys.stderr)
        return []

def format_paper(paper: Dict[str, Any]) -> Dict[str, Any]:
    """格式化论文信息"""
    title = paper.get("title", "Unknown")
    year = paper.get("year", "Unknown")
    venue = paper.get("venue", "Unknown")
    citation_count = paper.get("citationCount", 0)
    authors = ", ".join([author.get("name", "Unknown") for author in paper.get("authors", [])])
    abstract = paper.get("abstract", "No abstract available")
    if abstract is None:
        abstract = "No abstract available"
    
    # 获取 DOI
    external_ids = paper.get("externalIds", {})
    doi = external_ids.get("DOI", "N/A")
    url = paper.get("url", "N/A")
    
    return {
        "title": title,
        "authors": authors,
        "year": year,
        "venue": venue,
        "citation_count": citation_count,
        "abstract": abstract,
        "doi": doi,
        "url": url
    }

def main():
    """主函数"""
    # 搜索关键词列表
    search_queries = [
        "primary education empirical research",
        "elementary school teaching effectiveness",
        "elementary education classroom management",
        "elementary school mathematics teaching",
        "elementary school reading instruction",
        "educational psychology elementary school"
    ]
    
    all_papers = []
    
    print("开始检索小学教育专业期刊文献...\n")
    
    for query in search_queries:
        print(f"搜索关键词: {query}")
        papers = search_papers(query, limit=8)
        for paper in papers:
            formatted = format_paper(paper)
            # 只保留有DOI的期刊论文
            if formatted["doi"] != "N/A" and formatted["venue"]:
                all_papers.append(formatted)
        print(f"  找到 {len(papers)} 篇论文\n")
    
    # 按引用数排序
    all_papers.sort(key=lambda x: x["citation_count"], reverse=True)
    
    # 输出结果
    print("="*80)
    print("小学教育专业期刊文献检索结果")
    print("="*80)
    print(f"共找到 {len(all_papers)} 篇有DOI的文献\n")
    
    for i, paper in enumerate(all_papers, 1):
        print(f"{i}. {paper['title']}")
        print(f"   作者: {paper['authors']}")
        print(f"   年份: {paper['year']}")
        print(f"   期刊: {paper['venue']}")
        print(f"   引用数: {paper['citation_count']}")
        print(f"   DOI: {paper['doi']}")
        print(f"   摘要: {paper['abstract'][:200]}...")
        print()
    
    # 保存结果到文件
    output_file = os.path.expanduser("~/literature_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
