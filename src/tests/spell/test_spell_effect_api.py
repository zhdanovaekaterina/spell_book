from .fixture import effects_db
from src.spell.spell_effect.spell_effect_api import SpellEffectApi


def test_get(effects_db):
    """
    Тест получения эффекта для выбранного заклинания и ячейки
    :return:
    """

    # TODO: сделать на параметризованных тестах
    # Базовый случай
    SPELL_ID = 62
    CELL_LEVEL = 2

    effect_api = SpellEffectApi(effects_db)

    effect = effect_api.get(SPELL_ID, CELL_LEVEL)

    assert effect == {
        'effects': {
                'fire': '3d8',
            },
        'half_damage_on_success': True,
    }

    # Ошибка - заклинание более высокого уровня
    SPELL_ID = 62
    CELL_LEVEL = 1

    # Должен вернуть корректно посчитанное количество кубиков
    SPELL_ID = 62
    CELL_LEVEL = 3

    # Обработку заговоров пока что не пишем
