import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import yaml

with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)
MT5_ACCOUNT = settings['mt5']['account']
MT5_PASSWORD = settings['mt5']['password']
MT5_SERVER = settings['mt5']['server']

mt5.initialize(login=MT5_ACCOUNT, password=MT5_PASSWORD, server=MT5_SERVER)

PAIR_MAP = {
    "USDJPY": "USDJPY",
    "GBPUSD": "GBPUSD",
    "XAUUSD": "XAUUSD",
    "SILVER": "XAGUSD",
    "EURUSD": "EURUSD",
    "USDCAD": "USDCAD",
    "CADCHF": "CADCHF",
    "NZDCAD": "NZDCAD",
    "USDNZD": "USDNZD",
    "GBPJPY": "GBPJPY"
}

def get_live_data_mt5(pair, timeframe=mt5.TIMEFRAME_M1, n_candles=1000):
    symbol = PAIR_MAP[pair]
    utc_from = datetime.now() - timedelta(days=1)
    rates = mt5.copy_rates_from(symbol, timeframe, utc_from, n_candles)
    if rates is None:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df[['time','open','high','low','close']]
    return df
