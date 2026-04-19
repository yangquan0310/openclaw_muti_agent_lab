# 全代理定时任务与工作记忆一致性检查计划
**执行时间**：2026-04-09 15:32 (Asia/Shanghai)
**检查范围**：所有8个代理
**检查目标**：验证每个代理的定时任务表与工作记忆中子代理追踪表的一致性
---
## 检查标准
| 检查项 | 要求 |
|--------|------|
| 1. 定时任务表 | 是否添加了「子代理ID」列 |
| 2. 子代理ID命名 | 是否符合规范：`agent:<agentId>:cron:<taskId>` |
| 3. 工作记忆 | 子代理是否已添加到活跃子代理清单 |
| 4. 子代理状态 | 是否标记为 `persistent`（常驻模式） |
| 5. 职责对应 | 子代理分配的任务是否与定时任务一致 |
---
## 检查执行步骤
### 步骤1：检查大管家（steward）
✅ **已完成检查**
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID命名：符合规范 ✅
- 工作记忆：已添加到活跃子代理清单 ✅
- 子代理状态：已标记为 `persistent` ✅
- 职责对应：与定时任务一致 ✅
---
### 步骤2：检查其他7个代理
#### 【教务助手（academicassistant）】
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID：`agent:academicassistant:cron:31db3717-398c-432b-800b-58b74e52a840` ✅
- 工作记忆检查：待验证
- 状态检查：待验证
#### 【审稿助手（reviewer）】
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID：`agent:reviewer:cron:8d60078e-ccc5-4f1a-b7d6-36da4b4dd4fe` ✅
- 工作记忆检查：待验证
- 状态检查：待验证
#### 【写作助手（writer）】
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID：`agent:writer:cron:a6de78f3-a9f2-4dac-b2f6-b9de9f5be29a` ✅
- 工作记忆检查：待验证
- 状态检查：待验证
#### 【教学助手（teaching）】
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID：`agent:teaching:cron:e6c72b8b-8c2b-4772-8e32-9ae4d78d9204` ✅
- 工作记忆检查：待验证
- 状态检查：待验证
#### 【心理学家（psychologist）】
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID：`agent:psychologist:cron:548da0f2-db95-4b37-ad71-7d1f783a5d09` ✅
- 工作记忆检查：待验证
- 状态检查：待验证
#### 【数学家（mathematician）】
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID：`agent:mathematician:cron:b86ca7c9-5cda-43e8-8800-d340b32c165d` ✅
- 工作记忆检查：待验证
- 状态检查：待验证
#### 【物理学家（physicist）】
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID：`agent:physicist:cron:95c97b8c-1daa-4360-8f3e-e3dfea9dcb3e` ✅
- 工作记忆检查：待验证
- 状态检查：待验证
#### 【学工助手（studentaffairsassistant）】
- 定时任务表：已添加子代理ID列 ✅
- 子代理ID：`agent:studentaffairsassistant:cron:853a6b05-6957-46ec-8e86-caf4551acd95` ✅
- 工作记忆检查：待验证
- 状态检查：待验证
---
## 预期结果
所有代理均已正确配置定时任务子代理，子代理ID符合规范，已添加到各自工作记忆，状态为`persistent`常驻模式，与定时任务一一对应。
