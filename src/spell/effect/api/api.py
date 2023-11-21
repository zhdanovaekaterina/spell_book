from abc import ABC, abstractmethod

from src.spell.effect.db_driver import EffectDatabaseDriver
from src.spell.effect.instance import EffectInstance
from src.core.error import SpellError


class EffectApi(ABC):

    def __init__(self, db: EffectDatabaseDriver):
        self.db = db

    def get(self, spell_id: int, level: int | None = None):
        """
        Получение эффекта для выбранного заклинания/заговора и уровня.
        Для заклинания требуется уровень ячейки, для заговора - уровень персонажа.
        Если уровень не передан, возвращаются все доступные эффекты всех уровней.
        :param spell_id:
        :param level:
        :return: dict
            Если уровень передан, возвращается словарь вида
                {'<тип урона>': '<кол-во кубиков>'}
                например, {'thunder': '3d8'}
            Если уровень не передан, возвращаются все доступные эффекты в разбивке
                по уровням, для заклинаний вида
                {
                    1: {'<тип урона>': '<кол-во кубиков>'},
                    ...,
                    9: {'<тип урона>': '<кол-во кубиков>'},
                }
                начиная с уровня заклинания; для заговоров вида
                {
                    '1-4': {'<тип урона>': '<кол-во кубиков>'},
                    ...,
                    '17-20': {'<тип урона>': '<кол-во кубиков>'},
                }
                где ключами являются диапазоны уровней персонажа

        :raise: SpellError
        """

        obj = EffectInstance(spell_id=spell_id, level=level)

        self._check_valid_level(obj)  # Проверяем что передан валидный уровень
        self.db.get_effect(obj)  # Получаем данные из базы и дополняем объект
        self._check_valid_entity(obj)  # Проверяем что получена корректная сущность

        if level is None:  # Если не передан нужный уровень, возвращаем все эффекты
            effect = self._get_all_effects(obj)
        else:  # Иначе возвращаем эффект для выбранного уровня
            effect = self._get_effect_for_level(obj)

        if not effect:  # Если в конце эффект не получен, что-то пошло не так, зовем ошибку
            raise SpellError.internal_error()

        return effect

    @staticmethod
    @abstractmethod
    def _check_valid_entity(obj):
        """
        Проверка является ли переданный уровень валидным
        :return:
        :raise: SpellError
        """

    @staticmethod
    @abstractmethod
    def _get_all_effects(obj):
        """
        Получение всех эффектов
        :return:
        """

    @staticmethod
    @abstractmethod
    def _check_valid_level(obj):
        """
        Проверка является ли корректным переданный уровень
        в зависимости от конкретного заклинания/заговора
        :param obj:
        :return:
        :raise: SpellError
        """

    @staticmethod
    @abstractmethod
    def _get_effect_for_level(obj):
        """
        Получение эффекта для конкретного уровня
        :return:
        :raise: SpellError
        """
