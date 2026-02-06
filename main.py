import yfinance as yf
import random
from datetime import date
from PIL import Image, ImageDraw, ImageFont


# -----------------------------
# FETCH MARKET DATA (NIFTY 50)
# -----------------------------
def fetch_market_data():
    ticker = yf.Ticker("^NSEI")
    data = ticker.history(period="5d")

    if len(data) < 2:
        return None

    close_today = round(data["Close"].iloc[-1], 2)
    close_yesterday = round(data["Close"].iloc[-2], 2)
    change = round(close_today - close_yesterday, 2)
    pct_change = round((change / close_yesterday) * 100, 2)

    return close_today, change, pct_change


# -----------------------------
# GENERATE TEXT CONTENT
# -----------------------------
def generate_market_text(close, change, pct):
    direction = "up" if change >= 0 else "down"

    return (
        f"📊 Market Snapshot\n\n"
        f"NIFTY 50 closed {direction} today.\n"
        f"Close: {close}\n"
        f"Change: {change} ({pct}%)\n\n"
        f"Markets continue to react to global and domestic cues.\n"
        f"This is not investment advice."
    )


def generate_meme_text():
    memes = [
        "Investor routine:\ncheck chart → sigh → repeat 😮‍💨📉",
        "Market falls 1%\nMe: long term bro 😅",
        "Portfolio red\nConfidence green 💀",
    ]
    return random.choice(memes)


def generate_market_caption():
    captions = [
        "Markets ended mixed today 📊\nVolatility stays.\n\nNot investment advice.",
        "Choppy session in Dalal Street today.\nPatience matters 🧠\n\nNot investment advice.",
        "Red. Green. Repeat 🔁\nThat’s markets.\n\nNot investment advice.",
    ]
    return random.choice(captions)


def generate_meme_caption():
    captions = [
        "Every investor ever 😅📉",
        "If pain had a chart 💀",
        "Market psychology 101 📊",
    ]
    return random.choice(captions)


def generate_hashtags():
    return (
        "#StockMarket #IndianMarkets #Nifty50 #TradingLife "
        "#Investing #FinanceMemes #MarketNews "
        "#DalalStreet #Wealth"
    )


# -----------------------------
# CREATE IMAGE POST
# -----------------------------
def create_post_image(text, filename):
    img = Image.new("RGB", (1080, 1080), color=(15, 15, 15))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    y = 120
    for line in text.split("\n"):
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((1080 - w) / 2, y), line, fill="white", font=font)
        y += 70

    # Watermark
    draw.text((30, 1020), "@yourpage", fill="gray", font=small_font)

    img.save(filename)
    print(f"🖼️ Image created: {filename}")


# -----------------------------
# MAIN ENGINE
# -----------------------------
def main():
    print("🚀 Bot engine running")

    market_data = fetch_market_data()
    if not market_data:
        print("❌ Market data unavailable")
        return

    close, change, pct = market_data

    market_text = generate_market_text(close, change, pct)
    meme_text = generate_meme_text()

    print("\n📊 Market Snapshot")
    print(market_text)

    print("\n😂 Meme Text")
    print(meme_text)

    today = date.today().isoformat()
    image_text = market_text + "\n\n😂 " + meme_text
    create_post_image(image_text, f"post_{today}.png")

    print("\n📌 Captions")
    print("Market Caption:")
    print(generate_market_caption())

    print("\nMeme Caption:")
    print(generate_meme_caption())

    print("\nHashtags:")
    print(generate_hashtags())


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()
