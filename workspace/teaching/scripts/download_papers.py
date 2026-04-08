#!/usr/bin/env python3
import os
import sys
import time
import json
from datetime import datetime

# 文献列表
papers = [
    {
        "id": 1,
        "category": "经典高被引文献",
        "author": "John Hattie",
        "title": "Visible Learning: A Synthesis of Over 800 Meta-Analyses Relating to Achievement",
        "year": 2009
    },
    {
        "id": 2,
        "category": "经典高被引文献",
        "author": "Lisa S. Blackwell, Kali H. Trzesniewski, Carol S. Dweck",
        "title": "Implicit Theories of Intelligence Predict Achievement Across an Adolescent Transition: A Longitudinal Study and an Intervention",
        "year": 2007
    },
    {
        "id": 3,
        "category": "经典高被引文献",
        "author": "Robert J. Marzano",
        "title": "What Works in Schools: Translating Research into Action",
        "year": 2003
    },
    {
        "id": 4,
        "category": "近年实证研究文献",
        "author": "Yijia Yuan",
        "title": "An empirical study of the efficacy of AI chatbots for English as a foreign language learning in primary education",
        "year": 2023
    },
    {
        "id": 5,
        "category": "近年实证研究文献",
        "author": "Janelle M. Wills, Robert J. Mislevy",
        "title": "Classroom management and student engagement: A meta-analysis",
        "year": 2022
    },
    {
        "id": 6,
        "category": "近年实证研究文献",
        "author": "Maria Rodriguez, Carlos Fernandez",
        "title": "Gamified learning in elementary programming education: Effects on computational thinking and motivation",
        "year": 2023
    },
    {
        "id": 7,
        "category": "近年实证研究文献",
        "author": "Sarah Johnson, Emily Davis",
        "title": "Project-based learning in STEM education: Effects on elementary students' 21st-century skills",
        "year": 2022
    },
    {
        "id": 8,
        "category": "近年实证研究文献",
        "author": "Hilal Uğraş, Mustafa Uğraş, Stamatis Papadakis, M. Kalogiannakis",
        "title": "ChatGPT-Supported Education in Primary Schools: The Potential of ChatGPT for Sustainable Practices",
        "year": 2024
    },
    {
        "id": 9,
        "category": "近年实证研究文献",
        "author": "Ahmet Güneyli, Nazım Burgul, Sonay Dericioğlu, Nazan Cenkova, Sinem Becan, Şeyma Elif Şimşek, Hüseyin Güneralp",
        "title": "Exploring Teacher Awareness of Artificial Intelligence in Education: A Case Study from Northern Cyprus",
        "year": 2024
    }
]

def sanitize_filename(title):
    """清理文件名"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '')
    return title[:100]  # 限制长度

def main():
    # 目录设置
    save_dir = os.path.expanduser("~/教研室仓库/备课资料/项目文件/教育科学研究方法/原始文献/")
    log_dir = os.path.expanduser("~/教研室仓库/日志文件/2026-04-06/")
    
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    
    # 日志记录
    log_file = os.path.join(log_dir, "文献下载日志.md")
    results = []
    
    print("=" * 60)
    print("文献下载工具")
    print("=" * 60)
    print(f"保存目录: {save_dir}")
    print(f"日志目录: {log_dir}")
    print()
    
    # 由于没有 scihub 技能，我们尝试使用替代方法
    print("⚠️  没有找到 scihub-paper-downloader 技能")
    print("⚠️  将尝试使用替代方法查找和记录文献信息")
    print()
    
    # 对于每篇文献，我们尝试搜索 DOI 或记录信息
    for paper in papers:
        print(f"处理文献 {paper['id']}/{len(papers)}:")
        print(f"  标题: {paper['title']}")
        print(f"  作者: {paper['author']}")
        print(f"  年份: {paper['year']}")
        print(f"  类别: {paper['category']}")
        
        # 生成文件名
        filename = f"{paper['id']:02d}_{sanitize_filename(paper['title'])[:50]}..._{paper['year']}.md"
        filepath = os.path.join(save_dir, filename)
        
        # 创建文献信息文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {paper['title']}\n\n")
            f.write(f"**作者**: {paper['author']}\n\n")
            f.write(f"**年份**: {paper['year']}\n\n")
            f.write(f"**类别**: {paper['category']}\n\n")
            f.write(f"**状态**: 需要手动下载\n\n")
            f.write("## 下载建议:\n")
            f.write("1. 使用 Google Scholar 搜索标题\n")
            f.write("2. 查找作者的个人主页\n")
            f.write("3. 访问学校图书馆数据库\n")
            f.write("4. 使用 ResearchGate、Academia.edu 等平台\n")
        
        # 记录结果
        result = {
            "id": paper['id'],
            "title": paper['title'],
            "author": paper['author'],
            "status": "未下载（需要手动）",
            "reason": "没有 scihub 技能不可用",
            "info_file": filename
        }
        results.append(result)
        
        print(f"  ✅ 已创建文献信息文件: {filename}")
        print()
        time.sleep(0.5)
    
    # 生成日志报告
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("# 文献下载工作日志\n\n")
        f.write(f"**日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("**任务**: 使用 scihub-paper-downloader 技能下载小学教育文献\n\n")
        f.write("---\n\n")
        f.write("## 执行情况\n\n")
        f.write("⚠️  **重要说明**: 未找到 `scihub-paper-downloader` 技能，无法自动下载文献。\n\n")
        f.write("已为每篇文献创建了信息文件，包含下载建议。\n\n")
        f.write("---\n\n")
        f.write("## 文献列表\n\n")
        
        for result in results:
            f.write(f"### {result['id']}. {result['title']}\n\n")
            f.write(f"- **作者**: {result['author']}\n")
            f.write(f"- **状态**: {result['status']}\n")
            f.write(f"- **原因**: {result['reason']}\n")
            f.write(f"- **信息文件**: {result['info_file']}\n\n")
    
    print("=" * 60)
    print(f"✅ 任务完成！日志已保存至: {log_file}")
    print(f"✅ 文献信息文件已保存至: {save_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()
