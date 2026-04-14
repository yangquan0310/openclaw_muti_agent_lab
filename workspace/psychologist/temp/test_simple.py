
#!/usr/bin/env python3
"""
简单测试文件
"""

print("测试开始...")

import os
import sys
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

print("导入模块...")
try:
    from AcademicSearchSummarizer import AcademicSearchSummarizer
    print("✅ 导入成功！")
    
    # 设置环境变量
    os.environ['SEMANTIC_SCHOLAR_API_KEY'] = 'KpNolzKwWrMhKMZW0XHq5jBhmBfOfNg3Q0sErPdi'
    
    # 初始化
    print("初始化...")
    ass = AcademicSearchSummarizer()
    print("✅ 初始化成功！")
    
    print("\n🎉 测试通过！")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n测试结束")
