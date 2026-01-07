import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import datetime

# ---------------- CONFIG ----------------
SYMBOLS_FILE = "data/symbols.txt"
OUTPUT_FILE = "data/prices.csv"
DAYS = 220  # ~200 trading days buffer
# ----------------------------------------


def load_symbols():
    if not Path(SYMBOLS_FILE).exists():
        raise FileNotFoundError(f"Missing symbols file: {SYMBOLS_FILE}")

    with open(SYMBOLS_FILE) as f:
        symbols = [s.strip() for s in f if s.strip()]

    if not symbols:
        raise RuntimeError("symbols.txt is empty")

    return symbols


def fetch_symbol(symbol):
    try:
        df = yf.download(
            symbol,
            period=f"{DAYS}d",
            interval="1d",
            progress=False,
            auto_adjust=False,
            threads=False,
        )

        if df.empty:
            print(f"⚠️ No data: {symbol}")
            return None

        df = df.reset_index()
        df["Symbol"] = symbol

        df = df[["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]]
        return df

    except Exception as e:
        print(f"❌ Failed {symbol}: {e}")
        return None


def main():
    print("🚀 Yahoo fetch started")

    Path("data").mkdir(exist_ok=True)

    symbols = load_symbols()
    print(f"📄 Symbols loaded: {len(symbols)}")

    frames = []

    for i, sym in enumerate(symbols, 1):
        print(f"[{i}/{len(symbols)}] Fetching {sym}")
        df = fetch_symbol(sym)
        if df is not None:
            frames.append(df)

    if not frames:
        raise RuntimeError("No data fetched for any symbol")

    new_data = pd.concat(frames, ignore_index=True)

    # Merge with existing CSV (if exists)
    if Path(OUTPUT_FILE).exists():
        old = pd.read_csv(OUTPUT_FILE)
        combined = pd.concat([old, new_data], ignore_index=True)
    else:
        combined = new_data

    # Clean
    combined["Date"] = pd.to_datetime(combined["Date"])
    combined = combined.drop_duplicates(subset=["Date", "Symbol"])
    combined = combined.sort_values(["Symbol", "Date"])

    # Keep last ~200 days per symbol
    combined = (
        combined.groupby("Symbol", group_keys=False)
        .tail(200)
    )

    combined.to_csv(OUTPUT_FILE, index=False)

    print("✅ prices.csv updated successfully")


if __name__ == "__main__":
    main()
