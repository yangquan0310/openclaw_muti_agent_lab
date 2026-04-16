#!/usr/bin/env python3
"""
腾讯文档分段上传工具
将长文档切分成多个段落，逐段上传到腾讯文档
"""

import subprocess
import json
import sys

def run_mcporter(file_id, content):
    """调用 mcporter 上传一段内容"""
    args = {
        "file_id": file_id,
        "action": "INSERT_AFTER",
        "content": content
    }
    
    cmd = [
        "mcporter", "call", "tencent-docs", "smartcanvas.edit",
        "--args", json.dumps(args, ensure_ascii=False)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result.returncode == 0

def split_into_sections(file_path):
    """将文件切分成多个段落"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = []
    
    # 按主要章节切分
    lines = content.split('\n')
    current_section = []
    
    for line in lines:
        # 检测到新的主要标题时保存当前段落
        if line.startswith('## ') and current_section:
            sections.append('\n'.join(current_section))
            current_section = [line]
        else:
            current_section.append(line)
    
    # 添加最后一个段落
    if current_section:
        sections.append('\n'.join(current_section))
    
    return sections

def upload_to_tencent_docs(file_id, source_file):
    """上传文件到腾讯文档"""
    print("正在切分段落...")
    sections = split_into_sections(source_file)
    print(f"共切分成 {len(sections)} 个段落")
    
    # 跳过第一个标题（因为文档已创建）
    for i, section in enumerate(sections[1:], 2):
        print(f"正在上传第 {i}/{len(sections)} 段...")
        success = run_mcporter(file_id, section)
        if success:
            print(f"✓ 第 {i} 段上传成功")
        else:
            print(f"✗ 第 {i} 段上传失败")
    
    print("\n上传完成！")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='腾讯文档分段上传工具')
    parser.add_argument('--file-id', required=True, help='腾讯文档 file_id')
    parser.add_argument('--source-file', required=True, help='源文件路径')
    
    args = parser.parse_args()
    
    upload_to_tencent_docs(args.file_id, args.source_file)

if __name__ == "__main__":
    main()