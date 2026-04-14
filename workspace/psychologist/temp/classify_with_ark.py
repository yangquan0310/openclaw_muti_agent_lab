#!/usr/bin/env python3
"""
用ARK模型分类数字化存储与自传体记忆知识库
"""

import sys
import os
import json
import re
import shutil
from datetime import datetime

# 添加skill目录到路径
sys.path.insert(0, '/root/.openclaw/skills/knowledge-manager')

# 1. 读取config.json
CONFIG_PATH = "/root/.openclaw/skills/knowledge-manager/config.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 使用ARK模型
ark_config = config['llm']['providers']['ark']

print("="*80)
print("用ARK模型分类数字化存储与自传体记忆知识库")
print("="*80)

# 2. 定义7个主题
SEVEN_TOPICS = [
    "自传体记忆基础",
    "自传体记忆的自我参照编码",
    "自传体记忆功能",
    "自传体记忆的主动遗忘",
    "自传体记忆的系统性巩固",
    "数字化使用对自传体记忆的影响",
    "自传体记忆的生成性提取"
]

# 3. 知识库路径
KB_PATH = "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json"

# 4. 备份
if os.path.exists(KB_PATH):
    backup_path = KB_PATH + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(KB_PATH, backup_path)
    print(f"已备份到: {backup_path}")

# 5. 加载知识库
with open(KB_PATH, 'r', encoding='utf-8') as f:
    kb = json.load(f)

papers = kb['papers']
print(f"\n总论文数: {len(papers)}")

# 6. 初始化OpenAI client
import openai

api_key = os.environ.get(ark_config['api_key_env'])
if not api_key:
    print(f"错误: 请设置环境变量 {ark_config['api_key_env']}")
    sys.exit(1)

client = openai.OpenAI(
    api_key=api_key,
    base_url=ark_config['base_url']
)

# 7. 定义分类提示词 - 更明确
CLASSIFICATION_PROMPT = """你是一位专业的心理学文献分类专家。根据论文标题和摘要，将其分到以下7个主题中的一个，且只能分到一个主题：

## 7个主题定义

1. 自传体记忆基础
   - 定义、结构、模型、理论框架
   - 关键词: autobiographical memory, self-memory system, Conway, life story, reminiscence

2. 自传体记忆的自我参照编码
   - 自我参照效应、自我相关编码
   - 关键词: self-reference effect, self-referential encoding, self-related

3. 自传体记忆功能
   - 自我功能、社会功能、指导功能
   - 关键词: function, social, self-continuity, identity, directive

4. 自传体记忆的主动遗忘
   - 定向遗忘、有意遗忘、压抑
   - 关键词: directed forgetting, intentional forgetting, suppression, repression

5. 自传体记忆的系统性巩固
   - 记忆巩固、睡眠与记忆
   - 关键词: consolidation, sleep, memory consolidation, systems consolidation

6. 数字化使用对自传体记忆的影响
   - 拍照效应、Google效应、认知卸载、数字记忆
   - 关键词: photo taking, Google effect, cognitive offloading, digital memory, photographing

7. 自传体记忆的生成性提取
   - 精细提取、生成性检索、回忆策略
   - 关键词: generative retrieval, constructive recall, retrieval, recollection

## 任务
根据论文标题和摘要，判断它最适合哪个主题，返回主题编号（1-7）。

## 输出格式
用JSON格式返回，格式如下：
{"topic": 编号}

只返回JSON，不要有其他任何内容。"""

# 8. 逐个分类
print("\n开始分类论文到7个主题...")

topic_counts = {topic: 0 for topic in SEVEN_TOPICS}
fail_count = 0

for i, paper in enumerate(papers, 1):
    title = paper.get('title', '')
    abstract = paper.get('abstract', '')
    
    # 分类
    success = False
    for attempt in range(3):  # 最多重试3次
        try:
            response = client.chat.completions.create(
                model=ark_config['default_model'],
                messages=[
                    {"role": "system", "content": CLASSIFICATION_PROMPT},
                    {"role": "user", "content": f"标题: {title}\n\n摘要: {abstract}"}
                ],
                temperature=0.1,
                max_tokens=50
            )
            content = response.choices[0].message.content.strip()
            
            # 尝试解析JSON
            try:
                result = json.loads(content)
                topic_num = int(result['topic'])
            except:
                # 如果JSON解析失败，尝试提取数字
                match = re.search(r'(\d+)', content)
                if match:
                    topic_num = int(match.group(1))
                else:
                    raise ValueError(f"无法从响应中提取数字: {content}")
            
            if 1 <= topic_num <= 7:
                topic = SEVEN_TOPICS[topic_num - 1]
                paper['topic'] = [topic]
                topic_counts[topic] += 1
                success = True
                break
            else:
                raise ValueError(f"无效的主题编号: {topic_num}")
                
        except Exception as e:
            if attempt == 2:  # 最后一次尝试
                print(f"  警告: 第{i}篇分类失败: {e}")
            else:
                continue
    
    if not success:
        paper['topic'] = ["分类失败"]
        fail_count += 1
    
    if i % 10 == 0 or i == len(papers):
        print(f"  进度: {i}/{len(papers)} ({i/len(papers)*100:.1f}%) - 失败: {fail_count}")

# 9. 显示分类结果
print("\n" + "="*80)
print("分类结果")
print("="*80)
for topic, count in topic_counts.items():
    print(f"  {topic}: {count} 篇")
print(f"  分类失败: {fail_count} 篇")
print("="*80)

# 10. 保存
kb['papers'] = papers
kb['updated_at'] = datetime.now().isoformat()

with open(KB_PATH, 'w', encoding='utf-8') as f:
    json.dump(kb, f, ensure_ascii=False, indent=2)

print(f"\n保存完成: {KB_PATH}")
print("="*80)
