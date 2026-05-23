---
pageType: source
id: source.conda
createdAt: 2026-05-12T11:05:00+08:00
updatedAt: 2026-05-12T11:05:00+08:00
sourceIds:
  - source.system-config
---

# Conda 环境管理

> 系统级环境管理器，用于管理 Python、R 及其运行环境。

---

## 安装信息

| 属性 | 值 |
|------|-----|
| **安装路径** | `~/miniconda3/` |
| **安装包** | Miniconda3-latest-Linux-x86_64.sh |
| **配置路径** | `~/.condarc` |
| **环境根目录** | `~/.conda/envs/` |
| **包缓存目录** | `~/.conda/pkgs/` |

---

## 环境列表

| 环境名 | 路径 | 语言/版本 | 用途 | Jupyter 内核 |
|--------|------|-----------|------|-------------|
| `base` | `~/miniconda3/` | Python 3.13 | 基础环境（含 Jupyter） | `python3` |
| `py311` | `~/.conda/envs/py311` | Python 3.11.15 | 通用 Python 开发 | `py311` |
| `r-base` | `~/.conda/envs/r-base` | R 4.3.1 | 统计分析与可视化 | `r-base` |

---

## Jupyter 内核

```bash
# 查看已注册内核
jupyter kernelspec list
```

| 内核名称 | 显示名称 | 对应环境 |
|----------|----------|----------|
| `python3` | Python 3 | base |
| `py311` | Python 3.11 | py311 |
| `r-base` | R 4.3.1 | r-base |

---

## 常用命令

```bash
# 激活环境
conda activate py311
conda activate r-base

# 创建新环境
conda create -n <env_name> python=<version>

# 安装包
conda install <package>
# 或
pip install <package>

# 导出环境
conda env export > environment.yml

# 启动 Jupyter
jupyter lab
```

---

## .condarc 配置

```yaml
envs_dirs:
  - ~/.conda/envs
pkgs_dirs:
  - ~/.conda/pkgs
channels:
  - defaults
  - conda-forge
auto_activate_base: false
```

---

## 引用方式

- 引用本来源：`[[sources/conda]]`
- 引用具体环境：通过环境名在任务描述中明确指定

## Related
<!-- openclaw:wiki:related:start -->
### Referenced By

- [[sources/programming-languages|系统编程语言]]
<!-- openclaw:wiki:related:end -->
