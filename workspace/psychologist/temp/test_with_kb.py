
#!/usr/bin/env python3
"""
测试完整流程：加载知识库 + 补全元数据
"""

import os
import sys
import time
import json

sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')
from AcademicSearchSummarizer import AcademicSearchSummarizer

os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'

print("="*80)
print("测试：加载知识库 + 补全元数据（只试1篇）")
print("="*80)

# 初始化
ass = AcademicSearchSummarizer()

# 加载知识库
kb_path = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"
print(f"\n1. 加载知识库: {kb_path}")
ass.load_knowledge_base(kb_path)
print(f"   加载了 {len(ass.all_papers)} 篇文献")

# 只取第一篇测试
paper = ass.all_papers[0]
paper_id = paper.get('paperId')
print(f"\n2. 测试第一篇文献:")
print(f"   paperId: {paper_id}")
print(f"   标题: {paper.get('title')}")
print(f"   当前volume: '{paper.get('volume')}'")
print(f"   当前pages: '{paper.get('pages')}'")
print(f"   当前doi: '{paper.get('doi')}'")

# 等待避免速率限制
print(f"\n3. 等待3秒避免速率限制...")
time.sleep(3)

# 调用fetch_full_metadata（只试这1篇）
print(f"\n4. 调用_fetch_paper_details...")
result = ass.searcher._fetch_paper_details(paper_id)

if result:
    print(f"\n5. ✅ 成功获取元数据！")
    print(f"\n返回的字段: {list(result.keys())}")
    print(f"\n详细内容:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(f"\n6. 📊 提取到的元数据:")
    print(f"   volume: '{result.get('volume')}'")
    print(f"   pages: '{result.get('pages')}'")
    print(f"   doi: '{result.get('doi')}'")
    print(f"   journal_name: '{result.get('journal_name')}'")
    
    # 更新这篇文献
    print(f"\n7. 更新文献...")
    for key, value in result.items():
        if value is not None and str(value).strip():
            paper[key] = value
    
    print(f"\n8. 📊 更新后:")
    print(f"   volume: '{paper.get('volume')}'")
    print(f"   pages: '{paper.get('pages')}'")
    print(f"   doi: '{paper.get('doi')}'")
else:
    print(f"\n5. ❌ 获取失败")

print(f"\n{'='*80}")
