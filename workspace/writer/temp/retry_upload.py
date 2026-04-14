
import subprocess
import json

def upload_section(file_id, content):
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
    return result.returncode == 0, result.stdout, result.stderr

# 读取文件
with open('/root/实验室仓库/项目文件/跨期选择的年龄差异/知识库/文献综述/文献综述_跨期选择的年龄差异.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 按主要章节分割
sections = content.split('\n## ')

file_id = "WSsmBtvdyiVd"

# 从第6段开始重新上传（索引5开始，因为0是标题，1-5已成功）
for i in range(6, len(sections)):
    section_content = "## " + sections[i] if i > 0 else sections[i]
    print(f"上传第 {i+1}/{len(sections)} 段...")
    success, stdout, stderr = upload_section(file_id, section_content)
    if success:
        print(f"✓ 第 {i+1} 段上传成功")
    else:
        print(f"✗ 第 {i+1} 段上传失败: {stderr}")

print("\n重试完成！")
