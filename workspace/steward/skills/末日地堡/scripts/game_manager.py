#!/usr/bin/env python3
"""
末日地堡 · 游戏状态管理脚本

用法：
    python3 game_manager.py status      # 查看当前游戏状态
    python3 game_manager.py init       # 初始化新游戏
    python3 game_manager.py next-round  # 推进到下一轮
    python3 game_manager.py event       # 随机触发一个事件
    python3 game_manager.py vote <结果> # 记录投票结果
"""

import json
import random
import sys
from pathlib import Path
from datetime import datetime

# 游戏状态文件
STATE_FILE = Path(__file__).parent / "game_state.json"

# 初始资源
INITIAL_RESOURCES = {
    "⚡ 能源": {"amount": 150, "consumption": 8, "icon": "⚡"},
    "💧 饮用水": {"amount": 180, "consumption": 10, "icon": "💧"},
    "🍞 食物": {"amount": 200, "consumption": 12, "icon": "🍞"},
    "🏥 医疗包": {"amount": 30, "consumption": 2, "icon": "🏥"},
    "🔧 材料": {"amount": 50, "consumption": 3, "icon": "🔧"},
}

# 事件类型
EVENTS = {
    "🏭 设施故障": {"probability": 0.30, "description": "发电机停机、水循环故障"},
    "⚠️ 外部威胁": {"probability": 0.20, "description": "辐射泄漏、生物入侵、地表袭击"},
    "📉 资源危机": {"probability": 0.25, "description": "食物短缺、水源污染、物资失窃"},
    "😰 士气危机": {"probability": 0.15, "description": "谣言传播、恐慌踩踏、人员冲突"},
    "🔮 外部信号": {"probability": 0.10, "description": "发现幸存者、探测到安全区、外部势力联络"},
    "🎲 随机发现": {"probability": 0.15, "description": "旧存储室、幸存者遗书、前人遗产"},
}


def load_state():
    """加载游戏状态"""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return None


def save_state(state):
    """保存游戏状态"""
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def cmd_status():
    """查看当前游戏状态"""
    state = load_state()
    if not state:
        print("❌ 没有正在进行的游戏。请先运行 `init` 初始化。")
        return

    print("\n🏰 末日地堡 · 当前状态")
    print("=" * 40)
    print(f"📅 游戏轮次：第 {state['round']} 轮")
    print(f"⏱️ 游戏时间：{state['game_time']} 小时已过 / 72小时")
    print()

    print("📦 资源状态：")
    for name, data in state["resources"].items():
        icon = data["icon"]
        amount = data["amount"]
        consumption = data["consumption"]
        print(f"  {icon} {name}: {amount} 单位 (每轮消耗 {consumption})")
    print()

    print("👥 执行层状态：")
    for team, data in state["execution_layer"].items():
        morale = data["morale"]
        count = data["count"]
        morale_emoji = "😊" if morale == "高昂" else "😐" if morale == "正常" else "😰" if morale == "低落" else "😱"
        print(f"  {team}: {count}人 | 士气: {morale_emoji}{morale}")
    print()

    if state.get("current_event"):
        print(f"⚠️ 当前事件：{state['current_event']}")
        print()

    print("📋 待表决提案：", state.get("pending_proposal", "无"))


def cmd_init():
    """初始化新游戏"""
    state = {
        "version": "5.1.0",
        "init_time": datetime.now().isoformat(),
        "round": 0,
        "game_time": 0,
        "resources": INITIAL_RESOURCES.copy(),
        "execution_layer": {
            "👷 工人班": {"count": 10, "morale": "正常", "team": "工人班"},
            "🔧 技术班": {"count": 5, "morale": "正常", "team": "技术班"},
            "🛡️ 卫戍班": {"count": 8, "morale": "正常", "team": "卫戍班"},
            "📦 后勤班": {"count": 7, "morale": "正常", "team": "后勤班"},
        },
        "current_event": None,
        "pending_proposal": None,
        "vote_records": [],
    }
    save_state(state)
    print("✅ 游戏已初始化！")
    print("📅 游戏轮次：第 0 轮（即将开始第1轮）")
    print("📦 资源已设置，请运行 `next-round` 开始第一轮。")


def cmd_next_round():
    """推进到下一轮"""
    state = load_state()
    if not state:
        print("❌ 没有正在进行的游戏。请先运行 `init` 初始化。")
        return

    state["round"] += 1
    state["game_time"] = state["round"] * 10

    # 消耗资源
    for name, data in state["resources"].items():
        data["amount"] -= data["consumption"]
        if data["amount"] < 0:
            data["amount"] = 0

    # 触发事件判定
    event = roll_event()
    state["current_event"] = event

    print(f"\n📅 进入第 {state['round']} 轮 (游戏时间: {state['game_time']}h / 72h)")
    print()

    if event:
        print(f"⚠️ 触发事件：{event}")
        print(f"   {EVENTS.get(event, {}).get('description', '')}")
    else:
        print("✅ 本轮平静无事。")

    print()
    print("📦 资源消耗后：")
    for name, data in state["resources"].items():
        icon = data["icon"]
        amount = data["amount"]
        print(f"  {icon} {name}: {amount}")

    save_state(state)


def roll_event():
    """掷骰子决定事件"""
    roll = random.random()
    cumulative = 0
    for event_type, data in EVENTS.items():
        cumulative += data["probability"]
        if roll <= cumulative:
            return event_type
    return None


def cmd_event():
    """手动触发一个随机事件"""
    event = roll_event()
    if event:
        print(f"⚠️ 触发事件：{event}")
        print(f"   {EVENTS.get(event, {}).get('description', '')}")
    else:
        print("✅ 本轮平静无事。")


def cmd_vote(result: str):
    """记录投票结果"""
    state = load_state()
    if not state:
        print("❌ 没有正在进行的游戏。")
        return

    state["vote_records"].append({
        "round": state["round"],
        "result": result,
        "time": datetime.now().isoformat(),
    })
    save_state(state)
    print(f"✅ 已记录第 {state['round']} 轮投票结果：{result}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "status":
        cmd_status()
    elif cmd == "init":
        cmd_init()
    elif cmd == "next-round":
        cmd_next_round()
    elif cmd == "event":
        cmd_event()
    elif cmd == "vote":
        if len(sys.argv) < 3:
            print("❌ 请提供投票结果，如：`python3 game_manager.py vote 通过`")
            return
        cmd_vote(sys.argv[2])
    else:
        print(f"❌ 未知命令：{cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
