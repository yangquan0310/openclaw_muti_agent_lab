#!/usr/bin/env python3
"""
Semantic Scholar MCP Server
使用 Semantic Scholar API 进行论文搜索和检索
"""

import json
import os
import sys
from typing import Any, List, Dict, Optional
try:
    import httpx
    USE_HTTPX = True
except ImportError:
    import requests
    USE_HTTPX = False

# 从配置文件获取 API Key
CONFIG_PATH = os.path.expanduser("~/.openclaw/config/mcp/semantic_scholar_config.json")

def get_api_key() -> str:
    """从配置文件读取 API Key"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            return config.get('api_key', '')
    except:
        # 如果没有配置文件，使用环境变量或空字符串
        return os.environ.get('SEMANTIC_SCHOLAR_API_KEY', '')

def search_papers(query: str, limit: int = 10, fields: str = "title,authors,abstract,venue,year,citationCount") -> List[Dict[str, Any]]:
    """
    搜索论文
    
    Args:
        query: 搜索关键词
        limit: 返回结果数量
        fields: 返回字段列表
    
    Returns:
        论文列表
    """
    api_key = get_api_key()
    headers = {"x-api-key": api_key} if api_key else {}
    
    params = {
        "query": query,
        "limit": limit,
        "fields": fields
    }
    
    try:
        if USE_HTTPX:
            with httpx.Client() as client:
                response = client.get(
                    "https://api.semanticscholar.org/graph/v1/paper/search",
                    params=params,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        else:
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

def get_paper_details(paper_id: str, fields: str = "title,authors,abstract,venue,year,citationCount,references") -> Optional[Dict[str, Any]]:
    """
    获取论文详细信息
    
    Args:
        paper_id: 论文 ID
        fields: 返回字段列表
    
    Returns:
        论文详细信息
    """
    api_key = get_api_key()
    headers = {"x-api-key": api_key} if api_key else {}
    
    params = {
        "fields": fields
    }
    
    try:
        if USE_HTTPX:
            with httpx.Client() as client:
                response = client.get(
                    f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}",
                    params=params,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        else:
            response = requests.get(
                f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}",
                params=params,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"获取论文详情时出错: {e}", file=sys.stderr)
        return None

def format_paper_for_display(paper: Dict[str, Any]) -> str:
    """格式化论文信息用于显示"""
    title = paper.get("title", "Unknown")
    year = paper.get("year", "Unknown")
    venue = paper.get("venue", "Unknown")
    citation_count = paper.get("citationCount", 0)
    authors = ", ".join([author.get("name", "Unknown") for author in paper.get("authors", [])])
    abstract = paper.get("abstract", "No abstract available")
    if abstract is None:
        abstract = "No abstract available"
    
    return f"""📄 **{title}**
👥 作者: {authors}
📅 年份: {year}
🏛️ 会议/期刊: {venue}
📊 引用数: {citation_count}
📝 摘要: {abstract[:300]}{'...' if len(abstract) > 300 else ''}
"""

def main():
    """主函数，用于测试和命令行调用"""
    if len(sys.argv) < 2:
        print("Usage: python3 semantic_scholar_mcp.py <command> [args]", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  search <query> [limit] - 搜索论文", file=sys.stderr)
        print("  details <paper_id> - 获取论文详情", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        papers = search_papers(query, limit)
        
        print(f"找到 {len(papers)} 篇论文:\n")
        for i, paper in enumerate(papers, 1):
            print(f"{i}. " + "="*60)
            print(format_paper_for_display(paper))
            print()
    
    elif command == "details" and len(sys.argv) >= 3:
        paper_id = sys.argv[2]
        paper = get_paper_details(paper_id)
        
        if paper:
            print(format_paper_for_display(paper))
        else:
            print("未找到论文", file=sys.stderr)
            sys.exit(1)
    
    else:
        print(f"未知命令或参数不足: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()