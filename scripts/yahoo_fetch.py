import yfinance as yf
import pandas as pd
import time
from pathlib import Path

# ================= CONFIG =================
SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

DAYS = "200d"
SLEEP_SECONDS = 2
OUT_FILE = Path("data/prices.csv")

# ==========================================

def fetch_one(symbol: str) -> pd.DataFrame:
    print(f"Fetching {symbol}")

    df = yf.Ticker(symbol).history(
        period=DAYS,
        interval="1d",
        auto_adjust=False
    )

    if df.empty:
        print(f"⚠️ No data for {symbol}")
        return pd.DataFrame()

    df = df.reset_index()

    df = df.rename(columns={
        "Date": "Date",
        "Open": "Open",
        "High": "High",
        "Low": "Low",
        "Close": "Close",
        "Volume": "Volume"
    })

    df["Symbol"] = symbol

    return df[[
        "Date", "Symbol", "Open", "High", "Low", "Close", "Volume"
    ]]


def main():
    Path("data").mkdir(exist_ok=True)

    frames = []

    for sym in SYMBOLS:
        df = fetch_one(sym)
        if not df.empty:
            frames.append(df)
        time.sleep(SLEEP_SECONDS)

    if not frames:
        raise RuntimeError("❌ No data fetched from Yahoo")

    final = pd.concat(frames, axis=0, ignore_index=True)

    final["Date"] = pd.to_datetime(final["Date"]).dt.date
    final = final.sort_values(["Symbol", "Date"])

    final.to_csv(OUT_FILE, index=False)

    print(f"✅ Saved {len(final)} rows to {OUT_FILE}")


if __name__ == "__main__":
    main()
