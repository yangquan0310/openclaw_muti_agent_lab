
#!/usr/bin/env python3
"""
通过标题重新检索来补全元数据
"""

import os
import sys
import json
import time
import requests
import shutil
from datetime import datetime

# 添加knowledge-manager技能路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

# 设置环境变量
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

# 知识库路径
KB_PATHS = {
    "学生论文修改": "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json",
    "数字化存储与自传体记忆": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json",
    "跨期选择的年龄差异": "/root/实验室仓库/项目文件/跨期选择的年龄差异/知识库/index.json"
}

def backup_kb(kb_path):
    """备份知识库"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{kb_path}.refresh_backup_{timestamp}"
    shutil.copy2(kb_path, backup_path)
    return backup_path

def search_paper_by_title(title):
    """通过标题搜索文献并获取完整元数据"""
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    headers = {
        "Accept": "application/json",
        "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
    }
    
    # 用标题的前60个字符搜索（避免太长）
    search_query = title[:60] if len(title) &gt; 60 else title
    
    params = {
        "query": search_query,
        "limit": 3,
        "fields": "paperId,title,authors,year,venue,abstract"
    }
    
    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        papers = data.get('data', [])
        
        if not papers:
            return None
        
        # 找标题最匹配的
        best_match = None
        best_score = 0
        
        for paper in papers:
            paper_title = paper.get('title', '').lower()
            target_title = title.lower()
            
            # 简单的匹配分数：重叠词数
            words1 = set(paper_title.split())
            words2 = set(target_title.split())
            overlap = len(words1 &amp; words2)
            score = overlap / max(len(words1), len(words2), 1)
            
            if score &gt; best_score:
                best_score = score
                best_match = paper
        
        if best_match and best_score &gt; 0.5:  # 至少50%匹配
            # 现在尝试获取这篇文献的完整元数据
            paper_id = best_match['paperId']
            return fetch_paper_details(paper_id)
        
        return None
        
    except Exception as e:
        # print(f"  搜索失败: {e}")
        return None
    finally:
        time.sleep(0.3)  # 延迟避免速率限制

def fetch_paper_details(paper_id):
    """获取文献完整元数据"""
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper"
    
    headers = {
        "Accept": "application/json",
        "x-api-key": os.environ['SEMANTIC_SCHOLAR_API_KEY']
    }
    
    url = f"{BASE_URL}/{paper_id}"
    params = {
        "fields": "abstract,venue,year,journal,volume,issue,pages,doi,citationCount,isOpenAccess,openAccessPdf,authors"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # 提取需要的字段
            result = {}
            
            # 标准字段
            if data.get('abstract'):
                result['abstract'] = data['abstract']
            if data.get('venue'):
                result['venue'] = data['venue']
            if data.get('year'):
                result['year'] = data['year']
            if data.get('doi'):
                result['doi'] = data['doi']
            if data.get('citationCount') is not None:
                result['citationCount'] = data['citationCount']
            
            # 期刊信息（注意：Semantic Scholar返回的结构）
            if data.get('journal'):
                journal = data['journal']
                if journal.get('name'):
                    result['journal_name'] = journal['name']
                if journal.get('volume'):
                    result['volume'] = journal['volume']
                if journal.get('issue'):
                    result['issue'] = journal['issue']
                if journal.get('pages'):
                    result['pages'] = journal['pages']
            
            return result
            
        return None
        
    except Exception as e:
        # print(f"  获取详情失败: {e}")
        return None
    finally:
        time.sleep(0.2)

def refresh_kb(kb_name, kb_path):
    """刷新单个知识库"""
    print(f"\n{'='*80}")
    print(f"刷新知识库: {kb_name}")
    print(f"路径: {kb_path}")
    print(f"{'='*80}")
    
    # 备份
    backup_path = backup_kb(kb_path)
    print(f"✅ 已备份到: {backup_path}")
    
    # 读取现有知识库
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    papers = kb['papers']
    print(f"\n📋 开始处理 {len(papers)} 篇文献...")
    
    success_count = 0
    doi_count = 0
    volume_count = 0
    issue_count = 0
    pages_count = 0
    
    for i, paper in enumerate(papers):
        title = paper.get('title', '')
        
        if i % 10 == 0:
            print(f"  进度: {i}/{len(papers)} ({i/len(papers)*100:.1f}%)")
        
        if not title:
            continue
        
        # 通过标题搜索
        full_data = search_paper_by_title(title)
        
        if full_data:
            # 更新字段
            updated = False
            
            for key, value in full_data.items():
                # 只更新空值或更好的值
                if key in paper:
                    if not paper.get(key) or str(paper.get(key)).strip() == "":
                        paper[key] = value
                        updated = True
                else:
                    paper[key] = value
                    updated = True
            
            if updated:
                success_count += 1
                if full_data.get('doi'):
                    doi_count += 1
                if full_data.get('volume'):
                    volume_count += 1
                if full_data.get('issue'):
                    issue_count += 1
                if full_data.get('pages'):
                    pages_count += 1
    
    # 更新updated_at
    kb['updated_at'] = datetime.now().isoformat()
    
    # 保存
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 刷新完成！")
    print(f"  成功更新: {success_count}/{len(papers)} 篇")
    print(f"  新增DOI: {doi_count}")
    print(f"  新增卷号: {volume_count}")
    print(f"  新增期号: {issue_count}")
    print(f"  新增页码: {pages_count}")
    
    # 最终统计
    print(f"\n📊 最终状态:")
    has_abstract = sum(1 for p in papers if p.get('abstract') and len(p['abstract'].strip()) &gt; 0)
    has_doi = sum(1 for p in papers if p.get('doi') and len(p['doi'].strip()) &gt; 0)
    has_volume = sum(1 for p in papers if p.get('volume') and len(p['volume'].strip()) &gt; 0)
    has_issue = sum(1 for p in papers if p.get('issue') and len(p['issue'].strip()) &gt; 0)
    has_pages = sum(1 for p in papers if p.get('pages') and len(p['pages'].strip()) &gt; 0)
    
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
    print("通过标题重新检索补全元数据")
    print("="*80)
    
    # 按顺序处理
    kb_order = [
        "数字化存储与自传体记忆",
        "学生论文修改",
        "跨期选择的年龄差异"
    ]
    
    for kb_name in kb_order:
        kb_path = KB_PATHS[kb_name]
        
        if not os.path.exists(kb_path):
            print(f"\n❌ 文件不存在: {kb_path}")
            continue
        
        try:
            refresh_kb(kb_name, kb_path)
        except Exception as e:
            print(f"\n❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("所有知识库处理完成！")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
