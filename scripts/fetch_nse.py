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
MAX_LOOKBACK_DAYS = 300

os.makedirs(BHAV_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/zip,application/octet-stream,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/"
}

def get_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    # Warm up NSE cookies
    s.get("https://www.nseindia.com", timeout=15)
    return s

def fetch_bhavcopy(session, date):
    d = date.strftime("%d%m%Y")
    url = (
        f"https://archives.nseindia.com/content/historical/"
        f"EQUITIES/{date.year}/{date.strftime('%b').upper()}/cm{d}bhav.csv.zip"
    )

    try:
        r = session.get(url, timeout=20)
        if r.status_code != 200 or len(r.content) < 1000:
            return False

        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            name = z.namelist()[0]
            df = pd.read_csv(z.open(name))
            df["DATE"] = date.strftime("%Y-%m-%d")
            df = df[["SYMBOL","OPEN","HIGH","LOW","CLOSE","TOTTRDQTY","DATE"]]

            out = f"{BHAV_DIR}/{date.strftime('%Y-%m-%d')}.csv"
            df.to_csv(out, index=False)
            print(f"Downloaded {out}")
            return True

    except Exception as e:
        print(f"Failed {date.date()}: {e}")
        return False

def backfill_200_days():
    existing = set(os.path.basename(f)[:10] for f in glob(f"{BHAV_DIR}/*.csv"))
    collected = len(existing)

    session = get_session()
    date = datetime.today()

    looked_back = 0

    while collected < TARGET_DAYS and looked_back < MAX_LOOKBACK_DAYS:
        date -= timedelta(days=1)
        looked_back += 1

        date_str = date.strftime("%Y-%m-%d")
        if date_str in existing:
            continue

        if fetch_bhavcopy(session, date):
            collected += 1

    if collected < TARGET_DAYS:
        raise RuntimeError(
            f"Only collected {collected} days after looking back {looked_back} days"
        )

def merge_latest_200():
    files = sorted(glob(f"{BHAV_DIR}/*.csv"))[-TARGET_DAYS:]
    dfs = [pd.read_csv(f) for f in files]
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(MERGED_FILE, index=False)

    # cleanup old files
    for f in glob(f"{BHAV_DIR}/*.csv")[:-TARGET_DAYS]:
        os.remove(f)

def main():
    backfill_200_days()
    merge_latest_200()
    print("✅ Rolling 200-day bhavcopy ready")

if __name__ == "__main__":
    main()
