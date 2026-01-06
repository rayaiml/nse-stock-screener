import pandas as pd
import requests
from indicators import add

def fetch_nse_data():
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.nseindia.com/",
    }

    # Step 1: Warm up session
    session.get("https://www.nseindia.com", headers=headers, timeout=10)

    # Step 2: Actual API call
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
    response = session.get(url, headers=headers, timeout=10)

    response.raise_for_status()
    return response.json()["data"]


def scan(filters):
    try:
        data = fetch_nse_data()
    except Exception:
        return []

    rows = []
    for s in data:
        if "lastPrice" not in s or "totalTradedVolume" not in s:
            continue

        rows.append({
            "symbol": s["symbol"],
            "CLOSE": s["lastPrice"],
            "VOLUME": s["totalTradedVolume"]
        })

    if not rows:
        return []

    df = pd.DataFrame(rows)
    df = add(df)

    output = []

    for _, r in df.iterrows():

        if filters["adx"] and not (22 <= r.ADX <= 30):
            continue

        if filters["macd"] and r.MACD <= r.SIG:
            continue

        if filters["volume"] and r.VOLUME <= r.AVG_VOL:
            continue

        if filters["rsi"] and not (40 <= r.RSI <= 55):
            continue

        # EMA / BB placeholders (can be enhanced later)
        if filters["ema21"] and r.EMA14 <= r.EMA21:
            continue

        if filters["ema35"] and r.EMA14 <= r.EMA35:
            continue

        if filters["bb"] and r.CLOSE <= r.BBM:
            continue

        output.append({
            "stock": r.symbol,
            "rsi": round(r.RSI, 2),
            "adx": round(r.ADX, 2),
            "macd": "Yes" if r.MACD > r.SIG else "No",
            "volume": int(r.VOLUME),
            "avg_volume": int(r.AVG_VOL),
            "bb": "Above Middle" if r.CLOSE > r.BBM else "Below Middle",
            "trend": "Bullish"
        })

    return output

