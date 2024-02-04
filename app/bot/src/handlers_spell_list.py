import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

import functions as f
from keyboard import Keyboard
from callbacks import Paginator, ShowSpells
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

    # storage = await state.get_data()
    # user_id = storage.get('user_id')

    user_id = 1  # TODO: убрать заглушку
    spell_list = Gateway.spell_list_available(user_id)
    page_count = f.get_page_count(spell_list, Keyboard.PAGINATION)

    await state.update_data({
        'spell_data': spell_list,
        'spell_page_count': page_count
    })

    sliced_list = f.slice_list(spell_list, 1, Keyboard.PAGINATION)

    await event.answer(
        'Список доступных заклинаний:',
        reply_markup=Keyboard.spell_list(sliced_list, 1, page_count))


@router.callback_query(ShowSpells.filter())
async def cmd_show_spells(callback: CallbackQuery,
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

            text, keyboard = (
                'Список доступных заклинаний',
                Keyboard.spell_list(sliced_list, page_num, page_count)
            )

    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except TelegramBadRequest:
        pass

    await callback.answer()
