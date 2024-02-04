import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

# Логгер и роутер
logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


# ############# ОБРАБОТКА ДОЛГОГО ОТДЫХА ##############

@router.message(Command(commands=['long_rest']))
async def cmd_long_rest(event: Message,
                        state: FSMContext):
    """
    Обработка долгого отдыха
    """

    await event.answer('Выполняем долгий отдых')
