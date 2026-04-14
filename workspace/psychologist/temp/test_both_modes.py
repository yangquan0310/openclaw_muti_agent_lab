
#!/usr/bin/env python3
"""
测试老板修改后的两种模式
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager/knowledge-manager')

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试老板修改后的两种模式")
print("="*80)

from Searcher import Searcher

searcher = Searcher()

# ========================================
# 模式1：检索模式 - search_relevance()
# ========================================
print("\n" + "="*80)
print("模式1：检索模式 - search_relevance()")
print("="*80)

queries = {
    "自传体记忆": ["autobiographical memory"]
}

searcher.search_relevance(queries, limit=2).save("test_search_output.json", "测试检索")

print("\n✅ 检索模式测试完成！")

# ========================================
# 模式2：更新模式 - load_and_fetch()
# ========================================
print("\n" + "="*80)
print("模式2：更新模式 - load_and_fetch()")
print("="*80)

# 用刚才生成的文件测试
searcher.load_and_fetch("test_search_output.json")

print("\n✅ 更新模式测试完成！")

print("\n" + "="*80)
print("🎉 两种模式测试都成功！")
print("="*80)
