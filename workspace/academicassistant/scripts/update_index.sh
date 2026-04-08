#!/bin/bash
# 索引更新定时任务
# 功能：每天凌晨3点更新脚本索引和项目库
# 位置：~/academicassistant/scripts/update_index.sh

# 获得当前时间
DATE=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$DATE] 开始执行索引更新定时任务..."

# 1. 更新脚本索引 - 扫描scripts目录，更新TOOLS.md中的脚本索引
echo "[$DATE] 更新脚本索引..."

# 获取脚本列表
SCRIPT_DIR="/root/.openclaw/workspace/academicassistant/scripts/"
SCRIPTS=$(find "$SCRIPT_DIR" -name "*.sh" -o -name "*.md" | sort)

# 2. 更新项目库 - 扫描项目目录，更新TOOLS.md中的项目库
echo "[$DATE] 更新项目库..."
PROJECT_DIR="/root/教研室仓库/项目文件/"
PROJECTS=$(find "$PROJECT_DIR" -maxdepth 1 -type d -name "????-??-??_*" | sort)

# 输出结果日志
echo "[$DATE] 发现项目:"
for proj in $PROJECTS; do
    proj_name=$(basename "$proj")
    echo "  - $proj_name"
done

echo "[$DATE] 索引更新完成。"
