
#!/usr/bin/env python3
"""
修改字段提取逻辑，直接取journal.volume等
"""

file_path = "/root/.openclaw/skills/knowledge-manager/AcademicSearchSummarizer.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_extraction = '''            # 提取需要的字段
            result = {}
            
            # 基础字段
            if data.get("abstract"):
                result["abstract"] = data["abstract"]
            if data.get("venue"):
                result["venue"] = data["venue"]
            if data.get("year"):
                result["year"] = data["year"]
            if data.get("citationCount") is not None:
                result["citationCount"] = data["citationCount"]
            
            # 从journal对象中提取元数据（根据老板给的API响应格式）
            if data.get("journal"):
                journal = data["journal"]
                
                # 期刊名
                if journal.get("name"):
                    result["journal_name"] = journal["name"].strip()
                
                # 卷号 - 清理格式（去掉多余空格）
                if journal.get("volume"):
                    vol = journal["volume"].strip()
                    # 如果格式是 "107 2"，只取第一部分
                    if " " in vol:
                        vol = vol.split()[0]
                    result["volume"] = vol
                
                # 页码 - 清理格式（去掉多余换行和空格）
                if journal.get("pages"):
                    pages = journal["pages"].strip()
                    # 清理多余空白字符
                    pages = " ".join(pages.split())
                    result["pages"] = pages
            
            # 从externalIds中提取DOI（如果有的话）
            if data.get("externalIds"):
                external_ids = data["externalIds"]
                if external_ids.get("DOI"):
                    result["doi"] = external_ids["DOI"]'''

new_extraction = '''            # 提取需要的字段（根据老板给的API文档，用点号请求子字段）
            result = {}
            
            # 基础字段
            if data.get("abstract"):
                result["abstract"] = data["abstract"]
            if data.get("venue"):
                result["venue"] = data["venue"]
            if data.get("year"):
                result["year"] = data["year"]
            if data.get("citationCount") is not None:
                result["citationCount"] = data["citationCount"]
            
            # 直接取journal.name, journal.volume, journal.pages
            if data.get("journal.name"):
                result["journal_name"] = data["journal.name"].strip()
            if data.get("journal.volume"):
                vol = data["journal.volume"].strip()
                if " " in vol:
                    vol = vol.split()[0]
                result["volume"] = vol
            if data.get("journal.pages"):
                pages = data["journal.pages"].strip()
                pages = " ".join(pages.split())
                result["pages"] = pages
            
            # 直接取externalIds.DOI
            if data.get("externalIds.DOI"):
                result["doi"] = data["externalIds.DOI"]'''

if old_extraction in content:
    content = content.replace(old_extraction, new_extraction)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 字段提取逻辑修改成功！")
else:
    print("❌ 未找到目标文本，让我检查一下当前内容...")
    # 找到这部分并打印
    lines = content.split('\n')
    start = None
    for i, line in enumerate(lines):
        if '提取需要的字段' in line:
            start = i
            break
    if start is not None:
        print("\n当前提取逻辑:")
        for line in lines[start:start+50]:
            print(line)
