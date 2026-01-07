import logging
import pandas as pd
import requests
from flask import Flask, jsonify
from flask_cors import CORS

CSV_URL = "https://raw.githubusercontent.com/rayaiml/nse-stock-screener/main/data/latest.csv"

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_csv():
    try:
        logger.info(f"Loading CSV from {CSV_URL}")
        df = pd.read_csv(CSV_URL)
        logger.info(f"CSV loaded successfully, rows={len(df)}")
        return df
    except Exception as e:
        logger.exception("CSV LOAD FAILED")
        return pd.DataFrame()

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
            "error": "CSV is empty or not reachable",
            "csv_url": CSV_URL
        }), 200

    results = []
    avg_vol = int(df["TOTTRDQTY"].mean())

    for _, r in df.sort_values("TOTTRDQTY", ascending=False).head(10).iterrows():
        results.append({
            "stock": r["SYMBOL"],
            "rsi": "NA",
            "adx": "NA",
            "macd": "NA",
            "volume": int(r["TOTTRDQTY"]),
            "avg_volume": avg_vol,
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
            "sample": r.text[:300]
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
