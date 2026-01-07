
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

DATA_PATH = "data/prices.csv"

@app.route("/")
def home():
    return "NSE Stock Screener Backend Running"

@app.route("/data")
def data():
    try:
        df = pd.read_csv(DATA_PATH)
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
