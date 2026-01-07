import logging
import pandas as pd
import numpy as np
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

# ---------------- CONFIG ----------------
CSV_URL = "https://raw.githubusercontent.com/rayaiml/nse-stock-screener/main/data/latest.csv"

# ---------------- APP -------------------
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- HELPERS ----------------

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

def macd(series):
    fast = ema(series, 12)
    slow = ema(series, 26)
    macd_line = fast - slow
    signal = ema(macd_line, 9)
    return macd_line, signal

def bollinger(series, period=20):
    sma = series.rolling(period).mean()
    std = series.rolling(period).std()
    upper = sma + (2 * std)
    lower = sma - (2 * std)
    return upper, sma, lower

def adx(high, low, close, period=14):
    tr = np.maximum(high - low,
         np.maximum(abs(high - close.shift()),
                    abs(low - close.shift())))

    plus_dm = np.where((high - high.shift()) > (low.shift() - low),
                       np.maximum(high - high.shift(), 0), 0)

    minus_dm = np.where((low.shift() - low) > (high - high.shift()),
                        np.maximum(low.shift() - low, 0), 0)

    atr = pd.Series(tr).rolling(period).mean()
    plus_di = 100 * pd.Series(plus_dm).rolling(period).mean() / atr
    minus_di = 100 * pd.Series(minus_dm).rolling(period).mean() / atr

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    return dx.rolling(period).mean()

# ---------------- ROUTES ----------------

@app.route("/ping")
def ping():
    return "OK", 200

@app.route("/scan")
def scan():
    try:
        logger.info("Fetching CSV from GitHub...")
        df = pd.read_csv(CSV_URL)

        if df.empty:
            return jsonify([])

        results = []

        for symbol, g in df.groupby("SYMBOL"):
            if len(g) < 60:
                continue

            close = g["CLOSE"]
            high = g["HIGH"]
            low = g["LOW"]
            volume = g["TOTTRDQTY"]

            ema14 = ema(close, 14).iloc[-1]
            ema21 = ema(close, 21).iloc[-1]
            ema35 = ema(close, 35).iloc[-1]

            rsi_val = rsi(close).iloc[-1]
            macd_line, macd_signal = macd(close)

            bb_upper, bb_mid, bb_lower = bollinger(close)
            adx_val = adx(high, low, close).iloc[-1]

            results.append({
                "stock": symbol,
                "rsi": round(rsi_val, 2),
                "adx": round(adx_val, 2),
                "macd": macd_line.iloc[-1] > macd_signal.iloc[-1],
                "volume": int(volume.iloc[-1]),
                "avg_volume": int(volume.rolling(21).mean().iloc[-1]),
                "bb": (
                    "Upper" if close.iloc[-1] > bb_upper.iloc[-1]
                    else "Lower" if close.iloc[-1] < bb_lower.iloc[-1]
                    else "Middle"
                ),
                "trend": "Bullish" if ema14 > ema35 else "Neutral"
            })

        logger.info(f"Scan completed. {len(results)} stocks found")
        return jsonify(results[:10])

    except Exception as e:
        logger.exception("SCAN FAILED")
        return jsonify({
            "error": str(e)
        }), 500

# ---------------- MAIN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
