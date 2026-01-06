import pandas as pd
import requests
from indicators import add

def scan():
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = requests.get(url, headers=headers).json()["data"]

    rows = []
    for s in data:
        rows.append({
            "symbol": s["symbol"],
            "CLOSE": s["lastPrice"],
            "VOLUME": s["totalTradedVolume"]
        })

    df = pd.DataFrame(rows)
    df = add(df)

    out = []
    for _, r in df.iterrows():
        if r.MACD > r.SIG:
            out.append({
                "stock": r.symbol,
                "rsi": round(r.RSI, 2),
                "adx": "NA",
                "macd": "Yes",
                "volume": int(r.VOLUME),
                "avg_volume": int(r.AVG_VOL),
                "bb": "Middle",
                "trend": "Bullish"
            })
    return out
