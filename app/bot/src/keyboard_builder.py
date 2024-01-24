"""
Каркас модуля для генерации кнопок и клавиатуры.
"""

from typing import Union

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


class KeyboardBuilder(InlineKeyboardBuilder):
    """
    Класс для генерации кнопок бота.
    Создает объект инлайн-клавиатуры.
    Для использования необходимо в конце компоновки объекта вызвать метод finish().
    """

    def add_url_button(self,
                       text: str,
                       url: str
                       ) -> None:
        """
        Создает и добавляет к объекту клавиатуры url-кнопку.

        :param text: текст, который будет написан на кнопке.
        :param url: url, на который будет отправлен пользователь.
        """
        button = types.InlineKeyboardButton(text=text, url=url)
        self.add(button)

    def add_callback_button(self,
                            text: str,
                            callback_data: Union[str]
                            ) -> None:
        """
        Создает и добавляет к объекту клавиатуры callback-кнопку.

        :param text: текст, который будет написан на кнопке.
        :param callback_data: коллбэк, который будет вызван при нажатии.
        """
        button = types.InlineKeyboardButton(text=text, callback_data=callback_data)
        self.add(button)

    def add_row_button(self,
                       text: str,
                       callback_data: Union[str]
                       ) -> None:
        """
        Создает и добавляет к клавиатуре callback-кнопку во всю ширину ряда.

        :param text: текст, который будет написан на кнопке.
        :param callback_data: коллбэк, который будет вызван при нажатии.
        """
        self.row(types.InlineKeyboardButton(text=text, callback_data=callback_data))

    def finish(self):
        """Возвращает клавиатуру, готовую к использованию."""
        return self.as_markup()
