import pandas as pd
import time
from datetime import datetime, timedelta

SYMBOLS_FILE = "data/symbols.txt"
OUT_FILE = "data/merged_200d.csv"

DAYS = 200
PERIOD2 = int(time.time())
PERIOD1 = PERIOD2 - DAYS * 86400 * 2  # buffer

def fetch(symbol):
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}"
        f"?period1={PERIOD1}&period2={PERIOD2}&interval=1d&events=history"
    )
    try:
        df = pd.read_csv(url)
        df = df.dropna()
        df = df.tail(DAYS)
        df["SYMBOL"] = symbol.replace(".NS", "")
        df = df.rename(columns={
            "Date": "DATE",
            "Open": "OPEN",
            "High": "HIGH",
            "Low": "LOW",
            "Close": "CLOSE",
            "Volume": "VOLUME"
        })
        return df[["DATE","SYMBOL","OPEN","HIGH","LOW","CLOSE","VOLUME"]]
    except Exception as e:
        print(f"Failed {symbol}: {e}")
        return None

def main():
    symbols = open(SYMBOLS_FILE).read().splitlines()
    frames = []

    for s in symbols:
        df = fetch(s)
        if df is not None:
            frames.append(df)

    merged = pd.concat(frames)
    merged.to_csv(OUT_FILE, index=False)
    print("✅ Yahoo merged_200d.csv updated")

if __name__ == "__main__":
    main()
