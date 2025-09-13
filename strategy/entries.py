from strategy.structure import detect_swing_high_low, detect_choch_bos
from strategy.order_blocks import detect_order_blocks
from strategy.fvg import detect_fvg

TIMEFRAMES = ["1d","4h","1h","30m","15m","5m","1m"]

def get_market_bias(data_dict):
    for tf in ["1d","4h"]:
        df = data_dict[tf]
        swing_highs, swing_lows = detect_swing_high_low(df)
        last_high, last_low = swing_highs[-1][1], swing_lows[-1][1]
        if df['close'].iloc[-1] > last_high:
            return "bullish"
        elif df['close'].iloc[-1] < last_low:
            return "bearish"
    return "neutral"

def detect_choch_bos_multi_tf(data_dict):
    all_events = {}
    for tf, df in data_dict.items():
        swing_highs, swing_lows = detect_swing_high_low(df)
        choch, bos = detect_choch_bos(df, swing_highs, swing_lows)
        all_events[tf] = {"choch": choch, "bos": bos}
    return all_events

def detect_valid_entry_multi_tf(data_dict, market_bias):
    df_1m = data_dict["1m"]
    choch_bos = detect_choch_bos_multi_tf(data_dict)
    ob = detect_order_blocks(df_1m)
    fvg = detect_fvg(df_1m)

    direction = market_bias
    for level in ob + fvg:
        if level.get('direction', level.get('type', '')) == direction:
            entry_price = df_1m['close'].iloc[-1]
            sl = df_1m['low'].iloc[-1] if direction=="bullish" else df_1m['high'].iloc[-1]
            return {
                "entry": entry_price,
                "sl": sl,
                "tp1": entry_price + 0.5 if direction=="bullish" else entry_price - 0.5,
                "tp2": entry_price + 1 if direction=="bullish" else entry_price - 1,
                "tp3": entry_price + 1.5 if direction=="bullish" else entry_price - 1.5
            }
    return None
