---
pageType: source
id: source.programming-languages
createdAt: 2026-05-12T11:10:00+08:00
updatedAt: 2026-05-12T11:10:00+08:00
sourceIds:
  - source.system-config
---

# 系统编程语言

> 服务器上已安装的编程语言及运行时环境汇总。

---

## 语言清单

| 语言 | 版本 | 路径 | 类型 | 说明 |
|------|------|------|------|------|
| **Python** | 3.12.3 | `/usr/bin/python3` | 系统 | Ubuntu 自带 |
| **Node.js** | v22.22.2 | `/usr/bin/node` | 系统 | OpenClaw 依赖 |
| **npm** | 10.9.7 | `/usr/bin/npm` | 系统 | Node 包管理器 |
| **OpenJDK** | 21.0.10 | `/usr/bin/java` | 系统 | Java 运行时（无 javac） |
| **Ruby** | 3.2.3 | `/usr/bin/ruby` | 系统 | Ubuntu 自带 |
| **Perl** | — | `/usr/bin/perl` | 系统 | Ubuntu 自带 |
| **Bash** | 5.2.21 | `/usr/bin/bash` | 系统 | 默认 shell |

---

## Conda 管理的环境

由 [[sources/conda]] 统一管理：

| 环境 | 语言 | 版本 | 路径 |
|------|------|------|------|
| base | Python | 3.13 | `~/miniconda3/` |
| py311 | Python | 3.11.15 | `~/.conda/envs/py311` |
| r-base | R | 4.3.1 | `~/.conda/envs/r-base` |

---

## 使用建议

- **数据分析/科学计算**：使用 `conda activate py311` 或 `conda activate r-base`
- **OpenClaw 开发**：使用系统 Node.js（v22）
- **通用脚本**：系统 Python 3.12 或 Bash
- **需要 Java 编译**：系统未安装 javac，如需编译需另行安装 JDK

---

## 引用方式

- 引用本来源：`[[sources/programming-languages]]`
- 引用 Conda 环境：`[[sources/conda]]`

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
