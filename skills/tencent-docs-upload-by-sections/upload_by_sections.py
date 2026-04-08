import subprocess
import json
import sys
import argparse
import os

def run_mcporter(file_id, content, action="INSERT_AFTER"):
    """调用 mcporter 上传一段内容"""
    args = {
        "file_id": file_id,
        "action": action,
        "content": content
    }
    
    cmd = [
        "mcporter", "call", "tencent-docs", "smartcanvas.edit",
        "--args", json.dumps(args, ensure_ascii=False)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result.returncode == 0, result.stdout, result.stderr

def split_into_sections(file_path, split_strategy="headers"):
    """将文件切分成多个段落
    
    Args:
        file_path: 源文件路径
        split_strategy: 切分策略
            - "headers": 按二级标题切分（## 开头）
            - "paragraphs": 按段落切分（空行分隔）
            - "lines": 按固定行数切分（每50行）
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = []
    
    if split_strategy == "headers":
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
    
    elif split_strategy == "paragraphs":
        # 按空行切分
        sections = content.split('\n\n')
        sections = [s.strip() for s in sections if s.strip()]
    
    elif split_strategy == "lines":
        # 按固定行数切分（每50行）
        lines = content.split('\n')
        for i in range(0, len(lines), 50):
            section = '\n'.join(lines[i:i+50])
            if section.strip():
                sections.append(section)
    
    return sections

def upload_sections(file_id, source_file, split_strategy="headers", skip_first=False, start_index=1):
    """分段上传文件到腾讯云文档
    
    Args:
        file_id: 腾讯云文档的file_id
        source_file: 源Markdown文件路径
        split_strategy: 切分策略（headers/paragraphs/lines）
        skip_first: 是否跳过第一个段落（文档已创建的情况）
        start_index: 起始段落索引（用于断点续传）
    """
    print("正在切分段落...")
    sections = split_into_sections(source_file, split_strategy)
    print(f"共切分成 {len(sections)} 个段落")
    
    # 确定要上传的段落范围
    start = 1 if skip_first else 0
    if start_index > 1:
        start = start_index - 1
    
    success_count = 0
    fail_count = 0
    failed_sections = []
    
    for i in range(start, len(sections)):
        section = sections[i]
        display_index = i + 1
        
        print(f"正在上传第 {display_index}/{len(sections)} 段...")
        success, stdout, stderr = run_mcporter(file_id, section)
        
        if success:
            print(f"✓ 第 {display_index} 段上传成功")
            success_count += 1
        else:
            print(f"✗ 第 {display_index} 段上传失败")
            fail_count += 1
            failed_sections.append({
                "index": display_index,
                "content": section,
                "stderr": stderr
            })
    
    # 打印总结
    print("\n" + "="*50)
    print(f"上传完成！")
    print(f"成功: {success_count}/{len(sections)-start}")
    print(f"失败: {fail_count}/{len(sections)-start}")
    print("="*50)
    
    if failed_sections:
        print(f"\n失败的段落: {[s['index'] for s in failed_sections]}")
        print("可使用 --start-index 参数重新上传失败的段落")
    
    # 生成结果文件
    result = {
        "file_id": file_id,
        "source_file": source_file,
        "total_sections": len(sections),
        "uploaded_sections": success_count,
        "failed_sections": fail_count,
        "failed_indices": [s['index'] for s in failed_sections]
    }
    
    result_file = f"/tmp/tencent_upload_result_{file_id}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {result_file}")
    
    return success_count == (len(sections) - start)

def main():
    parser = argparse.ArgumentParser(description='腾讯云文档分段上传工具')
    parser.add_argument('--file-id', required=True, help='腾讯云文档的file_id')
    parser.add_argument('--source-file', required=True, help='源Markdown文件路径')
    parser.add_argument('--split-strategy', default='headers', 
                       choices=['headers', 'paragraphs', 'lines'],
                       help='切分策略（默认: headers）')
    parser.add_argument('--skip-first', action='store_true',
                       help='跳过第一个段落（文档已创建的情况）')
    parser.add_argument('--start-index', type=int, default=1,
                       help='起始段落索引（用于断点续传，默认: 1）')
    
    args = parser.parse_args()
    
    # 验证文件存在
    if not os.path.exists(args.source_file):
        print(f"错误: 源文件不存在: {args.source_file}")
        sys.exit(1)
    
    # 执行上传
    success = upload_sections(
        file_id=args.file_id,
        source_file=args.source_file,
        split_strategy=args.split_strategy,
        skip_first=args.skip_first,
        start_index=args.start_index
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()