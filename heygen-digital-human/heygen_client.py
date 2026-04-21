"""
HeyGen AI数字人视频生成客户端
猪八戒服务：AI数字人定制

使用方法：
  python heygen_client.py --script "你的文案" --avatar "avatar_id" --voice "voice_id"

依赖：
  pip install requests python-dotenv
"""

import os
import sys
import time
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY", "")
BASE_URL = "https://api.heygen.com"


def list_avatars() -> list:
    """获取可用的数字人形象列表"""
    resp = requests.get(
        f"{BASE_URL}/v2/avatars",
        headers={"X-Api-Key": HEYGEN_API_KEY}
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", {}).get("avatars", [])


def list_voices(language: str = "zh") -> list:
    """获取可用的配音列表"""
    resp = requests.get(
        f"{BASE_URL}/v2/voices",
        headers={"X-Api-Key": HEYGEN_API_KEY}
    )
    resp.raise_for_status()
    data = resp.json()
    voices = data.get("data", {}).get("voices", [])
    # 过滤指定语言
    return [v for v in voices if v.get("language", "").startswith(language)]


def create_video(
    script: str,
    avatar_id: str,
    voice_id: str,
    width: int = 1920,
    height: int = 1080,
    title: str = "digital_human_video"
) -> str:
    """
    创建数字人视频任务
    返回 video_id
    """
    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id,
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": script,
                    "voice_id": voice_id
                },
                "background": {
                    "type": "color",
                    "value": "#FAFAFA"
                }
            }
        ],
        "dimension": {
            "width": width,
            "height": height
        },
        "title": title
    }

    resp = requests.post(
        f"{BASE_URL}/v2/video/generate",
        headers={
            "X-Api-Key": HEYGEN_API_KEY,
            "Content-Type": "application/json"
        },
        json=payload
    )
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["video_id"]


def wait_for_video(video_id: str, poll_interval: int = 10, timeout: int = 600) -> str:
    """
    轮询视频生成状态，完成后返回下载URL
    """
    print(f"[+] 视频生成中，video_id: {video_id}")
    elapsed = 0
    while elapsed < timeout:
        resp = requests.get(
            f"{BASE_URL}/v1/video_status.get?video_id={video_id}",
            headers={"X-Api-Key": HEYGEN_API_KEY}
        )
        resp.raise_for_status()
        data = resp.json()
        status = data["data"]["status"]
        print(f"    状态: {status} ({elapsed}s)")

        if status == "completed":
            return data["data"]["video_url"]
        elif status == "failed":
            raise RuntimeError(f"视频生成失败: {data['data'].get('error', '未知错误')}")

        time.sleep(poll_interval)
        elapsed += poll_interval

    raise TimeoutError(f"视频生成超时（{timeout}s）")


def download_video(url: str, output_path: str) -> None:
    """下载视频到本地"""
    print(f"[+] 下载视频: {output_path}")
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"[✓] 下载完成: {output_path}")


def generate_digital_human_video(
    script: str,
    avatar_id: str,
    voice_id: str,
    output_path: str = "output.mp4",
    quality: str = "1080p"
) -> str:
    """
    一键生成数字人视频（主入口）

    Args:
        script: 文案内容（建议500字以内）
        avatar_id: 数字人形象ID
        voice_id: 配音ID
        output_path: 输出文件路径
        quality: 视频质量 "1080p" 或 "4k"

    Returns:
        本地视频文件路径
    """
    if not HEYGEN_API_KEY:
        raise ValueError("未设置 HEYGEN_API_KEY，请在 .env 文件中配置")

    # 分辨率映射
    quality_map = {
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
        "720p": (1280, 720)
    }
    width, height = quality_map.get(quality, (1920, 1080))

    print(f"[+] 开始生成数字人视频")
    print(f"    文案长度: {len(script)} 字")
    print(f"    分辨率: {width}x{height}")

    # 1. 创建视频任务
    video_id = create_video(script, avatar_id, voice_id, width, height)

    # 2. 等待生成完成
    video_url = wait_for_video(video_id)

    # 3. 下载到本地
    download_video(video_url, output_path)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="HeyGen AI数字人视频生成工具")
    parser.add_argument("--script", required=True, help="文案内容")
    parser.add_argument("--avatar", default="", help="数字人形象ID（留空则列出可用形象）")
    parser.add_argument("--voice", default="", help="配音ID（留空则列出中文配音）")
    parser.add_argument("--output", default="output.mp4", help="输出文件路径")
    parser.add_argument("--quality", default="1080p", choices=["720p", "1080p", "4k"], help="视频质量")
    parser.add_argument("--list-avatars", action="store_true", help="列出可用数字人形象")
    parser.add_argument("--list-voices", action="store_true", help="列出中文配音")

    args = parser.parse_args()

    if args.list_avatars:
        print("[+] 可用数字人形象：")
        for a in list_avatars():
            print(f"  ID: {a['avatar_id']}  名称: {a.get('avatar_name', '')}")
        return

    if args.list_voices:
        print("[+] 可用中文配音：")
        for v in list_voices("zh"):
            print(f"  ID: {v['voice_id']}  名称: {v.get('display_name', '')}  性别: {v.get('gender', '')}")
        return

    if not args.avatar or not args.voice:
        print("错误：请指定 --avatar 和 --voice，或使用 --list-avatars / --list-voices 查看可用选项")
        sys.exit(1)

    output = generate_digital_human_video(
        script=args.script,
        avatar_id=args.avatar,
        voice_id=args.voice,
        output_path=args.output,
        quality=args.quality
    )
    print(f"\n[✓] 完成！视频已保存至: {output}")


if __name__ == "__main__":
    main()
