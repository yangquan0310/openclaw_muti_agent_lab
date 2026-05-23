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
import tempfile
from pathlib import Path

# 默认配置
DEFAULT_OPEN_ID = "ou_25cf20a1973aecc51f73d8e2800d7f7e"
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
TMP_DIR = "/tmp"


def get_env(key: str) -> str:
    """从环境变量或配置文件获取凭证"""
    if key == "APP_ID":
        # 从 openclaw.json 读取
        oc_path = Path.home() / ".openclaw" / "openclaw.json"
        if oc_path.exists():
            try:
                with open(oc_path) as f:
                    data = json.load(f)
                return data.get("channels", {}).get("feishu", {}).get("accounts", {}).get("steward", {}).get("appId", "")
            except Exception:
                pass
    elif key == "APP_SECRET":
        # 从 .env 读取
        env_path = Path.home() / ".openclaw" / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("FEISHU_STEWARD_APP_SECRET="):
                    return line.split("=", 1)[1].strip()
    return ""


def get_tenant_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token"""
    import urllib.request

    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    if data.get("code") != 0:
        raise RuntimeError(f"获取 token 失败: {data.get('msg')}")
    return data["tenant_access_token"]


def convert_to_opus(mp3_path: str, output_path: str = None) -> tuple[str, int]:
    """
    将 MP3 转换为 OGG/Opus 格式
    返回: (output_path, duration_ms)
    """
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


def upload_file(token: str, file_path: str, file_name: str, duration_ms: int) -> str:
    """
    上传文件到飞书，返回 file_key
    """
    import urllib.request
    import urllib.parse

    url = f"{FEISHU_API_BASE}/im/v1/files?file_type=opus"
    boundary = "----WebKitFormBoundary" + os.urandom(16).hex()

    # 读取文件
    with open(file_path, "rb") as f:
        file_data = f.read()
    file_size = len(file_data)

    # 构建 multipart body
    body_parts = [
        f'--{boundary}\r\nContent-Disposition: form-data; name="file_type"\r\n\r\nopus',
        f'--{boundary}\r\nContent-Disposition: form-data; name="file_name"\r\n\r\n{file_name}',
        f'--{boundary}\r\nContent-Disposition: form-data; name="duration"\r\n\r\n{duration_ms}',
        f'--{boundary}\r\nContent-Disposition: form-data; name="purpose"\r\n\r\nbot',
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{file_name}"\r\nContent-Type: audio/ogg\r\n\r\n',
    ]

    body = b""
    for part in body_parts:
        if part.endswith(b"\r\n\r\n"):
            body += part.encode() + file_data + b"\r\n"
        else:
            body += part.encode() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())

    if data.get("code") != 0:
        raise RuntimeError(f"上传文件失败: {data.get('msg')}")

    return data["data"]["file_key"]


def send_audio_message(token: str, open_id: str, file_key: str, duration_ms: int) -> dict:
    """
    发送语音消息
    """
    import urllib.request

    url = f"{FEISHU_API_BASE}/im/v1/messages?receive_id_type=open_id"
    payload = json.dumps({
        "receive_id": open_id,
        "msg_type": "audio",
        "content": json.dumps({
            "file_key": file_key,
            "duration": duration_ms
        })
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    if data.get("code") != 0:
        raise RuntimeError(f"发送消息失败: {data.get('msg')}")

    return data["data"]


def send_feishu_voice(audio_path: str, open_id: str = DEFAULT_OPEN_ID, duration_ms: int = None) -> dict:
    """
    发送飞书语音消息的完整流程

    Args:
        audio_path: MP3 文件路径
        open_id: 接收者 open_id（默认：老板）
        duration_ms: 音频时长（毫秒），不指定则自动从文件计算

    Returns:
        包含 message_id, chat_id 等信息的字典
    """
    app_id = get_env("APP_ID")
    app_secret = get_env("APP_SECRET")

    if not app_id or not app_secret:
        raise RuntimeError("无法获取飞书凭证，请检查配置")

    # 1. 转换格式
    opus_path, calculated_duration = convert_to_opus(audio_path)
    duration = duration_ms or calculated_duration

    try:
        # 2. 获取 token
        token = get_tenant_token(app_id, app_secret)

        # 3. 上传文件
        file_key = upload_file(
            token, opus_path,
            os.path.basename(audio_path).replace(".mp3", ".ogg"),
            duration
        )

        # 4. 发送语音消息
        result = send_audio_message(token, open_id, file_key, duration)

        print(f"✅ 语音消息发送成功: message_id={result.get('message_id')}", file=sys.stderr)
        return result

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