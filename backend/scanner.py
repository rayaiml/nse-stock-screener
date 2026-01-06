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


def scan():
    try:
        data = fetch_nse_data()
    except Exception as e:
        print("NSE fetch failed:", e)
        return []   # IMPORTANT: don't crash app

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
        if r.MACD > r.SIG:
            output.append({
                "stock": r.symbol,
                "rsi": round(r.RSI, 2),
                "adx": "NA",
                "macd": "Yes",
                "volume": int(r.VOLUME),
                "avg_volume": int(r.AVG_VOL),
                "bb": "Middle",
                "trend": "Bullish"
            })

    return output
