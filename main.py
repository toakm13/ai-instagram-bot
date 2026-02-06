import yfinance as yf
import random
from datetime import date
import feedparser
from PIL import Image, ImageDraw, ImageFont


# =====================================================
# MARKET DATA (NIFTY 50)
# =====================================================
def fetch_market_data():
    ticker = yf.Ticker("^NSEI")
    data = ticker.history(period="5d")

    if len(data) < 2:
        return None

    close_today = round(data["Close"].iloc[-1], 2)
    close_yesterday = round(data["Close"].iloc[-2], 2)
    change = round(close_today - close_yesterday, 2)
    pct_change = round((change / close_yesterday) * 100, 2)

    direction = "up" if change >= 0 else "down"

    snapshot = (
        f"📊 Market Snapshot\n\n"
        f"NIFTY 50 closed {direction} today.\n"
        f"Close: {close_today}\n"
        f"Change: {change} ({pct_change}%)\n\n"
        f"Markets continue to react to global and domestic cues.\n"
        f"This is not investment advice."
    )

    return snapshot


# =====================================================
# DAILY MARKET NEWS (RSS – FREE)
# =====================================================
NEWS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://www.reuters.com/rssFeed/marketsNews"
]

BIG_KEYWORDS = [
    "rbi", "interest rate", "policy", "inflation",
    "budget", "ipo", "fed", "crash", "surge", "approval"
]


def fetch_market_news():
    headlines = []
    big_news = False

    for url in NEWS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            title = entry.title.strip()
            headlines.append(title)

            if any(word in title.lower() for word in BIG_KEYWORDS):
                big_news = True

    return headlines[:5], big_news


def generate_news_caption(headlines, big_news):
    if not headlines:
        return "Quiet news day today. Markets moved without major triggers."

    intro = (
        "🚨 Big market updates today:\n"
        if big_news
        else "📰 Today’s market headlines:\n"
    )

    body = ""
    for h in headlines[:3]:
        body += f"• {h}\n"

    outro = "\nMarkets react, we observe.\nNot investment advice."

    return intro + body + outro


# =====================================================
# MEMES & CAPTIONS (VIRAL, NEUTRAL)
# =====================================================
def generate_meme_text():
    memes = [
        "Investor routine:\ncheck chart → sigh → repeat 😮‍💨📉",
        "Market falls 1%\nMe: long term bro 😅",
        "Portfolio red\nConfidence green 💀",
        "One candle and emotions change 📊",
    ]
    return random.choice(memes)


def generate_market_caption():
    captions = [
        "Markets ended mixed today 📊\nVolatility stays.\n\nNot investment advice.",
        "Choppy session on Dalal Street.\nPatience matters 🧠\n\nNot investment advice.",
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


# =====================================================
# IMAGE GENERATION WITH WATERMARK
# =====================================================
def create_post_image(text, filename):
    img = Image.new("RGB", (1080, 1080), color=(15, 15, 15))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 42)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 26)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    y = 120
    for line in text.split("\n"):
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((1080 - w) / 2, y), line, fill="white", font=font)
        y += 60

    draw.text((30, 1030), "@yourpage", fill="gray", font=small_font)

    img.save(filename)
    print(f"🖼 Image created: {filename}")


# =====================================================
# MAIN ENGINE
# =====================================================
def main():
    print("🚀 Bot engine running")

    # Market snapshot
    market_text = fetch_market_data()
    if not market_text:
        print("❌ Market data unavailable")
        return

    print("\n📊 Market Snapshot")
    print(market_text)

    # Meme
    meme_text = generate_meme_text()
    print("\n😂 Meme Text")
    print(meme_text)

    # Image
    today = date.today().isoformat()
    image_text = market_text + "\n\n😂 " + meme_text
    create_post_image(image_text, f"post_{today}.png")

    # News
    headlines, big_news = fetch_market_news()
    news_caption = generate_news_caption(headlines, big_news)

    print("\n📰 Daily News Recap")
    print(news_caption)

    # Captions & hashtags
    print("\n📌 Instagram Captions")
    print("Market Caption:")
    print(generate_market_caption())

    print("\nMeme Caption:")
    print(generate_meme_caption())

    print("\nHashtags:")
    print(generate_hashtags())


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    main()
