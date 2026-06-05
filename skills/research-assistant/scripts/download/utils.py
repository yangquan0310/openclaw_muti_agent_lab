"""utils.py - download 模块共享工具

- 加载 .env（无 python-dotenv 依赖）
- 安全的 HTTP Basic Auth
- 文件名清理
"""

from __future__ import annotations

import base64
import re
from pathlib import Path
from typing import Dict


def load_env_file(path: str = "/root/.openclaw/.env") -> Dict[str, str]:
    """加载 .env 文件（简单 KEY=VALUE 解析，忽略 # 注释行）

    Args:
        path: .env 文件路径

    Returns:
        解析后的字典
    """
    env: Dict[str, str] = {}
    p = Path(path)
    if not p.exists():
        return env
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def basic_auth_header(user: str, password: str) -> str:
    """构造 HTTP Basic Auth 头（注意：不在返回值中保留明文）"""
    if not user or not password:
        raise ValueError("basic_auth_header: user 和 password 都必填")
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    return f"Basic {token}"


def safe_filename(s: str, max_length: int = 100) -> str:
    """清理非法文件名字符"""
    s = re.sub(r'[<>:"/\\|?*]', "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:max_length] if len(s) > max_length else s


def parse_zotero_date(date_str: str):
    """解析 Zotero date 字段为 (year, month, day) 元组

    支持格式：
    - '2017'
    - '08/2017'
    - '2017-08'
    - '2017-08-15'
    - '2017-08-15T10:30:00Z'
    """
    if not date_str:
        return None, None, None
    s = str(date_str).strip()
    # 优先尝试 ISO 格式（接受 1-2 位月份/日期）
    m = re.match(r"^(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?", s)
    if m:
        y, mo, d = int(m.group(1)), m.group(2), m.group(3)
        return y, int(mo) if mo else None, int(d) if d else None
    # 尝试 "MM/YYYY" 格式
    m = re.match(r"^(\d{1,2})/(\d{4})", s)
    if m:
        return int(m.group(2)), int(m.group(1)), None
    return None, None, None
