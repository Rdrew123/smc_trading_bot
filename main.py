from bot.notifier import send_trade_alert_with_chart
from strategy.live_data_mt5 import connect_to_broker, get_ohlc
from strategy.entries import detect_valid_entry_multi_tf
import yaml
import time

# Load config
with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

with open("strategy/pairs.yaml") as f:
    pairs = yaml.safe_load(f)

# Keep track of last alerted candle per symbol to prevent duplicates
last_alerted = {}

# Connect to each broker
for broker_name, broker_config in settings["brokers"].items():
    if connect_to_broker(broker_name, broker_config):
        symbols = pairs["justmarkets"] if "justmarkets" in broker_name else pairs["weltrade"]

        while True:  # Continuous scanning loop
            for symbol in symbols:
                # Pull live OHLC data
                data = get_ohlc(symbol, timeframe=None, num_bars=500)  # timeframe can be adjusted per TF

                if data is not None:
                    # Check for valid SMC entry
                    entry_info = detect_valid_entry_multi_tf(symbol, data, broker_name)

                    # Only alert if a valid entry is detected and it's new
                    if entry_info:
                        candle_id = entry_info.get("candle_id")  # Unique ID per triggering candle
                        if last_alerted.get(symbol) != candle_id:
                            last_alerted[symbol] = candle_id

                            # Send Telegram alert with chart
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

            time.sleep(10)  # Check every 10 seconds (adjust as needed)
