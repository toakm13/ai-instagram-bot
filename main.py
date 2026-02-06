import yfinance as yf
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


# ----------------------------
# MARKET DATA
# ----------------------------
def fetch_market_data():
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="5d")

    if len(data) < 2:
        return None

    close = round(data["Close"].iloc[-1], 2)
    prev = round(data["Close"].iloc[-2], 2)
    change = round(close - prev, 2)
    pct = round((change / prev) * 100, 2)

    snapshot = (
        "📊 Market Snapshot\n\n"
        f"NIFTY 50 closed {'up' if change > 0 else 'down'} today.\n"
        f"Close: {close} | Change: {change} ({pct}%)\n\n"
        "Markets continue to react to global and domestic cues.\n"
        "This is not investment advice."
    )

    return snapshot


# ----------------------------
# MEME TEXT
# ----------------------------
def generate_meme_text():
    memes = [
        "Investor routine: check chart → sigh → repeat 📉📈",
        "Market opens. Hope opens. Market closes. Hope closes.",
        "Long term investor since yesterday.",
        "Portfolio red but conviction green.",
        "Buy high. Sell low. Regret forever."
    ]
    return "😂 Meme Text\n\n" + memes[datetime.now().day % len(memes)]


# ----------------------------
# IMAGE CREATION (SAFE)
# ----------------------------
def create_post_image(text, filename):
    img = Image.new("RGB", (1080, 1080), (18, 18, 18))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 44)
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

    y = 250
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        draw.text(((1080 - w) / 2, y), line, fill="white", font=font)
        y += h + 14

    draw.text((30, 1030), "@yourpage", fill="gray", font=font)

    img.save(filename)
    print(f"🖼 Image created: {filename}")


# ----------------------------
# MAIN ENGINE
# ----------------------------
def main():
    print("🚀 Bot engine running\n")

    market_text = fetch_market_data()
    meme_text = generate_meme_text()

    if not market_text:
        print("❌ Market data unavailable")
        return

    print(market_text)
    print()
    print(meme_text)

    today = datetime.now().strftime("%Y-%m-%d")
    image_text = market_text + "\n\n" + meme_text

    create_post_image(image_text, f"post_{today}.png")


# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    main()
