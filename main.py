import yfinance as yf

def fetch_market_data():
    indices = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "NIFTY BANK": "^NSEBANK"
    }

    print("📊 Market Snapshot\n")

    for name, symbol in indices.items():
        data = yf.Ticker(symbol).history(period="2d")
        if len(data) >= 2:
            prev_close = data["Close"][-2]
            last_close = data["Close"][-1]
            change_pct = ((last_close - prev_close) / prev_close) * 100

            print(f"{name}")
            print(f"Previous Close: {prev_close:.2f}")
            print(f"Current Close: {last_close:.2f}")
            print(f"Change: {change_pct:.2f}%\n")

def main():
    print("🚀 Bot engine running\n")
    fetch_market_data()

if __name__ == "__main__":
    main()
