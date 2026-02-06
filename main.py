import yfinance as yf
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# -------------------------
# FETCH MARKET DATA
# -------------------------
def fetch_market_data():
    ticker = yf.Ticker("^NSEI")  # NIFTY 50
    data = ticker.history(period="5d")

    if data.empty or len(data) < 2:
        return None

    last_close = round(data["Close"].iloc[-1], 2)
    prev_close = round(data["Close"].iloc[-2], 2)
    change = round(last_close - prev_close, 2)
    pct = round((change / prev_close) * 100, 2)

    return {
        "index": "NIFTY 50",
        "last": last_close,
        "change": change,
        "pct": pct
    }

# -------------------------
# GENERATE TEXT CONTENT
# -------------------------
def generate_captions(market):
    direction = "up" if market["change"] > 0 else "down"

    market_caption = (
        f"{market['index']} closed {direction} today.\n"
        f"Close: {market['last']} | Change: {market['change']} ({market['pct']}%)\n\n"
        "Markets continue to react to global and domestic cues.\n"
        "This is not investment advice."
    )

    meme_text = "Investor routine: check chart → sigh → repeat 📉📈"

    return market_caption, meme_text

# -------------------------
# CREATE IMAGE WITH WATERMARK
# -------------------------
def create_post_image(text, filename):
    img = Image.new("RGB", (1080, 1080), color=(18, 18, 18))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 46)
    except:
        font = ImageFont.load_default()

    max_width = 900
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    y = 300
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        draw.text(((1080 - w) / 2, y), line, fill="white", font=font)
        y += h + 14

    # watermark
    draw.text((30, 1020), "@yourpage", fill="gray", font=font)

    img.save(filename)
    print(f"🖼 Image created: {filename}")

    y = 300
    for line in lines:
        w, h = draw.textsize(line, font=font)
        draw.text(((1080 - w) / 2, y), line, fill="white", font=font)
        y += h + 12

    # Watermark
    draw.text((30, 1020), "@yourpage", fill="gray", font=font)

    img.save(filename)
    print(f"🖼 Image created: {filename}")

# -------------------------
# MAIN CONTROLLER
# -------------------------
def main():
    print("🚀 Bot engine running")

    market = fetch_market_data()
    if not market:
        print("⚠️ Market data unavailable")
        return

    caption, meme = generate_captions(market)

    print("\n📊 Market Snapshot")
    print(caption)

    print("\n😂 Meme Text")
    print(meme)

    today = datetime.now().strftime("%Y-%m-%d")
    image_text = f"{market['index']} {market['pct']}%\n{meme}"

    create_post_image(image_text, f"post_{today}.png")

# -------------------------
# ENTRY POINT
# -------------------------
if __name__ == "__main__":
    main()
