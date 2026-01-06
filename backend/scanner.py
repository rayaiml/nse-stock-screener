import pandas as pd
import numpy as np
import requests
import zipfile
from io import BytesIO
from datetime import date, timedelta
from indicators import add_indicators

# ---------------- FETCH BHAVCOPY ----------------
def fetch_bhavcopy():
    d = date.today()
    for _ in range(5):  # try last 5 days (holidays safe)
        try:
            ds = d.strftime("%d%b%Y").upper()
            url = f"https://www1.nseindia.com/content/historical/EQUITIES/{d.year}/{d.strftime('%b').upper()}/cm{ds}bhav.csv.zip"

            r = requests.get(url, timeout=15)
            z = zipfile.ZipFile(BytesIO(r.content))
            df = pd.read_csv(z.open(z.namelist()[0]))
            return df
        except Exception:
            d -= timedelta(days=1)

    raise Exception("Bhavcopy not available")

# ---------------- MAIN SCAN ----------------
def scan(filters):
    df = fetch_bhavcopy()

    df = df[df["SERIES"] == "EQ"]
    df = df[[
        "SYMBOL", "OPEN", "HIGH", "LOW", "CLOSE", "TOTTRDQTY"
    ]]

    results = []

    # Group by stock (1 candle per stock for now)
    for _, r in df.iterrows():
        prices = pd.DataFrame({
            "open": [r.OPEN],
            "high": [r.HIGH],
            "low": [r.LOW],
            "close": [r.CLOSE],
            "volume": [r.TOTTRDQTY]
        })

        ind = add_indicators(prices)

        row = ind.iloc[-1]

        # ---------------- APPLY FILTERS ----------------
        if filters["rsi"] and not (40 <= row.RSI <= 55):
            continue

        if filters["macd"] and row.MACD <= row.MACD_SIGNAL:
            continue

        if filters["adx"] and not (22 <= row.ADX <= 30):
            continue

        if filters["volume"] and row.volume <= row.AVG_VOL:
            continue

        if filters["ema21"] and row.EMA14 <= row.EMA21:
            continue

        if filters["ema35"] and row.EMA14 <= row.EMA35:
            continue

        if filters["bb"] and row.close <= row.BB_MID:
            continue

        results.append({
            "stock": r.SYMBOL,
            "rsi": round(row.RSI, 2),
            "adx": round(row.ADX, 2),
            "macd": "Yes",
            "volume": int(row.volume),
            "avg_volume": int(row.AVG_VOL),
            "bb": "Above Middle",
            "trend": "Bullish"
        })

    # Always return something useful
    return sorted(
        results,
        key=lambda x: (x["macd"], x["rsi"], x["volume"]),
        reverse=True
    )[:20]
