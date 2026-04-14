
#!/usr/bin/env python3
"""
测试老板修改后的Summarizer.py
"""

import sys
import os
import json

# 直接读取.env文件
dotenv_path = "/root/.openclaw/.env"
if os.path.exists(dotenv_path):
    with open(dotenv_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
    print("已从.env加载环境变量")

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

# 1. 导入Summarizer
print("="*80)
print("测试老板修改后的Summarizer.py")
print("="*80)

# 手动设置api_key_env（因为老板修改后__init__里用了api_key_env但没定义）
api_key_env = "TOKENHUB_API_KEY"

from Summarizer import Summarizer

# 2. 初始化并测试
try:
    print("\n正在初始化Summarizer...")
    summarizer = Summarizer()
    print(f"✅ 初始化成功!")
    print(f"  base_url: {summarizer.base_url}")
    print(f"  model: {summarizer.model}")
    print(f"  API key: {len(summarizer.api_key)} chars")
    
    # 3. 测试简单调用
    print("\n正在测试简单调用...")
    resp = summarizer.client.chat.completions.create(
        model=summarizer.model,
        messages=[
            {"role": "system", "content": "你是一个助手。"},
            {"role": "user", "content": "你好，请回复'测试成功'。"}
        ],
        temperature=0.1,
        max_tokens=20
    )
    
    print(f"\n✅ 调用成功!")
    print(f"  响应: {resp.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ 失败!")
    print(f"  错误类型: {type(e).__name__}")
    print(f"  错误信息: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
