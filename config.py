import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
DATABASE_URL = "sqlite:///heartsync.db"

MAX_PHOTOS = 5
PROFILES_PER_PAGE = 1
SUPER_LIKES_DAILY = 3
SEARCH_RADIUS_KM = 50

INTERESTS_LIST = [
    "🎬 Кино", "🎵 Музыка", "📚 Книги", "🏀 Спорт", "🎮 Игры",
    "✈️ Путешествия", "🍳 Готовка", "🎨 Искусство", "🐶 Животные",
    "🌳 Природа", "💻 Технологии", "🎭 Театр", "🏋️ Фитнес",
    "📸 Фотография", "🎯 Настолки", "🚗 Авто", "🧵 Рукоделие"
]

CITY = "Красноуфимск"