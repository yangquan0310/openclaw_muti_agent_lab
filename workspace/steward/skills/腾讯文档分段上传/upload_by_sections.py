#!/usr/bin/env python3
"""
腾讯文档分段上传工具
将长文档切分成多个段落，逐段上传到腾讯文档智能文档

版本: 2.2.0
作者: 大管家
"""

import subprocess
import json
import sys
import os
from typing import List, Dict, Optional
from datetime import datetime


class TencentDocUploader:
    """腾讯文档分段上传器"""
    
    def __init__(self, file_id: str):
        """
        初始化上传器
        
        参数:
            file_id: 腾讯文档 file_id（必需）
        """
        self.file_id = file_id
    
    def run_mcporter(self, action: str, content: Optional[str] = None) -> bool:
        """调用 mcporter 执行操作"""
        args = {
            "file_id": self.file_id,
            "action": action
        }
        
        if content:
            args["content"] = content
        
        cmd = [
            "mcporter", "call", "tencent-docs", "smartcanvas.edit",
            "--args", json.dumps(args, ensure_ascii=False)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            return result.returncode == 0
        except Exception as e:
            print(f"  ✗ 执行失败: {e}")
            return False
    
    def split_into_sections(self, file_path: str) -> List[str]:
        """将文件切分成多个段落"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = []
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
    
    def upload(self, file: str) -> Dict:
        """
        上传文件到腾讯文档
        
        参数:
            file: 源文件路径
            
        返回:
            上传结果字典
        """
        result = {
            "success": False,
            "file_id": self.file_id,
            "file": file,
            "sections_count": 0,
            "uploaded_count": 0,
            "start_time": datetime.now().isoformat(),
            "end_time": None
        }
        
        try:
            print("正在切分段落...")
            sections = self.split_into_sections(file)
            result["sections_count"] = len(sections)
            print(f"共切分成 {len(sections)} 个段落")
            
            if not self.file_id:
                print("✗ 错误: 未提供 file_id")
                return result
            
            uploaded_count = 0
            
            # 跳过第一个标题（因为文档已创建）
            for i, section in enumerate(sections[1:], 2):
                print(f"正在上传第 {i}/{len(sections)} 段...")
                success = self.run_mcporter("INSERT_AFTER", section)
                if success:
                    print(f"✓ 第 {i} 段上传成功")
                    uploaded_count += 1
                else:
                    print(f"✗ 第 {i} 段上传失败")
            
            result["uploaded_count"] = uploaded_count
            result["success"] = uploaded_count == len(sections) - 1  # 减去跳过的第一段
            
        except Exception as e:
            print(f"✗ 上传过程出错: {e}")
            result["error"] = str(e)
        
        result["end_time"] = datetime.now().isoformat()
        return result


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='腾讯文档分段上传工具 v2.2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 upload_by_sections.py --file-id WRqFxRGmnIkj --file document.md
        """
    )
    
    # 必需参数
    parser.add_argument('--file-id', required=True, help='腾讯文档 file_id')
    parser.add_argument('--file', required=True, help='要上传的文档路径')
    
    args = parser.parse_args()
    
    # 创建上传器
    uploader = TencentDocUploader(file_id=args.file_id)
    
    # 显示信息
    print("=" * 60)
    print("腾讯文档分段上传工具 v2.2.0")
    print("=" * 60)
    print(f"文件 ID: {args.file_id}")
    print(f"文档: {args.file}")
    print("=" * 60)
    
    # 执行上传
    result = uploader.upload(args.file)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("上传完成")
    print("=" * 60)
    
    if result["success"]:
        print(f"✓ 成功: 上传了 {result['uploaded_count']}/{result['sections_count']} 个段落")
        sys.exit(0)
    else:
        print(f"✗ 失败: 仅上传了 {result['uploaded_count']}/{result['sections_count']} 个段落")
        if "error" in result:
            print(f"错误: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
