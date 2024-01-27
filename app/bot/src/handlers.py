import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

import functions as f
from keyboard import Keyboard
from callbacks import (ChooseClass, ChooseAction, SpellAction, Paginator,
                       ShowSpells)
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
    available_actions = Gateway.get_available_actions(user_class)

    # обновляем данные пользователя в хранилище
    await state.update_data({
        'user_id': user_id,
        'level': user_level,
        'user_class_properties': available_actions
    })

    await state.set_state()
    await event.answer(f'Вы выбрали класс {user_class} уровня {user_level}',
                       reply_markup=Keyboard.choose_action(available_actions))


# ############# ИНТЕРФЕЙС ДЛЯ ЗАРЕГИСТРИРОВАННОГО ПОЛЬЗОВАТЕЛЯ ##############

@router.message(Command(commands=['start']))
async def cmd_choose_class(event: Message,
                           state: FSMContext):
    """
    Стартовый хендлер для зарегистрированных пользователей
    """

    await event.answer('Здесь будет стартовый хендлер '
                       'для зарегистрированных пользователей')


@router.callback_query(ChooseAction.filter())
async def cmd_choose_action(callback: CallbackQuery,
                            callback_data: ChooseAction,
                            state: FSMContext):
    """
    Показ запрошенного списка заклинаний
    """

    action = callback_data.action

    storage = await state.get_data()
    user_id = storage.get('user_id')

    match action:
        case SpellAction.AVAILABLE:
            spell_list = Gateway.spell_list_available(user_id)
        case SpellAction.LEARNT:
            spell_list = Gateway.spell_list_learned(user_id)
        case SpellAction.PREPARED:
            spell_list = Gateway.spell_list_prepared(user_id)
        case _:
            # TODO: заменить внятной обработкой
            raise Exception('Произошла ошибка')

    page_count = f.get_page_count(spell_list, Keyboard.PAGINATION)

    await state.update_data({
        'spell_data': spell_list,
        'spell_page_count': page_count
    })

    sliced_list = f.slice_list(spell_list, 1, Keyboard.PAGINATION)

    await callback.message.answer(
        f'Список {action} заклинаний:',
        reply_markup=Keyboard.spell_list(sliced_list, 1, page_count))
    await callback.answer()


@router.callback_query(ShowSpells.filter())
async def cmd_test_keyboard(callback: CallbackQuery,
                            callback_data: ShowSpells,
                            state: FSMContext):
    """
    Обработка запроса данных заклинаний
    """

    # TODO: двухуровневая списковая с выбором уровня заклинаний

    action = callback_data.action
    page_num = callback_data.page_num

    match action:
        case Paginator.DETAIL:
            spell_alias = callback_data.spell_alias
            text, keyboard = (f'Детальный текст заклинания {spell_alias}',
                              Keyboard.spell_detail(page_num))
        case _:
            storage = await state.get_data()
            spell_list = storage.get('spell_data')
            page_count = storage.get('spell_page_count')
            sliced_list = f.slice_list(spell_list, page_num,
                                       Keyboard.PAGINATION)

            text, keyboard = 'Список заклинаний', Keyboard.spell_list(
                sliced_list, page_num, page_count
            )

    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except TelegramBadRequest:
        pass

    await callback.answer()

    # TODO: прописать выход наверх
