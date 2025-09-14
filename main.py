from bot.notifier import send_trade_alert_with_chart
from strategy.live_data_mt5 import connect_to_broker, get_ohlc
import yaml

with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

with open("strategy/pairs.yaml") as f:
    pairs = yaml.safe_load(f)

# Connect to each broker
for broker_name, broker_config in settings["brokers"].items():
    if connect_to_broker(broker_name, broker_config):
        symbols = pairs["justmarkets"] if "justmarkets" in broker_name else pairs["weltrade"]

        for symbol in symbols:
            data = get_ohlc(symbol)
            if data is not None:
                # Example values for testing (replace with SMC logic later)
                entry, sl, tp1, tp2, tp3 = 100, 95, 105, 110, 115
                chart_path = "charts/test.png"  # Replace with actual chart generator later

                send_trade_alert_with_chart(broker_name, symbol, entry, sl, tp1, tp2, tp3, chart_path)
