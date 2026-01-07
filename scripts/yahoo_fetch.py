import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# === CONFIG ===
SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

OUT_FILE = "data/prices.csv"
DAYS = "200d"
SLEEP_SECONDS = 2   # critical to avoid 429

def fetch_symbol(symbol):
    print(f"Fetching {symbol}")
    df = yf.download(
        symbol,
        period=DAYS,
        interval="1d",
        progress=False,
        auto_adjust=False
    )

    if df.empty:
        print(f"⚠️ No data for {symbol}")
        return None

    df = df.reset_index()
    df["Symbol"] = symbol

    return df[[
        "Date", "Symbol",
        "Open", "High", "Low", "Close", "Volume"
    ]]

def main():
    all_rows = []

    for sym in SYMBOLS:
        data = fetch_symbol(sym)
        if data is not None:
            all_rows.append(data)
        time.sleep(SLEEP_SECONDS)

    if not all_rows:
        raise RuntimeError("❌ No data fetched from Yahoo")

    final_df = pd.concat(all_rows, ignore_index=True)
    final_df.sort_values(["Symbol", "Date"], inplace=True)

    final_df.to_csv(OUT_FILE, index=False)
    print(f"✅ Saved {len(final_df)} rows to {OUT_FILE}")

if __name__ == "__main__":
    main()
