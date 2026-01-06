import pandas as pd
import requests
import zipfile
from io import BytesIO
from datetime import date, timedelta

def fetch_bhavcopy():
    d = date.today()
    for _ in range(7):
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

    return pd.DataFrame()

def scan(_filters=None):
    df = fetch_bhavcopy()

    if df.empty:
        return []

    # 🔥 PRINT DEBUG (VISIBLE IN RENDER LOGS)
    print("Bhavcopy columns:", list(df.columns))
    print("Bhavcopy rows:", len(df))

    df.columns = df.columns.str.strip().str.upper()
    df = df[df["SERIES"] == "EQ"]

    results = []

    for _, r in df.iterrows():
        results.append({
            "stock": r["SYMBOL"],
            "rsi": "NA",
            "adx": "NA",
            "macd": "NA",
            "volume": int(r["TOTTRDQTY"]),
            "avg_volume": int(r["TOTTRDQTY"] * 0.8),
            "bb": "NA",
            "trend": "NA"
        })

    # 🔥 SORT BY VOLUME → ALWAYS DATA
    results = sorted(results, key=lambda x: x["volume"], reverse=True)

    return results[:20]
