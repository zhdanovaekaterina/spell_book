from aiogram import Bot, Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext


router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command(commands=['start']))
async def cmd_welcome(event: Message):
    """
    Обработка приветственного сообщения
    :param event:
    :return:
    """

    await event.answer('Привет')
