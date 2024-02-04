from typing import List, Dict

from keyboard_builder import KeyboardBuilder
from gateway import Gateway
from callbacks import (ChooseClass, ChooseAction, SpellAction, Paginator,
                       ShowSpells)


def obj_getter(func):
    """
    Декоратор, который создает объект клавиатуры,
    передает его методу и возвращает наверх
    """

    def wrapper(*args, **kwargs):
        obj = Keyboard()
        func(obj, *args, **kwargs)
        return obj.finish()

    return wrapper


class Keyboard(KeyboardBuilder):
    """
    Построитель пользовательской клавиатуры
    """

    PAGINATION = 3  # кол-во записей для пагинации
    # TODO: сменить на 10-15 после отладки

    @staticmethod
    @obj_getter
    def choose_class(obj):
        """
        Выбор класса
        """

        # TODO: вынести все обращения к Gateway наружу
        classes = Gateway.get_classes()
        for alias, title in classes.items():
            button = ChooseClass(chs_class=alias).pack()
            obj.add_callback_button(title, button)

    @staticmethod
    @obj_getter
    def choose_action(obj):
        """
        Выбор действия с заклинаниями
        """

        button = ChooseAction(action=SpellAction.LEARN).pack()
        obj.add_callback_button('Изученные заклинания', button)

        button = ChooseAction(action=SpellAction.PREPARE).pack()
        obj.add_callback_button('Подготовленные заклинания', button)

    @staticmethod
    @obj_getter
    def spell_list(obj, spell_list: List[Dict], page_num, page_count):
        """
        Построитель клавиатуры с пагинацией для списка заклинаний
        """

        for spell_item in spell_list:
            button = ShowSpells(action=Paginator.DETAIL, page_num=page_num,
                                spell_alias=spell_item.get('alias')).pack()
            obj.add_row_button(spell_item.get('title'), button)

        if page_num != 1:
            button = (ShowSpells(action=Paginator.PREV, page_num=page_num-1)
                      .pack())
            obj.add_row_button('<-', button)
        else:
            button = (ShowSpells(action=Paginator.NONE, page_num=page_num)
                      .pack())
            obj.add_row_button('--', button)

        button = ShowSpells(action=Paginator.NONE, page_num=page_num).pack()
        obj.add_callback_button(f'{page_num}/{page_count}', button)

        if page_num < page_count:
            button = (ShowSpells(action=Paginator.NEXT, page_num=page_num+1)
                      .pack())
            obj.add_callback_button('->', button)
        else:
            button = (ShowSpells(action=Paginator.NONE, page_num=page_num)
                      .pack())
            obj.add_callback_button('--', button)

    @staticmethod
    @obj_getter
    def spell_detail(obj, prev_page):
        """
        Построитель клавиатуры для детальной страницы заклинания
        """

        button = ShowSpells(action=Paginator.INIT, page_num=prev_page).pack()
        obj.add_callback_button('Назад', button)
