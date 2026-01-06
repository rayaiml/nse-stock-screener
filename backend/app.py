from flask import Flask, jsonify, request
from flask_cors import CORS
from scanner import scan

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {
        "status": "OK",
        "message": "NSE Stock Screener API is running",
        "endpoints": ["/scan"]
    }

@app.route("/scan")
def run_scan():
    filters = {
        "adx": request.args.get("adx", "1") == "1",
        "macd": request.args.get("macd", "1") == "1",
        "volume": request.args.get("volume", "1") == "1",
        "ema21": request.args.get("ema21", "1") == "1",
        "ema35": request.args.get("ema35", "1") == "1",
        "bb": request.args.get("bb", "1") == "1",
        "rsi": request.args.get("rsi", "1") == "1",
    }

    return jsonify(scan(filters))

if __name__ == "__main__":
    app.run()
