
#!/usr/bin/env python3
"""
重构AcademicSearchSummarizer.py
"""

file_path = "/root/.openclaw/skills/knowledge-manager/AcademicSearchSummarizer.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 第一步：简化Searcher类，只保留search和get_paper_details两个方法
# search: relevance search，返回原始数据
# get_paper_details: details search，返回原始数据
# 去掉search_multiple、fetch_full_metadata等方法

old_searcher_class = '''# ============================================================================
# Searcher: 文献检索类
# ============================================================================

class Searcher:
    """
    从 Semantic Scholar 检索文献
    
    使用 Semantic Scholar API 进行文献检索，支持多关键词、多轮次检索。
    """
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper"
    SEARCH_URL= "https://api.semanticscholar.org/graph/v1/paper/search"
    PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Searcher
        
        Args:
            api_key: Semantic Scholar API key，默认从环境变量 SEMANTIC_SCHOLAR_API_KEY 读取
        """
        self.api_key = api_key or os.environ.get('SEMANTIC_SCHOLAR_API_KEY')
        if not self.api_key:
            print("警告: 未设置 Semantic Scholar API key，可能受到速率限制")
        
        self.session = requests.Session()
        # 设置默认 headers - GET请求不需要Content-Type
        self.session.headers.update({
            "Accept": "application/json"
        })
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})
    
    def search(self, query: str, limit: int = 20, 
               fields: str = "title,authors,year,venue,citationCount,url,abstract",
               publication_types: str = "Review,MetaAnalysis,JournalArticle,Study",
               year: str = None,
               venue: str = None,
               fields_of_study: str = None) -> List[Dict]:
        """
        检索文献
        
        Args:
            query: 检索关键词
            limit: 返回结果数量
            fields: 返回的字段（注意：doi字段不被支持）
            publication_types: 文献类型，默认只保留综述、元分析、期刊文章和研究
            year: 年份限制（默认不限制）
            venue: 期刊限制（默认不限制）
            fields_of_study: 研究领域限制（默认不限制）
            
        Returns:
            文献列表
        """
        params = {
            "query": query,
            "limit": limit,
            "fields": fields,
            "publicationTypes": publication_types
        }
        if year:
            params["year"] = year
        if venue:
            params["venue"] = venue
        if fields_of_study:
            params["fieldsOfStudy"] = fields_of_study
        
        try:
            response = self.session.get(self.SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            papers = data.get('data', [])
            
            # 格式化结果
            results = []
            for paper in papers:
                results.append({
                    "paperId": paper.get('paperId'),
                    "title": paper.get('title'),
                    "authors": [a.get('name') for a in paper.get('authors', [])],
                    "year": paper.get('year'),
                    "venue": paper.get('venue'),
                    "citationCount": paper.get('citationCount', 0),
                    "url": f"https://www.semanticscholar.org/paper/{paper.get('paperId')}",
                    "abstract": paper.get('abstract')
                })
            
            return results
            
        except requests.RequestException as e:
            print(f"检索失败: {e}")
            return []
    
    def search_multiple(self, queries: Dict[str, List[str]], 
                       limit: int = 20) -&gt; Dict[str, List[Dict]]:
        """
        多主题多轮次检索
        
        Args:
            queries: 检索词字典，格式 {主题: [关键词列表]}，列表长度即为轮次
            limit: 每轮检索数量
            
        Returns:
            按主题组织的文献字典 {主题: [文献列表]}
        """
        all_results = {}
        
        for topic, keywords in queries.items():
            print(f"\n【主题: {topic}】")
            topic_papers = []
            seen_ids = set()
            
            for i, keyword in enumerate(keywords, 1):
                print(f"  第{i}轮: {keyword}")
                results = self.search(keyword, limit=limit)
                
                # 去重
                new_papers = []
                for paper in results:
                    pid = paper.get('paperId')
                    if pid and pid not in seen_ids:
                        seen_ids.add(pid)
                        new_papers.append(paper)
                
                topic_papers.extend(new_papers)
                print(f"    新增: {len(new_papers)}篇，累计: {len(topic_papers)}篇")
                
                # 添加延迟避免速率限制
                time.sleep(0.5)
            
            all_results[topic] = topic_papers
        
        return all_results
        
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
            
    def fetch_full_metadata(self, papers: List[Dict], paper_ids: Optional[List[str]] = None) -&gt; int:
        """
        批量获取文献的完整元数据（摘要、DOI、期刊信息、卷期页码等）
        
        Args:
            papers: 文献列表
            paper_ids: 需要补全信息的文献ID列表，None表示补全所有
            
        Returns:
            成功补全的文献数量
        """
        print("\\n" + "="*60)
        print("正在补全文献完整元数据")
        print("="*60)
        
        count = 0
        for paper in papers:
            paper_id = paper.get('paperId')
            if not paper_id:
                continue
                
            # 判断是否需要补全
            need_fetch = False
            if paper_ids is None:
                # 补全所有文献，或摘要长度&gt;=500（疑似被截断）
                need_fetch = True
            else:
                # 补全指定ID的文献
                if paper.get('id') in paper_ids or paper.get('paperId') in paper_ids:
                    need_fetch = True
            
            if need_fetch:
                full_data = self._fetch_paper_details(paper_id)
                if full_data:
                    # 更新现有字段
                    for key, value in full_data.items():
                        if value is not None and str(value).strip():
                            paper[key] = value
                    count += 1
                    
                # 延迟避免速率限制
                time.sleep(0.5)
        
        print(f"补全完成：共{count}篇文献获取了完整元数据")
        return count'''

