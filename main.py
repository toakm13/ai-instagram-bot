import yfinance as yf
import feedparser
import random

# -------------------------
# MARKET DATA
# -------------------------
def fetch_market_data():
    indices = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "NIFTY BANK": "^NSEBANK"
    }

    print("📊 Market Snapshot\n")

    for name, symbol in indices.items():
        data = yf.Ticker(symbol).history(period="5d")

        if data is None or len(data) < 2:
            print(f"{name}: Not enough data\n")
            continue

        closes = data["Close"].dropna()
        if len(closes) < 2:
            print(f"{name}: Insufficient data\n")
            continue

        prev_close = closes.iloc[-2]
        last_close = closes.iloc[-1]
        change = ((last_close - prev_close) / prev_close) * 100

        print(f"{name}")
        print(f"Previous Close: {prev_close:.2f}")
        print(f"Current Close: {last_close:.2f}")
        print(f"Change: {change:.2f}%\n")


# -------------------------
# FINANCIAL NEWS
# -------------------------
NEWS_FEEDS = [
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
]

BIG_KEYWORDS = [
    "rbi", "rate", "policy", "inflation", "interest",
    "budget", "crash", "surge", "record", "ipo"
]

def fetch_financial_news():
    print("📰 Market News\n")
    big_news = False

    for url in NEWS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            title = entry.title
            print("•", title)
            if any(word in title.lower() for word in BIG_KEYWORDS):
                big_news = True

    print()
    return big_news


# -------------------------
# CONTENT GENERATION
# -------------------------
def generate_market_caption(trend):
    captions = [
        "Markets ended the session with marginal gains amid mixed global cues.",
        "A steady session as benchmarks closed with limited movement.",
        "Markets traded cautiously today as investors tracked macro signals."
    ]
    return random.choice(captions)


def generate_news_caption(is_big):
    if is_big:
        return "🚨 Big market-moving developments today. Staying informed is key."
    return "📰 A calm news day with no major market shocks."


def generate_meme_text():
    memes = [
        "That moment when the market finally moves after doing nothing all day 😅",
        "Investor routine: check chart → sigh → repeat 📉",
        "Markets teaching patience better than meditation 🧘‍♂️",
        "One candle and emotions go wild 📊"
    ]
    return random.choice(memes)


# -------------------------
# MAIN
# -------------------------
def main():
    print("🚀 Bot engine running\n")

    fetch_market_data()
    big_news = fetch_financial_news()

    print("✍️ Generated Content\n")

    print("Market Caption:")
    print(generate_market_caption("flat"))

    print("\nNews Caption:")
    print(generate_news_caption(big_news))

    print("\nMeme Text:")
    print(generate_meme_text())


if __name__ == "__main__":
    main()
