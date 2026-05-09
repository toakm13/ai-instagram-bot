import os
import random
import requests
import yfinance as yf
import mplfinance as mpf

from PIL import Image, ImageDraw, ImageFont

# =========================
# SETTINGS
# =========================

ticker = random.choice(["^NSEI", "^NSEBANK"])

headlines = [
    "NIFTY Showing Strong Momentum",
    "BANKNIFTY Near Key Resistance",
    "Markets Expected To Stay Volatile",
    "Bullish Momentum Building",
    "Traders Watching Breakout Levels"
]

caption = random.choice(headlines)

# =========================
# DOWNLOAD DATA
# =========================

data = yf.download(
    ticker,
    period="5d",
    interval="15m",
    auto_adjust=True
)

data.columns = data.columns.get_level_values(0)

data = data.astype(float)

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
# CREATE INSTAGRAM IMAGE
# =========================

img = Image.open(chart_file)

img = img.resize((1080, 1080))

draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 50)
except:
    font = ImageFont.load_default()

draw.text(
    (50, 80),
    caption,
    fill="white",
    font=font
)

final_image = "post.png"

img.save(final_image)

print("Instagram post image created.")

# =========================
# UPLOAD IMAGE TO FACEBOOK
# =========================

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")

url = f"https://graph.facebook.com/{FB_PAGE_ID}/photos"

files = {
    "source": open("post.png", "rb")
}

payload = {
    "caption": caption,
    "access_token": PAGE_ACCESS_TOKEN
}

response = requests.post(
    url,
    files=files,
    data=payload
)

print(response.text)

print("Posted successfully.")
