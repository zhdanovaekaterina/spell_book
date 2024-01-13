# Общие функции для настройки приложения


import logging
from time import time

from src.core import config

logger = logging.getLogger(__name__)


def timetracking(foo):
    """
    Декоратор для трекинга времени выполнения функции
    :param foo:
    :return:
    """

    async def track_time():
        start_time = time()
        logger.info('---Started working---')

        await foo()

        end_time = time()
        total_time = round((end_time - start_time), 3)
        logger.info(f'---Finished in {total_time} s.')

    return track_time


def set_preferences():
    """
    Задаем глобальные настройки модуля логгирования
    :return:
    """

    handlers = []
    console_handler = logging.StreamHandler()
    handlers.append(console_handler)

    logging.basicConfig(
        force=True,
        level=config.log_level,
        format=config.LOG_FORMAT,
        datefmt=config.LOG_DATEFMT,
        handlers=handlers
    )


def snake_to_camel(input_str):
    """
    Конвертирует строку из snake_style в CamelStyle
    :param input_str:
    :return:
    """

    return "".join(x.capitalize() for x in input_str.lower().split("_"))
