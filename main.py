import time
from bot.notifier import send_trade_alert_with_chart
from strategy.chart import generate_chart
from strategy.live_data import get_live_data
from strategy.entries import detect_valid_entry_multi_tf, get_market_bias, TIMEFRAMES

PAIRS = ["USDJPY","GBPUSD","XAUUSD","SILVER","EURUSD","USDCAD","CADCHF","NZDCAD","USDNZD","GBPJPY"]

# Track last alerted candle index per pair
last_alerted = {pair: None for pair in PAIRS}

while True:
    for pair in PAIRS:
        # Fetch live data for all timeframes
        data_dict = {tf: get_live_data(pair, interval=tf) for tf in TIMEFRAMES}

        # Determine higher timeframe bias
        market_bias = get_market_bias(data_dict)

        # Detect valid SMC entry
        entry_info = detect_valid_entry_multi_tf(data_dict, market_bias)

        if entry_info:
            # Use the latest 1m candle index to track duplicates
            entry_index = data_dict["1m"].index[-1]

            # Send alert only if this entry hasn’t been alerted yet
            if last_alerted[pair] != entry_index:
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
                # Mark this candle as alerted
                last_alerted[pair] = entry_index

    # Wait 60 seconds before next scan
    time.sleep(60)
