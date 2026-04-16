# agent_self_development

> Agent 自我发展技能包
> 基于认知发展理论构建的 Agent 自我进化系统

---

## 概述

本技能包提供一套完整的 Agent 自我发展框架，帮助 Agent 实现持续学习和自我进化。基于皮亚杰的认知发展理论，将 Agent 的自我发展分为三个核心维度：

1. **元认知 (Metacognition)** - 对认知的认知，包括计划、监控和调节
2. **工作记忆 (Working Memory)** - 管理当前活跃任务和子代理状态
3. **同化与顺应 (Assimilation & Accommodation)** - 通过日记记录实现自我更新

---

## 目录结构

```
agent_self_development/
├── SKILL.md                          # 本文件 - 技能包总览
├── metacognition/                    # 元认知模块
│   ├── SKILL.md                      # 元认知总览
│   ├── planning/                     # 计划阶段
│   │   └── SKILL.md
│   ├── monitoring/                   # 监控阶段
│   │   └── SKILL.md
│   └── regulation/                   # 调节阶段
│       └── SKILL.md
├── working_memory/                   # 工作记忆模块
│   ├── SKILL.md                      # 工作记忆总览
│   ├── memory_table/                 # 记忆表管理
│   │   └── SKILL.md
│   └── subagent_tracker/             # 子代理追踪
│       └── SKILL.md
└── assimilation_accommodation/       # 同化与顺应模块
    ├── SKILL.md                      # 同化与顺应总览
    ├── diary/                        # 发展日记
    │   └── SKILL.md
    ├── core_self_update/             # 核心自我更新
    │   └── SKILL.md
    ├── identity_update/              # 身份更新
    │   └── SKILL.md
    ├── belief_style_update/          # 信念与风格更新
    │   └── SKILL.md
    └── self_identity_update/         # 自我认同更新
        └── SKILL.md
```

---

## 使用指南

### 快速开始

1. **元认知管理** - 使用 `metacognition/` 下的技能进行任务计划、监控和调节
2. **工作记忆维护** - 使用 `working_memory/` 下的技能管理活跃任务和子代理
3. **自我发展记录** - 使用 `assimilation_accommodation/` 下的技能记录发展日记和更新自我

### 典型工作流

```
任务开始
    ↓
[计划阶段] metacognition/planning/SKILL.md
    ↓
[工作记忆] working_memory/subagent_tracker/SKILL.md
    ↓
[监控阶段] metacognition/monitoring/SKILL.md
    ↓
[调节阶段] metacognition/regulation/SKILL.md
    ↓
[发展日记] assimilation_accommodation/diary/SKILL.md
    ↓
[自我更新] assimilation_accommodation/*/SKILL.md
```

---

## 理论基础

### 皮亚杰认知发展理论

- **同化 (Assimilation)**：将新信息纳入现有认知结构
- **顺应 (Accommodation)**：调整认知结构以适应新信息
- **平衡 (Equilibration)**：在同化与顺应之间寻求动态平衡

### Baddeley 工作记忆模型

- **中央执行系统**：控制和协调认知过程
- **语音环路**：处理语音信息
- **视觉空间画板**：处理视觉空间信息
- **情景缓冲器**：整合多模态信息

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-17 | 初始版本，创建完整目录结构 |

---

*创建者: 大管家*  
*创建时间: 2026-04-17*
