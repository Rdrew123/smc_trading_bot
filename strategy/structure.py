def detect_swing_high_low(df, lookback=20):
    swing_highs, swing_lows = [], []
    for i in range(lookback, len(df)-lookback):
        if df['high'][i] == max(df['high'][i-lookback:i+lookback]):
            swing_highs.append((i, df['high'][i]))
        if df['low'][i] == min(df['low'][i-lookback:i+lookback]):
            swing_lows.append((i, df['low'][i]))
    return swing_highs, swing_lows

def detect_choch_bos(df, swing_highs, swing_lows):
    choch_events, bos_events = [], []
    for i in range(1, len(df)):
        if swing_highs and df['close'][i] > swing_highs[-1][1]:
            choch_events.append({'index': i, 'direction': 'bullish'})
            bos_events.append({'index': i, 'type': 'break_structure', 'direction': 'bullish'})
        if swing_lows and df['close'][i] < swing_lows[-1][1]:
            choch_events.append({'index': i, 'direction': 'bearish'})
            bos_events.append({'index': i, 'type': 'break_structure', 'direction': 'bearish'})
    return choch_events, bos_events
