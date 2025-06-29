import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MEDIA_ROOT = Path(__file__).parent / 'media'
STORAGE_IMG = MEDIA_ROOT / 'storages'
ITEM_IMG = MEDIA_ROOT / 'items'
STORAGE_IMG.mkdir(parents=True, exist_ok=True)
ITEM_IMG.mkdir(parents=True, exist_ok=True)

API_TOKEN = os.getenv('KEEPY_TELEGRAM_TOKEN')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
