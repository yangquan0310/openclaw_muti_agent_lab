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


# IM 任务派发模板 → Workboard notes 格式（与 task-guide.md §五 / §四 保持一致）
TASK_NOTES_TEMPLATE = """{task_desc}

{assignee}

📋 前置要求：
- 明确自己的角色：{agent_role}，找到对应的 .agents/agents/{agent_role}.md 阅读
- 查看 TODO.md 中的 {subtask} 子任务

🎯 任务目标：
- {goal}

📌 任务约束：
- {constraints}

📁 输入文件：
- {input_file}

📄 输出文件：
- {output_file}

💬 反馈：
- 完成后在群聊中艾特大管家汇报
- 汇报内容：完成的是什么任务
- 汇报内容：产出是什么（文件路径）
"""


def _build_task_notes(args) -> str:
    """根据 CLI 参数组装 notes 字段，结构与 IM 派发模板一致"""
    assignee = args.assignee or ""
    # --task-desc 优先，--notes 兜底
    task_desc = args.task_desc or args.notes or ""
    # 默认值（让模板不留空）
    goal = args.goal or "（待补充）"
    constraints = args.constraints or "（待补充）"
    feedback = args.feedback or "完成后在群聊中艾特大管家汇报，产出 = 文件路径"
    return TASK_NOTES_TEMPLATE.format(
        task_desc=task_desc,
        assignee=f"@{assignee}" if assignee else "（未指定）",
        agent_role=args.agent_role or assignee or "（未指定）",
        subtask=args.subtask or "（待补充）",
        goal=goal,
        constraints=constraints,
        input_file=args.input_file or "（无）",
        output_file=args.output_file or "（无）",
        feedback=feedback,
    )


async def cmd_create(client: WorkboardClient, args: argparse.Namespace) -> int:
    # 必填检查：agentId（卡片创建时必须指定 agent）
    if not args.assignee:
        return err_out("--assignee 必填：workboard 创建卡片时必须指定 agent")

    labels = [l.strip() for l in args.labels.split(",")] if args.labels else None

    # 根据结构化参数组装 notes（--notes 可选覆盖）
    notes = args.notes or _build_task_notes(args)

    # 联动：让 Dashboard 真的显示"已关联会话"（用户反馈：之前一直"没有已关联的会话"）
    session_key = None if args.no_session else f"agent:{args.assignee}:main"

    # 联动：让 Dashboard "代理"字段非空（值域 codex/claude，minimax m3 不在白名单）
    # 注意：workboard normalizeExecution 要求 execution 必须有 model 字段，否则返回 undefined 被丢
    execution = None
    if not args.no_execution:
        execution = {
            "engine": args.engine,
            "mode": "autonomous",
            "status": "idle",
            "model": args.model,  # 默认 model 跟实际执行模型一致
        }

    if args.dry_run:
        return out({
            "ok": True,
            "dry_run": True,
            "would_create": {
                "title": args.title,
                "notes_preview": notes,
                "status": args.status,
                "priority": args.priority,
                "labels": labels,
                "agentId": args.assignee,
                "sessionKey": session_key,
                "execution": execution,
            },
        })

    result = await client.create_card(
        title=args.title,
        notes=notes,
        status=args.status,
        priority=args.priority,
        labels=labels,
        agent_id=args.assignee,
        session_key=session_key,
        execution=execution,
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
    p = sub.add_parser("create", help="创建卡片（任务发布，--assignee 必填）")
    p.add_argument("--title", required=True, help="卡片标题")
    # 结构化任务参数（与 IM 派发模板一致，组装为 notes）
    p.add_argument("--task-desc", help="任务描述（→{{task_desc}}）")
    p.add_argument("--agent-role", help="代理角色（→{{agent_role}}，如 psychologist / writer）")
    p.add_argument("--subtask", help="TODO.md 子任务名（→{{subtask}}）")
    p.add_argument("--goal", help="任务目标（→{{任务目标}}）")
    p.add_argument("--constraints", help="任务约束（→{{任务约束}}）")
    p.add_argument("--input-file", help="输入文件路径（→{{输入文件}}）")
    p.add_argument("--output-file", help="输出文件路径（→{{输出文件}}）")
    p.add_argument("--feedback", help="反馈说明（→{{反馈}}）")
    p.add_argument("--notes", help="【可选覆盖】直接指定 notes，跳过模板组装")
    p.add_argument("--status", choices=sorted(VALID_STATUSES), default="backlog", help="初始状态（默认 backlog/待办池）")
    p.add_argument("--priority", choices=sorted(VALID_PRIORITIES), default="normal", help="优先级（默认 normal）")
    p.add_argument("--labels", help="标签，逗号分隔（如 ch12,文献检索）")
    p.add_argument("--assignee", required=True, help="【必填】指派给 agent（如 psychologist / writer）")
    p.add_argument("--engine", default="codex", choices=["codex", "claude"], help="execution.engine（workboard 白名单，默认 codex；Dashboard “代理”字段驱动）")
    p.add_argument("--model", default="minimax/MiniMax-M3", help="execution.model（workboard 必填，默认 minimax/MiniMax-M3 跟随实际执行模型）")
    p.add_argument("--no-session", action="store_true", help="不联动设 sessionKey（默认会设 agent:<assignee>:main）")
    p.add_argument("--no-execution", action="store_true", help="不联动设 execution.engine（默认会设 codex）")
    p.add_argument("--dry-run", action="store_true", help="仅预览 notes，不实际创建")
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
