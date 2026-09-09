import subprocess
from pathlib import Path

INPUT = Path("post.png")
OUTPUT = Path("reel.mp4")


def main():
    if not INPUT.exists():
        raise RuntimeError(f"{INPUT} does not exist. Run main.py first.")

    command = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(INPUT),
        "-t", "6",
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
        "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(OUTPUT),
    ]

    subprocess.run(command, check=True)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
