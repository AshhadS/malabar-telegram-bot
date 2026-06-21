# Malabar Gold Rate Telegram Bot

This project calls the Malabar Gold and Diamonds gold-rate API for Salmiyah, Kuwait and sends a formatted Telegram message.

## Example Telegram message

```text
🥇 Malabar Gold Rate Update

📍 Location: Salmiyah, Kuwait

22KT Gold: 38.35 KWD
24KT Gold: 41.82 KWD

🕘 Rate Updated: 19/06/2026 09:50 AM
🤖 Bot Checked: 21/06/2026 04:30 PM
```

## Run locally on Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` and rename it to `.env`.

Edit `.env`:

```env
TELEGRAM_BOT_TOKEN=your_real_bot_token
TELEGRAM_CHAT_ID=your_real_chat_id
```

Run:

```bash
python main.py
```

## Schedule on GitHub Actions

Push this folder to GitHub.

Add these secrets:

```text
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

The workflow runs every day at 08:00 AM Kuwait time.

## Notes

Do not commit your `.env` file.
Do not commit your Telegram bot token.
