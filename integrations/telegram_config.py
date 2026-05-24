"""Telegram Bot Configuration"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot token and settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_HANDLE = os.getenv("TELEGRAM_BOT_HANDLE", "")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")

print("Telegram Bot configuration loaded successfully!")
