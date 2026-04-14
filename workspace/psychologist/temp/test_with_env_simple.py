
#!/usr/bin/env python3
"""
测试tencent_tokenhub，直接读取.env文件
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

# 1. 读取config.json
CONFIG_PATH = "/root/.openclaw/skills/knowledge-manager/config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

tencent_config = config['llm']['providers']['tencent']

# 2. 显式获取API密钥
api_key_env = tencent_config['api_key_env']
api_key = os.environ.get(api_key_env)

if not api_key:
    print(f"错误: 环境变量 {api_key_env} 未设置!")
    print(f"当前环境变量: {list(os.environ.keys())}")
    sys.exit(1)

print("="*80)
print("测试tencent_tokenhub（直接读取.env）")
print("="*80)
print(f"\n使用配置: {tencent_config['name']}")
print(f"  base_url: {tencent_config['base_url']}")
print(f"  model: {tencent_config['default_model']}")
print(f"  API key: {len(api_key)} chars")

# 3. 尝试直接调用
print("\n尝试直接调用API...")
try:
    import openai
    client = openai.OpenAI(
        api_key=api_key,
        base_url=tencent_config['base_url']
    )
    
    resp = client.chat.completions.create(
        model=tencent_config['default_model'],
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
    print(f"\n❌ 调用失败!")
    print(f"  错误类型: {type(e).__name__}")
    print(f"  错误信息: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
