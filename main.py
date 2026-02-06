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
