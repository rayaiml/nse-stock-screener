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
            auto_adjust=False,
        )

        if df is None or df.empty:
            print(f"⚠️ No data: {symbol}")
            return None

        # Flatten columns (important for Yahoo)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        # Normalize date column
        if "Date" not in df.columns:
            if "Datetime" in df.columns:
                df.rename(columns={"Datetime": "Date"}, inplace=True)
            else:
                print(f"⚠️ Date missing: {symbol}")
                return None

        # Required columns check
        required = {"Date", "Open", "High", "Low", "Close", "Volume"}
        if not required.issubset(df.columns):
            print(f"⚠️ Missing OHLCV: {symbol}")
            return None

        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
        df["Symbol"] = symbol

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
        if df is not None and not df.empty:
            frames.append(df)

    if not frames:
        raise RuntimeError("❌ No valid stock data fetched from Yahoo")

    new_data = pd.concat(frames, ignore_index=True)

    # Safety check
    if not {"Date", "Symbol"}.issubset(new_data.columns):
        raise RuntimeError("❌ Critical columns missing after fetch")

    new_data["Date"] = pd.to_datetime(new_data["Date"], errors="coerce")
    new_data = new_data.dropna(subset=["Date", "Symbol"])

    # Merge with existing data
    if Path(OUTPUT_FILE).exists():
        old = pd.read_csv(OUTPUT_FILE)
        if {"Date", "Symbol"}.issubset(old.columns):
            old["Date"] = pd.to_datetime(old["Date"], errors="coerce")
            combined = pd.concat([old, new_data], ignore_index=True)
        else:
            combined = new_data
    else:
        combined = new_data

    # Final cleanup
    combined = combined.drop_duplicates(subset=["Date", "Symbol"])
    combined = combined.sort_values(["Symbol", "Date"])

    # Keep last 200 rows per stock
    combined = combined.groupby("Symbol", group_keys=False).tail(200)

    combined.to_csv(OUTPUT_FILE, index=False)

    print("✅ prices.csv updated successfully")


if __name__ == "__main__":
    main()
