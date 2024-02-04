import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

from keyboard import Keyboard
from callbacks import (ChooseClass)
from gateway import Gateway
from filters import NotRegistered
from states import RegistrationState

# Логгер и роутер
logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


# ############# РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ ##############

@router.message(NotRegistered(), Command(commands=['start']))
async def cmd_choose_class(event: Message,
                           state: FSMContext):
    """
    Обработка приветственного сообщения для новых пользователей
    """

    await state.set_state(RegistrationState.waiting_class)
    await event.answer('Пожалуйста, выберите класс',
                       reply_markup=Keyboard.choose_class())


@router.callback_query(RegistrationState.waiting_class, ChooseClass.filter())
async def cmd_choose_level(callback: CallbackQuery,
                           callback_data: ChooseClass,
                           state: FSMContext):
    """
    Выбор уровня
    """

    # Обновляем данные пользователя
    await state.update_data({
        'user_class': callback_data.chs_class,
    })

    await state.set_state(RegistrationState.waiting_level)
    await callback.message.answer('Введите уровень персонажа (от 1 до 20)')
    await callback.answer()


@router.message(RegistrationState.waiting_level)
async def cmd_register_user(event: Message,
                            state: FSMContext):
    """
    Регистрация пользователя
    """

    # получаем введенный уровень
    user_level = event.text

    # проверка на то что введено валидное значение
    is_valid_level = Gateway.check_valid_level(user_level)
    if not is_valid_level:
        return await event.answer(f'Персонажей уровня {user_level} не бывает. '
                                  f'Пожалуйста, введите корректный уровень.')

    # регистрируем пользователя в системе
    storage = await state.get_data()

    user_class = storage.get('user_class')
    user_id = Gateway.register_user(user_class, user_level)

    # обновляем данные пользователя в хранилище
    await state.update_data({
        'user_id': user_id,
        'level': user_level,
    })

    await state.set_state()
    await event.answer(f'Вы выбрали класс {user_class} уровня {user_level}')


# ############# ИНТЕРФЕЙС ДЛЯ ЗАРЕГИСТРИРОВАННОГО ПОЛЬЗОВАТЕЛЯ ##############

@router.message(Command(commands=['start']))
async def cmd_start(event: Message,
                    state: FSMContext):
    """
    TODO: Стартовый хендлер для зарегистрированных пользователей
    """

    await event.answer('Здесь будет стартовый хендлер '
                       'для зарегистрированных пользователей')
