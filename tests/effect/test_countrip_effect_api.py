import pytest

from .fixture import countrip_api
from src.core.error import SpellError


params_get = [
    (396, 1, {'cold': '1d6'}),  # Базовый случай
    (396, 5, {'cold': '2d6'}),  # Должен вернуть корректно посчитанное количество кубиков
    (396, None, {  # Должен вернуть словарь из эффектов для всех уровней для заговора
        '1-4': {'cold': '1d6'},
        '5-10': {'cold': '2d6'},
        '11-16': {'cold': '3d6'},
        '17-20': {'cold': '4d6'},
    }),
]


@pytest.mark.parametrize("spell_id,character_id,expected", params_get)
def test_get(countrip_api, spell_id, character_id, expected):
    """
    Тест для получения эффектов для выбранного заговора
    """
    effect = countrip_api.get(spell_id, character_id)
    assert effect == expected


params_get_errors = [
    (396, 21, 'Invalid character level'),  # Ошибка - персонаж несуществующего уровня
    (396, 0, 'Invalid character level'),  # Ошибка - персонаж несуществующего уровня
    (396, -1, 'Invalid character level'),  # Ошибка - персонаж несуществующего уровня
    (62, 1, 'countrip effect from spell'),  # Ошибка - пытаемся получить данные заговора для заклинания
    (62, None, 'countrip effect from spell'),  # Ошибка - пытаемся получить данные заговора для заклинания
]


@pytest.mark.parametrize("spell_id,cell_level,expected_error", params_get_errors)
def test_get_errors(countrip_api, spell_id, cell_level, expected_error):
    """
    Тест для проверки отработки ошибок
    """
    with pytest.raises(SpellError, match=expected_error):
        countrip_api.get(spell_id, cell_level)
