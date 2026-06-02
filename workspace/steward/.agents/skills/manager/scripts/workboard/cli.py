#!/usr/bin/env python3
"""
workboard/cli.py - Workboard RPC 命令行接口

通过 manager CLI 统一入口调用：
    manager workboard <子命令> [选项]

子命令：
    list                列出卡片
    read                读取卡片详情
    create              创建卡片
    update              更新卡片
    move                移动卡片（看板拖拽）
    delete              删除卡片
    archive             归档 / 取消归档
    claim               认领卡片
    heartbeat           续约
    release             释放
    comment             评论
    proof               附证明
    unblock             解阻塞
    bulk                批量操作
    export              导出
"""

import argparse
import asyncio
import json
import sys
from typing import Any

from .WorkboardClient import (
    WorkboardClient,
    WorkboardError,
    VALID_STATUSES,
    VALID_PRIORITIES,
)


# ──────────────────────────
# 输出辅助
# ──────────────────────────
def out(payload: Any) -> int:
    """以 JSON 格式输出到 stdout"""
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    return 0


def err_out(message: str, code: str = "", details: Any = None) -> int:
    """以 JSON 格式输出错误到 stderr"""
    payload = {"ok": False, "error": {"message": message, "code": code, "details": details or {}}}
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
    return 1


