import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PRICES_FILE = DATA_DIR / "prices.csv"
SYMBOLS_FILE = "symbols.txt"

DAYS = 200

def load_symbols():
    with open(SYMBOLS_FILE) as f:
        return [s.strip() for s in f if s.strip()]

def fetch_symbol(symbol):
    end = datetime.now()
    start = end - timedelta(days=DAYS * 2)  # buffer for holidays

    df = yf.download(
        symbol,
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
        progress=False,
        auto_adjust=False
    )

    if df.empty:
        print(f"⚠️ No data: {symbol}")
        return None

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
    df = df[["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]]

    return df.tail(200)

def main():
    symbols = load_symbols()
    all_rows = []

    for symbol in symbols:
        print(f"Fetching {symbol}")
        df = fetch_symbol(symbol)
        if df is not None:
            all_rows.append(df)

    if not all_rows:
        raise RuntimeError("❌ No data fetched for any symbol")

    final_df = pd.concat(all_rows, ignore_index=True)

    final_df.to_csv(PRICES_FILE, index=False)
    print(f"✅ Saved {len(final_df)} rows to {PRICES_FILE}")

if __name__ == "__main__":
    main()
