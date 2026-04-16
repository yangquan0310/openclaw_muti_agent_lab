#!/bin/bash
# 每日仓库维护任务脚本
# 检查内容：
# 1. 仓库结构是否完整
# 2. 所有README.md是否完整
# 3. 所有文档是否已经记录
# 4. 笔记命名是否规范

WORKSPACE="/root/实验室仓库"
REPORT_FILE="/tmp/warehouse_maintenance_report_$(date +%Y%m%d_%H%M%S).md"

echo "# 仓库维护检查报告 $(date '+%Y-%m-%d %H:%M:%S')" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 1. 检查仓库结构完整性
echo "## 1. 仓库结构检查" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

REQUIRED_DIRS=("项目文件" "日志文件" "日程管理" "心跳报告")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$WORKSPACE/$dir" ]; then
        echo "- ✅ $dir/ 目录存在" >> "$REPORT_FILE"
    else
        echo "- ❌ $dir/ 目录缺失" >> "$REPORT_FILE"
    fi
done
echo "" >> "$REPORT_FILE"

# 2. 检查README.md
echo "## 2. README.md 检查" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

README_FILES=("$WORKSPACE/README.md" "$WORKSPACE/项目文件/README.md")
for readme in "${README_FILES[@]}"; do
    if [ -f "$readme" ]; then
        echo "- ✅ $(basename $(dirname $readme))/README.md 存在" >> "$REPORT_FILE"
    else
        echo "- ❌ $(basename $(dirname $readme))/README.md 缺失" >> "$REPORT_FILE"
    fi
done
echo "" >> "$REPORT_FILE"

# 3. 检查项目元数据
echo "## 3. 项目文档记录检查" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

PROJECT_DIR="$WORKSPACE/项目文件"
for project in "$PROJECT_DIR"/*; do
    if [ -d "$project" ]; then
        project_name=$(basename "$project")
        metadata_file="$project/元数据.json"
        
        if [ -f "$metadata_file" ]; then
            # 检查是否有未记录的本地文件
            unrecorded=0
            
            # 检查文档目录
            if [ -d "$project/文档" ]; then
                for file in "$project/文档"/*; do
                    if [ -f "$file" ]; then
                        filename=$(basename "$file")
                        if ! grep -q "$filename" "$metadata_file" 2>/dev/null; then
                            echo "  - ⚠️ 未记录文件: 文档/$filename" >> "$REPORT_FILE"
                            unrecorded=$((unrecorded + 1))
                        fi
                    fi
                done
            fi
            
            # 检查终稿目录
            if [ -d "$project/终稿" ]; then
                for file in "$project/终稿"/*.md; do
                    if [ -f "$file" ]; then
                        filename=$(basename "$file")
                        if ! grep -q "$filename" "$metadata_file" 2>/dev/null; then
                            echo "  - ⚠️ 未记录文件: 终稿/$filename" >> "$REPORT_FILE"
                            unrecorded=$((unrecorded + 1))
                        fi
                    fi
                done
            fi
            
            if [ $unrecorded -eq 0 ]; then
                echo "- ✅ $project_name: 所有文件已记录" >> "$REPORT_FILE"
            else
                echo "- ⚠️ $project_name: 发现 $unrecorded 个未记录文件" >> "$REPORT_FILE"
            fi
        else
            echo "- ❌ $project_name: 元数据.json 缺失" >> "$REPORT_FILE"
        fi
    fi
done
echo "" >> "$REPORT_FILE"

# 4. 检查笔记命名规范
echo "## 4. 笔记命名规范检查" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

for project in "$PROJECT_DIR"/*; do
    if [ -d "$project" ]; then
        project_name=$(basename "$project")
        notes_dir="$project/知识库/笔记"
        
        if [ -d "$notes_dir" ]; then
            for note in "$notes_dir"/*.json; do
                if [ -f "$note" ]; then
                    filename=$(basename "$note")
                    # 检查命名规范：应该使用中文或英文描述性名称
                    if [[ "$filename" =~ ^[0-9] ]]; then
                        echo "- ⚠️ $project_name/笔记/$filename: 不建议以数字开头" >> "$REPORT_FILE"
                    else
                        echo "- ✅ $project_name/笔记/$filename: 命名规范" >> "$REPORT_FILE"
                    fi
                fi
            done
        fi
    fi
done
echo "" >> "$REPORT_FILE"

# 输出报告
cat "$REPORT_FILE"

# 发送报告到当前channel（通过消息）
echo ""
echo "仓库维护检查完成，报告已生成: $REPORT_FILE"
