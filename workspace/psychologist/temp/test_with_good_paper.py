
#!/usr/bin/env python3
"""
测试那篇有volume和pages的文献
"""

import os
import sys
import time
import json

sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')
from AcademicSearchSummarizer import AcademicSearchSummarizer

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试那篇有volume和pages的文献")
print("="*80)

# 这是刚才成功测试时找到的有volume和pages的paperId
test_paper_id = "13241a844c714549c173e239714ae020386172e3"

print(f"\ntest_paper_id: {test_paper_id}")

# 初始化
ass = AcademicSearchSummarizer()

# 等待避免速率限制
print(f"\n等待5秒避免速率限制...")
time.sleep(5)

# 调用
print(f"\n调用_fetch_paper_details...")
result = ass.searcher._fetch_paper_details(test_paper_id)

if result:
    print(f"\n✅ 成功获取元数据！")
    print(f"\n返回的字段: {list(result.keys())}")
    print(f"\n详细内容:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(f"\n📊 提取到的元数据:")
    print(f"   volume: '{result.get('volume')}'")
    print(f"   pages: '{result.get('pages')}'")
    print(f"   doi: '{result.get('doi')}'")
    print(f"   journal_name: '{result.get('journal_name')}'")
else:
    print(f"\n❌ 获取失败")

print(f"\n{'='*80}")
