
#!/usr/bin/env python3
"""
修改_fetch_paper_details方法
"""

file_path = "/root/.openclaw/skills/knowledge-manager/AcademicSearchSummarizer.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_method = '''    def _fetch_paper_details(self, paper_id: str) -&gt; Optional[Dict[str, Any]]:
        """
        获取文献的完整元数据
        
        Args:
            paper_id: Semantic Scholar paper ID
            
        Returns:
            包含完整信息的字典，如果获取失败则返回 None
        """
        url = self.PAPER_URL.format(paper_id=paper_id)
        params = {
            "fields": "abstract,venue,year,journal,volume,issue,pages,doi,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,authors"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 提取需要的字段
            result = {}
            if data.get('abstract'):
                result['abstract'] = data['abstract']
            if data.get('venue'):
                result['venue'] = data['venue']
            if data.get('journal'):
                result['journal'] = data['journal']
                if data['journal'].get('name'):
                    result['journal_name'] = data['journal']['name']
                if data['journal'].get('volume'):
                    result['journal_volume'] = data['journal']['volume']
                if data['journal'].get('issue'):
                    result['journal_issue'] = data['journal']['issue']
                if data['journal'].get('pages'):
                    result['journal_pages'] = data['journal']['pages']
            if data.get('doi'):
                result['doi'] = data['doi']
            if data.get('citationCount') is not None:
                result['citationCount'] = data['citationCount']
            if data.get('isOpenAccess') is not None:
                result['isOpenAccess'] = data['isOpenAccess']
            if data.get('openAccessPdf'):
                result['openAccessPdf'] = data['openAccessPdf']
            if data.get('authors'):
                result['authors'] = data['authors']
                # 提取作者姓名列表（兼容现有格式）
                result['author_names'] = [a['name'] for a in data['authors'] if a.get('name')]
            
            return result if result else None
            
        except requests.RequestException as e:
            # 静默失败，不影响主流程
            return None'''

new_method = '''    def _fetch_paper_details(self, paper_id: str) -&gt; Optional[Dict[str, Any]]:
        """
        获取文献的完整元数据
        
        Args:
            paper_id: Semantic Scholar paper ID
            
        Returns:
            包含完整信息的字典，如果获取失败则返回 None
        """
        url = self.PAPER_URL.format(paper_id=paper_id)
        params = {
            "fields": "paperId,title,abstract,venue,year,journal,publicationVenue,citationCount,authors"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 提取需要的字段
            result = {}
            
            # 基础字段
            if data.get('abstract'):
                result['abstract'] = data['abstract']
            if data.get('venue'):
                result['venue'] = data['venue']
            if data.get('year'):
                result['year'] = data['year']
            if data.get('citationCount') is not None:
                result['citationCount'] = data['citationCount']
            
            # 从journal对象中提取元数据（根据老板给的API响应格式）
            if data.get('journal'):
                journal = data['journal']
                
                # 期刊名
                if journal.get('name'):
                    result['journal_name'] = journal['name'].strip()
                
                # 卷号 - 清理格式（去掉多余空格）
                if journal.get('volume'):
                    vol = journal['volume'].strip()
                    # 如果格式是 "107 2"，只取第一部分
                    if ' ' in vol:
                        vol = vol.split()[0]
                    result['volume'] = vol
                
                # 页码 - 清理格式（去掉多余换行和空格）
                if journal.get('pages'):
                    pages = journal['pages'].strip()
                    # 清理多余空白字符
                    pages = ' '.join(pages.split())
                    result['pages'] = pages
            
            # 从externalIds中提取DOI（如果有的话）
            if data.get('externalIds'):
                external_ids = data['externalIds']
                if external_ids.get('DOI'):
                    result['doi'] = external_ids['DOI']
            
            return result if result else None
            
        except requests.RequestException as e:
            # 静默失败，不影响主流程
            return None'''

if old_method in content:
    content = content.replace(old_method, new_method)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ _fetch_paper_details方法更新成功！")
else:
    print("❌ 未找到目标方法，让我检查一下内容...")
    # 输出这部分看看
    lines = content.split('\n')
    for i, line in enumerate(lines[135:220]):
        print(f"{135+i}: {line}")
