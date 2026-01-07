import logging
import pandas as pd
import numpy as np
import requests
from flask import Flask, jsonify
from flask_cors import CORS

CSV_URL = "https://raw.githubusercontent.com/rayaiml/nse-stock-screener/main/data/latest.csv"

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- SAFE CSV LOADER ----------------
def load_csv():
    try:
        logger.info(f"Loading CSV from {CSV_URL}")
        df = pd.read_csv(CSV_URL)
        logger.info(f"CSV loaded successfully. Rows: {len(df)}")
        return df
    except Exception:
        logger.exception("CSV LOAD FAILED")
        return pd.DataFrame()

# ---------------- INDICATORS ----------------
def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return {"status": "OK"}

@app.route("/ping")
def ping():
    return "OK", 200

@app.route("/scan")
def scan():
    df = load_csv()

    if df.empty:
        return jsonify({
            "error": "CSV not reachable",
            "csv_url": CSV_URL
        }), 200

    results = []

    for _, r in df.head(10).iterrows():
        results.append({
            "stock": r["SYMBOL"],
            "rsi": "NA",
            "adx": "NA",
            "macd": "NA",
            "volume": int(r["TOTTRDQTY"]),
            "avg_volume": int(df["TOTTRDQTY"].mean()),
            "bb": "NA",
            "trend": "NA"
        })

    return jsonify(results)

@app.route("/debug/csv")
def debug_csv():
    try:
        r = requests.get(CSV_URL, timeout=10)
        return jsonify({
            "status_code": r.status_code,
            "sample": r.text[:500]
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
