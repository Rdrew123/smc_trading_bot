from bot.notifier import send_trade_alert

if __name__ == "__main__":
    send_trade_alert("USDJPY", "149.50", "149.20", "149.80", "150.10", "150.50")
