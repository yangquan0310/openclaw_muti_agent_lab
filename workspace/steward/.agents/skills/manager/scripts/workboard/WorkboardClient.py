#!/usr/bin/env python3
"""
WorkboardClient.py - OpenClaw Workboard RPC 客户端

封装 gateway WebSocket RPC + Ed25519 设备身份认证，
提供 workboard.cards.* 全套操作的 Python API。

用法示例：
    from workboard.WorkboardClient import WorkboardClient
    import asyncio

    async def main():
        client = WorkboardClient()
        await client.connect()
        cards = await client.list_cards()
        print(cards)
        await client.close()

    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import uuid
from typing import Any, Optional

import websockets
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


# 默认 gateway 配置（可通过环境变量覆盖）
DEFAULT_GATEWAY_URL = os.environ.get("OPENCLAW_GATEWAY_URL", "ws://127.0.0.1:18098")
OPENCLAW_GATEWAY_TOKEN = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")

# 默认 scope 集（按 control-ui 客户端行为取）
DEFAULT_SCOPES = [
    "operator.admin",
    "operator.read",
    "operator.write",
    "operator.approvals",
    "operator.pairing",
]

# 状态/优先级合法值
VALID_STATUSES = {"backlog", "todo", "running", "review", "blocked", "done"}
VALID_PRIORITIES = {"low", "normal", "high", "urgent"}


class WorkboardError(Exception):
    """Workboard RPC 错误"""
    def __init__(self, message: str, code: str = "", details: Optional[dict] = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}


class WorkboardClient:
    """Workboard RPC 客户端（自动处理设备身份认证）"""

    def __init__(
        self,
        token: Optional[str] = None,
        gateway_url: Optional[str] = None,
        client_id: str = "gateway-client",
        client_version: str = "1.0.0",
    ):
        self.token = token or OPENCLAW_GATEWAY_TOKEN
        if not self.token:
            raise WorkboardError("OPENCLAW_GATEWAY_TOKEN 未设置（从 ~/.openclaw/.env 读取）")
        self.gateway_url = gateway_url or DEFAULT_GATEWAY_URL
        self.client_id = client_id
        self.client_version = client_version
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self._seq = 0
        self._pending: dict[str, asyncio.Future] = {}
        self._reader_task: Optional[asyncio.Task] = None
        self._connected = False

    # ──────────────────────────
    # 连接管理
    # ──────────────────────────
    async def connect(self) -> dict:
        """连接 gateway 并完成设备身份 connect 握手。返回 hello 响应。"""
        self.ws = await websockets.connect(self.gateway_url, max_size=64 * 1024 * 1024)
        # 启动 reader 协程
        self._reader_task = asyncio.create_task(self._reader_loop())
        # 等待 connect.challenge 事件
        challenge = await self._wait_for_challenge()
        nonce = challenge["payload"]["nonce"]
        # 生成 Ed25519 设备身份（signedAt 在此计算一次，避免时间差）
        device_id, public_key_b64, signature, signed_at = await self._sign_connect(nonce)
        # 发送 connect 请求
        hello = await self.request("connect", {
            "minProtocol": 4,
            "maxProtocol": 4,
            "client": {
                "id": self.client_id,
                "version": self.client_version,
                "platform": "python",
                "mode": "cli",
            },
            "role": "operator",
            "scopes": DEFAULT_SCOPES,
            "device": {
                "id": device_id,
                "publicKey": public_key_b64,
                "signature": signature,
                "signedAt": signed_at,
                "nonce": nonce,
            },
            "caps": ["tool-events"],
            "auth": {"token": self.token},
        })
        self._connected = True
        return hello

    async def close(self) -> None:
        if self._reader_task:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except (asyncio.CancelledError, Exception):
                pass
        if self.ws:
            await self.ws.close()
        self._connected = False

    async def _wait_for_challenge(self, timeout: float = 5.0) -> dict:
        """等待 connect.challenge 事件"""
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            for fut in list(self._pending.values()):
                # 不会进来，这里只是占位
                pass
            # 简单轮询：等待 reader 收到 challenge
            await asyncio.sleep(0.05)
            if hasattr(self, "_challenge") and self._challenge:
                return self._challenge
        raise WorkboardError("等待 connect.challenge 超时")

    async def _sign_connect(self, nonce: str) -> tuple[str, str, str, int]:
        """生成 Ed25519 设备身份并签名 connect 握手。

        返回 (device_id, pub_b64, sig_b64, signed_at)。
        signed_at 必须与设备对象中的 signedAt 一致，否则签名验证失败。
        """
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        # 公钥 raw bytes -> base64url
        pub_raw = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        pub_b64 = _b64url(pub_raw)
        # 设备 ID = 公钥的 SHA-256 hex
        import hashlib
        device_id = hashlib.sha256(pub_raw).hexdigest()
        # 构造签名字符串（signedAt 只计算一次，connect() 拿到后原样填入 device 对象）
        signed_at = _now_ms()
        scopes_str = ",".join(DEFAULT_SCOPES)
        token_str = self.token if self.token else ""
        sign_payload = f"v2|{device_id}|{self.client_id}|cli|operator|{scopes_str}|{signed_at}|{token_str}|{nonce}"
        signature = private_key.sign(sign_payload.encode("utf-8"))
        sig_b64 = _b64url(signature)
        return device_id, pub_b64, sig_b64, signed_at

    async def _reader_loop(self) -> None:
        """后台读取 WebSocket 消息，分发到 pending futures"""
        try:
            async for raw in self.ws:
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if msg.get("type") == "event" and msg.get("event") == "connect.challenge":
                    self._challenge = msg
                elif msg.get("type") == "res":
                    req_id = msg.get("id")
                    fut = self._pending.pop(req_id, None)
                    if fut and not fut.done():
                        if msg.get("ok"):
                            fut.set_result(msg.get("payload"))
                        else:
                            err = msg.get("error") or {}
                            fut.set_exception(WorkboardError(
                                err.get("message", "rpc error"),
                                err.get("code", ""),
                                err.get("details"),
                            ))
        except websockets.ConnectionClosed:
            # 关闭所有 pending 请求
            for fut in self._pending.values():
                if not fut.done():
                    fut.set_exception(WorkboardError("gateway 连接已关闭"))
            self._pending.clear()

    # ──────────────────────────
    # 通用 RPC
    # ──────────────────────────
    async def request(self, method: str, params: dict) -> Any:
        """发送 RPC 请求并等待响应"""
        if not self.ws:
            raise WorkboardError("客户端未连接，请先调用 connect()")
        self._seq += 1
        req_id = f"req-{self._seq}-{uuid.uuid4().hex[:8]}"
        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        self._pending[req_id] = fut
        envelope = {"type": "req", "id": req_id, "method": method, "params": params}
        await self.ws.send(json.dumps(envelope))
        return await asyncio.wait_for(fut, timeout=15.0)

    # ──────────────────────────
    # Workboard 业务方法
    # ──────────────────────────
    async def list_cards(
        self,
        status: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 50,
        include_archived: bool = False,
    ) -> dict:
        params = {"limit": limit, "includeArchived": include_archived}
        if status:
            params["status"] = status
        if agent_id:
            params["agentId"] = agent_id
        return await self.request("workboard.cards.list", params)

    async def read_card(self, card_id: str) -> dict:
        """读单张卡片。workboard.cards.read RPC 不存在，改用 list 过滤。

        Returns:
            dict: 找到的卡片（脱敏后），或 {error: "not_found", id: ...}
        """
        # 先查活跃列表，再查已归档（archived 不在默认 list）
        result = await self.list_cards(limit=500, include_archived=True)
        for c in result.get("cards", []):
            if c.get("id") == card_id:
                return c
        return {"error": "not_found", "id": card_id}

    async def create_card(
        self,
        title: str,
        notes: str = "",
        status: str = "todo",
        priority: str = "normal",
        labels: Optional[list[str]] = None,
        agent_id: Optional[str] = None,
        source_url: Optional[str] = None,
        session_key: Optional[str] = None,
        execution: Optional[dict] = None,
    ) -> dict:
        if status not in VALID_STATUSES:
            raise WorkboardError(f"status 必须是 {VALID_STATUSES} 之一")
        if priority not in VALID_PRIORITIES:
            raise WorkboardError(f"priority 必须是 {VALID_PRIORITIES} 之一")
        params: dict[str, Any] = {
            "title": title,
            "status": status,
            "priority": priority,
        }
        if notes:
            params["notes"] = notes
        if labels:
            params["labels"] = labels
        if agent_id:
            params["agentId"] = agent_id
        if source_url:
            params["sourceUrl"] = source_url
        # 联动：让 Dashboard 真的显示"已关联会话"
        if session_key:
            params["sessionKey"] = session_key
        # 联动：让 Dashboard "代理"字段有非空显示（值域 codex/claude）
        if execution:
            params["execution"] = execution
        return await self.request("workboard.cards.create", params)

    async def update_card(self, card_id: str, patch: dict) -> dict:
        return await self.request("workboard.cards.update", {"id": card_id, "patch": patch})

    async def sessions_create(
        self,
        agent_id: str,
        label: str,
        model: str,
        message: Optional[str] = None,
    ) -> dict:
        """起一个 session。返回 dict 含 key（sessionKey）、sessionId、runId、entry。"""
        params: dict[str, Any] = {
            "agentId": agent_id,
            "label": label,
            "model": model,
        }
        if message:
            params["message"] = message
        return await self.request("sessions.create", params)

    async def move_card(self, card_id: str, status: str, position: Optional[int] = None) -> dict:
        if status not in VALID_STATUSES:
            raise WorkboardError(f"status 必须是 {VALID_STATUSES} 之一")
        params: dict[str, Any] = {"id": card_id, "status": status}
        if position is not None:
            params["position"] = position
        return await self.request("workboard.cards.move", params)

    async def delete_card(self, card_id: str) -> dict:
        return await self.request("workboard.cards.delete", {"id": card_id})

    async def archive_card(self, card_id: str, archived: bool = True) -> dict:
        return await self.request("workboard.cards.archive", {"id": card_id, "archived": archived})

    async def claim_card(
        self,
        card_id: str,
        owner_id: str,
        ttl_seconds: int = 120,
    ) -> dict:
        return await self.request(
            "workboard.cards.claim",
            {"id": card_id, "ownerId": owner_id, "ttlSeconds": ttl_seconds},
        )

    async def heartbeat_card(
        self,
        card_id: str,
        owner_id: Optional[str] = None,
        token: Optional[str] = None,
        note: Optional[str] = None,
    ) -> dict:
        params: dict[str, Any] = {"id": card_id}
        if owner_id:
            params["ownerId"] = owner_id
        if token:
            params["token"] = token
        if note:
            params["note"] = note
        return await self.request("workboard.cards.heartbeat", params)

    async def release_card(
        self,
        card_id: str,
        owner_id: Optional[str] = None,
        token: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        if status and status not in VALID_STATUSES:
            raise WorkboardError(f"status 必须是 {VALID_STATUSES} 之一")
        params: dict[str, Any] = {"id": card_id}
        if owner_id:
            params["ownerId"] = owner_id
        if token:
            params["token"] = token
        if status:
            params["status"] = status
        return await self.request("workboard.cards.release", params)

    async def comment_card(
        self,
        card_id: str,
        body: str,
        owner_id: Optional[str] = None,
        token: Optional[str] = None,
    ) -> dict:
        params: dict[str, Any] = {"id": card_id, "body": body}
        if owner_id:
            params["ownerId"] = owner_id
        if token:
            params["token"] = token
        return await self.request("workboard.cards.comment", params)

    async def proof_card(
        self,
        card_id: str,
        status: str = "passed",
        label: Optional[str] = None,
        command: Optional[str] = None,
        url: Optional[str] = None,
        note: Optional[str] = None,
        artifact_path: Optional[str] = None,
        owner_id: Optional[str] = None,
        token: Optional[str] = None,
    ) -> dict:
        params: dict[str, Any] = {"id": card_id, "status": status}
        for k, v in {
            "label": label, "command": command, "url": url,
            "note": note, "artifactPath": artifact_path,
            "ownerId": owner_id, "token": token,
        }.items():
            if v is not None:
                params[k] = v
        return await self.request("workboard.cards.proof", params)

    async def unblock_card(
        self,
        card_id: str,
        owner_id: Optional[str] = None,
        token: Optional[str] = None,
    ) -> dict:
        params: dict[str, Any] = {"id": card_id}
        if owner_id:
            params["ownerId"] = owner_id
        if token:
            params["token"] = token
        return await self.request("workboard.cards.unblock", params)

    async def bulk_action(self, action: str, card_ids: list[str], **kwargs) -> dict:
        params = {"action": action, "ids": card_ids, **kwargs}
        return await self.request("workboard.cards.bulk", params)

    async def export_cards(self) -> dict:
        return await self.request("workboard.cards.export", {})


# ──────────────────────────
# 工具函数
# ──────────────────────────
def _now_ms() -> int:
    return int(__import__("time").time() * 1000)


def _b64url(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii").replace("+", "-").replace("/", "_").rstrip("=")


# ──────────────────────────
# 异步上下文管理器支持
# ──────────────────────────
class async_conn:
    """async with WorkboardClient() as client: 的语法糖"""
    def __init__(self, **kwargs):
        self.client = WorkboardClient(**kwargs)

    async def __aenter__(self):
        await self.client.connect()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()
        return False
