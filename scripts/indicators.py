import pandas_ta as ta
def add(df):
    df['EMA14']=ta.ema(df.CLOSE,14)
    df['EMA21']=ta.ema(df.CLOSE,21)
    df['EMA35']=ta.ema(df.CLOSE,35)
    df['RSI']=ta.rsi(df.CLOSE,14)
    macd=ta.macd(df.CLOSE)
    df['MACD']=macd.iloc[:,0];df['SIG']=macd.iloc[:,1]
    adx=ta.adx(df.HIGH,df.LOW,df.CLOSE)
    df['ADX']=adx.iloc[:,0]
    bb=ta.bbands(df.CLOSE)
    df['BBM']=bb.iloc[:,1]
    df['AVG_VOL']=df.TOTTRDQTY.rolling(21).mean()
    return df
