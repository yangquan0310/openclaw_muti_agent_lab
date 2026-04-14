
#!/usr/bin/env python3
"""
修改search方法，添加publicationTypes参数
"""

file_path = "/root/.openclaw/skills/knowledge-manager/AcademicSearchSummarizer.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_search_def = '''    def search(self, query: str, limit: int = 20, 
               fields: str = "title,authors,year,venue,citationCount,url,abstract") -&gt; List[Dict]:
        """
        检索文献
        
        Args:
            query: 检索关键词
            limit: 返回结果数量
            fields: 返回的字段（注意：doi字段不被支持）
            
        Returns:
            文献列表
        """
        params = {
            "query": query,
            "limit": limit,
            "fields": fields
        }'''

new_search_def = '''    def search(self, query: str, limit: int = 20, 
               fields: str = "title,authors,year,venue,citationCount,url,abstract",
               publication_types: str = "Review,MetaAnalysis") -&gt; List[Dict]:
        """
        检索文献
        
        Args:
            query: 检索关键词
            limit: 返回结果数量
            fields: 返回的字段（注意：doi字段不被支持）
            publication_types: 文献类型，默认只保留综述和元分析
            
        Returns:
            文献列表
        """
        params = {
            "query": query,
            "limit": limit,
            "fields": fields,
            "publicationTypes": publication_types
        }'''

if old_search_def in content:
    content = content.replace(old_search_def, new_search_def)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ search方法修改成功！")
else:
    print("❌ 未找到目标文本")
