#!/usr/bin/env python3
"""
更新索引文件，添加Semantic Scholar验证信息
"""

import json
import os
from datetime import datetime

def load_json_file(filepath):
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(filepath, data):
    """保存JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_paper_with_verification(paper_data, verification_result):
    """使用验证结果更新论文数据"""
    paper_key = paper_data.get("key", "")
    
    # 检查是否是我们要更新的论文
    if verification_result.get("paper_key") != paper_key:
        return paper_data
    
    # 创建验证信息
    verification_info = {
        "verification_status": "semantic_scholar_verified" if verification_result.get("found") else "verification_failed",
        "verification_date": datetime.now().isoformat(),
        "verification_method": "semantic_scholar_api_search",
        "verification_confidence": verification_result.get("confidence", 0.0),
        "match_type": verification_result.get("match_type", "not_found"),
        "semantic_scholar_paper_id": None,
        "verification_evidence": []
    }
    
    # 如果验证成功，添加更多详细信息
    if verification_result.get("found"):
        semantic_data = verification_result.get("semantic_scholar_data")
        if semantic_data:
            verification_info["semantic_scholar_paper_id"] = semantic_data.get("paperId")
            
            # 更新DOI（如果找到）
            external_ids = semantic_data.get("externalIds", {})
            found_doi = external_ids.get("DOI")
            if found_doi:
                paper_data["doi"] = found_doi
                verification_info["verification_evidence"].append(f"通过Semantic Scholar找到DOI: {found_doi}")
            elif paper_data.get("doi"):
                verification_info["verification_evidence"].append(f"使用已有DOI但未匹配: {paper_data.get('doi')}")
            
            # 更新引用次数
            citation_count = semantic_data.get("citationCount")
            if citation_count is not None:
                paper_data["citations"] = citation_count
                verification_info["verification_evidence"].append(f"引用次数更新为: {citation_count}")
            
            # 添加URL
            url = semantic_data.get("url")
            if url:
                paper_data["semantic_scholar_url"] = url
            
            # 添加开放获取信息
            open_access_pdf = semantic_data.get("openAccessPdf", {})
            if open_access_pdf.get("url"):
                paper_data["open_access_pdf_url"] = open_access_pdf.get("url")
                paper_data["open_access_license"] = open_access_pdf.get("license")
            
            # 添加匹配信息
            title = semantic_data.get("title", "")
            year = semantic_data.get("year", "")
            venue = semantic_data.get("venue", "")
            verification_info["verification_evidence"].extend([
                f"匹配标题: {title}",
                f"匹配年份: {year}",
                f"匹配期刊: {venue}"
            ])
    
    # 如果验证失败
    else:
        verification_info["verification_evidence"].append("未在Semantic Scholar中找到匹配的论文")
        verification_info["verification_evidence"].append("可能原因: 1) API限流 2) 文献不在Semantic Scholar索引中 3) 标题/作者信息不准确")
    
    # 更新论文数据
    paper_data["verification_info"] = verification_info
    
    # 更新旧的验证状态（如果存在）
    if "verification_status" in paper_data:
        paper_data["previous_verification_status"] = paper_data.pop("verification_status")
    if "verification_date" in paper_data:
        paper_data["previous_verification_date"] = paper_data.pop("verification_date")
    if "verification_method" in paper_data:
        paper_data["previous_verification_method"] = paper_data.pop("verification_method")
    if "verification_confidence" in paper_data:
        paper_data["previous_verification_confidence"] = paper_data.pop("verification_confidence")
    
    return paper_data

def main():
    """主函数"""
    # 文件路径
    index_path = os.path.expanduser("~/实验室仓库/项目文件/2026-04-01_数字化存储与自传体记忆/知识库/索引/index.json")
    verification_report_path = os.path.expanduser("~/实验室仓库/项目文件/2026-04-01_数字化存储与自传体记忆/知识库/索引/semantic_scholar_verification_report.json")
    backup_index_path = index_path.replace(".json", "_backup_before_verification.json")
    
    print("开始更新索引文件...")
    print(f"索引文件: {index_path}")
    print(f"验证报告: {verification_report_path}")
    
    # 加载数据
    try:
        index_data = load_json_file(index_path)
        verification_data = load_json_file(verification_report_path)
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
        return
    
    # 创建备份
    print(f"创建备份: {backup_index_path}")
    save_json_file(backup_index_path, index_data)
    
    # 获取验证结果
    verification_results = verification_data.get("detailed_results", [])
    
    # 统计信息
    total_papers = len(index_data.get("papers", []))
    verified_papers = 0
    updated_papers = 0
    
    # 更新每篇论文
    papers = index_data.get("papers", [])
    for i, paper in enumerate(papers):
        paper_key = paper.get("key", "")
        
        # 查找对应的验证结果
        verification_result = None
        for result in verification_results:
            if result.get("paper_key") == paper_key:
                verification_result = result
                break
        
        if verification_result:
            # 更新论文数据
            updated_paper = update_paper_with_verification(paper, verification_result)
            papers[i] = updated_paper
            updated_papers += 1
            
            if verification_result.get("found"):
                verified_papers += 1
            
            print(f"✅ 更新论文: {paper_key}")
        else:
            print(f"⚠️  未找到验证结果: {paper_key}")
    
    # 更新索引元数据
    index_data["papers"] = papers
    
    # 添加验证历史记录
    verification_history = index_data.get("semantic_scholar_verification_history", [])
    verification_history.append({
        "verification_date": datetime.now().isoformat(),
        "verification_method": "automated_semantic_scholar_api_verification",
        "verification_summary": {
            "total_papers": total_papers,
            "verified_papers": verified_papers,
            "verification_rate": f"{(verified_papers/total_papers)*100:.1f}%" if total_papers > 0 else "0%",
            "updated_papers": updated_papers
        },
        "verification_report_path": "semantic_scholar_verification_report.json",
        "verification_summary_path": "semantic_scholar_verification_summary.md"
    })
    index_data["semantic_scholar_verification_history"] = verification_history
    
    # 更新最后验证日期
    index_data["last_semantic_scholar_verification"] = datetime.now().isoformat()
    
    # 保存更新后的索引文件
    save_json_file(index_path, index_data)
    
    print(f"\n✅ 更新完成!")
    print(f"  总论文数: {total_papers}")
    print(f"  验证成功: {verified_papers}")
    print(f"  更新论文: {updated_papers}")
    print(f"  验证成功率: {(verified_papers/total_papers)*100:.1f}%" if total_papers > 0 else "0%")
    print(f"\n备份文件: {backup_index_path}")
    print(f"验证报告: {verification_report_path}")

if __name__ == "__main__":
    main()