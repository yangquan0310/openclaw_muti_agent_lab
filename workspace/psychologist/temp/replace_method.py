
#!/usr/bin/env python3
"""
替换整个_fetch_paper_details方法
"""

file_path = "/root/.openclaw/skills/knowledge-manager/AcademicSearchSummarizer.py"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到方法开始和结束的行号
start_line = None
end_line = None

for i, line in enumerate(lines):
    if 'def _fetch_paper_details' in line:
        start_line = i
    if start_line is not None and 'def fetch_full_metadata' in line:
        end_line = i - 1  # 前一行是_fetch_paper_details的结束
        break

print(f"方法开始于行: {start_line}")
print(f"方法结束于行: {end_line}")

# 新的方法内容
new_method_lines = [
    '    def _fetch_paper_details(self, paper_id: str) -&gt; Optional[Dict[str, Any]]:\n',
    '        """\n',
    '        获取文献的完整元数据\n',
    '        \n',
    '        Args:\n',
    '            paper_id: Semantic Scholar paper ID\n',
    '            \n',
    '        Returns:\n',
    '            包含完整信息的字典，如果获取失败则返回 None\n',
    '        """\n',
    '        url = self.PAPER_URL.format(paper_id=paper_id)\n',
    '        params = {\n',
    '            "fields": "paperId,title,abstract,venue,year,journal,publicationVenue,citationCount,authors,externalIds"\n',
    '        }\n',
    '        \n',
    '        try:\n',
    '            response = self.session.get(url, params=params)\n',
    '            response.raise_for_status()\n',
    '            data = response.json()\n',
    '            \n',
    '            # 提取需要的字段\n',
    '            result = {}\n',
    '            \n',
    '            # 基础字段\n',
    '            if data.get("abstract"):\n',
    '                result["abstract"] = data["abstract"]\n',
    '            if data.get("venue"):\n',
    '                result["venue"] = data["venue"]\n',
    '            if data.get("year"):\n',
    '                result["year"] = data["year"]\n',
    '            if data.get("citationCount") is not None:\n',
    '                result["citationCount"] = data["citationCount"]\n',
    '            \n',
    '            # 从journal对象中提取元数据（根据老板给的API响应格式）\n',
    '            if data.get("journal"):\n',
    '                journal = data["journal"]\n',
    '                \n',
    '                # 期刊名\n',
    '                if journal.get("name"):\n',
    '                    result["journal_name"] = journal["name"].strip()\n',
    '                \n',
    '                # 卷号 - 清理格式（去掉多余空格）\n',
    '                if journal.get("volume"):\n',
    '                    vol = journal["volume"].strip()\n',
    '                    # 如果格式是 "107 2"，只取第一部分\n',
    '                    if " " in vol:\n',
    '                        vol = vol.split()[0]\n',
    '                    result["volume"] = vol\n',
    '                \n',
    '                # 页码 - 清理格式（去掉多余换行和空格）\n',
    '                if journal.get("pages"):\n',
    '                    pages = journal["pages"].strip()\n',
    '                    # 清理多余空白字符\n',
    '                    pages = " ".join(pages.split())\n',
    '                    result["pages"] = pages\n',
    '            \n',
    '            # 从externalIds中提取DOI（如果有的话）\n',
    '            if data.get("externalIds"):\n',
    '                external_ids = data["externalIds"]\n',
    '                if external_ids.get("DOI"):\n',
    '                    result["doi"] = external_ids["DOI"]\n',
    '            \n',
    '            return result if result else None\n',
    '            \n',
    '        except requests.RequestException as e:\n',
    '            # 静默失败，不影响主流程\n',
    '            return None\n',
    '\n'
]

# 替换
new_lines = lines[:start_line] + new_method_lines + lines[end_line:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ _fetch_paper_details方法替换成功！")
