# Точка входа в приложение

import time
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramRetryAfter, TelegramConflictError
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

import handlers_start
import handlers_spell_list
import handlers_my_spells
import handlers_my_cells
import handlers_long_rest
import handlers_level_up

import config as c


def create_bot_and_dp():

    # Конфигурация бота
    bot = Bot(token=c.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры
    dp.include_router(handlers_start.router)
    dp.include_router(handlers_spell_list.router)
    dp.include_router(handlers_my_spells.router)
    dp.include_router(handlers_my_cells.router)
    dp.include_router(handlers_long_rest.router)
    dp.include_router(handlers_level_up.router)

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
