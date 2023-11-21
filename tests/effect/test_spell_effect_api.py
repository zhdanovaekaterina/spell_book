import pytest

from .fixture import spell_api
from src.core.error import SpellError


params_get = [
    (62, 2, {'thunder': '3d8'}),  # Базовый случай
    (62, 3, {'thunder': '4d8'}),  # Должен вернуть корректно посчитанное количество кубиков
    (2451, None, {  # Должен вернуть словарь из эффектов для всех уровней
        6: {'force': '8d8'},
        7: {'force': '9d8'},
        8: {'force': '10d8'},
        9: {'force': '11d8'},
    }),
]


@pytest.mark.parametrize("spell_id,cell_level,expected", params_get)
def test_get(spell_api, spell_id, cell_level, expected):
    """
    Тест получения эффекта для выбранного заклинания и ячейки
    """
    effect = spell_api.get(spell_id, cell_level)
    assert effect == expected


params_get_errors = [
    (62, 1, 'higher base cell level'),  # Ошибка - заклинание более высокого уровня
    (62, 10, 'Invalid cell level'),  # Ошибка - заклинание несуществующего уровня
    (62, -1, 'Invalid cell level'),  # Ошибка - заклинание несуществующего уровня
    (62, 0, 'Invalid cell level'),  # Ошибка - заклинание несуществующего уровня
    (396, 1, 'spell effect from countrip'),  # Ошибка - пытаемся получить данные заклинания для заговора
    (396, None, 'spell effect from countrip'),  # Ошибка - пытаемся получить данные заклинания для заговора
    (1, None, 'not found'),  # Ошибка - заклинание не существует
]


@pytest.mark.parametrize("spell_id,cell_level,expected_error", params_get_errors)
def test_get_errors(spell_api, spell_id, cell_level, expected_error):
    """
    Тест для проверки отработки ошибок
    """

    with pytest.raises(SpellError, match=expected_error):
        spell_api.get(spell_id, cell_level)
