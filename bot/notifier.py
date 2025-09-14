import requests
import yaml

# Load Telegram settings
with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)

BOT_TOKEN = settings['telegram']['token']
CHAT_ID = settings['telegram']['chat_id']

def send_trade_alert_with_chart(broker, pair, entry, sl, tp1, tp2, tp3, chart_path):
    """
    Sends a trade alert to Telegram with an attached chart.
    """
    message = (
        f"📊 Trade Alert\n\n"
        f"Broker: {broker}\n"
        f"Pair: {pair}\n"
        f"Entry: {entry}\n"
        f"SL: {sl}\n"
        f"TP1: {tp1}\n"
        f"TP2: {tp2}\n"
        f"TP3: {tp3}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(chart_path, "rb") as chart:
        files = {"photo": chart}
        data = {"chat_id": CHAT_ID, "caption": message}
        response = requests.post(url, files=files, data=data)

    if response.status_code != 200:
        print("⚠️ Failed to send alert:", response.text)
