# 知识库同步指南

> 将规范、技能更新同步到 wiki

---

## 一、同步的本质

同步不是复制，而是**更新引用**。wiki 中的页面应该指向原始规范文件，而不是替代它。原始文件才是真相来源，wiki 只是索引。

---

## 二、同步时机

| 场景 | 是否同步 | 说明 |
|------|----------|------|
| 新增 SKILL 技能 | ✅ | 添加到 sources/ |
| 更新规范文档 | ✅ | 更新对应 wiki 页面 |
| 新增管理规范 | ✅ | 添加到 concepts/ |
| 项目结构变更 | ⚠️ | 只更新引用，不复制项目文件 |
| 临时文件 | ❌ | 不同步 |

---

## 三、同步操作

### 新增 SKILL 技能

```
来源：~/.openclaw/workspace/steward/skills/<skill-name>/
目标：~/.openclaw/wiki/sources/<skill-name>.md
```

操作：
1. 提取 HANDBOOK.md 核心内容
2. 保留引用路径指向原技能
3. 添加到 sources/index.md

### 更新规范文档

```
来源：~/.openclaw/workspace/steward/AGENTS.md
目标：~/.openclaw/wiki/concepts/agents.md
```

操作：
1. 同步关键规范变更
2. 更新版本历史
3. 保留引用指向原文件

### 新增管理规范

```
来源：skills/manager/references/<guide>.md
目标：~/.openclaw/wiki/concepts/<guide>.md
```

操作：
1. 判断是否需要升级为 wiki 页面
2. 如果是 AI 专用规范，保持在技能目录
3. 如果是人机共用规范，同步到 wiki

---

## 四、同步检查

同步后执行：

```bash
# 验证结构
openclaw wiki lint

# 验证链接
openclaw wiki status
```

---

## 五、禁止行为

| 禁止 | 原因 |
|------|------|
| 复制项目文件到 wiki | 项目文件应在仓库 |
| 同步临时文件 | wiki 是知识库，非存储库 |
| 创建重复页面 | 先检查是否已存在 |

---

## 六、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-05-19 | 初始版本 |

*最后更新：2026-05-22*
