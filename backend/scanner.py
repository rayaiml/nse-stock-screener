import pandas as pd
import requests
import zipfile
from io import BytesIO
from datetime import date, timedelta

# ---------------- FETCH LATEST BHAVCOPY SAFELY ----------------
def fetch_bhavcopy():
    d = date.today()
    for _ in range(7):  # try last 7 days (handles holidays)
        try:
            ds = d.strftime("%d%b%Y").upper()
            url = (
                f"https://www1.nseindia.com/content/historical/EQUITIES/"
                f"{d.year}/{d.strftime('%b').upper()}/cm{ds}bhav.csv.zip"
            )

            r = requests.get(url, timeout=20)
            r.raise_for_status()

            z = zipfile.ZipFile(BytesIO(r.content))
            df = pd.read_csv(z.open(z.namelist()[0]))

            return df
        except Exception:
            d -= timedelta(days=1)

    raise Exception("Bhavcopy not available")

# ---------------- MAIN SCAN (NO INDICATORS YET) ----------------
def scan(filters):
    try:
        df = fetch_bhavcopy()
    except Exception as e:
        print("Bhavcopy fetch failed:", e)
        return []

    
    df = df[df["SERIES"] == "EQ"]

    results = []

    for _, r in df.iterrows():
        try:
            results.append({
                "stock": r["SYMBOL"],
                "rsi": None,
                "adx": None,
                "macd": "NA",
                "volume": int(r["TOTTRDQTY"]),
                "avg_volume": int(r["TOTTRDQTY"] * 0.8),
                "bb": "NA",
                "trend": "NA"
            })
        except Exception:
            continue

    # Return top 20 by volume so UI always has data
    results = sorted(results, key=lambda x: x["volume"], reverse=True)

    return results[:20]
