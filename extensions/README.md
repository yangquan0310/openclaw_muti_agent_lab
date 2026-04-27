# Extensions 目录

此目录用于存放 OpenClaw 插件。

## 说明

- 第三方插件通过 `openclaw plugins install` 安装，不会同步到 Git
- 自己开发的插件可以放在此处，并修改 `.gitignore` 添加例外规则

## 当前安装的插件

### 第三方插件（不同步）

| 插件 | 版本 | 来源 |
|------|------|------|
| adp-openclaw | 0.0.77 | npm |
| ddingtalk | 2.0.1 | npm |
| lightclawbot | 1.1.2 | npm |
| memory-tencentdb | 0.2.2 | npm |
| openclaw-lark | 2026.4.7 | archive |
| openclaw-plugin-yuanbao | 2.10.0 | npm |
| openclaw-weixin | 2.1.9 | npm |
| wecom | 2026.3.24 | npm |

### 自研插件（同步）

| 插件 | 版本 | 来源 |
|------|------|------|
| agent-self-development | 1.0.0 | 本地开发 |

## 添加自研插件到 Git

在 `.gitignore` 的 extensions 区域添加：
```gitignore
!/extensions/your-plugin-name/
```

---

## 🤖 Agent Self-Development 插件（v1.0.0）

已升级为 OpenClaw 官方插件，基于 Hook 驱动。

详见 [`agent-self-development/README.md`](agent-self-development/README.md)
