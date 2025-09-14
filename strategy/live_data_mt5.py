import MetaTrader5 as mt5
import yaml

with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

def connect_to_broker(broker_name, broker_config):
    if not mt5.initialize(server=broker_config["server"], login=broker_config["login"], password=broker_config["password"]):
        print(f"⚠️ Failed to connect to {broker_name}: {mt5.last_error()}")
        return False
    print(f"✅ Connected to {broker_name}")
    return True

def get_ohlc(symbol, timeframe=mt5.TIMEFRAME_M5, num_bars=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)
    return rates
