import os
import time
import pandas as pd
import yfinance as yf

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.volatility import BollingerBands

# -----------------------------
# PATHS (DO NOT CHANGE)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

SYMBOL_FILE = os.path.join(DATA_DIR, "symbols.txt")
OUTPUT_FILE = os.path.join(DATA_DIR, "prices.csv")

DAYS = 220

os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------
# LOAD SYMBOLS
# -----------------------------
def load_symbols():
    with open(SYMBOL_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


# -----------------------------
# INDICATORS
# -----------------------------
def compute_indicators(df):
    df = df.copy()

    df["RSI_14"] = RSIIndicator(df["Close"], window=14).rsi()

    df["EMA_14"] = EMAIndicator(df["Close"], window=14).ema_indicator()
    df["EMA_21"] = EMAIndicator(df["Close"], window=21).ema_indicator()
    df["EMA_35"] = EMAIndicator(df["Close"], window=35).ema_indicator()
    df["EMA_50"] = EMAIndicator(df["Close"], window=50).ema_indicator()
    df["EMA_200"] = EMAIndicator(df["Close"], window=200).ema_indicator()

    macd = MACD(df["Close"], window_slow=26, window_fast=12, window_sign=9)
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()
    df["MACD_HIST"] = macd.macd_diff()

    adx = ADXIndicator(
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        window=14
    )
    df["ADX_14"] = adx.adx()
    df["+DI"] = adx.adx_pos()
    df["-DI"] = adx.adx_neg()

    bb = BollingerBands(df["Close"], window=20, window_dev=2)
    df["BB_UPPER"] = bb.bollinger_hband()
    df["BB_MIDDLE"] = bb.bollinger_mavg()
    df["BB_LOWER"] = bb.bollinger_lband()

    return df


# -----------------------------
# MAIN FETCH LOGIC
# -----------------------------
def main():
    print("🚀 Yahoo fetch started")

    symbols = load_symbols()
    print(f"📄 Symbols loaded: {len(symbols)}")

    frames = []

    for i, symbol in enumerate(symbols, 1):
        print(f"[{i}/{len(symbols)}] Fetching {symbol}")

        try:
            df = yf.download(
                symbol,
                period=f"{DAYS}d",
                interval="1d",
                auto_adjust=False,
                progress=False,
                threads=False
            )

            if df.empty:
                print(f"⚠️ No data: {symbol}")
                continue

            df.reset_index(inplace=True)
            df["Symbol"] = symbol

            df = compute_indicators(df)

            frames.append(df)
            time.sleep(1.2)

        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")
            continue

    if not frames:
        print("❌ No data fetched at all")
        return

    new_data = pd.concat(frames, ignore_index=True)

    new_data.dropna(subset=["Date", "Symbol"], inplace=True)

    if os.path.exists(OUTPUT_FILE):
        old = pd.read_csv(OUTPUT_FILE)
        combined = pd.concat([old, new_data], ignore_index=True)
    else:
        combined = new_data

    combined.drop_duplicates(subset=["Date", "Symbol"], inplace=True)
    combined.sort_values(["Symbol", "Date"], inplace=True)

    combined.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ prices.csv updated with {len(combined)} rows")


# -----------------------------
if __name__ == "__main__":
    main()
