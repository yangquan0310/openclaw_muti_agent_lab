---
pageType: synthesis
id: synthesis.audit.2026-06-23.fortunetelling
title: 技能审计：fortunetelling v1.0.0 现状（2026-06-23）
createdAt: "2026-06-23T20:57:00+08:00"
auditor: reviewer (workboard card bd68a40c-68bd-449a-8c4a-4244cbbf1d71)
target_skill: ~/.openclaw/workspace/steward/.agents/skills/fortunetelling/
audit_sop: skill-audit-workflow.md
target_version: 1.0.0
provenance:
  type: skill_audit
  scope: only_audit_no_modification
sourceIds:
  - placeholder  # TODO: 引用真实 source  # 待补：引用了哪些 sources
updatedAt: "2026-06-23T20:57:00+08:00"
---


# 技能审计：fortunetelling v1.0.0 现状

> **审计范围**：只审计，不修改
> **审计 SOP**：五章节结构 + references 命名 + 自检 4 问 + 常见问题修复

---

## 0. 摘要（TL;DR）

| 维度 | 评级 | 关键问题 |
|------|------|---------|
| 五章节结构 | 🟡 部分达标 | 触发条件清晰；核心原则缺失（被"核心功能"替代）；场景索引缺失；边界条件缺失 |
| references 命名规范 | 🔴 **完全不合规** | 7 个 references 全是 `bazi-theory.md / dayun-guide.md / gezhi-guide.md / guide.md / index.md / marriage-guide.md / shensha-guide.md`——但 dayun-guide / marriage-guide / shensha-guide / gezhi-guide 已含 `-guide` 后缀 ✅；guide.md 太通用 🟡 |
| 自检 4 问 | 🟡 触发条件✅；边界条件❌ | "做什么"✅ "何时用"✅；"不做什么"❌ 无显式边界条件 |
| 常见问题修复 | 🔴 触发 3 项 | description 较简洁 ✅；边界条件缺失 ❌；references 命名部分不合规；版本号 OK |

**整体结论**：fortunetelling 是**功能型技能**（CLI 计算），五章节结构按"触发条件 + 核心功能 + 目录结构 + 快速调用"组织，与 SOP 期望的"原则 + 索引 + 边界"模型有差距。**🔴 必须修：2 项；🟡 建议修：3 项；🟢 可选优化：2 项**。

---

## 1. 五章节结构核查

| 章节 | 必备内容 | 实际内容 | 评级 |
|------|---------|----------|------|
| **name** | 技能唯一标识 | `name: fortunetelling` ✅ | 🟢 |
| **description** | 触发条件 + 不激活场景 | "当用户提到「算命」、「八字」、「排盘」、「大运」、「流年」、「命理」、「算卦」时触发" ✅ 触发词具体 | 🟢 |
| **核心原则** | 3-5 条核心信念 | ❌ 缺失——SKILL.md 用"核心功能"表格替代（八字排盘 / 大运排盘 / 流年排盘等 8 项） | 🔴 |
| **场景索引** | 指南文件与用途对应 | ❌ 缺失 | 🔴 |
| **边界条件** | 不做什么 | ❌ 缺失——SKILL.md 未声明"不做什么" | 🔴 |

**关键问题**：SKILL.md 结构 = `description + 触发条件 + 核心功能 + 技术实现 + 目录结构 + 快速调用`，**与 SOP 期望的"原则 + 索引 + 边界"模型完全不同**。这是个**风格分歧**：fortunetelling 是 CLI 计算型技能（与 lark-* 家族类似），不需要"核心原则"。

---

## 2. references 命名规范核查

| 实际文件名 | SOP 期望 | 是否合规 | 类型 |
|------------|---------|---------|------|
| `index.md` | — | ✅ 例外 | 索引 |
| `guide.md` | `guide.md` 或 `*-guide.md` | 🟡 名称太通用 | 使用指南 |
| `bazi-theory.md` | `bazi-theory-guide.md` | 🟡 缺 `-guide` 后缀 | 理论指南 |
| `dayun-guide.md` | `*-guide.md` | ✅ | 指南 |
| `gezhi-guide.md` | `*-guide.md` | ✅ | 指南 |
| `marriage-guide.md` | `*-guide.md` | ✅ | 指南 |
| `shensha-guide.md` | `*-guide.md` | ✅ | 指南 |

**统计**：7 个 references 中 4 个合规（57%）——比 research-assistant 好，但比 manager 差。

---

## 3. 自检 4 问核查

