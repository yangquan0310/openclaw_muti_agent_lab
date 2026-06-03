---
pageType: source
id: source.openclaw-env
createdAt: "2026-05-12T10:55:00+08:00"
updatedAt: "2026-05-12T10:55:00+08:00"
title: openclaw-env
sourceIds:
  - source.system-config
aliases:
  - 环境变量配置
---

# OpenClaw 环境变量配置

> 敏感配置文件位置。
> **注意：本页面仅记录文件路径和配置类型，绝不记录具体值。**

---

## 路径

```
~/.openclaw/.env
```

## 包含的配置类型

| 类型 | 说明 | 示例（已脱敏） |
|------|------|----------------|
| API Key | 外部服务调用密钥 | `SEMANTIC_SCHOLAR_API_KEY=***` |
| Token | 认证令牌 | `FEISHU_APP_TOKEN=***` |
| 密码 | 数据库/服务密码 | `DB_PASSWORD=***` |

## 访问权限

- **系统管理员**：读写权限
- **Agent**：**禁止读取**（安全红线）
- **其他用户**：无权限

## 使用方式

Agent 通过 OpenClaw 内置机制访问 API，**不直接读取 .env 文件**。

## 相关

- [[sources/openclaw-system]] — OpenClaw 系统目录
-  — 安全红线（禁止泄露敏感信息）

---

*最后更新：2026-05-12*

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[syntheses/2026-06-04-01-57-46-Quarto-PDF编译配置总结-3范式-CJK字体-APA7th|Quarto PDF 编译配置总结：3 范式 + CJK 字体 + APA 7th]]
<!-- openclaw:wiki:related:end -->
