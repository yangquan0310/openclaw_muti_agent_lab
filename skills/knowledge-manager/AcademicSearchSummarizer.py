#!/usr/bin/env python3
"""
学术文献检索与总结系统 - 重构版本

包含三个核心类:
- Searcher: 从 Semantic Scholar 检索文献
- Summarizer: 使用 LLM 判断文献类型和总结
- AcademicSearchSummarizer: 总类，协调检索和总结流程

用法:
    python3 AcademicSearchSummarizer.py --queries queries.json --output result.json
"""

import json
import os
import sys
import requests
import time
import argparse
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime


# ============================================================================
# Searcher: 文献检索类
# ============================================================================

class Searcher:
    """
    从 Semantic Scholar 检索文献
    
    使用 Semantic Scholar API 进行文献检索，支持多关键词、多轮次检索。
    """
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    
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
               fields: str = "title,authors,year,venue,citationCount,url,abstract") -> List[Dict]:
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
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params)
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
                       limit: int = 20) -> Dict[str, List[Dict]]:
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
            
            # 列表长度即为轮次
            for round_num, keyword in enumerate(keywords, 1):
                print(f"  轮次 {round_num}: 检索 '{keyword}'")
                papers = self.search(keyword, limit)
                
                # 为主题和轮次标记
                for paper in papers:
                    paper['_topic'] = topic
                    paper['_round'] = round_num
                
                topic_papers.extend(papers)
                print(f"    获取 {len(papers)} 篇")
                
                # 添加延迟避免速率限制
                time.sleep(0.5)
            
            all_results[topic] = topic_papers
        
        return all_results
        
    def _fetch_paper_details(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文献的完整元数据
        
        Args:
            paper_id: Semantic Scholar paper ID
            
        Returns:
            包含完整信息的字典，如果获取失败则返回 None
        """
        url = f"{self.BASE_URL}/{paper_id}"
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
            return None
            
    def fetch_full_metadata(self, papers: List[Dict], paper_ids: Optional[List[str]] = None) -> int:
        """
        批量获取文献的完整元数据（摘要、DOI、期刊信息、卷期页码等）
        
        Args:
            papers: 文献列表
            paper_ids: 需要补全信息的文献ID列表，None表示补全所有
            
        Returns:
            成功补全的文献数量
        """
        print("\n" + "="*60)
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
                # 补全所有文献，或摘要长度>=500（疑似被截断）
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
        return count


# ============================================================================
# Summarizer: 文献总结类
# ============================================================================

class Summarizer:
    """
    使用 LLM 判断文献类型和总结
    
    继承 OpenAI API，通过多轮会话分析文献摘要，返回类型和笔记。
    """
    
    def __init__(self, api_key: Optional[str] = None, 
                 base_url: str = "https://ark.cn-beijing.volces.com/api/v3",
                 model: str = "deepseek-v3-2-251201"):
        """
        初始化 Summarizer
        
        Args:
            api_key: API key，默认从环境变量 ARK_API_KEY 读取
            base_url: API base URL，默认火山引擎
            model: 模型名称
        """
        self.api_key = api_key or os.environ.get('ARK_API_KEY')
        if not self.api_key:
            raise ValueError("ARK_API_KEY 环境变量未设置")
        
        self.base_url = base_url
        self.model = model
        
        self._init_openai()
        self._init_system_prompt()
    
    def _init_openai(self):
        """初始化 OpenAI 客户端"""
        try:
            import openai
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        except ImportError:
            print("错误: 未安装 openai 包。请运行: pip install openai")
            sys.exit(1)
    
    def _init_system_prompt(self):
        """初始化系统提示词 - 根据文献类型输出不同格式的notes"""
        self.system_prompt = """你是一位专业的学术文献分析专家。你的任务是根据文献的标题和摘要，判断文献的类型并提取关键信息。

## 文献类型定义

1. **📊实证 (Empirical)**
   - 包含明确的被试/样本描述
   - 有具体的研究方法和实验设计
   - 包含数据收集和统计分析
   - 摘要中通常有 "participants", "sample", "method", "results", "analysis" 等关键词

2. **📖综述 (Review)**
   - 综述、元分析、系统综述
   - 总结和整合已有研究
   - 标题或摘要中通常有 "review", "meta-analysis", "systematic review" 等关键词

3. **💡理论 (Theoretical)**
   - 理论文章、观点文章、评论
   - 提出新理论或概念框架
   - 标题中通常有 "theoretical", "theory", "perspective", "commentary", "viewpoint" 等关键词

4. **📋待分类 (Unclassified)**
   - 无法明确归类为上述三类的文献

## 输出格式

请先判断文献类型，然后以对应的 JSON 格式返回：

### 📊实证文献格式
```json
{
    "paper_type": "📊实证",
    "confidence": 0.95,
    "notes": {
        "研究问题": "文献试图解决的科学问题（1-2句话）",
        "研究方法": "采用的方法、被试/样本、实验设计（1-2句话）",
        "研究结果": "主要发现和效应大小（1-2句话）",
        "研究结论": "结论和理论贡献（1-2句话）"
    }
}
```

### 📖综述文献格式
```json
{
    "paper_type": "📖综述",
    "confidence": 0.90,
    "notes": {
        "研究问题": "综述试图解决的科学问题（1-2句话）",
        "研究结果": "主要发现和效应量（1-2句话）",
        "研究展望": "未来研究方向（1-2句话）"
    }
}
```

### 💡理论文献格式
```json
{
    "paper_type": "💡理论",
    "confidence": 0.85,
    "notes": {
        "研究问题": "理论试图解释的科学问题（1-2句话）",
        "理论观点": "核心概念和逻辑（1-2句话）"
    }
}
```

### 📋待分类文献格式
```json
{
    "paper_type": "📋待分类",
    "confidence": 0.50,
    "notes": {
        "说明": "无法明确归类的简要说明"
    }
}
```

## 判断规则

1. **优先判断为实证**：如果摘要中有明确的被试、方法、结果描述
2. **优先判断为综述**：如果标题或摘要中有 review/meta-analysis/systematic review
3. **优先判断为理论**：如果标题中有 theoretical/theory/perspective/commentary
4. **无法判断时**：标记为待分类

请确保：
1. 只返回 JSON 格式，不要返回其他内容
2. 所有内容使用中文
3. confidence 为 0-1 之间的数值
4. notes 中的内容必须基于文献摘要，不要编造
5. **根据判断的类型，使用对应的 notes 格式**"""
    
    def summarize(self, title: str, abstract: str) -> Dict[str, Any]:
        """
        分析单篇文献
        
        Args:
            title: 文献标题
            abstract: 文献摘要
            
        Returns:
            包含 paper_type, confidence, notes 的字典
        """
        user_prompt = f"""请分析以下文献：

**标题**: {title}

**摘要**: {abstract if abstract else '[无摘要]'}

请判断文献类型并提取关键信息，以 JSON 格式返回。"""

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # 解析 JSON
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # 尝试从代码块中提取
                start = content.find('```json')
                end = content.find('```', start + 7)
                if start != -1 and end != -1:
                    json_str = content[start + 7:end].strip()
                else:
                    start = content.find('{')
                    end = content.rfind('}')
                    json_str = content[start:end + 1]
                
                result = json.loads(json_str)
            
            return {
                "paper_type": result.get('paper_type', '📋待分类'),
                "confidence": result.get('confidence', 0.0),
                "notes": result.get('notes', {})
            }
            
        except Exception as e:
            print(f"分析失败: {e}")
            return {
                "paper_type": "📋待分类",
                "confidence": 0.0,
                "notes": {"error": str(e)}
            }
    
    def summarize_batch(self, papers: List[Dict], 
                       progress_interval: int = 10) -> List[Dict]:
        """
        批量分析文献
        
        Args:
            papers: 文献列表
            progress_interval: 进度打印间隔
            
        Returns:
            分析结果列表
        """
        results = []
        total = len(papers)
        
        print(f"\n开始分析 {total} 篇文献...")
        
        for i, paper in enumerate(papers, 1):
            title = paper.get('title', '')
            abstract = paper.get('abstract', '')
            
            result = self.summarize(title, abstract)
            result['paper_id'] = paper.get('paperId') or paper.get('id')
            results.append(result)
            
            if i % progress_interval == 0 or i == total:
                print(f"  进度: {i}/{total} ({i/total*100:.1f}%)")
        
        return results


# ============================================================================
# AcademicSearchSummarizer: 总类
# ============================================================================

class AcademicSearchSummarizer:
    """
    学术文献检索与总结总类
    
    协调 Searcher 和 Summarizer，完成从检索到总结的完整流程。
    """
    
    def __init__(self, 
                 semantic_scholar_key: Optional[str] = None,
                 llm_key: Optional[str] = None,
                 llm_base_url: str = "https://api.lkeap.cloud.tencent.com/v1",
                 llm_model: str = "deepseek-v3.2"):
        """
        初始化 AcademicSearchSummarizer
        
        Args:
            semantic_scholar_key: Semantic Scholar API key
            llm_key: LLM API key
            llm_base_url: LLM API base URL
            llm_model: LLM 模型名称
        """
        self.searcher = Searcher(semantic_scholar_key)
        
        # LLM 相关配置（延迟初始化）
        self._llm_key = llm_key
        self._llm_base_url = llm_base_url
        self._llm_model = llm_model
        self._summarizer = None
        
        self.all_papers: List[Dict] = []
        self.topic_map: Dict[str, List[str]] = {}
    
    @property
    def summarizer(self) -> Summarizer:
        """延迟初始化 Summarizer"""
        if self._summarizer is None:
            self._summarizer = Summarizer(self._llm_key, self._llm_base_url, self._llm_model)
        return self._summarizer
    
    def search(self, queries: Dict[str, List[str]], 
              limit: int = 20) -> 'AcademicSearchSummarizer':
        """
        执行检索（链式调用）
        
        Args:
            queries: 检索词字典，格式 {主题: [关键词列表]}，列表长度即为轮次
            limit: 每轮检索数量
            
        Returns:
            self (链式调用)
        """
        print("="*60)
        print("步骤 1: 检索文献")
        print("="*60)
        
        results = self.searcher.search_multiple(queries, limit)
        
        # 合并所有主题的文献
        for topic, papers in results.items():
            for paper in papers:
                title = paper.get('title', '')
                
                # 记录主题映射
                if title not in self.topic_map:
                    self.topic_map[title] = []
                if topic not in self.topic_map[title]:
                    self.topic_map[title].append(topic)
                
                # 添加到总列表
                self.all_papers.append(paper)
        
        print(f"\n检索完成: 共 {len(self.all_papers)} 篇文献")
        
        return self
    
    def deduplicate(self) -> 'AcademicSearchSummarizer':
        """去重（链式调用）"""
        print("\n" + "="*60)
        print("步骤 2: 去重")
        print("="*60)
        
        seen_titles = set()
        unique_papers = []
        
        for paper in self.all_papers:
            title = paper.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_papers.append(paper)
        
        self.all_papers = unique_papers
        print(f"去重后: {len(self.all_papers)} 篇")
        
        return self
    
    def filter_by_year(self, min_year: int) -> 'AcademicSearchSummarizer':
        """按年份筛选（链式调用）"""
        print(f"\n筛选 {min_year} 年后的文献...")
        self.all_papers = [p for p in self.all_papers if p.get('year', 0) >= min_year]
        print(f"筛选后: {len(self.all_papers)} 篇")
        return self
    
    def sort_by_citations(self) -> 'AcademicSearchSummarizer':
        """按引用量排序（链式调用）"""
        self.all_papers.sort(key=lambda x: x.get('citationCount', 0), reverse=True)
        return self
    
    def filter_by_criteria(self, filters: Dict = None, **kwargs) -> 'AcademicSearchSummarizer':
        """
        按多条件筛选文献（链式调用）
        
        默认筛选规则（不提供任何参数时自动启用）：
        - 奠基文献：无时间限制，引用≥500，全部保留
        - 重要文献：近10年，引用≥50，全部保留
        - 新近文献：近3年，实证研究，全部保留
        
        支持两种使用方式：
        1. 传统参数方式：filter_by_criteria(foundation_min=500, important_min=50, ...)
        2. 新筛选器方式：filter_by_criteria({
            "filter1": {
                "citations": {"min": 500, "max": None},  # ≥500引用
                "years": {"min": 2020, "max": 2025}     # 2020-2025年
            },
            "filter2": {
                "citations": {"min": 100, "max": 500},  # 100-500引用
                "venue": ["Journal of Personality", "Psychological Review"]  # 特定期刊
            }
        })
        
        多个filter之间取并集，满足任意一个filter条件的文献都会被保留
        
        Args:
            filters: 筛选条件字典，支持的筛选维度：
                citations: {"min": int, "max": int} - 引用量范围
                years: {"min": int, "max": int} - 发表年份范围
                venue: list - 期刊/会议名称列表（包含任意一个即匹配）
                type: list - 文献类型列表（📊实证/📖综述/💡理论等）
                importance: list - 重要性等级列表（🔴奠基/🟡重要/🔵一般）
                **kwargs: 传统参数，兼容旧版调用方式
        """
        print("\n" + "="*60)
        print("步骤 3: 按条件筛选")
        print("="*60)
        
        current_year = datetime.now().year
        
        # 默认筛选规则（不提供任何参数时使用）
        if filters is None and not kwargs:
            filters = {
                "奠基文献": {
                    "citations": {"min": 500, "max": None},
                    "years": {"min": 0, "max": current_year},  # 无时间限制
                    "limit": 99999  # 全部保留
                },
                "重要文献": {
                    "citations": {"min": 50, "max": 500},
                    "years": {"min": current_year - 10, "max": current_year},  # 近10年
                    "limit": 99999  # 全部保留
                },
                "新近文献": {
                    "years": {"min": current_year - 3, "max": current_year},  # 近3年
                    "type": ["📊实证"],  # 仅实证研究
                    "limit": 99999  # 全部保留
                }
            }
            print("使用默认筛选规则：")
            print("  奠基文献：引用≥500，无时间限制，全部保留")
            print("  重要文献：引用≥50，近10年，全部保留")
            print("  新近文献：近3年，实证研究，全部保留")
        # 兼容旧版参数调用
        elif filters is None and kwargs:
            foundation_min = kwargs.get('foundation_min', 500)
            important_min = kwargs.get('important_min', 50)
            important_max = kwargs.get('important_max', 500)
            foundation_limit = kwargs.get('foundation_limit', 5)
            important_limit = kwargs.get('important_limit', 10)
            general_limit = kwargs.get('general_limit', 30)
            
            # 转换为新的筛选器格式
            filters = {
                "foundation": {
                    "citations": {"min": foundation_min, "max": None},
                    "limit": foundation_limit
                },
                "important": {
                    "citations": {"min": important_min, "max": important_max},
                    "limit": important_limit
                },
                "general": {
                    "citations": {"min": 0, "max": important_min},
                    "limit": general_limit
                }
            }
        
        if not filters:
            print("未提供筛选条件，跳过筛选")
            return self
        
        filtered_papers = []
        filter_stats = {}
        
        for filter_name, filter_cond in filters.items():
            papers = self.all_papers.copy()
            
            # 应用筛选条件
            if 'citations' in filter_cond:
                cite_min = filter_cond['citations'].get('min', 0)
                cite_max = filter_cond['citations'].get('max', float('inf'))
                papers = [p for p in papers if cite_min <= p.get('citationCount', 0) < cite_max]
            
            if 'years' in filter_cond:
                year_min = filter_cond['years'].get('min', 0)
                year_max = filter_cond['years'].get('max', float('inf'))
                papers = [p for p in papers if year_min <= p.get('year', 0) <= year_max]
            
            if 'venue' in filter_cond:
                venues = [v.lower() for v in filter_cond['venue']]
                papers = [p for p in papers if p.get('venue', '').lower() in venues]
            
            # 应用数量限制
            if 'limit' in filter_cond and filter_cond['limit'] > 0:
                papers = papers[:filter_cond['limit']]
            
            filter_stats[filter_name] = len(papers)
            filtered_papers.extend(papers)
        
        # 去重（可能被多个filter匹配到同一篇）
        seen_ids = set()
        unique_papers = []
        for paper in filtered_papers:
            paper_id = paper.get('paperId', paper.get('id', ''))
            if paper_id and paper_id not in seen_ids:
                seen_ids.add(paper_id)
                unique_papers.append(paper)
        
        self.all_papers = unique_papers
        
        # 打印统计
        print("\n筛选结果：")
        for filter_name, count in filter_stats.items():
            print(f"  {filter_name}: {count} 篇")
        print(f"总计: {len(self.all_papers)} 篇（去重后）")
        
        return self
    
    def summarize(self) -> 'AcademicSearchSummarizer':
        """
        使用 LLM 分析文献（链式调用）
        
        为每篇文献添加 type 和 notes 字段
        """
        print("\n" + "="*60)
        print("步骤 4: LLM 分析文献")
        print("="*60)
        
        results = self.summarizer.summarize_batch(self.all_papers)
        
        # 将分析结果合并到文献中
        for paper, result in zip(self.all_papers, results):
            paper['labels'] = {
                'type': result['paper_type'],
                'importance': self._get_importance(paper.get('citationCount', 0)),
                'confidence': result['confidence']
            }
            paper['notes'] = result['notes']
            
            # 添加主题
            title = paper.get('title', '')
            paper['topic'] = self.topic_map.get(title, ['待分类'])
        
        return self
        
    def fetch_full_metadata(self, paper_ids: Optional[List[str]] = None) -> 'AcademicSearchSummarizer':
        """
        批量获取文献的完整元数据（摘要、DOI、期刊信息、卷期页码等）
        
        Args:
            paper_ids: 需要补全信息的文献ID列表，None表示补全所有
            
        Returns:
            self (链式调用)
        """
        self.searcher.fetch_full_metadata(self.all_papers, paper_ids)
        return self
    
    def _get_importance(self, citation_count: int) -> str:
        """根据引用量判断重要性"""
        if citation_count >= 500:
            return "🔴奠基"
        elif citation_count >= 50:
            return "🟡重要"
        else:
            return "🔵一般"
    
    def to_knowledge_base(self, project_name: str = "") -> Dict[str, Any]:
        """
        转换为知识库格式
        
        Args:
            project_name: 项目名称
            
        Returns:
            知识库字典
        """
        print("\n" + "="*60)
        print("步骤 5: 生成知识库")
        print("="*60)
        
        # 分配 ID
        for i, paper in enumerate(self.all_papers, 1):
            paper['id'] = f"paper_{i:03d}"
        
        # 统计
        total = len(self.all_papers)
        foundation = len([p for p in self.all_papers if p['labels']['importance'] == "🔴奠基"])
        important = len([p for p in self.all_papers if p['labels']['importance'] == "🟡重要"])
        general = len([p for p in self.all_papers if p['labels']['importance'] == "🔵一般"])
        
        empirical = len([p for p in self.all_papers if p['labels']['type'] == "📊实证"])
        review = len([p for p in self.all_papers if p['labels']['type'] == "📖综述"])
        theory = len([p for p in self.all_papers if p['labels']['type'] == "💡理论"])
        
        kb = {
            "version": "1.0.0",
            "project": project_name,
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "statistics": {
                "total_count": total,
                "foundation_count": foundation,
                "important_count": important,
                "general_count": general,
                "empirical_count": empirical,
                "review_count": review,
                "theory_count": theory
            },
            "papers": self.all_papers
        }
        
        print(f"知识库生成完成: {total} 篇文献")
        print(f"  奠基: {foundation} | 重要: {important} | 一般: {general}")
        print(f"  实证: {empirical} | 综述: {review} | 理论: {theory}")
        
        return kb
    
    def save(self, output_path: str, project_name: str = "") -> str:
        """
        保存知识库到文件
        
        Args:
            output_path: 输出路径，支持两种形式：
                         1. 完整文件路径：如 "/path/to/知识库/index.json"
                         2. 目录路径：如 "/path/to/知识库/"，自动保存为 index.json
            project_name: 项目名称
            
        Returns:
            保存的文件路径
        """
        kb = self.to_knowledge_base(project_name)
        
        # 处理路径：如果是目录，自动添加 index.json
        if os.path.isdir(output_path) or output_path.endswith('/'):
            os.makedirs(output_path, exist_ok=True)
            output_path = os.path.join(output_path, 'index.json')
        else:
            # 确保父目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(kb, f, ensure_ascii=False, indent=2)
        
        print(f"\n知识库已保存: {output_path}")
        return output_path
    
    def export_topic_notes(self, topic: str, notes_dir: str = None, 
                          kb_path: Optional[str] = None) -> str:
        """
        导出特定主题的笔记（JSON格式，index.json的子集）
        
        Args:
            topic: 主题名称，用作笔记文件名
            notes_dir: 笔记保存目录，默认在知识库同级的「笔记/」目录下
                       如果提供kb_path，会自动在kb_path所在目录下创建「笔记/」子目录
            kb_path: 知识库文件路径（如果已加载则不需要）
            
        Returns:
            导出的笔记文件路径
        """
        print("\n" + "="*60)
        print(f"导出主题 '{topic}' 的笔记")
        print("="*60)
        
        # 如果提供了知识库路径，加载它
        papers = self.all_papers
        if kb_path:
            with open(kb_path, 'r', encoding='utf-8') as f:
                kb = json.load(f)
            papers = kb.get('papers', [])
            
            # 如果没有指定notes_dir，默认在知识库所在目录下创建「笔记/」目录
            if notes_dir is None:
                kb_dir = os.path.dirname(os.path.abspath(kb_path))
                notes_dir = os.path.join(kb_dir, '笔记')
        
        # 筛选特定主题的文献
        topic_papers = [p for p in papers if topic in p.get('topic', [])]
        
        if not topic_papers:
            print(f"未找到主题 '{topic}' 的文献")
            return ""
        
        print(f"找到 {len(topic_papers)} 篇相关文献")
        
        # 构建笔记JSON（index.json的子集）
        notes_json = {
            "version": "1.0.0",
            "topic": topic,
            "source": kb_path if kb_path else "memory",
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "statistics": {
                "total_count": len(topic_papers),
                "empirical_count": len([p for p in topic_papers if p.get('labels', {}).get('type') == '📊实证']),
                "review_count": len([p for p in topic_papers if p.get('labels', {}).get('type') == '📖综述']),
                "theory_count": len([p for p in topic_papers if p.get('labels', {}).get('type') == '💡理论']),
                "foundation_count": len([p for p in topic_papers if p.get('labels', {}).get('importance') == '🔴奠基']),
                "important_count": len([p for p in topic_papers if p.get('labels', {}).get('importance') == '🟡重要']),
                "general_count": len([p for p in topic_papers if p.get('labels', {}).get('importance') == '🔵一般'])
            },
            "papers": topic_papers
        }
        
        # 确保笔记目录存在
        os.makedirs(notes_dir, exist_ok=True)
        
        # 笔记文件名：{主题名}.json，自动替换不合法字符
        notes_filename = f"{topic.replace('/', '_').replace(' ', '_')}.json"
        notes_path = os.path.join(notes_dir, notes_filename)
        
        with open(notes_path, 'w', encoding='utf-8') as f:
            json.dump(notes_json, f, ensure_ascii=False, indent=2)
        
        print(f"笔记已导出: {notes_path}")
        print(f"  总计: {len(topic_papers)} 篇")
        return notes_path
        
        # 保存笔记文件
        os.makedirs(notes_dir, exist_ok=True)
        notes_filename = f"{topic.replace(' ', '_').replace('/', '_')}.json"
        notes_path = os.path.join(notes_dir, notes_filename)
        
        with open(notes_path, 'w', encoding='utf-8') as f:
            json.dump(notes_json, f, ensure_ascii=False, indent=2)
        
        print(f"笔记已导出: {notes_path}")
        print(f"  总计: {len(topic_papers)} 篇")
        return notes_path
    
    def complete_notes(self, kb_path: str, 
                      paper_ids: Optional[List[str]] = None) -> 'AcademicSearchSummarizer':
        """
        给特定 index.json 补全笔记
        
        Args:
            kb_path: 知识库文件路径
            paper_ids: 需要补全的文献 ID 列表（None 表示全部）
            
        Returns:
            self (链式调用)
        """
        print("\n" + "="*60)
        print("补全知识库笔记")
        print("="*60)
        
        # 加载知识库
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        papers = kb.get('papers', [])
        
        # 确定需要补全的文献
        if paper_ids:
            target_papers = [p for p in papers if p.get('id') in paper_ids]
        else:
            # 补全所有缺少 notes、notes为空、或notes包含error的文献
            def needs_completion(paper):
                notes = paper.get('notes')
                if not notes:
                    return True
                if isinstance(notes, dict):
                    # 检查是否有error字段，或者notes为空字典
                    if notes.get('error') or len(notes) == 0:
                        return True
                return False
            
            target_papers = [p for p in papers if needs_completion(p)]
        
        if not target_papers:
            print("所有文献已有完整笔记，无需补全")
            return self
        
        print(f"需要补全 {len(target_papers)} 篇文献的笔记")
        
        # 使用 LLM 分析
        results = self.summarizer.summarize_batch(target_papers)
        
        # 更新知识库
        result_map = {r['paper_id']: r for r in results}
        updated_count = 0
        
        for paper in papers:
            paper_id = paper.get('id') or paper.get('paperId')
            if paper_id in result_map:
                result = result_map[paper_id]
                
                # 更新 labels
                if 'labels' not in paper:
                    paper['labels'] = {}
                paper['labels']['type'] = result['paper_type']
                paper['labels']['confidence'] = result['confidence']
                
                # 更新 notes
                paper['notes'] = result['notes']
                
                updated_count += 1
        
        # 更新统计信息
        empirical = len([p for p in papers if p.get('labels', {}).get('type') == '📊实证'])
        review = len([p for p in papers if p.get('labels', {}).get('type') == '📖综述'])
        theory = len([p for p in papers if p.get('labels', {}).get('type') == '💡理论'])
        
        kb['statistics']['empirical_count'] = empirical
        kb['statistics']['review_count'] = review
        kb['statistics']['theory_count'] = theory
        kb['updated_at'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        # 保存更新后的知识库
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump(kb, f, ensure_ascii=False, indent=2)
        
        print(f"\n补全完成: 更新了 {updated_count} 篇文献")
        print(f"统计: 实证 {empirical} | 综述 {review} | 理论 {theory}")
        print(f"知识库已保存: {kb_path}")
        
        return self
        
    def load_knowledge_base(self, kb_path: str) -> 'AcademicSearchSummarizer':
        """
        从已有的index.json加载文献
        
        Args:
            kb_path: 知识库文件路径
            
        Returns:
            self (链式调用)
        """
        print("\n" + "="*60)
        print("加载知识库")
        print("="*60)
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        self.all_papers = kb.get('papers', [])
        self.project_name = kb.get('project', '')
        
        # 构建主题映射
        self.topic_map = {}
        for paper in self.all_papers:
            title = paper.get('title', '')
            topics = paper.get('topic', [])
            if title and topics:
                self.topic_map[title] = topics
        
        print(f"加载完成：共{len(self.all_papers)}篇文献")
        return self
    
    def fill_metadata_from_kb(self, kb_path: str, paper_ids: Optional[List[str]] = None) -> int:
        """
        直接补全已有index.json中的完整元数据（摘要、DOI、期刊信息等）
        
        Args:
            kb_path: 知识库文件路径
            paper_ids: 需要补全信息的文献ID列表，None表示补全所有
            
        Returns:
            成功补全的文献数量
        """
        self.load_knowledge_base(kb_path)
        count = self.searcher.fetch_full_metadata(self.all_papers, paper_ids)
        
        # 保存更新后的知识库
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_knowledge_base(self.project_name), f, ensure_ascii=False, indent=2)
        
        print(f"元数据补全结果已保存到：{kb_path}")
        return count


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='学术文献检索与总结系统')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 检索命令
    search_parser = subparsers.add_parser('search', help='检索文献并生成知识库')
    search_parser.add_argument('--queries', '-q', required=True, help='检索词 JSON 文件路径')
    search_parser.add_argument('--output', '-o', required=True, help='输出知识库 JSON 文件路径')
    search_parser.add_argument('--project', '-p', default='', help='项目名称')
    search_parser.add_argument('--limit', '-l', type=int, default=20, help='每轮检索数量')
    search_parser.add_argument('--min-year', '-y', type=int, default=2020, help='最小年份')
    search_parser.add_argument('--no-summarize', action='store_true', help='跳过 LLM 总结')
    search_parser.add_argument('--fetch-abstracts', action='store_true', help='检索后自动补全完整摘要')
    
    # 摘要补全命令
    abstract_parser = subparsers.add_parser('fill-metadata', help='补全已有知识库的完整元数据（摘要、DOI、期刊信息等）')
    abstract_parser.add_argument('--kb-path', '-k', required=True, help='知识库index.json路径')
    abstract_parser.add_argument('--paper-ids', '-i', nargs='+', help='指定需要补全的文献ID列表，不指定则补全所有')
    
    args = parser.parse_args()
    
    if args.command == 'search':
        # 执行检索流程
        summarizer = AcademicSearchSummarizer()
        
        # 读取检索词
        with open(args.queries, 'r', encoding='utf-8') as f:
            queries = json.load(f)
        
        # 执行流程
        summarizer.search(queries, args.limit)
        summarizer.deduplicate()
        summarizer.filter_by_year(args.min_year)
        summarizer.sort_by_citations()
        summarizer.filter_by_criteria()
        
        if args.fetch_abstracts:
            summarizer.fetch_full_metadata()
        
        if not args.no_summarize:
            summarizer.summarize()
        
        summarizer.save(args.output, args.project)
        
        print("\n" + "="*60)
        print("全部完成!")
        print("="*60)
        
    elif args.command == 'fill-metadata':
        # 执行元数据补全
        summarizer = AcademicSearchSummarizer()
        count = summarizer.fill_metadata_from_kb(args.kb_path, args.paper_ids)
        print(f"\n元数据补全任务完成，共补全{count}篇文献")


if __name__ == "__main__":
    main()
