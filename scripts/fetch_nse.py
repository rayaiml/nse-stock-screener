import os
import io
import zipfile
import requests
import pandas as pd
from datetime import datetime, timedelta
from glob import glob

BASE_DIR = "data"
BHAV_DIR = f"{BASE_DIR}/bhavcopy"
MERGED_FILE = f"{BASE_DIR}/merged_200d.csv"
TARGET_DAYS = 200

os.makedirs(BHAV_DIR, exist_ok=True)

def is_trading_day(date):
    return date.weekday() < 5  # Mon–Fri

def fetch_bhavcopy(date):
    d = date.strftime("%d%m%Y")
    url = f"https://archives.nseindia.com/content/historical/EQUITIES/{date.year}/{date.strftime('%b').upper()}/cm{d}bhav.csv.zip"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/zip"
    }

    r = requests.get(url, headers=headers, timeout=20)
    if r.status_code != 200:
        return False

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = z.namelist()[0]
        df = pd.read_csv(z.open(name))
        df["DATE"] = date.strftime("%Y-%m-%d")
        df = df[["SYMBOL","OPEN","HIGH","LOW","CLOSE","TOTTRDQTY","DATE"]]

        out = f"{BHAV_DIR}/{date.strftime('%Y-%m-%d')}.csv"
        df.to_csv(out, index=False)

    return True

def ensure_200_days():
    files = sorted(glob(f"{BHAV_DIR}/*.csv"))
    dates = [datetime.strptime(os.path.basename(f)[:10], "%Y-%m-%d") for f in files]

    d = datetime.today()
    while len(files) < TARGET_DAYS:
        d -= timedelta(days=1)
        if not is_trading_day(d):
            continue
        if fetch_bhavcopy(d):
            files.append(f"{BHAV_DIR}/{d.strftime('%Y-%m-%d')}.csv")

def merge_latest_200():
    files = sorted(glob(f"{BHAV_DIR}/*.csv"))[-TARGET_DAYS:]
    dfs = [pd.read_csv(f) for f in files]
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(MERGED_FILE, index=False)

    # cleanup old
    for f in glob(f"{BHAV_DIR}/*.csv")[:-TARGET_DAYS]:
        os.remove(f)

def main():
    today = datetime.today()
    today_file = f"{BHAV_DIR}/{today.strftime('%Y-%m-%d')}.csv"

    if is_trading_day(today) and not os.path.exists(today_file):
        fetch_bhavcopy(today)

    ensure_200_days()
    merge_latest_200()
    print("✅ NSE 200-day dataset ready")

if __name__ == "__main__":
    main()
