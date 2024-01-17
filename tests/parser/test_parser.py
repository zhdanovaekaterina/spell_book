from pathlib import Path
from pprint import pprint

import pytest

from src.parser.parser import Parser
from src.helpers.file_helper import FileHelper
from .data import parsed_list, params_for_detail_raw, params_for_csv_saving
from .fixture import fake_parser, temp_dir, multilist


@pytest.mark.dependency()
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


@pytest.mark.dependency()
@pytest.mark.asyncio
@pytest.mark.parametrize("path,expected", params_for_detail_raw())
async def test_parse_spell_detail(fake_parser, path, expected):
    """
    Тест парсинга данных детальной страницы
    :return:
    """

    data = await fake_parser.parse_detail_raw(path)
    assert data == expected


@pytest.mark.dependency(depends=[
    'test_parse_spell_list',
    'test_parse_spell_detail[tests/data/fake_countrip_detail.html-expected0]'
])
@pytest.mark.parametrize("data,file_name,rows_count,field,expected", params_for_csv_saving())
def test_save_to_csv(temp_dir, data, file_name, rows_count, field, expected):
    """
    Проверка сохранения данных в файл csv
    Актуально при успешном тесте парсинга списка и детальной
    :return:
    """

    file_path = Path(temp_dir, file_name)

    FileHelper.to_csv(data, file_path)
    data_from_file = FileHelper.read_csv(file_path)

    assert len(data_from_file) == rows_count
    assert data_from_file[0][field] == expected


def test_dividing_multilist(multilist):
    """
    Тест разделения данных мультисписка на отдельные записи
    """
    
    divided = Parser._divide(multilist, 'classes')
    assert len(divided) == 31
