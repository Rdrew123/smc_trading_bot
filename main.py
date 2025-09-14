import time
from bot.notifier import send_trade_alert_with_chart
from strategy.mt5_orders import place_pending_order
from strategy.chart import generate_chart
from strategy.live_data_mt5 import get_live_data_mt5
from strategy.entries import detect_valid_entry_multi_tf, get_market_bias, TIMEFRAMES
import MetaTrader5 as mt5
import yaml

with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

PAIRS = ["USDJPY","GBPUSD","XAUUSD","SILVER","EURUSD","USDCAD","CADCHF","NZDCAD","USDNZD","GBPJPY"]
TIMEFRAME_MAP = {"1m": mt5.TIMEFRAME_M1,"5m": mt5.TIMEFRAME_M5,"15m": mt5.TIMEFRAME_M15,"30m": mt5.TIMEFRAME_M30,"1h": mt5.TIMEFRAME_H1,"4h": mt5.TIMEFRAME_H4,"1d": mt5.TIMEFRAME_D1}

last_alerted = {pair: None for pair in PAIRS}

while True:
    for pair in PAIRS:
        data_dict = {tf: get_live_data_mt5(pair, timeframe=TIMEFRAME_MAP[tf]) for tf in TIMEFRAMES}
        market_bias = get_market_bias(data_dict)
        entry_info = detect_valid_entry_multi_tf(data_dict, market_bias)

        if entry_info:
            entry_index = data_dict["1m"].index[-1]
            if last_alerted[pair] != entry_index:
                chart_path = generate_chart(pair, data_dict["1m"])

                # 1️⃣ Telegram alert
                send_trade_alert_with_chart(
                    pair,
                    entry_info['entry'],
                    entry_info['sl'],
                    entry_info['tp1'],
                    entry_info['tp2'],
                    entry_info['tp3'],
                    chart_path
                )

                # 2️⃣ Place pending MT5 order
                order_type = "buy" if market_bias=="bullish" else "sell"
                place_pending_order(
                    pair=pair,
                    order_type=order_type,
                    price=entry_info['entry'],
                    sl=entry_info['sl'],
                    tp=entry_info['tp1'],
                    volume=0.1
                )

                last_alerted[pair] = entry_index
    time.sleep(60)
