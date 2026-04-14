
#!/usr/bin/env python3
"""
测试老板修改后的两个核心方法
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager/knowledge-manager')

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试老板修改后的两个核心方法")
print("="*80)

from Searcher import Searcher

searcher = Searcher()

# ========================================
# 方法1：search() - 检索并保存
# ========================================
print("\n" + "="*80)
print("方法1：search() - 检索并保存")
print("="*80)

queries = {
    "自传体记忆": ["autobiographical memory"]
}

kb = searcher.search(queries, kb_path="test_two_methods.json", limit=2)

print(f"\n✅ search() 完成！")
print(f"   论文数: {len(kb['papers'])}")

# ========================================
# 方法2：update() - 更新知识库元数据
# ========================================
print("\n" + "="*80)
print("方法2：update() - 更新知识库元数据")
print("="*80)

kb = searcher.update(kb_path="test_two_methods.json")

print(f"\n✅ update() 完成！")
print(f"   论文数: {len(kb['papers'])}")

print("\n" + "="*80)
print("🎉 两个核心方法测试都成功！")
print("="*80)
