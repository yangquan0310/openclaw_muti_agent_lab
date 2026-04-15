#!/bin/bash
# 数学家索引更新脚本 - 简化版
# 功能：更新TOOLS.md中的个人技能索引、个人脚本索引和项目库

# 配置
WORKSPACE_DIR="/root/.openclaw/workspace/mathematician"
TOOLS_FILE="${WORKSPACE_DIR}/TOOLS.md"
SKILLS_DIR="${WORKSPACE_DIR}/skills"
SCRIPTS_DIR="${WORKSPACE_DIR}/scripts"
PROJECTS_DIR="/root/实验室仓库/项目文件"

# 创建备份
cp "$TOOLS_FILE" "$TOOLS_FILE.bak.$(date +%Y%m%d%H%M%S)"

# --------------------------
# 1. 更新个人技能索引
# --------------------------
echo "更新个人技能索引..."

# 读取技能目录
declare -A SKILLS
for skill_dir in "$SKILLS_DIR"/*/; do
  if [ -d "$skill_dir" ]; then
    skill_name=$(basename "$skill_dir")
    if [ "$skill_name" = "update_indexes" ]; then
      trigger="更新索引、维护 TOOLS.md"
      desc="自动更新 TOOLS.md 中的脚本索引和项目库"
    else
      trigger="使用技能 ${skill_name}"
      desc="${skill_name} 技能"
    fi
    SKILLS["$skill_name"]="$trigger|$desc"
  fi
done

# 生成新的个人技能索引
NEW_PERSONAL_SKILLS="### 个人技能索引
> 大管家维护格式
> 内容由各代理独立维护
| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
"

for skill in $(printf "%s\n" "${!SKILLS[@]}" | sort); do
  IFS='|' read -r trigger desc <<< "${SKILLS[$skill]}"
  NEW_PERSONAL_SKILLS+="| $skill | $trigger | $desc | ~/.openclaw/workspace/mathematician/skills/$skill/SKILL.md |
"
done

# 替换TOOLS.md中的个人技能索引部分
PERSONAL_SKILLS_START=$(grep -n "### 个人技能索引" "$TOOLS_FILE" | head -n1 | cut -d: -f1)
PERSONAL_SKILLS_END=$(grep -n "---" "$TOOLS_FILE" | awk -v start="$PERSONAL_SKILLS_START" 'NR > start {print NR; exit}')
if [ -z "$PERSONAL_SKILLS_END" ]; then
  PERSONAL_SKILLS_END=$(grep -n "### 个人脚本索引" "$TOOLS_FILE" | head -n1 | cut -d: -f1)
  PERSONAL_SKILLS_END=$((PERSONAL_SKILLS_END - 1))
fi

head -n $((PERSONAL_SKILLS_START - 1)) "$TOOLS_FILE" > "$TOOLS_FILE.tmp"
echo "$NEW_PERSONAL_SKILLS" >> "$TOOLS_FILE.tmp"
tail -n +$((PERSONAL_SKILLS_END + 1)) "$TOOLS_FILE" >> "$TOOLS_FILE.tmp"
mv "$TOOLS_FILE.tmp" "$TOOLS_FILE"

# --------------------------
# 2. 更新个人脚本索引
# --------------------------
echo "更新个人脚本索引..."

# 读取脚本目录
declare -A SCRIPTS
if [ -d "$SCRIPTS_DIR" ]; then
  for script_file in "$SCRIPTS_DIR"/*.md; do
    if [ -f "$script_file" ]; then
      script_name=$(basename "$script_file" .md)
      trigger="使用脚本 ${script_name}"
      desc="${script_name} 脚本"
      SCRIPTS["$script_name"]="$trigger|$desc"
    fi
  done
fi

# 生成新的个人脚本索引
NEW_PERSONAL_SCRIPTS="### 个人脚本索引
> 各个代理独立维护，这里显示数学家特有脚本

| 脚本名称 | 触发示例 | 描述 | 路径 |
|----------|----------|----------|------|
"

for script in $(printf "%s\n" "${!SCRIPTS[@]}" | sort); do
  IFS='|' read -r trigger desc <<< "${SCRIPTS[$script]}"
  NEW_PERSONAL_SCRIPTS+="| $script | $trigger | $desc | ~/.openclaw/workspace/mathematician/scripts/$script.md |
"
done

# 替换TOOLS.md中的个人脚本索引部分
PERSONAL_SCRIPTS_START=$(grep -n "### 个人脚本索引" "$TOOLS_FILE" | head -n1 | cut -d: -f1)
PERSONAL_SCRIPTS_END=$(grep -n "---" "$TOOLS_FILE" | awk -v start="$PERSONAL_SCRIPTS_START" 'NR > start {print NR; exit}')
if [ -z "$PERSONAL_SCRIPTS_END" ]; then
  PERSONAL_SCRIPTS_END=$(grep -n "## 索引" "$TOOLS_FILE" | head -n1 | cut -d: -f1)
  PERSONAL_SCRIPTS_END=$((PERSONAL_SCRIPTS_END - 1))
fi

head -n $((PERSONAL_SCRIPTS_START - 1)) "$TOOLS_FILE" > "$TOOLS_FILE.tmp"
echo "$NEW_PERSONAL_SCRIPTS" >> "$TOOLS_FILE.tmp"
tail -n +$((PERSONAL_SCRIPTS_END + 1)) "$TOOLS_FILE" >> "$TOOLS_FILE.tmp"
mv "$TOOLS_FILE.tmp" "$TOOLS_FILE"

# --------------------------
# 3. 更新项目库
# --------------------------
echo "更新项目库..."

# 读取项目目录
declare -A PROJECTS
for project_dir in "$PROJECTS_DIR"/*/; do
  if [ -d "$project_dir" ]; then
    project_name=$(basename "$project_dir")
    description="$project_name"
    if [ -f "$project_dir/README.md" ]; then
      description=$(grep -m1 "^#" "$project_dir/README.md" | cut -d# -f2- | sed 's/^ *//')
      if [ -z "$description" ]; then
        description="$project_name"
      fi
    fi
    PROJECTS["$project_name"]="$description"
  fi
done

# 生成新的项目库
NEW_PROJECTS="### 项目库
> 大管家维护格式
> 内容由各代理独立维护
| 项目名 | 存储位置 | 描述 |
|--------|----------|------|
"

for project in $(printf "%s\n" "${!PROJECTS[@]}" | sort); do
  NEW_PROJECTS+="| $project | ~/实验室仓库/项目文件/$project/ | ${PROJECTS[$project]} |
"
done

# 替换TOOLS.md中的项目库部分
PROJECTS_START=$(grep -n "### 项目库" "$TOOLS_FILE" | head -n1 | cut -d: -f1)
PROJECTS_END=$(grep -n "---" "$TOOLS_FILE" | awk -v start="$PROJECTS_START" 'NR > start {print NR; exit}')
if [ -z "$PROJECTS_END" ]; then
  PROJECTS_END=$(grep -n "## 索引" "$TOOLS_FILE" | head -n1 | cut -d: -f1)
  PROJECTS_END=$((PROJECTS_END - 1))
fi

head -n $((PROJECTS_START - 1)) "$TOOLS_FILE" > "$TOOLS_FILE.tmp"
echo "$NEW_PROJECTS" >> "$TOOLS_FILE.tmp"
tail -n +$((PROJECTS_END + 1)) "$TOOLS_FILE" >> "$TOOLS_FILE.tmp"
mv "$TOOLS_FILE.tmp" "$TOOLS_FILE"

echo "TOOLS.md 更新完成！"
echo "技能数量: ${#SKILLS[@]}"
echo "脚本数量: ${#SCRIPTS[@]}"
echo "项目数量: ${#PROJECTS[@]}"
