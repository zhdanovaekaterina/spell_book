from .db_driver import SpellEffectDatabaseDriver
from src.core.error import SpellError


class SpellEffectApi:
    """
    Апи для работы с эффектами заклинаний
    """

    COUNTRIP_LEVEL = 0
    MIN_CELL_LEVEL = 1
    MAX_CELL_LEVEL = 9

    def __init__(self, db: SpellEffectDatabaseDriver):
        self.db = db

    def get(self, spell_id: int, cell_level: int | None = None):
        """
        Получение эффекта для выбранного заклинания и уровня ячейки.
        Если уровень не передан, возвращаются все доступные эффекты всех ячеек.
        :param spell_id:
        :param cell_level:
        :return:
        :raise: SpellError
        """

        # TODO: рефакторинг

        if type(cell_level) == int and (cell_level < self.COUNTRIP_LEVEL or cell_level > self.MAX_CELL_LEVEL):
            raise SpellError(f'Invalid cell level provided: {cell_level}; '
                             f'must be between {self.COUNTRIP_LEVEL} and {self.MAX_CELL_LEVEL}')

        raw = self.db.get_spell_effect(spell_id)

        if raw is None:
            raise SpellError(f'Spell with ID {spell_id} not found')

        dice_count = 0

        if cell_level is None:
            base_dice_count = raw.get('dice_count')
            add_dice_count = raw.get('add_dice_count')
            level_difference = self.MAX_CELL_LEVEL - raw.get('spell_level')

            spell_effect = {}
            for lvl in range(level_difference + 1):
                dice_count = base_dice_count + lvl * add_dice_count

                spell_effect[raw.get('spell_level') + lvl] = {
                    raw.get('damage_type'): str(dice_count) + 'd' + str(raw.get('dice'))
                }

        else:
            if cell_level == 0 and raw.get('spell_level') > 0:
                raise SpellError('You are trying to get countrip effect from spell')
            elif cell_level > 0 and raw.get('spell_level') == 0:
                raise SpellError('You are trying to get spell effect from countrip')

            if cell_level == raw.get('spell_level'):
                dice_count = raw.get('dice_count')
            elif cell_level > raw.get('spell_level'):
                base_dice_count = raw.get('dice_count')
                add_dice_count = raw.get('add_dice_count')
                level_difference = cell_level - raw.get('spell_level')
                dice_count = base_dice_count + add_dice_count * level_difference
            elif cell_level < raw.get('spell_level'):
                spell_level = raw.get('spell_level')
                raise SpellError(f'This spell has higher base cell level; spell ID: {spell_id}, '
                                 f'spell level: {spell_level}, you asked for level {cell_level}')

            spell_effect = {
                raw.get('damage_type'): str(dice_count) + 'd' + str(raw.get('dice'))
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
    