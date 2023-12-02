from src.core.db.models import DamageType, Effect, Spell


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
        DamageType(
            alias='cold',
            title='Холод'
        ),
        Spell(
            id=62,
            alias='shatter',
            title='Дребезги',
            description='',
            level=2,
            school_alias='',
            time_to_cast_alias='',
            distance_alias='',
            duration_alias='',
            components_alias=1,
            spell_type_alias='',
            spell_mass_alias='',
            spell_roll_alias='',
            source_alias='',
            entity_alias='',
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
            school_alias='',
            time_to_cast_alias='',
            distance_alias='',
            duration_alias='',
            components_alias=1,
            spell_type_alias='',
            spell_mass_alias='',
            spell_roll_alias='',
            source_alias='',
            entity_alias='',
            concentration=False,
            ritual=False,
            is_active=False
        ),
        Spell(
            id=396,
            alias='frostbite',
            title='Обморожение',
            description='',
            level=0,
            school_alias='',
            time_to_cast_alias='',
            distance_alias='',
            duration_alias='',
            components_alias=1,
            spell_type_alias='',
            spell_mass_alias='',
            spell_roll_alias='',
            source_alias='',
            entity_alias='',
            concentration=False,
            ritual=False,
            is_active=False
        ),
        Effect(
            id=1,
            spell_id=62,
            dice_count=3,
            add_dice_count=1,
            dice=8,
            damage_type_alias='thunder'
        ),
        Effect(
            id=2,
            spell_id=2451,
            dice_count=8,
            add_dice_count=1,
            dice=8,
            damage_type_alias='force'
        ),
        Effect(
            id=3,
            spell_id=396,
            dice_count=1,
            add_dice_count=1,
            dice=6,
            damage_type_alias='cold'
        ),
    ]
