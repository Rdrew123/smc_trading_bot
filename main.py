import time
from bot.notifier import send_trade_alert_with_chart
from strategy.chart import generate_chart
from strategy.live_data import get_live_data
from strategy.entries import detect_valid_entry_multi_tf, get_market_bias, TIMEFRAMES

PAIRS = ["USDJPY","GBPUSD","XAUUSD","SILVER","EURUSD","USDCAD","CADCHF","NZDCAD","USDNZD","GBPJPY"]

while True:
    for pair in PAIRS:
        data_dict = {tf: get_live_data(pair, interval=tf) for tf in TIMEFRAMES}
        market_bias = get_market_bias(data_dict)
        entry_info = detect_valid_entry_multi_tf(data_dict, market_bias)
        if entry_info:
            chart_path = generate_chart(pair, data_dict["1m"])
            send_trade_alert_with_chart(
                pair,
                entry_info['entry'],
                entry_info['sl'],
                entry_info['tp1'],
                entry_info['tp2'],
                entry_info['tp3'],
                chart_path
            )
    time.sleep(60)
