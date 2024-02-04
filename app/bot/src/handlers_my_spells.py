import logging

from aiogram import Router, F
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

import functions as f
from keyboard import Keyboard
from gateway import Gateway
from filters import CanLearnAndPrepare
from callbacks import ChooseAction
from middlewares import GetAvailableActionsMiddleware

# Логгер, роутер и мидлварь
logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")
router.message.outer_middleware(GetAvailableActionsMiddleware())


# ############# ВЫВОД СПИСКА ЗАКЛИНАНИЙ ПОЛЬЗОВАТЕЛЯ ##############

@router.message(CanLearnAndPrepare(), Command(commands=['my_spells']))
async def cmd_my_spells_both(event: Message,
                             state: FSMContext):
    """
    Отображение клавиатуры для выбора между изученными и
    подготовленными заклинаниями
    """

    await event.answer('Выберите, какие заклинания вы хотите просмотреть',
                       reply_markup=Keyboard.choose_action())


@router.message(Command(commands=['my_spells']))
async def cmd_my_spells_command(event: Message,
                                state: FSMContext):
    """
    Отображение списка доступных заклинаний для пользователя по команде
    """

    storage = await state.get_data()
    # user_id = storage.get('user_id')

    user_id = 1  # TODO: убрать заглушку
    available_action = storage.get('user_class_action')

    spell_list = Gateway.user_spell_list(user_id, available_action)
    await show_user_spells(event, spell_list)


@router.callback_query(ChooseAction.filter())
async def cmd_my_spells_callback(callback: CallbackQuery,
                                 callback_data: ChooseAction,
                                 state: FSMContext):
    """
    Отображение списка доступных заклинаний для пользователя по коллбэку
    """

    # storage = await state.get_data()
    # user_id = storage.get('user_id')

    user_id = 1  # TODO: убрать заглушку

    spell_list = Gateway.user_spell_list(user_id, callback_data.action)
    await show_user_spells(callback.message, spell_list)
    await callback.answer()


async def show_user_spells(message, spell_list):
    """
    Отображение списка заклинаний для пользователя
    """

    page_count = f.get_page_count(spell_list, Keyboard.PAGINATION)
    sliced_list = f.slice_list(spell_list, 1, Keyboard.PAGINATION)

    await message.answer(
        'Список заклинаний:',
        reply_markup=Keyboard.spell_list(sliced_list, 1, page_count)
    )

    # TODO: навигация по списку
