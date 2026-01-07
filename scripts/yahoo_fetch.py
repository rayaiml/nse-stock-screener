import pandas as pd
import yfinance as yf
from pathlib import Path

SYMBOLS_FILE = "data/symbols.txt"
OUTPUT_FILE = "data/prices.csv"
DAYS = 220


def load_symbols():
    with open(SYMBOLS_FILE) as f:
        return [s.strip() for s in f if s.strip()]


def fetch_symbol(symbol):
    try:
        df = yf.download(
            symbol,
            period=f"{DAYS}d",
            interval="1d",
            progress=False,
            threads=False,
        )

        if df is None or df.empty:
            print(f"⚠️ No data: {symbol}")
            return None

        # Normalize dataframe
        df = df.reset_index()

        # Yahoo sometimes returns "Datetime" instead of "Date"
        if "Date" not in df.columns:
            if "Datetime" in df.columns:
                df.rename(columns={"Datetime": "Date"}, inplace=True)
            else:
                print(f"⚠️ Date missing: {symbol}")
                return None

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
        raise RuntimeError("No valid stock data fetched")

    new_data = pd.concat(frames, ignore_index=True)

    # Ensure correct dtypes
    new_data["Date"] = pd.to_datetime(new_data["Date"], errors="coerce")
    new_data = new_data.dropna(subset=["Date", "Symbol"])

    # Merge with existing data
    if Path(OUTPUT_FILE).exists():
        old = pd.read_csv(OUTPUT_FILE)
        old["Date"] = pd.to_datetime(old["Date"], errors="coerce")
        combined = pd.concat([old, new_data], ignore_index=True)
    else:
        combined = new_data

    # Final clean
    combined = combined.drop_duplicates(subset=["Date", "Symbol"])
    combined = combined.sort_values(["Symbol", "Date"])

    # Keep last 200 rows per symbol
    combined = (
        combined.groupby("Symbol", group_keys=False)
        .tail(200)
    )

    combined.to_csv(OUTPUT_FILE, index=False)

    print("✅ prices.csv updated successfully")


if __name__ == "__main__":
    main()
