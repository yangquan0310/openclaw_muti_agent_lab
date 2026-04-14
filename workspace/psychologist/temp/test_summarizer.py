#!/usr/bin/env python3
"""
简单测试脚本
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

ark_config = config['llm']['providers']['ark']

# 2. 显式获取API密钥
api_key_env = ark_config['api_key_env']
api_key = os.environ.get(api_key_env)

print("="*80)
print("测试脚本")
print("="*80)
print(f"\n使用配置: {ark_config['name']}")
print(f"  base_url: {ark_config['base_url']}")
print(f"  model: {ark_config['default_model']}")
print(f"  API key: {len(api_key)} chars")

print("\n环境变量检查:")
print(f"  ARK_API_KEY: {os.environ.get('ARK_API_KEY', 'not found')}")
print(f"  LKEAP_API_KEY: {os.environ.get('LKEAP_API_KEY', 'not found')[:10]}...")

# 3. 尝试导入Summarizer
try:
    print("\n尝试导入Summarizer...")
    from Summarizer import Summarizer
    print("  Summarizer导入成功!")
    
    # 测试初始化
    print("\n尝试初始化Summarizer...")
    summarizer = Summarizer(
        api_key=api_key,
        base_url=ark_config['base_url'],
        model=ark_config['default_model']
    )
    print("  Summarizer初始化成功!")
    
    # 测试简单的调用
    print("\n测试简单的API调用...")
    test_title = "测试标题"
    test_abstract = "这是一个测试摘要"
    result = summarizer._summarize_single(test_title, test_abstract)
    print(f"  成功! 结果: {result}")
    
except Exception as e:
    print(f"  错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("测试完成!")
print("="*80)
