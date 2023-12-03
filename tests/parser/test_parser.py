from src.parser.parser import Parser
from .data import parsed_list


def test_parse_spell_list():
    """
    Тест парсинга данных заклинаний из списка
    :return:
    """
    parser = Parser()
    spell_list = parser.parse_list('tests/parser/fake_spell_list.html')

    target_data = parsed_list()

    # Проверяем структуру данных
    assert spell_list[0] == target_data[0]

    # Проверяем парсинг компонентов
    assert spell_list[1]['components_alias'] == 'vsm'
    assert spell_list[2]['components_alias'] == '-s-'

    # Проверяем парсинг метки концентрации
    assert spell_list[1]['concentration'] is True
    assert spell_list[0]['concentration'] is False

    # Проверяем парсинг метки ритуала
    assert spell_list[2]['ritual'] is True
    assert spell_list[0]['ritual'] is False
