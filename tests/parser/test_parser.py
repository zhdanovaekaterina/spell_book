import pytest

from src.parser.parser import Parser
from .data import parsed_list, params_for_detail_raw
from .fixture import fake_parser


def test_parse_spell_list():
    """
    Тест парсинга данных заклинаний из списка
    :return:
    """
    parser = Parser()
    spell_list = parser.parse_list('tests/data/fake_spell_list.html')

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


@pytest.mark.asyncio
@pytest.mark.parametrize("path,expected", params_for_detail_raw())
async def test_parse_spell_detail(fake_parser, path, expected):
    """
    Тест парсинга данных детальной страницы
    :return:
    """

    data = await fake_parser.parse_detail_raw(path)
    assert data == expected
