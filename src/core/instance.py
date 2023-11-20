from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseInstance(ABC):
    """
    Датакласс для хранения данных сборной сущности
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def add(self, **kwargs):
        """
        Добавление атрибута/тов
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):

        string_pairs = [f'{key}={getattr(self, key)}' for key in self.__dict__]
        attributes = ', '.join(string_pairs)
        class_name = self.__class__.__name__

        return f'<{class_name}: {attributes}>'

