
#!/usr/bin/env python3
"""
最终测试：修复后的AcademicSearchSummarizer
"""

import os
import sys
import time
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

from AcademicSearchSummarizer import AcademicSearchSummarizer

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("最终测试：修复后的AcademicSearchSummarizer")
print("="*80)

# 找一篇测试用的paperId（从刚才的成功测试里取）
test_paper_id = "13241a844c714549c173e239714ae020386172e3"

print(f"\n测试paperId: {test_paper_id}")

# 初始化
ass = AcademicSearchSummarizer()
searcher = ass.searcher

print(f"\n调用修复后的_fetch_paper_details...")

# 等待一下避免速率限制
time.sleep(3)

result = searcher._fetch_paper_details(test_paper_id)

if result:
    print(f"\n✅ 成功获取数据！")
    print(f"\n返回的字段: {list(result.keys())}")
    print(f"\n详细内容:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(f"\n📊 元数据提取:")
    print(f"  volume: '{result.get('volume')}'")
    print(f"  pages: '{result.get('pages')}'")
    print(f"  doi: '{result.get('doi')}'")
    print(f"  journal_name: '{result.get('journal_name')}'")
else:
    print(f"\n❌ 获取失败")

print(f"\n{'='*80}")
