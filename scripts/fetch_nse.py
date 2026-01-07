import os
import pandas as pd
import requests

URL = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/"
}

def main():
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=HEADERS)

    response = session.get(URL, headers=HEADERS, timeout=20)
    response.raise_for_status()

    data = response.json()["data"]

    rows = []
    for d in data:
        rows.append({
            "SYMBOL": d["symbol"],
            "OPEN": d["open"],
            "HIGH": d["dayHigh"],
            "LOW": d["dayLow"],
            "CLOSE": d["lastPrice"],
            "TOTTRDQTY": d["totalTradedVolume"]
        })

    df = pd.DataFrame(rows)

    # 🔴 CRITICAL FIX (Scenario B)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/latest.csv", index=False)

    print("Saved data/latest.csv with", len(df), "rows")

if __name__ == "__main__":
    main()
