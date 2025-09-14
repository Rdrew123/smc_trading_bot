import requests
import yaml

with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)
BOT_TOKEN = settings['telegram']['bot_token']
CHAT_ID = settings['telegram']['chat_id']

def send_trade_alert_with_chart(pair, entry, sl, tp1, tp2, tp3, chart_path):
    message = f"📊 Trade Alert\n\nPair: {pair}\nEntry: {entry}\nSL: {sl}\nTP1: {tp1}\nTP2: {tp2}\nTP3: {tp3}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {"photo": open(chart_path, "rb")}
    data = {"chat_id": CHAT_ID, "caption": message}
    requests.post(url, files=files, data=data)
