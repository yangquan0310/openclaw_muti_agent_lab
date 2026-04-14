
#!/usr/bin/env python3
"""
修复AcademicSearchSummarizer.py中的bug
"""

file_path = "/root/.openclaw/skills/knowledge-manager/AcademicSearchSummarizer.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复bug: response = self.session.get(PAPER_URL, params=params)
# 改为: url = self.PAPER_URL.format(paper_id=paper_id)
#       response = self.session.get(url, params=params)

old_text = '''        params = {
            "fields": "abstract,venue,year,journal,volume,issue,pages,doi,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,authors"
        }
        
        try:
            response = self.session.get(PAPER_URL, params=params)'''

new_text = '''        url = self.PAPER_URL.format(paper_id=paper_id)
        params = {
            "fields": "abstract,venue,year,journal,volume,issue,pages,doi,referenceCount,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,authors"
        }
        
        try:
            response = self.session.get(url, params=params)'''

if old_text in content:
    content = content.replace(old_text, new_text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Bug修复成功！")
else:
    print("❌ 未找到目标文本，可能已经修复了")
    # 打印一下这部分内容看看
    lines = content.split('\n')
    for i, line in enumerate(lines[140:160]):
        print(f"{140+i}: {line}")