# ──────────────────────────
# 子命令实现
# ──────────────────────────
async def cmd_list(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.list_cards(
        status=args.status,
        agent_id=args.assignee,
        limit=args.limit,
        include_archived=args.archived,
    )
    return out({"ok": True, "cards": result.get("cards", []), "count": len(result.get("cards", []))})


async def cmd_read(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.read_card(args.id)
    return out(result)


async def cmd_create(client: WorkboardClient, args: argparse.Namespace) -> int:
    labels = [l.strip() for l in args.labels.split(",")] if args.labels else None
    result = await client.create_card(
        title=args.title,
        notes=args.notes or "",
        status=args.status,
        priority=args.priority,
        labels=labels,
        agent_id=args.assignee,
    )
    card = result.get("card", result)
    return out({"ok": True, "card": card, "card_id": card.get("id")})


async def cmd_update(client: WorkboardClient, args: argparse.Namespace) -> int:
    patch: dict = {}
    if args.title:
        patch["title"] = args.title
    if args.notes:
        patch["notes"] = args.notes
    if args.priority:
        patch["priority"] = args.priority
    if args.labels:
        patch["labels"] = [l.strip() for l in args.labels.split(",")]
    if not patch:
        return err_out("update 至少需要 --title/--notes/--priority/--labels 之一")
    result = await client.update_card(args.id, patch)
    return out(result)


async def cmd_move(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.move_card(args.id, args.status, position=args.position)
    return out(result)


async def cmd_delete(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.delete_card(args.id)
    return out({"ok": True, "deleted": args.id, "raw": result})


async def cmd_archive(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.archive_card(args.id, archived=not args.unarchive)
    return out(result)


async def cmd_claim(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.claim_card(args.id, args.owner, ttl_seconds=args.ttl)
    card = result.get("card", {})
    claim = card.get("metadata", {}).get("claim", {})
    return out({
        "ok": True,
        "card_id": args.id,
        "owner_id": claim.get("ownerId"),
        "expires_at": claim.get("expiresAt"),
        "token": result.get("token"),
    })


async def cmd_heartbeat(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.heartbeat_card(args.id, owner_id=args.owner, token=args.token, note=args.note)
    return out(result)


async def cmd_release(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.release_card(args.id, owner_id=args.owner, token=args.token, status=args.status)
    return out({"ok": True, "card_id": args.id, "released_to": args.status, "raw": result})


async def cmd_comment(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.comment_card(args.id, args.body, owner_id=args.owner, token=args.token)
    return out(result)


async def cmd_proof(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.proof_card(
        args.id, status=args.proof_status, label=args.label, command=args.command,
        url=args.url, note=args.note, artifact_path=args.artifact,
        owner_id=args.owner, token=args.token,
    )
    return out(result)


async def cmd_unblock(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.unblock_card(args.id, owner_id=args.owner, token=args.token)
    return out(result)


async def cmd_bulk(client: WorkboardClient, args: argparse.Namespace) -> int:
    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    extra: dict = {}
    if args.status:
        extra["status"] = args.status
    if args.archive is not None:
        extra["archived"] = args.archive
    result = await client.bulk_action(args.action, ids, **extra)
    return out(result)


async def cmd_export(client: WorkboardClient, args: argparse.Namespace) -> int:
    result = await client.export_cards()
    return out(result)


# ──────────────────────────
# argparse 构建
# ──────────────────────────
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="manager workboard",
        description="OpenClaw Workboard 任务发布/管理 CLI（gateway RPC + 设备身份认证）",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True, metavar="<子命令>")

    # list
    p = sub.add_parser("list", help="列出卡片")
    p.add_argument("--status", choices=sorted(VALID_STATUSES), help="按状态过滤")
    p.add_argument("--assignee", help="按 agentId 过滤")
    p.add_argument("--limit", type=int, default=50, help="最多返回数（默认 50）")
    p.add_argument("--archived", action="store_true", help="包含已归档")
    p.set_defaults(_func=cmd_list)

    # read
    p = sub.add_parser("read", help="读取卡片详情")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.set_defaults(_func=cmd_read)

    # create
    p = sub.add_parser("create", help="创建卡片（任务发布）")
    p.add_argument("--title", required=True, help="卡片标题")
    p.add_argument("--notes", help="卡片描述/笔记")
    p.add_argument("--status", choices=sorted(VALID_STATUSES), default="todo", help="初始状态（默认 todo）")
    p.add_argument("--priority", choices=sorted(VALID_PRIORITIES), default="normal", help="优先级（默认 normal）")
    p.add_argument("--labels", help="标签，逗号分隔（如 ch12,文献检索）")
    p.add_argument("--assignee", help="指派给 agent（如 psychologist / writer）")
    p.set_defaults(_func=cmd_create)

    # update
    p = sub.add_parser("update", help="更新卡片字段")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--title", help="新标题")
    p.add_argument("--notes", help="新描述")
    p.add_argument("--priority", choices=sorted(VALID_PRIORITIES), help="新优先级")
    p.add_argument("--labels", help="新标签（覆盖）")
    p.set_defaults(_func=cmd_update)

    # move
    p = sub.add_parser("move", help="移动卡片到另一状态（看板拖拽）")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--status", choices=sorted(VALID_STATUSES), required=True, help="目标状态")
    p.add_argument("--position", type=int, help="新位置")
    p.set_defaults(_func=cmd_move)

    # delete
    p = sub.add_parser("delete", help="删除卡片（不可恢复）")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.set_defaults(_func=cmd_delete)

    # archive
    p = sub.add_parser("archive", help="归档 / 取消归档卡片")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--unarchive", action="store_true", help="取消归档（默认归档）")
    p.set_defaults(_func=cmd_archive)

    # claim
    p = sub.add_parser("claim", help="认领卡片（独占）")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--owner", required=True, help="认领者 agentId（如 steward / writer）")
    p.add_argument("--ttl", type=int, default=120, help="TTL 秒数（默认 120）")
    p.set_defaults(_func=cmd_claim)

    # heartbeat
    p = sub.add_parser("heartbeat", help="续约（防 claim 过期）")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--owner", help="认领者 agentId")
    p.add_argument("--token", help="claim 返回的 token")
    p.add_argument("--note", help="续约时的进度备注（会作为评论记录）")
    p.set_defaults(_func=cmd_heartbeat)

    # release
    p = sub.add_parser("release", help="释放卡片（认领结束）")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--owner", help="认领者 agentId")
    p.add_argument("--token", help="claim 返回的 token")
    p.add_argument("--status", choices=sorted(VALID_STATUSES), help="释放后的目标状态")
    p.set_defaults(_func=cmd_release)

    # comment
    p = sub.add_parser("comment", help="添加评论")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--body", required=True, help="评论正文")
    p.add_argument("--owner", help="认领者 agentId（如已认领）")
    p.add_argument("--token", help="claim 返回的 token")
    p.set_defaults(_func=cmd_comment)

    # proof
    p = sub.add_parser("proof", help="附证明（测试/检查结果）")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--proof-status", choices=["passed", "failed", "skipped", "unknown"], default="passed", help="证明状态")
    p.add_argument("--label", help="证明标签")
    p.add_argument("--command", help="执行的命令")
    p.add_argument("--url", help="证明 URL")
    p.add_argument("--note", help="证明备注")
    p.add_argument("--artifact", help="本地 artifact 路径")
    p.add_argument("--owner", help="认领者 agentId")
    p.add_argument("--token", help="claim 返回的 token")
    p.set_defaults(_func=cmd_proof)

    # unblock
    p = sub.add_parser("unblock", help="解除阻塞（移到 todo）")
    p.add_argument("--id", required=True, help="卡片 ID")
    p.add_argument("--owner", help="认领者 agentId")
    p.add_argument("--token", help="claim 返回的 token")
    p.set_defaults(_func=cmd_unblock)

    # bulk
    p = sub.add_parser("bulk", help="批量操作（archive/move/delete/label）")
    p.add_argument("--action", required=True, choices=["archive", "unarchive", "move", "delete", "label"], help="批量动作")
    p.add_argument("--ids", required=True, help="卡片 ID 列表，逗号分隔")
    p.add_argument("--status", choices=sorted(VALID_STATUSES), help="move 时的目标状态")
    p.add_argument("--archive", type=lambda v: v.lower() in ("true", "1", "yes"), help="archive 状态（true/false）")
    p.set_defaults(_func=cmd_bulk)

    # export
    p = sub.add_parser("export", help="导出所有卡片")
    p.set_defaults(_func=cmd_export)

    return parser


# ──────────────────────────
# 主入口
# ──────────────────────────
def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    async def runner() -> int:
        client = WorkboardClient()
        try:
            await client.connect()
        except WorkboardError as e:
            return err_out(f"connect 失败: {e}", code=e.code, details=e.details)
        except Exception as e:
            return err_out(f"connect 失败: {e}")
        try:
            return await args._func(client, args)
        except WorkboardError as e:
            return err_out(f"{args.subcommand} 失败: {e}", code=e.code, details=e.details)
        except Exception as e:
            return err_out(f"{args.subcommand} 失败: {e}")
        finally:
            await client.close()

    return asyncio.run(runner())


if __name__ == "__main__":
    raise SystemExit(main())
