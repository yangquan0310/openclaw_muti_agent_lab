
#!/usr/bin/env python3
"""
修改_fetch_paper_details方法，用点号请求子字段
"""

file_path = "/root/.openclaw/skills/knowledge-manager/AcademicSearchSummarizer.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_text = '''        url = self.PAPER_URL.format(paper_id=paper_id)
        params = {
            "fields": "paperId,title,abstract,venue,year,journal,publicationVenue,citationCount,authors,externalIds"
        }'''

new_text = '''        url = self.PAPER_URL.format(paper_id=paper_id)
        params = {
            "fields": "paperId,title,abstract,venue,year,journal.name,journal.volume,journal.pages,publicationVenue,citationCount,authors,externalIds.DOI"
        }'''

if old_text in content:
    content = content.replace(old_text, new_text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 字段请求修改成功！")
else:
    print("❌ 未找到目标文本")
