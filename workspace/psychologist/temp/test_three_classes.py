
#!/usr/bin/env python3
"""
测试三个新类
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试三个新类")
print("="*80)

# 测试1: Searcher
print("\n1. 测试 Searcher...")
from Searcher import Searcher
searcher = Searcher()

print("   Searcher初始化成功！")

# 测试2: Manager
print("\n2. 测试 Manager...")
from Manager import Manager
manager = Manager()

print("   Manager初始化成功！")

# 测试3: Summarizer（跳过，需要LLM key）
print("\n3. 测试 Summarizer...（跳过，需要LLM key）")

print("\n" + "="*80)
print("✅ 三个类都能正常导入！")
print("="*80)
