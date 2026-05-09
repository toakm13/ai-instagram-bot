import os
import random
import yfinance as yf
import mplfinance as mpf
from PIL import Image, ImageDraw, ImageFont

# =========================
# SETTINGS
# =========================

ticker = random.choice(["^NSEI", "^NSEBANK"])

headlines = [
    "NIFTY Showing Strong Momentum",
    "BANKNIFTY Near Breakout Zone",
    "Markets May Stay Volatile Today",
    "Traders Watching Key Resistance",
    "Bullish Momentum Building Up",
]

caption = random.choice(headlines)

# =========================
# DOWNLOAD MARKET DATA
# =========================

data = yf.download(
    ticker,
    period="5d",
    interval="15m",
    auto_adjust=True
)

# Fix dataframe structure
data.columns = data.columns.get_level_values(0)

# Convert all to float
data = data.astype(float)

# Remove empty rows
data.dropna(inplace=True)

# =========================
# CREATE CHART
# =========================

chart_file = "chart.png"

mpf.plot(
    data,
    type="candle",
    style="charles",
    volume=True,
    mav=(5, 10),
    savefig=chart_file
)

# =========================
# CREATE INSTAGRAM POST IMAGE
# =========================

img = Image.open(chart_file)

# Resize for Instagram Reel
img = img.resize((1080, 1920))

draw = ImageDraw.Draw(img)

# Font
try:
    font = ImageFont.truetype("arial.ttf", 60)
except:
    font = ImageFont.load_default()

# Draw text
draw.text(
    (50, 100),
    caption,
    fill="white",
    font=font
)

# Save final image
final_image = "post.png"
img.save(final_image)

print("Post image created successfully.")

# =========================
# CREATE REEL VIDEO
# =========================

os.system(
    f'ffmpeg -loop 1 -i {final_image} -c:v libx264 '
    f'-t 6 -pix_fmt yuv420p -vf "scale=1080:1920" reel.mp4 -y'
)

print("Reel video created successfully.")

# =========================
# INSTAGRAM AUTO POST
# =========================

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

video_url = "https://raw.githubusercontent.com/toakm13/ai-instagram-bot/main/reel.mp4"

create_url = f"https://graph.facebook.com/v25.0/{IG_USER_ID}/media"

create_payload = {
    "media_type": "REELS",
    "video_url": video_url,
    "caption": caption,
    "access_token": PAGE_ACCESS_TOKEN
}

response = requests.post(create_url, data=create_payload)

print(response.text)