new_searcher_class = '''# ============================================================================
# Searcher: 文献检索类 - 简化版
# ============================================================================

class Searcher:
    """
    从 Semantic Scholar 检索文献
    
    只负责获取原始数据，不做处理。
    """
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper"
    SEARCH_URL= "https://api.semanticscholar.org/graph/v1/paper/search"
    PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Searcher
        
        Args:
            api_key: Semantic Scholar API key，默认从环境变量 SEMANTIC_SCHOLAR_API_KEY 读取
        """
        self.api_key = api_key or os.environ.get('SEMANTIC_SCHOLAR_API_KEY')
        if not self.api_key:
            print("警告: 未设置 Semantic Scholar API key，可能受到速率限制")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json"
        })
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})
    
    def search_relevance(self, query: str, limit: int = 20, 
                        fields: str = "title,authors,year,venue,citationCount,url,abstract",
                        publication_types: str = "Review,MetaAnalysis,JournalArticle,Study",
                        year: str = None,
                        venue: str = None,
                        fields_of_study: str = None) -&gt; List[Dict]:
        """
        Paper relevance search - 相关性检索
        
        Args:
            query: 检索关键词
            limit: 返回结果数量
            fields: 返回的字段
            publication_types: 文献类型
            year: 年份限制
            venue: 期刊限制
            fields_of_study: 研究领域限制
            
        Returns:
            原始文献列表（API返回的原始格式）
        """
        params = {
            "query": query,
            "limit": limit,
            "fields": fields,
            "publicationTypes": publication_types
        }
        if year:
            params["year"] = year
        if venue:
            params["venue"] = venue
        if fields_of_study:
            params["fieldsOfStudy"] = fields_of_study
        
        try:
            response = self.session.get(self.SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
            
        except requests.RequestException as e:
            print(f"检索失败: {e}")
            return []
    
    def get_paper_details(self, paper_id: str) -&gt; Optional[Dict]:
        """
        Paper details search - 获取文献详情（公有方法）
        
        Args:
            paper_id: Semantic Scholar paper ID
            
        Returns:
            原始文献详情（API返回的原始格式）
        """
        url = self.PAPER_URL.format(paper_id=paper_id)
        params = {
            "fields": "paperId,title,abstract,venue,year,journal,publicationVenue,citationCount,authors,externalIds"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"获取详情失败: {e}")
            return None'''

# 替换Searcher类
if old_searcher_class in content:
    content = content.replace(old_searcher_class, new_searcher_class)
    print("✅ Searcher类已简化")
else:
    print("❌ 未找到旧Searcher类，让我检查文件...")
    # 检查前500行
    print("\n文件前100行:")
    print(content[:3000])

# 保存
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 文件保存成功！")
