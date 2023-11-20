from src.core.instance import BaseInstance


class SpellEffectInstance(BaseInstance):
    """
    Класс для представления конкретной сущности эффекта заклинания
    """

    spell_id: int
    spell_level: int
    cell_level: int
    damage_type: str
    dice_count: int
    dice: int
    add_dice_count: int
