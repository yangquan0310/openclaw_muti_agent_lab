import json
import re

# 读取笔记文件
with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/笔记/自传体记忆的功能.json', 'r', encoding='utf-8') as f:
    notes = json.load(f)

# 读取综述文件
with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的功能.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 建立文献ID到APA引用的映射
citation_map = {}

for note_id, note_data in notes['notes'].items():
    paper = note_data['paper']
    authors = paper.get('authors', '')
    year = paper.get('year', '')
    
    # 处理作者格式
    if authors:
        # 分割作者
        author_list = [a.strip() for a in authors.split(',')]
        
        # 格式化APA作者
        if len(author_list) == 1:
            # 单个作者：姓氏
            apa_author = author_list[0].split()[-1]
        elif len(author_list) == 2:
            # 两个作者：姓氏 & 姓氏
            apa_author = f"{author_list[0].split()[-1]} & {author_list[1].split()[-1]}"
        elif len(author_list) >= 3:
            # 三个或更多作者：姓氏 et al.
            apa_author = f"{author_list[0].split()[-1]} et al."
        else:
            apa_author = "Unknown"
    else:
        apa_author = "Unknown"
    
    # 格式化APA引用
    if year:
        apa_citation = f"({apa_author}, {year})"
    else:
        apa_citation = f"({apa_author}, n.d.)"
    
    citation_map[note_id] = apa_citation

# 查找综述中所有的DSAM引用
dsam_refs = re.findall(r'DSAM_\d+', content)
unique_refs = sorted(set(dsam_refs))

print(f"综述中使用的DSAM引用数量: {len(dsam_refs)}")
print(f"唯一DSAM引用数量: {len(unique_refs)}")
print("\n使用的DSAM引用列表:")
for ref in unique_refs:
    apa = citation_map.get(ref, "未找到")
    print(f"  {ref} -> {apa}")

# 检查是否有缺失的引用
missing_refs = [ref for ref in unique_refs if ref not in citation_map]
if missing_refs:
    print(f"\n警告: 以下引用在笔记文件中未找到:")
    for ref in missing_refs:
        print(f"  {ref}")
