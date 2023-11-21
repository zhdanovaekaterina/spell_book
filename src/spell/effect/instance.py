from src.core.instance import BaseInstance


class EffectInstance(BaseInstance):
    """
    Класс для представления конкретной сущности эффекта заклинания или заговора
    """

    spell_id: int
    spell_level: int
    level: int
    damage_type: str
    dice_count: int
    dice: int
    add_dice_count: int
