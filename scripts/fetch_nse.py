
import pandas as pd
import requests

URL = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
HEADERS = {"User-Agent":"Mozilla/5.0","Referer":"https://www.nseindia.com/"}

s = requests.Session()
s.get("https://www.nseindia.com", headers=HEADERS)
r = s.get(URL, headers=HEADERS)
data = r.json()["data"]

rows=[]
for d in data:
    rows.append({
        "symbol":d["symbol"],
        "open":d["open"],
        "high":d["dayHigh"],
        "low":d["dayLow"],
        "close":d["lastPrice"],
        "volume":d["totalTradedVolume"]
    })

pd.DataFrame(rows).to_csv("data/latest.csv", index=False)
