import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

import functions as f
from keyboard import Keyboard
from callbacks import (ChooseAction, SpellAction, Paginator,
                       ShowSpells)
from gateway import Gateway

# Логгер и роутер
logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


# ############# ВЫВОД СПИСКА ДОСТУПНЫХ ЗАКЛИНАНИЙ ##############

@router.message(Command(commands=['spell_list']))
async def cmd_spell_list(event: Message,
                         state: FSMContext):
    """
    Отображение списка доступных заклинаний для пользователя
    """

    await event.answer('Тут будет список всех заклинаний')


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
