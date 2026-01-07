import os
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

DATA_PATH = "data/latest.csv"

@app.route("/scan")
def scan():
    if not os.path.exists(DATA_PATH):
        return jsonify({
            "error": "Data file not found",
            "hint": "Run GitHub Action and redeploy Render",
            "path": DATA_PATH
        }), 500

    df = pd.read_csv(DATA_PATH)

    # minimal response for now
    return jsonify(df.head(10).to_dict(orient="records"))
