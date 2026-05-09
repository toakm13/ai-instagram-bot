import yfinance as yf
import mplfinance as mpf
import pandas as pd
from PIL import Image, ImageDraw
from datetime import datetime

ticker = "^NSEI"

data = yf.download(ticker, period="5d", interval="15m")

latest_close = round(data["Close"].iloc[-1], 2)
previous_close = round(data["Close"].iloc[-2], 2)

change = round(latest_close - previous_close, 2)
pct_change = round((change / previous_close) * 100, 2)

chart_file = "chart.png"

mpf.plot(
    data.tail(50),
    type="candle",
    style="charles",
    volume=False,
    savefig=chart_file
)

chart = Image.open(chart_file).resize((900, 500))

img = Image.new("RGB", (1080, 1080), color=(10, 10, 10))
draw = ImageDraw.Draw(img)

img.paste(chart, (90, 120))

title = "NIFTY MARKET UPDATE"
price = f"NIFTY: {latest_close}"
movement = f"{change} ({pct_change}%)"

draw.text((90, 40), title, fill="white")
draw.text((90, 650), price, fill="white")

color = "green" if change >= 0 else "red"

draw.text((90, 720), movement, fill=color)

draw.text(
    (90, 850),
    "Discipline and risk management create consistency.",
    fill="orange"
)

filename = f"post_{datetime.now().strftime('%Y-%m-%d')}.png"

img.save(filename)

print(f"Saved {filename}")
