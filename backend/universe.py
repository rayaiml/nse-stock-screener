import pandas as pd

def get_nse_symbols():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(url)
    df = df[df[" SERIES"] == "EQ"]
    return [f"{s.strip()}.NS" for s in df["SYMBOL"]]
