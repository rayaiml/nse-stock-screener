import os
import yfinance as yf
import pandas as pd

# ✅ Ensure data directory exists
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

symbols = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

frames = []

for s in symbols:
    try:
        df = yf.download(s, period="1y", interval="1d", progress=False)
        if df.empty:
            print(f"❌ No data for {s}")
            continue

        df.reset_index(inplace=True)
        df["SYMBOL"] = s.replace(".NS", "")
        frames.append(df)

    except Exception as e:
        print(f"❌ Failed {s}: {e}")

# ✅ Prevent concat crash
if not frames:
    raise RuntimeError("No Yahoo data downloaded")

out = pd.concat(frames, ignore_index=True)
out.to_csv(f"{DATA_DIR}/prices.csv", index=False)

print("✅ Yahoo prices saved to data/prices.csv")
