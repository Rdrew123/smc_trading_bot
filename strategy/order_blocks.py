def detect_order_blocks(df, lookback=5):
    obs = []
    for i in range(lookback, len(df)-1):
        if df['close'][i+1] > df['high'][i]:
            obs.append({'index': i, 'direction': 'bullish'})
        if df['close'][i+1] < df['low'][i]:
            obs.append({'index': i, 'direction': 'bearish'})
    return obs
