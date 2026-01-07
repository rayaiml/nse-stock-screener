from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

CSV_URL = "https://raw.githubusercontent.com/rayaiml/nse-stock-screener/main/data/latest.csv"

@app.route("/")
def home():
    return "NSE Stock Screener Backend OK"

@app.route("/scan")
def scan():
    try:
        df = pd.read_csv(CSV_URL)

        # Replace NaN safely
        df = df.fillna(0)

        # Convert to records
        data = df.to_dict(orient="records")

        logging.info(f"Returned {len(data)} stocks")

        return jsonify({
            "count": len(data),
            "data": data
        })

    except Exception as e:
        logging.exception("SCAN FAILED")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
