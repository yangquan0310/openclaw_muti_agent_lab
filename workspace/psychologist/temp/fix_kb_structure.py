
#!/usr/bin/env python3
"""
知识库结构修复脚本
修复字段顺序和删除额外字段
"""

import json
import os
import shutil
from datetime import datetime

# 预期字段顺序（按知识库结构.md）
EXPECTED_FIELD_ORDER = [
    "id",
    "paperId",
    "authors",
    "year",
    "title",
    "venue",
    "volume",
    "issue",
    "pages",
    "doi",
    "url",
    "abstract",
    "topic",
    "citationCount",
    "labels",
    "notes"
]

# 知识库路径
KB_PATHS = {
    "学生论文修改": "/root/实验室仓库/项目文件/学生论文修改/知识库/index.json",
    "数字化存储与自传体记忆": "/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/index.json",
    "跨期选择的年龄差异": "/root/实验室仓库/项目文件/跨期选择的年龄差异/知识库/index.json"
}

def backup_kb(kb_path, kb_name):
    """备份知识库"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{kb_path}.backup_{timestamp}"
    shutil.copy2(kb_path, backup_path)
    print(f"  ✅ 已备份到: {backup_path}")
    return backup_path

def fix_student_paper_modification(kb_path):
    """修复学生论文修改知识库：删除额外字段"""
    print(f"\n{'='*80}")
    print(f"修复知识库: 学生论文修改")
    print(f"{'='*80}")
    
    # 备份
    backup_path = backup_kb(kb_path, "学生论文修改")
    
    # 读取
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    papers = kb["papers"]
    print(f"\n📋 开始处理 {len(papers)} 篇文献...")
    
    extra_fields_removed = 0
    
    for i, paper in enumerate(papers):
        # 删除额外字段
        if "_topic" in paper:
            del paper["_topic"]
            extra_fields_removed += 1
        if "_round" in paper:
            del paper["_round"]
            extra_fields_removed += 1
        
        # 重排字段顺序（虽然已经是对的，但确保一下）
        papers[i] = {k: paper.get(k, "") for k in EXPECTED_FIELD_ORDER if k in paper}
    
    print(f"  ✅ 删除了 {extra_fields_removed} 个额外字段")
    
    # 更新updated_at
    kb["updated_at"] = datetime.now().isoformat()
    
    # 保存
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 保存成功！")
    return True

def fix_field_order(kb_path, kb_name):
    """修复字段顺序"""
    print(f"\n{'='*80}")
    print(f"修复知识库: {kb_name}")
    print(f"{'='*80}")
    
    # 备份
    backup_path = backup_kb(kb_path, kb_name)
    
    # 读取
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    papers = kb["papers"]
    print(f"\n📋 开始处理 {len(papers)} 篇文献...")
    
    for i, paper in enumerate(papers):
        # 重排字段顺序，缺失的字段留空
        new_paper = {}
        for field in EXPECTED_FIELD_ORDER:
            if field in paper:
                new_paper[field] = paper[field]
            else:
                # 缺失的字段留空字符串或默认值
                if field in ["volume", "issue", "pages", "doi"]:
                    new_paper[field] = ""
                elif field in ["citationCount"]:
                    new_paper[field] = paper.get("citationCount", 0)
                elif field in ["labels"]:
                    new_paper[field] = paper.get("labels", {})
                elif field in ["notes"]:
                    new_paper[field] = paper.get("notes", {})
        
        papers[i] = new_paper
    
    print(f"  ✅ 字段顺序已重排！")
    
    # 更新updated_at
    kb["updated_at"] = datetime.now().isoformat()
    
    # 保存
    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 保存成功！")
    return True

def main():
    """主函数"""
    print("="*80)
    print("知识库结构修复工具")
    print("="*80)
    
    # 1. 学生论文修改：删除额外字段
    fix_student_paper_modification(KB_PATHS["学生论文修改"])
    
    # 2. 数字化存储与自传体记忆：重排字段顺序
    fix_field_order(KB_PATHS["数字化存储与自传体记忆"], "数字化存储与自传体记忆")
    
    # 3. 跨期选择的年龄差异：重排字段顺序
    fix_field_order(KB_PATHS["跨期选择的年龄差异"], "跨期选择的年龄差异")
    
    print(f"\n{'='*80}")
    print("修复完成！")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
