
#!/usr/bin/env python3
"""
测试两个腾讯云的deepseek
"""

import sys
import os
import json

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

# 1. 读取config.json
CONFIG_PATH = "/root/.openclaw/skills/knowledge-manager/config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 2. 显式获取API密钥
api_key_env = "LKEAP_API_KEY"
api_key = os.environ.get(api_key_env)

if not api_key:
    print(f"错误: 环境变量 {api_key_env} 未设置!")
    sys.exit(1)

print("="*80)
print("测试两个腾讯云的deepseek")
print("="*80)
print(f"\nAPI key: {len(api_key)} chars")

# 3. 定义两个测试配置
test_configs = [
    {
        "name": "腾讯云LKE",
        "base_url": "https://api.lkeap.cloud.tencent.com/v1",
        "model": "deepseek-v3.2"
    },
    {
        "name": "腾讯云tokenhub",
        "base_url": "https://tokenhub.tencentmaas.com/v1",
        "model": "deepseek-v3.2"
    }
]

# 4. 逐个测试
for i, test_cfg in enumerate(test_configs, 1):
    print(f"\n{'='*80}")
    print(f"测试 {i}/{len(test_configs)}: {test_cfg['name']}")
    print(f"{'='*80}")
    print(f"  base_url: {test_cfg['base_url']}")
    print(f"  model: {test_cfg['model']}")
    
    try:
        import openai
        client = openai.OpenAI(
            api_key=api_key,
            base_url=test_cfg['base_url']
        )
        
        resp = client.chat.completions.create(
            model=test_cfg['model'],
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

print("\n" + "="*80)
print("测试完成")
print("="*80)
