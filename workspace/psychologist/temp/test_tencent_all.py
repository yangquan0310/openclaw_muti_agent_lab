
#!/usr/bin/env python3
"""
测试tencent_hub和tencent配置
"""

import sys
import os
import json

# 1. 读取config.json
CONFIG_PATH = "/root/.openclaw/skills/knowledge-manager/config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

providers_to_test = ['tencent', 'tencent_hub']

print("="*80)
print("测试tencent和tencent_hub配置")
print("="*80)

for provider_name in providers_to_test:
    provider_config = config['llm']['providers'][provider_name]
    
    print(f"\n{'='*80}")
    print(f"测试: {provider_config['name']}")
    print(f"{'='*80}")
    
    # 2. 检查环境变量
    api_key_env = provider_config['api_key_env']
    api_key = os.environ.get(api_key_env)
    
    print(f"\n配置信息:")
    print(f"  name: {provider_config['name']}")
    print(f"  base_url: {provider_config['base_url']}")
    print(f"  default_model: {provider_config['default_model']}")
    print(f"  api_key_env: {api_key_env}")
    print(f"  API key已设置: {'是' if api_key else '否'}")
    
    if not api_key:
        print(f"\n错误: 环境变量 {api_key_env} 未设置!")
        continue
    
    # 3. 尝试调用
    print("\n尝试调用...")
    try:
        import openai
        client = openai.OpenAI(
            api_key=api_key,
            base_url=provider_config['base_url']
        )
        
        response = client.chat.completions.create(
            model=provider_config['default_model'],
            messages=[
                {"role": "system", "content": "你是一个助手。"},
                {"role": "user", "content": "你好，请回复'测试成功'。"}
            ],
            temperature=0.1,
            max_tokens=20
        )
        
        print(f"\n✅ 调用成功!")
        print(f"  响应: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"\n❌ 调用失败!")
        print(f"  错误类型: {type(e).__name__}")
        print(f"  错误信息: {e}")

print(f"\n{'='*80}")
print("测试完成")
print(f"{'='*80}")
