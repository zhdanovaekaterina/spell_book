# Импортируем переменные окружения и задаем остальные константы

from os import getenv

from dotenv import load_dotenv

load_dotenv()

# Настройки телеграм
BOT_TOKEN = getenv("BOT_TOKEN")
