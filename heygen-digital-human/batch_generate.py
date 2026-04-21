"""
批量生成数字人视频
适用场景：客户提供多条文案，批量生产内容

使用方法：
  python batch_generate.py --input scripts.txt --avatar <id> --voice <id>

scripts.txt 格式（每行一条文案，用 --- 分隔多个视频）：
  这是第一个视频的文案内容。
  ---
  这是第二个视频的文案内容。
"""

import os
import sys
import argparse
from pathlib import Path
from heygen_client import generate_digital_human_video


def load_scripts(filepath: str) -> list[str]:
    """从文件加载文案列表"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    scripts = [s.strip() for s in content.split("---") if s.strip()]
    return scripts


def batch_generate(
    scripts: list[str],
    avatar_id: str,
    voice_id: str,
    output_dir: str = "output",
    quality: str = "1080p"
) -> list[str]:
    """批量生成视频"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    results = []

    for i, script in enumerate(scripts, 1):
        output_path = os.path.join(output_dir, f"video_{i:03d}.mp4")
        print(f"\n[{i}/{len(scripts)}] 生成第 {i} 个视频...")
        print(f"    文案预览: {script[:50]}...")

        try:
            path = generate_digital_human_video(
                script=script,
                avatar_id=avatar_id,
                voice_id=voice_id,
                output_path=output_path,
                quality=quality
            )
            results.append({"index": i, "status": "success", "path": path})
        except Exception as e:
            print(f"[✗] 第 {i} 个视频生成失败: {e}")
            results.append({"index": i, "status": "failed", "error": str(e)})

    # 汇总报告
    print("\n" + "="*50)
    print("批量生成完成")
    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "failed"]
    print(f"  成功: {len(success)}/{len(results)}")
    print(f"  失败: {len(failed)}/{len(results)}")
    if failed:
        print("  失败列表:")
        for r in failed:
            print(f"    第{r['index']}个: {r['error']}")

    return results


def main():
    parser = argparse.ArgumentParser(description="批量生成AI数字人视频")
    parser.add_argument("--input", required=True, help="文案文件路径（每条用 --- 分隔）")
    parser.add_argument("--avatar", required=True, help="数字人形象ID")
    parser.add_argument("--voice", required=True, help="配音ID")
    parser.add_argument("--output-dir", default="output", help="输出目录")
    parser.add_argument("--quality", default="1080p", choices=["720p", "1080p", "4k"])

    args = parser.parse_args()

    scripts = load_scripts(args.input)
    print(f"[+] 共加载 {len(scripts)} 条文案")

    batch_generate(
        scripts=scripts,
        avatar_id=args.avatar,
        voice_id=args.voice,
        output_dir=args.output_dir,
        quality=args.quality
    )


if __name__ == "__main__":
    main()
