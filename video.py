from moviepy.editor import ImageClip
from datetime import datetime

# -----------------------------------
# DATE
# -----------------------------------

now = datetime.now()
date_text = now.strftime("%Y-%m-%d")

image_file = f"post_{date_text}.png"
video_file = f"reel_{date_text}.mp4"

# -----------------------------------
# CREATE REEL
# -----------------------------------

clip = (
    ImageClip(image_file)
    .set_duration(6)
    .resize((1080, 1920))
)

clip.write_videofile(
    video_file,
    fps=24,
    codec="libx264",
    audio=False,
)

print(f"✅ Reel created: {video_file}")
