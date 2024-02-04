import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

# Логгер и роутер
logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


# ############# ОБРАБОТКА ПОВЫШЕНИЯ УРОВНЯ ##############

@router.message(Command(commands=['level_up']))
async def cmd_level_up(event: Message,
                       state: FSMContext):
    """
    Обработка повышения уровня
    """

    await event.answer('Повышаем уровень персонажа')
