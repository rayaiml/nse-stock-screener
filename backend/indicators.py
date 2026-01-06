import pandas as pd
import numpy as np

def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def rsi(s, n=14):
    d = s.diff()
    g = d.clip(lower=0)
    l = -d.clip(upper=0)
    rs = g.rolling(n).mean() / l.rolling(n).mean()
    return 100 - (100 / (1 + rs))

def macd(s):
    m = ema(s,12) - ema(s,26)
    return m, ema(m,9)

def add(df):
    df["EMA14"] = ema(df.CLOSE,14)
    df["EMA21"] = ema(df.CLOSE,21)
    df["EMA35"] = ema(df.CLOSE,35)
    df["RSI"] = rsi(df.CLOSE)
    df["MACD"], df["SIG"] = macd(df.CLOSE)
    df["BBM"] = df.CLOSE.rolling(20).mean()
    df["AVG_VOL"] = df.VOLUME.rolling(21).mean()
    return df
