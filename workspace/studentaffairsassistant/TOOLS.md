> 配置档案
> 大管家按要求对公共内容进行维护
> 私有内容各代理独自维护

---

## 存储位置

### 公共存储位置
> 条目由大管家统一维护
> 实验室仓库、实验室项目等实验室相关内容同步给实验室成员
> 教研室仓库、教学助手仓库、教务助手仓库、学工助手仓库等教研室相关内容同步给教研室成员
| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| 技能文件夹 | ~/.openclaw/workspace/skills/README.md | 存放了所有技能文件（公共技能） |
| API密钥存储 | ~/.openclaw/.env | 安全存储所有API密钥 |
| 实验室仓库 | ~/实验室仓库/README.md | 实验室仓库 |
| 教研室仓库 | ~/教研室仓库/README.md | 教学研究、教务管理和学生工作相关文件存储 |

### 私人存储位置

| 文件 | 存储路径 | 说明 |
|----------|----------|------|
| Agent 个人记忆 | ~/.openclaw/workspace/studentaffairsassistant/MEMORY.md | 学工助手独立维护 |
| Agent 个人技能 | ~/.openclaw/workspace/studentaffairsassistant/skills/README.md | 学工助手专属技能存储目录 |
| Agent 临时文件 | ~/.openclaw/workspace/studentaffairsassistant/temp/README.md | 学工助手专属临时文件存储目录 |
| Agent 工作日志 | ~/.openclaw/workspace/studentaffairsassistant/memory/README.md | 任务执行记录 |
| 学工助手仓库 |	~/教研室仓库/学生工作/README.MD	|学工助手用来进行工作的文件夹、其他成员不可以写入，只能读取|
| 学工助手项目 |	~/教研室仓库/学生工作/项目文件/README.MD	|学工助手用来存储项目的文件夹、其他成员不可以写入，只能读取|
---

## 教研室仓库结构
> 只同步给教学助手、教务助手和学工助手
```
~/教研室仓库/
├── 主任信息/                   # 教研室主任个人信息和学术资料
├── 备课资料/                   # 课程准备材料
├── 学生工作/                   # 学生管理和辅导
├── 教务归档/                   # 教学教务文件归档
└── 日程文件/                   # 教学日程安排
```

## 项目

### 项目结构
> 学工项结构目索引详见 ~/教研室仓库/学生工作/项目文件/README.md

### 项目库
> 学工项结构目索引详见 ~/教研室仓库/学生工作/项目文件/README.md


---

## 技能索引

### 公共技能索引
> 完整列表见: `/root/.openclaw/workspace/skills/README.md`

---

### 个人技能索引
> 完整列表见: `/root/.openclaw/workspace/studentaffairsassistant/skills/README.md`

| 技能名称 | 触发示例 | 描述 | 路径 |
|---------|---------|------|------|
| *暂无个人技能* | - | - | - |
---

*最后重构: 2026-04-19 10:30 (按工作流1六阶段规范更新每日自我更新脚本)*
*重构者: 学工助手*