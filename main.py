import random
from datetime import datetime, timezone

import yfinance as yf
import mplfinance as mpf
from PIL import Image, ImageDraw, ImageFont, ImageOps

TICKERS = {
    "^NSEI": {
        "name": "NIFTY 50",
        "hashtags": "#NIFTY50 #NIFTY #IndianMarkets #StockMarket #Trading",
    },
    "^NSEBANK": {
        "name": "BANK NIFTY",
        "hashtags": "#BANKNIFTY #NIFTY #IndianMarkets #StockMarket #Trading",
    },
}

OUTPUT_IMAGE = "post.png"
OUTPUT_CHART = "chart.png"
OUTPUT_CAPTION = "caption.txt"


def download_market_data(ticker: str):
    data = yf.download(
        ticker,
        period="5d",
        interval="15m",
        auto_adjust=True,
        progress=False,
    )

    if data is None or data.empty:
        raise RuntimeError(f"No market data returned for {ticker}")

    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise RuntimeError(f"Market data is missing columns: {', '.join(missing)}")

    data = data[required].apply(lambda col: col.astype(float)).dropna()

    if len(data) < 20:
        raise RuntimeError(f"Not enough market bars for {ticker}: {len(data)}")

    return data


def build_caption(symbol: str, data):
    info = TICKERS[symbol]
    close = float(data["Close"].iloc[-1])
    previous_close = float(data["Close"].iloc[-2])
    change = close - previous_close
    change_pct = (change / previous_close) * 100 if previous_close else 0.0

    ma5 = float(data["Close"].rolling(5).mean().iloc[-1])
    ma10 = float(data["Close"].rolling(10).mean().iloc[-1])

    if close > ma5 > ma10:
        signal = "Short-term momentum is bullish"
    elif close < ma5 < ma10:
        signal = "Short-term momentum is bearish"
    else:
        signal = "Short-term momentum is mixed"

    direction = "up" if change >= 0 else "down"
    timestamp = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    caption = (
        f"📊 {info['name']} Market Update\n\n"
        f"Last: {close:,.2f}\n"
        f"Move: {change:+,.2f} ({change_pct:+.2f}%)\n"
        f"{signal}.\n\n"
        f"Market snapshot generated {timestamp}.\n\n"
        f"{info['hashtags']}"
    )

    overlay = f"{info['name']} • {direction.upper()} {change_pct:+.2f}%"
    return caption, overlay


def create_chart(data, overlay: str):
    mpf.plot(
        data,
        type="candle",
        style="charles",
        volume=True,
        mav=(5, 10),
        figsize=(12, 10),
        savefig=dict(fname=OUTPUT_CHART, dpi=140, bbox_inches="tight"),
    )

    chart = Image.open(OUTPUT_CHART).convert("RGB")
    canvas = Image.new("RGB", (1080, 1080), "black")
    fitted = ImageOps.contain(chart, (1040, 1040))
    canvas.paste(fitted, ((1080 - fitted.width) // 2, (1080 - fitted.height) // 2))

    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    try:
        font = ImageFont.truetype(font_path, 44)
    except OSError:
        font = ImageFont.load_default()

    draw.rounded_rectangle((30, 25, 1050, 95), radius=18, fill=(0, 0, 0))
    draw.text((55, 43), overlay, fill="white", font=font)

    canvas.save(OUTPUT_IMAGE, format="JPEG", quality=92, optimize=True)


def main():
    symbol = random.choice(list(TICKERS))
    data = download_market_data(symbol)
    caption, overlay = build_caption(symbol, data)

    create_chart(data, overlay)

    with open(OUTPUT_CAPTION, "w", encoding="utf-8") as handle:
        handle.write(caption + "\n")

    print(f"Generated {OUTPUT_IMAGE}, {OUTPUT_CAPTION} for {TICKERS[symbol]['name']}")
    print(caption)


if __name__ == "__main__":
    main()
