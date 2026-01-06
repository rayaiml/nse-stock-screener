import pandas as pd
from fetch_bhavcopy import fetch
from indicators import add

df=fetch()
out=[]
for s in df.SYMBOL.unique():
    d=df[df.SYMBOL==s].tail(200)
    if len(d)<50: continue
    d=add(d);l=d.iloc[-1]
    if not(22<l.ADX<30 and l.MACD>l.SIG and l.TOTTRDQTY>l.AVG_VOL and l.EMA14>l.EMA21>l.EMA35 and l.CLOSE>l.BBM): continue
    out.append({'stock':s,'rsi':round(l.RSI,2),'adx':round(l.ADX,2),'macd':'Yes','volume':int(l.TOTTRDQTY),'avg_volume':int(l.AVG_VOL),'bb':'Above Middle','trend':'Bullish'})
pd.DataFrame(out).to_json('data/scan_result.json',orient='records')
pd.DataFrame(out).to_csv('data/scan_result.csv',index=False)
