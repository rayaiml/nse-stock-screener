import yfinance as yf
import pandas as pd
from pathlib import Path
import time

# ---------------- CONFIG ---------------- #
DATA_DIR = Path("data")
SYMBOL_FILE = DATA_DIR / "symbols.txt"
OUTPUT_FILE = DATA_DIR / "prices.csv"

START_DATE = "2024-01-01"   # change if needed
END_DATE = None             # None = today
SLEEP_SECONDS = 1           # prevent Yahoo rate-limit
# ---------------------------------------- #

def load_symbols():
    if not SYMBOL_FILE.exists():
        raise FileNotFoundError("symbols.txt not found in data/")

    with open(SYMBOL_FILE) as f:
        symbols = [line.strip() for line in f if line.strip()]

    if not symbols:
        raise ValueError("symbols.txt is empty")

    return symbols


def fetch_symbol(symbol):
    """
    Fetch OHLCV for ONE symbol and return clean dataframe
    """
    try:
        df = yf.download(
            symbol,
            start=START_DATE,
            end=END_DATE,
            progress=False,
            auto_adjust=False
        )

        if df.empty:
            print(f"⚠️ No data for {symbol}")
            return None

        df.reset_index(inplace=True)

        # Standardize columns
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df["Symbol"] = symbol

        # Ensure correct order
        df = df[["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]]

        return df

    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
        return None


def main():
    DATA_DIR.mkdir(exist_ok=True)

    symbols = load_symbols()
    print(f"📈 Fetching data for {len(symbols)} symbols")

    all_data = []

    for i, symbol in enumerate(symbols, start=1):
        print(f"[{i}/{len(symbols)}] Fetching {symbol}")
        df = fetch_symbol(symbol)

        if df is not None:
            all_data.append(df)

        time.sleep(SLEEP_SECONDS)

    if not all_data:
        raise RuntimeError("No data fetched for any symbol")

    final_df = pd.concat(all_data, ignore_index=True)

    # Sort cleanly
    final_df.sort_values(["Symbol", "Date"], inplace=True)

    # Save
    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Saved {len(final_df)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
