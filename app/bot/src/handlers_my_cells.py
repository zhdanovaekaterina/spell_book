import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

# Логгер и роутер
logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


# ############# ВЫВОД ДОСТУПНЫХ ПОЛЬЗОВАТЕЛЮ ЯЧЕЕК ##############

@router.message(Command(commands=['my_cells']))
async def cmd_my_cells(event: Message,
                       state: FSMContext):
    """
    Отображение доступных ячеек для пользователя
    """

    await event.answer('Тут будет список ячеек')
