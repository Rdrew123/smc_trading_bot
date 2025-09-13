import yfinance as yf

PAIR_MAP = {
    "USDJPY": "USDJPY=X",
    "GBPUSD": "GBPUSD=X",
    "XAUUSD": "XAUUSD=X",
    "SILVER": "SILVER=X",
    "EURUSD": "EURUSD=X",
    "USDCAD": "USDCAD=X",
    "CADCHF": "CADCHF=X",
    "NZDCAD": "NZDCAD=X",
    "USDNZD": "USDNZD=X",
    "GBPJPY": "GBPJPY=X"
}

def get_live_data(pair, interval="1m", period="1d"):
    df = yf.download(PAIR_MAP[pair], interval=interval, period=period)
    df = df[['Open','High','Low','Close']]
    df.columns = ['open','high','low','close']
    df.reset_index(inplace=True)
    return df
