import pandas as pd
import ta

def add_indicators(df):
    df = df.copy()

    # RSI
    df["RSI"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

    # EMA
    df["EMA14"] = ta.trend.EMAIndicator(df["close"], 14).ema_indicator()
    df["EMA21"] = ta.trend.EMAIndicator(df["close"], 21).ema_indicator()
    df["EMA35"] = ta.trend.EMAIndicator(df["close"], 35).ema_indicator()

    # MACD
    macd = ta.trend.MACD(df["close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    # ADX
    adx = ta.trend.ADXIndicator(
        df["high"], df["low"], df["close"], window=14
    )
    df["ADX"] = adx.adx()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df["close"])
    df["BB_MID"] = bb.bollinger_mavg()

    # Avg volume (placeholder for now)
    df["AVG_VOL"] = df["volume"] * 0.8

    return df
