import re

# 读取综述文件
with open('/root/实验室仓库/项目文件/数字化存储与自传体记忆/知识库/综述/自传体记忆的功能.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有可能的引用格式
# 1. DSAM_XXXX格式
dsam_refs = re.findall(r'DSAM_\d+', content)
print(f"DSAM_XXXX格式引用数量: {len(dsam_refs)}")
if dsam_refs:
    print(f"  唯一值: {set(dsam_refs)}")

# 2. [DSAM_XXXX]格式
bracket_refs = re.findall(r'\[DSAM_\d+\]', content)
print(f"\n[DSAM_XXXX]格式引用数量: {len(bracket_refs)}")
if bracket_refs:
    print(f"  唯一值: {set(bracket_refs)}")

# 3. (作者, 年份)格式
apa_refs = re.findall(r'\([A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)?(?:\s+et\s+al\.)?,\s*\d{4}[a-z]?\)', content)
print(f"\nAPA格式引用数量: {len(apa_refs)}")
if len(apa_refs) > 0:
    print(f"  前10个: {apa_refs[:10]}")

# 4. 检查是否有其他格式，如脚注或上标
print("\n检查前1000字符内容:")
print(content[:1000])
