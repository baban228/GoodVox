import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка наличия токена
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Необходимо указать TELEGRAM_BOT_TOKEN в .env файле")


DEBUG = True
T2S_USE = False

CLAR_REPEATS = 3

BASE_DIR = Path(__file__).parent.parent
MEDIA_DIR = BASE_DIR / 'media'
