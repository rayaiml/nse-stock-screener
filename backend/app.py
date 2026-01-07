import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

CSV_PATH = "data/merged_200d.csv"

@app.route("/ping")
def ping():
    return {"status": "ok"}

@app.route("/scan")
def scan():
    try:
        df = pd.read_csv(CSV_PATH)

        # Basic validation
        required = {"SYMBOL", "OPEN", "HIGH", "LOW", "CLOSE", "TOTTRDQTY"}
        if not required.issubset(df.columns):
            return jsonify({"error": "Invalid CSV format"}), 400

        # Latest candle per stock
        df = df.sort_values("DATE").groupby("SYMBOL").tail(1)

        # Minimal payload (NO FILTERING YET)
        result = []
        for _, row in df.iterrows():
            result.append({
                "symbol": row["SYMBOL"],
                "close": round(row["CLOSE"], 2),
                "volume": int(row["TOTTRDQTY"])
            })

        return jsonify(result[:200])  # raw universe

    except Exception as e:
        logging.exception("SCAN FAILED")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
