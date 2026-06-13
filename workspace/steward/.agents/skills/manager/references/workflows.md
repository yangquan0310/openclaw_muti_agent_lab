# manager 核心工作流

> manager 技能的完整工作流程，涵盖任务管理、论文项目、课程项目、程序项目、知识库管理。

---

## 触发条件

当用户提到以下场景时触发：
- "推进任务"
- "完善TODO"
- "任务管理"
- "领取任务"
- "派任务"
- "分配任务"
- "通知"
- "整理项目"
- "管理项目"
- "创建新项目"
- "论文"
- "课程"
- "备课"
- "程序"
- "知识库"
- "wiki维护"

---

## 快速开始

- 领取任务 → 明确约束 → 更新TODO.md → 派发子代理 → 追踪进度 → 汇报老板
- 项目整理：检查现状 → 识别类型 → 确认需求 → 执行整理 → 验证结果 → 汇报用户

---

## 工作流速查

| 需求 | 对应工作流 | 对应文件名 |
|------|------|------|
| 给子代理派发任务 | 任务派发流程 | task-flow-guide.md |
| 论文项目整理 | 论文管理流程 | thesis-guide.md |
| 课程项目整理 | 课程管理流程 | course-guide.md |
| 程序项目整理 | 程序管理流程 | program-guide.md |
| 知识库维护 | 知识库管理 | knowledge-guide.md |
| 项目整理 | 整理工作流 | organize-workflow.md |
| 通用项目 | 通用项目管理 | project-guide.md |

---

## Q&A

### Q1：如何给子代理派发任务？

**4 步派发**（v3.0.1）：

1. **写 TODO.md**（7 字段：目标/约束/输入/产出，路径用绝对路径）
2. **建 workboard 卡**（`workboard_create({ ..., idempotencyKey: "..." })`，只到 backlog）
3. **IM 群里艾特代理**（**必须**，开头带 workboard 信息 + 双轨模版）
4. **代理自取 + 自动**：claim → spawn → running → done（Dx 全包）

**代理反馈**：通过 workboard（proof + comment），不走群消息
**大管家核验**：读文件 + workboard_comment + move to done + 更新 TODO

详见 [task-flow-guide.md](./task-flow-guide.md) v3.0.1

### Q2：如何新建一个项目？

1. 确定项目类型（论文/课程/程序/通用）
2. 创建标准目录结构
3. 填写四个契约文件（README.md、AGENTS.md、TODO.md、metadata.json）

### Q3：四个契约文件是什么？

- README.md（项目总览）
- AGENTS.md（操作手册）
- TODO.md（任务看板）
- metadata.json（机器可读配置）

这四个文件必须在项目根目录，不可移动。

---

## 错误排查

| 现象 | 可能原因 | 解决方法 |
|------|----------|----------|
| 子代理不清楚任务 | 约束说明不清晰 | 按模板明确约束/输入/产出 |
| 文件找不到 | 路径不正确 | 检查 metadata.json 中的路径 |
| 任务遗漏 | TODO.md 未更新 | 领取任务立即录入 TODO.md |

---

*详见 [索引](index.md)*
