
#!/usr/bin/env python3
"""
测试老板修改后的Summarizer.py - 简化版，直接测试
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

# 1. 直接用openai测试，不通过Summarizer
print("="*80)
print("直接测试API（不通过Summarizer）")
print("="*80)

try:
    import openai
    client = openai.OpenAI(
        api_key=os.environ.get('TOKENHUB_API_KEY'),
        base_url="https://tokenhub.tencentmaas.com/v1"
    )
    
    print(f"\nAPI配置:")
    print(f"  base_url: https://tokenhub.tencentmaas.com/v1")
    print(f"  model: deepseek-v3.2")
    print(f"  API key: {len(os.environ.get('TOKENHUB_API_KEY', ''))} chars")
    
    print("\n正在测试简单调用...")
    resp = client.chat.completions.create(
        model="deepseek-v3.2",
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
