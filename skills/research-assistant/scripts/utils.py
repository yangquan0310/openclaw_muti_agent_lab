"""common.py - 跨模块共享工具

- config(path)           加载 config.json + 解析 ${VAR}
- frontmatter(content)   拆 (metadata, body)
- field(content, key)    提取单字段

WIKI_* 路径常量：所有模块共享 wiki 后端路径。
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any


# ─── 路径常量 ────────────────────────────────────────

WIKI_ROOT = Path("~/.openclaw/wiki").expanduser()
WIKI_SOURCES = WIKI_ROOT / "sources"
WIKI_SYNTHESES = WIKI_ROOT / "syntheses"
WIKI_CONCEPTS = WIKI_ROOT / "concepts"
WIKI_REPORTS = WIKI_ROOT / "reports"
WIKI_RAW_PAPERS = WIKI_ROOT / "raw" / "papers"


def ensure_wiki_dirs():
    """确保 wiki 所有目录存在"""
    for d in [WIKI_SOURCES, WIKI_SYNTHESES, WIKI_CONCEPTS, WIKI_REPORTS, WIKI_RAW_PAPERS]:
        d.mkdir(parents=True, exist_ok=True)


# ─── config ──────────────────────────────────────────

_PLACEHOLDER_RE = re.compile(r"\$\{(\w+)\}")


def config(path: str = "scripts/config.json") -> dict:
    """加载 config.json + 递归替换 ${VAR} 为环境变量值。

    自动把 `xxx_env` 字段（如 `api_key_env`）解析后填到 `xxx`：
        api_key_env: "${SEMANTIC_SCHOLAR_API_KEY}" + 环境变量 = "KpNolz..."
        → 同时设置 api_key: "KpNolz..."（直接使用）

    Args:
        path: config.json 路径（默认 scripts/config.json）

    Returns:
        解析后的 dict（已替换所有 ${VAR}，且 `*_env` 字段已复制到 `*`）

    Note:
        - 占位符在加载时一次性解析
        - 缺失的 env var 保留原样 ${VAR}（让调用方决定）
        - 文件不存在返回 {}
    """
    p = Path(path).expanduser()
    if not p.exists():
        return {}
    raw = json.loads(p.read_text(encoding="utf-8"))
    resolved = _resolve(raw)
    return _expand_env_fields(resolved)


def _expand_env_fields(obj):
    """递归把 `*_env` 字段的值复制到对应的 `*` 字段（如果后者不存在）

    Example:
        {"api_key_env": "abc"} → {"api_key_env": "abc", "api_key": "abc"}
        {"api_key": "explicit"} → 不覆盖（保持显式值）
    """
    if isinstance(obj, dict):
        for k in list(obj.keys()):
            if k.endswith("_env"):
                base = k[:-4]  # api_key_env → api_key
                if base not in obj or not obj[base]:
                    obj[base] = obj[k]
            _expand_env_fields(obj[k])
    elif isinstance(obj, list):
        for v in obj:
            _expand_env_fields(v)
    return obj


def _resolve(obj: Any) -> Any:
    """递归解析 ${VAR} 占位符"""
    if isinstance(obj, str):
        return _PLACEHOLDER_RE.sub(
            lambda m: os.environ.get(m.group(1), m.group(0)),
            obj,
        )
    if isinstance(obj, dict):
        return {k: _resolve(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolve(v) for v in obj]
    return obj


# ─── frontmatter ─────────────────────────────────────

_FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)", re.DOTALL)


def frontmatter(content: str) -> tuple[dict, str]:
    """解析 wiki 文件的 YAML frontmatter。

    Args:
        content: 文件全文（含 --- 包裹的 frontmatter + body）

    Returns:
        (metadata dict, body markdown 字符串)

    Note:
        - 简单 key: value 解析（不引入 PyYAML）
        - 列表字段用 [item1, item2] 表示（不解析嵌套）
        - 没有 frontmatter 时返回 ({}, content)
    """
    m = _FRONT_RE.match(content)
    if not m:
        return {}, content
    yaml_text = m.group(1)
    body = m.group(2)
    metadata: dict = {}
    for line in yaml_text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not line.startswith((" ", "\t")):
            # 顶层 key
            if value == "[]":
                metadata[key] = []
            elif value == "":
                metadata[key] = ""
            else:
                metadata[key] = value
    return metadata, body


def field(content: str, key: str) -> str | None:
    """便捷函数：从 frontmatter 提取单字段。

    Args:
        content: 文件全文
        key: 字段名（如 "id" / "zotero_item_key"）

    Returns:
        字段值（字符串），未找到返回 None
    """
    metadata, _ = frontmatter(content)
    return metadata.get(key)