from enum import Enum

from aiogram.dispatcher.filters.callback_data import CallbackData


class ChooseClass(CallbackData, prefix='choose_class'):
    """Коллбэк для выбора класса"""

    chs_class: str = ''


class SpellAction(Enum):
    """Варианты коллбэков для выборки заклинаний"""

    LEARN = 'learnt'
    PREPARE = 'prepared'
    BOTH = 'both'


class ChooseAction(CallbackData, prefix='choose_action'):
    """Коллбэк для выборки заклинаний"""

    action: SpellAction


class Paginator(Enum):
    """Варианты коллбэков для пагинатора"""

    INIT = 'init'
    PREV = 'prev'
    NEXT = 'next'
    NONE = 'none'  # заглушка для вывода номера страницы
    DETAIL = 'detail'


class ShowSpells(CallbackData, prefix='show_spells'):
    """Коллбэк для показа заклинаний с пагинацией"""

    action: Paginator
    page_num: int = 1
    spell_alias: str | None = None
