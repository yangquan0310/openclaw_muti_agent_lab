#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('/root/.openclaw/.env')
SEMANTIC_SCHOLAR_API_KEY = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
ZOTERO_API_KEY = os.getenv('ZOTERO_API_KEY')
ZOTERO_USER_ID = os.getenv('ZOTERO_USER_ID')

# 配置
PROJECT_NAME = "2026-04-01_数字化存储与自传体记忆"
SEARCH_KEYWORDS = "photo-taking effect photo-taking impairment effect"
MAX_RESULTS = 50
TAGS = ["拍照效应", "数字化存储", "自传体记忆"]
PROJECT_INDEX_PATH = f"/root/实验室仓库/项目文件/{PROJECT_NAME}/知识库/index.json"

def search_semantic_scholar(keywords, max_results=50):
    """调用Semantic Scholar API检索文献"""
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {"x-api-key": SEMANTIC_SCHOLAR_API_KEY}
    params = {
        "query": keywords,
        "limit": max_results,
        "fields": "title,authors,year,abstract,doi,url,venue,citationCount"
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        papers = data.get('data', [])
        
        # 格式转换
        formatted_papers = []
        for paper in papers:
            authors = ", ".join([author.get('name', '') for author in paper.get('authors', [])])
            formatted_paper = {
                "title": paper.get('title', ''),
                "authors": authors,
                "year": paper.get('year'),
                "doi": paper.get('doi', ''),
                "abstract": paper.get('abstract', ''),
                "url": paper.get('url', ''),
                "venue": paper.get('venue', ''),
                "citationCount": paper.get('citationCount', 0),
                "tags": TAGS.copy(),
                "source": "semantic_scholar"
            }
            formatted_papers.append(formatted_paper)
        
        print(f"✅ Semantic Scholar检索完成，获取到 {len(formatted_papers)} 篇文献")
        return formatted_papers
    
    except Exception as e:
        print(f"❌ Semantic Scholar检索失败: {str(e)}")
        return []

def search_zotero(keywords):
    """检索Zotero本地库中的相关文献"""
    base_url = f"https://api.zotero.org/users/{ZOTERO_USER_ID}/items"
    headers = {
        "Zotero-API-Key": ZOTERO_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "q": keywords,
        "itemType": "-attachment",
        "limit": 100,
        "format": "json"
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        items = response.json()
        
        # 格式转换
        formatted_papers = []
        for item in items:
            data = item.get('data', {})
            creators = data.get('creators', [])
            authors = ", ".join([f"{creator.get('lastName', '')}, {creator.get('firstName', '')}" for creator in creators])
            
            formatted_paper = {
                "title": data.get('title', ''),
                "authors": authors,
                "year": int(data.get('date', '0000')[:4]) if data.get('date') else None,
                "doi": data.get('DOI', '').lower(),
                "abstract": data.get('abstractNote', ''),
                "url": data.get('url', ''),
                "venue": data.get('publicationTitle', ''),
                "citationCount": 0,
                "tags": TAGS.copy(),
                "source": "zotero_local"
            }
            formatted_papers.append(formatted_paper)
        
        print(f"✅ Zotero本地检索完成，获取到 {len(formatted_papers)} 篇文献")
        return formatted_papers
    
    except Exception as e:
        print(f"❌ Zotero检索失败: {str(e)}")
        return []

def merge_and_deduplicate(papers1, papers2):
    """合并两个文献列表，基于DOI去重"""
    seen_dois = set()
    merged = []
    
    # 优先保留Zotero中的文献
    for paper in papers2 + papers1:
        doi = paper.get('doi', '').strip().lower()
        if doi and doi in seen_dois:
            continue
        if doi:
            seen_dois.add(doi)
        merged.append(paper)
    
    print(f"✅ 合并去重完成，总共有 {len(merged)} 篇唯一文献")
    return merged

def load_existing_index():
    """加载现有项目知识库index.json"""
    if not os.path.exists(PROJECT_INDEX_PATH):
        # 创建空index结构
        os.makedirs(os.path.dirname(PROJECT_INDEX_PATH), exist_ok=True)
        empty_index = {
            "version": 1,
            "project": PROJECT_NAME,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "total_count": 0,
            "entries": []
        }
        with open(PROJECT_INDEX_PATH, 'w', encoding='utf-8') as f:
            json.dump(empty_index, f, ensure_ascii=False, indent=2)
        return empty_index
    
    with open(PROJECT_INDEX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def add_to_zotero(papers):
    """将新增文献添加到Zotero库"""
    base_url = f"https://api.zotero.org/users/{ZOTERO_USER_ID}/items"
    headers = {
        "Zotero-API-Key": ZOTERO_API_KEY,
        "Content-Type": "application/json"
    }
    
    added_count = 0
    for paper in papers:
        # 构造Zotero条目格式
        creators = []
        for author in paper.get('authors', '').split(', '):
            if ' ' in author:
                last, first = author.split(' ', 1)
                creators.append({"creatorType": "author", "lastName": last, "firstName": first})
        
        zotero_item = {
            "itemType": "journalArticle",
            "title": paper.get('title', ''),
            "creators": creators,
            "date": str(paper.get('year', '')) if paper.get('year') else '',
            "DOI": paper.get('doi', ''),
            "abstractNote": paper.get('abstract', ''),
            "url": paper.get('url', ''),
            "publicationTitle": paper.get('venue', ''),
            "tags": [{"tag": tag} for tag in paper.get('tags', [])]
        }
        
        try:
            response = requests.post(base_url, headers=headers, json=[zotero_item])
            response.raise_for_status()
            added_count += 1
        except Exception as e:
            print(f"⚠️ 添加文献到Zotero失败: {paper.get('title')[:50]}... - {str(e)}")
    
    print(f"✅ Zotero添加完成，共添加 {added_count} 篇新文献")
    return added_count

def update_project_index(new_papers):
    """更新项目知识库index.json"""
    index = load_existing_index()
    existing_dois = {entry.get('doi', '').strip().lower() for entry in index.get('entries', [])}
    
    # 筛选新增文献
    papers_to_add = []
    for paper in new_papers:
        doi = paper.get('doi', '').strip().lower()
        if doi not in existing_dois:
            papers_to_add.append(paper)
    
    if not papers_to_add:
        print("ℹ️ 没有需要添加到项目知识库的新文献")
        return 0, index
    
    # 分配自增ID
    max_id = max([entry.get('id', 0) for entry in index.get('entries', [])], default=0)
    now = datetime.now().isoformat()
    
    for i, paper in enumerate(papers_to_add):
        paper_entry = {
            "id": max_id + i + 1,
            "title": paper.get('title', ''),
            "authors": paper.get('authors', ''),
            "year": paper.get('year'),
            "doi": paper.get('doi', ''),
            "abstract": paper.get('abstract', ''),
            "url": paper.get('url', ''),
            "venue": paper.get('venue', ''),
            "citationCount": paper.get('citationCount', 0),
            "tags": paper.get('tags', []),
            "created_at": now,
            "updated_at": now
        }
        index['entries'].append(paper_entry)
    
    # 更新index元数据
    index['updated_at'] = now
    index['total_count'] = len(index['entries'])
    
    # 保存
    with open(PROJECT_INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 项目知识库更新完成，新增 {len(papers_to_add)} 篇文献")
    return len(papers_to_add), papers_to_add

def main():
    print("🔍 开始执行拍照效应文献检索任务...")
    print(f"关键词: {SEARCH_KEYWORDS}")
    print(f"目标项目: {PROJECT_NAME}")
    
    # 步骤1: 检索Semantic Scholar
    ss_papers = search_semantic_scholar(SEARCH_KEYWORDS, MAX_RESULTS)
    
    # 步骤2: 检索Zotero本地库
    zotero_papers = search_zotero(SEARCH_KEYWORDS)
    
    # 步骤3: 合并去重
    all_papers = merge_and_deduplicate(ss_papers, zotero_papers)
    
    # 步骤4: 与现有知识库比对，筛选新增文献
    index = load_existing_index()
    existing_dois = {entry.get('doi', '').strip().lower() for entry in index.get('entries', [])}
    
    new_papers = []
    existing_papers = []
    for paper in all_papers:
        doi = paper.get('doi', '').strip().lower()
        if doi and doi in existing_dois:
            existing_papers.append(paper)
        else:
            new_papers.append(paper)
    
    print(f"\n📊 检索统计:")
    print(f"  Semantic Scholar获取: {len(ss_papers)} 篇")
    print(f"  Zotero本地获取: {len(zotero_papers)} 篇")
    print(f"  合并去重后总文献: {len(all_papers)} 篇")
    print(f"  项目知识库已有: {len(existing_papers)} 篇")
    print(f"  新增文献: {len(new_papers)} 篇")
    
    if new_papers:
        # 步骤5: 添加到Zotero
        added_to_zotero = add_to_zotero(new_papers)
        
        # 步骤6: 更新项目知识库
        added_to_index, added_papers = update_project_index(new_papers)
        
        # 输出新增文献列表
        print(f"\n📋 新增文献列表 ({len(added_papers)} 篇):")
        for i, paper in enumerate(added_papers, 1):
            print(f"{i}. [{paper.get('year', '无年份')}] {paper.get('title', '无标题')}")
            print(f"   作者: {paper.get('authors', '无作者')}")
            print(f"   DOI: {paper.get('doi', '无DOI')}")
            print(f"   来源: {paper.get('source', '未知')}")
            print()
    else:
        print("\n🎉 没有新的文献需要添加，检索任务完成。")
    
    print("✅ 拍照效应文献检索任务全部完成！")

if __name__ == "__main__":
    main()
