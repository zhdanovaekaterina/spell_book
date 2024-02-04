import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

# Логгер и роутер
logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


# ############# ВЫВОД СПИСКА ЗАКЛИНАНИЙ ПОЛЬЗОВАТЕЛЯ ##############

@router.message(Command(commands=['my_spells']))
async def cmd_my_spells(event: Message,
                        state: FSMContext):
    """
    Отображение списка доступных заклинаний для пользователя
    """

    await event.answer('Тут будет список всех заклинаний пользователя')
