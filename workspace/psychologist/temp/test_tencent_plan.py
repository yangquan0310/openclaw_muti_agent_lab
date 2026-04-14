
#!/usr/bin/env python3
"""
测试tencent_plan配置
"""

import sys
import os
import json

# 1. 读取config.json
CONFIG_PATH = "/root/.openclaw/skills/knowledge-manager/config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

tencent_plan_config = config['llm']['providers']['tencent_plan']

print("="*80)
print("测试tencent_plan配置")
print("="*80)

# 2. 检查环境变量
api_key_env = tencent_plan_config['api_key_env']
api_key = os.environ.get(api_key_env)

print(f"\n配置信息:")
print(f"  name: {tencent_plan_config['name']}")
print(f"  base_url: {tencent_plan_config['base_url']}")
print(f"  default_model: {tencent_plan_config['default_model']}")
print(f"  api_key_env: {api_key_env}")
print(f"  API key已设置: {'是' if api_key else '否'}")

if not api_key:
    print(f"\n错误: 环境变量 {api_key_env} 未设置!")
    sys.exit(1)

# 3. 尝试调用
print("\n尝试调用tencent_plan...")
try:
    import openai
    client = openai.OpenAI(
        api_key=api_key,
        base_url=tencent_plan_config['base_url']
    )
    
    response = client.chat.completions.create(
        model=tencent_plan_config['default_model'],
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
    
    # 尝试测试tencent标准配置
    print("\n" + "="*80)
    print("尝试测试tencent标准配置...")
    print("="*80)
    
    try:
        tencent_config = config['llm']['providers']['tencent']
        print(f"\n配置信息:")
        print(f"  name: {tencent_config['name']}")
        print(f"  base_url: {tencent_config['base_url']}")
        print(f"  default_model: {tencent_config['default_model']}")
        
        client2 = openai.OpenAI(
            api_key=api_key,
            base_url=tencent_config['base_url']
        )
        
        response2 = client2.chat.completions.create(
            model=tencent_config['default_model'],
            messages=[
                {"role": "system", "content": "你是一个助手。"},
                {"role": "user", "content": "你好，请回复'测试成功'。"}
            ],
            temperature=0.1,
            max_tokens=20
        )
        
        print(f"\n✅ tencent标准配置调用成功!")
        print(f"  响应: {response2.choices[0].message.content}")
        
    except Exception as e2:
        print(f"\n❌ tencent标准配置调用失败!")
        print(f"  错误类型: {type(e2).__name__}")
        print(f"  错误信息: {e2}")

print("\n" + "="*80)
