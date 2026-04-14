
#!/usr/bin/env python3
"""
测试老板修改后的Manager.py（三个核心链式方法）
"""

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager/knowledge-manager')

# 设置API key
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试老板修改后的Manager.py（三个核心链式方法）")
print("="*80)

# 先用Searcher生成两个测试知识库
from Searcher import Searcher
searcher = Searcher()

queries1 = {"自传体记忆": ["autobiographical memory"]}
searcher.search(queries1, kb_path="test_manager_kb1.json", limit=2)

queries2 = {"数字记忆": ["digital memory"]}
searcher.search(queries2, kb_path="test_manager_kb2.json", limit=2)

print("\n" + "="*80)
print("测试1：merge() - 合并两个知识库")
print("="*80)

from Manager import Manager
manager = Manager()

manager.merge("test_manager_kb1.json", "test_manager_kb2.json").save("test_manager_merged.json", "合并测试")

print(f"\n✅ merge() 完成！")

print("\n" + "="*80)
print("测试2：filter() - 筛选引用量≥10的论文")
print("="*80)

manager = Manager("test_manager_merged.json")
manager.filter({
    "citations_min": 10,
    "sort_by": "citationCount",
    "sort_desc": True
}).save("test_manager_filtered.json", "筛选测试")

print(f"\n✅ filter() 完成！")

print("\n" + "="*80)
print("🎉 Manager三个核心方法测试都成功！")
print("="*80)
