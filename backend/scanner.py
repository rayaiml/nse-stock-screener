
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/nse-stock-screener/main/data/latest.csv"

def scan(filters):
    df = pd.read_csv(DATA_URL)

    if filters.get("volume"):
        df = df[df["volume"] > df["volume"].mean()]

    df = df.sort_values("volume", ascending=False)

    return [
        {
            "stock": r.symbol,
            "rsi": "NA",
            "adx": "NA",
            "macd": "NA",
            "volume": int(r.volume),
            "avg_volume": int(df["volume"].mean()),
            "bb": "NA",
            "trend": "NA",
        }
        for _, r in df.head(10).iterrows()
    ]
