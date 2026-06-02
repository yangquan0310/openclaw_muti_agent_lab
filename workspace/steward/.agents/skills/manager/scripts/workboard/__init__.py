"""
workboard - OpenClaw Workboard RPC 客户端

能力：建/改/移/删/批量/归档/列/读/认领/续约/释放/评论/证明 等全部 workboard 操作。
所有写操作（建/改/移/删/批量/归档）走 gateway WebSocket RPC + 设备身份认证。
"""

from .WorkboardClient import WorkboardClient, WorkboardError, OPENCLAW_GATEWAY_TOKEN

__all__ = ["WorkboardClient", "WorkboardError", "OPENCLAW_GATEWAY_TOKEN"]
