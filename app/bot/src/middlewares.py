import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from gateway import Gateway

logger = logging.getLogger(__name__)


class GetAvailableActionsMiddleware(BaseMiddleware):
    """
    Запрашивает для пользователя доступные списки заклинаний
    и сохраняет их в хранилище.
    Используется как outer-мидлварь
    """

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:

        # Проверяем, не добавлены ли уже доступные действия
        state = data.get('state')
        storage = await state.get_data()
        have_data = bool(storage.get('user_class_action'))

        # Если добавлены, выходим
        if have_data:
            return await handler(event, data)

        # Получаем класс пользователя
        # user_class = storage.get('user_class')
        user_class = 'cleric'  # TODO: убрать заглушку

        # Получаем доступные действия для класса и сохраняем их
        available_action = Gateway.get_available_action(user_class)
        await state.update_data(user_class_action=available_action)
        return await handler(event, data)
