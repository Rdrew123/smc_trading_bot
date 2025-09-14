import MetaTrader5 as mt5

def place_order(symbol, lot, entry, sl, tp, order_type="BUY_LIMIT"):
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": getattr(mt5, order_type),
        "price": entry,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 234000,
        "comment": "SMC Bot Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"⚠️ Failed to place {symbol} order:", result)
    else:
        print(f"✅ Order placed for {symbol}: Entry {entry}, SL {sl}, TP {tp}")
