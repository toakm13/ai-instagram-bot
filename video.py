from moviepy.editor import ImageClip

image_file = "post.png"

clip = (
    ImageClip(image_file)
    .set_duration(6)
    .resize((1080, 1920))
)

clip.write_videofile(
    "reel.mp4",
    fps=24
)

print("Reel created successfully.")
