from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseInstance(ABC):
    """
    Датакласс для хранения данных сборной сущности
    """

    def __init__(self, **kwargs):

        self._class_attrs = self.__class__.__dict__['__annotations__'].keys()
        self.add(**kwargs)

    def __repr__(self):

        string_pairs = [f'{key}={getattr(self, key)}' for key in self.__dict__]
        attributes = ', '.join(string_pairs)
        class_name = self.__class__.__name__

        return f'<{class_name}: {attributes}>'

    def add(self, **kwargs):
        """
        Добавление атрибута/тов
        Добавляются только те атрибуты, которые объявлены в переменных класса с указанием типа данных
        """

        for key, value in kwargs.items():
            if key in self._class_attrs:
                setattr(self, key, value)

    def get_public_attributes(self):
        """
        Возвращает словарь публичных свойств объекта
        """

        return {x: y for x, y in self.__dict__.items() if not x.startswith('_')}
