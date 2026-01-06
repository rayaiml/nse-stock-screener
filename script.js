import pandas as pd
import numpy as np

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def macd(series):
    ema12 = ema(series, 12)
    ema26 = ema(series, 26)
    macd_line = ema12 - ema26
    signal = ema(macd_line, 9)
    return macd_line, signal

def adx(high, low, close, period=14):
    plus_dm = high.diff()
    minus_dm = low.diff() * -1

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    return dx.rolling(period).mean()

def add(df):
    df["EMA14"] = ema(df["CLOSE"], 14)
    df["EMA21"] = ema(df["CLOSE"], 21)
    df["EMA35"] = ema(df["CLOSE"], 35)
    df["EMA50"] = ema(df["CLOSE"], 50)
    df["EMA200"] = ema(df["CLOSE"], 200)

    df["RSI"] = rsi(df["CLOSE"])

    df["MACD"], df["SIG"] = macd(df["CLOSE"])

    df["ADX"] = adx(df["HIGH"], df["LOW"], df["CLOSE"])

    df["BBM"] = df["CLOSE"].rolling(20).mean()

    df["AVG_VOL"] = df["TOTTRDQTY"].rolling(21).mean()

    return df
