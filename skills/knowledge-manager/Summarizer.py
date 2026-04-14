#!/usr/bin/env python3
"""
Summarizer.py - 使用 LLM 分析论文，生成 labels 和 notes

使用方式：
    summarizer = Summarizer()
    kb = summarizer.summarize(kb_path="index.json")
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Any


class Summarizer:
    """文献总结器 - 为知识库中的论文添加 labels 和 notes"""

    def __init__(self,
                 api_key: Optional[str] = None,
                 base_url: str = "https://ark.cn-beijing.volces.com/api/v3",
                 model: str = "deepseek-v3-2-251201"):
        """
        初始化 Summarizer
        Args:
            api_key: API key，默认从环境变量 LKEAP_API_KEY 或 ARK_API_KEY 读取
            base_url: API base URL
            model: 模型名称
        """
        self.api_key = api_key or os.environ.get('LKEAP_API_KEY') or os.environ.get('ARK_API_KEY')
        if not self.api_key:
            raise ValueError("请设置环境变量 LKEAP_API_KEY 或 ARK_API_KEY")
        self.base_url = base_url
        self.model = model
        self._init_openai()
        self._init_system_prompt()

    def _init_openai(self):
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)
        except ImportError:
            raise ImportError("请安装 openai 包: pip install openai")

    def _init_system_prompt(self):
        self.system_prompt = """你是一位专业的学术文献分析专家。根据标题和摘要判断文献类型并提取关键信息。

## 文献类型
- 📊实证 (Empirical): 包含明确的被试/样本、研究方法、数据分析
- 📖综述 (Review): 综述、元分析、系统综述
- 💡理论 (Theoretical): 理论文章、观点、评论
- 📋待分类 (Unclassified): 无法明确归类

## 输出 JSON 格式（必须严格遵守）

### 实证文献
{"paper_type": "📊实证", "confidence": 0.95, "notes": {"研究问题": "...", "研究方法": "...", "研究结果": "...", "研究结论": "..."}}

### 综述文献
{"paper_type": "📖综述", "confidence": 0.90, "notes": {"研究问题": "...", "研究结果": "...", "研究展望": "..."}}

### 理论文献
{"paper_type": "💡理论", "confidence": 0.85, "notes": {"研究问题": "...", "理论观点": "..."}}

### 待分类
{"paper_type": "📋待分类", "confidence": 0.50, "notes": {"说明": "..."}}

只返回 JSON，不要有其他内容。"""

    # ==================== 公共方法 ====================

    def summarize(self, kb_path: str = "index.json", progress_interval: int = 10) -> Dict:
        """
        分析知识库中所有论文，添加 labels 和 notes，保存并返回知识库
        Args:
            kb_path: 知识库文件路径（默认 index.json）
            progress_interval: 进度打印间隔
        Returns:
            更新后的知识库字典
        """
        # 加载知识库
        kb_data = self._load_kb(kb_path)
        papers = kb_data.get('papers', [])
        if not papers:
            print("知识库为空，无需分析")
            return kb_data

        print(f"\n开始分析 {len(papers)} 篇文献...")
        for i, paper in enumerate(papers, 1):
            title = paper.get('title', '')
            abstract = paper.get('abstract', '')
            result = self._summarize_single(title, abstract)
            # 更新 labels（保留原有 importance 和 JCR 如果存在）
            importance = paper.get('labels', {}).get('importance', self._calc_importance(paper.get('citationCount', 0)))
            jcr = paper.get('labels', {}).get('JCR', '')
            paper['labels'] = {
                "type": result['type'],
                "importance": importance,
                "JCR": jcr
            }
            paper['notes'] = result['notes']
            if i % progress_interval == 0 or i == len(papers):
                print(f"  进度: {i}/{len(papers)} ({i/len(papers)*100:.1f}%)")

        # 更新统计信息
        kb_data = self._update_statistics(kb_data)
        self._save_kb(kb_data, kb_path)
        return kb_data

    # ==================== 私有方法 ====================

    def _load_kb(self, kb_path: str) -> Dict:
        """加载知识库 JSON 文件"""
        if not os.path.exists(kb_path):
            raise FileNotFoundError(f"知识库文件不存在: {kb_path}")
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"已加载知识库: {kb_path}, 共 {len(data.get('papers', []))} 篇论文")
        return data

    def _save_kb(self, kb_data: Dict, kb_path: str):
        """保存知识库到文件"""
        os.makedirs(os.path.dirname(os.path.abspath(kb_path)), exist_ok=True)
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        print(f"知识库已保存: {kb_path}")

    def _update_statistics(self, kb_data: Dict) -> Dict:
        """重新计算统计信息并更新时间戳"""
        papers = kb_data.get('papers', [])
        total = len(papers)
        total_cites = sum(p.get('citationCount', 0) for p in papers)
        foundation = sum(1 for p in papers if p.get('labels', {}).get('importance') == '🔴奠基')
        important = sum(1 for p in papers if p.get('labels', {}).get('importance') == '🟡重要')
        general = total - foundation - important
        empirical = sum(1 for p in papers if p.get('labels', {}).get('type') == '📊实证')
        review = sum(1 for p in papers if p.get('labels', {}).get('type') == '📖综述')
        theory = sum(1 for p in papers if p.get('labels', {}).get('type') == '💡理论')
        kb_data['statistics'] = {
            "total_count": total,
            "total_citations": total_cites,
            "foundation_count": foundation,
            "important_count": important,
            "general_count": general,
            "empirical_count": empirical,
            "review_count": review,
            "theory_count": theory
        }
        kb_data['updated_at'] = datetime.now().isoformat()
        if not kb_data.get('created_at'):
            kb_data['created_at'] = datetime.now().isoformat()
        return kb_data

    def _summarize_single(self, title: str, abstract: str) -> Dict[str, Any]:
        """分析单篇论文，返回 {type, notes}"""
        user_prompt = f"标题：{title}\n摘要：{abstract if abstract else '无摘要'}\n请分析。"
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            content = resp.choices[0].message.content
            result = self._extract_json(content)
            return {
                "type": result.get('paper_type', '📋待分类'),
                "notes": result.get('notes', {})
            }
        except Exception as e:
            print(f"分析失败: {e}")
            return {"type": "📋待分类", "notes": {"error": str(e)}}

    def _extract_json(self, content: str) -> Dict:
        try:
            return json.loads(content)
        except:
            import re
            match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                return json.loads(content[start:end+1])
            raise ValueError("无法解析 JSON")

    def _calc_importance(self, citation_count: int) -> str:
        if citation_count >= 500:
            return "🔴奠基文献"
        elif citation_count >= 50:
            return "🟡重要文献"
        else:
            return "🔵一般文献"


# ==================== 测试入口 ====================
if __name__ == "__main__":
    summarizer = Summarizer()
    # 分析知识库
    kb = summarizer.summarize(kb_path="test_kb.json")
    print("分析完成，论文数:", len(kb['papers']))