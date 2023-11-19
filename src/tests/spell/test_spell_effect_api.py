from .fixture import effects_db
from src.spell.spell_effect.api import SpellEffectApi


def test_get(effects_db):
    """
    Тест получения эффекта для выбранного заклинания и ячейки
    :return:
    """

    effect_api = SpellEffectApi(effects_db)

    # TODO: сделать на параметризованных тестах
    # Базовый случай
    SPELL_ID = 62
    CELL_LEVEL = 2

    effect = effect_api.get(SPELL_ID, CELL_LEVEL)

    assert effect == {
        'effects': {
                'fire': '3d8',
            },
        'half_damage_on_success': True,
    }

    # Должен вернуть корректно посчитанное количество кубиков
    SPELL_ID = 62
    CELL_LEVEL = 3

    # Должен вернуть словарь из эффектов для всех уровней
    SPELL_ID = 62

    # Ошибка - заклинание более высокого уровня
    SPELL_ID = 62
    CELL_LEVEL = 1

    # Обработку заговоров пока что не пишем
