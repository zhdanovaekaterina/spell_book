import os
import shutil
from pathlib import Path

import pytest

from src.parser.parser import Parser
from src.helpers.file_helper import FileHelper
from .mock import mock_get


@pytest.fixture()
def fake_parser(monkeypatch):
    """
    Отдает парсер с измененным методом get() для чтения данных из файла
    :return:
    """
    monkeypatch.setattr(Parser, "get", mock_get)
    return Parser()


@pytest.fixture(scope='module')
def temp_dir():
    """
    Создает директорию для хранения временных файлов и очищает ее после теста
    :return:
    """

    # Создать директорию для хранения временных файлов
    temp_dir_path = Path(Path.cwd(), 'tests', 'temp')
    if not os.path.isdir(temp_dir_path):
        os.mkdir(temp_dir_path)

    yield temp_dir_path

    # Очистить директорию с временными файлами
    shutil.rmtree(temp_dir_path)


@pytest.fixture(scope='module')
def multilist():
    """
    Читает из файла данные для очистки и возвращает их
    """

    path = Path(Path.cwd(), 'tests', 'data', 'fake_spell_to_class.csv')
    data = FileHelper.read_csv(path)
    
    return data
