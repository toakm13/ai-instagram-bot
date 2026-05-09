from moviepy.editor import ImageClip
from datetime import datetime

image_file = f"post_{datetime.now().strftime('%Y-%m-%d')}.png"

clip = (
    ImageClip(image_file)
    .set_duration(6)
    .resize(height=1920)
)

clip.write_videofile(
    "reel.mp4",
    fps=24,
    codec="libx264"
)

print("Reel video created")
