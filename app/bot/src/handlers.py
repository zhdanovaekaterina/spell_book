from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

from keyboard import Keyboard
from callbacks import ChooseClass


router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command(commands=['start']))
async def cmd_choose_class(event: Message):
    """
    Обработка приветственного сообщения
    """

    await event.answer('Пожалуйста, выберите класс', reply_markup=Keyboard.choose_class())


@router.callback_query(ChooseClass.filter())
async def cmd_save_class(callback: CallbackQuery, callback_data: ChooseClass, state: FSMContext):
    """
    Сохранение выбранного класса для пользователя
    """

    # сохраняем класс в хранилище
    await state.update_data({
        'user_class': callback_data.chs_class
    })

    await callback.message.answer(f'Вы выбрали класс {callback_data.chs_class}')
    await callback.answer()


@router.message(Command(commands=['my_class']))
async def cmd_my_class(event: Message, state: FSMContext):
    """
    Получение данных класса пользователем
    """

    user_data = await state.get_data()
    user_class = user_data.get('user_class')

    # TODO: не работает клавиатура здесь
    await event.answer(f'Ваш класс: {user_class}', reply_markup=Keyboard.choose_action(user_class))

