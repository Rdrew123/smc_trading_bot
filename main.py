import time
import yaml
from bot.notifier import send_trade_alert_with_chart
from strategy.live_data_mt5 import connect_to_broker, get_ohlc, TIMEFRAMES
from strategy.entries import detect_valid_entry_multi_tf
import MetaTrader5 as mt5

# Map string TFs to MT5 timeframes
TF_MAPPING = {
    "1d": mt5.TIMEFRAME_D1,
    "4h": mt5.TIMEFRAME_H4,
    "1h": mt5.TIMEFRAME_H1,
    "30m": mt5.TIMEFRAME_M30,
    "15m": mt5.TIMEFRAME_M15,
    "5m": mt5.TIMEFRAME_M5,
    "1m": mt5.TIMEFRAME_M1
}

# Load configs
with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

with open("strategy/pairs.yaml") as f:
    pairs = yaml.safe_load(f)

last_alerted = {}  # prevent duplicate alerts

# Connect to each broker
for broker_name, broker_config in settings["brokers"].items():
    if connect_to_broker(broker_name, broker_config):
        symbols = pairs["justmarkets"] if "justmarkets" in broker_name else pairs["weltrade"]

        while True:  # continuous scanning loop
            for symbol in symbols:
                # Build data_dict with all TFs
                data_dict = {}
                for tf in TIMEFRAMES:
                    df = get_ohlc(symbol, timeframe=TF_MAPPING[tf], num_bars=500)
                    if df is not None and not df.empty:
                        data_dict[tf] = df

                if not data_dict:
                    continue

                # Detect valid SMC entry
                entry_info = detect_valid_entry_multi_tf(symbol, data_dict, broker_name)

                if entry_info:
                    candle_id = entry_info["candle_id"]
                    if last_alerted.get(symbol) != candle_id:
                        last_alerted[symbol] = candle_id
                        send_trade_alert_with_chart(
                            broker=broker_name,
                            pair=symbol,
                            entry=entry_info["entry"],
                            sl=entry_info["sl"],
                            tp1=entry_info["tp1"],
                            tp2=entry_info.get("tp2"),
                            tp3=entry_info.get("tp3"),
                            chart_path=entry_info["chart_path"]
                        )

            time.sleep(10)  # adjust as needed
