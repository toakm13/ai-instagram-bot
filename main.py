import feedparser

NEWS_FEEDS = [
    "https://www.moneycontrol.com/rss/latestnews.xml",
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.reuters.com/rssFeed/marketsNews"
]

BIG_KEYWORDS = [
    "rbi",
    "rate",
    "policy",
    "inflation",
    "interest",
    "budget",
    "crash",
    "surge",
    "record",
    "ban",
    "approval",
    "ipo"
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

def main():
    print("🚀 Bot engine running\n")
    fetch_market_data()
    fetch_financial_news()

if __name__ == "__main__":
    main()
