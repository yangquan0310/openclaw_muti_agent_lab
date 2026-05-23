# 知识库管理指南

> 管理 OpenClaw wiki 知识库，定期维护结构、更新内容、清理冗余。

---

## 一、知识库的本质

知识库是实验室的**长期记忆**，不是项目文件的副本仓库。

Wiki 中只存放需要长期保留的知识：规范、标准、流程、人物、系统。项目的完整文件应该留在仓库中，Wiki 只保留引用和摘要。

---

## 二、知识库结构

```
~/.openclaw/wiki/
├── concepts/     → 规范、标准、流程（AI 决策参考）
├── entities/     → 人物、系统、项目（AI 路由参考）
├── syntheses/    → 跨项目总结、经验提炼
├── sources/      → 工具/平台级文档（conda、openclaw-env等）
├── reports/      → 生成的仪表盘（按需）
└── _attachments/ → 附件
```

| 目录 | 内容 | 示例 |
|------|------|------|
| concepts | 规范/标准/流程 | project.md、thesis-project.md |
| entities | 人物/系统/项目 | steward.md、openclaw-gateway.md |
| syntheses | 跨项目总结 | 多agent协作案例 |
| sources | 工具/平台文档 | conda.md、openclaw-env.md |

---

## 三、管理原则

### 层级分明

每个目录有明确的职责边界。concepts/ 不放实体，entities/ 不放规范。

### 禁止重复

项目文件只存在一个地方：Wiki 放规范引用/摘要，仓库放完整项目文件。

### 定期维护

| 频率 | 操作 |
|------|------|
| 每月 | 检查 sources/ 冗余、清理无用页面 |
| 每季度 | 更新过时信息、补充新规范 |
| 按需 | wiki lint 检查结构问题 |

---

## 四、日常操作

```bash
# 检查 wiki 状态
openclaw wiki status

# 搜索内容
openclaw wiki search "关键词"

# 读取页面
openclaw wiki get concepts/project.md

# 结构检查
openclaw wiki lint
```

### 清理操作

| 操作 | 场景 |
|------|------|
| 删除冗余 sources | 项目文档误入 wiki |
| 归档过期页面 | 已完成项目无需 wiki 引用 |
| 更新过时内容 | 规范变更后同步 wiki |

### 同步操作

| 操作 | 场景 |
|------|------|
| 新建规范 | 新增 SKILL/TODO 模板后 |
| 更新引用 | 项目路径/名称变更 |
| 同步版本 | 技能版本更新后 |

---

## 五、检查清单

### 每月检查

- [ ] sources/ 是否有冗余的项目文件
- [ ] concepts/ 规范是否与实际 SKILL 同步
- [ ] entities/ 是否有未维护的过期信息
- [ ] reports/ 是否有过期仪表盘

### 按需检查

- [ ] wiki lint 有无错误
- [ ] 新规范是否已添加到 wiki
- [ ] 过期项目是否已归档

---

## 六、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-05-19 | 初始版本 |

*最后更新：2026-05-22*
