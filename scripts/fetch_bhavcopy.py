import pandas as pd, requests, zipfile, io
from datetime import datetime

def fetch():
    d=datetime.now().strftime('%d%m%Y')
    y=datetime.now().year
    m=datetime.now().strftime('%b').upper()
    url=f'https://archives.nseindia.com/content/historical/EQUITIES/{y}/{m}/cm{d}bhav.csv.zip'
    r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    z=zipfile.ZipFile(io.BytesIO(r.content))
    df=pd.read_csv(z.open(z.namelist()[0]))
    return df[df.SERIES=='EQ']
