import logging
from typing import Union, Dict, Any

from aiogram.dispatcher.filters import BaseFilter
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

logger = logging.getLogger(__name__)


class NotRegistered(BaseFilter):
    """
    Фильтр проверяет, зарегистрирован ли пользователь по полю user_id
    Если нет, возвращает True
    """

    async def __call__(self,
                       event: Message,
                       state: FSMContext
                       ) -> Union[bool, Dict[str, Any]]:

        data_storage = await state.get_data()
        is_registered = data_storage.get('user_id')
        return not is_registered