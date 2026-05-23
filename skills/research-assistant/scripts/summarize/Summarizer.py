#!/usr/bin/env python3
"""
Summarizer.py - 使用 LLM 分析论文，生成 labels 和 notes

修复记录 (2026-05-15):
- 修复: 支持从 config.json 读取 LLM 配置
- 修复: 支持多 provider 切换 (deepseek/tencent_token/kimi)
- 修复: 支持多种 API Key 来源 (参数 > 环境变量 > config.json)
- 修复: 添加 --provider 和 --api-key 命令行参数
- 修复: 支持多个环境变量名 (DEEPSEEK_API_KEY, TENCENTTOKENHUB_API_KEY 等)
- 修复: 删除文件末尾重复粘贴的多份代码

使用方式:
    # Python
    from summarize.Summarizer import Summarizer
    summarizer = Summarizer(kb_path="index.json", provider="deepseek")
    kb = summarizer.summarize()

    # CLI
    python3 Summarizer.py --kb-path index.json --provider deepseek
    python3 Summarizer.py --kb-path index.json --provider deepseek --api-key sk-xxx
"""

import os
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional, Any


class Summarizer:
    """文献总结器 - 为知识库中的论文添加 labels 和 notes（初始化时绑定知识库路径）"""

    def __init__(self,
                 kb_path: str = "index.json",
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 model: Optional[str] = None,
                 provider: Optional[str] = None,
                 use_conversation: bool = False):
        """
        初始化 Summarizer（绑定知识库路径）
        
        配置优先级（从高到低）:
        1. 直接传入的参数 (api_key, base_url, model)
        2. 环境变量 (DEEPSEEK_API_KEY / TOKENHUB_API_KEY / KIMI_API_KEY 等)
        3. config.json 中的 provider 配置
        
        Args:
            kb_path: 知识库文件路径（默认 index.json）
            api_key: API key
            base_url: API base URL
            model: 模型名称
            provider: LLM 提供商名称 (deepseek / tencent_token / kimi)，用于从 config.json 读取配置
            use_conversation: 是否使用会话模式（保留对话历史），默认 False
        """
        self.kb_path = kb_path
        self.use_conversation = use_conversation
        self.conversation_history = []  # 会话历史
        
        # 加载配置
        config = self._load_config()
        
        # 确定 provider
        self.provider = provider or config.get('default_provider', 'deepseek')
        provider_config = config.get('providers', {}).get(self.provider, {})
        
        # 设置 base_url（优先级: 参数 > config.json）
        self.base_url = base_url or provider_config.get('base_url', 'https://api.deepseek.com/v1')
        
        # 设置 model（优先级: 参数 > config.json）
        self.model = model or provider_config.get('default_model', 'deepseek-chat')
        
        # 设置 api_key（优先级: 参数 > 环境变量 > config.json）
        self.api_key = api_key
        if not self.api_key:
            # 按优先级尝试多个环境变量
            env_candidates = [
                provider_config.get('api_key_env', ''),
                'DEEPSEEK_API_KEY',
                'TOKENHUB_API_KEY',
                'TENCENTTOKENHUB_API_KEY',
                'KIMI_API_KEY',
            ]
            for env_name in env_candidates:
                if env_name:
                    value = os.environ.get(env_name)
                    if value and value.strip():
                        self.api_key = value.strip()
                        break
        
        # 最后尝试 config.json 中的明文 api_key（不推荐，但兼容旧配置）
        if not self.api_key:
            self.api_key = provider_config.get('api_key', '')
        
        if not self.api_key:
            raise ValueError(
                f"无法获取 API Key。请通过以下任一方式设置:\n"
                f"  1. 命令行参数: --api-key YOUR_KEY\n"
                f"  2. 环境变量: export DEEPSEEK_API_KEY=your_key (或 TOKENHUB_API_KEY / KIMI_API_KEY)\n"
                f"  3. 修改 config.json 中对应 provider 的 api_key 字段\n"
                f"当前 provider: {self.provider}, base_url: {self.base_url}, model: {self.model}"
            )
        
        self._init_openai()
        self._init_system_prompt()

    def _load_config(self) -> Dict:
        """加载 config.json 中的 llm 配置"""
        # 尝试多个路径
        search_paths = [
            os.path.join(os.path.dirname(__file__), '..', '..', 'config.json'),
            os.path.join(os.path.dirname(__file__), '..', 'config.json'),
            'config.json',
        ]
        for config_path in search_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        full_config = json.load(f)
                    return full_config.get('llm', {})
                except Exception:
                    continue
        return {}

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

    def summarize(self, progress_interval: int = 10) -> Dict:
        """
        分析知识库中所有论文，添加 labels 和 notes，保存并返回知识库
        Args:
            progress_interval: 进度打印间隔
        Returns:
            更新后的知识库字典
        """
        # 加载知识库
        kb_data = self._load_kb(self.kb_path)
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
        self._save_kb(kb_data, self.kb_path)
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
        
        if self.use_conversation:
            # 会话模式：保留对话历史
            if not self.conversation_history:
                # 第一次请求，添加system prompt
                self.conversation_history.append({"role": "system", "content": self.system_prompt})
            self.conversation_history.append({"role": "user", "content": user_prompt})
            messages = self.conversation_history
        else:
            # 非会话模式：每次都是新对话
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
            
            if self.use_conversation:
                # 会话模式：保存助手响应到历史
                self.conversation_history.append({"role": "assistant", "content": content})
            
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


# ==================== 命令行入口 ====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Summarizer - 文献总结工具 (修复版 v1.1)"
    )
    parser.add_argument(
        "--kb-path", 
        default="index.json", 
        help="知识库文件路径 (默认: index.json)"
    )
    parser.add_argument(
        "--provider",
        default="deepseek",
        choices=["deepseek", "tencent_token", "kimi"],
        help="LLM 提供商 (默认: deepseek)"
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API Key (默认从环境变量或 config.json 读取)"
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="API Base URL (覆盖 config.json 配置)"
    )
    parser.add_argument(
        "--model",
        default=None,
        help="模型名称 (覆盖 config.json 配置)"
    )
    parser.add_argument(
        "--progress-interval", 
        type=int, 
        default=10, 
        help="进度打印间隔 (默认: 10)"
    )
    parser.add_argument(
        "--use-conversation",
        action="store_true",
        help="使用会话模式（默认不使用会话模式）"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.kb_path):
        print(f"错误: 知识库文件不存在: {args.kb_path}")
        import sys
        sys.exit(1)
    
    print(f"正在总结文献...")
    print(f"  Provider: {args.provider}")
    print(f"  KB Path: {args.kb_path}")
    
    summarizer = Summarizer(
        kb_path=args.kb_path,
        provider=args.provider,
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model,
        use_conversation=args.use_conversation
    )
    
    print(f"  Model: {summarizer.model}")
    print(f"  Base URL: {summarizer.base_url}")
    print(f"  API Key: {summarizer.api_key[:10]}...")
    
    kb = summarizer.summarize(
        progress_interval=args.progress_interval
    )
    
    print(f"\n完成! 知识库: {args.kb_path}")
    print(f"  论文总数: {len(kb['papers'])}")
    print(f"  实证文献: {kb['statistics']['empirical_count']}")
    print(f"  综述文献: {kb['statistics']['review_count']}")
    print(f"  理论文献: {kb['statistics']['theory_count']}")
