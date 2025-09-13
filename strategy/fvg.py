def detect_fvg(df):
    fvg = []
    for i in range(1, len(df)-1):
        if df['low'][i] > df['close'][i-1]:
            fvg.append({'index': i, 'type': 'bullish'})
        if df['high'][i] < df['close'][i-1]:
            fvg.append({'index': i, 'type': 'bearish'})
    return fvg
