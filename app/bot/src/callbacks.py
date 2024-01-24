from enum import Enum

from aiogram.dispatcher.filters.callback_data import CallbackData


class ChooseClass(CallbackData, prefix='choose_class'):
    """Коллбэк для выбора класса"""

    chs_class: str = ''


class SpellAction(Enum):
    """Варианты коллбэков для выборки заклинаний"""

    AVAILABLE = 'available'
    LEARNT = 'learnt'
    PREPARED = 'prepared'


class ChooseAction(CallbackData, prefix='choose_action'):
    """Коллбэк для выборки заклинаний"""

    action: SpellAction
