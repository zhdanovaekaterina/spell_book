from aiogram.dispatcher.fsm.state import StatesGroup, State


class RegistrationState(StatesGroup):
    """Регистрация нового пользователя"""
    waiting_class = State()
    waiting_level = State()
