
import json
import sys
import os

# 定义文件列表
files = [
    {
        "name": "自传体记忆基础",
        "file_id": "WrazKpLjQVJT",
        "local_path": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆基础.md"
    },
    {
        "name": "自传体记忆功能",
        "file_id": "WZXDDuemDKfW",
        "local_path": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆功能.md"
    },
    {
        "name": "自传体记忆的自我参照编码",
        "file_id": "WZFPUbOhtGsk",
        "local_path": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的自我参照编码.md"
    },
    {
        "name": "自传体记忆的生成性提取",
        "file_id": "WqVJqLdJqTdW",
        "local_path": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的生成性提取.md"
    },
    {
        "name": "自传体记忆的系统性巩固",
        "file_id": "WGruGuTUNVjM",
        "local_path": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的系统性巩固.md"
    },
    {
        "name": "自传体记忆的主动遗忘",
        "file_id": "WdvQGMZnxGpp",
        "local_path": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的主动遗忘.md"
    }
]

for file_info in files:
    print(f"\n处理: {file_info['name']}")

    # 读取本地文件
    try:
        with open(file_info['local_path'], 'r', encoding='utf-8') as f:
            content = f.read()

        # 由于内容很长，我们写一个摘要版本用于MDX
        # 先提取前5000字符
        short_content = content[:8000] + "\n\n---\n\n**说明**：本文档为摘要版本，完整内容请查看本地文件。"

        # 构建参数
        params = {
            "file_id": file_info['file_id'],
            "action": "INSERT_AFTER",
            "id": "",  # 追加到文档末尾
            "content": short_content
        }

        # 写入临时参数文件
        param_file = f"/root/.openclaw/workspace/writer/temp/temp_param_{file_info['file_id']}.json"
        with open(param_file, 'w', encoding='utf-8') as f:
            json.dump(params, f, ensure_ascii=False)

        print(f"  参数文件已写入: {param_file}")
        print(f"  请手动执行: mcporter call tencent-docs smartcanvas.edit --args @{param_file}")

    except Exception as e:
        print(f"  错误: {e}")

print("\n所有文件准备完毕！")
