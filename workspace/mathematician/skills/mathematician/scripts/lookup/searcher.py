#!/usr/bin/env python3
"""
Mathematician References 搜索引擎
基于关键词匹配 + 语义相似度排序
"""

import json
import re
from pathlib import Path
from typing import Any


class ReferencesSearcher:
    def __init__(self, skill_dir: Path):
        self.skill_dir = skill_dir
        self.index_dir = skill_dir / "scripts" / "lookup" / "index"
        self._load_index()
    
    def _load_index(self):
        """加载索引"""
        manifest_path = self.index_dir / "manifest.json"
        chunks_path = self.index_dir / "chunks.json"
        
        if not manifest_path.exists():
            raise FileNotFoundError(f"索引不存在。请运行: python3 -m scripts.lookup.indexer")
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            self.manifest = json.load(f)
        
        if chunks_path.exists():
            with open(chunks_path, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
        else:
            self.chunks = []
    
    # 停用词（查询时过滤）
    STOPWORDS = {'是', '的', '了', '在', '和', '与', '或', '不', '一个', '什么', '怎么', '如何', '为什么', '哪些', '哪个', '有', '没有', '这', '那', '我', '你', '他', '她', '它', '们'}
    
    def _tokenize(self, text: str, filter_stopwords: bool = False) -> set[str]:
        """分词"""
        text = text.lower()
        # 英文词
        words = re.findall(r'[a-z]+', text)
        # 中文单字
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        # 中文2-gram
        chinese_2gram = [text[i:i+2] for i in range(len(text)-1) 
                         if re.match(r'[\u4e00-\u9fff]{2}', text[i:i+2])]
        tokens = set(words + chinese_chars + chinese_2gram)
        
        if filter_stopwords:
            tokens = tokens - self.STOPWORDS
        
        return tokens
    
    def _calculate_score(self, query_tokens: set[str], text: str, keywords: list[str] = None) -> float:
        """计算匹配分数"""
        text_tokens = self._tokenize(text)
        common = query_tokens & text_tokens
        
        if not common:
            return 0.0
        
        score = len(common) / len(query_tokens)
        
        if keywords:
            keyword_tokens = self._tokenize(' '.join(keywords))
            keyword_match = common & keyword_tokens
            if keyword_match:
                score += 0.5 * len(keyword_match) / len(keyword_tokens)
        
        return min(score, 1.0)
    
    def search_files(self, query: str) -> list[tuple[str, float]]:
        """搜索文件级别匹配"""
        query_tokens = self._tokenize(query, filter_stopwords=True)
        results = []
        
        for filename, data in self.manifest.items():
            title_score = self._calculate_score(query_tokens, data['title'], data.get('keywords', []))
            desc_score = self._calculate_score(query_tokens, data['description'])
            kw_score = 0.0
            if 'keywords' in data:
                kw_score = self._calculate_score(query_tokens, ' '.join(data['keywords']))
            
            section_score = 0.0
            for section in data.get('sections', []):
                section_score = max(section_score, self._calculate_score(query_tokens, section['heading']))
            
            total_score = max(title_score, desc_score, kw_score, section_score)
            
            if total_score > 0:
                results.append((filename, total_score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def search_chunks(self, query: str, file_filter: str = None) -> list[dict[str, Any]]:
        """搜索章节块级别匹配"""
        query_tokens = self._tokenize(query)
        results = []
        
        for chunk in self.chunks:
            if file_filter and chunk['file'].startswith(file_filter):
                continue
            
            heading_score = self._calculate_score(query_tokens, chunk['heading'])
            content_score = self._calculate_score(query_tokens, chunk.get('content_preview', ''))
            
            total_score = max(heading_score, content_score * 0.7)
            
            if total_score > 0:
                results.append({
                    **chunk,
                    'score': total_score
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:10]
    
    def search(self, query: str, show_chunks: bool = True) -> dict[str, Any]:
        """综合搜索"""
        file_results = self.search_files(query)
        
        if not file_results:
            return {"files": [], "chunks": [], "query": query}
        
        top_files = file_results[:3]
        
        chunks_results = []
        if show_chunks:
            for filename, _ in top_files[:2]:
                file_chunks = self.search_chunks(query, file_filter=filename)
                chunks_results.extend(file_chunks[:3])
        
        seen = set()
        unique_chunks = []
        for chunk in chunks_results:
            if chunk['id'] not in seen:
                seen.add(chunk['id'])
                unique_chunks.append(chunk)
        unique_chunks.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            "query": query,
            "files": [{"file": f, "score": s, **self.manifest[f]} for f, s in top_files],
            "chunks": unique_chunks[:5]
        }


def format_results(results: dict[str, Any]) -> str:
    """格式化输出"""
    output = []
    
    output.append(f"\n🔢 查询: {results['query']}")
    output.append("=" * 60)
    
    if not results['files']:
        output.append("\n❌ 没有找到相关内容")
        return '\n'.join(output)
    
    output.append("\n📚 相关指南:")
    for i, file_data in enumerate(results['files'], 1):
        score_stars = "★" * int(file_data['score'] * 5) + "☆" * (5 - int(file_data['score'] * 5))
        output.append(f"\n{i}. {file_data['title']}")
        output.append(f"   文件: {file_data['file']}")
        output.append(f"   匹配度: {score_stars} ({file_data['score']:.2f})")
        output.append(f"   描述: {file_data['description']}")
    
    if results['chunks']:
        output.append("\n\n📖 相关章节:")
        for chunk in results['chunks']:
            output.append(f"\n▶ {chunk['heading']}")
            output.append(f"  文件: {chunk['file']}")
            if 'content_preview' in chunk:
                preview = chunk['content_preview'][:150]
                if len(chunk['content_preview']) > 150:
                    preview += "..."
                output.append(f"  预览: {preview}")
    
    output.append("\n")
    return '\n'.join(output)


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='搜索 Mathematician 数学指南')
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--files-only', '-f', action='store_true', help='只显示文件匹配')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有已索引的文件')
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent.parent
    
    index_dir = script_dir / "index"
    if not (index_dir / "manifest.json").exists():
        print("❌ 索引不存在，请先运行索引构建器:")
        print(f"   python3 -m scripts.lookup.indexer")
        return
    
    searcher = ReferencesSearcher(skill_dir)
    
    if args.list:
        print("\n📚 已索引的指南:")
        print("=" * 60)
        for filename, data in searcher.manifest.items():
            print(f"\n• {data['title']}")
            print(f"  文件: {data['file']}")
            print(f"  关键词: {', '.join(data['keywords'][:5])}...")
        print()
        return
    
    if not args.query:
        parser.print_help()
        return
    
    results = searcher.search(args.query, show_chunks=not args.files_only)
    print(format_results(results))


if __name__ == "__main__":
    main()
