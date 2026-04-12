#!/usr/bin/env python3
"""
简单的文献检索脚本
"""

import json
import os
import sys
import requests

# 使用配置文件中的API key
CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/skills/semantic-scholar-mcp/semantic_scholar_config.json")

def get_api_key():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            return config.get('api_key', '')
    except:
        return ''

def search_and_save(query, filename):
    api_key = get_api_key()
    headers = {"x-api-key": api_key} if api_key else {}
    
    params = {
        "query": query,
        "limit": 10,
        "fields": "title,authors,abstract,venue,year,citationCount,externalIds"
    }
    
    try:
        response = requests.get(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            params=params,
            headers=headers,
            timeout=60.0
        )
        response.raise_for_status()
        data = response.json()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(data.get('data', []))} papers to {filename}")
        return data.get('data', [])
    except Exception as e:
        print(f"Error: {e}")
        return []

# 主程序
if __name__ == "__main__":
    queries = [
        "primary education empirical research",
        "elementary school teaching effectiveness", 
        "elementary classroom management research",
        "elementary mathematics education research"
    ]
    
    all_papers = []
    
    for i, query in enumerate(queries):
        print(f"\nSearching: {query}")
        papers = search_and_save(query, f"/tmp/papers_{i}.json")
        all_papers.extend(papers)
    
    # 整理并保存所有结果
    output = []
    for paper in all_papers:
        external_ids = paper.get('externalIds', {})
        doi = external_ids.get('DOI', 'N/A')
        
        if doi != 'N/A' and paper.get('venue'):
            output.append({
                'title': paper.get('title', ''),
                'authors': ', '.join([a.get('name', '') for a in paper.get('authors', [])]),
                'year': paper.get('year', ''),
                'venue': paper.get('venue', ''),
                'citationCount': paper.get('citationCount', 0),
                'doi': doi,
                'abstract': paper.get('abstract', 'No abstract')
            })
    
    # 按引用数排序
    output.sort(key=lambda x: x['citationCount'], reverse=True)
    
    # 保存最终结果
    with open('/tmp/final_papers.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal unique papers with DOI: {len(output)}")
    print("Saved to /tmp/final_papers.json")
