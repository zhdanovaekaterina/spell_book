from keyboard_builder import KeyboardBuilder
from gateway import Gateway
from callbacks import ChooseClass, ChooseAction, SpellAction


def obj_getter(func):
    """
    Декоратор, который создает объект клавиатуры, передает его методу и возвращает
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

    @staticmethod
    @obj_getter
    def choose_class(obj):
        """
        Выбор класса
        """

        classes = Gateway.get_classes()
        for alias, title in classes.items():
            button = ChooseClass(chs_class=alias).pack()
            obj.add_callback_button(title, button)

    @staticmethod
    @obj_getter
    def choose_action(obj, user_class):
        """
        Выбор действия с заклинаниями
        """

        button = ChooseAction(action=SpellAction.AVAILABLE).pack()
        obj.add_callback_button('Доступные заклинания', button)

        available_actions = Gateway.get_available_actions(user_class)
        print(available_actions)

        if available_actions.get('learn'):
            button = ChooseAction(action=SpellAction.LEARNT).pack()
            obj.add_callback_button('Изученные заклинания', button)

        if available_actions.get('prepare'):
            button = ChooseAction(action=SpellAction.PREPARED).pack()
            obj.add_callback_button('Подготовленные заклинания', button)
