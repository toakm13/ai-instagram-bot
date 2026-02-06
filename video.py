import subprocess
import glob
from datetime import date

def create_reel_from_image():
    today = date.today().isoformat()
    image_file = f"post_{today}.png"
    output_video = f"reel_{today}.mp4"

    # ffmpeg zoom & pan (Ken Burns effect)
    command = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image_file,
        "-vf",
        "scale=1080:1920,zoompan=z='min(zoom+0.0005,1.05)':d=150",
        "-t", "6",
        "-pix_fmt", "yuv420p",
        output_video
    ]

    subprocess.run(command, check=True)
    print(f"🎬 Reel created: {output_video}")

if __name__ == "__main__":
    create_reel_from_image()
