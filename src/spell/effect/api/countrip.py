import logging

from .api import EffectApi
from src.const import MIN_CHARACTER_LEVEL, MAX_CHARACTER_LEVEL
from src.core.error import SpellError


logger = logging.getLogger(__name__)


class CountripEffectApi(EffectApi):
    """
    Апи для работы с эффектами заговоров
    """

    @staticmethod
    def _check_valid_level(obj):

        if type(obj.level) == int and (obj.level < MIN_CHARACTER_LEVEL or obj.level > MAX_CHARACTER_LEVEL):
            raise SpellError.invalid_character_level(obj.level)

    @staticmethod
    def _check_valid_entity(obj):

        if obj.spell_level > 0:
            raise SpellError.countrip_from_spell()

    @staticmethod
    def _get_all_effects(obj):

        keys = ['1-4', '5-10', '11-16', '17-20']

        effect = {}
        for num, key in enumerate(keys):
            dice_count = obj.dice_count + num * obj.add_dice_count

            effect[key] = {
                obj.damage_type: str(dice_count) + 'd' + str(obj.dice)
            }

        return effect

    @staticmethod
    def _get_effect_for_level(obj):

        if obj.level >= 17:
            dice_count = obj.dice_count + obj.add_dice_count * 3
        elif obj.level >= 11:
            dice_count = obj.dice_count + obj.add_dice_count * 2
        elif obj.level >= 5:
            dice_count = obj.dice_count + obj.add_dice_count
        else:
            dice_count = obj.dice_count

        effect = {
            obj.damage_type: str(dice_count) + 'd' + str(obj.dice)
        }

        return effect
