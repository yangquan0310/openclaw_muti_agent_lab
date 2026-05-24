#!/usr/bin/env python3
"""
References 搜索引擎（中央版）
搜索指定技能的索引库。
"""

import json
import re
import argparse
import sys
from pathlib import Path
from typing import Any


class ReferencesSearcher:
    def __init__(self, index_dir: Path):
        self.index_dir = index_dir
        self._load_index()

    def _load_index(self):
        manifest_path = self.index_dir / "manifest.json"
        chunks_path = self.index_dir / "chunks.json"

        if not manifest_path.exists():
            raise FileNotFoundError(
                f"索引不存在。请先运行: lookup index --skill <技能名>"
            )

        with open(manifest_path, 'r', encoding='utf-8') as f:
            self.manifest = json.load(f)

        if chunks_path.exists():
            with open(chunks_path, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
        else:
            self.chunks = []

    STOPWORDS = {'是', '的', '了', '在', '和', '与', '或', '不', '一个', '什么',
                 '怎么', '如何', '为什么', '哪些', '哪个', '有', '没有', '这', '那',
                 '我', '你', '他', '她', '它', '们'}

    def _tokenize(self, text: str, filter_stopwords: bool = False) -> set[str]:
        text = text.lower()
        words = re.findall(r'[a-z]+', text)
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        chinese_2gram = [text[i:i+2] for i in range(len(text)-1)
                         if re.match(r'[\u4e00-\u9fff]{2}', text[i:i+2])]
        tokens = set(words + chinese_chars + chinese_2gram)
        if filter_stopwords:
            tokens = tokens - self.STOPWORDS
        return tokens

    def _calculate_score(self, query_tokens: set[str], text: str,
                          keywords: list[str] = None) -> float:
        text_tokens = self._tokenize(text)
        if not text_tokens:
            return 0.0
        overlap = len(query_tokens & text_tokens)
        score = overlap / len(query_tokens) if query_tokens else 0

        if keywords:
            for kw in keywords:
                if any(qt in kw.lower() for qt in query_tokens):
                    score += 0.1

        return score

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        query_tokens = self._tokenize(query, filter_stopwords=True)
        if not query_tokens:
            return []

        scored = []
        for chunk in self.chunks:
            text = chunk.get('heading', '') + ' ' + chunk.get('content_preview', '')
            score = self._calculate_score(query_tokens, text,
                                          chunk.get('keywords', []))
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda x: -x[0])
        return [item for _, item in scored[:top_k]]

    def search_files(self, query: str) -> list[tuple[float, dict[str, Any]]]:
        query_tokens = self._tokenize(query, filter_stopwords=True)
        if not query_tokens:
            return []

        scored = []
        for key, info in self.manifest.items():
            keywords = info.get('keywords', [])
            combined = ' '.join([info.get('title', ''),
                                  info.get('description', ''),
                                  ' '.join(keywords)])
            score = self._calculate_score(query_tokens, combined, keywords)
            if score > 0:
                scored.append((score, info))

        scored.sort(key=lambda x: -x[0])
        return scored

    def list_files(self) -> list[dict[str, Any]]:
        return list(self.manifest.values())


def resolve_skill_root(skill_name: str) -> Path | None:
    """解析技能根目录，支持 skills/ 和 workspace/ 两条路径。

    优先返回有 references/ 子目录的路径（真正的技能）。
    如果两者都有 references/，优先 workspace/ 路径。
    """
    candidates = [
        Path(f"/root/.openclaw/workspace/{skill_name}/skills/{skill_name}"),
        Path(f"/root/.openclaw/skills/{skill_name}"),
    ]

    # 优先：有 references/ 的路径
    for p in candidates:
        if p.exists() and (p / "references").is_dir():
            return p

    # 备选：第一个存在的路径
    for p in candidates:
        if p.exists():
            return p

    return None


def main():
    parser = argparse.ArgumentParser(
        description='搜索 References 指南'
    )
    parser.add_argument('query', nargs='?', help='搜索关键词')
    parser.add_argument('--skill',
                        help='技能名（默认 programmer）')
    parser.add_argument('--path',
                        help='技能根目录路径（与 --skill 二选一）')
    parser.add_argument('--files-only', '-f', action='store_true',
                        help='只显示文件匹配')
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有已索引文件')
    parser.add_argument('--top', '-k', type=int, default=5,
                        help='返回结果数（默认 5）')
    args = parser.parse_args()

    if not args.path:
        skill_arg = args.skill or 'programmer'
        skill_root = resolve_skill_root(skill_arg)
        if not skill_root:
            print(f"Error: 技能目录不存在: {skill_arg}")
            return 1
        skill_title = skill_arg.replace('-', ' ').title()
    else:
        skill_root = Path(args.path)
        skill_title = skill_root.name
        if not skill_root.exists():
            print(f"Error: 路径不存在: {args.path}")
            return 1

    index_dir = skill_root / "index"

    try:
        searcher = ReferencesSearcher(index_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        index_hint = f"lookup index --path {args.path}" if args.path else f"lookup index --skill {skill_arg}"
        print(f"\n请先构建索引: {index_hint}")
        return 1

    if args.list:
        files = searcher.list_files()
        print(f"【{skill_title}】已索引文件 ({len(files)}):\n")
        for info in files:
            title = info.get('title', info['file'])
            desc = info.get('description', '—')
            print(f"  • {title}")
            print(f"    {desc[:60]}...")
            print()
        return 0

    if not args.query:
        parser.print_help()
        return 0

    print(f"【{skill_title}】搜索: {args.query}\n")

    if args.files_only:
        results = searcher.search_files(args.query)
        if not results:
            print("  无匹配文件")
        for score, info in results:
            print(f"  • {info.get('title', info['file'])}")
            print(f"    匹配度: {score:.2f}")
    else:
        chunks = searcher.search(args.query, top_k=args.top)
        if not chunks:
            print("  无匹配内容，尝试 --files-only 扩大范围")
            return 0
        for chunk in chunks:
            print(f"  [{chunk['file']}] {chunk['heading']}")
            print(f"    {chunk.get('content_preview', '')[:100]}...")
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
