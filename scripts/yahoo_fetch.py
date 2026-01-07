
import yfinance as yf
import pandas as pd
from datetime import datetime

symbols = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS"]

frames = []
for s in symbols:
    df = yf.download(s, period="200d", interval="1d")
    if df.empty:
        continue
    df = df.reset_index()
    df["Symbol"] = s
    frames.append(df)

if not frames:
    raise RuntimeError("No data fetched")

out = pd.concat(frames)
out.to_csv("data/prices.csv", index=False)
print("Saved data/prices.csv")
