import yfinance as yf
import feedparser

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
            print(f"{name}: Not enough data available\n")
            continue

        closes = data["Close"].dropna()

        if len(closes) < 2:
            print(f"{name}: Insufficient closing data\n")
            continue

        prev_close = closes.iloc[-2]
        last_close = closes.iloc[-1]
        change_pct = ((last_close - prev_close) / prev_close) * 100

        print(f"{name}")
        print(f"Previous Close: {prev_close:.2f}")
        print(f"Current Close: {last_close:.2f}")
        print(f"Change: {change_pct:.2f}%\n")


# -------------------------
# FINANCIAL NEWS
# -------------------------
NEWS_FEEDS = [
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.reuters.com/rssFeed/marketsNews"
]

BIG_KEYWORDS = [
    "rbi", "rate", "policy", "inflation", "interest",
    "budget", "crash", "surge", "record",
    "ban", "approval", "ipo"
]

def fetch_financial_news():
    print("📰 Latest Financial News\n")
    big_news_found = False

    for feed_url in NEWS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:5]:
            title = entry.title.lower()
            print("•", entry.title)

            if any(keyword in title for keyword in BIG_KEYWORDS):
                big_news_found = True

        print()

    if big_news_found:
        print("🚨 BIG ANNOUNCEMENT DETECTED\n")
    else:
        print("ℹ️ No major announcement today\n")


# -------------------------
# MAIN ENTRY
# -------------------------
def
