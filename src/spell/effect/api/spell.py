from src.core.error import SpellError
from src.const import MIN_CELL_LEVEL, MAX_CELL_LEVEL
from .api import EffectApi


class SpellEffectApi(EffectApi):
    """
    Апи для работы с эффектами заклинаний
    """

    @staticmethod
    def _check_valid_level(obj):

        if type(obj.level) == int and (obj.level < MIN_CELL_LEVEL or obj.level > MAX_CELL_LEVEL):
            raise SpellError.invalid_cell_level(obj.level)

    @staticmethod
    def _check_valid_entity(obj):

        if obj.spell_level == 0:
            raise SpellError.spell_from_countrip()
        elif type(obj.level) == int and obj.level < obj.spell_level:
            raise SpellError.higher_level(obj.spell_id, obj.spell_level, obj.level)

    @staticmethod
    def _get_all_effects(raw):

        level_difference = MAX_CELL_LEVEL - raw.spell_level

        spell_effect = {}
        for lvl in range(level_difference + 1):
            dice_count = raw.dice_count + lvl * raw.add_dice_count

            spell_effect[raw.spell_level + lvl] = {
                raw.damage_type: str(dice_count) + 'd' + str(raw.dice)
            }

        return spell_effect

    @staticmethod
    def _get_effect_for_level(raw):

        dice_count = 0
        if raw.level == raw.spell_level:
            dice_count = raw.dice_count
        elif raw.level > raw.spell_level:
            level_difference = raw.level - raw.spell_level
            dice_count = raw.dice_count + raw.add_dice_count * level_difference

        spell_effect = {
            raw.damage_type: str(dice_count) + 'd' + str(raw.dice)
        }

        return spell_effect
    