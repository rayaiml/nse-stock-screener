import yfinance as yf
import pandas_ta as ta
from universe import get_nse_symbols

def run_scan():
    results = []
    symbols = get_nse_symbols()

    for symbol in symbols:
        try:
            df = yf.download(symbol, period="6mo", interval="1d", progress=False)
            if len(df) < 50:
                continue

            df.ta.adx(length=14, append=True)
            df.ta.macd(append=True)
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=14, append=True)
            df.ta.ema(length=21, append=True)
            df.ta.ema(length=35, append=True)
            df.ta.bbands(length=20, append=True)
            df["VOL_SMA_21"] = df["Volume"].rolling(21).mean()

            last = df.iloc[-1]
            adx = last["ADX_14"]

            if not (
                22 < adx < 30 and
                last["MACD_12_26_9"] > last["MACDs_12_26_9"] and
                last["Volume"] > last["VOL_SMA_21"] and
                last["Close"] > last["Open"] and
                last["EMA_14"] > last["EMA_21"] and
                last["EMA_14"] > last["EMA_35"] and
                last["Close"] > last["BBM_20_2.0"]
            ):
                continue

            if last["Close"] > last["BBU_20_2.0"]:
                bb = "Upper Band"
            elif last["Close"] < last["BBL_20_2.0"]:
                bb = "Lower Band"
            else:
                bb = "Middle Band"

            results.append({
                "stock": symbol.replace(".NS", ""),
                "rsi": round(last["RSI_14"], 2),
                "adx": round(adx, 2),
                "macd": "Yes",
                "current_volume": int(last["Volume"]),
                "avg_volume": int(last["VOL_SMA_21"]),
                "bb": f"{round(last['Close'],2)} – {bb}",
                "trend": "Emerging Uptrend – EMA Strength"
            })

        except:
            continue

    return results
