from .db_driver import SpellEffectDatabaseDriver
from src.core.error import SpellError
from .instance import SpellEffectInstance
from ...const import COUNTRIP_LEVEL, MAX_CELL_LEVEL


class SpellEffectApi:
    """
    Апи для работы с эффектами заклинаний
    """

    def __init__(self, db: SpellEffectDatabaseDriver):
        self.db = db

    def get(self, spell_id: int, cell_level: int | None = None):
        """
        Получение эффекта для выбранного заклинания и уровня ячейки.
        Если уровень не передан, возвращаются все доступные эффекты всех ячеек.
        :param spell_id:
        :param cell_level:
        :return: dict
                Если ячейка передана, возвращается словарь вида
                    {'<тип урона>': '<кол-во кубиков>'}
                    например, {'thunder': '3d8'}
                Если ячейка не передана, возвращаются все доступные эффекты
                    в разбивке по ячейкам вида
                    {
                        1: {'<тип урона>': '<кол-во кубиков>'},
                        ...,
                        9: {'<тип урона>': '<кол-во кубиков>'},
                    }
                    начиная с уровня заклинания

        :raise: SpellError
        """

        obj = SpellEffectInstance(spell_id=spell_id, cell_level=cell_level)

        self._check_valid_cell(obj)  # Проверяем что передана валидная ячейка
        self.db.get_spell_effect(obj)  # Получаем данные из базы и дополняем объект

        if cell_level is None:  # Если нет уровня ячейки, возвращаем все эффекты
            spell_effect = self._get_all_effects_for_spell(obj)
        else:  # Иначе возвращаем эффект для выбранного уровня ячейки
            self._check_valid_level(obj)
            spell_effect = self._get_effect_for_cell_level(obj)

        if not spell_effect:  # Если в конце эффект не получен, что-то пошло не так, зовем ошибку
            raise SpellError.internal_error()

        return spell_effect

    @staticmethod
    def _check_valid_cell(obj):
        """
        Проверка является ли уровень ячейки валидным
        :return:
        :raise: SpellError
        """
        if type(obj.cell_level) == int and (obj.cell_level < COUNTRIP_LEVEL or obj.cell_level > MAX_CELL_LEVEL):
            raise SpellError.invalid_cell_level(obj.cell_level)

    @staticmethod
    def _check_valid_level(raw):
        """
        Проверка является ли корректным переданный уровень ячейки
        в зависимости от конкретного заклинания
        :param raw:
        :return:
        :raise: SpellError
        """
        if raw.cell_level == 0 and raw.spell_level > 0:
            raise SpellError.countrip_from_spell()
        elif raw.cell_level > 0 and raw.spell_level == 0:
            raise SpellError.spell_from_countrip()
        elif raw.cell_level < raw.spell_level:
            raise SpellError.higher_level(raw.spell_id, raw.spell_level, raw.cell_level)

    @staticmethod
    def _get_all_effects_for_spell(raw):
        """
        Получение всех эффектов для заклинания
        :return:
        """

        level_difference = MAX_CELL_LEVEL - raw.spell_level

        spell_effect = {}
        for lvl in range(level_difference + 1):
            dice_count = raw.dice_count + lvl * raw.add_dice_count

            spell_effect[raw.spell_level + lvl] = {
                raw.damage_type: str(dice_count) + 'd' + str(raw.dice)
            }

        return spell_effect

    @staticmethod
    def _get_effect_for_cell_level(raw):
        """
        Получение эффекта для конкретного уровня ячейки
        :return:
        :raise: SpellError
        """

        dice_count = 0
        if raw.cell_level == raw.spell_level:
            dice_count = raw.dice_count
        elif raw.cell_level > raw.spell_level:
            level_difference = raw.cell_level - raw.spell_level
            dice_count = raw.dice_count + raw.add_dice_count * level_difference

        spell_effect = {
            raw.damage_type: str(dice_count) + 'd' + str(raw.dice)
        }

        return spell_effect

    def add(self, spell_id: int, spell_effect: dict):
        """
        Добавление нового эффекта для заклинания
        :param spell_id:
        :param spell_effect:
        :return:
        """
        pass
    