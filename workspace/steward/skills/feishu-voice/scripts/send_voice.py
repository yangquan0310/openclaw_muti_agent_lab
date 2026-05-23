#!/usr/bin/env python3
"""
飞书原生语音消息发送工具
将 MP3 转换为 OGG/Opus 并作为飞书语音消息气泡发送

用法:
    python3 send_voice.py <mp3_path> [open_id] [--duration DURATION] [--help]

示例:
    python3 send_voice.py /path/to/audio.mp3
    python3 send_voice.py /path/to/audio.mp3 ou_25cf20a1973aecc51f73d8e2800d7f7e
    python3 send_voice.py /path/to/audio.mp3 --duration 10000
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# 默认配置
DEFAULT_OPEN_ID = "ou_25cf20a1973aecc51f73d8e2800d7f7e"
TMP_DIR = "/tmp"


def convert_to_opus(mp3_path: str, output_path: str = None) -> tuple[str, int]:
    """
    将 MP3 转换为 OGG/Opus 格式
    返回: (output_path, duration_ms)
    """
    import json

    if output_path is None:
        output_path = os.path.join(TMP_DIR, f"voice_{os.getpid()}.ogg")

    # 获取音频时长
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", mp3_path],
        capture_output=True, text=True, check=True
    )
    duration_sec = float(json.loads(result.stdout)["format"]["duration"])
    duration_ms = int(duration_sec * 1000)

    # 转换为 OPUS in OGG
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", mp3_path,
            "-acodec", "libopus", "-ac", "1", "-ar", "16000",
            output_path
        ],
        capture_output=True, check=True
    )

    return output_path, duration_ms


def send_feishu_voice(audio_path: str, open_id: str = DEFAULT_OPEN_ID, duration_ms: int = None) -> dict:
    """
    发送飞书语音消息的完整流程
    使用 lark-cli 处理上传和发送（更简洁）

    Args:
        audio_path: MP3 文件路径
        open_id: 接收者 open_id（默认：老板）
        duration_ms: 音频时长（毫秒），不指定则自动从文件计算

    Returns:
        包含 message_id, chat_id 等信息的字典
    """
    # 1. 转换格式到源文件同一目录（lark-cli 需要相对路径）
    audio_dir = os.path.dirname(os.path.abspath(audio_path)) or "."
    audio_basename = os.path.basename(audio_path)
    # 转换后的文件与源文件同目录，后缀改为 .ogg
    opus_path = os.path.join(audio_dir, audio_basename.rsplit(".", 1)[0] + ".ogg")
    opus_path, calculated_duration = convert_to_opus(audio_path, opus_path)

    try:
        # 2. 使用 lark-cli 发送语音消息（从文件所在目录运行）
        # lark-cli 要求 --audio 使用相对路径
        orig_cwd = os.getcwd()
        try:
            os.chdir(audio_dir)
            result = subprocess.run(
                [
                    "lark-cli", "im", "+messages-send",
                    "--user-id", open_id,
                    "--audio", "./" + os.path.basename(opus_path)
                ],
                capture_output=True, text=True, check=True
            )
        finally:
            os.chdir(orig_cwd)

        import json
        output = result.stdout.strip()
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            # lark-cli 有时会输出非JSON（如警告）
            data = {"raw": output}

        if data.get("ok"):
            msg_data = data.get("data", {})
            print(f"✅ 语音消息发送成功: message_id={msg_data.get('message_id')}", file=sys.stderr)
            return msg_data
        else:
            error_msg = data.get("error", {}).get("message", output)
            raise RuntimeError(f"发送失败: {error_msg}")

    finally:
        # 清理临时文件
        if os.path.exists(opus_path):
            os.remove(opus_path)


def main():
    parser = argparse.ArgumentParser(
        description="飞书原生语音消息发送工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 send_voice.py audio.mp3
  python3 send_voice.py audio.mp3 ou_xxx --duration 10000
        """
    )
    parser.add_argument("audio_path", help="MP3 文件路径")
    parser.add_argument("open_id", nargs="?", default=DEFAULT_OPEN_ID, help=f"接收者 open_id（默认：{DEFAULT_OPEN_ID}）")
    parser.add_argument("--duration", "-d", type=int, dest="duration_ms", help="音频时长（毫秒）")

    args = parser.parse_args()

    if not os.path.exists(args.audio_path):
        print(f"❌ 文件不存在: {args.audio_path}", file=sys.stderr)
        sys.exit(1)

    try:
        result = send_feishu_voice(args.audio_path, args.open_id, args.duration_ms)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()