| 问题 | 回答 | 评级 |
|------|------|------|
| 能一句话说明做什么？ | ✅ "命理排盘技能，根据八字推算大运、流年、学业、婚姻、事业等运势" | 🟢 |
| 能说清楚不做什么？ | ❌ 无显式边界条件——例如：是否负责解梦？是否负责塔罗？是否提供择日服务？| 🔴 |
| 使用者能判断何时用？ | ✅ 触发词具体（算命/八字/排盘/大运/流年/命理/算卦）| 🟢 |
| 每次使用产生相同结果？ | ✅ 纯计算技能（lunar_python + 十神关系）——结果可重现 | 🟢 |

---

## 4. 常见问题修复 4 项核查

| 问题 | 是否触发 | 说明 |
|------|---------|------|
| description 触发条件模糊 | ✅ 不触发 | 触发词清晰 |
| 缺少边界条件 | 🔴 **触发** | 无 "不做什么" 章节 |
| references 文件名不规范 | 🟡 部分触发 | 3 个 `*-theory.md` / `guide.md` 不符合 `-guide` 后缀 |
| 版本号混乱 | ✅ 不触发 | SKILL.md `version: 1.0.0` 与 _meta.json `version: 1.0.0` 一致 |

---

## 5. 资产与脚本

| 类型 | 数量 | 评价 |
|------|------|------|
| assets/ | 1 个 templates/ 子目录 | 🟡 |
| scripts/ | 3 个（lunar.py / bazi.py / fate.py）| 🟢 |
| _meta.json | ✅ 存在（含 scripts 路径映射） | 🟢 |
| index/ | 存在（含 manifest.json / chunks.json）——lookup! 索引已构建 | 🟢 |

### 5.1 脚本与 _meta.json 一致性

- `_meta.json` 声明：`lunar.py` / `bazi.py` / `fate.py`
- 实际 scripts/：包含上述 3 个 ✅ 一致

### 5.2 SKILL.md "快速调用" 路径问题

```bash
lookup! index -r /root/.openclaw/workspace/steward/skills/fortunetelling/references
```

路径指向 `~/.openclaw/workspace/steward/skills/fortunetelling/` 而**实际技能在** `~/.openclaw/workspace/steward/.agents/skills/fortunetelling/`——**🟡 路径错误**（少 `.agents/` 一段）。可能是历史路径变更未更新。

---

## 6. 修复优先级与建议路径

| 优先级 | 项目 | 修复成本 | 风险 |
|--------|------|---------|------|
| 🔴 必须修 #1 | 加 "## 边界条件" 章节（明确不做什么：解梦、塔罗、择日、合婚以外的内容等）| 10 分钟 | 极低 |
| 🔴 必须修 #2 | SKILL.md "快速调用" 路径修复：补 `.agents/` 一段 | 2 分钟 | 极低 |
| 🟡 建议修 #1 | 加 "## 核心原则" 章节（如"节气为准 / 月令优先 / 综合判断 / 有错必改"——README 提到）| 10 分钟 | 极低 |
| 🟡 建议修 #2 | references/bazi-theory.md 改名为 bazi-theory-guide.md | 2 分钟 | 极低 |
| 🟡 建议修 #3 | SKILL.md 加 "## 场景索引" 指向 references/index.md | 5 分钟 | 极低 |
| 🟢 可选优化 #1 | references/guide.md 改名为 usage-guide.md 或明确指向主题 | 5 分钟 | 极低 |
| 🟢 可选优化 #2 | references/gezhi-guide.md 拼写核查（应为"gezi" 或 "gdzhi"？）—— 可能是 "格局" 的简写 | 5 分钟 | 极低 |

**总计**：~40 分钟可修复全部问题。

---

## 7. 审计结论

fortunetelling v1.0.0 是**功能完整但文档不达 SOP 标准**的技能：
- 触发条件清晰 ✅
- 核心功能表格化 ✅
- 缺失核心原则 + 场景索引 + 边界条件 3 个章节
- references 命名部分不合规
- 存在 1 处路径错误

**总体评级**：🟡 **C+ 级（可用但需补文档）**

---

## 8. 审计元数据

| 字段 | 值 |
|------|---|
| 审计时间 | 2026-06-23 20:57 (Asia/Shanghai) |
| 审计目标版本 | 1.0.0 |
| 发现问题 | 7 项（🔴 2 / 🟡 3 / 🟢 2） |
| 报告路径 | `~/.openclaw/wiki/syntheses/2026-06-23-audit-fortunetelling.md` |

---

*最后更新：2026-06-23 20:57 GMT+8*
*审计对象：fortunetelling v1.0.0*

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
