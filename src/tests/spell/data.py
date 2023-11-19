from src.core.db.models import DamageType, SpellEffect, Spell


def effects_data():
    """
    Данные для фикстуры effects_db
    :return:
    """

    return [
        DamageType(
            alias='thunder',
            title='Звук'
        ),
        DamageType(
            alias='force',
            title='Силовое поле'
        ),
        Spell(
            id=62,
            alias='shatter',
            title='Дребезги',
            description='',
            level=2,
            school='',
            time_to_cast='',
            distance='',
            duration='',
            components=1,
            spell_type='',
            spell_mass='',
            spell_roll='',
            source='',
            entity='',
            concentration=False,
            ritual=False,
            is_active=False
        ),
        Spell(
            id=2451,
            alias='gravity_fissure',
            title='Гравитационный разлом',
            description='',
            level=6,
            school='',
            time_to_cast='',
            distance='',
            duration='',
            components=1,
            spell_type='',
            spell_mass='',
            spell_roll='',
            source='',
            entity='',
            concentration=False,
            ritual=False,
            is_active=False
        ),
        SpellEffect(
            id=1,
            spell_id=62,
            dice_count=3,
            add_dice_count=1,
            dice=8,
            damage_type_alias='thunder'
        ),
        SpellEffect(
            id=2,
            spell_id=2451,
            dice_count=8,
            add_dice_count=1,
            dice=8,
            damage_type_alias='force'
        ),
    ]
