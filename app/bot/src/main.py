# Точка входа в приложение

import time
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramRetryAfter, TelegramConflictError
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

import handlers
import config as c


def create_bot_and_dp():

    # Конфигурация бота
    bot = Bot(token=c.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры
    dp.include_router(handlers.router)

    return bot, dp


async def main(bot, dp):

    # Запускаем бота
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    bot, dp = create_bot_and_dp()

    while True:
        try:
            asyncio.run(main(bot, dp))
        except TelegramRetryAfter as exception:
            time.sleep(exception.retry_after)
        except TelegramConflictError as exception:
            time.sleep(5)
