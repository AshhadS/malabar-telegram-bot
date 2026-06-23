import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import csv
from pathlib import Path

# Loads .env when running locally.
# In GitHub Actions, values will come from GitHub Secrets instead.
load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MALABAR_URL = "https://www.malabargoldanddiamonds.com/ae/malabarprice/index/getrates/"
KUWAIT_TZ = timezone(timedelta(hours=3))


def call_malabar_api():
    params = {
        "country": "KW",
        "state": "Salmiyah"
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.malabargoldanddiamonds.com",
        "referer": "https://www.malabargoldanddiamonds.com/ae/goldprice",
        "user-agent": "Mozilla/5.0",
        "x-requested-with": "XMLHttpRequest",
    }

    response = requests.post(
        MALABAR_URL,
        params=params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    return response.json()

def save_response_to_csv(data):
    csv_file = Path("gold_rates.csv")
    file_exists = csv_file.exists()

    row = {
        "saved_at": datetime.now(KUWAIT_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "location": "Salmiyah, Kuwait",
        "gold_22kt": data.get("22kt", ""),
        "gold_24kt": data.get("24kt", ""),
        "rate_updated_time": data.get("updated_time", "")
    }

    with csv_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

def format_message(data):
    """
    Expected API response example:
    {
        "22kt": "38.35 KWD",
        "24kt": "41.82 KWD",
        "updated_time": "19/06/2026 09:50 AM"
    }
    """

    current_time = datetime.now(KUWAIT_TZ).strftime("%d/%m/%Y %I:%M %p")

    rate_22kt = data.get("22kt", "Not available")
    rate_24kt = data.get("24kt", "Not available")
    updated_time = data.get("updated_time", "Not available")

    message = f"""
🥇 Malabar Gold Rate Update

📍 Location: Salmiyah, Kuwait

22KT Gold: {rate_22kt}
24KT Gold: {rate_24kt}

🕘 Rate Updated: {updated_time}
🤖 Bot Checked: {current_time}
""".strip()

    return message


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()


def main():
    try:
        data = call_malabar_api()

        save_response_to_csv(data)
        print("CSV saved successfully.")

        message = format_message(data)
        send_telegram_message(message)
        print("Telegram message sent successfully.")
        print(message)

    except Exception as e:
        error_message = f"❌ Malabar gold bot failed:\n{e}"
        print(error_message)

        try:
            send_telegram_message(error_message)
        except Exception:
            pass


if __name__ == "__main__":
    main()
