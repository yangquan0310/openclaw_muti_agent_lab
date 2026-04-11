import re

# 读取综述文件
with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的功能.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有可能的引用格式
# 1. DSAM_XXXX格式（包括括号内）
dsam_refs = re.findall(r'DSAM[_-]?\d+', content)
print(f"DSAM格式引用数量: {len(dsam_refs)}")
if dsam_refs:
    print(f"  唯一值: {set(dsam_refs)}")

# 2. 查找括号内的引用，如 (Author, Year)
parenthetical_refs = re.findall(r'\([A-Z][a-zA-Z\s&.,]+\d{4}[a-z]?\)', content)
print(f"\n括号内引用数量: {len(parenthetical_refs)}")
if len(parenthetical_refs) > 0:
    print(f"  前10个: {parenthetical_refs[:10]}")

# 3. 查找文本内引用，如 Author (Year)
narrative_refs = re.findall(r'[A-Z][a-z]+\s+et\s+al\.\s*\(\d{4}\)', content)
print(f"\net al.引用数量: {len(narrative_refs)}")
if len(narrative_refs) > 0:
    print(f"  前5个: {narrative_refs[:5]}")

# 4. 查找所有作者年份模式
all_refs = re.findall(r'[A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)?(?:\s+et\s+al\.)?\s*\(?\d{4}[a-z]?\)?', content)
print(f"\n所有作者年份模式数量: {len(all_refs)}")
if len(all_refs) > 0:
    print(f"  前10个: {all_refs[:10]}")

# 5. 查找是否有上标或脚注标记
superscript_refs = re.findall(r'\[\d+\]', content)
print(f"\n方括号数字引用数量: {len(superscript_refs)}")
if superscript_refs:
    print(f"  唯一值: {set(superscript_refs)}")
