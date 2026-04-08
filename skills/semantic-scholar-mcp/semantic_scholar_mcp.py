#!/usr/bin/env python3
"""
Semantic Scholar MCP Server
符合 Model Context Protocol 标准的 Semantic Scholar 检索服务
"""

import json
import os
import sys
import asyncio
from typing import Any, List, Dict, Optional
try:
    import httpx
    USE_HTTPX = True
except ImportError:
    import requests
    USE_HTTPX = False

# 从环境变量获取 API Key
def get_api_key() -> str:
    """从环境变量读取 API Key"""
    return os.environ.get('SEMANTIC_SCHOLAR_API_KEY', '')

def search_papers(query: str, limit: int = 10, fields: str = "title,authors,abstract,venue,year,citationCount,url,doi") -> List[Dict[str, Any]]:
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
        "fields": "title,authors,abstract,venue,year,citationCount,url"
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
                return response.json().get('data', [])
        else:
            response = requests.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params=params,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json().get('data', [])
    except Exception as e:
        print(f"搜索论文时出错: {e}", file=sys.stderr)
        return []

def get_paper_details(paper_id: str, fields: str = "title,authors,abstract,venue,year,citationCount,url,doi,references") -> Optional[Dict[str, Any]]:
    """
    获取论文详情
    
    Args:
        paper_id: Semantic Scholar 论文 ID
        fields: 返回字段列表
    
    Returns:
        论文详情
    """
    api_key = get_api_key()
    headers = {"x-api-key": api_key} if api_key else {}
    
    params = {"fields": "title,authors,abstract,venue,year,citationCount,url"}

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

# ==============================
# MCP 协议实现
# ==============================

def send_message(message: Dict[str, Any]) -> None:
    """发送 JSON-RPC 消息到 stdout"""
    print(json.dumps(message), flush=True)

def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """处理 JSON-RPC 请求"""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    # MCP 标准方法
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": True
                    }
                },
                "serverInfo": {
                    "name": "semantic-scholar",
                    "version": "1.0.0"
                }
            }
        }
    
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "semantic_scholar_search",
                        "description": "搜索 Semantic Scholar 学术文献",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "搜索关键词"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "返回结果数量",
                                    "default": 10
                                }
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "semantic_scholar_get_details",
                        "description": "获取论文详细信息",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "paper_id": {
                                    "type": "string",
                                    "description": "Semantic Scholar 论文 ID"
                                }
                            },
                            "required": ["paper_id"]
                        }
                    }
                ]
            }
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_params = params.get("arguments", {})

        if tool_name == "semantic_scholar_search":
            query = tool_params.get("query")
            limit = tool_params.get("limit", 10)
            papers = search_papers(query, limit)
            
            # 格式化结果
            result = []
            for paper in papers:
                authors = ", ".join([author.get("name", "Unknown") for author in paper.get("authors", [])])
                result.append({
                    "title": paper.get("title", "Unknown"),
                    "authors": authors,
                    "year": paper.get("year", "Unknown"),
                    "venue": paper.get("venue", "Unknown"),
                    "citationCount": paper.get("citationCount", 0),
                    "doi": paper.get("doi", ""),
                    "url": paper.get("url", ""),
                    "abstract": paper.get("abstract", "No abstract available")
                })
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            }
        
        elif tool_name == "semantic_scholar_get_details":
            paper_id = tool_params.get("paper_id")
            paper = get_paper_details(paper_id)
            
            if not paper:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "未找到论文"
                    }
                }
            
            authors = ", ".join([author.get("name", "Unknown") for author in paper.get("authors", [])])
            result = {
                "title": paper.get("title", "Unknown"),
                "authors": authors,
                "year": paper.get("year", "Unknown"),
                "venue": paper.get("venue", "Unknown"),
                "citationCount": paper.get("citationCount", 0),
                "doi": paper.get("doi", ""),
                "url": paper.get("url", ""),
                "abstract": paper.get("abstract", "No abstract available"),
                "references": paper.get("references", [])
            }
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"未知工具: {tool_name}"
                }
            }
    
    elif method == "notifications/initialized":
        # 初始化完成通知，无需返回
        return None
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"未知方法: {method}"
            }
        }

async def main():
    """MCP 服务器主循环"""
    # 支持命令行调用模式（向后兼容）
    if len(sys.argv) > 1 and sys.argv[1] in ["search", "details"]:
        command = sys.argv[1]
        
        if command == "search" and len(sys.argv) >= 3:
            query = sys.argv[2]
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            papers = search_papers(query, limit)
            
            print(f"找到 {len(papers)} 篇论文:\n")
            for i, paper in enumerate(papers, 1):
                authors = ", ".join([author.get("name", "Unknown") for author in paper.get("authors", [])])
                abstract = paper.get("abstract", "No abstract available")
                if abstract is None:
                    abstract = "No abstract available"
                
                print(f"{i}. 📄 **{paper.get('title', 'Unknown')}**")
                print(f"   👥 作者: {authors}")
                print(f"   📅 年份: {paper.get('year', 'Unknown')}")
                print(f"   🏛️ 会议/期刊: {paper.get('venue', 'Unknown')}")
                print(f"   📊 引用数: {paper.get('citationCount', 0)}")
                print(f"   🔗 DOI: {paper.get('doi', 'N/A')}")
                print(f"   📝 摘要: {abstract[:300]}{'...' if len(abstract) > 300 else ''}\n")
        
        elif command == "details" and len(sys.argv) >= 3:
            paper_id = sys.argv[2]
            paper = get_paper_details(paper_id)
            
            if paper:
                authors = ", ".join([author.get("name", "Unknown") for author in paper.get("authors", [])])
                abstract = paper.get("abstract", "No abstract available")
                if abstract is None:
                    abstract = "No abstract available"
                
                print(f"📄 **{paper.get('title', 'Unknown')}**")
                print(f"👥 作者: {authors}")
                print(f"📅 年份: {paper.get('year', 'Unknown')}")
                print(f"🏛️ 会议/期刊: {paper.get('venue', 'Unknown')}")
                print(f"📊 引用数: {paper.get('citationCount', 0)}")
                print(f"🔗 DOI: {paper.get('doi', 'N/A')}")
                print(f"📝 摘要: {abstract}\n")
            else:
                print("未找到论文", file=sys.stderr)
                sys.exit(1)
        
        return

    # MCP 标准输入输出模式
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            response = handle_request(request)
            
            if response is not None:
                send_message(response)
                
        except Exception as e:
            print(f"处理请求出错: {e}", file=sys.stderr)
            continue

if __name__ == "__main__":
    asyncio.run(main())
