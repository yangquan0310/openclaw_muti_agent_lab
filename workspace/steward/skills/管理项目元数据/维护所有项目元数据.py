#!/usr/bin/env python3
import os
import json
from datetime import datetime

PROJECTS_DIR = "/root/实验室仓库/项目文件"

def get_project_directories(project_path):
    """获取项目目录结构"""
    dirs = {}
    possible_dirs = ["文档", "草稿", "终稿", "知识库", "模板", "审稿意见"]
    
    for dir_name in possible_dirs:
        dir_path = os.path.join(project_path, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            dirs[dir_name] = f"{dir_name}/"
    
    return dirs

def get_project_documents(project_path):
    """获取项目文档列表"""
    documents = []
    
    # 检查文档目录
    doc_dir = os.path.join(project_path, "文档")
    if os.path.exists(doc_dir):
        for filename in os.listdir(doc_dir):
            if filename.endswith(('.md', '.docx', '.pdf', '.txt')):
                documents.append({
                    "title": os.path.splitext(filename)[0],
                    "version": "v1",
                    "path": f"文档/{filename}",
                    "type": "user_uploaded"
                })
    
    # 检查终稿目录
    final_dir = os.path.join(project_path, "终稿")
    if os.path.exists(final_dir):
        for filename in os.listdir(final_dir):
            if filename.endswith(('.md', '.docx', '.pdf', '.txt')):
                documents.append({
                    "title": os.path.splitext(filename)[0],
                    "version": "v1",
                    "path": f"终稿/{filename}",
                    "type": "agent_written"
                })
    
    return documents

def update_project_metadata(project_name):
    """更新单个项目的元数据"""
    project_path = os.path.join(PROJECTS_DIR, project_name)
    metadata_path = os.path.join(project_path, "元数据.json")
    
    # 检查项目路径是否存在
    if not os.path.exists(project_path):
        print(f"❌ 项目不存在: {project_name}")
        return False
    
    # 确保标准目录存在
    for dir_name in ["文档", "草稿", "终稿", "知识库"]:
        dir_path = os.path.join(project_path, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"  创建目录: {dir_name}")
    
    # 读取现有元数据或创建新的
    existing_metadata = {}
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                existing_metadata = json.load(f)
        except Exception as e:
            print(f"  ⚠️  读取现有元数据失败: {e}")
    
    # 创建新的元数据
    current_time = datetime.now().isoformat()
    created_date = existing_metadata.get("created_date", datetime.now().strftime("%Y-%m-%d"))
    
    metadata = {
        "project_id": project_name,
        "title": project_name,
        "created_date": created_date,
        "status": "active",
        "version": existing_metadata.get("version", "v1"),
        "description": existing_metadata.get("description", f"{project_name}项目"),
        "directories": get_project_directories(project_path),
        "documents": get_project_documents(project_path),
        "tags": existing_metadata.get("tags", []),
        "cloud_doc_mappings": existing_metadata.get("cloud_doc_mappings", {})
    }
    
    # 保存元数据
    try:
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        os.chmod(metadata_path, 0o644)
        print(f"✅ 更新元数据: {project_name}")
        return True
    except Exception as e:
        print(f"❌ 保存元数据失败: {project_name}, 错误: {e}")
        return False

def main():
    """主函数：维护所有项目的元数据"""
    print("=" * 60)
    print("开始维护所有项目的元数据")
    print("=" * 60)
    
    # 获取所有项目
    projects = []
    for item in os.listdir(PROJECTS_DIR):
        item_path = os.path.join(PROJECTS_DIR, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            projects.append(item)
    
    projects.sort()
    print(f"找到 {len(projects)} 个项目\n")
    
    # 逐个更新元数据
    success_count = 0
    for project in projects:
        if update_project_metadata(project):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"元数据维护完成：{success_count}/{len(projects)} 个项目成功更新")
    print("=" * 60)

if __name__ == "__main__":
    main()
