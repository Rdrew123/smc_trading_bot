import requests
import yaml

with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

TOKEN = config["telegram"]["bot_token"]
CHAT_ID = config["telegram"]["chat_id"]

def send_trade_alert(pair, entry, sl, tp1, tp2, tp3):
    message = (
        f"📊 Trade Alert\n\n"
        f"Pair: {pair}\n"
        f"Entry: {entry}\n"
        f"SL: {sl}\n"
        f"TP1: {tp1}\nTP2: {tp2}\nTP3: {tp3}"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})
