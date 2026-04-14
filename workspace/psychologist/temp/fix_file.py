
#!/usr/bin/env python3
"""
修复AcademicSearchSummarizer.py文件
"""

file_path = "/root/.openclaw/skills/knowledge-manager/AcademicSearchSummarizer.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 问题：第141-142行可能有语法错误
# 让我用一个简单但完整的_fetch_paper_details方法替换

old_text = '''        return all_results
        
    def _fetch_paper_details(self, paper_id: str) -&gt; Optional[Dict[str, Any]]:
        """
        获取文献的完整元数据
        
        Args:
            paper_id: Semantic Scholar paper ID
            
        Returns:
            包含完整信息的字典，如果获取失败则返回 None
        """
        url = self.PAPER_URL.format(paper_id=paper_id)
        params = {
            "fields": "paperId,title,abstract,venue,year,journal,publicationVenue,citationCount,authors,externalIds"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 提取需要的字段
            result = {}
            
            # 基础字段
            if data.get("abstract"):
                result["abstract"] = data["abstract"]
            if data.get("venue"):
                result["venue"] = data["venue"]
            if data.get("year"):
                result["year"] = data["year"]
            if data.get("citationCount") is not None:
                result["citationCount"] = data["citationCount"]
            
            # 从journal对象中提取元数据（根据老板给的API响应格式）
            if data.get("journal"):
                journal = data["journal"]
                
                # 期刊名
                if journal.get("name"):
                    result["journal_name"] = journal["name"].strip()
                
                # 卷号 - 清理格式（去掉多余空格）
                if journal.get("volume"):
                    vol = journal["volume"].strip()
                    # 如果格式是 "107 2"，只取第一部分
                    if " " in vol:
                        vol = vol.split()[0]
                    result["volume"] = vol
                
                # 页码 - 清理格式（去掉多余换行和空格）
                if journal.get("pages"):
                    pages = journal["pages"].strip()
                    # 清理多余空白字符
                    pages = " ".join(pages.split())
                    result["pages"] = pages
            
            # 从externalIds中提取DOI（如果有的话）
            if data.get("externalIds"):
                external_ids = data["externalIds"]
                if external_ids.get("DOI"):
                    result["doi"] = external_ids["DOI"]
            
            return result if result else None
            
        except requests.RequestException as e:
            # 静默失败，不影响主流程
            return None

            
    def fetch_full_metadata'''

new_text = '''        return all_results
        
    def _fetch_paper_details(self, paper_id: str):
        """
        获取文献的完整元数据
        
        Args:
            paper_id: Semantic Scholar paper ID
            
        Returns:
            包含完整信息的字典，如果获取失败则返回 None
        """
        url = self.PAPER_URL.format(paper_id=paper_id)
        params = {
            "fields": "paperId,title,abstract,venue,year,journal,publicationVenue,citationCount,authors,externalIds"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            result = {}
            
            if data.get("abstract"):
                result["abstract"] = data["abstract"]
            if data.get("venue"):
                result["venue"] = data["venue"]
            if data.get("year"):
                result["year"] = data["year"]
            if data.get("citationCount") is not None:
                result["citationCount"] = data["citationCount"]
            
            if data.get("journal"):
                journal = data["journal"]
                if journal.get("name"):
                    result["journal_name"] = journal["name"].strip()
                if journal.get("volume"):
                    vol = journal["volume"].strip()
                    if " " in vol:
                        vol = vol.split()[0]
                    result["volume"] = vol
                if journal.get("pages"):
                    pages = journal["pages"].strip()
                    pages = " ".join(pages.split())
                    result["pages"] = pages
            
            if data.get("externalIds"):
                external_ids = data["externalIds"]
                if external_ids.get("DOI"):
                    result["doi"] = external_ids["DOI"]
            
            return result if result else None
            
        except Exception:
            return None
            
    def fetch_full_metadata'''

if old_text in content:
    content = content.replace(old_text, new_text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 文件修复成功！")
else:
    print("❌ 未找到目标文本")
    # 检查前200个字符
    print("\n文件开头内容:")
    print(repr(content[:500]))
